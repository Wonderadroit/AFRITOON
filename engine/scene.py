"""Scene loading and timeline evaluation."""

from dataclasses import dataclass
from pathlib import Path
import yaml
from .actions import Action


@dataclass
class Scene:
    title: str
    duration: float
    character: dict
    timeline: list[Action]

    @classmethod
    def load(cls, path: str | Path) -> "Scene":
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        raw = data.get("scene", data)
        timeline = [Action(float(item["time"]), str(item["action"]), float(item.get("duration", 0))) for item in raw.get("timeline", [])]
        timeline.sort(key=lambda item: item.time)
        return cls(str(data.get("title", Path(path).stem)), float(raw.get("duration", 5)), dict(raw.get("character", {})), timeline)
