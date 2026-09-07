"""Deterministic illustrated environments for ITANRA scene rendering."""

from __future__ import annotations

from PIL import Image, ImageDraw, ImageFilter

W, H = 1080, 1920


def _gradient(size: tuple[int, int], top: tuple[int, int, int], bottom: tuple[int, int, int]) -> Image.Image:
    width, height = size
    image = Image.new("RGB", size)
    pixels = image.load()
    for y in range(height):
        t = y / max(1, height - 1)
        color = tuple(round(top[i] * (1.0 - t) + bottom[i] * t) for i in range(3))
        for x in range(width):
            pixels[x, y] = color
    return image.convert("RGBA")


def _rounded(draw: ImageDraw.ImageDraw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def render_background(scene_name: str, frame_time: float) -> Image.Image:
    """Render a reusable warm home environment with a power-outage lighting beat."""
    is_nepa = "nepa" in scene_name.lower()
    power_off = is_nepa and frame_time >= 7.0

    if power_off:
        image = _gradient((W, H), (42, 50, 66), (20, 25, 34))
    else:
        image = _gradient((W, H), (238, 225, 205), (190, 166, 140))

    draw = ImageDraw.Draw(image, "RGBA")

    # Wall panels and ceiling line.
    draw.rectangle((0, 0, W, 1120), fill=(245, 237, 222, 110 if power_off else 235))
    draw.rectangle((0, 1040, W, 1080), fill=(145, 117, 94, 150))
    draw.rectangle((0, 1080, W, H), fill=(119, 88, 69, 255 if not power_off else 230))

    # Window and curtains give the characters a real environment instead of a flat canvas.
    window = (74, 180, 438, 690)
    _rounded(draw, window, 18, (230, 240, 238, 255), (71, 66, 61, 220), 8)
    draw.rectangle((94, 200, 418, 670), fill=(157, 196, 207, 255 if not power_off else 125))
    draw.line((256, 200, 256, 670), fill=(245, 245, 240, 220), width=8)
    draw.line((94, 435, 418, 435), fill=(245, 245, 240, 220), width=8)
    draw.rectangle((48, 160, 112, 710), fill=(117, 70, 72, 225))
    draw.rectangle((400, 160, 464, 710), fill=(117, 70, 72, 225))

    # Wall art / family frame.
    _rounded(draw, (560, 210, 920, 520), 12, (101, 72, 54, 255), (55, 44, 38, 230), 6)
    _rounded(draw, (582, 232, 898, 498), 6, (221, 199, 170, 255), (112, 87, 67, 220), 4)
    draw.ellipse((650, 278, 760, 388), fill=(176, 116, 82, 230))
    draw.polygon([(620, 465), (705, 360), (770, 450), (830, 350), (875, 465)], fill=(91, 133, 108, 210))

    # Television/console: a familiar Nigerian living-room anchor.
    _rounded(draw, (650, 610, 970, 850), 18, (32, 35, 39, 255), (16, 17, 19, 255), 8)
    draw.rectangle((674, 634, 946, 802), fill=(76, 91, 98, 255 if not power_off else 55))
    if not power_off:
        draw.ellipse((785, 690, 835, 740), fill=(221, 190, 118, 90))
    draw.rectangle((720, 850, 900, 890), fill=(70, 53, 45, 255))

    # Sofa behind the cast.
    _rounded(draw, (80, 880, 1000, 1250), 55, (119, 77, 74, 235), (73, 52, 49, 240), 7)
    _rounded(draw, (120, 950, 960, 1215), 38, (155, 103, 94, 245), (91, 61, 59, 220), 5)
    draw.line((340, 965, 340, 1200), fill=(102, 69, 66, 170), width=4)
    draw.line((740, 965, 740, 1200), fill=(102, 69, 66, 170), width=4)

    # Rug and floor perspective.
    _rounded(draw, (110, 1240, 970, 1810), 90, (180, 135, 112, 185 if not power_off else 130), (105, 78, 67, 180), 5)
    _rounded(draw, (175, 1310, 905, 1740), 70, (203, 160, 131, 110 if not power_off else 80), (137, 97, 80, 130), 3)

    # Plant adds organic detail and depth.
    draw.rectangle((900, 770, 945, 1010), fill=(101, 66, 48, 255))
    for bx, by, r in ((922, 735, 78), (866, 790, 65), (972, 790, 66), (900, 680, 55)):
        draw.ellipse((bx-r, by-r, bx+r, by+r), fill=(60, 105, 76, 205 if not power_off else 130))

    # Soft practical light that disappears when NEPA fails.
    if not power_off:
        glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow, "RGBA")
        gd.ellipse((170, 40, 880, 920), fill=(255, 215, 150, 38))
        glow = glow.filter(ImageFilter.GaussianBlur(90))
        image = Image.alpha_composite(image, glow)
    else:
        # Small cool rim from the window keeps silhouettes readable during blackout.
        glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow, "RGBA")
        gd.ellipse((-160, 120, 620, 1050), fill=(104, 157, 196, 38))
        glow = glow.filter(ImageFilter.GaussianBlur(85))
        image = Image.alpha_composite(image, glow)

    # Final vignette keeps attention on the acting area.
    vignette = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vignette, "RGBA")
    vd.rectangle((0, 0, W, H), outline=(0, 0, 0, 70), width=50)
    vignette = vignette.filter(ImageFilter.GaussianBlur(28))
    return Image.alpha_composite(image, vignette)
