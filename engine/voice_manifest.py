"""Build a complete, inspectable voice manifest from dialogue."""

from __future__ import annotations

from dataclasses import asdict
from typing import Iterable

from .dialogue import DialogueLine
from .mouth_timing import estimate_duration, mouth_cues
from .voice_director import voice_cues


def build_voice_manifest(lines: Iterable[DialogueLine]) -> list[dict[str, object]]:
    """Return serializable voice/mouth instructions for a scene."""
    manifest: list[dict[str, object]] = []
    for cue in voice_cues(lines):
        duration = cue.duration or estimate_duration(cue.text)
        manifest.append(
            {
                "character": cue.character,
                "voice": asdict(cue.voice),
                "text": cue.text,
                "at": cue.at,
                "duration": duration,
                "mouth": [
                    {
                        "at": item.at,
                        "duration": item.duration,
                        "state": item.state.name,
                    }
                    for item in mouth_cues(cue.text, cue.at, duration)
                ],
            }
        )
    return manifest
