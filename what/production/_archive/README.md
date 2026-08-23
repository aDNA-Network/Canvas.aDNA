# what/production/_archive/ — in-vault archive shelf (SO-7)

Created 2026-08-22 at the Halftone H6 re-open, executing the archive step **ADR-009** authorized
("reader-only freeze now, archive after H3" — H3 rendered 2026-08-10, eye-gate PASSED 2026-08-13,
print E2E validated the trim/bleed lineage: 2062×3150 pages, 0 DPI warnings, real ICC CMYK).

**Not collected by pytest** (`pytest.ini: norecursedirs = _archive`). Nothing here is on any
production path. Archive-never-delete: history preserved in git; a later Hestia-driven move to
`Archive.aDNA` is possible but not required.

| Entry | What | Provenance |
|---|---|---|
| `canvas_comic/` | The legacy CanvasForge comic engine (~1150 LOC + 99 tests). Frozen at ADR-009; archived here with its tests (the geometry regression net they provided was discharged by H3/H6 real-pixel evidence). | CanvasForge lineage → PT-P5 relocation → ADR-009 |
| `mvp_comic_demo.py` | Legacy demo driving `canvas_comic` end-to-end. | CanvasForge `demos/` |
| `tests_excised_legacy_paths.py` | Test methods excised from live suites because their only subject was the archived engine: 5 from `canvas_core/tests/test_image_generation.py` (legacy panel-side `ImagenWiring` paths — `build_panel_selection_canvas` / `resolve_panel_from_surviving_files` / `resolve_panel_with_choice`), 1 from `test_generation_mode_independence.py`, 3 from `tests/test_federation_validation.py` (legacy SS comic-wrapper E2E builds). Preserved verbatim as records, not runnable doctrine. | Excised 2026-08-22 |

**Census correction recorded at excision (F-H6RE-1):** ADR-009 stated "other live importers:
exactly one" (`test_federation_validation.py:50`). Measured at archive time: **four** files imported
`canvas_comic` — that one, plus `canvas_core/tests/test_image_generation.py`,
`canvas_core/tests/test_generation_mode_independence.py`, and `demos/mvp_comic_demo.py`.
All four dispositioned above. The legacy panel-side `ImagenWiring` methods in
`canvas_core/image_generation.py` now have no direct test coverage and no live caller
(live `comic_render` uses only `generate_variants`) — flagged as deprecation candidates for the
successor campaign.
