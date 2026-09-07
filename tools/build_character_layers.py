"""Build deterministic semantic SVG/PNG layers from character masters.

The character masters are the source of truth. Layer extraction therefore
uses each master's ``data-layer`` names instead of brittle child indexes.
"""

from __future__ import annotations

import argparse
import copy
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)

# Fixed runtime contract. A master may intentionally omit a layer (for
# example back_hair when the hairstyle is fully represented by front_hair).
LAYERS = (
    "back_hair", "legs", "shoes", "torso", "left_arm", "right_arm", "neck",
    "head", "ears", "front_hair", "left_eye", "right_eye", "left_brow",
    "right_brow", "nose", "mouth",
)
CHARACTERS = ("tunde", "seyi", "mama")


def children(master: Path):
    root = ET.parse(master).getroot()
    groups = [n for n in root if n.tag.rsplit("}", 1)[-1] == "g"]
    if not groups:
        raise ValueError(f"No drawing group found: {master}")
    return root, list(groups[0])


def semantic_nodes(nodes: list[ET.Element], cid: str) -> dict[str, list[ET.Element]]:
    """Return master drawing groups keyed by their semantic data-layer name."""
    found: dict[str, list[ET.Element]] = {}
    for node in nodes:
        layer = node.attrib.get("data-layer")
        if not layer:
            continue
        if layer in found:
            raise ValueError(f"{cid} master defines duplicate data-layer '{layer}'")
        found[layer] = [node]

    unknown = sorted(set(found) - set(LAYERS))
    if unknown:
        raise ValueError(f"{cid} master defines unknown data-layer(s): {', '.join(unknown)}")
    return found


def write_layer(root: ET.Element, nodes: list[ET.Element], target: Path):
    out = ET.Element(f"{{{NS}}}svg", {"viewBox": root.attrib.get("viewBox", "0 0 600 1100")})
    group = ET.SubElement(out, f"{{{NS}}}g")
    for node in nodes:
        group.append(copy.deepcopy(node))
    target.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(out).write(target, encoding="utf-8", xml_declaration=True)


def write_png(svg_path: Path, png_path: Path) -> None:
    try:
        import cairosvg
    except ImportError as exc:
        raise RuntimeError("PNG output requires CairoSVG: pip install cairosvg") from exc
    png_path.parent.mkdir(parents=True, exist_ok=True)
    cairosvg.svg2png(url=str(svg_path), write_to=str(png_path), output_width=600, output_height=1100)


def build(cid: str, png: bool = False) -> None:
    if cid not in CHARACTERS:
        raise ValueError(f"Unknown character: {cid}")

    master = ROOT / "assets" / "characters" / cid / "art" / f"{cid}_front.svg"
    root, nodes = children(master)
    semantic = semantic_nodes(nodes, cid)

    output_root = ROOT / "assets" / "characters" / cid / "layers" / "front"
    for layer in LAYERS:
        # Empty semantic layers are valid and preserve the fixed runtime
        # contract without inventing geometry absent from the master.
        svg_path = output_root / f"{layer}.svg"
        write_layer(root, semantic.get(layer, []), svg_path)
        if png:
            write_png(svg_path, output_root / f"{layer}.png")

    expected = [output_root / f"{layer}.svg" for layer in LAYERS]
    if not all(path.exists() for path in expected):
        raise RuntimeError(f"Layer build incomplete for {cid}")
    print(f"built {cid}: {len(expected)}/16 SVG layers" + (" + PNG" if png else ""))


def main() -> int:
    parser = argparse.ArgumentParser(description="Build AFRITOON front-view character layers")
    parser.add_argument("--character", choices=(*CHARACTERS, "all"), default="all")
    parser.add_argument("--png", action="store_true", help="Also rasterize layers to PNG")
    args = parser.parse_args()
    characters = CHARACTERS if args.character == "all" else (args.character,)
    for cid in characters:
        build(cid, png=args.png)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
