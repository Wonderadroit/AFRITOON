"""Provider-neutral TTS execution contracts for AFRITOON."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from .voice import VoiceProfile


@dataclass(frozen=True)
class AudioResult:
    path: str
    duration: float | None = None
    provider: str = "unknown"


class TTSProvider(Protocol):
    """Minimal contract implemented by local or hosted TTS backends."""

    name: str

    def synthesize(self, text: str, voice: VoiceProfile, output_path: str | Path) -> AudioResult:
        ...


class FileTTSProvider:
    """Testing/development provider that accepts pre-generated audio files.

    It deliberately performs no synthesis. This lets the production pipeline be
    exercised on Termux/CI without downloading a large model or requiring an API.
    """

    name = "file"

    def synthesize(self, text: str, voice: VoiceProfile, output_path: str | Path) -> AudioResult:
        source = Path(text).expanduser()
        if not source.is_file():
            raise FileNotFoundError(f"Audio source does not exist: {source}")
        target = Path(output_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(source.read_bytes())
        return AudioResult(str(target), None, self.name)
