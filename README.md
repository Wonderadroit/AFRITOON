# AFRITOON

A code-first animation engine for short-form African relatable comedy.

## Character system

AFRITOON now has a reusable recurring cast:

- **Tunde** — the confident mistake.
- **Seyi** — the deadpan human reaction button.
- **Mama** — the final boss of information.

The character system separates:

```text
CHARACTER ARTWORK
      ↓
CHARACTER ASSET CONTRACT
      ↓
POSE / EXPRESSION / EMOTION STATE
      ↓
INTERACTION / SCENE DIRECTOR
      ↓
LAYERED CHARACTER RIG
      ↓
9:16 FRAME / VIDEO
```

The canonical front masters are original human-looking SVG artwork. The
repository also contains a deterministic builder for the 16-layer rig contract
and a view policy that explicitly falls back to the front master when a
three-quarter or side master has not yet been authored.

## Character build

```bash
python tools/validate_characters.py
python tools/build_character_layers.py --character all
```

For PNG layers when CairoSVG is available:

```bash
python tools/build_character_layers.py --character all --png
```

The generated front layers are build artifacts. The SVG masters remain the
source of truth for appearance.

## Scene engine

AFRITOON turns scene data into short-form vertical animation.

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
character definitions, emotions, expressions, recurring interactions,
multi-character cast state, layered-rig primitives, SVG master rendering and
FFmpeg encoding.

## Development rule

**Build → render → watch → improve → publish.**

Do not turn AFRITOON into a generic animation suite before the content proves
what is worth building.

## Music

Do not commit copyrighted songs to the repository. The renderer may accept
user-supplied or appropriately licensed/platform-native audio during
production.
