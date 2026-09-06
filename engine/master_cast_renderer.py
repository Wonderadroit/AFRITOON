"""Render a multi-character AFRITOON scene from canonical SVG masters."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping

from PIL import Image

from .cast_scene import CastScene
from .svg_renderer import rasterize_svg
from .view_policy import resolve_view

W, H = 1080, 1920

DEFAULT_POSITIONS = {
    "tunde": (280.0, 1500.0, 0.82),
    "seyi": (540.0, 1500.0, 0.78),
    "mama": (800.0, 1500.0, 0.88),
}


def render_master_cast(
    scene: CastScene,
    frame_time: float,
    repo_root: str | Path = ".",
    positions: Mapping[str, tuple[float, float, float]] | None = None,
    character_width: int = 420,
) -> Image.Image:
    """Compose the cast from canonical artwork.

    Scene-authored position/scale wins. Explicit renderer positions are an
    override, and defaults are used only for instances still at the library's
    neutral origin. Missing three-quarter/side masters fall back explicitly to
    front artwork; no view is geometrically faked.
    """
    canvas = Image.new("RGBA", (W, H), (247, 243, 235, 255))
    state = scene.state_at(frame_time)
    overrides = positions or {}

    for character_id, instance in state.characters.items():
        if character_id in overrides:
            x, baseline, scale = overrides[character_id]
        elif instance.x != 540.0 or instance.y != 1150.0 or instance.scale != 1.0:
            x, baseline, scale = instance.x, instance.y, instance.scale
        else:
            x, baseline, scale = DEFAULT_POSITIONS.get(
                character_id, (540.0, 1500.0, 0.8)
            )

        resolved = resolve_view(repo_root, character_id, instance.view)
        width = max(1, int(character_width * scale))
        artwork = rasterize_svg(resolved.path, width, width)
        px = int(x - artwork.width / 2)
        py = int(baseline - artwork.height)
        canvas.alpha_composite(artwork, (px, py))

    return canvas
