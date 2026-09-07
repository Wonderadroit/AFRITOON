"""Deterministic character entrances and exits for scene blocking."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class EntryExitCue:
    """Move a character into or out of frame over a finite time window."""

    at: float
    character: str
    action: str
    position: tuple[float, float] | None = None
    duration: float = 0.0

    def __post_init__(self) -> None:
        action = str(self.action).strip().lower()
        if action not in {"enter", "exit"}:
            raise ValueError("EntryExitCue.action must be 'enter' or 'exit'")
        if self.at < 0:
            raise ValueError("EntryExitCue.at must be non-negative")
        if self.duration < 0:
            raise ValueError("EntryExitCue.duration must be non-negative")
        if self.position is not None and len(self.position) != 2:
            raise ValueError("EntryExitCue.position must contain x and y")


def _smoothstep(amount: float) -> float:
    x = max(0.0, min(1.0, float(amount)))
    return x * x * (3.0 - 2.0 * x)


def _lerp(start: tuple[float, float], end: tuple[float, float], amount: float) -> tuple[float, float]:
    p = _smoothstep(amount)
    return (start[0] + (end[0] - start[0]) * p, start[1] + (end[1] - start[1]) * p)


def resolve_entry_exit(
    character: str,
    now: float,
    base: Mapping[str, tuple[float, float]],
    cues: tuple[EntryExitCue, ...] = (),
) -> tuple[tuple[float, float], bool]:
    """Resolve position and visibility after all entry/exit cues."""
    cid = str(character).strip().lower()
    authored = tuple(map(float, base.get(cid, (540.0, 1150.0))))
    current = authored
    visible = True
    character_cues = sorted(
        (cue for cue in cues if cue.character.strip().lower() == cid),
        key=lambda cue: cue.at,
    )

    # An explicit future entrance defines the character's pre-entrance state.
    for cue in character_cues:
        if cue.at > now:
            if cue.action == "enter":
                if cue.position is not None:
                    current = tuple(map(float, cue.position))
                visible = False
            break

    for cue in character_cues:
        if cue.at > now:
            break
        target = tuple(map(float, cue.position)) if cue.position is not None else authored
        if cue.action == "enter":
            start = current if not visible else (tuple(map(float, cue.position)) if cue.position is not None else current)
            if cue.duration <= 0 or now >= cue.at + cue.duration:
                current = authored
                visible = True
            else:
                current = _lerp(start, authored, (now - cue.at) / cue.duration)
                visible = True
        else:
            start = current
            if cue.duration <= 0 or now >= cue.at + cue.duration:
                current = target
                visible = False
            else:
                current = _lerp(start, target, (now - cue.at) / cue.duration)
                visible = True
    return current, visible


def resolve_entry_exit_states(
    now: float,
    base: Mapping[str, tuple[float, float, float]],
    cues: tuple[EntryExitCue, ...] = (),
) -> dict[str, tuple[float, float, float, bool]]:
    """Resolve entry/exit positions while preserving authored character scale."""
    result: dict[str, tuple[float, float, float, bool]] = {}
    xy = {cid: (value[0], value[1]) for cid, value in base.items()}
    for cid, (x, y, scale) in base.items():
        (px, py), visible = resolve_entry_exit(cid, now, xy, cues)
        result[cid] = (px, py, scale, visible)
    return result
