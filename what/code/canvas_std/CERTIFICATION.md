# Certifying an aDNA Canvas Standard implementation

The **certification kit** lets any implementation of the aDNA Canvas Standard verify that it agrees with the
reference on a fixed corpus of golden canvases. "Conformant" means *testable*, not asserted.

## The corpus

`tests/fixtures/` holds **10 golden `.canvas` fixtures** and a `manifest.json`. Each manifest entry is a public
contract for one fixture:

| field | meaning |
|-------|---------|
| `path` | the fixture file |
| `declared_level` | the level the document declares (`core` / `extended` / `adna_native`) |
| `expected_valid` | whether the document is valid at its declared level |
| `expected_level_reached` | the highest level a conformant validator reaches (`null` if it fails Core) |
| `expected_ok` | whether the suite outcome is OK |
| `degrades_to` | the level the document degrades to after `strip` |
| `note` | what the fixture exercises |

The corpus spans all three levels and includes positive, boundary, and negative cases (a missing `toEnd:arrow`,
an out-of-enum shape, a bad `_reserved` level, an orphaned anchor, the leg-3 interaction overlay).

## Run the reference certification

```bash
pip install -e .          # install canvas_std (the reference implementation)
python certify.py         # human-readable report
python certify.py --json  # machine-readable report (for CI / attestation records)
```

A passing run prints `CERTIFIED: 10/10 fixtures agree with the corpus`, plus a per-level self-attestation (how
many fixtures exercise Core / Extended / aDNA-Native and how many your validator agrees on). Exit code is 0 on
success, 1 on any disagreement.

## Certify your own implementation

The manifest is the contract. An external implementation certifies itself by running **its own** validator over
the same fixtures and matching each entry's `expected_level_reached` + `expected_ok`:

1. For each fixture, run your validator with the fixture's `declared_level`.
2. Record the highest conformance level your validator reaches, and whether the outcome is OK.
3. Compare to `expected_level_reached` + `expected_ok`. All 10 must agree.

`certify.py` is the reference runner (it calls `canvas_std.validate_suite`); adapt it to call your validator, or
drive your own tool over the fixtures. The Core / Extended / aDNA-Native self-attestation is the claim you
publish: *"this implementation reaches and agrees on all corpus fixtures at level L."*

## What certification does and doesn't prove

- **Does:** your validator agrees with the reference on the level each golden fixture reaches, on validity, and
  on the degradation boundary — the observable conformance contract.
- **Doesn't:** exhaustively prove correctness on all inputs. The corpus is a curated set of the boundaries that
  matter; extend it (add a fixture + a manifest entry) when you find a case it misses — that is how the corpus grows.

The normative rules the corpus encodes live in [`../../specs/`](../../specs/README.md); the conformance-suite
spec is [`spec_conformance_suite.md`](../../specs/spec_conformance_suite.md).
