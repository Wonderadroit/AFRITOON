"""Pillow frame renderer and FFmpeg encoder."""

import os
import shutil
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageFont
from .character import Character
from .scene import Scene
from .actions import action_at

W, H, FPS = 1080, 1920, 30


def _font(size: int):
    candidates = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/system/fonts/Roboto-Bold.ttf"]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _draw_centered(draw, text, y, font, fill=(25, 25, 25)):
    box = draw.textbbox((0, 0), text, font=font)
    x = (W - (box[2] - box[0])) / 2
    draw.text((x, y), text, font=font, fill=fill)


def render(scene: Scene, output: str) -> str:
    """Render a Scene to a 9:16 H.264 MP4."""
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("FFmpeg was not found. Install it with: pkg install ffmpeg")
    os.makedirs(os.path.dirname(output) or ".", exist_ok=True)
    frame_count = max(1, int(round(scene.duration * FPS)))

    with tempfile.TemporaryDirectory(prefix="afritoon-") as tmp:
        for i in range(frame_count):
            t = i / FPS
            img = Image.new("RGB", (W, H), (238, 231, 214))
            draw = ImageDraw.Draw(img)
            draw.rectangle((0, 1180, W, H), fill=(205, 194, 170))
            _draw_centered(draw, scene.title, 55, _font(52))
            current = action_at(scene.timeline, t)
            action = current.name if current else "idle"
            expression = "neutral"
            if action in {"shock", "shocked"}:
                expression = "shocked"
            elif action in {"laugh", "dance", "vibe"}:
                expression = "happy"
            character = Character(name=str(scene.character.get("name", "Tunde")), x=float(scene.character.get("x", 540)), y=float(scene.character.get("y", 1120)), scale=float(scene.character.get("scale", 1)), action=action, expression=expression)
            character.draw(draw, t)
            draw.text((60, H - 150), action.upper(), font=_font(42), fill=(25, 25, 25))
            img.save(os.path.join(tmp, f"{i:06d}.png"))
        command = ["ffmpeg", "-y", "-framerate", str(FPS), "-i", os.path.join(tmp, "%06d.png"), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart", output]
        try:
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        except subprocess.CalledProcessError as exc:
            raise RuntimeError(f"FFmpeg failed:\n{exc.stderr[-2000:]}") from exc
    return output
