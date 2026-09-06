from PIL import Image, ImageDraw, ImageFont
import math
from .scene import CharacterState


def _font(size: int):
    for path in ("/system/fonts/Roboto-Regular.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass
    return ImageFont.load_default()


def draw_background(img: Image.Image, kind: str = "campus") -> None:
    d = ImageDraw.Draw(img)
    w, h = img.size
    d.rectangle((0, 0, w, h), fill=(225, 240, 247))
    horizon = int(h * .58)
    d.rectangle((0, horizon, w, h), fill=(115, 173, 100))
    if kind == "room":
        d.rectangle((0, 0, w, horizon), fill=(244, 232, 211))
        d.rectangle((0, horizon, w, h), fill=(160, 130, 105))
        d.rectangle((w*.12, h*.16, w*.88, h*.43), fill=(210, 225, 235), outline=(80,80,80), width=8)
        d.rectangle((w*.18, h*.22, w*.82, h*.37), fill=(180, 215, 235))
    else:
        d.rectangle((w*.08, h*.30, w*.92, horizon), fill=(198, 180, 160), outline=(80,80,80), width=7)
        for i in range(4):
            x = int(w*(.16+i*.21))
            d.rectangle((x, h*.34, x+120, h*.49), fill=(150,190,205), outline=(70,70,70), width=5)
        d.polygon([(w*.02,h*.58),(w*.98,h*.58),(w*.82,h),(w*.18,h)], fill=(92,92,92))
        d.line((w*.5,h*.58,w*.5,h), fill=(245,210,80), width=12)


def draw_character(img: Image.Image, state: CharacterState, name: str, t: float, scale: float = 1.0):
    d = ImageDraw.Draw(img)
    w, h = img.size
    cx, ground = int(state.x*w), int(state.y*h)
    s = min(w,h) * .00105 * scale
    bob = 0
    if state.action in {"vibe", "dance"}:
        bob = int(math.sin(t*10) * 18*s)
    if state.action == "shock":
        cx += int(math.sin(t*35)*8*s)
    head_r = int(125*s)
    body_w, body_h = int(220*s), int(300*s)
    head_y = ground - body_h - head_r*2 + bob
    # shadow
    d.ellipse((cx-body_w//2, ground-15*s, cx+body_w//2, ground+25*s), fill=(70,70,70))
    # legs
    leg_y = ground - 15*s
    d.line((cx-45*s, leg_y, cx-65*s, ground+130*s), fill=(35,35,45), width=max(8,int(35*s)))
    d.line((cx+45*s, leg_y, cx+65*s, ground+130*s), fill=(35,35,45), width=max(8,int(35*s)))
    # shoes
    d.ellipse((cx-105*s, ground+105*s, cx-30*s, ground+150*s), fill=(25,25,30))
    d.ellipse((cx+30*s, ground+105*s, cx+105*s, ground+150*s), fill=(25,25,30))
    # body
    d.rounded_rectangle((cx-body_w//2, ground-body_h, cx+body_w//2, ground-25*s), radius=int(45*s), fill=(40,95,170), outline=(25,45,80), width=max(3,int(8*s)))
    # arms
    arm_y = ground-body_h+85*s
    swing = math.sin(t*10)*45*s if state.action in {"vibe","dance"} else 0
    d.line((cx-body_w//2, arm_y, cx-145*s, arm_y+100*s+swing), fill=(135,82,48), width=max(8,int(38*s)))
    d.line((cx+body_w//2, arm_y, cx+145*s, arm_y+100*s-swing), fill=(135,82,48), width=max(8,int(38*s)))
    # neck/head
    d.rectangle((cx-35*s, head_y+head_r*1.6, cx+35*s, head_y+head_r*2.1), fill=(135,82,48))
    d.ellipse((cx-head_r, head_y, cx+head_r, head_y+head_r*2), fill=(145,90,55), outline=(70,45,30), width=max(3,int(7*s)))
    # hair
    d.arc((cx-head_r*.8,head_y-head_r*.15,cx+head_r*.8,head_y+head_r*.8),180,355,fill=(25,20,18),width=max(10,int(25*s)))
    # eyes/expression
    ey = head_y + head_r*.92
    ex = cx + state.facing*head_r*.35
    expr = state.expression
    if expr in {"shock","shocked","surprise"}:
        d.ellipse((ex-head_r*.45,ey-head_r*.3,ex-head_r*.1,ey+head_r*.05), fill="white", outline="black", width=4)
        d.ellipse((ex+head_r*.1,ey-head_r*.3,ex+head_r*.45,ey+head_r*.05), fill="white", outline="black", width=4)
        d.ellipse((ex-head_r*.30,ey-head_r*.18,ex-head_r*.18,ey-.06*head_r), fill="black")
        d.ellipse((ex+head_r*.18,ey-head_r*.18,ex+head_r*.30,ey-.06*head_r), fill="black")
        d.ellipse((ex-head_r*.28,ey+head_r*.35,ex+head_r*.28,ey+head_r*.7), outline="black", width=5)
    else:
        d.ellipse((ex-head_r*.42,ey-head_r*.18,ex-head_r*.12,ey+head_r*.12), fill="white", outline="black", width=4)
        d.ellipse((ex+head_r*.12,ey-head_r*.18,ex+head_r*.42,ey+head_r*.12), fill="white", outline="black", width=4)
        d.ellipse((ex-head_r*.30,ey-head_r*.08,ex-head_r*.18,ey+.04*head_r), fill="black")
        d.ellipse((ex+head_r*.18,ey-head_r*.08,ex+head_r*.30,ey+.04*head_r), fill="black")
        if expr in {"happy","laugh"}:
            d.arc((ex-head_r*.4,ey+head_r*.15,ex+head_r*.4,ey+head_r*.75),0,180,fill="black",width=7)
        elif expr in {"sad","worried"}:
            d.arc((ex-head_r*.35,ey+head_r*.4,ex+head_r*.35,ey+head_r*.8),180,360,fill="black",width=7)
        else:
            d.line((ex-head_r*.3,ey+head_r*.45,ex+head_r*.3,ey+head_r*.45),fill="black",width=7)
    label = f"{name} • {state.action}"
    d.rounded_rectangle((cx-190*s, head_y-head_r*.9, cx+190*s, head_y-head_r*.45), radius=15, fill=(255,255,255), outline=(40,40,40), width=3)
    d.text((cx-175*s, head_y-head_r*.82), label, font=_font(max(20,int(28*s))), fill=(20,20,20))
