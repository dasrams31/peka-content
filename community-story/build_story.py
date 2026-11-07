#!/usr/bin/env python3
"""Build IG/FB story 1080x1920 v3: ajakan gabung Komunitas Peka AI.
Tidy edition: fewer elements, strict center column, even rhythm.
Mascot directly on dark bg with soft glow (no disc), no floating bubbles,
no chips row. One big word + one clean line + divider + two slim cards.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920
OUT = Path("/home/hatch/workspace/peka-content/community-story/2026-11-07/story-1080x1920.png")
OUT.parent.mkdir(parents=True, exist_ok=True)
MASCOT = "/home/hatch/workspace/peka-content/piko/piko-speaking.png"

BASE = (14, 14, 16)
WHITE = (255, 255, 255)
YELLOW = (255, 214, 10)
GREY = (148, 163, 184)
GREEN = (37, 211, 102)
BLUE = (34, 158, 217)

def font(name, size):
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}.ttf", size)

F_BIG = font("DejaVuSans-Bold", 132)
F_SUB = font("DejaVuSans-Bold", 76)
F_BODY = font("DejaVuSans", 37)
F_CARD_T = font("DejaVuSans-Bold", 44)
F_CARD_L = font("DejaVuSans-Bold", 34)
F_NOTE = font("DejaVuSans", 37)
F_FOOT = font("DejaVuSans-Bold", 46)
F_PILL = font("DejaVuSans-Bold", 32)

img = Image.new("RGB", (W, H), BASE)
d = ImageDraw.Draw(img)

def text_size(text, f):
    bb = d.textbbox((0, 0), text, font=f)
    return bb[2] - bb[0], bb[3] - bb[1]

def text_center(y, text, f, fill):
    w, h = text_size(text, f)
    d.text(((W - w) / 2, y), text, font=f, fill=fill)
    return y + h

def tracked_center(y, text, f, fill, tracking=16):
    widths = [d.textbbox((0, 0), ch, font=f)[2] for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = (W - total) / 2
    for ch, w in zip(text, widths):
        d.text((x, y), ch, font=f, fill=fill)
        x += w + tracking

# faint dot grid (very subtle)
for gx in range(38, W, 76):
    for gy in range(38, H, 76):
        d.ellipse([gx - 2, gy - 2, gx + 2, gy + 2], fill=(24, 24, 28))

# soft yellow glow behind mascot
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([290, 190, 790, 690], fill=(255, 214, 10, 45))
glow = glow.filter(ImageFilter.GaussianBlur(100))
img.paste(glow, (0, 0), glow)
d = ImageDraw.Draw(img)

# yellow frame
d.rectangle([0, 0, W - 1, H - 1], outline=YELLOW, width=10)

# top pill: KOMUNITAS PEKA AI
pill_text = "KOMUNITAS PEKA AI"
pw, ph = text_size(pill_text, F_PILL)
px0 = (W - pw) // 2 - 34
py0, py1 = 110, 110 + ph + 30
d.rounded_rectangle([px0, py0, px0 + pw + 68, py1], radius=(py1 - py0) // 2, fill=YELLOW)
d.text((px0 + 34, py0 + 13), pill_text, font=F_PILL, fill=(17, 17, 17))

# mascot, centered, no disc
mascot = Image.open(MASCOT).convert("RGBA").resize((460, 460), Image.LANCZOS)
img.paste(mascot, (540 - 230, 230), mascot)
d = ImageDraw.Draw(img)

# title
tracked_center(770, "GABUNG", F_BIG, YELLOW, tracking=18)
text_center(930, "Komunitas Peka AI", F_SUB, WHITE)

# subtitle
text_center(1060, "Info AI terbaru, bansos, dan diskusi.", F_BODY, GREY)

# divider
d.rectangle([495, 1160, 585, 1165], fill=YELLOW)

# group cards (slim, uniform)
def wa_icon(cx, cy, r, color):
    import math
    d.arc([cx - r, cy - r, cx + r, cy + r], start=195, end=345, fill=color, width=12)
    for ang in (195, 345):
        a = math.radians(ang)
        ex = cx + (r - 2) * math.cos(a)
        ey = cy + (r - 2) * math.sin(a)
        d.ellipse([ex - 10, ey - 10, ex + 10, ey + 10], fill=color)

def tg_icon(cx, cy, s, color):
    pts = [(cx - s, cy - s * 0.15), (cx + s, cy - s * 0.55), (cx + s * 0.15, cy + s * 0.75), (cx - s * 0.12, cy + s * 0.28)]
    d.polygon(pts, fill=color)
    d.line([(cx + s, cy - s * 0.55), (cx - s * 0.12, cy + s * 0.28)], fill=WHITE, width=4)

def card(y0, h, bg, title, link, icon_fn, icon_color):
    x0, x1 = 80, 1000
    d.rounded_rectangle([x0, y0, x1, y0 + h], radius=26, fill=bg)
    icx, icy, ir = x0 + 100, y0 + h // 2, 52
    d.ellipse([icx - ir, icy - ir, icx + ir, icy + ir], fill=WHITE)
    icon_fn(icx, icy, 30, icon_color)
    tx = x0 + 195
    d.text((tx, y0 + 40), title, font=F_CARD_T, fill=WHITE)
    d.text((tx, y0 + 100), link, font=F_CARD_L, fill=WHITE)

card(1240, 170, GREEN, "Gabung Grup WhatsApp", "s.peka.ai.id/k4iKBr", wa_icon, GREEN)
card(1440, 170, BLUE, "Gabung Grup Telegram", "s.peka.ai.id/pP4SHD", tg_icon, BLUE)

# footer
text_center(1690, "Gratis, tanpa daftar.", F_NOTE, GREY)
text_center(1760, "peka.ai.id", F_FOOT, YELLOW)

img.save(OUT, "PNG")
print(f"saved {OUT} {img.size}")
