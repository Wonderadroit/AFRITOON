"""Apply AFRITOON performance state to canonical character artwork."""

from __future__ import annotations

from dataclasses import dataclass
import math

from PIL import Image, ImageDraw

from .acting import acting_expression
from .cast_scene import CastScene
from .mouth_timing import mouth_cues
from .performance import PerformanceState


@dataclass(frozen=True)
class CharacterPerformanceProfile:
    skin: str
    face_center: tuple[float, float] = (300.0, 335.0)
    eye_y: float = 330.0
    left_eye_x: float = 245.0
    right_eye_x: float = 355.0
    mouth_y: float = 435.0


PROFILES = {
    "tunde": CharacterPerformanceProfile("#8b5a3c"),
    "seyi": CharacterPerformanceProfile("#6b3e24"),
    "mama": CharacterPerformanceProfile("#8b5a3c"),
}

CHARACTER_MOTION = {
    "tunde": {
        "idle": (0.0, 0.0, 1.0), "talk": (0.0, -2.0, 1.0),
        "shock": (-6.0, -10.0, 1.04), "shocked": (-6.0, -10.0, 1.04),
        "freeze": (0.0, 0.0, 1.0), "dance": (4.0, -6.0, 1.03),
        "vibe": (-2.0, -3.0, 1.02), "check_pocket": (3.0, 4.0, 1.0),
        "look_at_camera": (0.0, 0.0, 1.01), "laugh": (2.0, -4.0, 1.02),
        "stand": (0.0, 0.0, 1.0),
    },
    "seyi": {
        "idle": (0.0, 0.0, 1.0), "talk": (0.8, -1.0, 1.0),
        "look": (2.5, 0.0, 1.0), "turn": (5.0, 0.0, 1.0),
        "look_at_camera": (1.5, 0.0, 1.01), "laugh": (2.0, -2.0, 1.01),
        "freeze": (0.0, 0.0, 1.0),
    },
    "mama": {
        "idle": (0.0, 0.0, 1.0), "stand": (0.0, 0.0, 1.0),
        "talk": (-1.0, 1.0, 1.01), "turn": (-4.0, 0.0, 1.0),
        "look_at_camera": (-1.5, 0.0, 1.02), "angry": (0.0, 2.0, 1.01),
        "freeze": (0.0, 0.0, 1.0),
    },
}


def _face_scale(image: Image.Image) -> float:
    return image.width / 600.0


def _cover_face(draw: ImageDraw.ImageDraw, profile: CharacterPerformanceProfile, s: float, box: tuple[float, float, float, float]) -> None:
    draw.ellipse(tuple(int(v * s) for v in box), fill=profile.skin)


