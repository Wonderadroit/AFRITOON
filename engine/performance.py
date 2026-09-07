"""Resolve a character's visible performance state at a moment in time."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from .acting_timing import acting_motion
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
    motion_progress: float = 1.0
    focus: str | None = None


def performance_at(
    t: float,
    actions: Iterable[Action] = (),
    face_timeline: Iterable[Mapping[str, object]] = (),
    mouth_cues: Iterable[MouthCue] = (),
    default_pose: str = "idle",
    default_expression: str = "neutral",
    character: str = "",
) -> PerformanceState:
    """Combine body, face, mouth and continuous temporal acting state."""
    ordered_actions = sorted(actions, key=lambda item: item.time)
    action = action_at(ordered_actions, t)
    action_name = action.name if action is not None else default_pose
    if action is not None:
        phase, _, motion_progress = acting_motion(character, action_name, float(t) - action.time)
    else:
        phase, motion_progress = "hold", 1.0

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
        motion_progress=motion_progress,
    )
