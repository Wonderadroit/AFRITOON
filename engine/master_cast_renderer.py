"""Render a multi-character ITANRA scene from canonical SVG masters."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping

from PIL import Image, ImageDraw, ImageFilter

from .camera_director import apply_camera, camera_at
from .cast_scene import CastScene
from .gaze import gaze_direction as _gaze_direction, interaction_strength as _interaction_strength
from .performance_renderer import performance_for_character
from .scene_background import render_background
from .semantic_svg_rig import render_semantic_character
from .svg_renderer import SVGRenderUnavailable, rasterize_svg
from .view_policy import resolve_view

W, H = 1080, 1920
DEFAULT_POSITIONS = {"tunde": (300.0, 1650.0, 0.82), "seyi": (540.0, 1650.0, 0.78), "mama": (780.0, 1650.0, 0.88)}
SOURCE_ASPECT = 1100.0 / 600.0


def _has_semantic_layers(path: Path) -> bool:
    try:
        return 'data-layer="' in path.read_text(encoding="utf-8")
    except OSError:
        return False


def gaze_direction(character: str, focus: str | None, positions: Mapping[str, tuple[float, float, float]] | None = None) -> str:
    """Resolve a bounded horizontal gaze target from scene positions."""
    return _gaze_direction(character, focus, positions or DEFAULT_POSITIONS)


def _temporal_gaze(focus: str | None, phase: str, motion_progress: float) -> str | None:
    """Acquire and release gaze with the acting beat instead of snapping."""
    if not focus or focus == "camera":
        return focus
    progress = max(0.0, min(1.0, float(motion_progress)))
    if phase == "anticipation":
        return None
    if phase == "recovery" and progress < 0.70:
        return None
    return focus


def _character_shadow_layer(positions: Mapping[str, tuple[float, float, float]], visible: Mapping[str, bool]) -> Image.Image:
    """Create soft contact shadows so characters sit in the environment."""
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(shadow, "RGBA")
    for cid, (x, baseline, scale) in positions.items():
        if not visible.get(cid, False):
            continue
        width = max(90, int(190 * scale))
        height = max(18, int(34 * scale))
        draw.ellipse((int(x - width / 2), int(baseline - height / 2), int(x + width / 2), int(baseline + height / 2)), fill=(30, 22, 20, 85))
    return shadow.filter(ImageFilter.GaussianBlur(14))


def _artwork_width(camera_shot: str, requested: int) -> int:
    """Give short-form portraits enough screen presence without crowding ensembles."""
    if requested != 390:
        return max(1, int(requested))
    return {"wide": 410, "medium": 455, "close": 515}.get(camera_shot, 410)


def render_master_cast(scene: CastScene, frame_time: float, repo_root: str | Path = ".", positions: Mapping[str, tuple[float, float, float]] | None = None, character_width: int = 390) -> Image.Image:
    """Compose canonical artwork, performance, staging and camera."""
    canvas = render_background(scene.name, frame_time)
    state = scene.state_at(frame_time)
    overrides = positions or {}
    scene_positions = overrides or {cid: (item.x, item.y, item.scale) for cid, item in state.characters.items()}
    visible_positions = {cid: (item.x, item.y, item.scale) for cid, item in state.characters.items() if item.visible}
    canvas = Image.alpha_composite(canvas, _character_shadow_layer(visible_positions, {cid: True for cid in visible_positions}))

    camera = camera_at(scene, frame_time)
    for character_id, instance in state.characters.items():
        if not instance.visible:
            continue
        if character_id in overrides:
            x, baseline, scale = overrides[character_id]
        elif instance.x != 540.0 or instance.y != 1150.0 or instance.scale != 1.0:
            x, baseline, scale = instance.x, instance.y, instance.scale
        else:
            x, baseline, scale = DEFAULT_POSITIONS.get(character_id, (540.0, 1650.0, 0.8))
        resolved = resolve_view(repo_root, character_id, instance.view)
        width = max(1, int(_artwork_width(camera.shot, character_width) * scale))
        height = max(1, int(round(width * SOURCE_ASPECT)))
        performance = performance_for_character(scene, character_id, frame_time)
        focus = _temporal_gaze(performance.focus, performance.phase, performance.motion_progress)
        gaze = gaze_direction(character_id, focus, scene_positions)
        strength = _interaction_strength(character_id, focus, scene_positions)
        dialogue = scene.dialogue_at(frame_time)
        is_speaking = dialogue is not None and dialogue.character == character_id
        if _has_semantic_layers(resolved.path):
            try:
                artwork = render_semantic_character(
                    resolved.path,
                    character_id,
                    performance.pose,
                    scale=1.0,
                    expression_name=performance.expression,
                    mouth_name=performance.mouth,
                    phase=performance.phase,
                    motion_progress=performance.motion_progress,
                    gaze=gaze,
                    interaction_strength=strength,
                    time=frame_time,
                    attention=focus is not None,
                    speaking=is_speaking,
                )
                artwork = artwork.resize((width, height), Image.Resampling.LANCZOS)
            except (SVGRenderUnavailable, ValueError, OSError):
                artwork = rasterize_svg(resolved.path, width, height)
        else:
            artwork = rasterize_svg(resolved.path, width, height)
        canvas.alpha_composite(artwork, (int(x - artwork.width / 2), int(baseline - artwork.height)))

    # Camera is the final composition pass so it moves the complete scene,
    # including shadows and background, rather than moving characters alone.
    return apply_camera(canvas, camera)
