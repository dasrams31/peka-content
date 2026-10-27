#!/usr/bin/env python3
"""Japanese-style animated reel for Huashu Design (IG + FB, same file).

Style: washi cream paper, vermilion rising sun, indigo Great-Wave
lines at the bottom, falling sakura petals in every scene, vertical
Japanese accent text. Copy is the short revised showcase copy.
15 s at 24 fps, rendered 1080x1920, scaled to 1440x2560 by ffmpeg.
Scenes: cover 3 s, proof 4 s, how 4 s, question 2 s, follow 2 s.
"""
import os, math, random
from PIL import Image, ImageDraw, ImageFont, ImageOps

BASE = os.path.dirname(os.path.abspath(__file__))
SHOW = os.path.join(BASE, "showcase")
OUT = os.path.join(BASE, "frames_jp")
os.makedirs(OUT, exist_ok=True)

W, H, FPS = 1080, 1920, 24
CREAM = (246, 241, 230)
INK = (17, 17, 17)
RED = (193, 39, 45)
INDIGO = (31, 58, 95)
MUTED = (110, 105, 95)
POPPINS = "/home/hatch/workspace/sertiku-poster/fonts"
CJK = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"


def F(name, size):
    return ImageFont.truetype(os.path.join(POPPINS, name), size)


def JP(size):
    try:
        return ImageFont.truetype(CJK, size, index=2)
    except Exception:
        return ImageFont.truetype(CJK, size)


def fit(path, w, h, radius=28):
    im = Image.open(path).convert("RGB")
    im = ImageOps.fit(im, (w, h), Image.LANCZOS)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, fill=255)
    im.putalpha(mask)
    return im


HOKUSAI = fit(os.path.join(SHOW, "case-hokusai-hero.jpg"), 920, 560)
MINGJI = fit(os.path.join(SHOW, "case-mingji-birding-app.jpg"), 920, 480)

# Sakura petals: x0, speed, sway phase, size, shade
random.seed(28)
PETALS = []
for _ in range(26):
    PETALS.append((random.uniform(0, W), random.uniform(60, 220),
                   random.uniform(0, 6.28), random.uniform(26, 44),
                   random.choice([(248, 187, 208), (244, 143, 177), (255, 205, 210)])))
PETAL_BASE = {}
for shade in set(p[4] for p in PETALS):
    s = max(p[3] for p in PETALS if p[4] == shade)
    im = Image.new("RGBA", (int(s), int(s * 0.65)), (0, 0, 0, 0))
    ImageDraw.Draw(im).ellipse([0, 0, int(s) - 1, int(s * 0.65) - 1], fill=shade + (255,))
    PETAL_BASE[shade] = im


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def wave(d, t, ybase, amp, color, phase):
    pts = []
    for x in range(0, W + 21, 20):
        y = ybase + math.sin((x / W) * 2 * math.pi * 2 + phase + t * 0.9) * amp
        pts.append((x, y))
    pts += [(W, H), (0, H)]
    d.polygon(pts, fill=color)


def petals(img, t):
    for x0, speed, ph, size, shade in PETALS:
        y = (speed * t * 10 + ph * 90) % (H + 120) - 60
        x = x0 + math.sin(t * 0.7 + ph) * 45
        base = PETAL_BASE[shade]
        rot = base.rotate(int((t * 50 + ph * 80) % 360), expand=True, resample=Image.BICUBIC)
        sc = size / base.size[0]
        rot = rot.resize((max(8, int(rot.size[0] * sc)), max(6, int(rot.size[1] * sc))))
        img.paste(rot, (int(x), int(y)), rot)


def text_in(d, xy, txt, font, fill, t, delay, dur=0.6):
    a = ease((t - delay) / dur)
    off = int((1 - a) * 70)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    od.text((xy[0], xy[1] + off), txt, font=font, fill=fill + (int(a * 255),))
    return ov


