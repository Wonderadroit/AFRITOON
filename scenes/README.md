# AFRITOON Scenes

A scene describes timing and composition. Character definitions remain reusable and independent.

## Cast flow

`scene YAML → interaction cues → CastScene.state_at(t) → character states → cast renderer → frame/video`

The first cast renderer uses the existing procedural renderer as a compatibility fallback. This is deliberate: the production artwork can be introduced without rewriting scene direction or interaction timing.

## Current showcase

`trio_showcase.yaml` demonstrates the recurring Tunde/Seyi/Mama chemistry:

- Tunde drives the situation.
- Seyi reacts before the punchline.
- Mama arrives with authority.
- Tunde freezes.
- Seyi and Mama deliver the reaction beat.
