#!/usr/bin/env python3
"""Custom slides for REA (morluto/rea), Repo of the Day edition.

Design represents REA itself, not a generic template: dark terminal /
decompiler look, neon green + amber, faint hex dump, assembly-style
panels. Copy is lay + soft (2026-10-28 rule). No Hopper screenshot
(user correction for ROTW slide 2); code panels are generic
illustrations, not claimed REA screenshots.
Facts verified 2026-10-28 from GitHub API + README:
stars 396,515, forks 99,421, MIT, install
`npm install --global rea-agents`, setup `npx rea-agents setup`,
DX-Ball showcase: 3,205 original-x86 cases, 63 function bytes.
"""
import os, random
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
W = H = 2048
MX = 140
BG = (10, 15, 10)
PANEL = (18, 28, 18)
GREEN = (51, 255, 153)
AMBER = (255, 176, 0)
CREAM = (242, 239, 230)
MUTED = (150, 160, 150)
HAIR = (40, 55, 40)
POPPINS = "/home/hatch/workspace/sertiku-poster/fonts"
DEJAVU = "/usr/share/fonts/truetype/dejavu"


def F(name, size):
    return ImageFont.truetype(os.path.join(POPPINS, name), size)


def mono(size):
    return ImageFont.truetype(os.path.join(DEJAVU, "DejaVuSansMono-Bold.ttf"), size)


def base(page):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # Faint hex dump background, deterministic.
    rnd = random.Random(42)
    hx = "0123456789abcdef"
    for y in range(120, H - 200, 52):
        line = " ".join("".join(rnd.choice(hx) for _ in range(2)) for _ in range(18))
        d.text((MX, y), line, font=mono(24), fill=(22, 38, 22))
    d.rectangle([0, 0, W, H], outline=None)
    # Top bar over hex.
    d.rectangle([0, 0, W, 220], fill=BG)
    d.text((MX, 110), "REPO OF THE DAY", font=mono(34), fill=GREEN)
    d.text((W - MX - d.textlength("peka.ai.id", font=F("Poppins-Bold.ttf", 40)), 110),
           "peka.ai.id", font=F("Poppins-Bold.ttf", 40), fill=CREAM)
    d.line([(MX, H - 180), (W - MX, H - 180)], fill=HAIR, width=2)
    d.text((MX, H - 140), "GABUNG KE KOMUNITAS KAMI: URL.PEKA.AI.ID",
           font=mono(30), fill=MUTED)
    d.text((W - MX - d.textlength(f"{page:02d} / 04", font=mono(30)), H - 140),
           f"{page:02d} / 04", font=mono(30), fill=MUTED)
    return img, d


def panel(img, d, x, y, w, h, title, lines):
    d.rounded_rectangle([x, y, x + w, y + h], radius=28, fill=PANEL, outline=HAIR, width=2)
    d.ellipse([x + 36, y + 28, x + 60, y + 52], fill=(255, 95, 87))
    d.ellipse([x + 76, y + 28, x + 100, y + 52], fill=(254, 188, 46))
    d.ellipse([x + 116, y + 28, x + 140, y + 52], fill=(40, 200, 64))
    d.text((x + 170, y + 24), title, font=mono(30), fill=MUTED)
    ly = y + 90
    for text, color in lines:
        d.text((x + 40, ly), text, font=mono(36), fill=color)
        ly += 58


