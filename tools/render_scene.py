"""CLI for rendering an AFRITOON YAML scene to MP4."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

# Make direct execution from the repository's tools/ directory behave like
# execution from the repository root (e.g. ``python tools/render_scene.py``).
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.cast_scene import CastScene
from engine.cast_video import render_video


def main() -> int:
    parser = argparse.ArgumentParser(description="Render an AFRITOON scene to vertical MP4")
    parser.add_argument("scene", help="Scene YAML path")
    parser.add_argument("--output", default="output/scene.mp4", help="Output MP4 path")
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--audio", help="Optional user-supplied/licensed audio file")
    args = parser.parse_args()

    scene_path = Path(args.scene).resolve()
    scene = CastScene.from_yaml(scene_path)
    output = render_video(
        scene,
        args.output,
        repo_root=scene_path.parent.parent,
        fps=args.fps,
        audio=args.audio,
    )
    print(f"Rendered {scene.name} ({scene.duration:.2f}s) -> {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
