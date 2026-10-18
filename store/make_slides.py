#!/usr/bin/env python3
"""Generate Peka Store price-list slide deck (2048x2048, 2K) from products.json.
Usage: python3 make_slides.py
Output: slides/slide-01.png ... slide-08.png
Re-run whenever products.json changes.
Layout is authored in 1080-space and scaled by S.
"""
import json
import os

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
S = 2048 / 1080  # 2K scale factor
W = H = 2048
BG = "#111111"; YEL = "#ffd60a"; WHT = "#ffffff"; BLK = "#111111"; GRY = "#9a9a9a"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FM = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

def X(v):
    return int(round(v * S))

def f(sz, bold=True):
    return ImageFont.truetype(FB if bold else FR, X(sz))

def mono(sz):
    return ImageFont.truetype(FM, X(sz))

# P creature cropped for the header lockup
_m = Image.open("/home/hatch/workspace/peka-logo/mascot-p.png").convert("RGB")
_mmask = Image.new("L", _m.size, 0)
_mp = _m.load(); _mk = _mmask.load()
for yy in range(_m.size[1]):
    for xx in range(_m.size[0]):
        r, g, b = _mp[xx, yy]
        if r > 30 or g > 30 or b > 30:
            _mk[xx, yy] = 255
_creature = _m.crop(_mmask.getbbox())
_cmask = _mmask.crop(_mmask.getbbox())

def lockup(img, d, cy=95, mh=46):
    cy, mh = X(cy), X(mh)
    cr = _creature.resize((int(_creature.width * mh / _creature.height), mh), Image.LANCZOS)
    mr = _cmask.resize(cr.size, Image.LANCZOS)
    tf = f(34)
    txt_w = d.textlength("peka.ai.id", font=tf)
    gap = X(12)
    tx = X(1010) - txt_w
    mx = tx - gap - cr.width
    img.paste(cr, (int(mx), int(cy - mh / 2)), mr)
    d.text((tx, cy - X(17)), "peka.ai.id", font=tf, fill=YEL)

def badge(d, label):
    font = f(36)
    w = d.textlength(label, font=font) + X(60)
    d.rounded_rectangle([X(70), X(60), X(70) + w, X(130)], radius=X(35), fill=YEL)
    d.text((X(100), X(73)), label, font=font, fill=BLK)

def texture(d):
    for i in range(0, X(420), X(52)):
        d.line([(W - i, 0), (W, i)], fill="#181818", width=X(16))

def footer(d, i, n):
    d.text((X(70), X(1015)), "PEKA STORE", font=f(24, False), fill=GRY)
    pg = f"{i}/{n}"
    d.text((X(1010) - d.textlength(pg, font=f(24, False)), X(1015)), pg, font=f(24, False), fill=GRY)

def draw_cover(d, img, n):
    texture(d); badge(d, "PEKA STORE"); lockup(img, d)
    y = X(200)
    for line, col, sz0 in [("PEKA STORE", WHT, 118), ("LIST HARGA", YEL, 118)]:
        sz = sz0
        while d.textlength(line, font=f(sz)) > W - X(140) and sz > 20:
            sz -= 2
        d.text((X(70), y), line, font=f(sz), fill=col)
        y += int(X(sz) * 1.14)
    d.text((X(70), y + X(20)), "Update Oktober 2026 · semua ready stock", font=f(34, False), fill=GRY)
    d.rounded_rectangle([X(70), X(620), X(1010), X(780)], radius=X(18), fill="#161616",
                        outline=YEL, width=X(3))
    d.text((X(110), X(650)), "ORDER? DM:", font=f(44), fill=WHT)
    d.text((X(110), X(710)), '"MAU [NAMA PRODUK]"', font=mono(40), fill=YEL)
    d.text((X(70), X(830)), "Geser untuk lihat semua list.", font=f(32, False), fill=GRY)
    footer(d, 1, n)

def draw_products(d, img, slide, i, n):
    texture(d); badge(d, slide["badge"]); lockup(img, d)
    y = X(220)
    for it in slide["items"]:
        sold = it.get("sold", False)
        name_col = "#6a6a6a" if sold else WHT
        price_col = "#6a6a6a" if sold else YEL
        name = it["name"]
        nsz = 38
        while d.textlength(name, font=f(nsz)) > X(640) and nsz > 22:
            nsz -= 2
        d.text((X(70), y), name, font=f(nsz), fill=name_col)
        price = it["price"]
        pw = d.textlength(price, font=mono(42))
        d.text((X(1010) - pw, y - X(2)), price, font=mono(42), fill=price_col)
        if sold:
            ny = y + X(22)
            d.line([(X(70), ny), (X(70) + d.textlength(name, font=f(nsz)), ny)],
                   fill="#6a6a6a", width=X(3))
        y += X(56)
        if it.get("note"):
            d.text((X(70), y), it["note"], font=f(28, False), fill=GRY)
            y += X(40)
        y += X(32)
    if slide.get("type") == "products_cta":
        d.rounded_rectangle([X(70), y + X(10), X(1010), y + X(150)], radius=X(18), fill=YEL)
        d.text((X(110), y + X(32)), "READY STOCK", font=f(48), fill=BLK)
        d.text((X(110), y + X(92)), 'ORDER? DM: "MAU [NAMA PRODUK]"', font=f(30), fill=BLK)
    footer(d, i, n)

def main():
    with open(os.path.join(BASE, "products.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    slides = data["slides"]
    outdir = os.path.join(BASE, "slides")
    os.makedirs(outdir, exist_ok=True)
    n = len(slides)
    for idx, s in enumerate(slides, 1):
        img = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(img)
        if s["type"] == "cover":
            draw_cover(d, img, n)
        else:
            draw_products(d, img, s, idx, n)
        path = os.path.join(outdir, f"slide-{idx:02d}.png")
        img.save(path)
        print("wrote", path, img.size)

if __name__ == "__main__":
    main()
