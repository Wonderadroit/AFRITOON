"""Runtime compositor for semantically grouped character SVG artwork."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import io
import xml.etree.ElementTree as ET

from PIL import Image

from .acting_dynamics import micro_motion
from .assets import LAYER_NAMES
from .character_pose import pose_for_motion, pose_for_phase
from .expressions import expression
from .svg_renderer import SVGRenderUnavailable

SOURCE_W, SOURCE_H = 600, 1100
SVG_NS = "http://www.w3.org/2000/svg"


def _svg_namespace(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _interaction_geometry(gaze: str, phase: str, motion_progress: float, strength: float = 1.0) -> tuple[float, float]:
    direction = {"left": -1.0, "right": 1.0, "center": 0.0}.get(gaze, 0.0)
    progress = max(0.0, min(1.0, float(motion_progress)))
    strength = max(0.0, min(1.0, float(strength)))
    phase_amount = {"anticipation": 0.0, "action": progress, "hold": 1.0, "recovery": max(0.0, 1.0 - progress)}.get(phase, progress)
    amount = max(0.0, min(1.0, phase_amount)) * strength
    return direction * 3.0 * amount, direction * 1.0 * amount


def _face_transform(expression_name: str, layer: str, mouth_name: str | None = None, gaze: str = "center", phase: str = "hold", motion_progress: float = 1.0, interaction_strength: float = 1.0, blink: float = 0.0, head_tilt: float = 0.0) -> str | None:
    state = expression(expression_name)
    transforms: list[str] = []
    expression_head_angle = {"neutral": 0.0, "happy": -2.0, "curious": -4.0, "shocked": 2.0, "deadpan": 1.0, "angry": -2.0, "sad": 3.0, "laughing": -3.0, "surprised": 2.0}[state.name]
    interaction_head_angle, _ = _interaction_geometry(gaze, phase, motion_progress, interaction_strength)
    head_angle = expression_head_angle + interaction_head_angle + max(-1.6, min(1.6, float(head_tilt)))
    face_layers = {"head", "ears", "front_hair", "left_eye", "right_eye", "left_brow", "right_brow", "nose", "mouth"}
    if layer in face_layers and head_angle:
        transforms.append(f"rotate({head_angle} 300 335)")
    if layer in {"left_eye", "right_eye"}:
        eye_scale_y = {"normal": 1.0, "happy": 0.78, "wide": 1.22, "closed": 0.48, "narrow": 0.72, "sad": 0.86}.get(state.eyes, 1.0)
        if blink > 0.0:
            eye_scale_y *= max(0.12, 1.0 - 0.88 * min(1.0, blink))
        transforms.append(f"translate(0 330) scale(1 {eye_scale_y}) translate(0 -330)")
        gaze_shift = {"left": -9.0, "right": 9.0, "center": 0.0}.get(gaze, 0.0) * max(0.0, min(1.0, float(interaction_strength)))
        if gaze_shift:
            transforms.append(f"translate({gaze_shift} 0)")
    if layer in {"left_brow", "right_brow"}:
        brow_angle = {"normal": 0.0, "raised": 4.0 if layer == "left_brow" else -4.0, "flat": 0.0, "furrowed": -9.0 if layer == "left_brow" else 9.0, "raised_inner": -5.0 if layer == "left_brow" else 5.0}.get(state.brows, 0.0)
        if state.brows == "flat":
            transforms.append("translate(0 272) scale(1 0.35) translate(0 -272)")
        elif brow_angle:
            pivot = "245 270" if layer == "left_brow" else "355 270"
            transforms.append(f"rotate({brow_angle} {pivot})")
    if layer == "mouth":
        active_mouth = mouth_name or state.mouth
        mouth_scale_y = {"closed": 0.20, "smile": 0.72, "small_open": 0.70, "open": 1.18, "flat": 0.18, "tight": 0.28, "sad": 0.70, "wide_smile": 0.95, "talk_o": 1.05, "talk_e": 0.72, "talk_a": 0.90, "talk_m": 0.18, "talk_rest": 0.55}.get(active_mouth, 1.0)
        transforms.append(f"translate(0 435) scale(1 {mouth_scale_y}) translate(0 -435)")
    return " ".join(transforms) or None


def _set_mouth_variant_visibility(root: ET.Element, mouth_name: str | None) -> None:
    """Select one authored mouth shape while preserving legacy masters."""
    variants = [node for node in root.iter() if node.attrib.get("data-mouth")]
    if not variants:
        return
    names = {node.attrib["data-mouth"] for node in variants}
    selected = mouth_name if mouth_name in names else next(iter(names))
    for node in variants:
        node.set("display", "inline" if node.attrib.get("data-mouth") == selected else "none")


@lru_cache(maxsize=1024)
def _layer_svgs_cached(master_name: str, expression_name: str, mouth_name: str | None, gaze: str, phase: str, motion_progress: float, interaction_strength: float, blink: float, head_tilt: float) -> tuple[tuple[str, str], ...]:
    master = Path(master_name)
    root = ET.fromstring(master.read_text(encoding="utf-8"))
    defs = [ET.fromstring(ET.tostring(node, encoding="unicode")) for node in root if _svg_namespace(node.tag) == "defs"]
    groups: dict[str, str] = {}
    for node in root.iter():
        if _svg_namespace(node.tag) != "g":
            continue
        layer = node.attrib.get("data-layer")
        if not layer:
            continue
        wrapper = ET.Element(f"{{{SVG_NS}}}svg", {"viewBox": f"0 0 {SOURCE_W} {SOURCE_H}"})
        for definition in defs:
            wrapper.append(ET.fromstring(ET.tostring(definition, encoding="unicode")))
        wrapper_group = ET.fromstring(ET.tostring(node, encoding="unicode"))
        if layer == "mouth":
            _set_mouth_variant_visibility(wrapper_group, mouth_name or expression(expression_name).mouth)
        transform = _face_transform(expression_name, layer, mouth_name, gaze, phase, motion_progress, interaction_strength, blink, head_tilt)
        if transform:
            wrapper_group.set("transform", transform)
        wrapper.append(wrapper_group)
        groups[layer] = ET.tostring(wrapper, encoding="unicode")
    return tuple(groups.items())


def _quantize(value: float, step: float) -> float:
    return round(round(float(value) / step) * step, 4)


def _layer_svgs(master: Path, expression_name: str = "neutral", mouth_name: str | None = None, gaze: str = "center", phase: str = "hold", motion_progress: float = 1.0, interaction_strength: float = 1.0, blink: float = 0.0, head_tilt: float = 0.0) -> dict[str, str]:
    return dict(_layer_svgs_cached(str(master.resolve()), expression_name, mouth_name, gaze, phase, _quantize(motion_progress, 0.08), _quantize(interaction_strength, 0.05), _quantize(blink, 0.10), _quantize(head_tilt, 0.20)))


@lru_cache(maxsize=1024)
def _rasterize_svg_cached(source: str) -> Image.Image:
    try:
        import cairosvg
    except ImportError as exc:
        raise SVGRenderUnavailable("CairoSVG is required for semantic SVG rendering") from exc
    png = cairosvg.svg2png(bytestring=source.encode("utf-8"), output_width=SOURCE_W, output_height=SOURCE_H)
    return Image.open(io.BytesIO(png)).convert("RGBA")


def _rasterize_svg_text(source: str) -> Image.Image:
    return _rasterize_svg_cached(source).copy()


def _layer_anchor(layer: Image.Image) -> tuple[Image.Image, float, float] | None:
    bbox = layer.getbbox()
    if not bbox:
        return None
    left, top, right, bottom = bbox
    return layer.crop(bbox), (left + right) / 2, (top + bottom) / 2


def _transform_layer(layer: Image.Image, *, target_anchor: tuple[float, float], rotation: float, scale: float) -> tuple[Image.Image, tuple[int, int]]:
    prepared = _layer_anchor(layer)
    if prepared is None:
        return layer, (round(target_anchor[0]), round(target_anchor[1]))
    cropped, _, _ = prepared
    if scale != 1.0:
        cropped = cropped.resize((max(1, round(cropped.width * scale)), max(1, round(cropped.height * scale))), Image.Resampling.LANCZOS)
    if rotation:
        cropped = cropped.rotate(rotation, resample=Image.Resampling.BICUBIC, expand=True)
    return cropped, (round(target_anchor[0] - cropped.width / 2), round(target_anchor[1] - cropped.height / 2))


def render_semantic_character(master: str | Path, character_id: str, pose: str, scale: float = 1.0, expression_name: str = "neutral", mouth_name: str | None = None, phase: str = "hold", motion_progress: float | None = None, gaze: str = "center", interaction_strength: float = 1.0, time: float = 0.0, attention: bool | None = None, speaking: bool | None = None) -> Image.Image:
    """Render canonical artwork with authored performance plus subtle life motion."""
    master_path = Path(master)
    effective_progress = 1.0 if motion_progress is None else motion_progress
    effective_strength = max(0.0, min(1.0, float(interaction_strength)))
    active_mouth = mouth_name or expression(expression_name).mouth
    is_speaking = bool(speaking) if speaking is not None else active_mouth not in {"closed", "talk_rest"}
    is_attentive = bool(attention) if attention is not None else gaze != "center"
    dynamics = micro_motion(character_id, time, attention=is_attentive, speaking=is_speaking, expression=expression_name)
    groups = _layer_svgs(master_path, expression_name=expression_name, mouth_name=mouth_name, gaze=gaze, phase=phase, motion_progress=effective_progress, interaction_strength=effective_strength, blink=dynamics.blink, head_tilt=dynamics.head_tilt)
    if not groups:
        raise ValueError(f"Master artwork has no semantic layers: {master_path}")
    canvas = Image.new("RGBA", (SOURCE_W, SOURCE_H), (0, 0, 0, 0))
    if motion_progress is None:
        pose_spec = pose_for_phase(character_id, pose, phase, scale=scale)
    else:
        pose_spec = pose_for_motion(character_id, pose, effective_progress, scale=scale)
    canonical_pose = pose_for_phase(character_id, "idle", "hold", scale=1.0)
    _, body_turn = _interaction_geometry(gaze, phase, effective_progress, effective_strength)
    breath = dynamics.breath
    weight = dynamics.weight
    speech = dynamics.speech
    for layer_name in LAYER_NAMES:
        svg = groups.get(layer_name)
        if not svg:
            continue
        layer = _rasterize_svg_text(svg)
        prepared = _layer_anchor(layer)
        if prepared is None:
            continue
        _, source_x, source_y = prepared
        current = pose_spec.layers[layer_name]
        canonical = canonical_pose.layers[layer_name]
        target_x = source_x + (current.x - canonical.x)
        target_y = source_y + (current.y - canonical.y)
        if layer_name in {"torso", "left_arm", "right_arm", "legs"}:
            target_y += breath * 1.25
            target_x += weight * 1.25
            if is_speaking:
                target_y += speech * 0.65
        elif layer_name in {"head", "ears", "front_hair", "left_eye", "right_eye", "left_brow", "right_brow", "nose", "mouth"}:
            target_y += breath * 0.75
            target_x += weight * 0.55
            if is_speaking and layer_name in {"head", "ears", "front_hair"}:
                target_y += speech * 0.45
        body_rotation = body_turn if layer_name in {"torso", "left_arm", "right_arm"} else 0.0
        micro_scale = 1.0 + (0.004 * breath if layer_name == "torso" else 0.0)
        transformed, position = _transform_layer(layer, target_anchor=(target_x, target_y), rotation=current.rotation + body_rotation, scale=current.scale * micro_scale)
        if transformed.getbbox():
            canvas.alpha_composite(transformed, position)
    return canvas
