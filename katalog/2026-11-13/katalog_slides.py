"""Peka-design catalog slides, generic template.

Peka visual language: yellow #FFD60A, black #111111, cream text,
mascot lockup, community footer + page number. Slides are 4096x4096:
one cover plus as many product slides as the list needs. Products are
grouped by section (one header per brand, one row per duration
variant) and paginated greedily so no slide overflows: at most ~2640px
of product rows per slide. The last product slide carries the CTA band.
Prices are exactly the user's list in ../prices.json. Do not "correct"
them. This file is the template source for the katalog cron: each
edition copies it into its own folder and OUT follows the script's
own directory, so the copy needs no edits.
"""
import json
import os
from collections import OrderedDict

from PIL import Image, ImageDraw, ImageFont

_HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(_HERE, "..", "prices.json"), encoding="utf-8") as _fh:
    _PRICES = json.load(_fh)
PRODUCTS = _PRICES["products"]
DATE_LABEL = _PRICES["date_label"]
MIN_PRICE = min(p["price_num"] for p in PRODUCTS)
START_LABEL = f"{MIN_PRICE}K."

W = H = 4096
YELLOW = (255, 214, 10)
BLACK = (17, 17, 17)
CREAM = (246, 241, 230)
MUTED = (170, 165, 150)
CARD_LINE = (246, 241, 230, 90)

FONTS = "/home/hatch/workspace/sertiku-poster/fonts"
FB = f"{FONTS}/Poppins-Bold.ttf"
FX = f"{FONTS}/Poppins-ExtraBold.ttf"
FS = f"{FONTS}/Poppins-SemiBold.ttf"
FM = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

MASCOT = "/home/hatch/workspace/peka-content/blueprint/animated/assets/mascot-keyed.png"
OUT = _HERE

M = 420  # content margin inside the card
Y_TOP = 760
Y_LIMIT = 3400
SEC_GAP = 300


def tracked(d, text, font, fill, x, y, ls):
    cx = x
    for ch in text:
        d.text((cx, y), ch, font=font, fill=fill)
        cx += d.textlength(ch, font=font) + ls
    return cx


def tracked_w(d, text, font, ls):
    return sum(d.textlength(ch, font=font) + ls for ch in text) - ls


def dashed_rect(d, box, fill, width=4, dash=36, gap=26):
    x0, y0, x1, y1 = box
    x = x0
    while x < x1:
        d.line([x, y0, min(x + dash, x1), y0], fill=fill, width=width)
        d.line([x, y1, min(x + dash, x1), y1], fill=fill, width=width)
        x += dash + gap
    y = y0
    while y < y1:
        d.line([x0, y, x0, min(y + dash, y1)], fill=fill, width=width)
        d.line([x1, y, x1, min(y + dash, y1)], fill=fill, width=width)
        y += dash + gap


def base():
    img = Image.new("RGB", (W, H), YELLOW)
    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle([160, 160, 3936, 3936], radius=90, fill=BLACK)
    dashed_rect(d, [240, 240, 3856, 3856], CARD_LINE, width=4)
    return img, d


def footer(d, page, total):
    fy = 3560
    f_foot = ImageFont.truetype(FS, 44)
    tracked(d, "GABUNG KE KOMUNITAS KAMI: S.PEKA.AI.ID/GABUNG", f_foot,
            MUTED, M, fy, 5)
    f_pg = ImageFont.truetype(FB, 44)
    pg = f"{page:02d} / {total:02d}"
    pw = d.textlength(pg, font=f_pg)
    d.text((3936 - M + 80 - pw, fy), pg, font=f_pg, fill=YELLOW)


def header_row(d, kicker):
    f_kick = ImageFont.truetype(FB, 52)
    tracked(d, kicker, f_kick, YELLOW, M, 470, 8)


def product_rows(d, blocks, y):
    f_sec = ImageFont.truetype(FS, 88)
    f_item = ImageFont.truetype(FS, 124)
    f_price = ImageFont.truetype(FB, 150)
    for si, (sec_name, items) in enumerate(blocks):
        tracked(d, sec_name, f_sec, YELLOW, M, y, 10)
        y += 180
        for label, price in items:
            d.text((M, y), label, font=f_item, fill=CREAM)
            pw = d.textlength(price, font=f_price)
            d.text((W - M - pw, y - 14), price, font=f_price, fill=YELLOW)
            lx = M + d.textlength(label, font=f_item) + 70
            rx = W - M - pw - 70
            dot_y = y + 82
            x = lx
            while x < rx:
                d.ellipse([x, dot_y, x + 12, dot_y + 12],
                          fill=(170, 165, 150, 170))
                x += 52
            y += 230
            d.line([M, y, W - M, y], fill=CARD_LINE, width=3)
            y += 130
        if si < len(blocks) - 1:
            y += SEC_GAP
    return y


