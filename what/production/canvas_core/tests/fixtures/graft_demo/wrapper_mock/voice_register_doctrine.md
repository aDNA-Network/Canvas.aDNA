# Voice Register Doctrine — Science Stanley wrapper override

Voice registers R1-R12 are the operational vocabulary by which canvas
artifacts declare their narrative voice. Each register has an author
intent, a tonal range, and a permitted-content surface.

R11 (Patient's Voice) gating is the canonical substrate enforcement
point — wrappers declare where R11 may appear; substrate enforces
human approval before render.

## Wrapper-local override

This wrapper carries an additional editorial gloss that does not appear
in canonical: the SS brand uses R6 satirical-reportage as its default
register. R6 voice mappings live in `cc_presentation_voice_mapping.yaml`.
