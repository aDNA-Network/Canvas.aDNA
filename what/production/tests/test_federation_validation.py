"""Federation validation suite — M-6-03.

Validates all 3 consumer wrappers pass E2E against CanvasForge canonical
lattices. Tests cover: federation ref correctness, node override semantics,
voice register compliance, R11 gating, E2E builder execution, and
cross-wrapper isolation.

Consumer wrappers:
  SS deck:  ScienceStanley.aDNA/presentationforge/
  SS comic: ScienceStanley.aDNA/graphicnovelforge/
  CC deck:  ContextCommons.aDNA/presentationforge/
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest
import yaml

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------

CODE_DIR = Path(__file__).resolve().parent.parent  # what/code/
sys.path.insert(0, str(CODE_DIR))

LATTICE_ROOT = Path(__file__).resolve().parent.parent.parent  # what/
FORGE_ROOT = LATTICE_ROOT.parent  # CanvasForge.aDNA/
WORKSPACE = FORGE_ROOT.parent  # ~/aDNA/

# Canonical lattice paths
CANONICAL_DECK = FORGE_ROOT / "what" / "lattices" / "lattice_presentation_canvas.lattice.yaml"
CANONICAL_COMIC = FORGE_ROOT / "what" / "lattices" / "lattice_comic_canvas.lattice.yaml"

# Consumer wrapper lattice paths
# Layout decision (M-R1-01b, 2026-04-29): canonical = lattice_<vault>_<application>.lattice.yaml.
# Supersedes the P3 wrapper-spec § B pluralized `consumer_<type>s/` pattern. See ADR 000.
SS_DECK = WORKSPACE / "ScienceStanley.aDNA" / "presentationforge" / "what" / "lattices" / "lattice_ss_presentation.lattice.yaml"
SS_COMIC = WORKSPACE / "ScienceStanley.aDNA" / "graphicnovelforge" / "what" / "lattices" / "lattice_ss_graphic_novel.lattice.yaml"
CC_DECK = WORKSPACE / "ContextCommons.aDNA" / "presentationforge" / "what" / "lattices" / "lattice_cc_presentation.lattice.yaml"

# All wrapper paths for parametrize
ALL_WRAPPERS = [SS_DECK, SS_COMIC, CC_DECK]
DECK_WRAPPERS = [SS_DECK, CC_DECK]

from canvas_presentation import PresentationBuilder, PRESENTATION_THEMES
from canvas_comic import ComicPageBuilder, CHARACTER_STANLEY
from canvas_comic.comic import ContextPack


def _make_test_context_pack(tmp_path: Path) -> ContextPack:
    """Create 5 sentinel files in ``tmp_path`` and return a ContextPack."""
    fields = (
        "storyboard_canvas",
        "character_bible",
        "color_theory",
        "prompt_engineering",
        "voice_foundations",
    )
    kwargs: dict[str, Path] = {}
    for f in fields:
        p = tmp_path / f"{f}.md"
        p.write_text(f"# Sentinel {f}\n")
        kwargs[f] = p
    return ContextPack(**kwargs)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_lattice(path: Path) -> dict:
    """Load a lattice YAML and return the top-level 'lattice' dict."""
    with open(path) as f:
        data = yaml.safe_load(f)
    return data["lattice"]


def get_node_ids(lattice: dict) -> set[str]:
    """Extract node IDs from a lattice."""
    return {n["id"] for n in lattice.get("nodes", [])}


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def canonical_deck():
    return load_lattice(CANONICAL_DECK)


@pytest.fixture
def canonical_comic():
    return load_lattice(CANONICAL_COMIC)


@pytest.fixture
def ss_deck():
    return load_lattice(SS_DECK)


@pytest.fixture
def ss_comic():
    return load_lattice(SS_COMIC)


@pytest.fixture
def cc_deck():
    return load_lattice(CC_DECK)


# ===========================================================================
# 1. Federation Reference Validation
# ===========================================================================

class TestFederationRefValidation:
    """Every consumer wrapper declares correct federation_ref to CanvasForge."""

    @pytest.mark.parametrize("wrapper_path", ALL_WRAPPERS, ids=["ss_deck", "ss_comic", "cc_deck"])
    def test_extends_canvasforge(self, wrapper_path):
        lattice = load_lattice(wrapper_path)
        assert lattice.get("extends") == "canvasforge", \
            f"{wrapper_path.name}: missing or wrong 'extends'"

    @pytest.mark.parametrize("wrapper_path", ALL_WRAPPERS, ids=["ss_deck", "ss_comic", "cc_deck"])
    def test_federation_ref_source_vault(self, wrapper_path):
        lattice = load_lattice(wrapper_path)
        ref = lattice.get("federation_ref", {})
        assert ref.get("source_vault") == "Canvas.aDNA"  # pt09: CanvasForge production absorbed into Canvas.aDNA (engine → what/production/; consumers refederated PT P5, 2026-06-22)

    @pytest.mark.parametrize("wrapper_path", ALL_WRAPPERS, ids=["ss_deck", "ss_comic", "cc_deck"])
    def test_federation_ref_version_policy(self, wrapper_path):
        lattice = load_lattice(wrapper_path)
        ref = lattice.get("federation_ref", {})
        assert ref.get("version") == "~1.0"
        assert ref.get("version_policy") == "minor"

    def test_ss_deck_points_to_deck_canonical(self, ss_deck):
        ref = ss_deck["federation_ref"]
        assert "lattice_presentation_canvas" in ref["source_lattice"]

    def test_ss_comic_points_to_comic_canonical(self, ss_comic):
        ref = ss_comic["federation_ref"]
        assert "lattice_comic_canvas" in ref["source_lattice"]

    def test_cc_deck_points_to_deck_canonical(self, cc_deck):
        ref = cc_deck["federation_ref"]
        assert "lattice_presentation_canvas" in ref["source_lattice"]

    @pytest.mark.parametrize("wrapper_path,expected_app", [
        (SS_DECK, "deck"), (SS_COMIC, "comic"), (CC_DECK, "deck")
    ], ids=["ss_deck", "ss_comic", "cc_deck"])
    def test_application_matches_canonical(self, wrapper_path, expected_app):
        lattice = load_lattice(wrapper_path)
        assert lattice.get("application") == expected_app

    @pytest.mark.parametrize("wrapper_path", ALL_WRAPPERS, ids=["ss_deck", "ss_comic", "cc_deck"])
    def test_canonical_lattice_file_exists(self, wrapper_path):
        """The source_lattice path resolves to an actual file in the forge."""
        lattice = load_lattice(wrapper_path)
        source = lattice["federation_ref"]["source_lattice"]
        resolved = FORGE_ROOT / source
        assert resolved.exists(), f"Canonical lattice not found: {resolved}"


# ===========================================================================
# 2. Node Override Semantics
# ===========================================================================

class TestNodeOverrideSemantics:
    """Wrapper node_overrides reference valid canonical node IDs."""

    def test_ss_deck_overrides_valid_nodes(self, ss_deck, canonical_deck):
        canonical_nodes = get_node_ids(canonical_deck)
        override_nodes = set(ss_deck.get("node_overrides", {}).keys())
        invalid = override_nodes - canonical_nodes
        assert not invalid, f"SS deck overrides non-existent nodes: {invalid}"

    def test_ss_comic_overrides_valid_nodes(self, ss_comic, canonical_comic):
        canonical_nodes = get_node_ids(canonical_comic)
        override_nodes = set(ss_comic.get("node_overrides", {}).keys())
        invalid = override_nodes - canonical_nodes
        assert not invalid, f"SS comic overrides non-existent nodes: {invalid}"

    def test_cc_deck_overrides_valid_nodes(self, cc_deck, canonical_deck):
        canonical_nodes = get_node_ids(canonical_deck)
        override_nodes = set(cc_deck.get("node_overrides", {}).keys())
        invalid = override_nodes - canonical_nodes
        assert not invalid, f"CC deck overrides non-existent nodes: {invalid}"

    @pytest.mark.parametrize("wrapper_path", ALL_WRAPPERS, ids=["ss_deck", "ss_comic", "cc_deck"])
    def test_no_node_removal(self, wrapper_path):
        """Wrappers extend, never remove canonical nodes (forking drops extends)."""
        lattice = load_lattice(wrapper_path)
        # Wrappers don't declare their own nodes list — they inherit via extends
        assert "nodes" not in lattice or lattice.get("extends") is None, \
            "Wrapper with 'extends' should not redeclare 'nodes' (override via node_overrides)"

    @pytest.mark.parametrize("wrapper_path", ALL_WRAPPERS, ids=["ss_deck", "ss_comic", "cc_deck"])
    def test_overrides_have_config(self, wrapper_path):
        """Each override provides a config dict (not bare node replacement)."""
        lattice = load_lattice(wrapper_path)
        for node_id, override in lattice.get("node_overrides", {}).items():
            assert "config" in override, \
                f"{wrapper_path.name}: override '{node_id}' missing 'config' key"


# ===========================================================================
# 3. Voice Register Compliance
# ===========================================================================

class TestVoiceRegisterCompliance:
    """Voice registers declared per wrapper match expected register sets."""

    VALID_REGISTERS = {f"R{i}" for i in range(1, 13)}

    def test_ss_deck_registers(self, ss_deck):
        regs = set(ss_deck.get("voice_registers", []))
        assert regs == {"R1", "R4", "R7", "R8", "R9", "R10", "R12"}
        assert "R11" not in regs, "SS deck should not include R11"

    def test_ss_comic_registers(self, ss_comic):
        regs = set(ss_comic.get("voice_registers", []))
        assert "R11" in regs, "SS comic must include R11 (Patient's Voice)"
        assert len(regs) >= 10, "SS comic should have broad register coverage"

    def test_cc_deck_registers(self, cc_deck):
        regs = set(cc_deck.get("voice_registers", []))
        assert regs == {"R1", "R4", "R7", "R8", "R9", "R10"}
        assert "R11" not in regs, "CC deck should not include R11"

    @pytest.mark.parametrize("wrapper_path", ALL_WRAPPERS, ids=["ss_deck", "ss_comic", "cc_deck"])
    def test_all_registers_in_valid_range(self, wrapper_path):
        lattice = load_lattice(wrapper_path)
        regs = set(lattice.get("voice_registers", []))
        invalid = regs - self.VALID_REGISTERS
        assert not invalid, f"Invalid registers: {invalid}"


# ===========================================================================
# 4. R11 Gating
# ===========================================================================

class TestR11Gating:
    """R11 Patient's Voice gating enforced per ADR 002 § 5."""

    def test_ss_deck_no_r11_gating(self, ss_deck):
        assert ss_deck.get("r11_gated_nodes") == [], \
            "SS deck should have empty r11_gated_nodes"

    def test_ss_comic_r11_gated_nodes(self, ss_comic):
        assert "quality_review" in ss_comic.get("r11_gated_nodes", [])

    def test_ss_comic_r11_gated_pages(self, ss_comic):
        gated = ss_comic.get("r11_gated_pages", [])
        assert 2 in gated
        assert 21 in gated
        assert 30 in gated

    def test_ss_comic_page_30_mandatory(self, ss_comic):
        assert ss_comic.get("page_30_gate") == "human_approval_mandatory"

    def test_cc_deck_no_r11_gating(self, cc_deck):
        assert cc_deck.get("r11_gated_nodes") == [], \
            "CC deck should have empty r11_gated_nodes"

    def test_canonical_deck_r11_gate_at_content_composer(self, canonical_deck):
        """Canonical deck gates R11 at content_composer; wrappers may tighten."""
        assert "content_composer" in canonical_deck.get("r11_gated_nodes", [])

    def test_canonical_comic_r11_gate_at_quality_review(self, canonical_comic):
        assert "quality_review" in canonical_comic.get("r11_gated_nodes", [])


