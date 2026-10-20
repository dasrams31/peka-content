#!/usr/bin/env python3
"""Peka Store CATALOG slide generator (2048x2048) with daily rotating themes.

Replaces the old single-look price list. Every day the deck renders in a
different catalog theme, rotating by day_of_year % 4:
  0 KERTAS  - cream paper catalog, dotted price leaders, ink type
  1 ETALASE - black shelf catalog, dark rows, yellow price chips
  2 KUNING  - full yellow market catalog, black type, inverted price blocks
  3 PUTIH   - minimal white catalog, hairlines, quiet type

Content always comes from products.json (same 8-slide structure as before:
cover + one page per category + closing CTA on the last page). Prices are
never invented; SOLD items render as HABIS with a struck name.

Usage:
  python3 make_slides.py [--date YYYY-MM-DD] [--theme N] [--out DIR]
Defaults: today, theme from date, out = slides/ next to this file.
"""
import argparse
import datetime
import json
import os

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
S = 2048

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FM = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FMB = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

YELLOW = (255, 214, 10)
BLACK = (17, 17, 17)

THEMES = [
    {"name": "KERTAS", "bg": (246, 241, 230), "ink": (22, 22, 22),
     "sub": (110, 104, 90), "line": (198, 190, 168), "leader": (168, 160, 138),
     "price_bg": YELLOW, "price_fg": BLACK, "band_bg": BLACK, "band_fg": (246, 241, 230),
     "lockup": (22, 22, 22), "lockup_chip": BLACK, "row_bg": None},
    {"name": "ETALASE", "bg": BLACK, "ink": (255, 255, 255),
     "sub": (154, 154, 154), "line": (48, 48, 48), "leader": (90, 90, 90),
     "price_bg": (34, 34, 34), "price_fg": YELLOW, "band_bg": YELLOW, "band_fg": BLACK,
     "lockup": YELLOW, "lockup_chip": None, "row_bg": (26, 26, 26)},
    {"name": "KUNING", "bg": YELLOW, "ink": BLACK,
     "sub": (92, 77, 0), "line": (17, 17, 17), "leader": (150, 128, 0),
     "price_bg": BLACK, "price_fg": YELLOW, "band_bg": BLACK, "band_fg": YELLOW,
     "lockup": BLACK, "lockup_chip": BLACK, "row_bg": None},
    {"name": "PUTIH", "bg": (255, 255, 255), "ink": (20, 20, 20),
     "sub": (138, 138, 138), "line": (227, 227, 227), "leader": (190, 190, 190),
     "price_bg": None, "price_fg": (20, 20, 20), "band_bg": (20, 20, 20),
     "band_fg": (255, 255, 255), "lockup": (20, 20, 20), "lockup_chip": BLACK,
     "row_bg": None},
]

HARI = ["SENIN", "SELASA", "RABU", "KAMIS", "JUMAT", "SABTU", "MINGGU"]
BULAN = ["JANUARI", "FEBRUARI", "MARET", "APRIL", "MEI", "JUNI", "JULI",
         "AGUSTUS", "SEPTEMBER", "OKTOBER", "NOVEMBER", "DESEMBER"]


def f(sz):
    return ImageFont.truetype(FB, sz)


def fr(sz):
    return ImageFont.truetype(FR, sz)


def mono(sz, bold=True):
    return ImageFont.truetype(FMB if bold else FM, sz)


# --- mascot chroma-key (shared Peka asset handling) ---
_m = Image.open("/home/hatch/workspace/peka-logo/mascot-p.png").convert("RGB")
_mmask = Image.new("L", _m.size, 0)
_mp = _m.load()
_mk = _mmask.load()
for _yy in range(_m.size[1]):
    for _xx in range(_m.size[0]):
        _r, _g, _b = _mp[_xx, _yy]
        if _r > 30 or _g > 30 or _b > 30:
            _mk[_xx, _yy] = 255
_creature = _m.crop(_mmask.getbbox())
_cmask = _mmask.crop(_mmask.getbbox())


