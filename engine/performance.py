"""Resolve a character's visible performance state at a moment in time."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from .acting_timing import acting_phase
from .actions import Action, action_at
from .face_state import face_state_at
from .mouth_timing import MouthCue


@dataclass(frozen=True)
class PerformanceState:
    pose: str
    action: str
    expression: str
    mouth: str
    phase: str = "hold"


def performance_at(
    t: float,
    actions: Iterable[Action] = (),
    face_timeline: Iterable[Mapping[str, object]] = (),
    mouth_cues: Iterable[MouthCue] = (),
    default_pose: str = "idle",
    default_expression: str = "neutral",
    character: str = "",
) -> PerformanceState:
    """Combine body, face, mouth and temporal acting state."""
    ordered_actions = sorted(actions, key=lambda item: item.time)
    action = action_at(ordered_actions, t)
    action_name = action.name if action is not None else default_pose
    phase = (
        acting_phase(character, action_name, float(t) - action.time)
        if action is not None
        else "hold"
    )
    face = face_state_at(face_timeline, t, default_expression)
    active_mouth = face.mouth.name
    for cue in mouth_cues:
        if cue.at <= float(t) < cue.at + cue.duration:
            active_mouth = cue.state.name
            break
    return PerformanceState(
        pose=action_name,
        action=action_name,
        expression=face.expression.name,
        mouth=active_mouth,
        phase=phase,
    )
