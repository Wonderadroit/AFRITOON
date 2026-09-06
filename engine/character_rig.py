"""Factory for reusable AFRITOON character rigs."""

from __future__ import annotations

from pathlib import Path

from .assets import LAYER_NAMES
from .character_assets import CharacterAssetResolver
from .character_library import CharacterInstance
from .character_pose import pose_for
from .layered_rig import LayeredRig


class CharacterRig:
    """Bind a character instance to its artwork layers and semantic pose."""

    def __init__(self, instance: CharacterInstance, repo_root: str | Path = "."):
        self.instance = instance
        self.repo_root = Path(repo_root)
        self.art = CharacterAssetResolver(repo_root).resolve(instance.id, instance.view)
        self.rig = LayeredRig(self.art.layers.root, LAYER_NAMES)
        self.apply_pose()

    @property
    def ready(self) -> bool:
        return self.art.has_rig

    def apply_pose(self) -> None:
        pose = pose_for(
            self.instance.id,
            self.instance.pose,
            origin_x=self.instance.x,
            origin_y=self.instance.y,
            scale=self.instance.scale,
        )
        for layer, transform in pose.layers.items():
            self.rig.set_transform(layer, transform)

    def render(self, canvas):
        return self.rig.render(canvas)
