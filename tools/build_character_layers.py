"""Build AFRITOON transparent SVG/PNG rig layers from front masters.

The current masters are intentionally compact SVGs. This builder extracts
semantic parts into the 16-layer contract without changing the master source.
It never invents new artwork: generated layers remain derived build output.
"""

from __future__ import annotations

import argparse
import copy
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)

LAYERS = (
    "back_hair", "legs", "shoes", "torso", "left_arm", "right_arm",
    "neck", "head", "ears", "front_hair", "left_eye", "right_eye",
    "left_brow", "right_brow", "nose", "mouth",
)

# Direct-child indices in the first drawing group of each current master.
# Empty lists create transparent placeholders for parts not yet drawn.
MAP = {
    "tunde": {
        "back_hair": [], "legs": [0], "shoes": [1, 2], "torso": [3, 4],
        "left_arm": [5], "right_arm": [6], "neck": [7], "head": [10],
        "ears": [8, 9], "front_hair": [11], "left_eye": [12, 14],
        "right_eye": [13, 15], "left_brow": [16], "right_brow": [17],
        "nose": [18], "mouth": [19],
    },
    "seyi": {
        "back_hair": [], "legs": [0], "shoes": [1, 2], "torso": [3],
        "left_arm": [], "right_arm": [], "neck": [4], "head": [7],
        "ears": [5, 6], "front_hair": [8], "left_eye": [9, 11],
        "right_eye": [10, 12], "left_brow": [13], "right_brow": [14],
        "nose": [15], "mouth": [16],
    },
    "mama": {
        "back_hair": [], "legs": [0], "shoes": [1, 2], "torso": [3],
        "left_arm": [18], "right_arm": [19], "neck": [4], "head": [7],
        "ears": [5, 6], "front_hair": [8, 9], "left_eye": [10, 12],
        "right_eye": [11, 13], "left_brow": [14], "right_brow": [15],
        "nose": [16], "mouth": [17],
    },
}


def _children(master: Path) -> tuple[ET.Element, list[ET.Element]]:
    root = ET.parse(master).getroot()
    groups = [node for node in root if node.tag.rsplit("}", 1)[-1] == "g"]
    if not groups:
        raise ValueError(f"No drawing group found in {master}")
    return root, list(groups[0])


def _write_layer(master_root: ET.Element, nodes: list[ET.Element], target: Path) -> None:
    root = ET.Element(f"{{{NS}}}svg", {"viewBox": master_root.attrib.get("viewBox", "0 0 600 1100")})
    group = ET.SubElement(root, f"{{{NS}}}g")
    for node in nodes:
        group.append(copy.deepcopy(node))
    target.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(target, encoding="utf-8", xml_declaration=True)


def build(character_id: str, png: bool = False) -> None:
    master = ROOT / "assets" / "characters" / character_id / "art" / f"{character_id}_front.svg"
    if not master.exists():
        raise FileNotFoundError(master)
    root, children = _children(master)
    for layer in LAYERS:
        nodes = [children[i] for i in MAP[character_id][layer] if i < len(children)]
        target = ROOT / "assets" / "characters" / character_id / "layers" / "front" / f"{layer}.svg"
        _write_layer(root, nodes, target)
        if png:
            try:
                import cairosvg
            except ImportError as exc:
                raise RuntimeError("PNG build requires CairoSVG: pip install cairosvg") from exc
            cairosvg.svg2png(url=str(target), write_to=str(target.with_suffix(".png")), output_width=600, output_height=1100)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--character", choices=["tunde", "seyi", "mama", "all"], default="all")
    parser.add_argument("--png", action="store_true")
    args = parser.parse_args()
    ids = ("tunde", "seyi", "mama") if args.character == "all" else (args.character,)
    for character_id in ids:
        build(character_id, png=args.png)
        print(f"built {character_id}: {len(LAYERS)} front layers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
