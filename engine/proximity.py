"""Deterministic proximity and conversational-staging helpers for ITANRA."""

from __future__ import annotations

from math import hypot
from typing import Mapping


PROXIMITY_FAR = "far"
PROXIMITY_NEAR = "near"
PROXIMITY_CLOSE = "close"
PROXIMITY_CONTACT = "contact"


def distance_between(
    character_id: str,
    target_id: str | None,
    positions: Mapping[str, tuple[float, float, float] | tuple[float, float]],
) -> float | None:
    """Return planar distance between two cast members, or None if unavailable."""
    if target_id is None:
        return None
    character = str(character_id).strip().lower()
    target = str(target_id).strip().lower()
    if not target or character == target:
        return None
    source = positions.get(character)
    destination = positions.get(target)
    if source is None or destination is None:
        return None
    dx = float(destination[0]) - float(source[0])
    dy = float(destination[1]) - float(source[1])
    return hypot(dx, dy)


def interaction_zone(
    character_id: str,
    target_id: str | None,
    positions: Mapping[str, tuple[float, float, float] | tuple[float, float]],
    *,
    contact: float = 55.0,
    close: float = 120.0,
    near: float = 300.0,
) -> str:
    """Classify a character's current physical relationship to its target."""
    distance = distance_between(character_id, target_id, positions)
    if distance is None:
        return PROXIMITY_FAR
    if distance <= max(0.0, float(contact)):
        return PROXIMITY_CONTACT
    if distance <= max(float(contact), float(close)):
        return PROXIMITY_CLOSE
    if distance <= max(float(close), float(near)):
        return PROXIMITY_NEAR
    return PROXIMITY_FAR


def conversational_stop_x(
    actor_x: float,
    target_x: float,
    *,
    distance: float = 70.0,
) -> float:
    """Return a deterministic horizontal stopping point for a conversation."""
    gap = max(0.0, float(distance))
    if actor_x < target_x:
        return float(target_x) - gap
    if actor_x > target_x:
        return float(target_x) + gap
    return float(target_x) - gap
