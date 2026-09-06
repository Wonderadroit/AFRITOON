"""Canonical character-art asset resolution for AFRITOON."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .assets import LAYER_NAMES, CharacterAssetSet
from .character_spec import character


@dataclass(frozen=True)
class CharacterArt:
    character_id: str
    root: Path
    view: str
    master: Path
    layers: CharacterAssetSet

    @property
    def has_master(self) -> bool:
        return self.master.exists()

    @property
    def has_rig(self) -> bool:
        return self.layers.complete

    @property
    def missing_layers(self) -> tuple[str, ...]:
        return self.layers.missing()


class CharacterAssetResolver:
    """Resolve artwork without embedding asset paths in scene logic."""

    def __init__(self, repo_root: str | Path = "."):
        self.repo_root = Path(repo_root)

    def resolve(self, character_id: str, view: str = "front") -> CharacterArt:
        definition = character(character_id)
        if view not in definition.views:
            raise ValueError(f"Unsupported view for {character_id}: {view}")
        root = self.repo_root / "assets" / "characters" / character_id
        master = root / "art" / f"{character_id}_{view}.svg"
        layers = CharacterAssetSet.discover(root / "layers" / view)
        return CharacterArt(character_id, root, view, master, layers)

    def summary(self) -> dict[str, dict[str, object]]:
        result = {}
        for definition in (character("tunde"), character("seyi"), character("mama")):
            views = {}
            for view in definition.views:
                art = self.resolve(definition.id, view)
                views[view] = {
                    "master": art.has_master,
                    "rig": art.has_rig,
                    "missing_layers": list(art.missing_layers),
                }
            result[definition.id] = views
        return result


def character_layer_contract() -> tuple[str, ...]:
    """Expose the immutable 16-layer production contract."""
    return LAYER_NAMES
