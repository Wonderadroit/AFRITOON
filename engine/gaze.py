"""Deterministic target-aware gaze and interaction helpers for ITANRA."""

from __future__ import annotations

from typing import Mapping

Gaze = str


def gaze_direction(
    character_id: str,
    focus_id: str | None,
    positions: Mapping[str, tuple[float, float, float]],
    *,
    deadband: float = 18.0,
) -> Gaze:
    """Return left/right/center from a character toward its focus target."""
    character = str(character_id).strip().lower()
    target = str(focus_id).strip().lower() if focus_id is not None else ""
    if not target or target == character:
        return "center"
    source = positions.get(character)
    destination = positions.get(target)
    if source is None or destination is None:
        return "center"
    delta = float(destination[0]) - float(source[0])
    threshold = max(0.0, float(deadband))
    if delta < -threshold:
        return "left"
    if delta > threshold:
        return "right"
    return "center"


def interaction_strength(
    character_id: str,
    focus_id: str | None,
    positions: Mapping[str, tuple[float, float, float]],
    *,
    near_distance: float = 90.0,
    far_distance: float = 360.0,
) -> float:
    """Return bounded 0..1 interaction strength from horizontal target distance.

    Nearby targets produce a restrained response; farther targets produce a
    stronger orientation. This deliberately ignores vertical distance and
    remains a simple acting cue rather than a camera/IK solver.
    """
    character = str(character_id).strip().lower()
    target = str(focus_id).strip().lower() if focus_id is not None else ""
    if not target or target == character:
        return 0.0
    source = positions.get(character)
    destination = positions.get(target)
    if source is None or destination is None:
        return 0.0
    distance = abs(float(destination[0]) - float(source[0]))
    near = max(0.0, float(near_distance))
    far = max(near + 1.0, float(far_distance))
    if distance <= near:
        return 0.0
    return max(0.0, min(1.0, (distance - near) / (far - near)))
