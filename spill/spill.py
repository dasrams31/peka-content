#!/usr/bin/env python3
"""Peka SPILL series - paper cheat-sheet carousel (4096x4096, 4K).

Format: light paper background, black ink type, yellow marker
highlights, mono accents, rotated SPILL stamp. Deliberately different
from the dark HM news frames and the dark Store cards.

Header keeps the locked Peka lockup spec (cy=95, mascot h=46, gap=12,
text right edge x=1010, 1080-space) but ink-black text for light bg.

Usage: python3 spill.py --out <dir>
"""
import argparse
import os

from PIL import Image, ImageDraw, ImageFont

S = 4096 / 1080
W = H = 4096
PAPER = "#f6f1e6"
INK = "#161616"
YEL = "#ffd60a"
DESC = "#3d3a33"
HAIR = "#d9d1ba"
GRY = "#8a8375"

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FM = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def X(v):
    return int(round(v * S))


def f(sz, bold=True):
    return ImageFont.truetype(FB if bold else FR, X(sz))


def mono(sz, bold=False):
    return ImageFont.truetype(FB if bold else FM, X(sz))


# --- mascot with chroma-key (same source as hm/designer.py) ---
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


def lockup(img, d, cy=95, mh=46):
    cy_px, mh_px = X(cy), X(mh)
    cr = _creature.resize((int(_creature.width * mh_px / _creature.height), mh_px), Image.LANCZOS)
    mr = _cmask.resize(cr.size, Image.LANCZOS)
    tf = f(34)
    label = "peka.ai.id"
    ascent, descent = tf.getmetrics()
    tx = X(1010) - d.textlength(label, font=tf)
    ty = cy_px - (ascent + descent) // 2
    mx = tx - X(12) - cr.width
    my = cy_px - mh_px // 2 - int(mh_px * 0.03)
    img.paste(cr, (int(mx), int(my)), mr)
    d.text((tx, ty), label, font=tf, fill=INK)


