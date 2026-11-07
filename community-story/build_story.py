#!/usr/bin/env python3
"""Build IG/FB story 1080x1920: ajakan gabung Komunitas Peka AI.
Peka brand: black #111111 + yellow #FFD60A. Links printed as admin shortlinks.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
OUT = Path("/home/hatch/workspace/peka-content/community-story/2026-11-07/story-1080x1920.png")
OUT.parent.mkdir(parents=True, exist_ok=True)

BLACK = (17, 17, 17)
WHITE = (255, 255, 255)
YELLOW = (255, 214, 10)
GREY = (148, 163, 184)
GREEN = (37, 211, 102)
BLUE = (34, 158, 217)
DARKTXT = (17, 17, 17)

def font(name, size):
    p = f"/usr/share/fonts/truetype/dejavu/{name}.ttf"
    return ImageFont.truetype(p, size)

F_TITLE = font("DejaVuSans-Bold", 96)
F_BODY = font("DejaVuSans", 42)
F_BTN = font("DejaVuSans-Bold", 50)
F_LINK = font("DejaVuSans-Bold", 38)
F_EYE = font("DejaVuSans-Bold", 34)
F_NOTE = font("DejaVuSans", 38)
F_FOOT = font("DejaVuSans-Bold", 44)

img = Image.new("RGB", (W, H), BLACK)
d = ImageDraw.Draw(img)

def text_center(y, text, f, fill):
    bb = d.textbbox((0, 0), text, font=f)
    w = bb[2] - bb[0]
    d.text(((W - w) / 2 - bb[0], y), text, font=f, fill=fill)
    return y + (bb[3] - bb[1])

def rounded_rect(x0, y0, x1, y1, r, fill):
    d.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=fill)

def tracked_center(y, text, f, fill, tracking=10):
    # draw with manual letter spacing
    widths = [d.textbbox((0, 0), ch, font=f)[2] for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = (W - total) / 2
    for ch, w in zip(text, widths):
        d.text((x, y), ch, font=f, fill=fill)
        x += w + tracking

# yellow top strip
d.rectangle([0, 0, W, 14], fill=YELLOW)

# people-icon tile (yellow rounded square + two black person shapes)
TX0, TY0, TX1, TY1 = 450, 150, 630, 330
rounded_rect(TX0, TY0, TX1, TY1, 36, YELLOW)
cx = (TX0 + TX1) // 2
# person left (smaller, behind)
d.ellipse([cx - 62, TY0 + 62, cx - 22, TY0 + 102], fill=BLACK)
d.pieslice([cx - 78, TY0 + 108, cx - 6, TY0 + 180], 180, 360, fill=BLACK)
# person right (front)
d.ellipse([cx + 8, TY0 + 58, cx + 52, TY0 + 102], fill=BLACK)
d.pieslice([cx - 8, TY0 + 108, cx + 68, TY0 + 180], 180, 360, fill=BLACK)

# eyebrow
tracked_center(390, "KOMUNITAS PEKA AI", F_EYE, YELLOW, tracking=12)

# title (2 lines)
y = text_center(470, "Gabung Komunitas", F_TITLE, WHITE)
y = text_center(y + 8, "Peka AI", F_TITLE, YELLOW)

# body (2 lines)
text_center(800, "Info AI terbaru, bansos, dan diskusi", F_BODY, GREY)
text_center(855, "seputar AI. Info naik duluan di grup,", F_BODY, GREY)
text_center(910, "sebelum naik ke feed.", F_BODY, GREY)

# WhatsApp card
rounded_rect(90, 1010, 990, 1230, 28, GREEN)
text_center(1050, "Gabung Grup WhatsApp", F_BTN, WHITE)
text_center(1120, "s.peka.ai.id/k4iKBr", F_LINK, WHITE)

# Telegram card
rounded_rect(90, 1270, 990, 1490, 28, BLUE)
text_center(1310, "Gabung Grup Telegram", F_BTN, WHITE)
text_center(1380, "s.peka.ai.id/pP4SHD", F_LINK, WHITE)

# note + footer
text_center(1560, "Gratis, tanpa daftar.", F_NOTE, GREY)
d.line([340, 1660, 740, 1660], fill=(60, 60, 60), width=2)
text_center(1700, "peka.ai.id", F_FOOT, YELLOW)
text_center(1760, "Informasi AI terbaru.", font("DejaVuSans", 34), GREY)

img.save(OUT, "PNG")
print(f"saved {OUT} {img.size}")
