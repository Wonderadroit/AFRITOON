"""Reusable human-style Tunde character rig for AFRITOON."""

from dataclasses import dataclass
from PIL import ImageDraw


@dataclass
class CharacterStyle:
    skin: tuple = (117, 72, 45)
    hair: tuple = (35, 25, 20)
    shirt: tuple = (40, 95, 175)
    trousers: tuple = (45, 45, 55)
    shoes: tuple = (25, 25, 25)
    outline: tuple = (25, 20, 18)


class Tunde:
    """Reusable full-body 2D character with pose and expression states."""

    def __init__(self, x=540, y=1150, scale=1.0, pose="idle", expression="neutral"):
        self.x, self.y, self.scale = float(x), float(y), max(0.1, float(scale))
        self.pose, self.expression = pose, expression
        self.s = CharacterStyle()

    def _p(self, value):
        return int(value * self.scale)

    def draw(self, d: ImageDraw.ImageDraw):
        x, y, p, s = self.x, self.y, self._p, self.s
        stroke = max(2, p(5))
        d.ellipse((x-p(190), y+p(215), x+p(190), y+p(265)), fill=(170,160,145))

        # Legs and shoes.
        shift = p(28) if self.pose == "walk" else 0
        d.rounded_rectangle((x-p(105)+shift, y+p(65), x-p(20)+shift, y+p(225)), radius=p(25), fill=s.trousers, outline=s.outline, width=stroke)
        d.rounded_rectangle((x+p(20)-shift, y+p(65), x+p(105)-shift, y+p(225)), radius=p(25), fill=s.trousers, outline=s.outline, width=stroke)
        d.ellipse((x-p(125)+shift, y+p(205), x-p(5)+shift, y+p(255)), fill=s.shoes, outline=s.outline, width=stroke)
        d.ellipse((x+p(5)-shift, y+p(205), x+p(125)-shift, y+p(255)), fill=s.shoes, outline=s.outline, width=stroke)

        # Torso and neck.
        d.rounded_rectangle((x-p(125), y-p(120), x+p(125), y+p(90)), radius=p(45), fill=s.shirt, outline=s.outline, width=stroke)
        d.rectangle((x-p(42), y-p(165), x+p(42), y-p(105)), fill=s.skin, outline=s.outline, width=stroke)

        # Arms change pose while remaining part of the same rig.
        if self.pose in {"vibe", "dance"}:
            ends = ((-180, -150), (180, -150))
        elif self.pose in {"shock", "shocked"}:
            ends = ((-175, -185), (175, -185))
        elif self.pose == "check_pocket":
            ends = ((-55, 45), (165, 45))
        else:
            ends = ((-165, 45), (165, 45))
        for side, (ex, ey) in ((-1, ends[0]), (1, ends[1])):
            hx, hy = x + side*p(abs(ex)), y + p(ey)
            d.line((x+side*p(105), y-p(55), hx, hy), fill=s.skin, width=p(38))
            d.ellipse((hx-p(22), hy-p(22), hx+p(22), hy+p(22)), fill=s.skin, outline=s.outline, width=max(1,p(3)))

        # Head, ears and hair.
        d.ellipse((x-p(135), y-p(360), x+p(135), y-p(105)), fill=s.skin, outline=s.outline, width=stroke)
        d.pieslice((x-p(138), y-p(375), x+p(138), y-p(145)), 180, 360, fill=s.hair, outline=s.outline)
        d.rounded_rectangle((x-p(105), y-p(325), x+p(105), y-p(245)), radius=p(28), fill=s.hair)
        d.ellipse((x-p(150), y-p(280), x-p(115), y-p(210)), fill=s.skin, outline=s.outline, width=max(1,p(3)))
        d.ellipse((x+p(115), y-p(280), x+p(150), y-p(210)), fill=s.skin, outline=s.outline, width=max(1,p(3)))

        # Eyes, pupils and eyebrows.
        eye_y = y-p(245)
        for cx in (x-p(55), x+p(55)):
            d.ellipse((cx-p(20), eye_y-p(12), cx+p(20), eye_y+p(15)), fill=(250,250,245), outline=s.outline, width=max(1,p(3)))
            pupil = p(10 if self.expression == "shocked" else 7)
            d.ellipse((cx-pupil, eye_y-pupil, cx+pupil, eye_y+pupil), fill=(20,20,20))
        brow_y = y-p(280)
        lift = p(14) if self.expression == "shocked" else 0
        d.line((x-p(82), brow_y, x-p(28), brow_y-lift), fill=s.hair, width=p(11))
        d.line((x+p(28), brow_y-lift, x+p(82), brow_y), fill=s.hair, width=p(11))

        # Nose and expressive mouth.
        d.line((x, y-p(235), x-p(12), y-p(195), x+p(12), y-p(190)), fill=s.outline, width=p(6), joint="curve")
        if self.expression == "shocked":
            d.ellipse((x-p(30), y-p(175), x+p(30), y-p(105)), fill=(45,25,25), outline=s.outline, width=p(5))
        elif self.expression in {"happy", "laugh"}:
            d.arc((x-p(48), y-p(190), x+p(48), y-p(120)), 15, 165, fill=s.outline, width=p(8))
        elif self.expression in {"sad", "angry"}:
            d.arc((x-p(42), y-p(125), x+p(42), y-p(175)), 200, 340, fill=s.outline, width=p(7))
        else:
            d.line((x-p(38), y-p(145), x+p(38), y-p(145)), fill=s.outline, width=p(7))
