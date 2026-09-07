"""Translate story beats into deterministic performance cues."""
from __future__ import annotations
from dataclasses import dataclass
from .acting_timing import timing_for
from .character_spec import character
from .story_director import StoryBeat, StoryPlan

EMOTION_TO_EXPRESSION = {
    "calm": "neutral", "happy": "happy", "funny": "happy", "curious": "curious",
    "nostalgic": "sad", "sad": "sad", "hopeful": "happy", "angry": "angry",
    "surprised": "surprised", "shocked": "shocked", "deadpan": "deadpan",
}

@dataclass(frozen=True)
class StoryPerformanceCue:
    at: float
    character: str
    action: str
    expression: str
    duration: float | None = None
    focus: str | None = None

REACTION_RULES = {
    ("tunde", "shock"): (("seyi", 0.35, "look", "deadpan"), ("mama", 0.65, "turn", "curious")),
    ("tunde", "freeze"): (("seyi", 0.40, "look_at_camera", "deadpan"), ("mama", 0.80, "look_at_camera", "deadpan")),
    ("tunde", "check_pocket"): (("seyi", 0.45, "look", "deadpan"),),
    ("mama", "angry"): (("tunde", 0.35, "freeze", "shocked"), ("seyi", 0.60, "look_at_camera", "deadpan")),
}

def _action_for(beat: StoryBeat) -> str:
    text = f"{beat.event} {beat.intent or ''}".lower()
    if any(word in text for word in ("panic", "power goes off", "shock", "shocked")): return "shock"
    if any(word in text for word in ("camera", "audience", "look at")): return "look_at_camera"
    if any(word in text for word in ("dance", "vibe")): return "dance"
    if any(word in text for word in ("laugh", "funny", "joke")): return "laugh"
    if any(word in text for word in ("talk", "speak", "say", "question")): return "talk"
    if any(word in text for word in ("turn", "notice", "look")): return "look"
    if any(word in text for word in ("freeze", "silence", "caught")): return "freeze"
    if any(word in text for word in ("approach", "come over", "walk to", "go to", "join")): return "look"
    return "idle"

def _expression_for(beat: StoryBeat) -> str:
    return EMOTION_TO_EXPRESSION.get(beat.emotion.strip().lower(), "neutral")

def _focus_for(beat: StoryBeat, actor: str, available: set[str]) -> str | None:
    text = f"{beat.event} {beat.intent or ''}".lower()
    if any(word in text for word in ("camera", "audience")):
        return "camera"
    for candidate in sorted(available - {actor}):
        if candidate in text:
            return candidate
    return None

def _reaction_cues_for(plan: StoryPlan, character_id: str) -> list[StoryPerformanceCue]:
    result: list[StoryPerformanceCue] = []
    target_definition = character(character_id)
    available = {"tunde", "seyi", "mama"}
    for beat in plan.beats:
        if beat.character is None:
            continue
        source = beat.character.strip().lower()
        if source == target_definition.id:
            continue
        source_action = _action_for(beat)
        for target, delay, action, expression in REACTION_RULES.get((source, source_action), ()):
            if target != target_definition.id or action not in target_definition.actions or expression not in target_definition.expressions:
                continue
            result.append(StoryPerformanceCue(float(beat.at) + float(delay), target_definition.id, action, expression, timing_for(target_definition.id, action).total, source))
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
        expression = _expression_for(beat)
        if expression not in definition.expressions:
            expression = definition.default_expression
        result.append(StoryPerformanceCue(beat.at, definition.id, action, expression, focus=_focus_for(beat, definition.id, available)))
    result.extend(_reaction_cues_for(plan, definition.id))
    result.sort(key=lambda cue: cue.at)
    return tuple(result)

def cue_at(cues: tuple[StoryPerformanceCue, ...], t: float) -> StoryPerformanceCue | None:
    current = None
    now = float(t)
    for cue in cues:
        if cue.at > now:
            break
        if cue.duration is not None and now >= cue.at + cue.duration:
            continue
        current = cue
    return current
