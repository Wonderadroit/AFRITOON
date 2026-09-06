"""Turn dialogue records into provider-ready voice instructions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .dialogue import DialogueLine
from .voice import VoiceProfile, character_voice, voice_profile


@dataclass(frozen=True)
class VoiceCue:
    character: str
    text: str
    at: float
    voice: VoiceProfile
    duration: float | None = None


def voice_cues(lines: Iterable[DialogueLine]) -> tuple[VoiceCue, ...]:
    """Resolve every dialogue line to a stable character voice."""
    result: list[VoiceCue] = []
    for line in sorted(lines, key=lambda item: item.at):
        profile = voice_profile(line.voice) if line.voice else character_voice(line.character)
        if profile.character != line.character.strip().lower():
            raise ValueError(
                f"Voice {profile.id} belongs to {profile.character}, not {line.character}"
            )
        result.append(VoiceCue(line.character, line.text, line.at, profile, line.duration))
    return tuple(result)
