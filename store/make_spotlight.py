#!/usr/bin/env python3
"""Generate Peka Store spotlight slides (2048x2048, 2K) for hero products.
Usage: python3 make_spotlight.py
Output: spotlight/spot-01.png ... spot-04.png
"""
import os

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
S = 2048 / 1080
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

def lockup(img, d):
    cy, mh = X(95), X(46)
    cr = _creature.resize((int(_creature.width * mh / _creature.height), mh), Image.LANCZOS)
    mr = _cmask.resize(cr.size, Image.LANCZOS)
    tf = f(34)
    txt_w = d.textlength("peka.ai.id", font=tf)
    gap = X(12)
    tx = X(1010) - txt_w
    mx = tx - gap - cr.width
    img.paste(cr, (int(mx), int(cy - mh / 2)), mr)
    d.text((tx, cy - X(17)), "peka.ai.id", font=tf, fill=YEL)

def badge(d, label="PEKA STORE"):
    font = f(36)
    w = d.textlength(label, font=font) + X(60)
    d.rounded_rectangle([X(70), X(60), X(70) + w, X(130)], radius=X(35), fill=YEL)
    d.text((X(100), X(73)), label, font=font, fill=BLK)

def texture(d):
    for i in range(0, X(420), X(52)):
        d.line([(W - i, 0), (W, i)], fill="#181818", width=X(16))

def footer(d, i, n):
    d.text((X(70), X(1015)), "PEKA STORE · SPOTLIGHT", font=f(24, False), fill=GRY)
    pg = f"{i}/{n}"
    d.text((X(1010) - d.textlength(pg, font=f(24, False)), X(1015)), pg, font=f(24, False), fill=GRY)

def headline(d, lines, y0):
    y = X(y0)
    for line, col, sz0 in lines:
        sz = sz0
        while d.textlength(line, font=f(sz)) > W - X(140) and sz > 20:
            sz -= 2
        d.text((X(70), y), line, font=f(sz), fill=col)
        y += int(X(sz) * 1.14)
    return y

def rows(d, items, y0):
    y = X(y0)
    for name, price, note in items:
        nsz = 40
        while d.textlength(name, font=f(nsz)) > X(620) and nsz > 22:
            nsz -= 2
        d.text((X(70), y), name, font=f(nsz), fill=WHT)
        pw = d.textlength(price, font=mono(46))
        d.text((X(1010) - pw, y - X(2)), price, font=mono(46), fill=YEL)
        y += X(58)
        if note:
            d.text((X(70), y), note, font=f(28, False), fill=GRY)
            y += X(40)
        y += X(34)
    return y

def price_hero(d, price, per, y0):
    # huge centered price, starting below the headline
    sz = 210
    while d.textlength(price, font=f(sz)) > W - X(280) and sz > 40:
        sz -= 4
    pw = d.textlength(price, font=f(sz))
    y = y0 + X(10)
    d.text(((W - pw) / 2, y), price, font=f(sz), fill=YEL)
    per_w = d.textlength(per, font=f(40, False))
    d.text(((W - per_w) / 2, y + int(X(sz) * 1.05)), per, font=f(40, False), fill=GRY)
    return y + int(X(sz) * 1.05) + X(70)

def cta(d, y, order_text):
    d.rounded_rectangle([X(70), y, X(1010), y + X(150)], radius=X(18), fill=YEL)
    d.text((X(110), y + X(28)), "READY STOCK", font=f(44), fill=BLK)
    d.text((X(110), y + X(88)), f'ORDER? DM: "{order_text}"', font=f(32), fill=BLK)
    return y + X(150)

SPOTS = [
    {"file": "spot-01.png", "head": [("GEMINI", WHT, 130), ("PRO", YEL, 130)],
     "rows": [("18 Bulan", "19K", None), ("3 Bulan", "13K", None)],
     "cta": "MAU GEMINI PRO"},
    {"file": "spot-02.png", "head": [("CAPCUT", WHT, 130), ("PRO", YEL, 130)],
     "hero": ("29K", "1 Bulan"), "cta": "MAU CAPCUT PRO"},
    {"file": "spot-03.png", "head": [("CANVA", YEL, 130)],
     "rows": [("Pro Invite 1 Bulan", "6K", None), ("Pro Head 1 Bulan", "11K", None),
              ("EDU 6 Bulan", "18K", None), ("2 Tahun", "40K", "Garansi 6 bulan")],
     "cta": "MAU CANVA"},
    {"file": "spot-04.png", "head": [("MICROSOFT", WHT, 120), ("365", YEL, 120)],
     "hero": ("34K", "1 Tahun"), "cta": "MAU MICROSOFT 365"},
]

def main():
    outdir = os.path.join(BASE, "spotlight")
    os.makedirs(outdir, exist_ok=True)
    n = len(SPOTS)
    for idx, s in enumerate(SPOTS, 1):
        img = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(img)
        texture(d); badge(d); lockup(img, d)
        y = headline(d, s["head"], 200)
        if s.get("rows"):
            y = rows_at(d, s["rows"], y + X(30))
        elif s.get("hero"):
            y = price_hero(d, s["hero"][0], s["hero"][1], y)
        y = cta(d, y + X(20), s["cta"])
        footer(d, idx, n)
        path = os.path.join(outdir, s["file"])
        img.save(path)
        print("wrote", path, img.size)

def rows_at(d, items, y):
    for name, price, note in items:
        nsz = 40
        while d.textlength(name, font=f(nsz)) > X(620) and nsz > 22:
            nsz -= 2
        d.text((X(70), y), name, font=f(nsz), fill=WHT)
        pw = d.textlength(price, font=mono(46))
        d.text((X(1010) - pw, y - X(2)), price, font=mono(46), fill=YEL)
        y += X(58)
        if note:
            d.text((X(70), y), note, font=f(28, False), fill=GRY)
            y += X(40)
        y += X(34)
    return y

if __name__ == "__main__":
    main()
