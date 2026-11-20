#!/usr/bin/env python3
"""Render RuteStrip special carousel v2, 6 slides 4096x4096, emerald green theme.

v2 changes (user feedback 21 Nov 00:16): white Peka logo mark beside the
"peka.ai.id" text in the header (real asset, recolored from
~/workspace/peka-logo/mascot-p.png), mountain silhouettes on the dark
slides, tighter vertical balance so content fills the frame.

Palette taken from the live rutestrip.ai.id site CSS.
Fonts: Poppins (~/workspace/sertiku-poster/fonts/).
Usage: python3 render_slides.py  (writes carousel/slide-01.png .. slide-06.png)
"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.dirname(os.path.abspath(__file__))
CAR = os.path.join(OUT, "carousel")
os.makedirs(CAR, exist_ok=True)
FONTS = "/home/hatch/workspace/sertiku-poster/fonts"

DARK = (6, 78, 59)        # #064e3b
GREEN = (5, 150, 105)     # #059669
GREEN2 = (4, 120, 87)     # #047857
RIDGE1 = (8, 95, 70)      # mountain back layer on dark bg
MINT = (236, 253, 245)    # #ecfdf5
MINT2 = (209, 250, 229)   # #d1fae5
MINT3 = (167, 243, 208)   # #a7f3d0
WHITE = (255, 255, 255)
INK = (17, 17, 17)
MUTED = (70, 90, 82)
SIZE = 4096
MARGIN = 240

MARK_W = Image.open(os.path.join(OUT, "peka-mark-white.png"))
MARK_D = Image.open(os.path.join(OUT, "peka-mark-dark.png"))


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


XB = lambda s: font("Poppins-ExtraBold.ttf", s)
B = lambda s: font("Poppins-Bold.ttf", s)
SB = lambda s: font("Poppins-SemiBold.ttf", s)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, max_w, leading=1.25):
    lines = wrap(draw, text, fnt, max_w)
    lh = int(fnt.size * leading)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def card(draw, box, fill=WHITE, outline=DARK, width=10, radius=90, shadow=22):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle([x0 + shadow, y0 + shadow, x1 + shadow, y1 + shadow],
                           radius=radius, fill=DARK)
    draw.rounded_rectangle(box, radius=radius, fill=fill,
                           outline=outline, width=width)


def chip(draw, x, y, text, fnt, fg, bg):
    w = int(draw.textlength(text, font=fnt)) + 90
    h = int(fnt.size * 2.1)
    draw.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=bg)
    draw.text((x + 45, y + (h - fnt.size) // 2 - 6), text, font=fnt, fill=fg)
    return w


def lockup(img, draw, dark_bg):
    """White (dark slides) or dark-green (light slides) Peka mark + peka.ai.id."""
    mark = MARK_W if dark_bg else MARK_D
    mh = 150
    mw = int(mh * mark.width / mark.height)
    m = mark.resize((mw, mh), Image.LANCZOS)
    fnt = B(96)
    txt = "peka.ai.id"
    tw = int(draw.textlength(txt, font=fnt))
    x = SIZE - MARGIN - (mw + 28 + tw)
    y = 150
    img.paste(m, (x, y + 4), m)
    draw.text((x + mw + 28, y + (mh - fnt.size) // 2 + 6), txt, font=fnt,
              fill=WHITE if dark_bg else DARK)


def header(img, draw, dark_bg):
    chip(draw, MARGIN, 150, "KONTEN KHUSUS", B(72), WHITE, GREEN)
    lockup(img, draw, dark_bg)


def ridge(draw, points, color):
    poly = [(0, SIZE)] + points + [(SIZE, SIZE)]
    draw.polygon(poly, fill=color)


def mountains(draw):
    ridge(draw, [(0, 3520), (600, 3300), (1300, 3540), (2100, 3250),
                 (2900, 3520), (3600, 3280), (4096, 3500)], RIDGE1)
    ridge(draw, [(0, 3680), (800, 3450), (1700, 3700), (2600, 3420),
                 (3400, 3660), (4096, 3480)], GREEN2)


def footer(draw, text, dark_bg):
    if not dark_bg:
        draw.rectangle([MARGIN, 3830, SIZE - MARGIN, 3838], fill=MINT3)
    draw.text((MARGIN, 3890), text, font=SB(64),
              fill=WHITE if dark_bg else MUTED)


def kicker(draw, y, text):
    draw.text((MARGIN, y), text, font=B(76), fill=GREEN)
    return y + 130


def headline(draw, y, text, fill=INK, size=215, max_w=SIZE - 2 * MARGIN):
    return text_block(draw, MARGIN, y, text, XB(size), fill, max_w, 1.12)


# ---------------------------------------------------------------- slide 1
def slide1():
    img = Image.new("RGB", (SIZE, SIZE), DARK)
    d = ImageDraw.Draw(img)
    mountains(d)
    header(img, d, True)
    y = 780
    d.text((MARGIN, y), "RUTESTRIP", font=XB(430), fill=WHITE)
    y = 1280
    y = text_block(d, MARGIN, y, "Mau mendaki, bingung pilih gunung?",
                   XB(170), MINT3, SIZE - 2 * MARGIN, 1.15)
    y += 60
    y = text_block(d, MARGIN, y,
                   "RuteStrip itu AI yang ngerti gunung. Sistem rekomendasi "
                   "pendakian + chatbot asisten. Tanya jalur, cuaca, sampai "
                   "biaya, dijawab pakai data.",
                   SB(105), WHITE, SIZE - 2 * MARGIN, 1.4)
    box = [MARGIN, 2100, SIZE - MARGIN, 2580]
    d.rounded_rectangle([box[0] + 22, box[1] + 22, box[2] + 22, box[3] + 22],
                        radius=80, fill=(3, 50, 38))
    d.rounded_rectangle(box, radius=80, fill=GREEN)
    d.text((MARGIN + 90, 2190), "COBA SEKARANG", font=XB(92), fill=WHITE)
    text_block(d, MARGIN + 90, 2330,
               "Buka chat RuteStrip, tanya gunung buat pemula.",
               SB(92), WHITE, SIZE - 2 * MARGIN - 180, 1.3)
    # GESER as a proper button pill, clear of the mountain ridge
    pill = [MARGIN, 2680, MARGIN + 660, 2680 + 170]
    d.rounded_rectangle([pill[0] + 14, pill[1] + 14, pill[2] + 14, pill[3] + 14],
                        radius=85, fill=(3, 50, 38))
    d.rounded_rectangle(pill, radius=85, fill=WHITE)
    d.text((MARGIN + 70, 2722), "GESER", font=B(88), fill=DARK)
    ax = MARGIN + 470
    d.polygon([(ax, 2730), (ax, 2800), (ax + 80, 2765)], fill=GREEN)
    d.rectangle([ax - 70, 2755, ax + 10, 2775], fill=GREEN)
    footer(d, "RuteStrip  •  Edisi khusus Peka AI", True)
    img.save(os.path.join(CAR, "slide-01.png"))


# ---------------------------------------------------------------- slide 2
def slide2():
    img = Image.new("RGB", (SIZE, SIZE), MINT)
    d = ImageDraw.Draw(img)
    header(img, d, False)
    y = kicker(d, 420, "MASALAHNYA")
    y = headline(d, y, "Mau mendaki, bingung pilih gunung yang mana?")
    y += 90
    cards = [
        ("Info berserakan",
         "Tiap gunung beda jalur, jarak, elevasi, dan durasi. "
         "Nyari satu-satu capek."),
        ("Spek jalur beda-beda",
         "Yang kelihatan gampang bisa ternyata nanjak terus "
         "tanpa henti."),
        ("Salah pilih, kapok",
         "Pemula butuh jalur yang ramah, bukan yang bikin trauma "
         "di pendakian pertama."),
    ]
    cw = SIZE - 2 * MARGIN
    ch, gap = 660, 70
    for title, body in cards:
        card(d, [MARGIN, y, MARGIN + cw, y + ch])
        blines = wrap(d, body, SB(100), cw - 160)
        content_h = 118 + 50 + len(blines) * 135
        ty = y + (ch - content_h) // 2
        d.text((MARGIN + 80, ty), title, font=XB(118), fill=DARK)
        text_block(d, MARGIN + 80, ty + 118 + 50, body, SB(100), INK, cw - 160, 1.35)
        y += ch + gap
    y += 50
    text_block(d, MARGIN, y, "RuteStrip jawab pakai data, bukan tebak-tebakan.",
               XB(108), GREEN2, cw, 1.25)
    footer(d, "RuteStrip  •  2 / 6", False)
    img.save(os.path.join(CAR, "slide-02.png"))


# ---------------------------------------------------------------- slide 3
def slide3():
    img = Image.new("RGB", (SIZE, SIZE), MINT)
    d = ImageDraw.Draw(img)
    header(img, d, False)
    y = kicker(d, 420, "CARA KERJA")
    y = headline(d, y, "Dari file GPX jadi rekomendasi")
    y += 80
    steps = [
        ("1", "File GPX masuk",
         "Jarak, elevasi, grade, dan durasi Naismith diekstrak dari jalur."),
        ("2", "SBERT ubah jadi angka",
         "Tiap rute diubah jadi embedding 384 dimensi yang paham Bahasa Indonesia."),
        ("3", "Cosine Similarity",
         "Pertanyaan kamu dibandingkan dengan semua rute, dicari yang paling mirip."),
        ("4", "Top-N naik ke atas",
         "Rute paling cocok diurutkan. Yang tidak cocok, tidak dipaksa tampil."),
    ]
    cw = SIZE - 2 * MARGIN
    ch, gap = 560, 55
    for num, title, body in steps:
        card(d, [MARGIN, y, MARGIN + cw, y + ch])
        blines = wrap(d, body, SB(90), cw - 400)
        content_h = 105 + 40 + len(blines) * 117
        ty = y + (ch - content_h) // 2
        d.ellipse([MARGIN + 70, y + (ch - 180) // 2, MARGIN + 250,
                   y + (ch - 180) // 2 + 180], fill=GREEN)
        d.text((MARGIN + 138, y + (ch - 180) // 2 + 26), num, font=XB(120), fill=WHITE)
        d.text((MARGIN + 320, ty), title, font=XB(105), fill=DARK)
        text_block(d, MARGIN + 320, ty + 105 + 40, body, SB(90), INK, cw - 400, 1.3)
        y += ch + gap
    y += 40
    text_block(d, MARGIN, y,
               "Model: paraphrase-multilingual-MiniLM-L12-v2.",
               SB(88), MUTED, cw, 1.3)
    footer(d, "RuteStrip  •  3 / 6", False)
    img.save(os.path.join(CAR, "slide-03.png"))


# ---------------------------------------------------------------- slide 4
def slide4():
    img = Image.new("RGB", (SIZE, SIZE), MINT)
    d = ImageDraw.Draw(img)
    header(img, d, False)
    y = kicker(d, 420, "BUKTI, BUKAN JANJI")
    y = headline(d, y, "Aku sudah coba chatbotnya. Ini hasilnya.")
    y += 80
    qbox = [MARGIN, y, SIZE - MARGIN, y + 330]
    d.rounded_rectangle([qbox[0] + 20, qbox[1] + 20, qbox[2] + 20, qbox[3] + 20],
                        radius=70, fill=DARK)
    d.rounded_rectangle(qbox, radius=70, fill=WHITE, outline=DARK, width=8)
    d.text((MARGIN + 80, y + 55), "AKU TANYA:", font=B(72), fill=GREEN)
    text_block(d, MARGIN + 80, y + 150,
               "Rekomendasi gunung untuk pemula di Jawa Barat.",
               SB(95), INK, SIZE - 2 * MARGIN - 160, 1.3)
    y = qbox[3] + 70
    abox = [MARGIN, y, SIZE - MARGIN, y + 1260]
    card(d, abox, fill=DARK)
    d.text((MARGIN + 80, y + 60), "JAWABAN CHATBOT:", font=B(72), fill=MINT3)
    d.text((MARGIN + 80, y + 170), "Gunung Papandayan", font=XB(150), fill=WHITE)
    text_block(d, MARGIN + 80, y + 360,
               "Top pick buat pemula. Jalurnya bersahabat, ada kawah "
               "dan Hutan Mati yang ikonik.",
               SB(95), (220, 250, 235), SIZE - 2 * MARGIN - 160, 1.35)
    stats = [("1,79 km", "jarak"), ("341 m", "elevasi"),
             ("1,5 jam", "Naismith"), ("Mudah", "sulit")]
    sw = (SIZE - 2 * MARGIN - 160 - 3 * 60) // 4
    sx = MARGIN + 80
    sy = y + 800
    for val, lab in stats:
        d.rounded_rectangle([sx, sy, sx + sw, sy + 330], radius=50, fill=GREEN)
        vw = d.textlength(val, font=XB(88))
        d.text((sx + (sw - vw) / 2, sy + 70), val, font=XB(88), fill=WHITE)
        lw = d.textlength(lab, font=SB(68))
        d.text((sx + (sw - lw) / 2, sy + 200), lab, font=SB(68), fill=WHITE)
        sx += sw + 60
    y = abox[3] + 55
    # runner-up strip
    sbox = [MARGIN, y, SIZE - MARGIN, y + 380]
    card(d, sbox)
    d.text((MARGIN + 80, y + 50), "JUGA DARI JAWABAN YANG SAMA:", font=B(68), fill=GREEN)
    text_block(d, MARGIN + 80, y + 150,
               "Patuha, 1,24 km, 1,1 jam, Mudah. Lembu, 1,92 km, 1,5 jam, Mudah.",
               SB(92), INK, SIZE - 2 * MARGIN - 160, 1.3)
    y = sbox[3] + 45
    text_block(d, MARGIN, y,
               "Diambil dari jawaban asli chatbot, 21 November 2026. "
               "Retrieval 190 ms.",
               SB(84), MUTED, SIZE - 2 * MARGIN, 1.3)
    footer(d, "RuteStrip  •  4 / 6", False)
    img.save(os.path.join(CAR, "slide-04.png"))


# ---------------------------------------------------------------- slide 5
def slide5():
    img = Image.new("RGB", (SIZE, SIZE), MINT)
    d = ImageDraw.Draw(img)
    header(img, d, False)
    y = kicker(d, 420, "CHATBOTNYA")
    y = headline(d, y, "Sekali tanya, semua dijawab")
    y += 80
    cards = [
        ("Rekomendasi jalur",
         "Papandayan, Patuha, Lembu. Dipilih dari data rute, bukan dari iklan."),
        ("Checklist logistik",
         "Air 18 liter buat 3 orang 2 hari, tenda, gas, sampai isi kotak P3K."),
        ("Itinerary + biaya",
         "2 hari 1 malam Papandayan, total sekitar Rp250-300 ribu per orang."),
        ("Cuaca dan survival",
         "Cek cuaca realtime dan panduan bertahan di gunung sebelum berangkat."),
    ]
    cw = SIZE - 2 * MARGIN
    ch, gap = 540, 60
    for title, body in cards:
        card(d, [MARGIN, y, MARGIN + cw, y + ch])
        blines = wrap(d, body, SB(92), cw - 160)
        content_h = 108 + 45 + len(blines) * 124
        ty = y + (ch - content_h) // 2
        d.text((MARGIN + 80, ty), title, font=XB(108), fill=DARK)
        text_block(d, MARGIN + 80, ty + 108 + 45, body, SB(92), INK, cw - 160, 1.35)
        y += ch + gap
    y += 40
    text_block(d, MARGIN, y,
               "Semua contoh di atas dari jawaban asli chatbot yang aku tes.",
               SB(88), MUTED, cw, 1.3)
    footer(d, "RuteStrip  •  5 / 6", False)
    img.save(os.path.join(CAR, "slide-05.png"))


# ---------------------------------------------------------------- slide 6
def slide6():
    img = Image.new("RGB", (SIZE, SIZE), DARK)
    d = ImageDraw.Draw(img)
    mountains(d)
    header(img, d, True)
    y = 800
    y = text_block(d, MARGIN, y, "Coba sendiri, gratis.",
                   XB(210), WHITE, SIZE - 2 * MARGIN, 1.12)
    y += 90
    links = [("WEBSITE", "rutestrip.ai.id", "s.peka.ai.id/TknXVJ"),
             ("CHATBOT", "chat.rutestrip.ai.id", "s.peka.ai.id/gXbVzB")]
    for label, name, short in links:
        box = [MARGIN, y, SIZE - MARGIN, y + 480]
        d.rounded_rectangle([box[0] + 20, box[1] + 20, box[2] + 20, box[3] + 20],
                            radius=70, fill=(3, 50, 38))
        d.rounded_rectangle(box, radius=70, fill=WHITE)
        d.text((MARGIN + 80, y + 55), label, font=B(70), fill=GREEN)
        d.text((MARGIN + 80, y + 150), name, font=XB(120), fill=INK)
        d.text((MARGIN + 80, y + 320), short, font=B(88), fill=GREEN2)
        y += 480 + 55
    y += 60
    y = text_block(d, MARGIN, y, "Gunung mana yang mau kamu daki duluan?",
                   XB(120), MINT3, SIZE - 2 * MARGIN, 1.25)
    y += 70
    text_block(d, MARGIN, y, "Follow @peka.ai.id buat konten AI lainnya.",
               SB(92), WHITE, SIZE - 2 * MARGIN, 1.3)
    footer(d, "RuteStrip  •  Edisi khusus Peka AI", True)
    img.save(os.path.join(CAR, "slide-06.png"))


if __name__ == "__main__":
    slide1(); slide2(); slide3(); slide4(); slide5(); slide6()
    print("done:", sorted(os.listdir(CAR)))
