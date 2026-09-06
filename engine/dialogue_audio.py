"""Resolve dialogue into provider audio and evidence-based timing."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .audio_probe import audio_duration
from .dialogue import DialogueLine
from .tts_provider import AudioResult, TTSProvider
from .voice_director import voice_cues


@dataclass(frozen=True)
class DialogueAudio:
    character: str
    text: str
    at: float
    voice: str
    path: str
    duration: float
    provider: str


def synthesize_dialogue(
    lines: Iterable[DialogueLine], provider: TTSProvider, output_dir: str | Path
) -> tuple[DialogueAudio, ...]:
    target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    results: list[DialogueAudio] = []
    for index, cue in enumerate(voice_cues(lines)):
        output = target_dir / f"{index:03d}_{cue.character}_{cue.at:.2f}.wav"
        result: AudioResult = provider.synthesize(cue.text, cue.voice, output)
        duration = result.duration if result.duration is not None else audio_duration(result.path)
        results.append(DialogueAudio(
            character=cue.character,
            text=cue.text,
            at=cue.at,
            voice=cue.voice.id,
            path=result.path,
            duration=duration,
            provider=result.provider,
        ))
    return tuple(results)