def _draw_expression(image: Image.Image, character: str, expression: str, mouth: str) -> None:
    profile = PROFILES.get(character, PROFILES["tunde"])
    s = _face_scale(image)
    draw = ImageDraw.Draw(image)
    stroke = max(2, round(8 * s))
    black = "#171717"
    white = "#ffffff"

    _cover_face(draw, profile, s, (202, 235, 288, 305))
    _cover_face(draw, profile, s, (312, 235, 398, 305))
    _cover_face(draw, profile, s, (235, 395, 365, 480))

    eye_y = profile.eye_y * s
    eye_h = 34 * s
    eye_w = 30 * s
    centers = (profile.left_eye_x * s, profile.right_eye_x * s)
    if expression in {"shocked", "surprised"}:
        eye_w, eye_h = 37 * s, 43 * s
    elif expression == "angry":
        eye_h = 27 * s
    elif expression == "deadpan":
        eye_h = 25 * s

    for cx in centers:
        draw.ellipse((cx - eye_w, eye_y - eye_h, cx + eye_w, eye_y + eye_h), fill=white, outline=black, width=stroke)
        pupil = 13 * s if expression in {"shocked", "surprised"} else 10 * s
        draw.ellipse((cx - pupil, eye_y - pupil, cx + pupil, eye_y + pupil), fill=black)

    brow_y = 275 * s
    if expression == "angry":
        draw.line((210 * s, 285 * s, 275 * s, 260 * s), fill=black, width=stroke)
        draw.line((325 * s, 260 * s, 390 * s, 285 * s), fill=black, width=stroke)
    elif expression == "deadpan":
        draw.line((210 * s, brow_y, 275 * s, brow_y), fill=black, width=stroke)
        draw.line((325 * s, brow_y, 390 * s, brow_y), fill=black, width=stroke)
    elif expression in {"shocked", "surprised", "curious"}:
        draw.line((210 * s, 260 * s, 275 * s, 250 * s), fill=black, width=stroke)
        draw.line((325 * s, 250 * s, 390 * s, 260 * s), fill=black, width=stroke)
    else:
        draw.line((210 * s, 270 * s, 275 * s, 258 * s), fill=black, width=stroke)
        draw.line((325 * s, 258 * s, 390 * s, 270 * s), fill=black, width=stroke)

    mx, my = 300 * s, profile.mouth_y * s
    if mouth in {"open", "talk_o"}:
        draw.ellipse((mx - 31 * s, my - 27 * s, mx + 31 * s, my + 27 * s), fill=black)
    elif mouth in {"small_open", "talk_e"}:
        draw.ellipse((mx - 23 * s, my - 17 * s, mx + 23 * s, my + 17 * s), fill=black)
    elif mouth in {"talk_a", "talk_rest"}:
        draw.ellipse((mx - 27 * s, my - 20 * s, mx + 27 * s, my + 20 * s), fill=black)
    elif mouth == "talk_m":
        draw.line((275 * s, my, 325 * s, my), fill=black, width=stroke)
    elif mouth in {"smile", "wide_smile", "happy", "laughing"}:
        draw.arc((255 * s, 405 * s, 345 * s, 465 * s), 10, 165, fill=black, width=stroke)
    elif mouth in {"sad", "tight"}:
        draw.arc((255 * s, 420 * s, 345 * s, 470 * s), 195, 345, fill=black, width=stroke)
    else:
        draw.line((270 * s, my, 330 * s, my), fill=black, width=stroke)


def apply_face_performance(image: Image.Image, state: PerformanceState, character: str) -> Image.Image:
    """Apply only expression and mouth; body movement belongs to the semantic rig."""
    image = image.convert("RGBA")
    _draw_expression(image, character, state.expression, state.mouth)
    return image


def apply_performance(image: Image.Image, state: PerformanceState, character: str) -> Image.Image:
    """Legacy whole-artwork performance path kept for fallback rendering."""
    image = apply_face_performance(image, state, character)
    motions = CHARACTER_MOTION.get(character, CHARACTER_MOTION["tunde"])
    rotation, y_shift, scale = motions.get(state.pose, motions.get("idle", (0.0, 0.0, 1.0)))
    if state.pose == "dance":
        rotation *= math.sin(1.0)
    if scale != 1.0:
        image = image.resize((max(1, round(image.width * scale)), max(1, round(image.height * scale))), Image.Resampling.LANCZOS)
    if rotation:
        image = image.rotate(rotation, resample=Image.Resampling.BICUBIC, expand=True)
    if y_shift:
        shifted = Image.new("RGBA", image.size, (0, 0, 0, 0))
        shifted.alpha_composite(image, (0, round(y_shift * image.width / 600.0)))
        image = shifted
    return image


def performance_for_character(scene: CastScene, character: str, frame_time: float) -> PerformanceState:
    """Resolve visible performance from canonical scene state + dialogue."""
    state = scene.state_at(frame_time)
    if character not in state.characters:
        raise ValueError(f"Character not present in scene: {character}")
    instance = state.characters[character]
    line = scene.dialogue_at(frame_time)
    mouth = ()
    if line is not None and line.character.strip().lower() == character:
        mouth = mouth_cues(line.text, line.at, line.duration)
    active = "closed"
    for cue in mouth:
        if cue.at <= frame_time < cue.at + cue.duration:
            active = cue.state.name
            break
    resolved_expression = acting_expression(character, instance.pose, instance.expression)
    return PerformanceState(
        pose=instance.pose,
        action=instance.pose,
        expression=resolved_expression,
        mouth=active,
    )
