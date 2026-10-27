#!/usr/bin/env python3
"""Japanese-style carousel slides for Huashu Design, matching the JP reel.

Washi cream, vermilion sun, indigo waves, falling sakura petals,
vertical Japanese accent. Short revised copy only. 2048x2048.
"""
import os, math, random
from PIL import Image, ImageDraw, ImageFont, ImageOps

BASE = os.path.dirname(os.path.abspath(__file__))
SHOW = os.path.join(BASE, "showcase")
W = H = 2048
MX = 140
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


def fit(path, w, h, radius=36):
    im = Image.open(path).convert("RGB")
    im = ImageOps.fit(im, (w, h), Image.LANCZOS)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, fill=255)
    im.putalpha(mask)
    return im


random.seed(28)
PETALS = [(random.uniform(0, W), random.uniform(0, H), random.uniform(0, 6.28),
           random.uniform(48, 80), random.choice([(248, 187, 208), (244, 143, 177)]))
          for _ in range(36)]


def base(page):
    img = Image.new("RGBA", (W, H), CREAM + (255,))
    d = ImageDraw.Draw(img)
    d.ellipse([1720, 130, 1900, 310], fill=RED + (255,))
    jp = JP(72)
    for i, ch in enumerate("一言でデザイン"):
        d.text((W - 110, 420 + i * 100), ch, font=jp, fill=INDIGO + (255,))
    d.text((MX, 120), "peka.ai.id", font=F("Poppins-Bold.ttf", 40), fill=INK + (255,))
    # Sakura petals.
    for x, y, ph, size, shade in PETALS:
        px = x + math.sin(ph) * 30
        pet = Image.new("RGBA", (int(size), int(size * 0.65)), (0, 0, 0, 0))
        ImageDraw.Draw(pet).ellipse([0, 0, int(size) - 1, int(size * 0.65) - 1], fill=shade + (210,))
        pet = pet.rotate(int(ph * 60) % 360, expand=True, resample=Image.BICUBIC)
        img.paste(pet, (int(px), int(y)), pet)
    d = ImageDraw.Draw(img)
    # Indigo waves above the footer strip.
    for ybase, amp, alpha, phase in [(H - 280, 34, 90, 0), (H - 200, 26, 140, 2)]:
        pts = [(x, ybase + math.sin((x / W) * 4 * math.pi + phase) * amp)
               for x in range(0, W + 21, 20)]
        pts += [(W, H), (0, H)]
        d.polygon(pts, fill=INDIGO + (alpha,))
    d.rectangle([0, H - 120, W, H], fill=CREAM + (255,))
    d.text((MX, H - 90), "GABUNG KE KOMUNITAS KAMI: URL.PEKA.AI.ID",
           font=F("Poppins-Bold.ttf", 28), fill=MUTED + (255,))
    d.text((W - MX - d.textlength(f"{page:02d} / 04", font=F("Poppins-Bold.ttf", 28)), H - 90),
           f"{page:02d} / 04", font=F("Poppins-Bold.ttf", 28), fill=MUTED + (255,))
    return img, d


def cover():
    img, d = base(1)
    d.text((MX, 300), "Ketik satu kalimat,", font=F("Poppins-ExtraBold.ttf", 110), fill=INK + (255,))
    d.text((MX, 430), "jadi desain.", font=F("Poppins-ExtraBold.ttf", 110), fill=RED + (255,))
    d.text((MX, 600), "Ini Huashu Design. Kamu ketik, dia yang gambar.",
           font=F("Poppins-SemiBold.ttf", 44), fill=MUTED + (255,))
    hero = fit(os.path.join(SHOW, "case-hokusai-hero.jpg"), W - 2 * MX, 860)
    img.paste(hero, (MX, 720), hero)
    d = ImageDraw.Draw(img)
    d.text((MX, 1630), "Contoh: web pameran Hokusai.",
           font=F("Poppins-SemiBold.ttf", 38), fill=INK + (255,))
    d.text((MX, 1690), "Disukai 27 ribu orang  •  Gratis",
           font=F("Poppins-Bold.ttf", 38), fill=RED + (255,))
    return img.convert("RGB")


