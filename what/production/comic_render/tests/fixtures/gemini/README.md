# Gemini API contract fixtures (Halftone H3)

Unlike the `comfy/` fixtures — which record raw HTTP bodies — the gemini backend speaks through the
`google-genai` SDK, so the contract is a *call shape* and a *response shape*, not a wire format.
`api_surface_20260809.json` is therefore a **dated capture of the live service**, and the tests
build fake SDK response objects matching the shape it records.

**Everything in that file was read from the service.** The aspect menu in particular was not copied
from documentation: sending a deliberately invalid ratio returns a 400 that enumerates the valid
set. That costs nothing (it is rejected at validation, before generation) and it cannot silently
drift the way a hand-maintained list does.

## Re-verifying

Run this before any run that spends real money. It is free.

```python
from google import genai
from google.genai import types
c = genai.Client()                                   # reads GEMINI_API_KEY from the environment

# 1. what image models exist right now
print(sorted(m.name for m in c.models.list() if "image" in m.name))

# 2. the aspect menu, straight from the service
try:
    c.models.generate_content(
        model="gemini-3-pro-image", contents="probe",
        config=types.GenerateContentConfig(
            response_modalities=["Image"],
            image_config=types.ImageConfig(aspect_ratio="7:13", image_size="2K")))
except Exception as e:
    print(e)                                          # the 400 lists the valid ratios
```

If the menu changed, update `backends/gemini.py::SUPPORTED_ASPECT_RATIOS` — plan snaps panel
geometry against it, so a stale menu means either a refused request or a worse-fitting crop.

If pricing changed, update `PRICING` **and** `PRICING_VERIFIED_ON`. That map feeds the manifest
budget cap; a stale number there is a real overspend, not a documentation nit.

## Known state at capture (2026-08-09)

- **Imagen 4 is deprecated, shutdown 2026-08-17.** The `adna_lab` precedent client this backend was
  adapted from targets it. Do not "restore" the `generate_images` path.
- **Billing was blocked**: `429 RESOURCE_EXHAUSTED — prepayment credits are depleted`, account-wide.
  The credential was valid (the 400 above proves auth succeeded). H3's live run is gated on the
  operator topping up credits, not on anything in this package.
