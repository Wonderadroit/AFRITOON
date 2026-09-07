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
    """Transform a layer around its authored source-space anchor.

    The important distinction is that pose coordinates are interpreted as
    offsets from the canonical artwork, not as guesses for the cropped bitmap
    dimensions.  This means changing an SVG's transparent margins cannot make
    an arm, eye, or head jump when the same pose is reused.
    """
    prepared = _layer_anchor(layer)
    if prepared is None:
        return layer, (round(target_anchor[0]), round(target_anchor[1]))
    cropped, source_x, source_y = prepared

    # The visible center is the stable default pivot until explicit artwork
    # pivots are authored. Keep the source anchor separate from the target
    # anchor so the pose system remains expressed in canonical coordinates.
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
) -> Image.Image:
    """Render a master SVG through semantic layers and a character pose."""
    master_path = Path(master)
    groups = _layer_svgs(master_path)
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