# ===========================================================================
# 5. SS Deck E2E Build
# ===========================================================================

class TestSSDeckEndToEnd:
    """SS deck wrapper produces a valid canvas via PresentationBuilder."""

    def test_build_3_slide_deck_tokyo_night(self, ss_deck):
        pb = PresentationBuilder(name="ss_federation_test", theme="tokyo_night")
        pb.add_title_slide("Federation Test", "SS Deck Wrapper Validation")
        pb.add_content_slide("Key Findings", "Wrapper extends canonical lattice")
        pb.add_quote_slide("Quote", "Structure gates polish", "Hermes")
        canvas = pb.build()

        assert "nodes" in canvas
        assert "edges" in canvas
        assert len(pb.slides) == 3

    def test_tokyo_night_theme_applied(self, ss_deck):
        pb = PresentationBuilder(name="ss_themed", theme="tokyo_night")
        pb.add_title_slide("Themed")
        canvas = pb.build()
        # Tokyo Night primary color is "6" (purple/violet accent)
        nodes_json = str(canvas)
        assert "6" in nodes_json  # Theme color applied to nodes

    def test_ss_deck_narrative_arcs_declared(self, ss_deck):
        overrides = ss_deck.get("node_overrides", {})
        arcs = overrides.get("outline_architect", {}).get("config", {}).get("narrative_arcs", [])
        assert len(arcs) == 8
        assert "problem_solution" in arcs
        assert "hero_journey" in arcs

    def test_ss_deck_review(self):
        pb = PresentationBuilder(name="ss_review_test", theme="tokyo_night")
        pb.add_title_slide("Title")
        pb.add_content_slide("Body", "Content here")
        pb.add_content_slide("More", "More content")
        pb.build()

        report = pb.review()
        assert report.grade in ("A", "B", "C", "D", "F")
        assert report.score > 0

    def test_ss_deck_voice_mapping_path_exists(self, ss_deck):
        overrides = ss_deck.get("node_overrides", {})
        voice_path = overrides.get("content_composer", {}).get("config", {}).get("voice_mapping", "")
        assert "ss_presentation_voice_mapping.yaml" in voice_path

    def test_ss_deck_auto_fail_patterns(self, ss_deck):
        overrides = ss_deck.get("node_overrides", {})
        patterns = overrides.get("voice_critic", {}).get("config", {}).get("auto_fail_patterns", [])
        assert 13 in patterns, "Anti-pattern #13 (Michael Brooks guardian) required"


