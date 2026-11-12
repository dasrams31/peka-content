#!/usr/bin/env python3
"""Slides for the Peka sales post: Prompt Automation Konten Sosmed.

4 slides, 4096x4096, Peka yellow/black two-tone. No em-dash in any text.
Usage: jualan_slides.py <out_dir>
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

YELLOW = (255, 214, 10)
BLACK = (17, 17, 17)
INK = (22, 22, 22)
WHITE = (255, 255, 255)
GREY = (168, 168, 158)

FONT_DIR = "/home/hatch/workspace/sertiku-poster/fonts"
MONO = "/home/hatch/workspace/peka-content/prompt/animated/assets/DejaVuSansMono-Bold.ttf"
MASCOT = "/home/hatch/workspace/peka-content/blueprint/animated/assets/mascot-keyed.png"

W = H = 4096
MARGIN = 300


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, fnt_name, size, max_w, max_h, lh):
    while size > 40:
        fnt = font(fnt_name, size)
        lines = wrap(draw, text, fnt, max_w)
        if len(lines) * size * lh <= max_h:
            return fnt, lines
        size -= 6
    fnt = font(fnt_name, size)
    return fnt, wrap(draw, text, fnt, max_w)


def chip(draw, x, y, text, fnt, fg, bg, pad_x=64, pad_y=36, outline=None, width=None):
    tw = draw.textlength(text, font=fnt)
    w = width or (tw + pad_x * 2)
    h = fnt.size + pad_y * 2
    draw.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=bg,
                           outline=outline, width=8 if outline else 1)
    draw.text((x + (w - tw) / 2, y + pad_y - 8), text, font=fnt, fill=fg)
    return w, h


def mascot(draw, base, x, y, size=260):
    if not os.path.exists(MASCOT):
        return
    m = Image.open(MASCOT).convert("RGBA").resize((size, size), Image.LANCZOS)
    base.paste(m, (x, y), m)


def slide1(out):
    img = Image.new("RGB", (W, H), YELLOW)
    d = ImageDraw.Draw(img)
    f_chip = font("Poppins-Bold.ttf", 92)
    chip(d, MARGIN, MARGIN, "JUALAN SPESIAL", f_chip, YELLOW, BLACK)
    f_head = font("Poppins-ExtraBold.ttf", 330)
    y = 1080
    for line in ["AUTOMATION", "KONTEN SOSMED", "DI MUSE AI."]:
        d.text((MARGIN, y), line, font=f_head, fill=INK)
        y += 345
    f_sub, lines = fit_lines(d, "Prompt 7 fase siap salin. Paste ke Muse baru, ikuti fasenya, sistemnya jalan tiap hari.",
                             "Poppins-SemiBold.ttf", 118, W - 2 * MARGIN, 620, 1.35)
    y = 2300
    for ln in lines:
        d.text((MARGIN, y), ln, font=f_sub, fill=INK)
        y += int(f_sub.size * 1.35)
    f_price = font("Poppins-Bold.ttf", 120)
    w1, _ = chip(d, MARGIN, 3120, "RP75.000", f_price, YELLOW, BLACK)
    chip(d, MARGIN + w1 + 48, 3120, "SEKALI BAYAR", f_price, INK, None, outline=INK)
    d.text((MARGIN, H - 340), "@PEKA.AI.ID", font=font("Poppins-Bold.ttf", 96), fill=INK)
    img.save(out)


def slide2(out):
    img = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(img)
    d.text((MARGIN, 330), "ISI PROMPTNYA", font=font("Poppins-Bold.ttf", 120), fill=YELLOW)
    rows = [
        "Fondasi brand dan akun",
        "Struktur folder dan file kunci",
        "Aturan main yang terkunci",
        "Pilar konten dan resep satu edisi",
        "Generator visual dan reel animasi",
        "Posting, cron, dan guard anti-dobel",
        "Learning loop dan lampiran template",
    ]
    y = 640
    for i, row in enumerate(rows, 1):
        d.rounded_rectangle([MARGIN, y, MARGIN + 170, y + 170], radius=36, fill=YELLOW)
        f_num = font("Poppins-ExtraBold.ttf", 104)
        num = str(i)
        nw = d.textlength(num, font=f_num)
        d.text((MARGIN + (170 - nw) / 2, y + 24), num, font=f_num, fill=INK)
        f_txt = font("Poppins-SemiBold.ttf", 108)
        d.text((MARGIN + 240, y + 26), row, font=f_txt, fill=WHITE)
        y += 440
    d.text((MARGIN, H - 340), "7 FASE, DARI NOL SAMPAI JALAN.", font=font("Poppins-Bold.ttf", 84), fill=GREY)
    img.save(out)


def slide3(out):
    img = Image.new("RGB", (W, H), YELLOW)
    d = ImageDraw.Draw(img)
    d.text((MARGIN, 330), "CARA BELI", font=font("Poppins-Bold.ttf", 120), fill=INK)
    steps = [
        ("1", "Beli akun Muse Spark Lifetime, 24 ribu."),
        ("2", "Beli prompt 7 fase, 75 ribu."),
        ("3", "Paste promptnya ke Muse baru, automation jalan."),
    ]
    y = 640
    for num, text in steps:
        d.rounded_rectangle([MARGIN, y, W - MARGIN, y + 640], radius=72, fill=WHITE)
        f_num = font("Poppins-ExtraBold.ttf", 200)
        f_txt, lines = fit_lines(d, text, "Poppins-SemiBold.ttf", 128, W - 2 * MARGIN - 420, 480, 1.3)
        block_h = len(lines) * int(f_txt.size * 1.3)
        d.text((MARGIN + 80, y + (640 - 200) // 2 - 20), num, font=f_num, fill=INK)
        ty = y + (640 - block_h) // 2
        for ln in lines:
            d.text((MARGIN + 360, ty), ln, font=f_txt, fill=INK)
            ty += int(f_txt.size * 1.3)
        y += 740
    d.text((MARGIN, H - 340), "Beli akun Muse bisa DM, atau di bot dan web.",
           font=font("Poppins-Bold.ttf", 92), fill=INK)
    img.save(out)


def slide4(out, shortlink):
    img = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(img)
    f_head = font("Poppins-ExtraBold.ttf", 340)
    y = 900
    for line in ["MULAI", "MALAM INI."]:
        d.text((MARGIN, y), line, font=f_head, fill=YELLOW)
        y += 355
    f_mono = font("DejaVuSansMono-Bold.ttf", 118) if False else ImageFont.truetype(MONO, 118)
    label = shortlink
    tw = d.textlength(label, font=f_mono)
    bw, bh = tw + 160, 280
    bx, by = MARGIN, 1980
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=48, outline=YELLOW, width=10)
    d.text((bx + 80, by + 72), label, font=f_mono, fill=YELLOW)
    f_band = font("Poppins-Bold.ttf", 104)
    w1, _ = chip(d, MARGIN, 2480, "FOLLOW @PEKA.AI.ID", f_band, BLACK, YELLOW)
    d.text((MARGIN, H - 520), "GABUNG KE KOMUNITAS KAMI: S.PEKA.AI.ID/GABUNG",
           font=font("Poppins-Bold.ttf", 80), fill=GREY)
    d.text((MARGIN, H - 380), "Save dan share kalau berguna.",
           font=font("Poppins-SemiBold.ttf", 88), fill=GREY)
    img.save(out)


def main():
    out_dir = sys.argv[1]
    shortlink = sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)
    slide1(os.path.join(out_dir, "slide-01.png"))
    slide2(os.path.join(out_dir, "slide-02.png"))
    slide3(os.path.join(out_dir, "slide-03.png"))
    slide4(os.path.join(out_dir, "slide-04.png"), shortlink)
    print("slides done:", out_dir)


main()
