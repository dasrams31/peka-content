#!/usr/bin/env python3
"""Build blog cover for Coba Dulu #03 (Pollinations), libur blog-only.
2048x1152, Peka dark + yellow. Uses the verified generated robot image.
No em-dash in any text."""
from PIL import Image, ImageDraw, ImageFont

OUT = "/home/hatch/workspace/peka-content/coba-dulu/out/2026-11-27-pollinations-bikin-ilustrasi-dari-teks"
IMG = "/home/hatch/workspace/peka-content/images/pollinations-bikin-ilustrasi-dari-teks.jpg"

W, H = 2048, 1152
BG = (17, 17, 17)
YELLOW = (255, 214, 10)
WHITE = (245, 245, 245)
GRAY = (170, 170, 170)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

canvas = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(canvas)

# Right side: generated robot illustration
robot = Image.open(f"{OUT}/hasil-2-robot.jpg").convert("RGB")
robot = robot.resize((980, 980), Image.LANCZOS)
canvas.paste(robot, (1000, 86))
draw.rectangle([1000, 86, 1980, 1066], outline=YELLOW, width=6)

# Left side text
x = 90
draw.rectangle([x, 150, x + 420, 168], fill=YELLOW)
f_label = ImageFont.truetype(BOLD, 58)
draw.text((x, 200), "COBA DULU #03", font=f_label, fill=YELLOW)

f_title = ImageFont.truetype(BOLD, 132)
title_lines = ["Ketik Satu", "Kalimat,", "Jadi Ilustrasi."]
# auto-fit: shrink until the widest line fits the left column (x=90..990)
while max(draw.textlength(ln, font=f_title) for ln in title_lines) > 890 and f_title.size > 60:
    f_title = ImageFont.truetype(BOLD, f_title.size - 4)
y = 320
for ln in title_lines:
    draw.text((x, y), ln, font=f_title, fill=YELLOW if ln.startswith("Jadi") else WHITE)
    y += int(f_title.size * 1.08)

f_sub = ImageFont.truetype(REG, 56)
draw.text((x, 800), "Pollinations, gratis", font=f_sub, fill=GRAY)
draw.text((x, 870), "tanpa daftar.", font=f_sub, fill=GRAY)

f_small = ImageFont.truetype(REG, 40)
draw.text((x, 1040), "Gabung komunitas: s.peka.ai.id/gabung", font=f_small, fill=GRAY)

canvas.save(f"{OUT}/cover.jpg", quality=92)
canvas.save(IMG, quality=92)
print("saved", f"{OUT}/cover.jpg", "and", IMG)
print("size", canvas.size)
