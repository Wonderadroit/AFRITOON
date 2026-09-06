"""Render a reusable AFRITOON cast without coupling scenes to final artwork."""

from __future__ import annotations

from PIL import Image, ImageDraw

from .cast_scene import CastScene
from .character import Tunde

W, H = 1080, 1920

# Stage positions are deliberately data-driven and easy to replace when
# production artwork is rasterized into the layered rig.
DEFAULT_POSITIONS = {
    "tunde": (280, 1180, 0.78),
    "seyi": (540, 1180, 0.72),
    "mama": (800, 1180, 0.82),
}


def _fallback_character(instance):
    """Return the legacy procedural character only until layered assets exist."""
    definition = instance.definition
    return Tunde(
        x=instance.x,
        y=instance.y,
        scale=instance.scale,
        pose=instance.pose,
        expression=instance.expression,
    )


def render_cast(scene: CastScene, frame_time: float, size=(W, H)) -> Image.Image:
    """Render one frame of a CastScene.

    The renderer intentionally owns composition, not character identity. Once
    layered PNG artwork is available, this function can select the character's
    LayeredRig while keeping the same CastScene API.
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
                x=x, y=y, scale=scale,
                view=active.view, pose=active.pose,
                expression=active.expression,
            )
        _fallback_character(active).draw(draw)

    return img
