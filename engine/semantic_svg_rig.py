"""Runtime compositor for semantically grouped character SVG artwork."""

from __future__ import annotations

from pathlib import Path
import io
import xml.etree.ElementTree as ET

from PIL import Image

from .assets import LAYER_NAMES
from .character_pose import pose_for
from .svg_renderer import SVGRenderUnavailable, rasterize_svg

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


def _crop_with_origin(image: Image.Image) -> tuple[Image.Image, tuple[int, int]]:
    bbox = image.getbbox()
    if not bbox:
        return image, (0, 0)
    return image.crop(bbox), (bbox[0], bbox[1])


def render_semantic_character(
    master: str | Path,
    character_id: str,
    pose: str,
    scale: float = 1.0,
) -> Image.Image:
    """Render a master SVG through its semantic layers and pose transforms."""
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
        try:
            layer = rasterize_svg(io.BytesIO(svg.encode("utf-8")), SOURCE_W, SOURCE_H)
        except (SVGRenderUnavailable, OSError, ValueError):
            continue
        layer, origin = _crop_with_origin(layer)
        if not layer.getbbox():
            continue
        transform = pose_spec.layers[layer_name]
        if transform.scale != 1.0:
            layer = layer.resize(
                (max(1, round(layer.width * transform.scale)),
                 max(1, round(layer.height * transform.scale))),
                Image.Resampling.LANCZOS,
            )
        if transform.rotation:
            layer = layer.rotate(transform.rotation, Image.Resampling.BICUBIC, expand=True)
        # Transform coordinates describe the intended layer center in the
        # canonical 600x1100 character space, independent of cropped bounds.
        px = round(transform.x - layer.width / 2)
        py = round(transform.y - layer.height / 2)
        canvas.alpha_composite(layer, (px, py))

    return canvas
