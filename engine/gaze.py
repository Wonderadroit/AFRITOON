"""Deterministic target-aware gaze helpers for ITANRA."""

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
    """Return left/right/center from a character toward its focus target.

    Positions use the scene compositor's x/y/scale tuples. Vertical distance is
    intentionally ignored: gaze is a small horizontal acting cue, not a camera
    solver. Missing targets and self-focus safely resolve to center.
    """
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
