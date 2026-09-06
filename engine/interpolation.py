"""Frame-safe interpolation utilities for AFRITOON character motion."""

from dataclasses import replace
from .layered_rig import Transform


def clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def smoothstep(value: float) -> float:
    """Ease-in/ease-out interpolation for readable cartoon motion."""
    t = clamp01(value)
    return t * t * (3.0 - 2.0 * t)


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def interpolate_transform(a: Transform, b: Transform, progress: float) -> Transform:
    t = smoothstep(progress)
    return Transform(
        x=lerp(a.x, b.x, t),
        y=lerp(a.y, b.y, t),
        rotation=lerp(a.rotation, b.rotation, t),
        scale=lerp(a.scale, b.scale, t),
    )


def interpolate_pose(start: dict[str, Transform], end: dict[str, Transform], progress: float) -> dict[str, Transform]:
    """Blend two pose maps, preserving layers present in only one pose."""
    names = set(start) | set(end)
    result = {}
    for name in names:
        a = start.get(name, end[name])
        b = end.get(name, start[name])
        result[name] = interpolate_transform(a, b, progress)
    return result
