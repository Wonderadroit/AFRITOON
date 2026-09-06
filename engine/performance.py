"""Resolve a character's visible performance state at a moment in time."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from .actions import action_at
from .expressions import expression
from .face_state import face_state_at
from .mouth_timing import MouthCue


@dataclass(frozen=True)
class PerformanceState:
    pose: str
    action: str
    expression: str
    mouth: str


def performance_at(
    t: float,
    actions: Iterable[Mapping[str, object]] = (),
    face_timeline: Iterable[Mapping[str, object]] = (),
    mouth_cues: Iterable[MouthCue] = (),
    default_pose: str = "idle",
    default_expression: str = "neutral",
) -> PerformanceState:
    """Combine body, face and mouth state without coupling them to a renderer."""
    action = action_at(actions, t)
    action_name = action.name if action is not None else default_pose
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
    )
