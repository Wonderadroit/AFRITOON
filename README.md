# ITANRA

**ITANRA** is a code-first storytelling and animation engine for short-form African relatable stories.

> **Stories that feel like home.**

ITANRA is not intended to become a generic animation suite. It is a specialized production system that turns story intent into repeatable animated short-form content.

## The universe

The first recurring cast is:

- **Tunde** — the confident mistake.
- **Seyi** — the deadpan human reaction button.
- **Mama** — the final boss of information.

The goal is not photorealism. The target is recognizable, expressive, human-looking stylized 2D characters whose identity survives across episodes.

## Production chain

```text
IDEA / TREND / STORY
        ↓
STORY + EMOTIONAL BEATS
        ↓
CHARACTER STATE
        ↓
DIALOGUE / VOICE
        ↓
POSE + EXPRESSION + MOUTH
        ↓
SCENE DIRECTOR
        ↓
CHARACTER-SPECIFIC RENDERER
        ↓
9:16 FRAME
        ↓
FFMPEG
        ↓
MP4 SHORT
```

The canonical front masters are original human-looking SVG artwork. Each character is resolved independently; Seyi and Mama are never substituted with Tunde. The view policy falls back to the front master when a genuine three-quarter or side master has not yet been authored.

## Character layers

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

Requires FFmpeg. Audio is optional and should be user-supplied, licensed, or platform-native rather than committed to the repository.

```bash
python tools/render_scene.py scenes/trio_showcase.yaml --output output/trio.mp4
```

With audio:

```bash
python tools/render_scene.py scenes/trio_showcase.yaml --output output/trio.mp4 --audio audio/trend.mp3
```

## Story engine

```text
IDEA / TREND / SONG
        ↓
STORY DIRECTOR
        ↓
EMOTIONAL + CHARACTER STATE
        ↓
SCENE DIRECTOR
        ↓
ANIMATION ENGINE
        ↓
VOICE / AUDIO TIMELINE
        ↓
9:16 MP4
```

Current foundations include 1080×1920 output, YAML scenes, timeline actions, character definitions, emotions, expressions, independent mouth states, recurring interactions, multi-character cast state, layered-rig primitives, SVG master rendering and FFmpeg encoding.

## Development rule

**Build → render → watch → improve → publish.**

Do not turn ITANRA into a generic animation suite before the content proves what is worth building.

## Music

Do not commit copyrighted songs to the repository. The renderer accepts user-supplied or appropriately licensed/platform-native audio during production.

## Brand

- Studio / product: **ITANRA**
- Engine: **ITANRA Engine**
- First recurring universe: **Tunde, Seyi & Mama**
- Positioning: **Stories that feel like home.**
