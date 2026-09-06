"""Scene loading and timeline evaluation."""

from dataclasses import dataclass
import yaml
from .actions import Action


@dataclass
class Scene:
    title: str
    duration: float
    character: dict
    timeline: list[Action]

    @classmethod
    def load(cls, path: str) -> "Scene":
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        raw = data.get("scene", data)
        timeline = [Action(float(x["time"]), str(x["action"]), float(x.get("duration", 0))) for x in raw.get("timeline", [])]
        return cls(str(data.get("title", path)), float(raw.get("duration", 5)), raw.get("character", {}), timeline)
