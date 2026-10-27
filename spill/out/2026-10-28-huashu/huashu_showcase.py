#!/usr/bin/env python3
"""Special showcase carousel for Huashu Design (NOT the SPILL template).

Dark Peka style: charcoal background, yellow accent, cream text.
Showcase images are Huashu's own v3.0 case images from its GitHub
releases, used to demonstrate the repo's output, not as our own work.
Slides: 01 cover + hero, 02 proof (App + PPT), 03 how to use,
04 follow + community.
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

BASE = os.path.dirname(os.path.abspath(__file__))
SHOW = os.path.join(BASE, "showcase")
POPPINS = "/home/hatch/workspace/sertiku-poster/fonts"
DEJAVU = "/usr/share/fonts/truetype/dejavu"

BG = (17, 17, 17)
SURF = (27, 27, 30)
YEL = (255, 214, 10)
CREAM = (242, 239, 230)
MUTED = (154, 149, 138)
HAIR = (60, 60, 64)
W = H = 2048
MX = 140


def font(name, size):
    path = os.path.join(POPPINS, name)
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype(os.path.join(DEJAVU, "DejaVuSans-Bold.ttf"), size)


def mono(size):
    return ImageFont.truetype(os.path.join(DEJAVU, "DejaVuSansMono-Bold.ttf"), size)


def wrap(d, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def rounded_mask(size, radius):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius=radius, fill=255)
    return m


def fit_img(path, w, h, radius=32):
    im = Image.open(path).convert("RGB")
    im = ImageOps.fit(im, (w, h), Image.LANCZOS)
    im.putalpha(rounded_mask((w, h), radius))
    return im


def base_slide():
    img = Image.new("RGB", (W, H), BG)
    return img, ImageDraw.Draw(img)


def lockup(d):
    d.text((W - MX - d.textlength("peka.ai.id", font=font("Poppins-Bold.ttf", 40)),
            120), "peka.ai.id", font=font("Poppins-Bold.ttf", 40), fill=CREAM)


def footer(d, page):
    d.line([(MX, H - 180), (W - MX, H - 180)], fill=HAIR, width=2)
    d.text((MX, H - 140), "GABUNG KE KOMUNITAS KAMI: URL.PEKA.AI.ID",
           font=mono(30), fill=MUTED)
    d.text((W - MX - d.textlength(f"{page:02d} / 04", font=mono(30)), H - 140),
           f"{page:02d} / 04", font=mono(30), fill=MUTED)


def cover():
    img, d = base_slide()
    lockup(d)
    d.text((MX, 170), "SHOWCASE // SKILL DESAIN AI", font=mono(34), fill=YEL)
    tf = font("Poppins-ExtraBold.ttf", 130)
    d.text((MX, 230), "SATU KALIMAT.", font=tf, fill=CREAM)
    d.rectangle([MX, 390, MX + d.textlength("JADI DESAIN.", font=tf) + 40, 390 + 150], fill=YEL)
    d.text((MX + 20, 395), "JADI DESAIN.", font=tf, fill=BG)
    d.text((MX, 580), "Huashu Design: skill desain buat agent AI.",
           font=font("Poppins-SemiBold.ttf", 44), fill=CREAM)
    hero = fit_img(os.path.join(SHOW, "case-hokusai-hero.jpg"), W - 2 * MX, 860, 40)
    img.paste(hero, (MX, 680), hero)
    d.text((MX, 1580), "Hasil beneran: web pameran Hokusai.",
           font=font("Poppins-SemiBold.ttf", 36), fill=MUTED)
    d.text((MX, 1640), "alchaincyf/huashu-design  •  27RB star  •  MIT, gratis",
           font=mono(34), fill=YEL)
    footer(d, 1)
    return img


def proof():
    img, d = base_slide()
    lockup(d)
    d.text((MX, 170), "BUKTI, BUKAN JANJI", font=mono(34), fill=YEL)
    tf = font("Poppins-ExtraBold.ttf", 110)
    d.text((MX, 230), "INI HASILNYA,", font=tf, fill=CREAM)
    d.text((MX, 350), "BUKAN MOCKUP.", font=tf, fill=CREAM)
    d.text((MX, 500), "Ini hasil beneran dari repo-nya.",
           font=font("Poppins-SemiBold.ttf", 36), fill=MUTED)
    # Two showcase images side by side.
    bw = (W - 2 * MX - 40) // 2
    left = fit_img(os.path.join(SHOW, "case-mingji-birding-app.jpg"), bw, 980, 36)
    right = fit_img(os.path.join(SHOW, "case-qianli-cover.jpg"), bw, 980, 36)
    img.paste(left, (MX, 600), left)
    img.paste(right, (MX + bw + 40, 600), right)
    d.text((MX, 1610), "App Mingji, bisa diklik",
           font=font("Poppins-Bold.ttf", 36), fill=CREAM)
    d.text((MX + bw + 40, 1610), "PPT Qianli, bisa diedit",
           font=font("Poppins-Bold.ttf", 36), fill=CREAM)
    footer(d, 2)
    return img


def how():
    img, d = base_slide()
    lockup(d)
    d.text((MX, 170), "CARA PAKAI", font=mono(34), fill=YEL)
    tf = font("Poppins-ExtraBold.ttf", 110)
    d.text((MX, 230), "6 JADI 3,", font=tf, fill=CREAM)
    d.text((MX, 350), "LALU PILIH.", font=tf, fill=CREAM)
    steps = [
        ("01", "Ketik satu kalimat", "Web, App, PPT, animasi. Tanpa Figma."),
        ("02", "Agent bikin 6 thumbnail", "3 yang paling beda, dibikin beneran."),
        ("03", "Pilih dan pakai", "84 gaya, plus bacaan aset brand."),
    ]
    y = 520
    for num, title, body in steps:
        d.text((MX, y), num, font=font("Poppins-ExtraBold.ttf", 64), fill=YEL)
        d.text((MX + 170, y), title, font=font("Poppins-Bold.ttf", 52), fill=CREAM)
        for ln in wrap(d, body, font("Poppins-SemiBold.ttf", 38), W - 2 * MX - 170):
            y += 0  # placeholder, body drawn below
        y += 70
        for ln in wrap(d, body, font("Poppins-SemiBold.ttf", 38), W - 2 * MX - 170):
            d.text((MX + 170, y), ln, font=font("Poppins-SemiBold.ttf", 38), fill=MUTED)
            y += 52
        y += 50
    # Terminal panel.
    ty = 1180
    panel = Image.new("RGB", (W - 2 * MX, 170), SURF)
    pd = ImageDraw.Draw(panel)
    for i, c in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
        pd.ellipse([40 + i * 44, 26, 40 + i * 44 + 24, 50], fill=c)
    pd.text((196, 22), "terminal", font=mono(32), fill=MUTED)
    cmd = "npx skills add alchaincyf/huashu-design"
    tf2 = mono(44)
    pd.text((44, 84), "$ ", font=tf2, fill=YEL)
    pd.text((44 + pd.textlength("$ ", font=tf2), 84), cmd, font=tf2, fill=CREAM)
    img.paste(panel, (MX, ty), rounded_mask((W - 2 * MX, 170), 28))
    d.text((MX, ty + 200), "Buat deck, landing page, dan prototipe. Tanpa tim desain.",
           font=font("Poppins-Bold.ttf", 40), fill=CREAM)
    footer(d, 3)
    return img


def follow():
    img, d = base_slide()
    lockup(d)
    d.text((MX, 170), "IKUTI PEKA AI", font=mono(34), fill=YEL)
    tf = font("Poppins-ExtraBold.ttf", 130)
    d.text((MX, 230), "FOLLOW", font=tf, fill=CREAM)
    d.rectangle([MX, 390, MX + d.textlength("DAN GABUNG.", font=tf) + 40, 390 + 150], fill=YEL)
    d.text((MX + 20, 395), "DAN GABUNG.", font=tf, fill=BG)
    lines = [
        "Follow @peka.ai.id.",
        "Gabung grup WA lewat url.peka.ai.id.",
        "Save dan share buat stok.",
        "Link repo ada di komentar.",
    ]
    y = 620
    for text in lines:
        for ln in wrap(d, text, font("Poppins-SemiBold.ttf", 44), W - 2 * MX):
            d.text((MX, y), ln, font=font("Poppins-SemiBold.ttf", 44), fill=CREAM)
            y += 60
        y += 30
    footer(d, 4)
    return img


def main():
    for i, fn in enumerate([cover, proof, how, follow], start=1):
        fn().save(os.path.join(BASE, f"showcase-{i:02d}.png"))
        print("saved", i)


if __name__ == "__main__":
    main()