def scene(t):
    img = Image.new("RGBA", (W, H), CREAM + (255,))
    d = ImageDraw.Draw(img)
    # Rising sun, top right (cover) / small corner (others)
    if t < 3:
        sy = 420 - ease(t / 3) * 110
        d.ellipse([720, sy, 970, sy + 250], fill=RED + (255,))
    else:
        d.ellipse([880, 120, 1000, 240], fill=RED + (255,))
    # Vertical Japanese accent on the right edge.
    jp = JP(44)
    for i, ch in enumerate("一言でデザイン"):
        d.text((W - 90, 320 + i * 62), ch, font=jp, fill=INDIGO + (255,))
    d.text((80, 110), "peka.ai.id", font=F("Poppins-Bold.ttf", 40), fill=INK + (255,))

    if t < 3:
        st = t
        for ov in [text_in(d, (80, 620), "Ketik satu kalimat,", F("Poppins-ExtraBold.ttf", 80), INK, st, 0.2),
                   text_in(d, (80, 730), "jadi desain.", F("Poppins-ExtraBold.ttf", 80), RED, st, 0.5)]:
            img.alpha_composite(ov)
        d = ImageDraw.Draw(img)
        d.text((80, 860), "Ini Huashu Design. Kamu ketik, dia yang gambar.",
               font=F("Poppins-SemiBold.ttf", 40), fill=MUTED + (255,))
        hero = HOKUSAI.copy()
        img.paste(hero, (80, 990), hero)
        d = ImageDraw.Draw(img)
        d.text((80, 1600), "Contoh: web pameran Hokusai.",
               font=F("Poppins-SemiBold.ttf", 36), fill=INK + (255,))
        d.text((80, 1660), "Disukai 27 ribu orang  •  Gratis",
               font=F("Poppins-Bold.ttf", 36), fill=RED + (255,))
    elif t < 7:
        st = t - 3
        for ov in [text_in(d, (80, 300), "Ini contoh", F("Poppins-ExtraBold.ttf", 96), INK, st, 0.1),
                   text_in(d, (80, 420), "hasil aslinya.", F("Poppins-ExtraBold.ttf", 96), RED, st, 0.4)]:
            img.alpha_composite(ov)
        d = ImageDraw.Draw(img)
        d.text((80, 560), "Bukan gambar tempelan, ini beneran jadi.",
               font=F("Poppins-SemiBold.ttf", 38), fill=MUTED + (255,))
        d.text((80, 600), "Web Hokusai, atas. App Mingji, bawah.",
               font=F("Poppins-Bold.ttf", 34), fill=INK + (255,))
        for im, y in [(HOKUSAI, 650), (MINGJI, 1260)]:
            img.paste(im, (80, y), im)
    elif t < 11:
        st = t - 7
        d.text((80, 300), "Dari 6 pilihan,", font=F("Poppins-ExtraBold.ttf", 96), fill=INK + (255,))
        d.text((80, 420), "jadi 3.", font=F("Poppins-ExtraBold.ttf", 96), fill=RED + (255,))
        steps = [("01", "Ketik yang kamu mau", "Web, App, PPT, animasi. Nggak perlu Figma."),
                 ("02", "Dibuatkan 6 contoh dulu", "3 yang paling beda, dibuat sampai jadi."),
                 ("03", "Tinggal pilih yang kamu suka", "Ada 84 gaya, bisa disesuaikan sama gayamu.")]
        y = 620
        for i, (num, title, body) in enumerate(steps):
            ov = text_in(d, (80, y), num, F("Poppins-ExtraBold.ttf", 72), RED, st, 0.2 + i * 0.7)
            ov2 = text_in(d, (220, y), title, F("Poppins-Bold.ttf", 56), INK, st, 0.2 + i * 0.7)
            ov3 = text_in(d, (220, y + 80), body, F("Poppins-SemiBold.ttf", 38), MUTED, st, 0.3 + i * 0.7)
            for o in (ov, ov2, ov3):
                img.alpha_composite(o)
            y += 230
        d = ImageDraw.Draw(img)
        d.text((80, 1360), "Cara pasang: npx skills add alchaincyf/huashu-design",
               font=F("Poppins-Bold.ttf", 34), fill=INDIGO + (255,))
        d.text((80, 1440), "Buat deck, landing page, dan contoh App.",
               font=F("Poppins-Bold.ttf", 38), fill=INK + (255,))
        d.text((80, 1500), "Nggak perlu tim desain.",
               font=F("Poppins-Bold.ttf", 38), fill=INK + (255,))
    elif t < 13:
        st = t - 11
        for ov in [text_in(d, (80, 700), "Kamu pengin", F("Poppins-ExtraBold.ttf", 96), INK, st, 0.1),
                   text_in(d, (80, 820), "bikin apa dulu?", F("Poppins-ExtraBold.ttf", 96), RED, st, 0.4)]:
            img.alpha_composite(ov)
        d = ImageDraw.Draw(img)
        d.text((80, 980), "Web, App, atau PPT? Coba komen ya.",
               font=F("Poppins-SemiBold.ttf", 44), fill=MUTED + (255,))
    else:
        st = t - 13
        for ov in [text_in(d, (80, 700), "Follow,", F("Poppins-ExtraBold.ttf", 110), INK, st, 0.1),
                   text_in(d, (80, 830), "kalau kamu suka.", F("Poppins-ExtraBold.ttf", 90), RED, st, 0.4)]:
            img.alpha_composite(ov)
        d = ImageDraw.Draw(img)
        d.text((80, 1010), "Follow @peka.ai.id, kalau kontennya kepakai.",
               font=F("Poppins-SemiBold.ttf", 36), fill=INK + (255,))
        d.text((80, 1080), "Grup WA: url.peka.ai.id, kalau mau ngobrol.",
               font=F("Poppins-SemiBold.ttf", 36), fill=INK + (255,))
        d.text((80, 1150), "Save dulu, biar gampang dicari lagi.",
               font=F("Poppins-SemiBold.ttf", 36), fill=INK + (255,))
    # Waves at the bottom, petals on top.
    d = ImageDraw.Draw(img)
    wave(d, t, H - 150, 26, INDIGO + (90,), 0)
    wave(d, t, H - 90, 20, INDIGO + (140,), 2)
    petals(img, t)
    d = ImageDraw.Draw(img)
    d.rectangle([0, H - 60, W, H], fill=CREAM + (255,))
    d.text((80, H - 48), "GABUNG KE KOMUNITAS KAMI: URL.PEKA.AI.ID",
           font=F("Poppins-Bold.ttf", 22), fill=MUTED + (255,))
    return img.convert("RGB")


def main():
    total = 15 * FPS
    for i in range(total):
        scene(i / FPS).save(os.path.join(OUT, f"f{i:04d}.png"))
        if i % 60 == 0:
            print("frame", i)
    print("done", total)


if __name__ == "__main__":
    main()
