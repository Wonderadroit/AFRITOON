"""Procedural AFRITOON characters."""

from dataclasses import dataclass
from PIL import ImageDraw


@dataclass
class Character:
    name: str = "Tunde"
    x: float = 540
    y: float = 1320
    scale: float = 1.0
    expression: str = "neutral"
    action: str = "idle"

    def draw(self, draw: ImageDraw.ImageDraw, t: float) -> None:
        s = self.scale
        bounce = 0
        if self.action in {"dance", "vibe"}:
            bounce = int(abs(__import__("math").sin(t * 8)) * 22 * s)
        x, y = self.x, self.y - bounce
        r = int(105 * s)
        draw.ellipse((x-r, y-r*2, x+r, y), fill=(180, 125, 80), outline=(25, 25, 25), width=6)
        draw.ellipse((x-135*s, y-330*s, x+135*s, y-60*s), fill=(35, 35, 35))
        eye_y = y - 145*s
        for ex in (-38, 38):
            draw.ellipse((x+ex-10*s, eye_y-10*s, x+ex+10*s, eye_y+10*s), fill=(255,255,255))
        mouth = self.expression
        if mouth in {"shock", "shocked"}:
            draw.ellipse((x-22*s, y-90*s, x+22*s, y-35*s), fill=(25,25,25))
        elif mouth in {"happy", "laugh"}:
            draw.arc((x-45*s, y-105*s, x+45*s, y-45*s), 0, 180, fill=(25,25,25), width=7)
        else:
            draw.line((x-35*s, y-70*s, x+35*s, y-70*s), fill=(25,25,25), width=6)
        body_top = y
        body_bottom = y + 360*s
        draw.rounded_rectangle((x-125*s, body_top, x+125*s, body_bottom), radius=int(35*s), fill=(50,95,170), outline=(25,25,25), width=6)
        arm = 165*s
        draw.line((x-105*s, y+45*s, x-arm, y+160*s), fill=(180,125,80), width=int(28*s))
        draw.line((x+105*s, y+45*s, x+arm, y+160*s), fill=(180,125,80), width=int(28*s))
        draw.line((x-60*s, body_bottom, x-75*s, body_bottom+180*s), fill=(25,25,25), width=int(35*s))
        draw.line((x+60*s, body_bottom, x+75*s, body_bottom+180*s), fill=(25,25,25), width=int(35*s))
