"""Data-first multi-character scene state for AFRITOON."""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Tuple

import yaml

from .character_library import DEFAULT_LIBRARY, CharacterInstance
from .interactions import CharacterCue, interaction


@dataclass(frozen=True)
class CastState:
    time: float
    characters: Dict[str, CharacterInstance]


class CastScene:
    def __init__(self, name: str, duration: float, characters: Iterable[CharacterInstance]):
        self.name = str(name)
        self.duration = float(duration)
        self.characters = {item.definition.id: item for item in characters}
        if not self.characters:
            raise ValueError("CastScene requires at least one character")

    @classmethod
    def from_interaction(cls, name: str, duration: float | None = None):
        spec = interaction(name)
        ids = []
        for cue in spec.cues:
            if cue.character not in ids:
                ids.append(cue.character)
        instances = [DEFAULT_LIBRARY.spawn(cid) for cid in ids]
        end = max((cue.time for cue in spec.cues), default=0.0)
        return cls(name, float(duration if duration is not None else end + 1.0), instances)

    @classmethod
    def from_yaml(cls, path: str | Path):
        """Load cast composition, positions and interaction from scene YAML."""
        source = Path(path)
        data = yaml.safe_load(source.read_text(encoding="utf-8")) or {}
        raw = data.get("scene", data)
        interaction_name = str(raw.get("interaction", ""))
        duration = float(raw.get("duration", 0.0))
        items = raw.get("characters", [])
        if not items:
            return cls.from_interaction(interaction_name, duration or None)

        instances = []
        for item in items:
            cid = str(item["id"])
            position = item.get("position", [540, 1150])
            if len(position) != 2:
                raise ValueError(f"Invalid position for {cid}")
            instances.append(DEFAULT_LIBRARY.spawn(
                cid,
                x=float(position[0]),
                y=float(position[1]),
                scale=float(item.get("scale", 1.0)),
            ))
        return cls(interaction_name or source.stem, duration, instances)

    def state_at(self, t: float) -> CastState:
        now = max(0.0, min(float(t), self.duration))
        states = dict(self.characters)
        try:
            cues = interaction(self.name).cues
        except ValueError:
            cues = ()
        for character_id in self.characters:
            applicable = [c for c in cues if c.character == character_id and c.time <= now]
            if applicable:
                cue = max(applicable, key=lambda item: item.time)
                states[character_id] = states[character_id].with_state(
                    pose=cue.pose, expression=cue.expression
                )
        return CastState(now, states)

    def cues(self) -> Tuple[CharacterCue, ...]:
        try:
            return interaction(self.name).cues
        except ValueError:
            return ()
