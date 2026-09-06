"""Build deterministic semantic SVG layers from AFRITOON character masters."""

from __future__ import annotations

import argparse
import copy
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)

LAYERS = (
    "back_hair", "legs", "shoes", "torso", "left_arm", "right_arm",
    "neck", "head", "ears", "front_hair", "left_eye", "right_eye",
    "left_brow", "right_brow", "nose", "mouth",
)

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
        "ears": [5, 6], "front_hair": [8], "left_eye": [9], "right_eye": [10],
        "left_brow": [11], "right_brow": [11], "nose": [12], "mouth": [13],
    },
    "mama": {
        "back_hair": [], "legs": [0], "shoes": [1, 2], "torso": [3],
        "left_arm": [18], "right_arm": [19], "neck": [4], "head": [7],
        "ears": [5, 6], "front_hair": [8, 9], "left_eye": [10], "right_eye": [11],
        "left_brow": [12], "right_brow": [12], "nose": [13], "mouth": [14],
    },
}


def children(master: Path):
    root = ET.parse(master).getroot()
    groups = [n for n in root if n.tag.rsplit("}", 1)[-1] == "g"]
    if not groups:
        raise ValueError(f"No drawing group found: {master}")
    return root, list(groups[0])


def write_layer(root, nodes, target: Path):
    out = ET.Element(
        f"{{{NS}}}svg",
        {"viewBox": root.attrib.get("viewBox", "0 0 600 1100")},
    )
    group = ET.SubElement(out, f"{{{NS}}}g")
    for node in nodes:
        group.append(copy.deepcopy(node))
    target.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(out).write(target, encoding="utf-8", xml_declaration=True)


def build(cid: str) -> None:
    master = ROOT / "assets" / "characters" / cid / "art" / f"{cid}_front.svg"
    root, nodes = children(master)
    mapping = MAP[cid]

    referenced = sorted({index for indexes in mapping.values() for index in indexes})
    invalid = [index for index in referenced if index < 0 or index >= len(nodes)]
    if invalid:
        raise ValueError(
            f"{cid} layer map references element indexes outside source: {invalid}; "
            f"source contains {len(nodes)} drawing elements"
        )

    missing_layers = [layer for layer in LAYERS if layer not in mapping]
    if missing_layers:
        raise ValueError(f"{cid} missing layer mappings: {missing_layers}")

    output_root = ROOT / "assets" / "characters" / cid / "layers" / "front"
    for layer in LAYERS:
        selected = [nodes[index] for index in mapping[layer]]
        write_layer(root, selected, output_root / f"{layer}.svg")

    produced = [output_root / f"{layer}.svg" for layer in LAYERS]
    if not all(path.exists() for path in produced):
        raise RuntimeError(f"Layer build incomplete for {cid}")
    print(f"built {cid}: {len(produced)}/16 semantic layer files")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build AFRITOON front-view character layers")
    parser.add_argument("--character", choices=("tunde", "seyi", "mama", "all"), default="all")
    args = parser.parse_args()
    characters = ("tunde", "seyi", "mama") if args.character == "all" else (args.character,)
    for cid in characters:
        build(cid)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
