"""Translate story beats into deterministic performance cues.

This module is deliberately rule-based. Story intent can influence performance,
but it does not replace explicit scene interaction cues. Existing hand-authored
scene cues therefore remain the highest-priority performance source.
"""

from __future__ import annotations

from dataclasses import dataclass

from .character_spec import character
from .story_director import StoryBeat, StoryPlan


EMOTION_TO_EXPRESSION = {
    "calm": "neutral",
    "happy": "happy",
    "funny": "happy",
    "curious": "curious",
    "nostalgic": "sad",
    "sad": "sad",
    "hopeful": "happy",
    "angry": "angry",
    "surprised": "surprised",
    "shocked": "shocked",
    "deadpan": "deadpan",
}


@dataclass(frozen=True)
class StoryPerformanceCue:
    at: float
    character: str
    action: str
    expression: str


def _action_for(beat: StoryBeat) -> str:
    text = f"{beat.event} {beat.intent or ''}".lower()
    if any(word in text for word in ("panic", "power goes off", "shock", "shocked")):
        return "shock"
    if any(word in text for word in ("camera", "audience", "look at")):
        return "look_at_camera"
    if any(word in text for word in ("dance", "vibe")):
        return "dance"
    if any(word in text for word in ("laugh", "funny", "joke")):
        return "laugh"
    if any(word in text for word in ("talk", "speak", "say", "question")):
        return "talk"
    if any(word in text for word in ("turn", "notice", "look")):
        return "look"
    if any(word in text for word in ("freeze", "silence", "caught")):
        return "freeze"
    return "idle"


def _expression_for(beat: StoryBeat) -> str:
    return EMOTION_TO_EXPRESSION.get(beat.emotion.strip().lower(), "neutral")


def cues_for(plan: StoryPlan, character_id: str) -> tuple[StoryPerformanceCue, ...]:
    """Return validated performance cues for one character.

    Character-specific beats target only that character. A beat without a
    character applies to every character in the scene and is useful for broad
    emotional transitions.
    """
    definition = character(character_id)
    result: list[StoryPerformanceCue] = []
    for beat in plan.beats:
        if beat.character is not None and beat.character.strip().lower() != definition.id:
            continue
        action = _action_for(beat)
        if action not in definition.actions:
            action = definition.default_pose
        expression = _expression_for(beat)
        if expression not in definition.expressions:
            expression = definition.default_expression
        result.append(StoryPerformanceCue(beat.at, definition.id, action, expression))
    return tuple(result)


def cue_at(cues: tuple[StoryPerformanceCue, ...], t: float) -> StoryPerformanceCue | None:
    """Return the latest story-derived performance cue at time ``t``."""
    current = None
    for cue in cues:
        if cue.at <= float(t):
            current = cue
        else:
            break
    return current
