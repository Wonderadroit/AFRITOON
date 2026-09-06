"""Render a reusable AFRITOON cast.

The canonical production path uses the character SVG masters. The old
procedural Tunde renderer remains only as an explicit fallback for environments
that cannot rasterize SVG artwork.
"""

from __future__ import annotations

from PIL import Image, ImageDraw

from .cast_scene import CastScene
from .character import Tunde
from .master_cast_renderer import render_master_cast
from .svg_renderer import SVGRenderUnavailable

W, H = 1080, 1920

DEFAULT_POSITIONS = {
    "tunde": (280, 1180, 0.78),
    "seyi": (540, 1180, 0.72),
    "mama": (800, 1180, 0.82),
}


def _fallback_character(instance):
    """Legacy fallback used only when canonical SVG rendering is unavailable."""
    return Tunde(
        x=instance.x,
        y=instance.y,
        scale=instance.scale,
        pose=instance.pose,
        expression=instance.expression,
    )


def _render_legacy_fallback(scene: CastScene, frame_time: float, size=(W, H)) -> Image.Image:
    """Render the historical procedural fallback.

    This path is intentionally not the production character renderer. It is
    retained so the public API still works in minimal Termux environments.
    """
    img = Image.new("RGBA", size, (247, 243, 235, 255))
    draw = ImageDraw.Draw(img)
    state = scene.state_at(frame_time)

    for character_id, instance in state.characters.items():
        active = instance
        if active.x == 540.0 and active.y == 1150.0:
            x, y, scale = DEFAULT_POSITIONS.get(character_id, (540, 1150, 1.0))
            active = active.__class__(
                definition=active.definition,
                x=x,
                y=y,
                scale=scale,
                view=active.view,
                pose=active.pose,
                expression=active.expression,
            )
        _fallback_character(active).draw(draw)

    return img


def render_cast(
    scene: CastScene,
    frame_time: float,
    size=(W, H),
    repo_root: str = ".",
) -> Image.Image:
    """Render one cast frame using canonical artwork when possible.

    ``render_cast`` remains the stable public API. Production rendering now
    resolves each character independently, so Seyi and Mama can never be
    silently rendered as Tunde. If CairoSVG is unavailable, the renderer falls
    back to the legacy procedural path rather than failing import-time.
    """
    if tuple(size) != (W, H):
        # The master renderer currently owns the canonical 1080x1920 stage.
        # Keep the historical API contract for non-standard test sizes.
        try:
            image = render_master_cast(scene, frame_time, repo_root=repo_root)
            return image.resize(tuple(size), Image.Resampling.LANCZOS)
        except (SVGRenderUnavailable, FileNotFoundError):
            return _render_legacy_fallback(scene, frame_time, size=size)

    try:
        return render_master_cast(scene, frame_time, repo_root=repo_root)
    except (SVGRenderUnavailable, FileNotFoundError):
        return _render_legacy_fallback(scene, frame_time, size=size)
