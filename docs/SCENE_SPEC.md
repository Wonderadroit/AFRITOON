# AFRITOON Scene Specification v0.1

A scene is declarative YAML describing timing and intent.

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

Current action vocabulary: `idle`, `vibe`, `dance`, `shock`, `shocked`, `laugh`, `look_at_camera`.

Future schema sections can add multiple characters, camera events, dialogue/subtitles, audio, beat/lyric cues, props, reusable assets and transitions.
