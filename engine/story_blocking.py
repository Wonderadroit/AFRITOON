"""Derive deterministic spatial and entrance/exit blocking from story intent."""
from __future__ import annotations
from dataclasses import dataclass
from .entrance_exit import EntryExitCue
from .proximity import conversational_stop_x
from .story_director import StoryPlan


@dataclass(frozen=True)
class StoryBlockingCue:
    at: float
    character: str
    x: float
    y: float
    duration: float = 0.0
    target: str | None = None
    interaction_distance: float = 280.0

    @property
    def to(self) -> tuple[float, float]:
        """SpatialCue-compatible destination for the shared resolver."""
        return (self.x, self.y)


def _target_id(text: str, available: set[str]) -> str | None:
    lowered = text.lower()
    for candidate in sorted(available):
        if candidate in lowered:
            return candidate
    return None


def cues_for(plan: StoryPlan, positions: dict[str, tuple[float, float]]) -> tuple[StoryBlockingCue, ...]:
    """Create deterministic approach cues that end at a natural conversational distance."""
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
        tx, _ = positions[target]
        ax, ay = positions[actor]
        distance = 280.0
        stop_x = conversational_stop_x(ax, tx, distance=distance)
        result.append(StoryBlockingCue(float(beat.at), actor, stop_x, float(ay), 1.0, target, distance))
    return tuple(result)


def entry_exit_cues_for(plan: StoryPlan, positions: dict[str, tuple[float, float]]) -> tuple[EntryExitCue, ...]:
    """Derive only explicit character entrance/exit language."""
    available = set(positions)
    result: list[EntryExitCue] = []
    enter_words = ("enters", "enter", "comes in", "come in", "walks in", "walk in")
    exit_words = ("leaves", "leave", "walks out", "walk out", "exits", "exit")
    collective_subjects = ("everybody", "everyone", "they all", "all of them")
    for beat in plan.beats:
        if beat.character is None:
            continue
        actor = beat.character.strip().lower()
        if actor not in available:
            continue
        text = f"{beat.event} {beat.intent or ''}".lower()
        if any(word in text for word in enter_words):
            result.append(EntryExitCue(float(beat.at), actor, "enter", _offscreen_start(positions[actor], positions), 1.0))
        elif any(word in text for word in exit_words):
            if any(subject in text for subject in collective_subjects):
                continue
            result.append(EntryExitCue(float(beat.at), actor, "exit", _offscreen_exit(positions[actor], positions), 1.0))
    return tuple(result)


def _offscreen_start(position: tuple[float, float], positions: dict[str, tuple[float, float]]) -> tuple[float, float]:
    center = sum(x for x, _ in positions.values()) / max(1, len(positions))
    return (-180.0, position[1]) if position[0] >= center else (1260.0, position[1])


def _offscreen_exit(position: tuple[float, float], positions: dict[str, tuple[float, float]]) -> tuple[float, float]:
    center = sum(x for x, _ in positions.values()) / max(1, len(positions))
    return (1260.0, position[1]) if position[0] >= center else (-180.0, position[1])


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
