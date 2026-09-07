"""Convert story beats into deterministic character performance cues."""

from __future__ import annotations

from dataclasses import dataclass

from .acting_timing import timing_for
from .character_spec import character
from .story_director import StoryBeat, StoryPlan


@dataclass(frozen=True)
class StoryPerformanceCue:
    at: float
    character: str
    action: str
    expression: str
    duration: float | None = None
    focus: str | None = None


EMOTION_TO_EXPRESSION = {
    "calm": "neutral",
    "happy": "happy",
    "funny": "happy",
    "shocked": "shocked",
    "surprised": "surprised",
    "deadpan": "deadpan",
    "angry": "angry",
    "sad": "sad",
    "curious": "curious",
}

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

APPROACH_WORDS = ("approach", "comes over", "come over", "walk to", "walks to", "go to", "goes to", "join", "joins")


def _expression_for(beat: StoryBeat) -> str:
    return EMOTION_TO_EXPRESSION.get(beat.emotion.strip().lower(), "neutral")


def _action_for(beat: StoryBeat) -> str:
    text = f"{beat.event} {beat.intent or ''}".lower()
    if any(word in text for word in ("panic", "power goes off", "shock")):
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
    if any(word in text for word in APPROACH_WORDS):
        return "look"
    return "idle"


def _focus_for(beat: StoryBeat, character_id: str, available: set[str]) -> str | None:
    text = f"{beat.event} {beat.intent or ''}".lower()
    if "camera" in text or "audience" in text:
        return "camera"
    for candidate in sorted(available - {character_id}):
        if candidate in text:
            return candidate
    return None


def _reaction_cues_for(plan: StoryPlan, source_character: str) -> list[StoryPerformanceCue]:
    result: list[StoryPerformanceCue] = []
    for beat in plan.beats:
        if beat.character is None or beat.character.strip().lower() != source_character:
            continue
        source_action = _action_for(beat)
        for target, delay, action, expression_name in REACTION_RULES.get((source_character, source_action), ()):
            duration = timing_for(target, action).total
            result.append(StoryPerformanceCue(
                at=beat.at + delay,
                character=target,
                action=action,
                expression=expression_name,
                duration=duration,
                focus=source_character,
            ))
        text = f"{beat.event} {beat.intent or ''}".lower()
        if any(word in text for word in APPROACH_WORDS):
            for target in ("tunde", "seyi", "mama"):
                if target == source_character or target not in text:
                    continue
                result.append(StoryPerformanceCue(
                    at=beat.at + 0.25,
                    character=source_character,
                    action="look",
                    expression=_expression_for(beat),
                    focus=target,
                    duration=timing_for(source_character, "look").total,
                ))
    return result


def cues_for(plan: StoryPlan, character_id: str) -> tuple[StoryPerformanceCue, ...]:
    definition = character(character_id)
    result: list[StoryPerformanceCue] = []
    available = {"tunde", "seyi", "mama"}
    for beat in plan.beats:
        if beat.character is not None and beat.character.strip().lower() != definition.id:
            continue
        action = _action_for(beat)
        if action not in definition.actions:
            action = definition.default_pose
        expression_name = _expression_for(beat)
        if expression_name not in definition.expressions:
            expression_name = definition.default_expression
        result.append(StoryPerformanceCue(
            beat.at,
            definition.id,
            action,
            expression_name,
            focus=_focus_for(beat, definition.id, available),
        ))
    result.extend(_reaction_cues_for(plan, definition.id))
    result.sort(key=lambda cue: cue.at)
    return tuple(result)


def cue_at(cues: tuple[StoryPerformanceCue, ...], t: float) -> StoryPerformanceCue | None:
    current = None
    now = float(t)
    for cue in cues:
        if cue.at > now:
            break
        # Acting windows are sampled at animation-frame precision. Treat a
        # sub-frame boundary as expired so authored decimal durations do not
        # keep a cue alive for an extra visible frame.
        if cue.duration is not None and now >= cue.at + cue.duration - 0.01:
            if abs(now - cue.at) >= 0.01:
                continue
        current = cue
    return current
