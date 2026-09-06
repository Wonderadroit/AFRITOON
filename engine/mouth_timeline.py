"""Deterministic dialogue-to-mouth planning for AFRITOON.

This is a lightweight planning layer, not a phoneme recognizer. It provides a
stable fallback until real audio/phoneme analysis is connected to a TTS backend.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from .mouths import mouth


@dataclass(frozen=True)
class MouthCue:
    at: float
    mouth: str


_VOWEL_SHAPES = {
    "a": "talk_a",
    "e": "talk_e",
    "i": "talk_e",
    "o": "talk_o",
    "u": "talk_o",
}


def text_mouth_timeline(text: str, start: float = 0.0, seconds_per_unit: float = 0.07) -> tuple[MouthCue, ...]:
    """Create a simple, deterministic mouth plan from dialogue text."""
    if not text.strip():
        return (MouthCue(float(start), mouth("closed").name),)

    cues: list[MouthCue] = []
    t = float(start)
    for token in re.findall(r"[A-Za-z]+|[^A-Za-z]+", text):
        if token.isalpha():
            for char in token.lower():
                if char in _VOWEL_SHAPES:
                    cues.append(MouthCue(t, _VOWEL_SHAPES[char]))
                    t += seconds_per_unit
        elif any(ch in token for ch in ".,!?;:"):
            cues.append(MouthCue(t, "talk_rest"))
            t += seconds_per_unit * 2
    if not cues:
        cues.append(MouthCue(float(start), "talk_rest"))
    return tuple(cues)