def lockup(img, cy, color, chip=None, mh=104):
    d = ImageDraw.Draw(img)
    cr = _creature.resize((int(_creature.width * mh / _creature.height), mh), Image.LANCZOS)
    mr = _cmask.resize(cr.size, Image.LANCZOS)
    tf = f(int(mh * 0.74))
    label = "peka.ai.id"
    ascent, descent = tf.getmetrics()
    tx = 1938 - d.textlength(label, font=tf)
    ty = cy - (ascent + descent) // 2
    mx = int(tx - 26 - cr.width)
    my = cy - mh // 2
    if chip is not None:
        pad = 20
        d.rounded_rectangle([mx - pad, my - pad, mx + cr.width + pad, my + mh + pad],
                            radius=34, fill=chip)
    img.paste(cr, (mx, my), mr)
    d.text((tx, ty), label, font=tf, fill=color)


def dotted(d, x0, x1, y, color, r=6, gap=26):
    x = x0
    while x < x1:
        d.ellipse([x, y - r, x + 2 * r, y + r], fill=color)
        x += gap


def price_val(p):
    try:
        return int(p.replace("K", ""))
    except (ValueError, AttributeError):
        return None


def header(d, img, th, edisi, tema_name):
    lockup(img, 128, th["lockup"], chip=th["lockup_chip"])
    d.text((110, 92), "KATALOG PEKA STORE", font=mono(44), fill=th["ink"])
    d.text((110, 152), f"{edisi}", font=fr(40), fill=th["sub"])
    d.line([110, 216, 1938, 216], fill=th["line"], width=4)


def footer(d, th, i, n, edisi):
    d.text((110, 1946), f"PEKA STORE - {edisi}", font=fr(36), fill=th["sub"])
    pg = f"HAL {i}/{n}"
    d.text((1938 - d.textlength(pg, font=mono(36)), 1946), pg, font=mono(36), fill=th["sub"])


def draw_price(d, th, x_right, y_mid, price, sold):
    pf = mono(74)
    label = "HABIS" if sold else price
    tw = d.textlength(label, font=pf)
    if sold:
        d.text((x_right - tw, y_mid - 46), label, font=pf, fill=th["sub"])
        return tw
    if th["price_bg"] is not None:
        pad_x, pad_y = 30, 14
        d.rounded_rectangle([x_right - tw - pad_x * 2, y_mid - 46 - pad_y,
                             x_right, y_mid + 46 + pad_y], radius=20, fill=th["price_bg"])
        d.text((x_right - tw - pad_x, y_mid - 46), label, font=pf, fill=th["price_fg"])
        return tw + pad_x * 2
    d.text((x_right - tw, y_mid - 46), label, font=pf, fill=th["price_fg"])
    d.rectangle([x_right - tw, y_mid + 62, x_right, y_mid + 74], fill=YELLOW)
    return tw


def product_page(d, img, th, slide, i, n, edisi, tema_name):
    header(d, img, th, edisi, tema_name)
    items = slide["items"]
    bw = d.textlength(slide["badge"], font=f(88)) + 72
    d.rounded_rectangle([110, 268, 110 + bw, 268 + 128], radius=24, fill=th["band_bg"])
    d.text((146, 288), slide["badge"], font=f(88), fill=th["band_fg"])
    cnt = f"{len(items)} PRODUK"
    d.text((1938 - d.textlength(cnt, font=mono(44)), 306), cnt, font=mono(44), fill=th["sub"])

    y = 486
    for num, it in enumerate(items, 1):
        sold = it.get("sold", False)
        row_h = 148 if it.get("note") else 118
        if th["row_bg"] is not None:
            d.rounded_rectangle([86, y - 22, 1962, y + row_h - 8], radius=22, fill=th["row_bg"])
        name_col = th["sub"] if sold else th["ink"]
        d.text((110, y + 8), f"{num:02d}", font=mono(52), fill=th["sub"])
        pf = mono(74)
        pw = d.textlength("HABIS" if sold else it["price"], font=pf) + 70
        name = it["name"]
        nsz = 64
        while d.textlength(name, font=f(nsz)) > 1938 - pw - 90 - 250 and nsz > 34:
            nsz -= 2
        nf = f(nsz)
        nw = d.textlength(name, font=nf)
        d.text((250, y), name, font=nf, fill=name_col)
        if sold:
            mid = y + nsz // 2 + 8
            d.line([250, mid, 250 + nw, mid], fill=th["sub"], width=5)
        dotted(d, 250 + nw + 44, 1938 - pw - 26, y + 40, th["leader"])
        draw_price(d, th, 1938, y + 40, it["price"], sold)
        if it.get("note"):
            d.text((250, y + 84), it["note"], font=fr(40), fill=th["sub"])
        y += row_h + 34
    if slide.get("type") == "products_cta":
        y += 6
        d.rounded_rectangle([110, y, 1938, y + 190], radius=26, fill=th["band_bg"])
        d.text((160, y + 34), "READY STOCK - ORDER LEWAT DM", font=f(58), fill=th["band_fg"])
        d.text((160, y + 112), 'Ketik: "MAU [NAMA PRODUK]"', font=mono(46), fill=th["band_fg"])
    footer(d, th, i, n, edisi)


