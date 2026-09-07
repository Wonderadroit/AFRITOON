# ITANRA Visual Production Bible

## Purpose

The first full NEPA render proved the story/performance pipeline but exposed a visual-quality gap: technically valid vector characters can still look like a rough AI prototype. ITANRA therefore treats visual quality as a production gate, not a cosmetic afterthought.

## Visual target

ITANRA's recurring cast must read as original, clean 2D animation artwork at 1080x1920 phone output.

### Non-negotiables

- Character identity must remain stable across scenes.
- Silhouettes must be recognizable without facial detail.
- Faces must have deliberate eye, brow, nose and mouth construction.
- Line weight must remain controlled at phone-sized output.
- Clothing and hair must provide character distinction.
- Lighting must communicate important story events.
- Characters must sit in an environment rather than float on a flat canvas.
- Contact shadows must ground characters.
- Background detail must support the story and never overpower acting.
- Comedy comes from acting, timing, staging and writing—not distorted ethnic stereotypes.
- AI-generated assets may assist production, but the canonical runtime asset must be deterministic and editable.

## Production asset rule

Concept art is reference material. Canonical SVG masters are the production source of truth. Masters are separated into semantic layers and are never regenerated per frame.

## Scene rule

Every production scene should have:

1. layout/background
2. character staging
3. character acting
4. lighting state
5. camera framing
6. contact/depth cues
7. final encoding

## Quality gate

A scene is not production-ready because tests pass. It must pass both:

- semantic/runtime validation
- visual review of the rendered video

The visual review asks:

- Does it look like a designed animation rather than an AI image sequence?
- Do characters remain on-model?
- Are poses readable?
- Are expressions readable at phone size?
- Does the environment establish place and depth?
- Does lighting change when the story changes the world?
- Do characters feel planted on the floor?
- Does camera composition direct attention to the active beat?

## Performance rule

Development rendering must use caching and reusable rasterization. Canonical artwork should be rasterized only when its semantic state changes. Final output remains 1080x1920 at the configured frame rate.
