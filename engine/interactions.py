"""Small, data-first interaction primitives for AFRITOON's recurring cast."""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class CharacterCue:
    time: float
    character: str
    pose: str = "idle"
    expression: str = "neutral"
    visible: bool | None = None


@dataclass(frozen=True)
class Interaction:
    name: str
    cues: Tuple[CharacterCue, ...]


INTERACTIONS = {
    "tunde_seyi_deadpan": Interaction(
        name="tunde_seyi_deadpan",
        cues=(
            CharacterCue(0.0, "tunde", "talk", "happy"),
            CharacterCue(1.5, "seyi", "idle", "deadpan"),
            CharacterCue(2.4, "tunde", "look_at_camera", "surprised"),
            CharacterCue(3.0, "seyi", "look_at_camera", "deadpan"),
        ),
    ),
    "tunde_mama_exposed": Interaction(
        name="tunde_mama_exposed",
        cues=(
            CharacterCue(0.0, "tunde", "talk", "happy"),
            CharacterCue(2.0, "mama", "stand", "neutral"),
            CharacterCue(2.6, "tunde", "freeze", "shocked"),
            CharacterCue(3.4, "mama", "look_at_camera", "deadpan"),
        ),
    ),
    "trio_problem": Interaction(
        name="trio_problem",
        cues=(
            CharacterCue(0.0, "tunde", "talk", "happy"),
            CharacterCue(1.5, "seyi", "look_at_camera", "deadpan"),
            CharacterCue(2.5, "mama", "stand", "neutral"),
            CharacterCue(3.0, "tunde", "freeze", "shocked"),
            CharacterCue(3.8, "seyi", "look_at_camera", "deadpan"),
            CharacterCue(4.5, "mama", "look_at_camera", "deadpan"),
        ),
    ),
    "nepa_panic": Interaction(
        name="nepa_panic",
        cues=(
            CharacterCue(0.0, "tunde", "talk", "happy"),
            CharacterCue(0.0, "seyi", "idle", "deadpan", False),
            CharacterCue(0.0, "mama", "idle", "neutral", False),
            CharacterCue(3.6, "tunde", "idle", "happy"),
            CharacterCue(7.0, "tunde", "shock", "shocked"),
            CharacterCue(9.4, "tunde", "check_pocket", "surprised"),
            CharacterCue(12.8, "seyi", "look", "deadpan", True),
            CharacterCue(14.5, "tunde", "talk", "shocked"),
            CharacterCue(18.0, "mama", "stand", "neutral", True),
            CharacterCue(19.8, "tunde", "freeze", "shocked"),
            CharacterCue(21.0, "mama", "angry", "angry"),
            CharacterCue(22.8, "seyi", "look_at_camera", "deadpan"),
        ),
    ),
}


def interaction(name: str) -> Interaction:
    try:
        return INTERACTIONS[name]
    except KeyError as exc:
        raise ValueError(f"Unknown AFRITOON interaction: {name}") from exc
