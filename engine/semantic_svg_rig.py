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
        wrapper = ET.Element("svg", {
            "xmlns": "http://www.w3.org/2000/svg",
            "viewBox": f"0 0 {SOURCE_W} {SOURCE_H}",
        })
        wrapper.append(ET.fromstring(ET.tostring(node, encoding="unicode")))
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
        bbox = layer.getbbox()
        if not bbox:
            continue
        layer = layer.crop(bbox)
        transform = pose_spec.layers[layer_name]
        if transform.scale != 1.0:
            layer = layer.resize(
                (max(1, round(layer.width * transform.scale)),
                 max(1, round(layer.height * transform.scale))),
                Image.Resampling.LANCZOS,
            )
        if transform.rotation:
            layer = layer.rotate(
                transform.rotation,
                resample=Image.Resampling.BICUBIC,
                expand=True,
            )
        px = round(transform.x - layer.width / 2)
        py = round(transform.y - layer.height / 2)
        canvas.alpha_composite(layer, (px, py))

    return canvas
