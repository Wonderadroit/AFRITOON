"""Pillow frame renderer and FFmpeg encoder."""

import os
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


def render(scene: Scene, output: str) -> str:
    os.makedirs(os.path.dirname(output) or ".", exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="afritoon-") as tmp:
        for i in range(int(scene.duration * FPS)):
            t = i / FPS
            img = Image.new("RGB", (W, H), (238, 231, 214))
            draw = ImageDraw.Draw(img)
            draw.rectangle((0, 1180, W, H), fill=(205, 194, 170))
            draw.text((60, 55), scene.title, font=_font(52), fill=(25,25,25))
            a = action_at(scene.timeline, t)
            action = a.name if a else "idle"
            expression = "neutral"
            if action in {"shock", "shocked"}: expression = "shocked"
            elif action in {"laugh", "dance", "vibe"}: expression = "happy"
            c = Character(name=str(scene.character.get("name", "Tunde")), x=float(scene.character.get("x", 540)), y=float(scene.character.get("y", 1120)), scale=float(scene.character.get("scale", 1)), action=action, expression=expression)
            c.draw(draw, t)
            draw.text((60, H-150), action.upper(), font=_font(42), fill=(25,25,25))
            img.save(os.path.join(tmp, f"{i:06d}.png"))
        subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", os.path.join(tmp, "%06d.png"), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart", output], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    return output