def proof():
    img, d = base(2)
    d.text((MX, 300), "Ini contoh", font=F("Poppins-ExtraBold.ttf", 110), fill=INK + (255,))
    d.text((MX, 430), "hasil aslinya.", font=F("Poppins-ExtraBold.ttf", 110), fill=RED + (255,))
    d.text((MX, 580), "Bukan gambar tempelan, ini beneran jadi.",
           font=F("Poppins-SemiBold.ttf", 38), fill=MUTED + (255,))
    bw = (W - 2 * MX - 40) // 2
    left = fit(os.path.join(SHOW, "case-mingji-birding-app.jpg"), bw, 980)
    right = fit(os.path.join(SHOW, "case-qianli-cover.jpg"), bw, 980)
    img.paste(left, (MX, 680), left)
    img.paste(right, (MX + bw + 40, 680), right)
    d = ImageDraw.Draw(img)
    d.text((MX, 1690), "App Mingji, bisa dicoba",
           font=F("Poppins-Bold.ttf", 36), fill=INK + (255,))
    d.text((MX + bw + 40, 1690), "PPT Qianli, bisa diubah",
           font=F("Poppins-Bold.ttf", 36), fill=INK + (255,))
    return img.convert("RGB")


def how():
    img, d = base(3)
    d.text((MX, 300), "Dari 6 pilihan,", font=F("Poppins-ExtraBold.ttf", 110), fill=INK + (255,))
    d.text((MX, 430), "jadi 3.", font=F("Poppins-ExtraBold.ttf", 110), fill=RED + (255,))
    steps = [("01", "Ketik yang kamu mau", "Web, App, PPT, animasi. Nggak perlu Figma."),
             ("02", "Dibuatkan 6 contoh dulu", "3 yang paling beda, dibuat sampai jadi."),
             ("03", "Tinggal pilih yang kamu suka", "Ada 84 gaya, bisa disesuaikan sama gayamu.")]
    y = 620
    for num, title, body in steps:
        d.text((MX, y), num, font=F("Poppins-ExtraBold.ttf", 64), fill=RED + (255,))
        d.text((MX + 170, y), title, font=F("Poppins-Bold.ttf", 52), fill=INK + (255,))
        d.text((MX + 170, y + 80), body, font=F("Poppins-SemiBold.ttf", 38), fill=MUTED + (255,))
        y += 230
    d.text((MX, 1360), "Cara pasang: npx skills add alchaincyf/huashu-design",
           font=F("Poppins-Bold.ttf", 40), fill=INDIGO + (255,))
    d.text((MX, 1450), "Buat deck, landing page, dan contoh App.",
           font=F("Poppins-Bold.ttf", 40), fill=INK + (255,))
    d.text((MX, 1510), "Nggak perlu tim desain.",
           font=F("Poppins-Bold.ttf", 40), fill=INK + (255,))
    return img.convert("RGB")


def follow():
    img, d = base(4)
    d.text((MX, 300), "Follow,", font=F("Poppins-ExtraBold.ttf", 130), fill=INK + (255,))
    d.text((MX, 450), "kalau kamu suka.", font=F("Poppins-ExtraBold.ttf", 110), fill=RED + (255,))
    y = 680
    for line in ["Follow @peka.ai.id, kalau kontennya kepakai.",
                 "Grup WA: url.peka.ai.id, kalau mau ngobrol.",
                 "Save dulu, biar gampang dicari lagi.",
                 "Link-nya ada di komentar."]:
        d.text((MX, y), line, font=F("Poppins-SemiBold.ttf", 46), fill=INK + (255,))
        y += 90
    return img.convert("RGB")


def main():
    for i, fn in enumerate([cover, proof, how, follow], start=1):
        fn().save(os.path.join(BASE, f"slide-jp-{i:02d}.png"))
        print("saved", i)


if __name__ == "__main__":
    main()
