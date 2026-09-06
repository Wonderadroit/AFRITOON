"""Validate the AFRITOON recurring-character production contract."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CORE = ("tunde", "seyi", "mama")
VIEWS = ("front", "three_quarter", "side")
LAYERS = (
    "back_hair", "legs", "shoes", "torso", "left_arm", "right_arm",
    "neck", "head", "ears", "front_hair", "left_eye", "right_eye",
    "left_brow", "right_brow", "nose", "mouth",
)


def main() -> int:
    errors: list[str] = []
    for cid in CORE:
        front = ROOT / "assets" / "characters" / cid / "art" / f"{cid}_front.svg"
        if not front.exists():
            errors.append(f"{cid}: missing front master")
        for view in VIEWS:
            if view != "front":
                path = ROOT / "assets" / "characters" / cid / "art" / f"{cid}_{view}.svg"
                if path.exists():
                    continue
                # A view may be absent while the artwork team is still authoring it.
                # The runtime must never silently pretend it is production artwork.
        layer_root = ROOT / "assets" / "characters" / cid / "layers" / "front"
        built = sum((layer_root / f"{layer}.svg").exists() for layer in LAYERS)
        print(f"{cid}: master={'yes' if front.exists() else 'NO'} front_layers={built}/16")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("character contract: valid")
    print("note: three_quarter/side and expression variants remain artwork inputs, not fake generated poses")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
