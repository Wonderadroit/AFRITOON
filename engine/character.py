"""Procedural AFRITOON characters."""

from dataclasses import dataclass
from math import sin
from PIL import ImageDraw


@dataclass
class Character:
    name: str = "Tunde"
    x: float = 540
    y: float = 1120
    scale: float = 1.0
    expression: str = "neutral"
    action: str = "idle"

    def draw(self, draw: ImageDraw.ImageDraw, t: float) -> None:
        s = self.scale
        bounce = int(abs(sin(t * 8.0)) * 22 * s) if self.action in {"dance", "vibe"} else 0
        x, y = self.x, self.y - bounce
        r = 105 * s
        outline = (25, 25, 25)
        skin = (180, 125, 80)
        draw.ellipse((x-r, y-2*r, x+r, y), fill=skin, outline=outline, width=max(1, int(6*s)))
        draw.ellipse((x-135*s, y-330*s, x+135*s, y-60*s), fill=(35, 35, 35))
        eye_y = y - 145*s
        for ex in (-38, 38):
            draw.ellipse((x+ex-10*s, eye_y-10*s, x+ex+10*s, eye_y+10*s), fill=(255,255,255))
        if self.expression in {"shock", "shocked"}:
            draw.ellipse((x-22*s, y-90*s, x+22*s, y-35*s), fill=outline)
        elif self.expression in {"happy", "laugh"}:
            draw.arc((x-45*s, y-105*s, x+45*s, y-45*s), 0, 180, fill=outline, width=max(1, int(7*s)))
        else:
            draw.line((x-35*s, y-70*s, x+35*s, y-70*s), fill=outline, width=max(1, int(6*s)))
        body_top, body_bottom = y, y + 360*s
        draw.rounded_rectangle((x-125*s, body_top, x+125*s, body_bottom), radius=max(1, int(35*s)), fill=(50,95,170), outline=outline, width=max(1, int(6*s)))
        arm = 165*s
        draw.line((x-105*s, y+45*s, x-arm, y+160*s), fill=skin, width=max(1, int(28*s)))
        draw.line((x+105*s, y+45*s, x+arm, y+160*s), fill=skin, width=max(1, int(28*s)))
        draw.line((x-60*s, body_bottom, x-75*s, body_bottom+180*s), fill=outline, width=max(1, int(35*s)))
        draw.line((x+60*s, body_bottom, x+75*s, body_bottom+180*s), fill=outline, width=max(1, int(35*s)))
