"""Validate the ITANRA recurring-character production contract."""

from __future__ import annotations

from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CORE = ("tunde", "seyi", "mama")
VIEWS = ("front", "three_quarter", "side")
LAYERS = (
    "back_hair", "legs", "shoes", "torso", "left_arm", "right_arm",
    "neck", "head", "ears", "front_hair", "left_eye", "right_eye",
    "left_brow", "right_brow", "nose", "mouth",
)


def _semantic_layers(path: Path) -> tuple[str, ...]:
    root = ET.fromstring(path.read_text(encoding="utf-8"))
    return tuple(
        node.attrib["data-layer"]
        for node in root.iter()
        if node.tag.rsplit("}", 1)[-1] == "g" and "data-layer" in node.attrib
    )


def main() -> int:
    errors: list[str] = []
    for cid in CORE:
        front = ROOT / "assets" / "characters" / cid / "art" / f"{cid}_front.svg"
        if not front.exists():
            errors.append(f"{cid}: missing front master")
            continue

        try:
            layers = _semantic_layers(front)
        except (ET.ParseError, OSError) as exc:
            errors.append(f"{cid}: invalid front SVG: {exc}")
            continue

        missing = [layer for layer in LAYERS if layer not in layers]
        duplicates = sorted({layer for layer in layers if layers.count(layer) > 1})
        unknown = sorted(set(layers) - set(LAYERS))
        if missing:
            errors.append(f"{cid}: missing semantic layers: {', '.join(missing)}")
        if duplicates:
            errors.append(f"{cid}: duplicate semantic layers: {', '.join(duplicates)}")
        if unknown:
            errors.append(f"{cid}: unknown semantic layers: {', '.join(unknown)}")

        layer_root = ROOT / "assets" / "characters" / cid / "layers" / "front"
        built = sum((layer_root / f"{layer}.svg").exists() for layer in LAYERS)
        print(f"{cid}: master=yes semantic_layers={len(layers)}/16 built_layers={built}/16")

        for view in VIEWS:
            if view == "front":
                continue
            path = ROOT / "assets" / "characters" / cid / "art" / f"{cid}_{view}.svg"
            if path.exists():
                try:
                    view_layers = _semantic_layers(path)
                except (ET.ParseError, OSError) as exc:
                    errors.append(f"{cid}/{view}: invalid SVG: {exc}")
                    continue
                if any(layer not in view_layers for layer in LAYERS):
                    errors.append(f"{cid}/{view}: incomplete semantic layer contract")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("character contract: valid")
    print("note: three_quarter/side remain authored artwork inputs; runtime fallback to front is explicit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
