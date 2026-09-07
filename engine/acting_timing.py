"""Deterministic timing for character actions and reactions.

Temporal acting is deliberately renderer-independent. A performance can be
reasoned about as anticipation -> action -> hold -> recovery before any
animation backend decides how those phases look.
"""

from __future__ import annotations

from dataclasses import dataclass


PHASES = ("anticipation", "action", "hold", "recovery")


@dataclass(frozen=True)
class ActingTiming:
    """Durations for the four phases of a single acting beat."""

    anticipation: float
    action: float
    hold: float
    recovery: float

    def __post_init__(self) -> None:
        if any(value < 0 for value in (
            self.anticipation,
            self.action,
            self.hold,
            self.recovery,
        )):
            raise ValueError("acting phase durations cannot be negative")
        if self.total <= 0:
            raise ValueError("acting timing must have a positive total duration")

    @property
    def total(self) -> float:
        return (
            self.anticipation
            + self.action
            + self.hold
            + self.recovery
        )


# Character-specific timing is part of acting grammar, not rendering.
# The values intentionally stay simple and deterministic so scenes remain
# reproducible while still giving each character a distinct rhythm.
CHARACTER_TIMING: dict[str, dict[str, ActingTiming]] = {
    "tunde": {
        "shock": ActingTiming(0.16, 0.10, 0.34, 0.22),
        "check_pocket": ActingTiming(0.10, 0.24, 0.30, 0.16),
        "dance": ActingTiming(0.06, 0.24, 0.18, 0.12),
        "laugh": ActingTiming(0.08, 0.18, 0.28, 0.16),
    },
    "seyi": {
        "look": ActingTiming(0.16, 0.34, 0.48, 0.18),
        "turn": ActingTiming(0.18, 0.38, 0.50, 0.20),
        "look_at_camera": ActingTiming(0.12, 0.28, 0.52, 0.18),
        "laugh": ActingTiming(0.08, 0.18, 0.30, 0.16),
    },
    "mama": {
        "angry": ActingTiming(0.22, 0.30, 0.62, 0.26),
        "turn": ActingTiming(0.24, 0.40, 0.58, 0.24),
        "look_at_camera": ActingTiming(0.18, 0.30, 0.58, 0.22),
        "laugh": ActingTiming(0.08, 0.18, 0.30, 0.16),
    },
}

DEFAULT_TIMING = ActingTiming(0.10, 0.20, 0.30, 0.15)


def timing_for(character: str, action: str) -> ActingTiming:
    """Return the deterministic timing profile for a character/action."""
    return CHARACTER_TIMING.get(character, {}).get(action, DEFAULT_TIMING)


def acting_phase(character: str, action: str, elapsed: float) -> str:
    """Return the acting phase at ``elapsed`` seconds into an action.

    Time before zero is treated as anticipation. Time after the configured
    duration remains in recovery, making a completed beat visually settle
    instead of jumping back to an unrelated state.
    """
    timing = timing_for(character, action)
    t = max(0.0, float(elapsed))

    if t < timing.anticipation:
        return "anticipation"
    t -= timing.anticipation
    if t < timing.action:
        return "action"
    t -= timing.action
    if t < timing.hold:
        return "hold"
    return "recovery"
