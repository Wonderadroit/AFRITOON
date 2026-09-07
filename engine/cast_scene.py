"""Data-first multi-character scene state for ITANRA."""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Tuple

import yaml

from .character_library import DEFAULT_LIBRARY, CharacterInstance
from .dialogue import DialogueLine
from .interactions import CharacterCue, interaction
from .story_director import StoryPlan, story_plan_from_yaml
from .story_performance import cue_at, cues_for
from .spatial_blocking import SpatialCue, resolve_positions
from .story_blocking import cues_for as story_blocking_cues_for


@dataclass(frozen=True)
class CastState:
    time: float
    characters: Dict[str, CharacterInstance]


class CastScene:
    def __init__(
        self,
        name: str,
        duration: float,
        characters: Iterable[CharacterInstance],
        dialogue: Iterable[DialogueLine] = (),
        story_plan: StoryPlan | None = None,
        spatial_cues: Iterable[SpatialCue] = (),
    ):
        self.name = str(name)
        self.duration = float(duration)
        self.characters = {item.definition.id: item for item in characters}
        self.dialogue = tuple(sorted(dialogue, key=lambda item: item.at))
        self.story_plan = story_plan
        self.spatial_cues = tuple(sorted(spatial_cues, key=lambda item: item.at))
        if self.duration <= 0:
            raise ValueError("CastScene duration must be positive")
        if not self.characters:
            raise ValueError("CastScene requires at least one character")
        if story_plan is not None and story_plan.duration != self.duration:
            raise ValueError("StoryPlan duration must match CastScene duration")
        unknown = {cue.character for cue in self.spatial_cues} - set(self.characters)
        if unknown:
            raise ValueError(f"Spatial cue references unknown character(s): {sorted(unknown)}")

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
        """Load cast composition, story plan, spatial blocking and dialogue from YAML."""
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
        spatial_cues = []
        for item in raw.get("blocking", []):
            destination = item.get("to")
            if not isinstance(destination, (list, tuple)) or len(destination) != 2:
                raise ValueError(f"Invalid blocking destination for {item.get('character')}")
            spatial_cues.append(SpatialCue(
                at=float(item["at"]),
                character=str(item["character"]),
                to=(float(destination[0]), float(destination[1])),
                duration=float(item.get("duration", 0.0)),
            ))

        story_plan = None
        if raw.get("story") is not None:
            story_raw = dict(raw["story"])
            story_raw.setdefault("duration", duration)
            story_plan = story_plan_from_yaml({"story": story_raw})

        if not items:
            scene = cls.from_interaction(interaction_name, duration or None)
            scene.dialogue = dialogue
            scene.story_plan = story_plan
            scene.spatial_cues = tuple(spatial_cues)
            return scene

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
                visible=bool(item.get("visible", True)),
            ))
        return cls(interaction_name or source.stem, duration, instances, dialogue, story_plan, spatial_cues)

    def state_at(self, t: float) -> CastState:
        now = max(0.0, min(float(t), self.duration))
        states = dict(self.characters)
        if self.story_plan is not None:
            for character_id in self.characters:
                cue = cue_at(cues_for(self.story_plan, character_id), now)
                if cue is not None:
                    states[character_id] = states[character_id].with_state(
                        pose=cue.action,
                        expression=cue.expression,
                    )
        try:
            cues = interaction(self.name).cues
        except ValueError:
            cues = ()
        for character_id in self.characters:
            applicable = [c for c in cues if c.character == character_id and c.time <= now]
            if applicable:
                cue = max(applicable, key=lambda item: item.time)
                states[character_id] = states[character_id].with_state(
                    pose=cue.pose,
                    expression=cue.expression,
                    visible=cue.visible,
                )

        base_positions = {cid: (item.x, item.y, item.scale) for cid, item in states.items()}
        blocking = list(self.spatial_cues)
        if self.story_plan is not None:
            story_positions = {cid: (item.x, item.y) for cid, item in states.items()}
            # Derived story blocking is deliberately lower priority than explicit
            # blocking: explicit scene staging is the author's final say.
            derived = story_blocking_cues_for(self.story_plan, story_positions)
            blocking = list(derived) + blocking
        moved = resolve_positions(now, base_positions, tuple(blocking))
        for cid, item in states.items():
            x, y, _ = moved[cid]
            states[cid] = CharacterInstance(
                definition=item.definition, x=x, y=y, scale=item.scale,
                view=item.view, pose=item.pose, expression=item.expression,
                visible=item.visible,
            )
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
