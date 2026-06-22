"""Resolver-interface tests (spec_canvas_context_loading §5) — in-vault wikilink + federation descriptor."""

from __future__ import annotations

from canvas_context import UNRESOLVED, DefaultPathResolver, FederationDescriptor, LocalHandle, Ref


def test_wikilink_resolves_to_local_handle(tmp_path):
    (tmp_path / "spec_adna_canvas_standard.md").write_text("# spec")
    r = DefaultPathResolver(tmp_path)
    handle = r.resolve(Ref(form="wikilink", target="[[spec_adna_canvas_standard]]"))
    assert isinstance(handle, LocalHandle)
    assert handle.path.endswith("spec_adna_canvas_standard.md")


def test_wikilink_with_alias_and_anchor_resolves(tmp_path):
    (tmp_path / "doc.canvas").write_text("{}")
    r = DefaultPathResolver(tmp_path)
    handle = r.resolve(Ref(form="wikilink", target="[[doc#section|Display Name]]"))
    assert isinstance(handle, LocalHandle)
    assert handle.path.endswith("doc.canvas")


def test_missing_wikilink_is_unresolved(tmp_path):
    r = DefaultPathResolver(tmp_path)
    assert r.resolve(Ref(form="wikilink", target="[[does_not_exist]]")) is UNRESOLVED


def test_federation_ref_returns_descriptor_not_content(tmp_path):
    """Cross-vault refs are parsed into a descriptor and NEVER fetched (§5.2 / ADR-006)."""
    r = DefaultPathResolver(tmp_path)
    desc = r.resolve(Ref(form="federation_ref", target="lattice://other_vault/some_lattice/node7"))
    assert isinstance(desc, FederationDescriptor)
    assert desc.instance == "other_vault"
    assert desc.lattice == "some_lattice"
    assert desc.node == "node7"


def test_canvas_preferred_over_md_for_same_stem(tmp_path):
    (tmp_path / "thing.md").write_text("# md")
    (tmp_path / "thing.canvas").write_text("{}")
    r = DefaultPathResolver(tmp_path)
    handle = r.resolve(Ref(form="wikilink", target="[[thing]]"))
    assert isinstance(handle, LocalHandle)
    assert handle.path.endswith("thing.canvas")  # .canvas extension takes precedence
