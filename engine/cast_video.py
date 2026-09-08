"""Encode a CastScene directly to a vertical H.264 video."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from .cast_scene import CastScene
from .master_cast_renderer import H, W, render_master_cast

FPS = 30


def render_video(
    scene: CastScene,
    output: str | Path,
    repo_root: str | Path = ".",
    fps: int = FPS,
    audio: str | Path | None = None,
) -> Path:
    """Render scene frames and stream them to FFmpeg.

    Audio is optional and must be supplied separately; AFRITOON never bundles
    copyrighted music into the repository. When supplied, audio is padded or
    trimmed to the authored scene duration so the render cannot silently end
    early because a voice file is shorter than the picture.
    """
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("FFmpeg was not found. Install it with: pkg install ffmpeg")
    if fps <= 0:
        raise ValueError("fps must be positive")

    destination = Path(output)
    destination.parent.mkdir(parents=True, exist_ok=True)

    command = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}",
        "-r", str(fps), "-i", "-",
    ]
    if audio is not None:
        command += ["-i", str(audio), "-af", "apad"]
    command += [
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        "-t", f"{scene.duration:.3f}", str(destination),
    ]

    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    assert process.stdin is not None
    try:
        frame_count = max(1, int(round(scene.duration * fps)))
        for index in range(frame_count):
            t = index / fps
            frame = render_master_cast(scene, t, repo_root=repo_root)
            process.stdin.write(frame.tobytes())
        process.stdin.close()
        return_code = process.wait()
    except Exception:
        process.kill()
        process.wait()
        raise

    if return_code != 0:
        raise RuntimeError(f"FFmpeg failed with exit code {return_code}")
    return destination
