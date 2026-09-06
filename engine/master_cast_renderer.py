"""Render a multi-character AFRITOON scene from canonical SVG masters."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping

from PIL import Image

from .cast_scene import CastScene
from .svg_renderer import rasterize_svg
from .view_policy import resolve_view

W, H = 1080, 1920


def render_master_cast(
    scene: CastScene,
    frame_time: float,
    repo_root: str | Path = ".",
    positions: Mapping[str, tuple[float, float, float]] | None = None,
    character_width: int = 420,
) -> Image.Image:
    """Compose the cast from the best available canonical artwork.

    Missing three-quarter/side masters explicitly fall back to the front
    master. This is a build-state decision, never a claim that the missing
    view has been authored.
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
        resolved = resolve_view(repo_root, character_id, instance.view)
        width = max(1, int(character_width * scale))
        artwork = rasterize_svg(resolved.path, width, width)
        px = int(x - artwork.width / 2)
        py = int(baseline - artwork.height)
        canvas.alpha_composite(artwork, (px, py))

    return canvas
