"""Layered 2D character compositor for AFRITOON.

Production artwork is split into transparent layers. Each layer can be
positioned, scaled and rotated around an anchor without changing scene YAML.
"""

from dataclasses import dataclass
from pathlib import Path
from PIL import Image


@dataclass(frozen=True)
class Transform:
    x: float = 0.0
    y: float = 0.0
    rotation: float = 0.0
    scale: float = 1.0


class LayeredRig:
    """Compose named RGBA artwork layers in a deterministic draw order."""

    def __init__(self, root: str | Path, order: tuple[str, ...]):
        self.root = Path(root)
        self.order = order
        self.transforms: dict[str, Transform] = {}

    def set_transform(self, layer: str, transform: Transform) -> None:
        self.transforms[layer] = transform

    def available(self, layer: str) -> bool:
        return (self.root / f"{layer}.png").exists()

    def render(self, canvas: Image.Image) -> Image.Image:
        """Render available layers; missing artwork is intentionally skipped."""
        if canvas.mode != "RGBA":
            canvas = canvas.convert("RGBA")
        for name in self.order:
            path = self.root / f"{name}.png"
            if not path.exists():
                continue
            layer = Image.open(path).convert("RGBA")
            transform = self.transforms.get(name, Transform())
            if transform.scale != 1.0:
                w = max(1, round(layer.width * transform.scale))
                h = max(1, round(layer.height * transform.scale))
                layer = layer.resize((w, h), Image.Resampling.LANCZOS)
            if transform.rotation:
                layer = layer.rotate(transform.rotation, resample=Image.Resampling.BICUBIC, expand=True)
            px = round(transform.x - layer.width / 2)
            py = round(transform.y - layer.height / 2)
            canvas.alpha_composite(layer, (px, py))
        return canvas
