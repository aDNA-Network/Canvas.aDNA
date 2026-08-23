"""Backcompat tests for the M-R2-02 dual-prompt protocol.

Authored at M-R2-02 S2 (campaign_canvasforge_review). Verifies the str
backcompat path through ``_coerce_prompt`` plus end-to-end forwarding via
the ImageClient Protocol. Spec authority:
``how/campaigns/campaign_canvasforge_review/missions/artifacts/m_r2_01_dual_prompt_protocol_spec.md``
§ 7.1 (ImagePrompt) · § 7.4 (Protocol upgrade with str backcompat).

Lives in ``canvas_comic/tests/`` (not ``canvas_core/tests/``) because the
backcompat surface is exercised end-to-end via comic-application
generators in production, and the test fixtures are aligned with the
F-38 ContextPack discipline.
"""

from __future__ import annotations

import os
import sys
import unittest
import warnings
from typing import Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from canvas_core.image_generation import (
    ImageClient,
    ImagePrompt,
    _coerce_prompt,
)


class _MockImageClient:
    """Minimal ImageClient Protocol conformant mock that records its inputs."""

    def __init__(self) -> None:
        self.last_prompt: Any = None
        self.calls: list[Any] = []

    def generate_image(
        self,
        prompt: ImagePrompt | str,
        output_path: str | None = None,
        style: str = "photo",
        aspect_ratio: str = "1:1",
        image_size: str = "2K",
        model: str = "ultra",
    ) -> dict[str, Any]:
        self.last_prompt = prompt
        self.calls.append(prompt)
        return {"success": True, "image_path": output_path or "<sink>"}


class TestStrBackcompat(unittest.TestCase):
    """str → ImagePrompt coercion with DeprecationWarning (spec § 7.4)."""

    def test_coerce_prompt_wraps_str_with_warning(self):
        """Passing a str triggers DeprecationWarning and returns ImagePrompt(text=...)."""
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            result = _coerce_prompt("hello world")
        self.assertIsInstance(result, ImagePrompt)
        self.assertEqual(result.text, "hello world")
        self.assertIsNone(result.mermaid_layout)
        self.assertEqual(result.aspect_ratio, "1:1")
        self.assertTrue(any(
            issubclass(w.category, DeprecationWarning)
            and "deprecated" in str(w.message).lower()
            and "v1.2" in str(w.message)
            for w in caught
        ))

    def test_coerce_prompt_passthrough_image_prompt(self):
        """Passing an ImagePrompt returns it identity-wise with no warning."""
        original = ImagePrompt(text="abc", mermaid_layout="x", aspect_ratio="3:4")
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            result = _coerce_prompt(original)
        self.assertIs(result, original)
        self.assertEqual(
            [w for w in caught if issubclass(w.category, DeprecationWarning)],
            [],
        )

    def test_protocol_str_path_works_via_mock_client(self):
        """A Protocol-conformant client receives whatever the caller passed; the
        coerce shim runs at the wiring boundary, not inside the client. This test
        documents that contract — Protocol implementers see the caller's argument
        verbatim, and the str path remains usable end-to-end through v1.2."""
        client: ImageClient = _MockImageClient()
        # str path
        result_str = client.generate_image(prompt="text-only")
        self.assertTrue(result_str["success"])
        self.assertEqual(client.last_prompt, "text-only")
        # ImagePrompt path
        ip = ImagePrompt(text="dual", mermaid_layout="layout", aspect_ratio="3:4")
        result_dual = client.generate_image(prompt=ip)
        self.assertTrue(result_dual["success"])
        self.assertIs(client.last_prompt, ip)


if __name__ == "__main__":
    unittest.main()
