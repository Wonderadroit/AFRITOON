"""Map semantic Tunde poses to transforms used by the layered rig."""

from dataclasses import dataclass
from .layered_rig import Transform


@dataclass(frozen=True)
class PoseMap:
    layers: dict[str, Transform]


BASE = {
    "head": Transform(540, 900, 0, 1),
    "neck": Transform(540, 1040, 0, 1),
    "torso": Transform(540, 1190, 0, 1),
    "left_arm": Transform(400, 1190, 0, 1),
    "right_arm": Transform(680, 1190, 0, 1),
    "legs": Transform(540, 1450, 0, 1),
    "shoes": Transform(540, 1630, 0, 1),
}

POSES = {
    "idle": {},
    "vibe": {
        "left_arm": Transform(385, 1135, -18, 1),
        "right_arm": Transform(695, 1135, 18, 1),
        "torso": Transform(540, 1180, 0, 1),
    },
    "dance": {
        "left_arm": Transform(375, 1100, -35, 1),
        "right_arm": Transform(705, 1085, 35, 1),
        "torso": Transform(540, 1170, -3, 1),
        "legs": Transform(525, 1450, -5, 1),
    },
    "check_pocket": {
        "left_arm": Transform(475, 1280, 42, 1),
        "right_arm": Transform(610, 1280, -25, 1),
    },
    "shock": {
        "left_arm": Transform(385, 1080, -40, 1),
        "right_arm": Transform(695, 1080, 40, 1),
        "head": Transform(540, 880, 0, 1.04),
    },
    "shocked": {
        "left_arm": Transform(385, 1080, -40, 1),
        "right_arm": Transform(695, 1080, 40, 1),
        "head": Transform(540, 880, 0, 1.04),
    },
    "shrug": {
        "left_arm": Transform(390, 1125, -25, 1),
        "right_arm": Transform(690, 1125, 25, 1),
    },
    "freeze": {},
}


def pose_map(name: str, *, origin_x: float = 0, origin_y: float = 0, scale: float = 1.0) -> PoseMap:
    """Return absolute layer transforms for a named pose."""
    if name not in POSES:
        raise ValueError(f"Unsupported Tunde pose: {name}")
    transforms = {}
    for layer, base in BASE.items():
        override = POSES[name].get(layer, base)
        transforms[layer] = Transform(
            x=origin_x + override.x * scale,
            y=origin_y + override.y * scale,
            rotation=override.rotation,
            scale=override.scale * scale,
        )
    return PoseMap(transforms)
