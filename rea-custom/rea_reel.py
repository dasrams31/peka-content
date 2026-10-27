#!/usr/bin/env python3
"""Custom reel for REA, matching the REA slides: dark terminal,
neon green + amber, falling hex columns, scanline, typing terminal.
15 s, 24 fps, 1080x1920, scaled to 1440x2560 by ffmpeg.
Music (separate pick, one per reel): Oppressive Gloom by Kevin MacLeod.
Scenes: cover 3 s, how 4 s, what+proof 4 s, question 2 s, follow 2 s.
"""
import os, math, random
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "frames")
os.makedirs(OUT, exist_ok=True)
W, H, FPS = 1080, 1920, 24
BG = (10, 15, 10)
GREEN = (51, 255, 153)
AMBER = (255, 176, 0)
CREAM = (242, 239, 230)
MUTED = (150, 160, 150)
POPPINS = "/home/hatch/workspace/sertiku-poster/fonts"
DEJAVU = "/usr/share/fonts/truetype/dejavu"


def F(name, size):
    return ImageFont.truetype(os.path.join(POPPINS, name), size)


def mono(size):
    return ImageFont.truetype(os.path.join(DEJAVU, "DejaVuSansMono-Bold.ttf"), size)


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


random.seed(7)
COLS = []
for i in range(14):
    COLS.append((40 + i * 74, random.uniform(0, 400), random.uniform(40, 90),
                 "".join(random.choice("0123456789abcdef") for _ in range(40))))


def hex_rain(img, t):
    d = ImageDraw.Draw(img)
    for x, y0, speed, s in COLS:
        y = (y0 + speed * t) % (H + 400) - 200
        for j, ch in enumerate(s[:12]):
            d.text((x, y + j * 36), ch, font=mono(24), fill=(22, 50, 30))


def text_in(d, xy, txt, font, fill, t, delay, dur=0.6):
    a = ease((t - delay) / dur)
    off = int((1 - a) * 70)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(ov).text((xy[0], xy[1] + off), txt, font=font, fill=fill + (int(a * 255),))
    return ov