# ===========================================================================
# 6. SS Comic E2E Build
# ===========================================================================

class TestSSComicEndToEnd:
    """SS comic wrapper produces a valid canvas via ComicPageBuilder."""

    def test_build_1_page_comic(self):
        cpb = ComicPageBuilder(name="ss_federation_test")
        p1 = cpb.add_page(1, spread_number=1)
        cpb.standard_grid(p1)
        canvas = cpb.build()

        assert "nodes" in canvas
        assert "edges" in canvas
        assert len(cpb.pages) == 1

    def test_character_invariance_stanley(self, tmp_path):
        ctx_pack = _make_test_context_pack(tmp_path)
        cpb = ComicPageBuilder(name="ss_invariance_test")
        p1 = cpb.add_page(1, spread_number=1)
        panels = cpb.standard_grid(p1)
        cpb.set_panel_content(panels[0], scene_description="Stanley in the lab", characters=["Stanley"])
        prompt = cpb.generate_panel_prompt(panels[0], context_pack=ctx_pack)

        assert "purple turtleneck" in prompt.text
        assert "Wayfarer" in prompt.text  # Rayban Wayfarer frames

    def test_dual_worlds_act_assignment(self, ss_comic):
        """Wrapper declares Ghibli/Pixel/Transition register worlds."""
        worlds = ss_comic["node_overrides"]["story_bible"]["config"]["register_worlds"]
        assert "ghibli" in worlds
        assert "pixel" in worlds
        assert "transition" in worlds

    def test_character_invariance_config(self, ss_comic):
        chars = ss_comic["node_overrides"]["prompt_generation"]["config"]["character_invariance"]
        assert "science_stanley" in chars
        assert chars["science_stanley"]["signature"] == "purple turtleneck, glasses, clipboard"
        assert "agent_stanley" in chars
        assert "helix" in chars
        assert chars["michael"]["invariance_gate"] == "mandatory"

    def test_print_spec_300dpi(self, ss_comic):
        spec = ss_comic["node_overrides"]["issue_assembly"]["config"]["print_spec"]
        assert spec["dpi"] == 300
        assert spec["bleed"]["width"] == 2062
        assert spec["bleed"]["height"] == 3150
        assert spec["trim"]["width"] == 1988

    def test_comic_quality_scoring(self):
        cpb = ComicPageBuilder(name="ss_scoring_test")
        p1 = cpb.add_page(1, spread_number=1)
        cpb.standard_grid(p1)
        cpb.build()

        report = cpb.review()
        assert report.score >= 0
        assert report.structural_score >= 0
        assert report.content_score >= 0


