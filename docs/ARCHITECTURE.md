# ITANRA Architecture

ITANRA is a specialized code-first storytelling and animation engine for short-form African relatable stories.

```text
Idea / Trend / Song
      ↓
Story + Emotional Beats
      ↓
Episode / Scene YAML
      ↓
Scene Director
      ↓
Character + Action + Performance State
      ↓
Voice / Audio Timing
      ↓
Frame Renderer
      ↓
FFmpeg
      ↓
9:16 MP4
```

The story layer describes **what happens and why**. The performance layer describes **how characters behave**. The renderer decides **how frames are drawn**. This separation lets ITANRA evolve the visual assets without rewriting story logic.

## Product boundary

ITANRA is not a general-purpose animation suite. It is optimized for repeatable short-form storytelling: recurring characters, emotional beats, dialogue, reactions, camera timing, audio and fast production iteration.

## Character architecture

```text
CHARACTER ARTWORK
      ↓
SEMANTIC ASSET LAYERS
      ↓
POSE / EXPRESSION / MOUTH
      ↓
PERFORMANCE
      ↓
SCENE COMPOSITION
      ↓
FRAME / VIDEO
```

Artwork and animation logic remain separate so the current human-looking SVG cast can later be replaced with upgraded production artwork without rebuilding the engine.

## Current roadmap

- foundation: reusable cast, semantic SVG artwork and vertical rendering
- performance: action, expression, mouth and character-specific motion
- dialogue: provider-independent voice contracts and measured audio timing
- scene intelligence: story beats, emotional state and camera intent
- production: repeatable idea → scene → animation → audio → publish workflow
