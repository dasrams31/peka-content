#!/usr/bin/env python3
"""PekaAI Virtual Office announcement carousel (special edition).

Spec-sheet style matching virtual.peka.ai.id: paper background, ink frame,
yellow accents, mono labels. 4 slides, 1600x1600.
Copy rules: no em dash, no en dash; clause separators use colons.
"""
from PIL import Image, ImageDraw, ImageFont
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "out")
ASSETS = os.path.join(BASE, "assets")
os.makedirs(OUT, exist_ok=True)

S = 1600
PAPER = (243, 243, 240)
INK = (17, 17, 17)
YELLOW = (255, 214, 10)
GREY = (110, 110, 102)
HAIR = (216, 216, 208)
WHITE = (255, 255, 255)

POP_XB = "/home/hatch/workspace/sertiku-poster/fonts/Poppins-ExtraBold.ttf"
POP_B = "/home/hatch/workspace/sertiku-poster/fonts/Poppins-Bold.ttf"
POP_SB = "/home/hatch/workspace/sertiku-poster/fonts/Poppins-SemiBold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

MASCOT = "/home/hatch/workspace/peka-logo/mascot-p.png"
SCENE = os.path.join(ASSETS, "scene.png")

_cache = {}
def F(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]

def wrap(d, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text_block(d, x, y, text, font, fill, max_w, leading=1.18):
    lines = wrap(d, text, font, max_w)
    asc, desc = font.getmetrics()
    lh = int((asc + desc) * leading)
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y

def base(page):
    img = Image.new("RGB", (S, S), PAPER)
    d = ImageDraw.Draw(img)
    # faint graph paper grid
    for gx in range(0, S + 1, 100):
        d.line([(gx, 0), (gx, S)], fill=(233, 233, 227), width=1)
        d.line([(0, gx), (S, gx)], fill=(233, 233, 227), width=1)
    # ink frame
    d.rectangle([34, 34, S - 34, S - 34], outline=INK, width=3)
    # header: badge left
    bx, by = 72, 66
    bf = F(MONO_B, 30)
    label = "KANTOR VIRTUAL"
    tw = d.textlength(label, font=bf)
    d.rounded_rectangle([bx, by, bx + tw + 44, by + 52], radius=26, fill=YELLOW, outline=INK, width=2)
    d.text((bx + 22, by + 9), label, font=bf, fill=INK)
    # lockup right: mascot + peka.ai.id
    mascot = Image.open(MASCOT).convert("RGBA")
    mh = 58
    mascot = mascot.resize((int(mascot.width * mh / mascot.height), mh))
    lf = F(POP_B, 42)
    lt = "peka.ai.id"
    ltw = d.textlength(lt, font=lf)
    total = mascot.width + 14 + ltw
    lx = S - 72 - total
    img.paste(mascot, (int(lx), 62), mascot)
    d.text((lx + mascot.width + 14, 68), lt, font=lf, fill=INK)
    # footer
    ff = F(MONO, 24)
    d.text((72, S - 108), "GABUNG KE KOMUNITAS KAMI: URL.PEKA.AI.ID", font=ff, fill=GREY)
    pg = f"{page:02d} / 04"
    pw = d.textlength(pg, font=ff)
    d.text((S - 72 - pw, S - 108), pg, font=ff, fill=GREY)
    return img, d

def scene_band(img, y, h, focus_y=0.42):
    """Paste the office scene as a full-bleed band inside the frame."""
    sc = Image.open(SCENE).convert("RGB")
    target_w = S - 72 * 2
    scale = target_w / sc.width
    new_h = int(sc.height * scale)
    sc = sc.resize((target_w, new_h))
    if new_h > h:
        top = int((new_h - h) * focus_y)
        sc = sc.crop((0, top, target_w, top + h))
    img.paste(sc, (72, y))
    d = ImageDraw.Draw(img)
    d.rectangle([72, y, 72 + target_w, y + h], outline=INK, width=3)
    return y + h

def kicker(d, y, text):
    d.text((72, y), text, font=F(MONO_B, 27), fill=GREY)
    return y + 48

MX = 72
CW = S - 2 * MX  # content width

# ---------------------------------------------------------------- slide 1
img, d = base(1)
y = kicker(d, 168, "PENGUMUMAN · SUDAH LIVE HARI INI")
y = text_block(d, MX, y + 6, "PekaAI sekarang punya kantor.", F(POP_XB, 104), INK, CW, 1.08)
y = text_block(d, MX, y + 26,
               "Kantor virtual 3D yang bisa kamu intip kapan aja. Yang kerja di "
               "dalamnya beneran: mereka yang ngerjain berita, prompt, dan konten "
               "PekaAI tiap hari.",
               F(SANS, 37), (52, 52, 48), CW, 1.3)
y = scene_band(img, y + 44, 560, focus_y=0.30)
# black strip like the in-office banner
d.rectangle([72, y + 40, S - 72, y + 116], fill=INK)
strip = "VIRTUAL.PEKA.AI.ID : BUKA 24 JAM"
sf = F(MONO_B, 40)
sw = d.textlength(strip, font=sf)
d.text(((S - sw) / 2, y + 56), strip, font=sf, fill=YELLOW)
img.save(os.path.join(OUT, "slide-1.png"))

# ---------------------------------------------------------------- slide 2
img, d = base(2)
y = kicker(d, 168, "ISI KANTORNYA")
y = text_block(d, MX, y + 6, "18 staf AI. 11 divisi. 1 kantor.", F(POP_XB, 88), INK, CW, 1.1)
divs = [
    ("00", "Direksi", "Dipa + Megumi"),
    ("01", "Redaksi", "Prita, Panji, Pipo"),
    ("02", "Sosial Media", "Pasha, Pungki"),
    ("03", "Bansos", "Pegi, Panca"),
    ("04", "Blog & SEO", "Peni, Pio"),
    ("05", "Prompt", "Prama"),
    ("06", "Store", "Puspa"),
    ("07", "Riset", "Pandu"),
    ("08", "Marketing", "Pita"),
    ("09", "Produk & Web", "Pixo"),
    ("10", "Infrastruktur", "Piko, Satria"),
]
col_w = (CW - 60) // 2
row_h = 118
top = y + 58
nf, df, sf2 = F(MONO_B, 34), F(POP_SB, 40), F(SANS, 30)
for i, (num, name, staff) in enumerate(divs):
    cx = MX + (i % 2) * (col_w + 60)
    cy = top + (i // 2) * row_h
    d.rounded_rectangle([cx, cy + 4, cx + 62, cy + 52], radius=8, fill=YELLOW, outline=INK, width=2)
    d.text((cx + 11, cy + 11), num, font=F(MONO_B, 28), fill=INK)
    d.text((cx + 82, cy), name, font=df, fill=INK)
    d.text((cx + 82, cy + 56), staff, font=sf2, fill=GREY)
rows = (len(divs) + 1) // 2
y = top + rows * row_h + 30
d.line([MX, y, S - MX, y], fill=HAIR, width=2)
y = text_block(d, MX, y + 34,
               "Lengkap pakai lounge, pantry, ruang meeting, dan resepsi. "
               "Satria si satpam patroli keliling area depan, beneran jalan.",
               F(SANS, 37), (52, 52, 48), CW, 1.3)
img.save(os.path.join(OUT, "slide-2.png"))

# ---------------------------------------------------------------- slide 3
img, d = base(3)
y = kicker(d, 168, "CARA KERJANYA")
y = text_block(d, MX, y + 6, "Statusnya ngikutin jam kerja asli.", F(POP_XB, 84), INK, CW, 1.1)
statuses = [
    ("BEKERJA", INK, YELLOW, "di meja, ngerjain edisi yang lagi tayang"),
    ("SIAGA", (140, 110, 0), None, "keliling area kantor, siap giliran berikutnya"),
    ("SANTAI", GREY, None, "istirahat ke lounge atau pantry"),
    ("LIBUR", (170, 170, 162), None, "di luar jamnya, kursinya kosong"),
]
sy = y + 52
for name, dot, chipfill, desc in statuses:
    d.ellipse([MX + 4, sy + 14, MX + 30, sy + 40], fill=dot)
    d.text((MX + 52, sy), name, font=F(MONO_B, 40), fill=INK)
    nw = d.textlength(name, font=F(MONO_B, 40))
    d.text((MX + 52 + nw + 28, sy + 6), ": " + desc, font=F(SANS, 33), fill=(52, 52, 48))
    sy += 92
sy += 26
d.line([MX, sy, S - MX, sy], fill=HAIR, width=2)
sy += 40
d.text((MX, sy), "JADWAL HARIAN KANTOR (WIB)", font=F(MONO_B, 30), fill=GREY)
sy += 62
sched = [
    ("09:36", "Redaksi rilis berita AI hari ini"),
    ("12:30", "Prama kirim Prompt Harian"),
    ("19:00", "Puspa buka PekaAI Store"),
    ("21:30", "Pandu spill repo GitHub pilihan"),
    ("24 JAM", "Piko jaga server, backup, dan tunnel"),
]
for t, what in sched:
    d.text((MX, sy), t, font=F(MONO_B, 38), fill=INK)
    d.text((MX + 240, sy + 3), what, font=F(SANS, 35), fill=(52, 52, 48))
    sy += 76
img.save(os.path.join(OUT, "slide-3.png"))

# ---------------------------------------------------------------- slide 4
img, d = base(4)
y = kicker(d, 168, "MAMPIR SEKARANG")
y = text_block(d, MX, y + 6, "Mampir. Kantornya buka terus.", F(POP_XB, 88), INK, CW, 1.1)
y = text_block(d, MX, y + 28,
               "Nggak perlu janji temu, nggak perlu izin satpam. Klik nama stafnya "
               "buat lihat dia lagi ngapain: lagi fokus di meja, lagi rapat, atau "
               "lagi santai di lounge.",
               F(SANS, 37), (52, 52, 48), CW, 1.3)
# big yellow address block
by = y + 52
d.rectangle([MX, by, S - MX, by + 190], fill=YELLOW, outline=INK, width=3)
addr = "virtual.peka.ai.id"
af = F(POP_XB, 96)
aw = d.textlength(addr, font=af)
d.text(((S - aw) / 2, by + 38), addr, font=af, fill=INK)
y = scene_band(img, by + 190 + 48, 430, focus_y=0.05)
text_block(d, MX, y + 34, "Bisa dibuka dari HP. Datanya ngikutin jam WIB, jadi datang jam berapa pun selalu ada cerita.",
           F(SANS, 32), GREY, CW, 1.3)
img.save(os.path.join(OUT, "slide-4.png"))

print("slides written to", OUT)