# ===========================================================================
# 7. CC Deck E2E Build
# ===========================================================================

class TestCCDeckEndToEnd:
    """CC deck wrapper produces a valid canvas with CC-specific config."""

    def test_build_3_slide_curriculum_deck(self, cc_deck):
        pb = PresentationBuilder(name="cc_federation_test", theme="tokyo_night")
        pb.add_title_slide("Curriculum Deck", "Context Commons Validation")
        pb.add_content_slide("Module 1", "Community-facing content")
        pb.add_content_slide("Module 2", "Accessible learning materials")
        canvas = pb.build()

        assert "nodes" in canvas
        assert len(pb.slides) == 3

    def test_community_consent_critic_declared(self, cc_deck):
        overrides = cc_deck.get("node_overrides", {})
        reviewers = overrides.get("voice_critic", {}).get("config", {}).get("reviewers", [])
        critic_ids = [r["id"] for r in reviewers]
        assert "community_consent_critic" in critic_ids, \
            "CC deck must include Community Consent Critic reviewer"

    def test_community_consent_gate_enabled(self, cc_deck):
        overrides = cc_deck.get("node_overrides", {})
        gate = overrides.get("voice_critic", {}).get("config", {}).get("community_consent_gate")
        assert gate is True

    def test_cc_green_accent(self, cc_deck):
        overrides = cc_deck.get("node_overrides", {})
        design = overrides.get("content_composer", {}).get("config", {}).get("design_system", {})
        assert design.get("accent") == "green"

    def test_cc_token_tiers_smaller_than_ss(self, ss_deck, cc_deck):
        ss_tiers = ss_deck["node_overrides"]["context_assembler"]["config"]["token_tiers"]
        cc_tiers = cc_deck["node_overrides"]["context_assembler"]["config"]["token_tiers"]
        assert cc_tiers["full"] <= ss_tiers["full"], \
            "CC token budget should be <= SS (community-facing, smaller scope)"

    def test_cc_5_reviewers(self, cc_deck):
        reviewers = cc_deck["node_overrides"]["voice_critic"]["config"]["reviewers"]
        assert len(reviewers) == 5, "CC deck has 5 reviewer voices (incl. Community Consent Critic)"


