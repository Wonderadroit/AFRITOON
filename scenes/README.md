# ITANRA Scenes

A scene describes timing and composition. Character definitions remain reusable and independent.

## Cast flow

`scene YAML → interaction cues → CastScene.state_at(t) → character states → cast renderer → frame/video`

The renderer can use the canonical human-looking SVG artwork while preserving the scene and interaction logic.

## Current showcase

`trio_showcase.yaml` demonstrates the recurring Tunde/Seyi/Mama chemistry:

- Tunde drives the situation.
- Seyi reacts before the punchline.
- Mama arrives with authority.
- Tunde freezes.
- Seyi and Mama deliver the reaction beat.
