"""Deterministic timing and motion curves for character acting.

Temporal acting is renderer-independent. A performance can be reasoned about
as anticipation -> action -> hold -> recovery before any animation backend
decides how those phases look.
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
        # Phase constants are decimal authoring values. Normalize the tiny
        # binary floating-point residue so timing comparisons remain stable.
        return round(self.anticipation + self.action + self.hold + self.recovery, 10)


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

# Motion characterizes rhythm, not identity: Tunde snaps, Seyi glides,
# Mama moves deliberately. Values are bounded so renders stay deterministic.
MOTION_CURVES: dict[str, str] = {
    "tunde": "snap",
    "seyi": "smooth",
    "mama": "deliberate",
}


def timing_for(character: str, action: str) -> ActingTiming:
    """Return the deterministic timing profile for a character/action."""
    return CHARACTER_TIMING.get(character, {}).get(action, DEFAULT_TIMING)


def smoothstep(value: float) -> float:
    """Cubic ease-in/ease-out, clamped to [0, 1]."""
    t = max(0.0, min(1.0, float(value)))
    return t * t * (3.0 - 2.0 * t)


def ease_in(value: float) -> float:
    """Accelerate from rest."""
    t = max(0.0, min(1.0, float(value)))
    return t * t


def ease_out(value: float) -> float:
    """Decelerate into the destination."""
    t = max(0.0, min(1.0, float(value)))
    return 1.0 - (1.0 - t) ** 2


def motion_curve(character: str, phase: str, progress: float) -> float:
    """Shape normalized phase progress according to character rhythm."""
    t = max(0.0, min(1.0, float(progress)))
    style = MOTION_CURVES.get(str(character).strip().lower(), "smooth")
    if phase == "action":
        if style == "snap":
            return ease_out(t)
        if style == "deliberate":
            return smoothstep(t)
        return smoothstep(t)
    if phase == "anticipation":
        return ease_in(t) if style == "snap" else smoothstep(t)
    if phase == "recovery":
        return ease_out(t)
    return 1.0


def acting_phase(character: str, action: str, elapsed: float) -> str:
    """Return the acting phase at ``elapsed`` seconds into an action."""
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


def acting_motion(character: str, action: str, elapsed: float) -> tuple[str, float, float]:
    """Return ``(phase, phase_progress, pose_amount)`` for a timed action."""
    timing = timing_for(character, action)
    t = max(0.0, float(elapsed))

    if t < timing.anticipation and timing.anticipation > 0:
        phase = "anticipation"
        progress = t / timing.anticipation
        amount = 0.15 * motion_curve(character, phase, progress)
        return phase, progress, amount

    t -= timing.anticipation
    if t < timing.action and timing.action > 0:
        phase = "action"
        progress = t / timing.action
        amount = 0.15 + 0.85 * motion_curve(character, phase, progress)
        return phase, progress, amount

    t -= timing.action
    if t < timing.hold or timing.recovery == 0:
        return "hold", 1.0, 1.0

    t -= timing.hold
    progress = min(1.0, t / timing.recovery)
    amount = 1.0 - motion_curve(character, "recovery", progress)
    return "recovery", progress, amount
