#!/usr/bin/env python3
"""Fresh editorial carousel for the Hallmark repo spotlight (2026-10-25).

Palette inspired by Hallmark's own theme screenshots (Dusk warmth +
Cobalt mono details), deliberately different from the standard Peka
yellow/black carousel: warm paper, ink type, thin rules, mono labels.
Square 2048x2048 to match the Peka carousel convention.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 2048
CREAM = (250, 245, 236)
INK = (20, 20, 20)
GRAY = (110, 105, 95)
HAIRLINE = (210, 203, 188)
AMBER = (232, 163, 76)
COBALT = (43, 79, 224)
CARD = (255, 252, 246)
DARK = (24, 24, 24)

FONT_DIR = "/home/hatch/workspace/sertiku-poster/fonts"
DEJAVU = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    paths = {
        "xb": f"{FONT_DIR}/Poppins-ExtraBold.ttf",
        "b": f"{FONT_DIR}/Poppins-Bold.ttf",
        "sb": f"{FONT_DIR}/Poppins-SemiBold.ttf",
        "sans": f"{DEJAVU}/DejaVuSans.ttf",
        "mono": f"{DEJAVU}/DejaVuSansMono.ttf",
        "mono_b": f"{DEJAVU}/DejaVuSansMono-Bold.ttf",
    }
    return ImageFont.truetype(paths[name], size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def base(page, total, kicker):
    im = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(im)
    # top rule + kicker + lockup
    d.line([(120, 150), (1928, 150)], fill=HAIRLINE, width=3)
    d.text((120, 185), kicker, font=font("mono_b", 44), fill=INK)
    # lockup: black chip + mascot P + peka.ai.id
    try:
        p = Image.open("/home/hatch/workspace/peka-logo/mascot-p.png").convert("RGBA")
        p.thumbnail((110, 110))
        d.rounded_rectangle([1560, 170, 1690, 300], radius=30, fill=INK)
        im.paste(p, (1560 + (130 - p.width) // 2, 170 + (130 - p.height) // 2), p)
    except Exception:
        d.rounded_rectangle([1560, 170, 1690, 300], radius=30, fill=INK)
        d.text((1605, 195), "P", font=font("xb", 80), fill=(255, 214, 10))
    d.text((1710, 205), "peka.ai.id", font=font("b", 56), fill=INK)
    # footer (locked community line, gray, one tone)
    d.line([(120, 1900), (1928, 1900)], fill=HAIRLINE, width=3)
    d.text((120, 1930), "GABUNG KE KOMUNITAS KAMI: URL.PEKA.AI.ID",
           font=font("sans", 40), fill=GRAY)
    d.text((1928, 1930), f"HAL {page}/{total}", font=font("sans", 40),
           fill=GRAY, anchor="ra")
    return im, d


def cover(out):
    im, d = base(1, 5, "TRENDING GITHUB HARI INI")
    d.rectangle([120, 420, 260, 436], fill=AMBER)
    y = 500
    for line in ["Desain AI yang", "nggak kelihatan", "buatan mesin."]:
        d.text((120, y), line, font=font("xb", 185), fill=INK)
        y += 215
    d.text((120, 1210), "Hallmark, skill desain buat Claude Code, Cursor,",
           font=font("sans", 62), fill=INK)
    d.text((120, 1295), "Codex, dan OpenCode.",
           font=font("sans", 62), fill=INK)
    # badges: pill width hugs its text (same height, even padding),
    # so a short label like MIT does not sit in an oversized oval.
    x = 120
    for label in ["32,7rb stars", "MIT"]:
        fnt = font("sb", 54)
        w = int(d.textlength(label, font=fnt)) + 120
        d.rounded_rectangle([x, 1440, x + w, 1560], radius=60,
                            outline=INK, width=4)
        d.text((x + w // 2, 1500), label, font=fnt, fill=INK, anchor="mm")
        x += w + 40
    d.text((120, 1700), "GESER BUAT BEDAHNYA", font=font("mono_b", 52),
           fill=COBALT)
    im.save(out)


def why(out):
    im, d = base(2, 5, "HALLMARK")
    d.text((120, 420), "Kenapa ini beda?", font=font("xb", 150), fill=INK)
    body = ("Hasil AI itu gampang ketahuan dari polanya: label kapital "
            "di atas tiap judul, satu kata warna-warni di headline, "
            "hero kosong, dan form yang bilang makasih tanpa ngirim "
            "apa-apa. Hallmark nolak semua itu dari awal, jadi "
            "halamannya terasa dibuat manusia, bukan mesin.")
    y = 680
    for line in wrap(d, body, font("sans", 66), 1808):
        d.text((120, y), line, font=font("sans", 66), fill=INK)
        y += 95
    d.rectangle([120, 1420, 260, 1436], fill=AMBER)
    d.text((120, 1480), "Bukan template. Tiap build dibikin dari job-nya:",
           font=font("sb", 58), fill=INK)
    d.text((120, 1570), "halaman booking ya buat booking, toko ya buat jualan.",
           font=font("sans", 58), fill=GRAY)
    im.save(out)


def features(out):
    im, d = base(3, 5, "HALLMARK")
    d.text((120, 420), "Tiga hal yang bikin beda", font=font("xb", 130),
           fill=INK)
    items = [
        ("01", "48 tema material",
         "Tiap tema itu material lengkap: kertas, tipografi, warna, "
         "dan komponennya sendiri. Bukan sekadar ganti warna."),
        ("02", "Sloplint di browser asli",
         "Hasilnya dicek di 8 lebar layar sebelum dikirim, lalu "
         "direview ulang dengan mata segar."),
        ("03", "Redesign tanpa merusak",
         "/hallmark redesign rebuild halaman tapi konten dan wiring "
         "tetap utuh. Audit saja juga bisa, tanpa mengubah apa-apa."),
    ]
    y = 680
    for num, title, desc in items:
        d.text((120, y), num, font=font("mono_b", 64), fill=AMBER)
        d.text((300, y), title, font=font("b", 72), fill=INK)
        y += 110
        for line in wrap(d, desc, font("sans", 56), 1628):
            d.text((300, y), line, font=font("sans", 56), fill=GRAY)
            y += 82
        y += 70
    im.save(out)


def examples(out, shot_dusk, shot_cobalt):
    im, d = base(4, 5, "HALLMARK")
    d.text((120, 420), "Contoh hasilnya", font=font("xb", 150), fill=INK)
    d.text((120, 600), "Dua halaman dari katalog tema Hallmark:",
           font=font("sans", 58), fill=GRAY)
    shots = [(shot_dusk, "Tema Dusk: Closewise,",
              "rekonsiliasi bank"),
             (shot_cobalt, "Tema Cobalt: Relay,",
              "API webhook")]
    x = 120
    for path, label1, label2 in shots:
        shot = Image.open(path).convert("RGB")
        shot = shot.resize((880, 550))
        im.paste(shot, (x, 760))
        d.rectangle([x, 760, x + 880, 1310], outline=HAIRLINE, width=3)
        d.text((x, 1350), label1, font=font("sb", 52), fill=INK)
        d.text((x, 1430), label2, font=font("sb", 52), fill=INK)
        x += 948
    d.text((120, 1620), "Dua tema, dua produk, dua rasa yang beda jauh.",
           font=font("sans", 58), fill=INK)
    d.text((120, 1710), "Itu yang dimaksud material, bukan template.",
           font=font("sans", 58), fill=INK)
    im.save(out)


def install(out):
    im, d = base(5, 5, "HALLMARK")
    d.text((120, 420), "Cobain sendiri", font=font("xb", 150), fill=INK)
    d.rounded_rectangle([120, 660, 1928, 900], radius=36, fill=DARK)
    d.text((180, 735), "npx skills add nutlope/hallmark -g",
           font=font("mono_b", 62), fill=(250, 245, 236))
    d.text((120, 1000), "Gratis, lisensi MIT. Buat Claude Code, Cursor,",
           font=font("sans", 62), fill=INK)
    d.text((120, 1090), "Codex, dan OpenCode. Butuh Node 18+.",
           font=font("sans", 62), fill=INK)
    d.rectangle([120, 1300, 260, 1316], fill=AMBER)
    d.text((120, 1360), "Hasil AI kamu paling ketahuan slop di bagian apa?",
           font=font("b", 62), fill=INK)
    d.text((120, 1450), "Ceritain di komentar.",
           font=font("sans", 62), fill=GRAY)
    d.text((120, 1620), "Link repo lengkap ada di komentar.",
           font=font("sans", 58), fill=COBALT)
    im.save(out)


if __name__ == "__main__":
    import os
    out_dir = "/home/hatch/workspace/peka-content/hallmark/out/2026-10-25"
    os.makedirs(out_dir, exist_ok=True)
    cover(f"{out_dir}/hallmark-01.png")
    why(f"{out_dir}/hallmark-02.png")
    features(f"{out_dir}/hallmark-03.png")
    examples(f"{out_dir}/hallmark-04.png",
             f"{out_dir}/shot-dusk-closewise.jpg",
             f"{out_dir}/shot-cobalt-relay.jpg")
    install(f"{out_dir}/hallmark-05.png")
    print("done", out_dir)
