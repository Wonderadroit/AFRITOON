"""Validate the ITANRA recurring-character production contract."""

from __future__ import annotations

from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CORE = ("tunde", "seyi", "mama")
VIEWS = ("front", "three_quarter", "side")
LAYERS = (
    "back_hair", "legs", "shoes", "torso", "left_arm", "right_arm",
    "neck", "head", "ears", "front_hair", "left_eye", "right_eye",
    "left_brow", "right_brow", "nose", "mouth",
)
MOUTH_VARIANTS = {
    "closed", "smile", "small_open", "open", "flat", "tight", "sad",
    "wide_smile", "talk_a", "talk_e", "talk_o", "talk_m", "talk_rest",
}


def _semantic_layers(path: Path) -> tuple[str, ...]:
    root = ET.fromstring(path.read_text(encoding="utf-8"))
    return tuple(
        node.attrib["data-layer"]
        for node in root.iter()
        if node.tag.rsplit("}", 1)[-1] == "g" and "data-layer" in node.attrib
    )


def _mouth_variants(path: Path) -> set[str]:
    root = ET.fromstring(path.read_text(encoding="utf-8"))
    mouth_layers = [
        node for node in root.iter()
        if node.tag.rsplit("}", 1)[-1] == "g" and node.attrib.get("data-layer") == "mouth"
    ]
    return {
        node.attrib["data-mouth"]
        for layer in mouth_layers
        for node in layer.iter()
        if "data-mouth" in node.attrib
    }


def _has_pupil(path: Path, layer_name: str) -> bool:
    root = ET.fromstring(path.read_text(encoding="utf-8"))
    for layer in root.iter():
        if layer.tag.rsplit("}", 1)[-1] != "g" or layer.attrib.get("data-layer") != layer_name:
            continue
        for node in layer.iter():
            if node.tag.rsplit("}", 1)[-1] == "ellipse" and node.attrib.get("fill", "").lower() == "#171717":
                return True
    return False


def main() -> int:
    errors: list[str] = []
    for cid in CORE:
        front = ROOT / "assets" / "characters" / cid / "art" / f"{cid}_front.svg"
        if not front.exists():
            errors.append(f"{cid}: missing front master")
            continue

        try:
            layers = _semantic_layers(front)
            mouth_variants = _mouth_variants(front)
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

        missing_mouths = sorted(MOUTH_VARIANTS - mouth_variants)
        if missing_mouths:
            errors.append(f"{cid}: missing mouth variants: {', '.join(missing_mouths)}")
        for eye in ("left_eye", "right_eye"):
            if not _has_pupil(front, eye):
                errors.append(f"{cid}: {eye} has no authored pupil ellipse")

        layer_root = ROOT / "assets" / "characters" / cid / "layers" / "front"
        built = sum((layer_root / f"{layer}.svg").exists() for layer in LAYERS)
        print(
            f"{cid}: master=yes semantic_layers={len(layers)}/16 "
            f"built_layers={built}/16 mouth_variants={len(mouth_variants)}/13 pupils=yes"
        )

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