def wrap(d, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def stamp(img, x, y, label="SPILL", size=54, angle=4):
    """Rotated outlined stamp, top-left area."""
    layer = Image.new("RGBA", (X(360), X(150)), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    tf = f(size)
    tw = ld.textlength(label, font=tf)
    bw, bh = int(tw + X(44)), X(104)
    ld.rectangle([X(4), X(4), bw, bh], outline=INK, width=X(5))
    ascent, descent = tf.getmetrics()
    ld.text(((bw - tw) / 2, (bh - (ascent + descent)) / 2), label, font=tf, fill=INK)
    layer = layer.crop((0, 0, bw + X(8), bh + X(8))).rotate(angle, expand=True, resample=Image.BICUBIC)
    img.paste(layer, (X(x), X(y)), layer)


def highlight(d, x, y, text, font):
    """Yellow marker bar behind text drawn at (x, y). Returns text width."""
    tw = d.textlength(text, font=font)
    ascent, descent = font.getmetrics()
    d.rectangle([x - X(8), y + X(4), x + tw + X(8), y + ascent + descent - X(2)], fill=YEL)
    d.text((x, y), text, font=font, fill=INK)
    return tw


def header(img, d, page, total=5):
    stamp(img, 56, 44)
    d = ImageDraw.Draw(img)
    lockup(img, d)
    return d


def footer(d, page, total=5):
    y = X(1022)
    d.text((X(70), y), "GABUNG KE KOMUNITAS KAMI: URL.PEKA.AI.ID", font=mono(22), fill=GRY)
    pg = f"{page:02d} / {total:02d}"
    d.text((X(1010) - d.textlength(pg, font=mono(22)), y), pg, font=mono(22), fill=GRY)


def base(page):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d = header(img, d, page)
    return img, d


def skill_table(d, rows, y0):
    """Two-column cheat-sheet table: index + name left, desc right.
    Row height adapts to the taller column so lines never collide."""
    name_f, desc_f, idx_f = f(32), f(28, False), mono(24)
    y = y0
    for i, (name, desc) in enumerate(rows):
        name_lines = wrap(d, name, name_f, X(268))
        desc_lines = wrap(d, desc, desc_f, X(560))
        content_h = max(len(name_lines) * 40, len(desc_lines) * 38)
        if i > 0:
            d.line([X(70), X(y), X(1010), X(y)], fill=HAIR, width=X(2))
        top = y + 12
        d.text((X(70), X(top + 4)), f"{i + 1:02d}", font=idx_f, fill=GRY)
        ny = top
        for ln in name_lines:
            d.text((X(128), X(ny)), ln, font=name_f, fill=INK)
            ny += 40
        dy = top
        for ln in desc_lines:
            d.text((X(432), X(dy)), ln, font=desc_f, fill=DESC)
            dy += 38
        y += 12 + content_h + 12
    return y


def verdict(d, text, y=948):
    d.rectangle([X(70), X(y), X(1010), X(y + 58)], fill=INK)
    size = 27
    tf = f(size)
    while size > 17 and d.textlength(text, font=tf) > X(880):
        size -= 1
        tf = f(size)
    tw = d.textlength(text, font=tf)
    ascent, descent = tf.getmetrics()
    d.text((X(540) - tw / 2, X(y + 29) - (ascent + descent) / 2), text, font=tf, fill=YEL)


def agent_head(d, num, name, tag):
    d.text((X(70), X(158)), f"FILE {num} // AGENT", font=mono(26), fill=GRY)
    nf = f(100)
    d.rectangle([X(70), X(202), X(118), X(214)], fill=YEL)
    d.text((X(70), X(220)), name, font=nf, fill=INK)
    d.text((X(70), X(336)), tag, font=f(32, False), fill=DESC)


# ---------------------------------------------------------------- slides

def slide1(out):
    img, d = base(1)
    d.text((X(70), X(172)), "CONTEKAN PEKA // EDISI AGENT AI", font=mono(26), fill=GRY)
    tf = f(96)
    y = 220
    highlight(d, X(70), X(y), "SKILL AGENT AI", tf)
    y += 116
    d.text((X(70), X(y)), "YANG KEPAKAI", font=tf, fill=INK)
    y += 116
    d.text((X(70), X(y)), "BENERAN", font=tf, fill=INK)
    sub = ("Claude sama Hermes. Dua agent AI yang bisa dipasangin "
           "skill buat ngoding, ngedit dokumen, sampai jalanin tugas otomatis.")
    sy = 584
    for ln in wrap(d, sub, f(30, False), X(930)):
        d.text((X(70), X(sy)), ln, font=f(30, False), fill=DESC)
        sy += 42
    gf = f(28)
    gt = "Geser buat contekan lengkapnya >>>"
    d.text((X(1010) - d.textlength(gt, font=gf), X(724)), gt, font=gf, fill=INK)
    chips = [
        ("CLAUDE", "jago ngoding + dokumen"),
        ("HERMES", "otonom 24/7, belajar sendiri"),
    ]
    cy = 764
    for name, role in chips:
        d.rectangle([X(70), X(cy), X(1010), X(cy + 72)], fill=INK)
        d.text((X(98), X(cy + 17)), name, font=f(34), fill=YEL)
        rf = f(27, False)
        d.text((X(982) - d.textlength(role, font=rf), X(cy + 21)), role, font=rf, fill="#ffffff")
        cy += 88
    footer(d, 1)
    img.save(os.path.join(out, "spill-01.png"))


def slide2(out):
    img, d = base(2)
    d.text((X(70), X(168)), "DASAR DULU // 30 DETIK PAHAM", font=mono(26), fill=GRY)
    tf = f(72)
    highlight(d, X(70), X(206), "Skill itu apa sih?", tf)
    lead = ("Anggap aja skill itu SOP buat agent AI. Satu folder isinya file "
            "SKILL.md: instruksi langkah demi langkah, kadang plus script. "
            "Agent baca cuma pas topiknya relevan, jadi konteks nggak kepenuhan.")
    ly = 322
    for ln in wrap(d, lead, f(30, False), X(930)):
        d.text((X(70), X(ly)), ln, font=f(30, False), fill=DESC)
        ly += 42
    rows = [
        ("SEKALI BIKIN, PAKAI TERUS",
         "Ditulis sekali, dipakai agent berkali-kali. Nggak perlu dijelasin ulang."),
        ("FORMAT TERBUKA",
         "Standar agentskills.io. Satu skill jalan di Claude, Hermes, dan agent lain."),
        ("BISA DARI KOMUNITAS",
         "Nggak harus nulis sendiri. Tinggal install skill bikinan komunitas."),
        ("MAKIN LAMA MAKIN PINTER",
         "Hermes nulis skill sendiri dari pengalaman. Agent lain tinggal diajarin."),
    ]
    skill_table(d, rows, 520)
    footer(d, 2)
    img.save(os.path.join(out, "spill-02.png"))


def slide_agent(out, page, num, name, tag, rows, verdict_text):
    img, d = base(page)
    agent_head(d, num, name, tag)
    skill_table(d, rows, 392)
    verdict(d, verdict_text)
    footer(d, page)
    img.save(os.path.join(out, f"spill-{page:02d}.png"))


def slide6(out):
    img, d = base(5)
    d.text((X(70), X(168)), "PENUTUP // PILIH SENJATA", font=mono(26), fill=GRY)
    tf = f(72)
    highlight(d, X(70), X(206), "Jadi, pilih yang mana?", tf)
    cards = [
        ("Ngoding + dokumen serius", "CLAUDE"),
        ("Asisten 24/7 yang belajar sendiri", "HERMES"),
    ]
    cy = 330
    for need, agent in cards:
        d.rectangle([X(70), X(cy), X(1010), X(cy + 118)], outline=INK, width=X(3))
        d.text((X(98), X(cy + 38)), need, font=f(31, False), fill=DESC)
        af = f(56)
        d.text((X(982) - d.textlength(agent, font=af), X(cy + 26)), agent, font=af, fill=INK)
        cy += 140
    closing = ("Keduanya pakai format skill yang mirip. Belajar satu, sisanya gampang. "
               "Yang penting bukan agent-nya, tapi skill apa yang kamu pasang di dalamnya.")
    ly = cy + 28
    for ln in wrap(d, closing, f(30, False), X(930)):
        d.text((X(70), X(ly)), ln, font=f(30, False), fill=DESC)
        ly += 42
    cf = f(32)
    ct = "Follow @peka.ai.id buat spill AI berikutnya."
    d.text((X(70), X(ly + 24)), ct, font=cf, fill=INK)
    d.text((X(70), X(ly + 68)), "Save postingan ini buat contekan.", font=cf, fill=INK)
    footer(d, 5)
    img.save(os.path.join(out, "spill-05.png"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    slide1(a.out)
    slide2(a.out)
    slide_agent(a.out, 3, "01", "CLAUDE", "Andalan buat ngoding dan dokumen serius", [
        ("DOKUMEN OFFICE",
         "Bikin dan edit Word, Excel, PowerPoint, PDF dari chat. Format tetap rapi."),
        ("CODE REVIEW",
         "Claude Code baca repo kamu di terminal, cari bug, kasih usulan perbaikan."),
        ("FRONTEND DESIGN",
         "Bikin UI web yang nggak generik dan nggak terasa template pasaran."),
        ("TESTING WEB",
         "Jalanin aplikasi otomatis: klik, isi form, screenshot, lapor bug."),
        ("SKILL SENDIRI",
         "Tulis SKILL.md buat workflow tim. Sekali tulis, konsisten seterusnya."),
    ], "Paling matang buat kerja kantoran dan programming harian.")
    slide_agent(a.out, 4, "02", "HERMES", "Agent otonom open source dari Nous Research", [
        ("BELAJAR SENDIRI",
         "Habis tugas berat, Hermes nulis skill sendiri. Tugas serupa jadi lebih cepat."),
        ("MEMORY PERSISTEN",
         "Ingat preferensi dan proyek lintas sesi. Nggak mulai dari nol tiap chat."),
        ("JALAN 24/7",
         "Nginap di VPS: cron, monitoring, laporan otomatis jalan sendiri."),
        ("BANYAK APLIKASI",
         "Telegram, WhatsApp, Discord, Slack, email. Satu otak di semua aplikasi."),
        ("MODEL BEBAS",
         "Claude, GPT, Gemini, sampai model lokal. Ganti provider tanpa ganti agent."),
    ], "Paling otonom. Cocok buat asisten yang kerja terus di belakang layar.")
    slide6(a.out)
    print("done:", sorted(os.listdir(a.out)))


if __name__ == "__main__":
    main()
