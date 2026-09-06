"""Render one AFRITOON scene frame from canonical character artwork."""

from __future__ import annotations

import argparse
from pathlib import Path

from engine.cast_scene import CastScene
from engine.master_cast_renderer import render_master_cast


def main() -> int:
    parser = argparse.ArgumentParser(description="Render one AFRITOON scene frame")
    parser.add_argument("scene", help="Scene YAML path")
    parser.add_argument("--time", type=float, default=0.0, help="Frame time in seconds")
    parser.add_argument("--output", default="frame.png", help="Output PNG path")
    args = parser.parse_args()

    scene_path = Path(args.scene)
    scene = CastScene.from_yaml(scene_path)
    image = render_master_cast(scene, args.time, repo_root=scene_path.parent.parent)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)
    print(f"Rendered {scene.name} at {max(0.0, min(args.time, scene.duration)):.2f}s -> {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