def cover(d, img, th, cats, edisi, tema_name, n, total, min_price, updated_label):
    lockup(img, 128, th["lockup"], chip=th["lockup_chip"])
    d.text((110, 92), "PEKA STORE - KATALOG RESMI", font=mono(44), fill=th["ink"])
    d.text((110, 152), "AKUN PREMIUM HARGA MAHASISWA", font=fr(40), fill=th["sub"])
    d.line([110, 216, 1938, 216], fill=th["line"], width=4)

    d.text((110, 330), "KATALOG", font=f(250), fill=th["ink"])
    d.text((110, 590), "PEKA STORE", font=f(250), fill=th["band_bg"])
    d.rounded_rectangle([110, 900, 1938, 1032], radius=24, fill=th["band_bg"])
    band = f"{edisi} - {total} PRODUK - MULAI {min_price}K"
    bsz = 52
    while d.textlength(band, font=mono(bsz)) > 1768 and bsz > 30:
        bsz -= 2
    bf = mono(bsz)
    d.text((110 + (1828 - d.textlength(band, font=bf)) / 2, 966 - bsz // 2), band, font=bf,
           fill=th["band_fg"])

    d.text((110, 1112), "ISI KATALOG", font=mono(44), fill=th["sub"])
    y = 1188
    for name, cnt, mn in cats:
        d.text((110, y), name, font=f(58), fill=th["ink"])
        mid = f"{cnt} produk - mulai {mn}K"
        mw = d.textlength(mid, font=fr(46))
        dotted(d, 110 + d.textlength(name, font=f(58)) + 40, 1938 - mw - 40, y + 34,
               th["leader"])
        d.text((1938 - mw, y + 4), mid, font=fr(46), fill=th["sub"])
        y += 88
    d.text((110, y + 22), f"Harga update {updated_label}, bisa berubah sewaktu-waktu.",
           font=fr(42), fill=th["sub"])
    d.text((110, y + 84), 'Order lewat DM: "MAU [NAMA PRODUK]" - geser buat lihat semua halaman.',
           font=f(44), fill=th["ink"])
    footer(d, th, 1, n, edisi)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=None)
    ap.add_argument("--theme", type=int, default=None)
    ap.add_argument("--out", default=os.path.join(BASE, "slides"))
    args = ap.parse_args()

    dt = (datetime.date.fromisoformat(args.date) if args.date
          else datetime.date.today())
    theme_idx = args.theme if args.theme is not None else dt.timetuple().tm_yday % 4
    th = THEMES[theme_idx]
    edisi = f"EDISI {HARI[dt.weekday()]} {dt.day} {BULAN[dt.month - 1]} {dt.year}"

    with open(os.path.join(BASE, "products.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    slides = data["slides"]
    n = len(slides)

    cats, total, mins = [], 0, []
    seen = set()
    for s in slides:
        if s["type"] == "cover":
            continue
        vals = [price_val(it["price"]) for it in s["items"] if not it.get("sold")]
        vals = [v for v in vals if v is not None]
        label = s["badge"]
        if label in seen:
            label = label + " LANJUTAN"
        seen.add(s["badge"])
        cats.append((label, len(s["items"]), min(vals) if vals else 0))
        total += len(s["items"])
        mins.extend(vals)
    min_price = min(mins) if mins else 0

    os.makedirs(args.out, exist_ok=True)
    for idx, s in enumerate(slides, 1):
        img = Image.new("RGB", (S, S), th["bg"])
        d = ImageDraw.Draw(img)
        if s["type"] == "cover":
            cover(d, img, th, cats, edisi, th["name"], n, total, min_price,
                  f"{BULAN[dt.month - 1].capitalize()} {dt.year}")
        else:
            s2 = dict(s)
            s2["badge"] = cats[idx - 2][0]
            product_page(d, img, th, s2, idx, n, edisi, th["name"])
        path = os.path.join(args.out, f"slide-{idx:02d}.png")
        img.save(path)
        print("wrote", path)


if __name__ == "__main__":
    main()
