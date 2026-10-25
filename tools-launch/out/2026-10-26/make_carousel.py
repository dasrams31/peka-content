#!/usr/bin/env python3
"""Carousel pengumuman tools.peka.ai.id: 6 slide 2048x2048, gaya brand Peka."""
from PIL import Image, ImageDraw, ImageFont

W, H = 2048, 2048
BG = (17, 17, 17)
YEL = (255, 214, 10)
CREAM = (245, 241, 230)
MUT = (163, 158, 143)
DIM = (143, 138, 125)
CARD = (27, 27, 27)
LINE = (255, 255, 255, 23)
FONT_DIR = "/home/hatch/workspace/sertiku-poster/fonts/"
MASCOT = "/home/hatch/workspace/peka-logo/mascot-p.png"
OUT = "/home/hatch/workspace/peka-content/tools-launch/out/2026-10-26"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


XB = lambda s: font("Poppins-ExtraBold.ttf", s)
B = lambda s: font("Poppins-Bold.ttf", s)
SB = lambda s: font("Poppins-SemiBold.ttf", s)
DV = lambda s: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", s)
DVB = lambda s: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", s)


def wrap(draw, text, f, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=f) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def base(page_no):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.line([(140, 150), (W - 140, 150)], fill=(58, 58, 58), width=3)
    # badge kiri
    badge = "PEKA TOOLS"
    fb = DVB(44)
    bw = d.textlength(badge, font=fb) + 70
    d.rounded_rectangle([140, 195, 140 + bw, 195 + 88], radius=16, fill=YEL)
    d.text((140 + 35, 195 + 20), badge, font=fb, fill=BG)
    # lockup kanan: chip hitam + maskot + teks
    mascot = Image.open(MASCOT).convert("RGBA").resize((104, 104))
    chip_x = W - 140 - 104 - 36 - d.textlength("peka.ai.id", font=B(52)) - 30
    d.rounded_rectangle([chip_x - 20, 190, W - 140 + 20, 190 + 116], radius=24, fill=(0, 0, 0))
    img.paste(mascot, (W - 140 - 104, 196), mascot)
    d.text((chip_x + 10, 218), "peka.ai.id", font=B(52), fill=YEL)
    # footer
    d.text((140, H - 150), "GABUNG KE KOMUNITAS KAMI: URL.PEKA.AI.ID", font=DV(34), fill=DIM)
    d.text((W - 140 - d.textlength(str(page_no), font=DVB(40)), H - 152), str(page_no), font=DVB(40), fill=MUT)
    return img, d


def headline(d, lines, y, size=168):
    for ln in lines:
        d.text((140, y), ln, font=XB(size), fill=CREAM)
        y += size + 18
    return y


def sub(d, text, y, max_w=W - 280, size=66):
    for ln in wrap(d, text, DV(size), max_w):
        d.text((140, y), ln, font=DV(size), fill=MUT)
        y += size + 26
    return y


def stat_row(d, y, items):
    # items: list of (big, small); 3 kolom
    x0, gap = 140, 60
    col_w = (W - 280 - gap * 2) // 3
    for i, (big, small) in enumerate(items):
        x = x0 + i * (col_w + gap)
        d.rounded_rectangle([x, y, x + col_w, y + 300], radius=28, fill=CARD)
        d.text((x + 44, y + 40), big, font=XB(104), fill=YEL)
        d.text((x + 44, y + 190), small, font=SB(44), fill=CREAM)
    return y + 300


def rows(d, y, items, row_h=172):
    for title, desc in items:
        d.line([(140, y + row_h - 2), (W - 140, y + row_h - 2)], fill=(255, 255, 255, 23), width=2)
        d.text((140, y + 18), title, font=B(64), fill=CREAM)
        tw = d.textlength(title, font=B(64))
        d.text((140, y + 96), desc, font=DV(46), fill=MUT)
        y += row_h
    return y


def url_chip(d, y, text="tools.peka.ai.id"):
    f = B(64)
    w = d.textlength(text, font=f) + 90
    d.rounded_rectangle([140, y, 140 + w, y + 120], radius=20, fill=YEL)
    d.text((140 + 45, y + 28), text, font=f, fill=BG)
    return y + 120


