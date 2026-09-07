"""Derive deterministic spatial and entrance/exit blocking from story intent."""
from __future__ import annotations
from dataclasses import dataclass
from .story_director import StoryPlan


@dataclass(frozen=True)
class StoryBlockingCue:
    at: float
    character: str
    x: float
    y: float
    duration: float = 0.0
    target: str | None = None


def _target_id(text: str, available: set[str]) -> str | None:
    lowered = text.lower()
    for candidate in sorted(available):
        if candidate in lowered:
            return candidate
    return None


def cues_for(plan: StoryPlan, positions: dict[str, tuple[float, float]]) -> tuple[StoryBlockingCue, ...]:
    """Create deterministic approach cues from explicit story intent."""
    available = set(positions)
    result: list[StoryBlockingCue] = []
    for beat in plan.beats:
        if beat.character is None:
            continue
        actor = beat.character.strip().lower()
        if actor not in available:
            continue
        text = f"{beat.event} {beat.intent or ''}".lower()
        if not any(word in text for word in ("approach", "come over", "walk to", "go to", "join")):
            continue
        target = _target_id(text, available - {actor})
        if target is None:
            continue
        tx, ty = positions[target]
        ax, ay = positions[actor]
        direction = 1.0 if ax < tx else -1.0
        stop_x = tx - direction * 70.0
        result.append(StoryBlockingCue(float(beat.at), actor, float(stop_x), float(ay), 1.0, target))
    return tuple(result)


def cue_at(cues: tuple[StoryBlockingCue, ...], character_id: str, t: float) -> StoryBlockingCue | None:
    current = None
    for cue in cues:
        if cue.character == character_id and cue.at <= float(t):
            current = cue
    return current


def position_at(base: tuple[float, float], cue: StoryBlockingCue | None, t: float) -> tuple[float, float]:
    if cue is None:
        return base
    if cue.duration <= 0 or float(t) >= cue.at + cue.duration:
        return cue.x, cue.y
    if float(t) <= cue.at:
        return base
    progress = (float(t) - cue.at) / cue.duration
    progress = progress * progress * (3.0 - 2.0 * progress)
    return base[0] + (cue.x - base[0]) * progress, base[1] + (cue.y - base[1]) * progress
