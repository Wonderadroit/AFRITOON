from pathlib import Path

import pytest

from engine.audio_probe import audio_duration
from engine.dialogue import DialogueLine
from engine.dialogue_audio import synthesize_dialogue
from engine.tts_provider import FileTTSProvider
from engine.voice import character_voice


def test_file_provider_copies_audio(tmp_path: Path):
    source = tmp_path / "source.wav"
    source.write_bytes(b"RIFF-test")
    output = tmp_path / "out"
    line = DialogueLine("tunde", str(source), 0.5)
    result = FileTTSProvider().synthesize(line.text, character_voice("tunde"), output / "voice.wav")
    assert Path(result.path).read_bytes() == b"RIFF-test"
    assert result.provider == "file"


def test_audio_duration_requires_existing_file(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        audio_duration(tmp_path / "missing.wav")


def test_dialogue_audio_uses_provider_duration(tmp_path: Path):
    source = tmp_path / "voice.wav"
    source.write_bytes(b"audio")

    class Provider:
        name = "fake"

        def synthesize(self, text, voice, output_path):
            from engine.tts_provider import AudioResult
            Path(output_path).write_bytes(source.read_bytes())
            return AudioResult(str(output_path), 1.25, self.name)

    line = DialogueLine("tunde", "Hello", 0.5)
    result = synthesize_dialogue([line], Provider(), tmp_path / "out")
    assert len(result) == 1
    assert result[0].duration == 1.25
    assert result[0].voice == "tunde_v1"