def label_of(p):
    label = p["name"]
    if p.get("note"):
        label += f" ({p['note']})"
    return f"{label}  ·  {p['dur']}"


def sections_of(ps):
    grouped = OrderedDict()
    for p in ps:
        grouped.setdefault(p["sec"], []).append((label_of(p), p["price"]))
    return list(grouped.items())


def section_height(n_rows):
    return 180 + n_rows * 360


def paginate(sections):
    pages = []
    cur, cur_h = [], 0
    for sec in sections:
        h = section_height(len(sec[1]))
        add = h if not cur else h + SEC_GAP
        if cur and cur_h + add > Y_LIMIT - Y_TOP:
            pages.append(cur)
            cur, cur_h = [sec], h
        else:
            cur.append(sec)
            cur_h += add
    if cur:
        pages.append(cur)
    return pages


SECTIONS = sections_of(PRODUCTS)
PAGES = paginate(SECTIONS)
TOTAL = 1 + len(PAGES)

# Row indices per page, for the "01 - 03" header ranges.
_row_starts = []
_n = 0
for _page in PAGES:
    _row_starts.append(_n + 1)
    _n += sum(len(items) for _, items in _page)
ROW_RANGES = [
    (_row_starts[i], _row_starts[i] + sum(len(items) for _, items in _page) - 1)
    for i, _page in enumerate(PAGES)
]

# ---------------- cover ----------------
img, d = base()
header_row(d, "KATALOG HARI INI")

mascot = Image.open(MASCOT)
mw, mh = mascot.size
mh2 = 1260
mascot = mascot.resize((int(mh2 * mw / mh), mh2), Image.LANCZOS)
img.paste(mascot, (W - M - mascot.width - 60, 600), mascot)

f_h = ImageFont.truetype(FX, 300)
d.text((M - 8, 760), "AKUN", font=f_h, fill=CREAM)
d.text((M - 8, 1080), "PREMIUM", font=f_h, fill=CREAM)
f_h2 = ImageFont.truetype(FX, 300)
t2 = START_LABEL
d.text((M - 8, 1440), "MULAI ", font=f_h2, fill=CREAM)
w_pre = d.textlength("MULAI ", font=f_h2)
hl_w = d.textlength(t2, font=f_h2)
d.rounded_rectangle([M - 8 + w_pre - 24, 1440 - 40,
                     M - 8 + w_pre + hl_w + 24, 1440 + 372],
                    radius=36, fill=YELLOW)
d.text((M - 8 + w_pre, 1440), t2, font=f_h2, fill=BLACK)

f_sub = ImageFont.truetype(FS, 84)
d.text((M, 1960), f"{len(PRODUCTS)} akun ready hari ini.", font=f_sub, fill=CREAM)
d.text((M, 2075), f"{DATE_LABEL}.", font=f_sub, fill=MUTED)

f_geser = ImageFont.truetype(FM, 62)
tracked(d, "GESER BUAT LIHAT HARGANYA  >>", f_geser, YELLOW, M, 3040, 4)

footer(d, 1, TOTAL)
img.save(f"{OUT}/peka-katalog-01.png")
print("saved slide 1")

# ---------------- product slides ----------------
for pi, page in enumerate(PAGES):
    img, d = base()
    r0, r1 = ROW_RANGES[pi]
    header_row(d, f"KATALOG HARI INI  //  {r0:02d} - {r1:02d}")
    y = product_rows(d, page, Y_TOP)
    if pi == len(PAGES) - 1:
        # Cap the CTA band so its note (band_y + 320, font 72) never
        # reaches the footer at y=3560 on a tall last page.
        band_y = min(y + 200, 3100)
        d.rounded_rectangle([M, band_y, W - M, band_y + 250], radius=48, fill=YELLOW)
        f_cta = ImageFont.truetype(FB, 96)
        cta = "MAU?  CHAT:  MAU [NAMA PRODUK]"
        cw = d.textlength(cta, font=f_cta)
        d.text(((W - cw) / 2, band_y + 72), cta, font=f_cta, fill=BLACK)
        f_note = ImageFont.truetype(FS, 72)
        note = "Atau gabung grup WA: s.peka.ai.id/gabung"
        nw = d.textlength(note, font=f_note)
        d.text(((W - nw) / 2, band_y + 320), note, font=f_note, fill=CREAM)
    footer(d, pi + 2, TOTAL)
    img.save(f"{OUT}/peka-katalog-{pi + 2:02d}.png")
    print(f"saved slide {pi + 2}")
