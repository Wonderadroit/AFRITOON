"""Runtime compositor for semantically grouped character SVG artwork."""

from __future__ import annotations

from pathlib import Path
import io
import xml.etree.ElementTree as ET

from PIL import Image

from .assets import LAYER_NAMES
from .character_pose import pose_for
from .svg_renderer import SVGRenderUnavailable

SOURCE_W, SOURCE_H = 600, 1100
SVG_NS = "http://www.w3.org/2000/svg"


def _svg_namespace(tag: str) -> str:
    return tag.split("}", 1)[-1]


def _layer_svgs(master: Path) -> dict[str, str]:
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


def _transform_layer(layer: Image.Image, x: float, y: float, rotation: float, scale: float) -> tuple[Image.Image, tuple[int, int]]:
    """Transform a cropped layer while keeping its authored anchor stable.

    The semantic SVG is rasterized in the canonical 600x1100 coordinate space.
    We crop only for efficiency, but compute the crop's source-space center
    before transforming it.  The transformed center is then explicitly mapped
    to the pose target (x, y). This prevents rotation/scale from changing the
    layer's placement merely because its transparent margins changed.
    """
    bbox = layer.getbbox()
    if not bbox:
        return layer, (round(x), round(y))

    layer = layer.crop(bbox)
    anchor_x = layer.width / 2
    anchor_y = layer.height / 2

    if scale != 1.0:
        layer = layer.resize(
            (max(1, round(layer.width * scale)),
             max(1, round(layer.height * scale))),
            Image.Resampling.LANCZOS,
        )

    if rotation:
        layer = layer.rotate(
            rotation,
            resample=Image.Resampling.BICUBIC,
            expand=True,
        )

    # All transforms above are centered on the layer's authored visual center.
    # Mapping that center to the pose target keeps the semantic part stable.
    px = round(x - layer.width / 2)
    py = round(y - layer.height / 2)
    return layer, (px, py)


def render_semantic_character(
    master: str | Path,
    character_id: str,
    pose: str,
    scale: float = 1.0,
) -> Image.Image:
    """Render a master SVG through semantic layers and a character pose."""
    master_path = Path(master)
    groups = _layer_svgs(master_path)
    if not groups:
        raise ValueError(f"Master artwork has no semantic layers: {master_path}")

    canvas = Image.new("RGBA", (SOURCE_W, SOURCE_H), (0, 0, 0, 0))
    pose_spec = pose_for(character_id, pose, scale=scale)

    for layer_name in LAYER_NAMES:
        svg = groups.get(layer_name)
        if not svg:
            continue
        layer = _rasterize_svg_text(svg)
        transform = pose_spec.layers[layer_name]
        layer, position = _transform_layer(
            layer,
            transform.x,
            transform.y,
            transform.rotation,
            transform.scale,
        )
        if layer.getbbox():
            canvas.alpha_composite(layer, position)

    return canvas
