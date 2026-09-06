"""CLI entry point for AFRITOON v0.1."""

import argparse
from engine.scene import Scene
from engine.renderer import render


def main() -> None:
    parser = argparse.ArgumentParser(description="Render an AFRITOON scene")
    parser.add_argument("scene", help="Path to a YAML scene")
    parser.add_argument("-o", "--output", help="Output MP4 path")
    args = parser.parse_args()
    scene = Scene.load(args.scene)
    stem = args.scene.rsplit("/", 1)[-1].rsplit(".", 1)[0]
    output = args.output or f"output/{stem}.mp4"
    print(f"Rendering: {scene.title}")
    print(f"Output: {output}")
    print(render(scene, output))


if __name__ == "__main__":
    main()
