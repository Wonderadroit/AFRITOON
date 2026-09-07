"""Runtime compositor for semantically grouped character SVG artwork."""

from __future__ import annotations

from pathlib import Path
import io
import xml.etree.ElementTree as ET

from PIL import Image

from .assets import LAYER_NAMES
from .character_pose import pose_for
from .expressions import expression
from .svg_renderer import SVGRenderUnavailable

SOURCE_W, SOURCE_H = 600, 1100
SVG_NS = "http://www.w3.org/2000/svg"


def _svg_namespace(tag: str) -> str:
    return tag.split("}", 1)[-1]


def _face_transform(expression_name: str, layer: str) -> str | None:
    """Return a small runtime transform for one authored facial layer.

    Expressions change the performance of the canonical artwork; they do not
    replace it with a second drawing.  The transforms deliberately stay small
    so the character's authored identity remains visible across states.
    """
    state = expression(expression_name)
    transforms: list[str] = []

    # Keep the face as one acting unit when an expression calls for a head tilt.
    head_angle = {
        "neutral": 0.0,
        "happy": -2.0,
        "curious": -4.0,
        "shocked": 2.0,
        "deadpan": 1.0,
        "angry": -2.0,
        "sad": 3.0,
        "laughing": -3.0,
        "surprised": 2.0,
    }[state.name]
    if layer in {"head", "ears", "front_hair", "left_eye", "right_eye", "left_brow", "right_brow", "nose", "mouth"} and head_angle:
        transforms.append(f"rotate({head_angle} 300 335)")

    if layer in {"left_eye", "right_eye"}:
        eye_scale_y = {
            "normal": 1.0,
            "happy": 0.78,
            "wide": 1.22,
            "closed": 0.48,
            "narrow": 0.72,
            "sad": 0.86,
        }.get(state.eyes, 1.0)
        transforms.append(f"translate(0 330) scale(1 {eye_scale_y}) translate(0 -330)")

    if layer in {"left_brow", "right_brow"}:
        brow_angle = {
            "normal": 0.0,
            "raised": 4.0 if layer == "left_brow" else -4.0,
            "flat": 0.0,
            "furrowed": -9.0 if layer == "left_brow" else 9.0,
            "raised_inner": -5.0 if layer == "left_brow" else 5.0,
        }.get(state.brows, 0.0)
        if state.brows == "flat":
            transforms.append(f"translate(0 272) scale(1 0.35) translate(0 -272)")
        elif brow_angle:
            transforms.append(f"rotate({brow_angle} 245 270)" if layer == "left_brow" else f"rotate({brow_angle} 355 270)")

    if layer == "mouth":
        mouth_scale_y = {
            "closed": 0.20,
            "smile": 0.72,
            "small_open": 0.70,
            "open": 1.18,
            "flat": 0.18,
            "tight": 0.28,
            "sad": 0.70,
            "wide_smile": 0.95,
        }.get(state.mouth, 1.0)
        transforms.append(f"translate(0 435) scale(1 {mouth_scale_y}) translate(0 -435)")

    return " ".join(transforms) or None


def _layer_svgs(master: Path, expression_name: str = "neutral") -> dict[str, str]:
    root = ET.fromstring(master.read_text(encoding="utf-8"))
    groups: dict[str, str] = {}
    for node in root.iter():
        if _svg_namespace(node.tag) != "g":
            continue
        layer = node.attrib.get("data-layer")
        if not layer:
            continue
        wrapper = ET.Element(f"{{{SVG_NS}}}svg", {
            "viewBox": f"0 0 {SOURCE_W} {SOURCE_H}",
        })
        wrapper_group = ET.fromstring(ET.tostring(node, encoding="unicode"))
        transform = _face_transform(expression_name, layer)
        if transform:
            wrapper_group.set("transform", transform)
        wrapper_group.set("stroke", "#171717")
        wrapper_group.set("stroke-width", "12")
        wrapper_group.set("stroke-linejoin", "round")
        wrapper_group.set("stroke-linecap", "round")
        wrapper.append(wrapper_group)
        groups[layer] = ET.tostring(wrapper, encoding="unicode")
    return groups


def _rasterize_svg_text(source: str) -> Image.Image:
    try:
        import cairosvg
    except ImportError as exc:
        raise SVGRenderUnavailable("CairoSVG is required for semantic SVG rendering") from exc
    png = cairosvg.svg2png(
        bytestring=source.encode("utf-8"),
        output_width=SOURCE_W,
        output_height=SOURCE_H,
    )
    return Image.open(io.BytesIO(png)).convert("RGBA")


def _layer_anchor(layer: Image.Image) -> tuple[Image.Image, float, float] | None:
    """Return the visible layer plus its canonical source-space visual center."""
    bbox = layer.getbbox()
    if not bbox:
        return None
    left, top, right, bottom = bbox
    cropped = layer.crop(bbox)
    return cropped, (left + right) / 2, (top + bottom) / 2


def _transform_layer(
    layer: Image.Image,
    *,
    source_anchor: tuple[float, float],
    target_anchor: tuple[float, float],
    rotation: float,
    scale: float,
) -> tuple[Image.Image, tuple[int, int]]:
    """Transform a layer around its authored source-space anchor."""
    prepared = _layer_anchor(layer)
    if prepared is None:
        return layer, (round(target_anchor[0]), round(target_anchor[1]))
    cropped, _, _ = prepared
    del source_anchor
    if scale != 1.0:
        cropped = cropped.resize(
            (max(1, round(cropped.width * scale)),
             max(1, round(cropped.height * scale))),
            Image.Resampling.LANCZOS,
        )
    if rotation:
        cropped = cropped.rotate(
            rotation,
            resample=Image.Resampling.BICUBIC,
            expand=True,
        )

    px = round(target_anchor[0] - cropped.width / 2)
    py = round(target_anchor[1] - cropped.height / 2)
    return cropped, (px, py)


def render_semantic_character(
    master: str | Path,
    character_id: str,
    pose: str,
    scale: float = 1.0,
    expression_name: str = "neutral",
) -> Image.Image:
    """Render canonical artwork with semantic body pose and facial performance."""
    master_path = Path(master)
    groups = _layer_svgs(master_path, expression_name=expression_name)
    if not groups:
        raise ValueError(f"Master artwork has no semantic layers: {master_path}")

    canvas = Image.new("RGBA", (SOURCE_W, SOURCE_H), (0, 0, 0, 0))
    pose_spec = pose_for(character_id, pose, scale=scale)
    canonical_pose = pose_for(character_id, "idle", scale=1.0)

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
        transformed, position = _transform_layer(
            layer,
            source_anchor=(source_x, source_y),
            target_anchor=(target_x, target_y),
            rotation=current.rotation,
            scale=current.scale,
        )
        if transformed.getbbox():
            canvas.alpha_composite(transformed, position)

    return canvas
