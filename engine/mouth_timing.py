"""Deterministic dialogue-to-mouth timing for AFRITOON prototypes.

This is intentionally provider-independent: it can consume real TTS timing later,
while still giving the renderer a useful approximation when only text is known.
"""

from __future__ import annotations

from dataclasses import dataclass
import re

from .mouths import MouthState, mouth


@dataclass(frozen=True)
class MouthCue:
    at: float
    duration: float
    state: MouthState


def estimate_duration(text: str, characters_per_second: float = 12.0) -> float:
    """Estimate spoken duration from text when no audio timing exists."""
    if characters_per_second <= 0:
        raise ValueError("characters_per_second must be positive")
    words = len(re.findall(r"\S+", text))
    punctuation = len(re.findall(r"[,;:!?]", text))
    return max(0.25, words / 2.6 + punctuation * 0.12)


def mouth_cues(text: str, start: float = 0.0, duration: float | None = None) -> tuple[MouthCue, ...]:
    """Create a lightweight phonetic rhythm from text.

    It is not a phoneme recognizer. Real TTS/audio alignment can replace this
    later without changing the scene contract.
    """
    if start < 0:
        raise ValueError("start cannot be negative")
    total = estimate_duration(text) if duration is None else float(duration)
    if total <= 0:
        raise ValueError("duration must be positive")

    letters = [c.lower() for c in text if c.isalpha()]
    if not letters:
        return (MouthCue(start, total, mouth("talk_rest")),)

    step = total / len(letters)
    states: list[MouthCue] = []
    for index, char in enumerate(letters):
        if char in "aáàeéèiíì":
            name = "talk_a" if char in "aáà" else "talk_e"
        elif char in "oóòuúù":
            name = "talk_o"
        elif char in "mbp":
            name = "talk_m"
        else:
            name = "talk_rest"
        states.append(MouthCue(start + index * step, step, mouth(name)))
    return tuple(states)
