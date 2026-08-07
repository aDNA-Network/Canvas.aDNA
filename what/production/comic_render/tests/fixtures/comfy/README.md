# ComfyUI HTTP contract fixtures (Halftone H4)

Recorded-shape responses for the four endpoints the refine seam speaks. **These files are the
contract with Vulcan (ComfyUI.aDNA)** — when the `comic_panel_refine` workflow lands upstream,
diff a real capture against these and the delta *is* the integration work.

| File | Endpoint | Notes |
|------|----------|-------|
| `system_stats.json` | `GET /system_stats` | health probe / circuit-breaker |
| `upload_image.json` | `POST /upload/image` | multipart seed upload → `{name, subfolder, type}` |
| `prompt.json` | `POST /prompt` | workflow submit → `{prompt_id}` |
| `history.json` | `GET /history/{id}` | completion → `outputs.<node>.images[]` |
| `comic_panel_refine.json` | *(template)* | the img2img graph **shape asked of Vulcan** — the fallback built-in graph in `canvas_core.comfyforge_adapter._build_img2img_workflow` is its structural twin |

`comic_panel_refine.json` is a Canvas-side *request shape*, not a copy of an upstream artifact:
ComfyUI.aDNA owns the real workflow. Patch convention (what the adapter relies on): first
`CLIPTextEncode` is positive, second is negative, `LoadImage` takes the uploaded seed, `KSampler`
takes `denoise` + `seed`.
