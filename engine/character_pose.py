"""Character-specific semantic pose transforms for AFRITOON."""

from __future__ import annotations

from dataclasses import dataclass

from .layered_rig import Transform


@dataclass(frozen=True)
class CharacterPose:
    character_id: str
    name: str
    layers: dict[str, Transform]


BASE = {
    "head": Transform(300, 330), "neck": Transform(300, 500), "torso": Transform(300, 650),
    "left_arm": Transform(190, 625), "right_arm": Transform(410, 625), "legs": Transform(300, 875),
    "shoes": Transform(300, 1015), "ears": Transform(300, 335), "back_hair": Transform(300, 190),
    "front_hair": Transform(300, 190), "left_eye": Transform(245, 330), "right_eye": Transform(355, 330),
    "left_brow": Transform(245, 270), "right_brow": Transform(355, 270), "nose": Transform(300, 370),
    "mouth": Transform(300, 435),
}

COMMON = {
    "idle": {}, "stand": {},
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
        "talk": {"torso": Transform(300, 645, -1, 1.02), "left_arm": Transform(202, 606, -12), "right_arm": Transform(424, 620, 8)},
        "look_at_camera": {"head": Transform(300, 328, 0, 1.01)},
        "laugh": {"head": Transform(300, 325, -3), "left_arm": Transform(185, 590, -20)},
    },
    "seyi": {
        "idle": {"torso": Transform(300, 655, -2)},
        "look": {"head": Transform(304, 330, 2), "left_arm": Transform(205, 640, 8)},
        "talk": {"torso": Transform(300, 652, -1), "left_arm": Transform(205, 620, -8), "right_arm": Transform(417, 650, 5)},
        "look_at_camera": {"head": Transform(300, 332, 0, 1.01)},
        "laugh": {"head": Transform(300, 327, -2), "left_arm": Transform(205, 610, -10)},
    },
    "mama": {
        "idle": {"torso": Transform(300, 660), "legs": Transform(300, 880)},
        "talk": {"torso": Transform(300, 655, -1, 1.02), "left_arm": Transform(192, 620, -8), "right_arm": Transform(415, 635, 10)},
        "angry": {"left_arm": Transform(190, 635, -18), "right_arm": Transform(407, 600, 28), "torso": Transform(300, 650, 1, 1.02)},
        "look": {"head": Transform(304, 332, 2), "right_arm": Transform(420, 650, 6)},
        "look_at_camera": {"head": Transform(300, 328, 0, 1.02)},
    },
}


def _interpolate(a: Transform, b: Transform, amount: float) -> Transform:
    p = max(0.0, min(1.0, float(amount)))
    return Transform(x=a.x + (b.x - a.x) * p, y=a.y + (b.y - a.y) * p, rotation=a.rotation + (b.rotation - a.rotation) * p, scale=a.scale + (b.scale - a.scale) * p)


def pose_for(character_id: str, pose: str, *, origin_x: float = 0, origin_y: float = 0, scale: float = 1.0) -> CharacterPose:
    cid = str(character_id).strip().lower()
    name = "shock" if pose == "surprised" else str(pose).strip().lower()
    if name not in COMMON and name not in CHARACTER_OVERRIDES.get(cid, {}):
        raise ValueError(f"Unsupported pose for {cid}: {pose}")
    overrides = dict(COMMON.get(name, {})); overrides.update(CHARACTER_OVERRIDES.get(cid, {}).get(name, {}))
    layers = {}
    for layer, base in BASE.items():
        item = overrides.get(layer, base)
        layers[layer] = Transform(x=origin_x + item.x * scale, y=origin_y + item.y * scale, rotation=item.rotation, scale=item.scale * scale)
    return CharacterPose(cid, name, layers)


def pose_for_phase(character_id: str, pose: str, phase: str, *, origin_x: float = 0, origin_y: float = 0, scale: float = 1.0) -> CharacterPose:
    target = pose_for(character_id, pose, origin_x=origin_x, origin_y=origin_y, scale=scale)
    idle = pose_for(character_id, "idle", origin_x=origin_x, origin_y=origin_y, scale=scale)
    amount = {"anticipation": 0.35, "action": 1.0, "hold": 1.0, "recovery": 0.45}.get(phase, 0.0)
    layers = {name: _interpolate(idle.layers[name], target.layers[name], amount) for name in BASE}
    return CharacterPose(str(character_id).strip().lower(), target.name, layers)


def pose_for_motion(character_id: str, pose: str, amount: float, *, origin_x: float = 0, origin_y: float = 0, scale: float = 1.0) -> CharacterPose:
    target = pose_for(character_id, pose, origin_x=origin_x, origin_y=origin_y, scale=scale)
    idle = pose_for(character_id, "idle", origin_x=origin_x, origin_y=origin_y, scale=scale)
    layers = {name: _interpolate(idle.layers[name], target.layers[name], amount) for name in BASE}
    return CharacterPose(str(character_id).strip().lower(), target.name, layers)
