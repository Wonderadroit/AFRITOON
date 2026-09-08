"""Deterministic shot planning for short-form ITANRA scenes."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Mapping

from .cast_scene import CastScene

W, H = 1080.0, 1920.0


@dataclass(frozen=True)
class CameraState:
    """Camera target after deterministic story-aware shot selection."""

    scale: float
    center_x: float
    center_y: float
    shot: str
    focus: str | None


def _visible_positions(scene: CastScene, t: float) -> dict[str, tuple[float, float, float]]:
    state = scene.state_at(t)
    return {
        cid: (item.x, item.y, item.scale)
        for cid, item in state.characters.items()
        if item.visible
    }


def _latest_story_focus(scene: CastScene, t: float) -> str | None:
    plan = scene.story_plan
    if plan is None or not plan.beats:
        return None
    active = [beat for beat in plan.beats if beat.at <= float(t)]
    if not active:
        return None
    return active[-1].character


def _story_event(scene: CastScene, t: float) -> str:
    plan = scene.story_plan
    if plan is None or not plan.beats:
        return ""
    active = [beat for beat in plan.beats if beat.at <= float(t)]
    return str(active[-1].event).strip().lower() if active else ""


def _target(scene: CastScene, t: float) -> CameraState:
    positions = _visible_positions(scene, t)
    dialogue = scene.dialogue_at(t)
    speaker = dialogue.character if dialogue is not None else None
    event = _story_event(scene, t)
    focus = speaker or _latest_story_focus(scene, t)
    if focus not in positions:
        focus = None

    # The default is a readable ensemble frame. Dialogue then earns a
    # medium-close shot; high-impact beats get a slightly stronger push-in.
    scale = 1.0
    shot = "wide"
    if focus is not None:
        scale = 1.08
        shot = "medium"
    if event in {"power_goes_off", "exposure", "tunde_realizes_problem"} and focus is not None:
        scale = 1.16
        shot = "close"

    if focus is None:
        if positions:
            xs = [item[0] for item in positions.values()]
            ys = [item[1] for item in positions.values()]
            center_x = sum(xs) / len(xs)
            center_y = min(1100.0, sum(ys) / len(ys) - 360.0)
        else:
            center_x, center_y = W / 2.0, 1040.0
    else:
        x, baseline, _ = positions[focus]
        # Aim above the baseline so the face and upper body carry the shot.
        center_x = float(x)
        center_y = float(baseline) - 520.0

    return CameraState(scale=scale, center_x=center_x, center_y=center_y, shot=shot, focus=focus)


def _smoothstep(value: float) -> float:
    x = max(0.0, min(1.0, value))
    return x * x * (3.0 - 2.0 * x)


def _blend(a: CameraState, b: CameraState, amount: float) -> CameraState:
    p = _smoothstep(amount)
    return CameraState(
        scale=a.scale + (b.scale - a.scale) * p,
        center_x=a.center_x + (b.center_x - a.center_x) * p,
        center_y=a.center_y + (b.center_y - a.center_y) * p,
        shot=b.shot if p >= 0.5 else a.shot,
        focus=b.focus if p >= 0.5 else a.focus,
    )


def camera_at(scene: CastScene, t: float, *, transition: float = 0.32) -> CameraState:
    """Resolve a shot with a short eased transition around cue boundaries.

    Camera movement is deliberately bounded: no arbitrary shake, no random
    zooms, and no dependence on an LLM. The dialogue/story timeline is the
    source of shot intent.
    """
    now = max(0.0, min(float(t), scene.duration))
    target = _target(scene, now)
    if transition <= 0.0:
        return target

    # Find the most recent point where the target camera intent changed.
    probe = min(now, 0.05)
    previous = _target(scene, max(0.0, now - transition),)
    if previous == target:
        return target
    amount = min(1.0, probe / transition) if now < transition else 1.0
    if now >= transition:
        # Search backward just far enough to identify whether we are entering
        # a new dialogue/story state. A coarse deterministic probe is enough
        # because scene cues are authored at human-readable times.
        previous = _target(scene, max(0.0, now - min(transition, 0.16)))
        return _blend(previous, target, 0.72)
    return _blend(previous, target, amount)


def apply_camera(image, camera: CameraState):
    """Apply a bounded camera crop while preserving the output resolution."""
    if camera.scale <= 1.0001:
        return image

    width, height = image.size
    scale = max(1.0, min(1.18, float(camera.scale)))
    crop_w = width / scale
    crop_h = height / scale
    left = max(0.0, min(width - crop_w, camera.center_x - crop_w / 2.0))
    top = max(0.0, min(height - crop_h, camera.center_y - crop_h / 2.0))
    box = (
        int(round(left)),
        int(round(top)),
        int(round(left + crop_w)),
        int(round(top + crop_h)),
    )
    cropped = image.crop(box)
    return cropped.resize((width, height), image.Resampling.LANCZOS)
