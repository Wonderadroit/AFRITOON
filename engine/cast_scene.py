"""Data-first multi-character scene state for AFRITOON."""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Tuple

import yaml

from .character_library import DEFAULT_LIBRARY, CharacterInstance
from .dialogue import DialogueLine
from .interactions import CharacterCue, interaction


@dataclass(frozen=True)
class CastState:
    time: float
    characters: Dict[str, CharacterInstance]


class CastScene:
    def __init__(self, name: str, duration: float, characters: Iterable[CharacterInstance], dialogue: Iterable[DialogueLine] = ()):
        self.name = str(name)
        self.duration = float(duration)
        self.characters = {item.definition.id: item for item in characters}
        self.dialogue = tuple(sorted(dialogue, key=lambda item: item.at))
        if self.duration <= 0:
            raise ValueError("CastScene duration must be positive")
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
        """Load cast composition, positions, interaction and dialogue from YAML."""
        source = Path(path)
        data = yaml.safe_load(source.read_text(encoding="utf-8")) or {}
        raw = data.get("scene", data)
        interaction_name = str(raw.get("interaction", ""))
        duration = float(raw.get("duration", 0.0))
        items = raw.get("characters", [])
        dialogue_items = raw.get("dialogue", [])
        dialogue = tuple(
            DialogueLine(
                character=str(item["character"]), text=str(item["text"]), at=float(item["at"]),
                duration=float(item["duration"]) if item.get("duration") is not None else None,
                voice=str(item["voice"]) if item.get("voice") is not None else None,
            )
            for item in dialogue_items
        )
        if not items:
            scene = cls.from_interaction(interaction_name, duration or None)
            scene.dialogue = dialogue
            return scene
        instances = []
        for item in items:
            cid = str(item["id"])
            position = item.get("position", [540, 1150])
            if len(position) != 2:
                raise ValueError(f"Invalid position for {cid}")
            instances.append(DEFAULT_LIBRARY.spawn(
                cid, x=float(position[0]), y=float(position[1]), scale=float(item.get("scale", 1.0))
            ))
        return cls(interaction_name or source.stem, duration, instances, dialogue)

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
                states[character_id] = states[character_id].with_state(pose=cue.pose, expression=cue.expression)
        return CastState(now, states)

    def cues(self) -> Tuple[CharacterCue, ...]:
        try:
            return interaction(self.name).cues
        except ValueError:
            return ()

    def dialogue_at(self, t: float) -> DialogueLine | None:
        """Return the dialogue line active at time t."""
        current: DialogueLine | None = None
        for line in self.dialogue:
            if line.at > float(t):
                break
            if line.duration is None or float(t) < line.at + line.duration:
                current = line
        return current
