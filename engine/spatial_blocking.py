"""Deterministic spatial blocking for multi-character scenes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class SpatialCue:
    """Move one character between authored scene positions over a finite window."""

    at: float
    character: str
    to: tuple[float, float]
    duration: float = 0.0

    def __post_init__(self) -> None:
        if self.at < 0:
            raise ValueError("SpatialCue.at must be non-negative")
        if self.duration < 0:
            raise ValueError("SpatialCue.duration must be non-negative")


def _smoothstep(amount: float) -> float:
    x = max(0.0, min(1.0, float(amount)))
    return x * x * (3.0 - 2.0 * x)


def position_at(
    character: str,
    now: float,
    base: Mapping[str, tuple[float, float]],
    cues: tuple[SpatialCue, ...] = (),
) -> tuple[float, float]:
    """Resolve a character's position after all applicable spatial cues."""
    cid = str(character).strip().lower()
    x, y = base.get(cid, (540.0, 1150.0))
    current = (float(x), float(y))
    ordered = sorted((cue for cue in cues if cue.character == cid and cue.at <= now), key=lambda cue: cue.at)
    for cue in ordered:
        start = current
        if cue.duration <= 0 or now >= cue.at + cue.duration:
            current = cue.to
            continue
        progress = _smoothstep((now - cue.at) / cue.duration)
        current = (
            start[0] + (cue.to[0] - start[0]) * progress,
            start[1] + (cue.to[1] - start[1]) * progress,
        )
    return current


def resolve_positions(
    now: float,
    base: Mapping[str, tuple[float, float, float]],
    cues: tuple[SpatialCue, ...] = (),
) -> dict[str, tuple[float, float, float]]:
    """Return scene positions with deterministic movement applied."""
    result = dict(base)
    for cid, (x, y, scale) in base.items():
        px, py = position_at(cid, now, {key: (value[0], value[1]) for key, value in base.items()}, cues)
        result[cid] = (px, py, scale)
    return result
