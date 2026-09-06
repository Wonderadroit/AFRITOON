"""Layered 2D character compositor for AFRITOON."""

from dataclasses import dataclass
from pathlib import Path

from PIL import Image

from .svg_renderer import SVGRenderUnavailable, rasterize_svg


@dataclass(frozen=True)
class Transform:
    x: float = 0.0
    y: float = 0.0
    rotation: float = 0.0
    scale: float = 1.0


class LayeredRig:
    """Compose named RGBA artwork layers in deterministic draw order.

    PNG is preferred for production. SVG layers are also accepted so compact
    vector artwork can remain the source while generated binaries stay out of
    version control.
    """

    def __init__(self, root: str | Path, order: tuple[str, ...]):
        self.root = Path(root)
        self.order = order
        self.transforms: dict[str, Transform] = {}

    def set_transform(self, layer: str, transform: Transform) -> None:
        self.transforms[layer] = transform

    def available(self, layer: str) -> bool:
        return (self.root / f"{layer}.png").exists() or (self.root / f"{layer}.svg").exists()

    def _load(self, name: str) -> Image.Image | None:
        png = self.root / f"{name}.png"
        if png.exists():
            return Image.open(png).convert("RGBA")
        svg = self.root / f"{name}.svg"
        if svg.exists():
            try:
                return rasterize_svg(svg, 600, 1100)
            except SVGRenderUnavailable:
                return None
        return None

    @staticmethod
    def _crop(layer: Image.Image) -> Image.Image:
        bbox = layer.getbbox()
        return layer.crop(bbox) if bbox else layer

    def render(self, canvas: Image.Image) -> Image.Image:
        if canvas.mode != "RGBA":
            canvas = canvas.convert("RGBA")
        for name in self.order:
            layer = self._load(name)
            if layer is None:
                continue
            layer = self._crop(layer)
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
