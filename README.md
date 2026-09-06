# AFRITOON

A code-first animation engine for short-form African relatable comedy.

## v0.1 — Scene Animation Engine

AFRITOON turns a small YAML scene definition into a vertical MP4 using procedural characters and FFmpeg.

### Current primitives

- 1080×1920 (9:16) output
- YAML scene definitions
- Timeline-based actions
- Procedural Tunde character
- Basic expressions and movement
- Procedural background
- FFmpeg MP4 encoding
- Smoke tests for scene/timeline logic

### Quick start

```bash
cd ~/AFRITOON
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
python render.py scenes/tunde_test.yaml
```

Output: `output/tunde_test.mp4`

## Architecture direction

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

The engine is intentionally specialized for fast, repeatable short-form comedy. We will add only primitives that make production faster: characters, reusable actions, expressions, camera movement, dialogue timing, music timing and asset-based characters.

## Development rule

**Build → render → watch → improve → publish.**

Do not turn AFRITOON into a generic animation suite before the content proves what is worth building.

## Music

Do not commit copyrighted songs to the repository. The renderer may accept user-supplied or appropriately licensed/platform-native audio during production.
