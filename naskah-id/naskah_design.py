#!/usr/bin/env python3
"""Editorial carousel for the naskah-id repo spotlight (2026-10-26).

Same fresh paper system as the Hallmark spotlight: warm paper, ink
type, thin rules, mono labels. Square 2048x2048, Peka carousel
convention. Facts verified from the repo README + KONTRAK.md
(2026-10-25): 81 stars, MIT, install via npx skills.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 2048
CREAM = (250, 245, 236)
INK = (20, 20, 20)
GRAY = (110, 105, 95)
HAIRLINE = (210, 203, 188)
AMBER = (232, 163, 76)
COBALT = (43, 79, 224)
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
    d.line([(120, 150), (1928, 150)], fill=HAIRLINE, width=3)
    d.text((120, 185), kicker, font=font("mono_b", 44), fill=INK)
    try:
        p = Image.open("/home/hatch/workspace/peka-logo/mascot-p.png").convert("RGBA")
        p.thumbnail((110, 110))
        d.rounded_rectangle([1560, 170, 1690, 300], radius=30, fill=INK)
        im.paste(p, (1560 + (130 - p.width) // 2, 170 + (130 - p.height) // 2), p)
    except Exception:
        d.rounded_rectangle([1560, 170, 1690, 300], radius=30, fill=INK)
        d.text((1605, 195), "P", font=font("xb", 80), fill=(255, 214, 10))
    d.text((1710, 205), "peka.ai.id", font=font("b", 56), fill=INK)
    d.line([(120, 1900), (1928, 1900)], fill=HAIRLINE, width=3)
    d.text((120, 1930), "GABUNG KE KOMUNITAS KAMI: URL.PEKA.AI.ID",
           font=font("sans", 40), fill=GRAY)
    d.text((1928, 1930), f"HAL {page}/{total}", font=font("sans", 40),
           fill=GRAY, anchor="ra")
    return im, d


def cover(out):
    im, d = base(1, 6, "SKILL BARU DARI KREATOR INDONESIA")
    d.rectangle([120, 420, 260, 436], fill=AMBER)
    y = 500
    for line in ["Naskah Indonesia", "yang nggak", "kedengeran", "terjemahan AI."]:
        d.text((120, y), line, font=font("xb", 175), fill=INK)
        y += 205
    d.text((120, 1380), "Skill agen AI buat nulis dan nyunting karya ilmiah:",
           font=font("sans", 62), fill=INK)
    d.text((120, 1465), "skripsi, tesis, jurnal, proposal hibah.",
           font=font("sans", 62), fill=INK)
    x = 120
    for label in ["81 stars", "MIT"]:
        fnt = font("sb", 54)
        w = int(d.textlength(label, font=fnt)) + 120
        d.rounded_rectangle([x, 1600, x + w, 1720], radius=60,
                            outline=INK, width=4)
        d.text((x + w // 2, 1660), label, font=fnt, fill=INK, anchor="mm")
        x += w + 40
    d.text((120, 1800), "GESER BUAT BEDAHNYA", font=font("mono_b", 52),
           fill=COBALT)
    im.save(out)


def problem(out):
    im, d = base(2, 6, "NASKAH-ID")
    d.text((120, 420), "Kenapa ini beda?", font=font("xb", 150), fill=INK)
    body = ("Naskah Indonesia hasil AI itu gampang ketahuan dari "
            "polanya. Skill ini nyasar lima tanda paling sering "
            "muncul, lalu membetulkannya tanpa mengubah isi:")
    y = 640
    for line in wrap(d, body, font("sans", 62), 1808):
        d.text((120, y), line, font=font("sans", 62), fill=INK)
        y += 90
    items = [
        ("Di era digital ini, tidak dapat dipungkiri bahwa...",
         "pembuka kosmik yang isinya kosong."),
        ("Dari hasil analisis menunjukkan bahwa...",
         "subjek kalimatnya hilang ketimpa kata depan."),
        ("...di mana kelompok tani memainkan peran penting...",
         "perangkai tiruan bahasa Inggris, harusnya tempat dan berperan."),
    ]
    y = 1080
    for quote, note in items:
        d.rectangle([120, y, 136, y + 130], fill=AMBER)
        for line in wrap(d, quote, font("sb", 54), 1650):
            d.text((180, y), line, font=font("sb", 54), fill=INK)
            y += 80
        for line in wrap(d, note, font("sans", 50), 1650):
            d.text((180, y), line, font=font("sans", 50), fill=GRAY)
            y += 72
        y += 50
    im.save(out)


def what(out):
    im, d = base(3, 6, "NASKAH-ID")
    d.text((120, 420), "Yang dikerjain", font=font("xb", 150), fill=INK)
    items = [
        ("01", "Nulis dan nyunting karya ilmiah",
         "Skripsi, tesis, artikel jurnal, proposal hibah, dan "
         "laporan penelitian, dari bahan yang kamu berikan."),
        ("02", "Ejaan ikut EYD V dan KBBI",
         "Kata baku dan tanda baca dibetulkan, kalimat disusun "
         "ulang tanpa menggeser makna."),
        ("03", "Angka dan sitasi tidak diubah",
         "Hasil, angka, dan rujukanmu aman saat disunting. "
         "Klaim tanpa bukti ditulis apa adanya, bukan dibumbui."),
    ]
    y = 680
    for num, title, desc in items:
        d.text((120, y), num, font=font("mono_b", 64), fill=AMBER)
        d.text((300, y), title, font=font("b", 68), fill=INK)
        y += 108
        for line in wrap(d, desc, font("sans", 56), 1628):
            d.text((300, y), line, font=font("sans", 56), fill=GRAY)
            y += 82
        y += 70
    im.save(out)


def guardrails(out):
    im, d = base(4, 6, "NASKAH-ID")
    d.text((120, 420), "Proteksinya", font=font("xb", 150), fill=INK)
    d.text((120, 600), "Agen yang pakai skill ini terikat kontrak 10 pasal:",
           font=font("sans", 58), fill=GRAY)
    items = [
        ("Nggak ngarang data atau rujukan",
         "Yang belum terverifikasi ditulis [PERLU RUJUKAN], "
         "bukan dikarang biar kelihatan meyakinkan."),
        ("Nolak joki skripsi utuh",
         "Menulis tugas utuh buat diserahkan sebagai karya sendiri "
         "ditolak. Begitu juga permintaan nyamarin hasil AI."),
        ("Penulis tetap manusia",
         "AI nggak dicantumkan sebagai penulis. Kamu menanggung "
         "seluruh isi naskah, plus draf pernyataan pemakaian AI."),
    ]
    y = 760
    for title, desc in items:
        d.ellipse([120, y + 12, 160, y + 52], fill=AMBER)
        d.text((200, y), title, font=font("b", 64), fill=INK)
        y += 100
        for line in wrap(d, desc, font("sans", 54), 1628):
            d.text((200, y), line, font=font("sans", 54), fill=GRAY)
            y += 78
        y += 60
    im.save(out)


def install(out):
    im, d = base(5, 6, "NASKAH-ID")
    d.text((120, 420), "Cobain sendiri", font=font("xb", 150), fill=INK)
    d.rounded_rectangle([120, 660, 1928, 900], radius=36, fill=DARK)
    d.text((180, 735), "npx skills add nothinx/naskah-id -g",
           font=font("mono_b", 60), fill=(250, 245, 236))
    d.text((120, 1000), "Gratis, lisensi MIT. Buat Claude Code, Codex,",
           font=font("sans", 62), fill=INK)
    d.text((120, 1090), "Cursor, dan banyak agen lain. Butuh Node 18+.",
           font=font("sans", 62), fill=INK)
    d.rectangle([120, 1300, 260, 1316], fill=AMBER)
    d.text((120, 1360), "Kalimat AI apa yang paling sering kamu temui",
           font=font("b", 62), fill=INK)
    d.text((120, 1450), "di naskah? Ceritain di komentar.",
           font=font("b", 62), fill=INK)
    d.text((120, 1620), "Link repo lengkap ada di komentar.",
           font=font("sans", 58), fill=COBALT)
    im.save(out)


def follow(out):
    im, d = base(6, 6, "NASKAH-ID")
    d.text((120, 420), "Follow dan gabung.", font=font("xb", 150), fill=INK)
    d.rectangle([120, 640, 260, 656], fill=AMBER)
    items = [
        "Follow @peka.ai.id di Instagram, Threads, dan TikTok.",
        "Gabung grup WhatsApp Peka AI lewat url.peka.ai.id.",
        "Save dan share postingan ini biar makin banyak yang kebantu.",
    ]
    y = 760
    for text in items:
        for line in wrap(d, text, font("sans", 62), 1808):
            d.text((120, y), line, font=font("sans", 62), fill=INK)
            y += 90
        y += 60
    im.save(out)


if __name__ == "__main__":
    import os
    out_dir = "/home/hatch/workspace/peka-content/naskah-id/out/2026-10-26"
    os.makedirs(out_dir, exist_ok=True)
    cover(f"{out_dir}/naskah-01.png")
    problem(f"{out_dir}/naskah-02.png")
    what(f"{out_dir}/naskah-03.png")
    guardrails(f"{out_dir}/naskah-04.png")
    install(f"{out_dir}/naskah-05.png")
    follow(f"{out_dir}/naskah-06.png")
    print("done", out_dir)
