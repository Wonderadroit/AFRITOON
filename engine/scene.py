"""AFRITOON scene primitives."""
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Action:
    time: float
    name: str
    duration: float = 0.0
    params: dict[str, Any] = field(default_factory=dict)


@dataclass
class CharacterState:
    x: float = 0.5
    y: float = 0.68
    expression: str = "neutral"
    action: str = "idle"
    facing: int = 1


@dataclass
class Scene:
    width: int = 1080
    height: int = 1920
    fps: int = 30
    duration: float = 8.0
    background: str = "campus"
    characters: dict[str, CharacterState] = field(default_factory=dict)
    actions: dict[str, list[Action]] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Scene":
        cfg = data.get("scene", data)
        scene = cls(
            width=int(cfg.get("width", 1080)),
            height=int(cfg.get("height", 1920)),
            fps=int(cfg.get("fps", 30)),
            duration=float(cfg.get("duration", 8)),
            background=cfg.get("background", "campus"),
        )
        chars = cfg.get("characters", {})
        for name, value in chars.items():
            scene.characters[name] = CharacterState(
                x=float(value.get("x", 0.5)),
                y=float(value.get("y", 0.68)),
                expression=value.get("expression", "neutral"),
                facing=int(value.get("facing", 1)),
            )
        for item in data.get("actions", []):
            name = item["character"]
            scene.actions.setdefault(name, []).append(Action(
                time=float(item.get("at", item.get("time", 0))),
                name=item["action"],
                duration=float(item.get("duration", 0)),
                params=item.get("params", {}),
            ))
        for actions in scene.actions.values():
            actions.sort(key=lambda a: a.time)
        return scene
