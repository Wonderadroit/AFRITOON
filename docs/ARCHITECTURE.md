# AFRITOON Architecture

## Purpose

AFRITOON is a specialized code-first renderer for short-form African relatable comedy.

The engine separates **what happens** from **how frames are rendered**.

## Pipeline

```text
Idea / Trend / Song
      ↓
Episode / Scene YAML
      ↓
Scene Director
      ↓
Character + Action State
      ↓
Frame Renderer
      ↓
FFmpeg
      ↓
9:16 MP4
```

## State model

A scene timeline produces a current action at time `t`. The renderer maps that action into character state such as position, bounce and expression. This keeps story timing declarative and makes future additions—camera events, dialogue, audio cues and reusable assets—possible without rewriting the renderer.

## Roadmap

- v0.1: procedural character + timeline + vertical MP4
- v0.2: multiple characters and scene composition
- v0.3: reusable action/pose library
- v0.4: asset-based characters and backgrounds
- v0.5: dialogue timing and mouth states
- v0.6: camera system
- v0.7: audio/music timing and beat cues
- v1.0: fast idea → scene → animation → audio → publish workflow
