"""Audio inspection helpers used as the timing source of truth."""

from __future__ import annotations

import subprocess
from pathlib import Path


def audio_duration(path: str | Path) -> float:
    """Read duration with ffprobe, avoiding Python audio-library dependencies."""
    source = Path(path)
    if not source.is_file():
        raise FileNotFoundError(f"Audio file does not exist: {source}")
    try:
        result = subprocess.run(
            [
                "ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1", str(source),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("ffprobe is required for real audio timing") from exc
    value = float(result.stdout.strip())
    if value <= 0:
        raise ValueError(f"Audio duration must be positive: {source}")
    return value
