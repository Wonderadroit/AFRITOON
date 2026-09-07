"""Render a multi-character AFRITOON scene from canonical SVG masters."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping

from PIL import Image

from .cast_scene import CastScene
from .performance_renderer import apply_face_performance, apply_performance, performance_for_character
from .semantic_svg_rig import render_semantic_character
from .svg_renderer import SVGRenderUnavailable, rasterize_svg
from .view_policy import resolve_view

W, H = 1080, 1920
DEFAULT_POSITIONS = {
    "tunde": (280.0, 1500.0, 0.82),
    "seyi": (540.0, 1500.0, 0.78),
    "mama": (800.0, 1500.0, 0.88),
}
SOURCE_ASPECT = 1100.0 / 600.0


def _has_semantic_layers(path: Path) -> bool:
    try:
        return 'data-layer="' in path.read_text(encoding="utf-8")
    except OSError:
        return False


def render_master_cast(
    scene: CastScene,
    frame_time: float,
    repo_root: str | Path = ".",
    positions: Mapping[str, tuple[float, float, float]] | None = None,
    character_width: int = 420,
) -> Image.Image:
    """Compose canonical artwork with semantic body poses and face performance."""
    canvas = Image.new("RGBA", (W, H), (247, 243, 235, 255))
    state = scene.state_at(frame_time)
    overrides = positions or {}

    for character_id, instance in state.characters.items():
        if character_id in overrides:
            x, baseline, scale = overrides[character_id]
        elif instance.x != 540.0 or instance.y != 1150.0 or instance.scale != 1.0:
            x, baseline, scale = instance.x, instance.y, instance.scale
        else:
            x, baseline, scale = DEFAULT_POSITIONS.get(character_id, (540.0, 1500.0, 0.8))

        resolved = resolve_view(repo_root, character_id, instance.view)
        width = max(1, int(character_width * scale))
        height = max(1, int(round(width * SOURCE_ASPECT)))
        performance = performance_for_character(scene, character_id, frame_time)

        if _has_semantic_layers(resolved.path):
            try:
                artwork = render_semantic_character(
                    resolved.path,
                    character_id,
                    performance.pose,
                    scale=1.0,
                )
                artwork = apply_face_performance(artwork, performance, character_id)
                artwork = artwork.resize((width, height), Image.Resampling.LANCZOS)
            except (SVGRenderUnavailable, ValueError, OSError):
                artwork = rasterize_svg(resolved.path, width, height)
                artwork = apply_performance(artwork, performance, character_id)
        else:
            artwork = rasterize_svg(resolved.path, width, height)
            artwork = apply_performance(artwork, performance, character_id)

        px = int(x - artwork.width / 2)
        py = int(baseline - artwork.height)
        canvas.alpha_composite(artwork, (px, py))

    return canvas
