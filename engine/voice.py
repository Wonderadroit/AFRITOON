"""Voice contracts for AFRITOON character dialogue.

The engine deliberately separates voice selection from the TTS provider. A local,
open-source Nigerian voice model can be plugged in later without changing scenes.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Protocol


@dataclass(frozen=True)
class VoiceProfile:
    id: str
    character: str
    language: str = "en-NG"
    style: str = "natural"
    speed: float = 1.0
    pitch: float = 0.0


VOICE_PROFILES: Mapping[str, VoiceProfile] = {
    "tunde_v1": VoiceProfile("tunde_v1", "tunde", "en-NG", "energetic", 1.05, 0.0),
    "seyi_v1": VoiceProfile("seyi_v1", "seyi", "en-NG", "deadpan", 0.92, -0.5),
    "mama_v1": VoiceProfile("mama_v1", "mama", "en-NG", "warm_authoritative", 0.88, -0.2),
}


class VoiceProvider(Protocol):
    """Provider contract for text-to-speech backends."""

    def synthesize(self, text: str, voice: VoiceProfile, output_path: str) -> str:
        ...


def voice_profile(name: str) -> VoiceProfile:
    key = str(name).strip().lower()
    if key not in VOICE_PROFILES:
        raise ValueError(f"Unknown AFRITOON voice: {name}")
    return VOICE_PROFILES[key]


def character_voice(character_id: str) -> VoiceProfile:
    key = str(character_id).strip().lower()
    for profile in VOICE_PROFILES.values():
        if profile.character == key:
            return profile
    raise ValueError(f"No voice profile for character: {character_id}")