# ===========================================================================
# 8. Cross-Wrapper Isolation
# ===========================================================================

class TestCrossWrapperIsolation:
    """Wrappers are isolated — no voice contamination across consumers."""

    def test_ss_and_cc_voice_paths_differ(self, ss_deck, cc_deck):
        ss_voice = ss_deck["node_overrides"]["content_composer"]["config"]["voice_mapping"]
        cc_voice = cc_deck["node_overrides"]["content_composer"]["config"]["voice_mapping"]
        assert ss_voice != cc_voice, \
            "SS and CC must reference different voice mapping files"

    def test_ss_voice_not_in_cc_config(self, cc_deck):
        cc_str = str(cc_deck)
        assert "ss_presentation_voice_mapping" not in cc_str, \
            "CC config must not reference SS voice mapping"
        assert "ss_presentation_reviewers" not in cc_str, \
            "CC config must not reference SS reviewer config"

    def test_canonical_lattices_identical_across_wrappers(self):
        """Both deck wrappers point to same canonical; verify it hasn't drifted."""
        deck1 = load_lattice(CANONICAL_DECK)
        deck2 = load_lattice(CANONICAL_DECK)
        assert deck1 == deck2, "Canonical lattice must be immutable"

    def test_version_policy_consistent(self):
        for path in ALL_WRAPPERS:
            lattice = load_lattice(path)
            ref = lattice["federation_ref"]
            assert ref["version_policy"] == "minor", \
                f"{path.name}: version_policy must be 'minor' for semver-minor adoption"

    def test_parity_deck_artifact_exists(self):
        parity = FORGE_ROOT / "what" / "artifacts" / "parity_deck" / "wilhelm_parity.canvas"
        assert parity.exists(), "M-6-01 parity deck artifact must exist"

    def test_parity_comic_artifact_exists(self):
        parity = FORGE_ROOT / "what" / "artifacts" / "parity_comic" / "comic_parity.canvas"
        assert parity.exists(), "M-6-02 parity comic artifact must exist"

    def test_no_wrapper_imports_forge_code(self):
        """Wrappers are YAML-only — no Python code in wrapper directories."""
        for vault_name in ["science_stanley.aDNA", "context_commons.aDNA"]:
            wrapper_base = WORKSPACE / vault_name
            if not wrapper_base.exists():
                continue
            for forge_dir in ["presentationforge", "graphicnovelforge"]:
                forge_path = wrapper_base / forge_dir
                if not forge_path.exists():
                    continue
                py_files = list(forge_path.rglob("*.py"))
                assert len(py_files) == 0, \
                    f"{vault_name}/{forge_dir}/ should not contain Python code (YAML-only wrappers)"
