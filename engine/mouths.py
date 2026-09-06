"""Small reusable mouth-state vocabulary for AFRITOON dialogue animation."""

from dataclasses import dataclass

SUPPORTED_MOUTHS = {
    "closed", "smile", "small_open", "open", "wide_smile", "sad", "flat", "tight",
    "talk_a", "talk_e", "talk_o", "talk_m", "talk_rest",
}

@dataclass(frozen=True)
class MouthState:
    name: str
    openness: float
    shape: str

MOUTHS = {
    "closed": MouthState("closed", 0.0, "closed"),
    "smile": MouthState("smile", 0.15, "smile"),
    "small_open": MouthState("small_open", 0.35, "round"),
    "open": MouthState("open", 0.65, "round"),
    "wide_smile": MouthState("wide_smile", 0.25, "smile"),
    "sad": MouthState("sad", 0.15, "frown"),
    "flat": MouthState("flat", 0.0, "flat"),
    "tight": MouthState("tight", 0.05, "tight"),
    "talk_a": MouthState("talk_a", 0.55, "a"),
    "talk_e": MouthState("talk_e", 0.35, "e"),
    "talk_o": MouthState("talk_o", 0.65, "o"),
    "talk_m": MouthState("talk_m", 0.0, "m"),
    "talk_rest": MouthState("talk_rest", 0.2, "rest"),
}

def mouth(name: str) -> MouthState:
    key = str(name).strip().lower()
    if key not in SUPPORTED_MOUTHS:
        raise ValueError(f"Unsupported mouth state: {name}")
    return MOUTHS[key]