# ---- slide 1: cover ----
img, d = base(1)
y = headline(d, ["86 tools AI", "open source,", "tinggal pakai."], 430, 178)
y = sub(d, "Direktori gratis pilihan Peka. Udah diringkas Bahasa Indonesia, udah dicek langsung ke GitHub-nya.", y + 40)
y = stat_row(d, y + 60, [("86", "tools"), ("8", "kategori"), ("0", "rupiah")])
url_chip(d, y + 70)
img.save(f"{OUT}/tools-01.png")

# ---- slide 2: apa itu ----
img, d = base(2)
y = headline(d, ["Bukan sekadar", "daftar link."], 430, 168)
y = sub(d, "Tiap repo di Peka Tools udah diringkas Bahasa Indonesia dan dicek langsung ke GitHub-nya. Lengkap sama bintang, fork, bahasa, sama lisensi.", y + 40)
y = rows(d, y + 60, [
    ("Ringkasan jujur", "Ditulis dari repo aslinya, tanpa klaim yang nggak terbukti."),
    ("Angka dari GitHub", "Bintang dan fork diambil pas data disusun."),
    ("Gratis, tanpa daftar", "Buka, cari, simpan bookmark, langsung pakai."),
])
img.save(f"{OUT}/tools-02.png")

# ---- slide 3: 8 kategori ----
img, d = base(3)
y = headline(d, ["8 kategori,", "satu tempat."], 430, 168)
y = rows(d, y + 50, [
    ("Claude  23", "Skill, CLI, sama template buat Claude Code."),
    ("OpenCode  17", "Plugin, TUI, sama perkakas OpenCode."),
    ("OpenClaw  14", "Asisten, skill, sama registry OpenClaw."),
    ("Hermes  13", "Agen, plugin, sama desktop Hermes."),
    ("Codex  11", "CLI sama perkakas ekosistem Codex."),
    ("Antigravity  5  ·  Desain  1  ·  Buatan Peka  2", "Plus skill Antigravity sama tools buatan Peka."),
], row_h=168)
img.save(f"{OUT}/tools-03.png")

# ---- slide 4: fitur ----
img, d = base(4)
y = headline(d, ["Cari, saring,", "simpan, usulkan."], 430, 168)
y = rows(d, y + 50, [
    ("Cari cepat", "Ketik kata kunci, atau tekan tombol / di keyboard."),
    ("Filter kategori dan bahasa", "Persempit hasil sesuai kebutuhan kamu."),
    ("Urut sesukamu", "Peringkat, nama A-Z, atau terbaru."),
    ("Bookmark tanpa daftar", "Tersimpan di browser, nggak perlu daftar."),
    ("Usulkan repo", "Nemu repo bagus? Usulin, nanti direview admin."),
])
img.save(f"{OUT}/tools-04.png")

# ---- slide 5: 58 baru ----
img, d = base(5)
y = headline(d, ["Baru: 58 tools", "agen AI."], 430, 168)
y = sub(d, "Kurasi terbaru dari ekosistem agen AI yang lagi naik daun. Ini sebagian contohnya:", y + 40)
y = rows(d, y + 50, [
    ("openai/codex", "Coding agent terminal resmi dari OpenAI."),
    ("anthropics/claude-code", "Coding agent terminal resmi dari Anthropic."),
    ("openclaw/openclaw", "Asisten AI self-hosted yang beneran bertindak."),
    ("obra/superpowers", "Framework skill dan metodologi untuk coding agent."),
    ("openclaw/clawhub", "Registry resmi skill dan plugin OpenClaw."),
], row_h=150)
img.save(f"{OUT}/tools-05.png")

# ---- slide 6: penutup follow ----
img, d = base(6)
y = headline(d, ["Mampir,", "terus simpan."], 430, 178)
y = sub(d, "Semua tools di atas bisa langsung dibuka dan dipakai gratis. Nggak perlu daftar, nggak perlu bayar.", y + 40)
y = url_chip(d, y + 60)
y = sub(d, "Follow @peka.ai.id biar nggak ketinggalan edisi baru. Gabung komunitas lewat url.peka.ai.id. Save dan share postingan ini kalo berguna.", y + 70, size=62)
img.save(f"{OUT}/tools-06.png")
print("done 6 slides")
