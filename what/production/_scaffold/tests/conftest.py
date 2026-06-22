"""Shared fixtures.

TODO(clone): build a domain input fixture + a ``doc`` fixture = ``build(<input>)``, mirroring an exemplar
(``what/production/diagram_generator/tests/conftest.py``). Until then the ``doc`` fixture skips.
"""

from __future__ import annotations

import pytest


@pytest.fixture
def doc() -> dict:
    pytest.skip("scaffold template — clone and implement the `doc` fixture")
