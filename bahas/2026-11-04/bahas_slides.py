"""Bahas-bersama carousel: humanizer-lint discussion from the Prompt #13
comment thread (@yanstd888 + @meta.ai). Peka black/yellow design language,
same card/frame/footer helpers as the katalog template. 3 slides 4096x4096.
Framing is the honest one: polishing is editing, not disguising. No link
in any text; the community URL lives only in the footer line.
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = HERE

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
M = 420


def tracked(d, text, font, fill, x, y, ls):
    cx = x
    for ch in text:
        d.text((cx, y), ch, font=font, fill=fill)
        cx += d.textlength(ch, font=font) + ls
    return cx


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
    tracked(d, "GABUNG KE KOMUNITAS KAMI: URL.PEKA.AI.ID", f_foot,
            MUTED, M, fy, 5)
    f_pg = ImageFont.truetype(FB, 44)
    pg = f"{page:02d} / {total:02d}"
    pw = d.textlength(pg, font=f_pg)
    d.text((3936 - M + 80 - pw, fy), pg, font=f_pg, fill=YELLOW)


def header_row(d, kicker):
    f_kick = ImageFont.truetype(FB, 52)
    tracked(d, kicker, f_kick, YELLOW, M, 470, 8)


def wrap_lines(d, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---------------- slide 1: cover ----------------
img, d = base()
header_row(d, "BAHAS BARENG // KOMENTAR EDISI #13")

mascot = Image.open(MASCOT)
mw, mh = mascot.size
mh2 = 1260
mascot = mascot.resize((int(mh2 * mw / mh), mh2), Image.LANCZOS)
img.paste(mascot, (W - M - mascot.width - 60, 600), mascot)

f_h = ImageFont.truetype(FX, 300)
d.text((M - 8, 760), "TULISAN AI", font=f_h, fill=CREAM)
d.text((M - 8, 1080), "BIAR GAK", font=f_h, fill=CREAM)
t2 = "KAKU."
d.text((M - 8, 1440), "", font=f_h, fill=CREAM)
hl_w = d.textlength(t2, font=f_h)
d.rounded_rectangle([M - 8 - 24, 1440 - 40,
                     M - 8 + hl_w + 24, 1440 + 372],
                    radius=36, fill=YELLOW)
d.text((M - 8, 1440), t2, font=f_h, fill=BLACK)

f_sub = ImageFont.truetype(FS, 84)
d.text((M, 1960), "Habis generate, poles dulu", font=f_sub, fill=CREAM)
d.text((M, 2075), "sebelum dikumpul.", font=f_sub, fill=CREAM)
d.text((M, 2260), "3 lint cepat, 5 menit.", font=f_sub, fill=MUTED)

f_geser = ImageFont.truetype(FM, 62)
tracked(d, "GESER BUAT LIHAT LINT-NYA  >>", f_geser, YELLOW, M, 3040, 4)

footer(d, 1, 3)
img.save(f"{OUT}/bahas-01.png")
print("saved slide 1")

# ---------------- slide 2: 3 lint ----------------
img, d = base()
header_row(d, "3 LINT CEPAT")

blocks = [
    ("01  DIKSI",
     "Ganti kata yang tidak pernah kamu ucapkan sehari-hari."),
    ("02  KALIMAT",
     "Pecah kalimat panjang. Variasikan pendek dan panjang."),
    ("03  NADA",
     "Baca keras-keras. Kalau terdengar robot, tulis ulang."),
]
f_sec = ImageFont.truetype(FS, 88)
f_item = ImageFont.truetype(FS, 104)
y = 780
max_w = W - 2 * M
for sec_name, body in blocks:
    tracked(d, sec_name, f_sec, YELLOW, M, y, 10)
    y += 190
    for line in wrap_lines(d, body, f_item, max_w):
        d.text((M, y), line, font=f_item, fill=CREAM)
        y += 150
    y += 130
    d.line([M, y, W - M, y], fill=CARD_LINE, width=3)
    y += 190

footer(d, 2, 3)
img.save(f"{OUT}/bahas-02.png")
print("saved slide 2")

# ---------------- slide 3: honest boundary ----------------
img, d = base()
header_row(d, "BATAS JUJURNYA")

f_big = ImageFont.truetype(FX, 210)
d.text((M - 8, 800), "Poles itu edit,", font=f_big, fill=CREAM)
d.text((M - 8, 1040), "bukan nyamar.", font=f_big, fill=CREAM)

f_body = ImageFont.truetype(FS, 92)
body = ("Intinya tetap tulisanmu. AI bantu kerangka, "
        "kamu yang mikir isinya.")
y = 1520
for line in wrap_lines(d, body, f_body, max_w):
    d.text((M, y), line, font=f_body, fill=CREAM)
    y += 140
y += 60
warn = "Kalau kampusmu melarang AI, jangan pakai."
for line in wrap_lines(d, warn, f_body, max_w):
    d.text((M, y), line, font=f_body, fill=MUTED)
    y += 140

band_y = 2620
d.rounded_rectangle([M, band_y, W - M, band_y + 200], radius=36, fill=YELLOW)
f_cta = ImageFont.truetype(FB, 72)
cta = "FOLLOW DAN GABUNG, KALAU KAMU SUKA."
cw = d.textlength(cta, font=f_cta)
d.text(((W - cw) / 2, band_y + 62), cta, font=f_cta, fill=BLACK)

footer(d, 3, 3)
img.save(f"{OUT}/bahas-03.png")
print("saved slide 3")
