"""ITANRA story-to-performance planning primitives.

The story director converts declarative story intent into deterministic beats.
It does not generate prose, voice, or pixels. Those remain separate stages.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class StoryBeat:
    """A meaningful dramatic event in an episode."""

    at: float
    event: str
    character: str | None = None
    emotion: str = "calm"
    intent: str | None = None
    payoff: bool = False


@dataclass(frozen=True)
class StoryPlan:
    """Validated, ordered story plan consumed by downstream directors."""

    title: str
    duration: float
    beats: tuple[StoryBeat, ...]

    def at(self, t: float) -> StoryBeat | None:
        now = max(0.0, min(float(t), self.duration))
        current = None
        for beat in self.beats:
            if beat.at <= now:
                current = beat
            else:
                break
        return current


def build_story_plan(
    title: str,
    duration: float,
    beats: Iterable[StoryBeat],
) -> StoryPlan:
    """Build and validate a deterministic story plan.

    Story beats must be chronological and remain inside the episode duration.
    Duplicate timestamps are allowed because multiple dramatic events may occur
    at the same instant, but their supplied order is preserved.
    """
    total = float(duration)
    if total <= 0:
        raise ValueError("Story duration must be positive")

    ordered = tuple(sorted(beats, key=lambda beat: beat.at))
    for beat in ordered:
        if beat.at < 0 or beat.at > total:
            raise ValueError(f"Story beat outside duration: {beat.at}")
        if not beat.event.strip():
            raise ValueError("Story beat event cannot be empty")
        if not beat.emotion.strip():
            raise ValueError("Story beat emotion cannot be empty")

    return StoryPlan(str(title), total, ordered)


def story_plan_from_yaml(raw: dict) -> StoryPlan:
    """Create a StoryPlan from a scene's optional ``story`` mapping."""
    story = raw.get("story", raw)
    beats = tuple(
        StoryBeat(
            at=float(item["at"]),
            event=str(item["event"]),
            character=str(item["character"]) if item.get("character") is not None else None,
            emotion=str(item.get("emotion", "calm")),
            intent=str(item["intent"]) if item.get("intent") is not None else None,
            payoff=bool(item.get("payoff", False)),
        )
        for item in story.get("beats", ())
    )
    return build_story_plan(
        title=str(story.get("title", "Untitled")),
        duration=float(story.get("duration", 0.0)),
        beats=beats,
    )
