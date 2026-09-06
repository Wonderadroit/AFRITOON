# AFRITOON Scene Specification v0.1

A scene is a small declarative YAML file. It describes timing and intent; the renderer decides how to draw frames.

```yaml
title: "Tunde's First Vibe"
scene:
  duration: 8
  character:
    name: Tunde
    x: 540
    y: 1120
    scale: 1.0
  timeline:
    - time: 0
      action: idle
    - time: 2
      action: vibe
    - time: 4
      action: shocked
    - time: 5
      action: look_at_camera
    - time: 6
      action: dance
```

### Current action vocabulary

`idle`, `vibe`, `dance`, `shock`, `shocked`, `laugh`, `look_at_camera`.

The vocabulary is intentionally small. New actions should be added when a real episode needs them, not merely because a generic animation system could support them.

### Future extensions

The schema can grow with optional sections for:

- multiple characters
- camera events
- dialogue and subtitles
- audio tracks
- beat/lyric cues
- props
- reusable assets
- scene transitions
