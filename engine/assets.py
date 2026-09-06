"""Character asset contracts for AFRITOON."""

from dataclasses import dataclass, field
from pathlib import Path


LAYER_NAMES = (
    "back_hair", "legs", "shoes", "torso", "left_arm", "right_arm",
    "neck", "head", "ears", "front_hair", "left_eye", "right_eye",
    "left_brow", "right_brow", "nose", "mouth",
)


@dataclass(frozen=True)
class LayerAsset:
    name: str
    path: Path
    anchor_x: float = 0.0
    anchor_y: float = 0.0


@dataclass
class CharacterAssetSet:
    """Named artwork layers for one reusable character."""

    root: Path
    layers: dict[str, LayerAsset] = field(default_factory=dict)

    def layer(self, name: str) -> LayerAsset:
        if name not in LAYER_NAMES:
            raise ValueError(f"Unsupported character layer: {name}")
        try:
            return self.layers[name]
        except KeyError as exc:
            raise FileNotFoundError(f"Missing character layer: {name}") from exc

    @classmethod
    def discover(cls, root: str | Path) -> "CharacterAssetSet":
        base = Path(root)
        layers = {}
        for name in LAYER_NAMES:
            png = base / f"{name}.png"
            svg = base / f"{name}.svg"
            path = png if png.exists() else svg
            if path.exists():
                layers[name] = LayerAsset(name=name, path=path)
        return cls(base, layers)

    @property
    def complete(self) -> bool:
        return all(name in self.layers for name in LAYER_NAMES)

    def missing(self) -> tuple[str, ...]:
        return tuple(name for name in LAYER_NAMES if name not in self.layers)
