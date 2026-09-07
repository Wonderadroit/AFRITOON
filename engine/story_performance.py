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


# Source action -> contextual reactions. These are deliberately sparse: the
# engine should react to meaningful beats, not make every character twitch.
# Reactions are derived only from authored story beats, so generated reactions
# never recursively trigger more reactions.
REACTION_RULES = {
    ("tunde", "shock"): (
        ("seyi", 0.35, "look", "deadpan"),
        ("mama", 0.65, "turn", "curious"),
    ),
    ("tunde", "freeze"): (
        ("seyi", 0.40, "look_at_camera", "deadpan"),
        ("mama", 0.80, "look_at_camera", "deadpan"),
    ),
    ("tunde", "check_pocket"): (
        ("seyi", 0.45, "look", "deadpan"),
    ),
    ("mama", "angry"): (
        ("tunde", 0.35, "freeze", "shocked"),
        ("seyi", 0.60, "look_at_camera", "deadpan"),
    ),
}


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


def _reaction_cues_for(
    plan: StoryPlan,
    character_id: str,
) -> list[StoryPerformanceCue]:
    """Derive sparse contextual reactions from character-specific story beats."""
    result: list[StoryPerformanceCue] = []
    target_definition = character(character_id)
    for beat in plan.beats:
        if beat.character is None:
            continue
        source = beat.character.strip().lower()
        if source == target_definition.id:
            continue
        source_action = _action_for(beat)
        for target, delay, action, expression in REACTION_RULES.get((source, source_action), ()):
            if target != target_definition.id:
                continue
            if action not in target_definition.actions:
                continue
            if expression not in target_definition.expressions:
                continue
            result.append(
                StoryPerformanceCue(
                    at=float(beat.at) + float(delay),
                    character=target_definition.id,
                    action=action,
                    expression=expression,
                )
            )
    return result


def cues_for(plan: StoryPlan, character_id: str) -> tuple[StoryPerformanceCue, ...]:
    """Return deterministic story and contextual reaction cues for one character.

    Character-specific beats target only that character. A beat without a
    character applies to every character in the scene and is useful for broad
    emotional transitions. Contextual reactions are derived from salient
    character-specific beats and never recursively trigger further reactions.
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

    result.extend(_reaction_cues_for(plan, definition.id))
    result.sort(key=lambda cue: cue.at)
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
