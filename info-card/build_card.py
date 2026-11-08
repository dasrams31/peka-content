#!/usr/bin/env python3
"""Info card v2: Peka content status, 8 Nov 2026, 20:00 WIB."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1480
BG = (17, 17, 17)
YEL = (255, 214, 10)
WHITE = (241, 245, 249)
GREY = (148, 163, 184)
GREEN = (16, 185, 129)
CARD = (20, 23, 33)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

d.rectangle([0, 0, W, 12], fill=YEL)

d.text((70, 60), "KONTEN PEKA", font=font(FB, 72), fill=YEL)
d.text((70, 150), "8 November 2026 - 20:00", font=font(FR, 36), fill=GREY)
d.line([(70, 215), (W - 70, 215)], fill=(60, 60, 60), width=2)

def section(y, label):
    d.text((70, y), label, font=font(FB, 40), fill=YEL)
    return y + 70

def row(y, title, detail, mark, mark_color):
    d.rounded_rectangle([70, y, W - 70, y + 100], radius=18, fill=CARD)
    d.ellipse([95, y + 30, 135, y + 70], fill=mark_color)
    if mark == "check":
        d.line([(104, y + 50), (113, y + 59), (128, y + 41)], fill=(17, 17, 17), width=5, joint="curve")
    else:
        d.text((115, y + 34), mark, font=font(FB, 26), fill=(17, 17, 17), anchor="mm")
    d.text((160, y + 14), title, font=font(FB, 34), fill=WHITE)
    d.text((160, y + 58), detail, font=font(FR, 26), fill=GREY)
    return y + 116

y = section(245, "SUDAH TAYANG")
y = row(y, "Kabar Harian", "iPhone storage penuh - IG, FB, Blog", "check", GREEN)
y = row(y, "Prompt Harian #18", "Skrip Reels 30 detik - IG, Threads, FB, Blog", "check", GREEN)
y = row(y, "SertiKu", "Reels jejak sertifikat - siap, posting manual", "check", GREEN)
y = row(y, "Aeternum", "Carousel FAQ website - siap, posting manual", "check", GREEN)
y = row(y, "Review Mingguan 20:00", "BUNUH Pancingan, LANJUT Gratisan + Prompt, ROMBAK HM", "check", GREEN)

y = section(y + 10, "MALAM INI")
y = row(y, "SPILL #19 - HERMES", "21:30 - 5 repo fresh", "\u25b6", YEL)
y = row(y, "Laporan Harian", "22:30 - rekap semua edisi hari ini", "\u25b6", YEL)

d.line([(70, 1270), (W - 70, 1270)], fill=(60, 60, 60), width=2)
d.text((70, 1295), "3 rekomendasi review sudah aktif otomatis di cron.", font=font(FR, 28), fill=GREY)
d.text((70, 1350), "peka.ai.id", font=font(FB, 30), fill=YEL)

out = "/home/hatch/workspace/peka-content/info-card/info-card-2026-11-08-2000.png"
img.save(out)
print("saved", out)
