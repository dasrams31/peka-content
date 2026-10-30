"""Peka-design catalog slides for the 31 Oct 2026 product list.

Peka visual language: yellow #FFD60A, black #111111, cream text,
mascot lockup, community footer + page number. Three 4096x4096
slides: cover, products 1-3, products 4-5 + CTA.
Prices are exactly the user's list. Do not "correct" them
against the 21 Oct Aeternum catalog. All product data is read from
../prices.json; that file's `updated` date is the freshness signal
for the posting cron.
"""
import json
import os

from PIL import Image, ImageDraw, ImageFont

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "prices.json"), encoding="utf-8") as _fh:
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
OUT = "/home/hatch/workspace/peka-content/katalog/2026-10-31"

M = 420  # content margin inside the card


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


def footer(d, page):
    fy = 3560
    f_foot = ImageFont.truetype(FS, 44)
    tracked(d, "GABUNG KE KOMUNITAS KAMI: URL.PEKA.AI.ID", f_foot,
            MUTED, M, fy, 5)
    f_pg = ImageFont.truetype(FB, 44)
    pg = f"0{page} / 03"
    pw = d.textlength(pg, font=f_pg)
    d.text((3936 - M + 80 - pw, fy), pg, font=f_pg, fill=YELLOW)


def header_row(d, kicker):
    f_kick = ImageFont.truetype(FB, 52)
    tracked(d, kicker, f_kick, YELLOW, M, 470, 8)


def product_rows(d, blocks, y):
    f_sec = ImageFont.truetype(FS, 84)
    f_item = ImageFont.truetype(FS, 118)
    f_price = ImageFont.truetype(FB, 138)
    for sec_name, items in blocks:
        tracked(d, sec_name, f_sec, YELLOW, M, y, 10)
        y += 170
        for label, price in items:
            d.text((M, y), label, font=f_item, fill=CREAM)
            pw = d.textlength(price, font=f_price)
            d.text((W - M - pw, y - 14), price, font=f_price, fill=YELLOW)
            lx = M + d.textlength(label, font=f_item) + 70
            rx = W - M - pw - 70
            dot_y = y + 78
            x = lx
            while x < rx:
                d.ellipse([x, dot_y, x + 12, dot_y + 12],
                          fill=(170, 165, 150, 170))
                x += 52
            y += 210
            d.line([M, y, W - M, y], fill=CARD_LINE, width=3)
            y += 120
        y += 150
    return y


def label_of(p):
    label = p["name"]
    if p.get("note"):
        label += f" ({p['note']})"
    return f"{label}  ·  {p['dur']}"


def blocks_of(ps):
    return [(p["sec"], [(label_of(p), p["price"])]) for p in ps]
img, d = base()
header_row(d, "KATALOG HARI INI")

mascot = Image.open(MASCOT)
mw, mh = mascot.size
mh2 = 1050
mascot = mascot.resize((int(mh2 * mw / mh), mh2), Image.LANCZOS)
img.paste(mascot, (W - M - mascot.width - 60, 640), mascot)

f_h = ImageFont.truetype(FX, 300)
d.text((M - 8, 760), "AKUN", font=f_h, fill=CREAM)
d.text((M - 8, 1080), "PREMIUM", font=f_h, fill=CREAM)
f_h2 = ImageFont.truetype(FX, 300)
t2 = START_LABEL
d.text((M - 8, 1400), "MULAI ", font=f_h2, fill=CREAM)
w_pre = d.textlength("MULAI ", font=f_h2)
hl_w = d.textlength(t2, font=f_h2)
d.rounded_rectangle([M - 8 + w_pre - 24, 1400 - 40,
                     M - 8 + w_pre + hl_w + 24, 1400 + 372],
                    radius=36, fill=YELLOW)
d.text((M - 8 + w_pre, 1400), t2, font=f_h2, fill=BLACK)

f_sub = ImageFont.truetype(FS, 84)
d.text((M, 1960), f"{len(PRODUCTS)} akun ready hari ini.", font=f_sub, fill=CREAM)
d.text((M, 2075), f"{DATE_LABEL}.", font=f_sub, fill=MUTED)

f_geser = ImageFont.truetype(FM, 62)
tracked(d, "GESER BUAT LIHAT HARGANYA  >>", f_geser, YELLOW, M, 3120, 4)

footer(d, 1)
img.save(f"{OUT}/peka-katalog-01.png")
print("saved slide 1")

# ---------------- slide 2: products 1-3 ----------------
img, d = base()
header_row(d, "KATALOG HARI INI  //  01 - 03")

product_rows(d, blocks_of(PRODUCTS[:3]), 760)

footer(d, 2)
img.save(f"{OUT}/peka-katalog-02.png")
print("saved slide 2")

# ---------------- slide 3: products 4-5 + CTA ----------------
img, d = base()
header_row(d, "KATALOG HARI INI  //  04 - 05")

y = product_rows(d, blocks_of(PRODUCTS[3:]), 760)

band_y = y + 60
d.rounded_rectangle([M, band_y, W - M, band_y + 250], radius=48, fill=YELLOW)
f_cta = ImageFont.truetype(FB, 96)
cta = "MAU?  CHAT:  MAU [NAMA PRODUK]"
cw = d.textlength(cta, font=f_cta)
d.text(((W - cw) / 2, band_y + 72), cta, font=f_cta, fill=BLACK)

f_note = ImageFont.truetype(FS, 72)
note = "Atau gabung grup WA: url.peka.ai.id"
nw = d.textlength(note, font=f_note)
d.text(((W - nw) / 2, band_y + 320), note, font=f_note, fill=CREAM)

footer(d, 3)
img.save(f"{OUT}/peka-katalog-03.png")
print("saved slide 3")
