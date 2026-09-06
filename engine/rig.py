"""Reusable 2D rig primitives for AFRITOON characters."""

from dataclasses import dataclass
from math import cos, radians, sin


@dataclass(frozen=True)
class Joint:
    x: float
    y: float
    rotation: float = 0.0


@dataclass(frozen=True)
class Pose:
    name: str
    head: Joint = Joint(0, -250, 0)
    left_shoulder: Joint = Joint(-105, -55, 0)
    right_shoulder: Joint = Joint(105, -55, 0)
    left_elbow: Joint = Joint(-150, 30, 0)
    right_elbow: Joint = Joint(150, 30, 0)
    left_hand: Joint = Joint(-165, 45, 0)
    right_hand: Joint = Joint(165, 45, 0)
    left_knee: Joint = Joint(-65, 140, 0)
    right_knee: Joint = Joint(65, 140, 0)
    left_foot: Joint = Joint(-65, 245, 0)
    right_foot: Joint = Joint(65, 245, 0)


POSES = {
    "idle": Pose("idle"),
    "vibe": Pose("vibe", left_elbow=Joint(-150,-115,-20), right_elbow=Joint(150,-115,20), left_hand=Joint(-180,-150,-20), right_hand=Joint(180,-150,20)),
    "dance": Pose("dance", left_shoulder=Joint(-105,-55,-20), right_shoulder=Joint(105,-55,20), left_elbow=Joint(-165,-105,-35), right_elbow=Joint(165,-105,35), left_hand=Joint(-190,-155,-35), right_hand=Joint(190,-155,35), left_knee=Joint(-80,150,-8), right_knee=Joint(75,135,8), left_foot=Joint(-105,245,-8), right_foot=Joint(100,235,8)),
    "check_pocket": Pose("check_pocket", left_elbow=Joint(-75,20,15), right_elbow=Joint(75,20,-15), left_hand=Joint(-55,35,0), right_hand=Joint(90,25,0)),
    "shock": Pose("shock", left_elbow=Joint(-165,-120,-25), right_elbow=Joint(165,-120,25), left_hand=Joint(-175,-185,-25), right_hand=Joint(175,-185,25)),
    "shrug": Pose("shrug", left_shoulder=Joint(-105,-75,-12), right_shoulder=Joint(105,-75,12), left_elbow=Joint(-160,-35,-12), right_elbow=Joint(160,-35,12), left_hand=Joint(-175,-5,0), right_hand=Joint(175,-5,0)),
    "freeze": Pose("freeze"),
}


def pose_for(name: str) -> Pose:
    key = "shock" if name == "shocked" else name
    if key not in POSES:
        raise ValueError(f"Unsupported Tunde pose: {name}")
    return POSES[key]


def lerp(a: float, b: float, amount: float) -> float:
    amount = max(0.0, min(1.0, amount))
    return a + (b - a) * amount


def blend_pose(a: Pose, b: Pose, amount: float) -> Pose:
    def blend(ja: Joint, jb: Joint) -> Joint:
        return Joint(lerp(ja.x,jb.x,amount), lerp(ja.y,jb.y,amount), lerp(ja.rotation,jb.rotation,amount))
    return Pose(
        f"{a.name}->{b.name}", blend(a.head,b.head), blend(a.left_shoulder,b.left_shoulder),
        blend(a.right_shoulder,b.right_shoulder), blend(a.left_elbow,b.left_elbow),
        blend(a.right_elbow,b.right_elbow), blend(a.left_hand,b.left_hand),
        blend(a.right_hand,b.right_hand), blend(a.left_knee,b.left_knee),
        blend(a.right_knee,b.right_knee), blend(a.left_foot,b.left_foot), blend(a.right_foot,b.right_foot)
    )


def point_from(origin: Joint, length: float, angle: float) -> Joint:
    theta = radians(angle)
    return Joint(origin.x + cos(theta) * length, origin.y + sin(theta) * length, angle)
