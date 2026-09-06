"""Character-agnostic semantic pose transforms for the AFRITOON cast."""

from __future__ import annotations

from dataclasses import dataclass

from .layered_rig import Transform


@dataclass(frozen=True)
class CharacterPose:
    character_id: str
    name: str
    layers: dict[str, Transform]


BASE = {
    "head": Transform(540, 900),
    "neck": Transform(540, 1040),
    "torso": Transform(540, 1190),
    "left_arm": Transform(400, 1190),
    "right_arm": Transform(680, 1190),
    "legs": Transform(540, 1450),
    "shoes": Transform(540, 1630),
}

COMMON = {
    "idle": {},
    "vibe": {"left_arm": Transform(385, 1135, -18), "right_arm": Transform(695, 1135, 18)},
    "dance": {"left_arm": Transform(375, 1100, -35), "right_arm": Transform(705, 1085, 35), "torso": Transform(540, 1170, -3)},
    "check_pocket": {"left_arm": Transform(475, 1280, 42), "right_arm": Transform(610, 1280, -25)},
    "shock": {"left_arm": Transform(385, 1080, -40), "right_arm": Transform(695, 1080, 40), "head": Transform(540, 880, 0, 1.04)},
    "shocked": {"left_arm": Transform(385, 1080, -40), "right_arm": Transform(695, 1080, 40), "head": Transform(540, 880, 0, 1.04)},
    "shrug": {"left_arm": Transform(390, 1125, -25), "right_arm": Transform(690, 1125, 25)},
    "freeze": {},
}

CHARACTER_OVERRIDES = {
    "tunde": {},
    "seyi": {
        "idle": {"torso": Transform(540, 1195, -2)},
        "look_at_camera": {"head": Transform(540, 900, 0, 1.01)},
    },
    "mama": {
        "idle": {"torso": Transform(540, 1210), "legs": Transform(540, 1460)},
        "angry": {"left_arm": Transform(390, 1150, -25), "right_arm": Transform(690, 1150, 25)},
        "look_at_camera": {"head": Transform(540, 895, 0, 1.02)},
    },
}


def pose_for(character_id: str, pose: str, *, origin_x: float = 0, origin_y: float = 0, scale: float = 1.0) -> CharacterPose:
    cid = str(character_id).strip().lower()
    name = "shock" if pose == "surprised" else str(pose).strip().lower()
    if name not in COMMON and name not in CHARACTER_OVERRIDES.get(cid, {}):
        raise ValueError(f"Unsupported pose for {cid}: {pose}")
    overrides = dict(COMMON.get(name, {}))
    overrides.update(CHARACTER_OVERRIDES.get(cid, {}).get(name, {}))
    layers = {}
    for layer, base in BASE.items():
        item = overrides.get(layer, base)
        layers[layer] = Transform(
            x=origin_x + item.x * scale,
            y=origin_y + item.y * scale,
            rotation=item.rotation,
            scale=item.scale * scale,
        )
    return CharacterPose(cid, name, layers)