def scene(t):
    img = Image.new("RGBA", (W, H), BG + (255,))
    hex_rain(img, t)
    d = ImageDraw.Draw(img)
    d.text((80, 110), "REPO OF THE DAY", font=mono(30), fill=GREEN + (255,))
    _lk = Image.open(os.path.join(BASE, "peka-lockup-white-text.png")).convert("RGBA")
    _lh = 64
    _lw = int(_lk.width * _lh / _lk.height)
    _lk = _lk.resize((_lw, _lh), Image.LANCZOS)
    img.paste(_lk, (W - 80 - _lw, 82), _lk)
    if t < 3:
        st = t
        for ov in [text_in(d, (80, 500), "Lihat fitur yang", F("Poppins-ExtraBold.ttf", 88), CREAM, st, 0.2),
                   text_in(d, (80, 610), "kamu suka.", F("Poppins-ExtraBold.ttf", 88), CREAM, st, 0.4),
                   text_in(d, (80, 720), "Bongkar cara kerjanya.", F("Poppins-ExtraBold.ttf", 72), GREEN, st, 0.6)]:
            img.alpha_composite(ov)
        d = ImageDraw.Draw(img)
        d.rounded_rectangle([80, 900, 1000, 1180], radius=24, fill=(18, 28, 18, 255))
        d.text((110, 940), "$ npm install --global rea-agents", font=mono(32), fill=GREEN + (255,))
        d.text((110, 1000), "$ rea --help", font=mono(32), fill=CREAM + (255,))
        d.text((110, 1080), "Ini REA. Tanpa kode sumbernya.", font=F("Poppins-SemiBold.ttf", 34), fill=MUTED + (255,))
        d.text((80, 1260), "Disukai 396 ribu orang  •  Gratis", font=F("Poppins-Bold.ttf", 36), fill=AMBER + (255,))
    elif t < 7:
        st = t - 3
        d.text((80, 400), "Gimana cara", font=F("Poppins-ExtraBold.ttf", 88), fill=CREAM + (255,))
        d.text((80, 510), "kerjanya?", font=F("Poppins-ExtraBold.ttf", 88), fill=GREEN + (255,))
        steps = [("01", "Tanya agent kamu", "Gimana cara kerja search di Notes?"),
                 ("02", "REA bongkar targetnya", "Sampai ke kode paling dalam."),
                 ("03", "Kamu dapat bukti", "Lalu bisa ditiru buat project kamu.")]
        y = 680
        for i, (num, title, body) in enumerate(steps):
            for ov in [text_in(d, (80, y), num, F("Poppins-ExtraBold.ttf", 64), GREEN, st, 0.2 + i * 0.7),
                       text_in(d, (220, y), title, F("Poppins-Bold.ttf", 48), CREAM, st, 0.2 + i * 0.7),
                       text_in(d, (220, y + 70), body, F("Poppins-SemiBold.ttf", 34), MUTED, st, 0.3 + i * 0.7)]:
                img.alpha_composite(ov)
            y += 210
    elif t < 11:
        st = t - 7
        d.text((80, 400), "Apa yang bisa", font=F("Poppins-ExtraBold.ttf", 88), fill=CREAM + (255,))
        d.text((80, 510), "dibongkar?", font=F("Poppins-ExtraBold.ttf", 88), fill=GREEN + (255,))
        items = ["Aplikasi desktop", "File biner", "App JS / Electron",
                 "APK Android", "Website", ".NET, dan banyak lagi"]
        y = 660
        for i, it in enumerate(items):
            ov = text_in(d, (80, y), "›  " + it, F("Poppins-Bold.ttf", 48), CREAM, st, 0.2 + i * 0.4)
            img.alpha_composite(ov)
            y += 100
        d = ImageDraw.Draw(img)
        d.rounded_rectangle([80, 1320, 1000, 1560], radius=24, fill=(18, 28, 18, 255))
        d.text((110, 1360), "Contoh nyata: DX-Ball,", font=F("Poppins-Bold.ttf", 36), fill=CREAM + (255,))
        d.text((110, 1420), "lolos 3.205 kasus asli.", font=F("Poppins-Bold.ttf", 36), fill=AMBER + (255,))
    elif t < 13:
        st = t - 11
        for ov in [text_in(d, (80, 700), "Fitur app apa", F("Poppins-ExtraBold.ttf", 88), CREAM, st, 0.1),
                   text_in(d, (80, 810), "yang pengin kamu", F("Poppins-ExtraBold.ttf", 88), CREAM, st, 0.3),
                   text_in(d, (80, 920), "bongkar?", F("Poppins-ExtraBold.ttf", 88), GREEN, st, 0.5)]:
            img.alpha_composite(ov)
        d = ImageDraw.Draw(img)
        d.text((80, 1060), "Coba komen ya.", font=F("Poppins-SemiBold.ttf", 40), fill=MUTED + (255,))
    else:
        st = t - 13
        for ov in [text_in(d, (80, 700), "Follow,", F("Poppins-ExtraBold.ttf", 100), CREAM, st, 0.1),
                   text_in(d, (80, 820), "kalau kamu suka.", F("Poppins-ExtraBold.ttf", 84), GREEN, st, 0.4)]:
            img.alpha_composite(ov)
        d = ImageDraw.Draw(img)
        d.text((80, 990), "Follow @peka.ai.id, kalau kontennya kepakai.",
               font=F("Poppins-SemiBold.ttf", 34), fill=CREAM + (255,))
        d.text((80, 1050), "Grup WA: url.peka.ai.id, kalau mau ngobrol.",
               font=F("Poppins-SemiBold.ttf", 34), fill=CREAM + (255,))
        d.text((80, 1110), "Save dulu, biar gampang dicari lagi.",
               font=F("Poppins-SemiBold.ttf", 34), fill=CREAM + (255,))
    d = ImageDraw.Draw(img)
    # Scanline.
    sy = int((t * 220) % (H + 100) - 50)
    d.line([(0, sy), (W, sy)], fill=GREEN + (60,), width=3)
    d.rectangle([0, H - 60, W, H], fill=BG + (255,))
    d.text((80, H - 48), "GABUNG KE KOMUNITAS KAMI: URL.PEKA.AI.ID",
           font=F("Poppins-Bold.ttf", 22), fill=MUTED + (255,))
    return img.convert("RGB")


def main():
    for i in range(15 * FPS):
        scene(i / FPS).save(os.path.join(OUT, f"f{i:04d}.png"))
        if i % 60 == 0:
            print("frame", i)
    print("done", 15 * FPS)


if __name__ == "__main__":
    main()
