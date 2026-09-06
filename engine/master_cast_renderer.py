"""Render a multi-character AFRITOON scene from canonical SVG masters.

This is the artwork bridge between scene direction and the future 16-layer
PNG rigs. It keeps character art independent from timing and interaction code.
"""

from __future__ import annotations

from pathlib import Path
from typing import Mapping

from PIL import Image

from .cast_scene import CastScene
from .svg_renderer import master_path, rasterize_svg

W, H = 1080, 1920


def render_master_cast(
    scene: CastScene,
    frame_time: float,
    repo_root: str | Path = ".",
    positions: Mapping[str, tuple[float, float, float]] | None = None,
    character_width: int = 420,
) -> Image.Image:
    """Compose the current cast using human-looking SVG master artwork.

    `positions` maps character id to `(center_x, baseline_y, scale)`.
    Expressions/poses are resolved by CastScene but are not baked into these
    static masters; true facial and body animation arrives with layered rigs.
    """
    canvas = Image.new("RGBA", (W, H), (247, 243, 235, 255))
    state = scene.state_at(frame_time)
    positions = positions or {
        "tunde": (280.0, 1500.0, 0.82),
        "seyi": (540.0, 1500.0, 0.78),
        "mama": (800.0, 1500.0, 0.88),
    }

    for character_id, instance in state.characters.items():
        x, baseline, scale = positions.get(character_id, (540.0, 1500.0, 0.8))
        path = master_path(repo_root, character_id, instance.view)
        if not path.exists():
            continue
        width = max(1, int(character_width * scale))
        # Masters use a square-ish viewBox; preserve their aspect ratio.
        artwork = rasterize_svg(path, width, width)
        px = int(x - artwork.width / 2)
        py = int(baseline - artwork.height)
        canvas.alpha_composite(artwork, (px, py))

    return canvas
