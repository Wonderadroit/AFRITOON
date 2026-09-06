# AFRITOON

A code-first animation engine for short-form African relatable comedy.

## Character system

AFRITOON has a reusable recurring cast:

- **Tunde** — the confident mistake.
- **Seyi** — the deadpan human reaction button.
- **Mama** — the final boss of information.

The production chain is:

```text
CHARACTER ARTWORK
      ↓
CHARACTER ASSET CONTRACT
      ↓
POSE + EXPRESSION + MOUTH STATE
      ↓
INTERACTION / SCENE DIRECTOR
      ↓
CHARACTER-SPECIFIC RENDERER
      ↓
9:16 FRAME
      ↓
FFMPEG
      ↓
MP4
```

The canonical front masters are original human-looking SVG artwork. Each
character is resolved independently; Seyi and Mama are never substituted with
Tunde. The view policy explicitly falls back to the front master when a genuine
three-quarter or side master has not yet been authored.

## Build character layers

```bash
python tools/validate_characters.py
python tools/build_character_layers.py --character all
```

To also create raster PNG layers when CairoSVG is installed:

```bash
python tools/build_character_layers.py --character all --png
```

Generated layers are build artifacts. SVG masters remain the source of truth.

## Render a frame

```bash
python tools/render_frame.py scenes/trio_showcase.yaml --time 3.2 --output output/frame.png
```

## Render a scene to MP4

Requires FFmpeg. Audio is optional and should be user-supplied, licensed, or
platform-native rather than committed to the repository.

```bash
python tools/render_scene.py scenes/trio_showcase.yaml --output output/trio.mp4
```

With audio:

```bash
python tools/render_scene.py scenes/trio_showcase.yaml --output output/trio.mp4 --audio audio/trend.mp3
```

## Scene engine

```text
IDEA / TREND / SONG
        ↓
   SCENE DEFINITION
        ↓
   SCENE DIRECTOR
        ↓
   ANIMATION ENGINE
        ↓
      MP4 9:16
```

Current foundations include 1080×1920 output, YAML scenes, timeline actions,
character definitions, emotions, expressions, independent mouth states,
recurring interactions, multi-character cast state, layered-rig primitives,
SVG master rendering and FFmpeg encoding.

## Development rule

**Build → render → watch → improve → publish.**

Do not turn AFRITOON into a generic animation suite before the content proves
what is worth building.

## Music

Do not commit copyrighted songs to the repository. The renderer accepts
user-supplied or appropriately licensed/platform-native audio during
production.
