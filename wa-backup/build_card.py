#!/usr/bin/env python3
"""Build broadcast card 1080x1350 v3: ajakan gabung 2 grup WhatsApp.
Back to the proven story style (mascot + tracked title), stripped down:
no pill, no divider, no extra body lines, no fake WA icons in cards.
Mascot fills the top, tight vertical rhythm, text-only green cards.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1350
OUT = Path("/home/hatch/workspace/peka-content/wa-backup/wa-backup-card.png")
OUT.parent.mkdir(parents=True, exist_ok=True)
MASCOT = "/home/hatch/workspace/peka-content/piko/piko-speaking.png"

BASE = (14, 14, 16)
WHITE = (255, 255, 255)
YELLOW = (255, 214, 10)
GREY = (148, 163, 184)
GREEN = (37, 211, 102)
GREEN_DARK = (18, 140, 74)
INK = (17, 17, 17)

def font(name, size):
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}.ttf", size)

F_BIG = font("DejaVuSans-Bold", 120)
F_SUB = font("DejaVuSans-Bold", 68)
F_BODY = font("DejaVuSans", 34)
F_CARD_T = font("DejaVuSans-Bold", 40)
F_CARD_L = font("DejaVuSans-Bold", 34)
F_FOOT = font("DejaVuSans-Bold", 30)

img = Image.new("RGB", (W, H), BASE)
d = ImageDraw.Draw(img)

def text_size(text, f):
    bb = d.textbbox((0, 0), text, font=f)
    return bb[2] - bb[0], bb[3] - bb[1]

def text_center(y, text, f, fill):
    w, h = text_size(text, f)
    d.text(((W - w) / 2, y), text, font=f, fill=fill)
    return y + h

def tracked_center(y, text, f, fill, tracking=18):
    widths = [d.textbbox((0, 0), ch, font=f)[2] for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = (W - total) / 2
    for ch, w in zip(text, widths):
        d.text((x, y), ch, font=f, fill=fill)
        x += w + tracking

# faint dot grid
for gx in range(38, W, 76):
    for gy in range(38, H, 76):
        d.ellipse([gx - 2, gy - 2, gx + 2, gy + 2], fill=(24, 24, 28))

# soft yellow glow behind mascot
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([340, 140, 740, 540], fill=(255, 214, 10, 45))
glow = glow.filter(ImageFilter.GaussianBlur(100))
img.paste(glow, (0, 0), glow)
d = ImageDraw.Draw(img)

# yellow frame
d.rectangle([0, 0, W - 1, H - 1], outline=YELLOW, width=10)

# mascot, centered
mascot = Image.open(MASCOT).convert("RGBA").resize((360, 360), Image.LANCZOS)
img.paste(mascot, (540 - 180, 150), mascot)
d = ImageDraw.Draw(img)

# title + one line
tracked_center(560, "GABUNG", F_BIG, YELLOW, tracking=18)
text_center(700, "Grup WhatsApp", F_SUB, WHITE)

# two cards: white with black border (Peka link-hub style), dark title, green link
def card(y0, h, title, link):
    x0, x1 = 80, 1000
    d.rounded_rectangle([x0, y0, x1, y0 + h], radius=26, fill=WHITE,
                        outline=INK, width=4)
    d.rounded_rectangle([x0 + 6, y0 + 12, x0 + 20, y0 + h - 12], radius=7, fill=GREEN)
    tx = x0 + 60
    d.text((tx, y0 + 32), title, font=F_CARD_T, fill=INK)
    d.text((tx, y0 + 94), link, font=F_CARD_L, fill=GREEN_DARK)

card(860, 150, "Grup WhatsApp Peka", "s.peka.ai.id/k4iKBr")
card(1030, 150, "Grup WhatsApp Aeternum PremiApp", "s.peka.ai.id/7SZw07")

# footer
text_center(1270, "peka.ai.id", F_FOOT, YELLOW)

img.save(OUT)
print("saved", OUT, img.size)