def cover():
    img, d = base(1)
    d.text((MX, 300), "Lihat fitur yang", font=F("Poppins-ExtraBold.ttf", 110), fill=CREAM)
    d.text((MX, 430), "kamu suka.", font=F("Poppins-ExtraBold.ttf", 110), fill=CREAM)
    d.text((MX, 560), "Bongkar cara kerjanya.", font=F("Poppins-ExtraBold.ttf", 110), fill=GREEN)
    d.text((MX, 710), "Ini REA. Bongkar aplikasi apa pun, tanpa kode sumbernya.",
           font=F("Poppins-SemiBold.ttf", 38), fill=MUTED)
    panel(img, d, MX, 820, W - 2 * MX, 620, "terminal", [
        ("$ npm install --global rea-agents", GREEN),
        ("$ rea --help", CREAM),
        ("# tanya agent: gimana cara kerja", MUTED),
        ("# fitur search di Notes?", MUTED),
        ("-> REA bongkar, kasih bukti,", GREEN),
        ("-> lalu bantu tiru buat project kamu.", GREEN),
    ])
    d.text((MX, 1500), "Disukai 396 ribu orang  •  Gratis",
           font=F("Poppins-Bold.ttf", 38), fill=AMBER)
    d.text((MX, 1560), "morluto/rea  •  Reverse Engineer Anything",
           font=mono(32), fill=MUTED)
    return img


def how():
    img, d = base(2)
    d.text((MX, 300), "Gimana cara", font=F("Poppins-ExtraBold.ttf", 110), fill=CREAM)
    d.text((MX, 430), "kerjanya?", font=F("Poppins-ExtraBold.ttf", 110), fill=GREEN)
    steps = [("01", "Tanya agent kamu", "Contoh: gimana cara kerja search di Notes?"),
             ("02", "REA bongkar targetnya", "Tanpa kode sumber, sampai ke kode paling dalam."),
             ("03", "Kamu dapat bukti + penjelasan", "Lalu bisa ditiru buat project kamu sendiri.")]
    y = 620
    for num, title, body in steps:
        d.text((MX, y), num, font=F("Poppins-ExtraBold.ttf", 64), fill=GREEN)
        d.text((MX + 170, y), title, font=F("Poppins-Bold.ttf", 52), fill=CREAM)
        d.text((MX + 170, y + 80), body, font=F("Poppins-SemiBold.ttf", 36), fill=MUTED)
        y += 210
    panel(img, d, MX, 1280, W - 2 * MX, 380, "contoh nyata", [
        ("DX-Ball: hitungan suara game lama,", CREAM),
        ("dibangun ulang, lolos 3.205 kasus asli.", AMBER),
    ])
    return img


def what():
    img, d = base(3)
    d.text((MX, 300), "Apa yang bisa", font=F("Poppins-ExtraBold.ttf", 110), fill=CREAM)
    d.text((MX, 430), "dibongkar?", font=F("Poppins-ExtraBold.ttf", 110), fill=GREEN)
    items = ["Aplikasi desktop", "File biner", "App JS / Electron",
             "APK Android", "Website", ".NET, dan banyak lagi"]
    y = 620
    for it in items:
        d.text((MX, y), "›", font=F("Poppins-ExtraBold.ttf", 56), fill=GREEN)
        d.text((MX + 80, y), it, font=F("Poppins-Bold.ttf", 52), fill=CREAM)
        y += 110
    panel(img, d, MX, 1340, W - 2 * MX, 380, "catatan", [
        ("Analisis jalan lokal, di komputermu sendiri.", GREEN),
        ("Cara pasang: npx rea-agents setup", CREAM),
    ])
    return img


def follow():
    img, d = base(4)
    d.text((MX, 300), "Follow,", font=F("Poppins-ExtraBold.ttf", 130), fill=CREAM)
    d.text((MX, 450), "kalau kamu suka.", font=F("Poppins-ExtraBold.ttf", 110), fill=GREEN)
    y = 680
    for line in ["Follow @peka.ai.id, kalau kontennya kepakai.",
                 "Grup WA: url.peka.ai.id, kalau mau ngobrol.",
                 "Save dulu, biar gampang dicari lagi.",
                 "Link-nya ada di komentar."]:
        d.text((MX, y), line, font=F("Poppins-SemiBold.ttf", 44), fill=CREAM)
        y += 90
    return img


def main():
    for i, fn in enumerate([cover, how, what, follow], start=1):
        fn().save(os.path.join(BASE, f"rea-slide-{i:02d}.png"))
        print("saved", i)


if __name__ == "__main__":
    main()
