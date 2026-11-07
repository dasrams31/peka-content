#!/usr/bin/env python3
"""Build IG/FB story 1080x1920 v2: ajakan gabung Komunitas Peka AI.
Anti-slop: dot-grid texture, soft glow, mascot P on white disc, floating
chat bubbles, two-tone title, icon cards. Peka brand black + yellow.
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
DARK = (30, 30, 34)
GREEN = (37, 211, 102)
BLUE = (34, 158, 217)

def font(name, size):
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}.ttf", size)

F_BIG = font("DejaVuSans-Bold", 150)
F_SUB = font("DejaVuSans-Bold", 82)
F_BODY = font("DejaVuSans", 37)
F_CHIP = font("DejaVuSans-Bold", 34)
F_CARD_T = font("DejaVuSans-Bold", 46)
F_CARD_L = font("DejaVuSans-Bold", 36)
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

# 1. dot grid texture
for gx in range(38, W, 76):
    for gy in range(38, H, 76):
        d.ellipse([gx - 3, gy - 3, gx + 3, gy + 3], fill=(26, 26, 30))

# 2. soft yellow glow behind mascot
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([190, 90, 890, 790], fill=(255, 214, 10, 55))
glow = glow.filter(ImageFilter.GaussianBlur(110))
img.paste(glow, (0, 0), glow)
d = ImageDraw.Draw(img)

# 3. yellow frame
d.rectangle([0, 0, W - 1, H - 1], outline=YELLOW, width=10)

# 4. top pill: KOMUNITAS PEKA AI
pill_text = "KOMUNITAS PEKA AI"
pw, ph = text_size(pill_text, F_PILL)
px0 = (W - pw) // 2 - 34
py0, py1 = 64, 64 + ph + 30
d.rounded_rectangle([px0, py0, px0 + pw + 68, py1], radius=(py1 - py0) // 2, fill=YELLOW)
d.text((px0 + 34, py0 + 13), pill_text, font=F_PILL, fill=(17, 17, 17))

# 5. white disc + mascot (speaking)
cx, cy, r = 540, 450, 250
d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE)
d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=YELLOW, width=6)
mascot = Image.open(MASCOT).convert("RGBA").resize((500, 500), Image.LANCZOS)
img.paste(mascot, (cx - 250, cy - 250), mascot)
d = ImageDraw.Draw(img)

# 6. floating chat bubbles
def bubble(x, y, text, f, bg, fg, border=None, tail="right"):
    tw, th = text_size(text, f)
    w, h = tw + 44, th + 30
    if border:
        d.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=bg, outline=border, width=3)
    else:
        d.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=bg)
    if tail == "right":
        d.polygon([(x + w - 28, y + h - 6), (x + w + 16, y + h + 22), (x + w - 52, y + h - 2)], fill=bg)
    else:
        d.polygon([(x + 28, y + h - 6), (x - 16, y + h + 22), (x + 52, y + h - 2)], fill=bg)
    d.text((x + 22, y + 13), text, font=f, fill=fg)
    return w, h

bubble(58, 330, "Bansos!", F_CHIP, WHITE, (17, 17, 17), tail="right")
bubble(748, 250, "AI terbaru", F_CHIP, DARK, YELLOW, border=YELLOW, tail="left")

# 7. title: GABUNG (yellow, tracked) + Komunitas Peka AI (two-tone)
def tracked_center(y, text, f, fill, tracking=14):
    widths = [d.textbbox((0, 0), ch, font=f)[2] for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = (W - total) / 2
    for ch, w in zip(text, widths):
        d.text((x, y), ch, font=f, fill=fill)
        x += w + tracking
    _, h = text_size(text, f)
    return y + h

y = tracked_center(770, "GABUNG", F_BIG, YELLOW, tracking=18)
# two-tone line: "Komunitas " white + "Peka AI" yellow
part1, part2 = "Komunitas ", "Peka AI"
w1, h1 = text_size(part1, F_SUB)
w2, _ = text_size(part2, F_SUB)
x0 = (W - (w1 + w2)) // 2
d.text((x0, 950), part1, font=F_SUB, fill=WHITE)
d.text((x0 + w1, 950), part2, font=F_SUB, fill=YELLOW)

# 8. chips row: AI Terbaru / Bansos / Diskusi
chips = ["AI Terbaru", "Bansos", "Diskusi"]
cw = []
for c in chips:
    w, h = text_size(c, F_CHIP)
    cw.append(w + 56)
gap = 20
total = sum(cw) + gap * (len(chips) - 1)
x = (W - total) / 2
cy0 = 1080
for c, w in zip(chips, cw):
    d.rounded_rectangle([x, cy0, x + w, cy0 + 62], radius=31, outline=YELLOW, width=3)
    tw, th = text_size(c, F_CHIP)
    d.text((x + (w - tw) / 2, cy0 + 12), c, font=F_CHIP, fill=YELLOW)
    x += w + gap

# 9. body line
text_center(1180, "Info naik duluan di grup, sebelum naik ke feed.", F_BODY, GREY)

# 10. group cards with icons
def wa_icon(cx, cy, r, color):
    # white circle handled by caller; draw green handset: arc + end dots
    d.arc([cx - r, cy - r, cx + r, cy + r], start=195, end=345, fill=color, width=13)
    import math
    for ang in (195, 345):
        a = math.radians(ang)
        ex = cx + (r - 2) * math.cos(a)
        ey = cy + (r - 2) * math.sin(a)
        d.ellipse([ex - 11, ey - 11, ex + 11, ey + 11], fill=color)

def tg_icon(cx, cy, s, color):
    # paper plane polygon
    pts = [(cx - s, cy - s * 0.15), (cx + s, cy - s * 0.55), (cx + s * 0.15, cy + s * 0.75), (cx - s * 0.12, cy + s * 0.28)]
    d.polygon(pts, fill=color)
    d.line([(cx + s, cy - s * 0.55), (cx - s * 0.12, cy + s * 0.28)], fill=WHITE, width=4)

def card(y0, h, bg, title, link, icon_fn, icon_color):
    x0, x1 = 80, 1000
    d.rounded_rectangle([x0, y0, x1, y0 + h], radius=28, fill=bg)
    icx, icy, ir = x0 + 95, y0 + h // 2, 58
    d.ellipse([icx - ir, icy - ir, icx + ir, icy + ir], fill=WHITE)
    icon_fn(icx, icy, 34, icon_color)
    tx = x0 + 190
    d.text((tx, y0 + 42), title, font=F_CARD_T, fill=WHITE)
    d.text((tx, y0 + 108), link, font=F_CARD_L, fill=WHITE)

card(1260, 190, GREEN, "Gabung Grup WhatsApp", "s.peka.ai.id/k4iKBr", wa_icon, GREEN)
card(1480, 190, BLUE, "Gabung Grup Telegram", "s.peka.ai.id/pP4SHD", tg_icon, BLUE)

# 11. footer
text_center(1715, "Gratis, tanpa daftar.", F_NOTE, GREY)
text_center(1785, "peka.ai.id", F_FOOT, YELLOW)

img.save(OUT, "PNG")
print(f"saved {OUT} {img.size}")
