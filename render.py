# AFRITOON

A code-first animation engine for short-form African relatable comedy.

## v0.1

The first vertical-video prototype provides:

- 1080x1920 (9:16) rendering
- YAML-driven scenes
- Procedural characters
- Multiple actions and expressions
- Procedural backgrounds
- MP4 output through FFmpeg

## Quick start

```bash
cd ~/AFRITOON
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python render.py scenes/tunde_test.yaml
```

The first test renders to `output/tunde_test.mp4`.

## Direction

AFRITOON is deliberately built around a fast loop:

**idea → scene → render → watch → improve → publish**

The engine is not intended to become a generic animation suite. We will build the primitives needed to make funny, repeatable Shorts quickly: characters, actions, expressions, camera movement, dialogue timing, music timing and reusable scene definitions.

Copyright and music rights remain outside the renderer. Do not commit copyrighted music into the repository; use appropriately licensed or platform-native audio when publishing.
