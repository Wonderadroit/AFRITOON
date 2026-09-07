"""Character-specific semantic pose transforms for AFRITOON."""

from __future__ import annotations

from dataclasses import dataclass

from .layered_rig import Transform


@dataclass(frozen=True)
class CharacterPose:
    character_id: str
    name: str
    layers: dict[str, Transform]


# Canonical 600x1100 artwork coordinates.  These are layer centres, not
# screen coordinates, so the same pose can be rendered at any final size.
BASE = {
    "head": Transform(300, 330),
    "neck": Transform(300, 500),
    "torso": Transform(300, 650),
    "left_arm": Transform(190, 625),
    "right_arm": Transform(410, 625),
    "legs": Transform(300, 875),
    "shoes": Transform(300, 1015),
    "ears": Transform(300, 335),
    "back_hair": Transform(300, 190),
    "front_hair": Transform(300, 190),
    "left_eye": Transform(245, 330),
    "right_eye": Transform(355, 330),
    "left_brow": Transform(245, 270),
    "right_brow": Transform(355, 270),
    "nose": Transform(300, 370),
    "mouth": Transform(300, 435),
}

COMMON = {
    "idle": {},
    "stand": {},
    "talk": {"torso": Transform(300, 646, 0, 1.01)},
    "look": {"head": Transform(304, 330, 3), "left_eye": Transform(249, 330), "right_eye": Transform(359, 330)},
    "turn": {"head": Transform(309, 330, 8), "left_eye": Transform(252, 330), "right_eye": Transform(362, 330), "torso": Transform(303, 650, 3)},
    "look_at_camera": {"head": Transform(300, 330)},
    "laugh": {"head": Transform(300, 325, -3), "torso": Transform(300, 648, 0, 1.02)},
    "vibe": {"left_arm": Transform(180, 590, -18), "right_arm": Transform(420, 590, 18), "torso": Transform(300, 648, -1)},
    "dance": {"left_arm": Transform(165, 570, -35), "right_arm": Transform(435, 560, 35), "torso": Transform(300, 640, -3), "head": Transform(300, 325, -4)},
    "check_pocket": {"left_arm": Transform(245, 665, 42), "right_arm": Transform(370, 660, -25), "torso": Transform(300, 650, 2)},
    "shock": {"left_arm": Transform(175, 570, -40), "right_arm": Transform(425, 570, 40), "head": Transform(300, 315, 0, 1.04), "torso": Transform(300, 650, 0, 0.98)},
    "shocked": {"left_arm": Transform(175, 570, -40), "right_arm": Transform(425, 570, 40), "head": Transform(300, 315, 0, 1.04), "torso": Transform(300, 650, 0, 0.98)},
    "shrug": {"left_arm": Transform(180, 585, -25), "right_arm": Transform(420, 585, 25)},
    "freeze": {},
}

CHARACTER_OVERRIDES = {
    "tunde": {
        "talk": {"torso": Transform(300, 645, -1, 1.02)},
        "look_at_camera": {"head": Transform(300, 328, 0, 1.01)},
    },
    "seyi": {
        "idle": {"torso": Transform(300, 655, -2)},
        "look": {"head": Transform(304, 330, 2)},
        "look_at_camera": {"head": Transform(300, 332, 0, 1.01)},
        "laugh": {"head": Transform(300, 327, -2)},
    },
    "mama": {
        "idle": {"torso": Transform(300, 660), "legs": Transform(300, 880)},
        "talk": {"torso": Transform(300, 655, -1, 1.02)},
        "angry": {"left_arm": Transform(180, 600, -25), "right_arm": Transform(420, 600, 25), "torso": Transform(300, 650, 1, 1.02)},
        "look_at_camera": {"head": Transform(300, 328, 0, 1.02)},
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
