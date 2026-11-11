#!/usr/bin/env python3
"""Claude Fable 5.2 special edition - carousel designer (6 slides, 4096x4096).

Special dark "benchmark lab" theme: deep charcoal/navy, Peka yellow accents,
high data density, no gradients, no theme name printed on the design.
Bar charts are the hero: one bar group per model, exact value at the end of
each bar, model names clear, 0-100 scale implied by bar length.
Color legend is identical on every chart slide:
  Fable 5.2 = Peka yellow, Fable 5.1 = light grey, Opus 5.5 = white/slate,
  GPT-6 Astra = blue, Gemini 4 Carbon = green/teal.
All benchmark numbers are Anthropic vendor-reported (see footnote on slides),
exact values from the 9 Nov 2026 announcement.
"""
import os

from PIL import Image, ImageDraw, ImageFont

OUT = os.path.dirname(os.path.abspath(__file__))
S = 4096 / 1080
W = H = 4096

BG = "#0C1220"
PANEL = "#141C2E"
PANEL_LINE = "#26324A"
YEL = "#FFD60A"
WHT = "#F5F7FA"
MUT = "#9AA7BD"
DIM = "#5B6B85"

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FM = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

MODEL_COLORS = {
    "Claude Fable 5.2": YEL,
    "Claude Fable 5.1": "#8A99B5",
    "Claude Opus 5.5": "#E8EDF5",
    "GPT-6 Astra": "#38BDF8",
    "Gemini 4 Carbon": "#34D399",
}
LEGEND_SHORT = {
    "Claude Fable 5.2": "Fable 5.2",
    "Claude Fable 5.1": "Fable 5.1",
    "Claude Opus 5.5": "Opus 5.5",
    "GPT-6 Astra": "GPT-6 Astra",
    "Gemini 4 Carbon": "Gemini 4 Carbon",
}

SHORTLINK = "s.peka.ai.id/y3ZY2I"
TOTAL = 6


def X(v):
    return int(round(v * S))


def f(sz, bold=True):
    return ImageFont.truetype(FB if bold else FR, X(sz))


def mono(sz):
    return ImageFont.truetype(FM, X(sz))


# ---- mascot lockup (same source asset as HM designer) ----
_m = Image.open("/home/hatch/workspace/peka-logo/mascot-p.png").convert("RGB")
_mmask = Image.new("L", _m.size, 0)
_mp = _m.load()
_mk = _mmask.load()
for yy in range(_m.size[1]):
    for xx in range(_m.size[0]):
        r, g, b = _mp[xx, yy]
        if r > 30 or g > 30 or b > 30:
            _mk[xx, yy] = 255
_creature = _m.crop(_mmask.getbbox())
_cmask = _mmask.crop(_mmask.getbbox())


def lockup(img, d):
    cy_px, mh_px = X(95), X(46)
    cr = _creature.resize((int(_creature.width * mh_px / _creature.height), mh_px), Image.LANCZOS)
    mr = _cmask.resize(cr.size, Image.LANCZOS)
    tf = f(34)
    label = "peka.ai.id"
    ascent, descent = tf.getmetrics()
    tx = X(1010) - d.textlength(label, font=tf)
    img.paste(cr, (int(tx - X(12) - cr.width), int(cy_px - mh_px / 2 - mh_px * 0.03)), mr)
    d.text((tx, cy_px - (ascent + descent) / 2), label, font=tf, fill=YEL)


def chip(d, x, y, text, fill=YEL, fg="#111111", size=30):
    tf = f(size)
    tw = d.textlength(text, font=tf)
    pad_x = X(22)
    d.rounded_rectangle([x, y, x + tw + pad_x * 2, y + X(56)], radius=X(12), fill=fill)
    d.text((x + pad_x, y + X(9)), text, font=tf, fill=fg)
    return x + tw + pad_x * 2


def wrap(d, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
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


def para(d, x, y, text, font, fill, max_w, lh=1.28):
    lines = wrap(d, text, font, max_w)
    ascent, descent = font.getmetrics()
    step = int((ascent + descent) * lh)
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += step
    return y


def base(title, kicker="EDISI KHUSUS"):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([X(72), X(148), X(1008), X(150)], fill=PANEL_LINE)
    chip(d, X(72), X(56), kicker)
    lockup(img, d)
    if title:
        d.text((X(72), X(178)), title, font=f(64), fill=WHT)
    return img, d


def footer(d, n, note="Skor dari Anthropic, belum diverifikasi independen."):
    d.text((X(72), X(1008)), note, font=f(24, bold=False), fill=DIM)
    d.text((X(1008), X(1008)), f"{n}/{TOTAL}", font=f(24), fill=MUT, anchor="ra")


def panel(d, box, fill=PANEL, outline=PANEL_LINE):
    d.rounded_rectangle(box, radius=X(18), fill=fill, outline=outline, width=X(2))


def legend(d, x, y, size=18):
    """Identical color legend on every chart slide. Returns next y."""
    tf = f(size)
    cx = x
    for name in ["Claude Fable 5.2", "Claude Fable 5.1", "Claude Opus 5.5",
                 "GPT-6 Astra", "Gemini 4 Carbon"]:
        d.rounded_rectangle([cx, y, cx + X(20), y + X(20)], radius=X(5),
                            fill=MODEL_COLORS[name])
        cx += X(28)
        short = LEGEND_SHORT[name]
        d.text((cx, y - X(2)), short, font=tf, fill=MUT)
        cx += d.textlength(short, font=tf) + X(22)
    return y + X(34)


def full_bar(d, x, y, w, label, value, color, tag=None, label_w=290):
    """One large bar row for the full charts. Scale 0-100. Returns next y."""
    lf = f(30, bold=False)
    vf = f(36)
    d.text((x, y), label, font=lf, fill=WHT)
    track_x = x + X(label_w)
    track_w = w - X(label_w) - X(310)
    d.rounded_rectangle([track_x, y + X(4), track_x + track_w, y + X(60)],
                        radius=X(10), fill="#1B2540")
    bw = max(int(track_w * value / 100.0), X(10))
    d.rounded_rectangle([track_x, y + X(4), track_x + bw, y + X(60)],
                        radius=X(10), fill=color)
    val = f"{value:.1f}%"
    tx = track_x + track_w + X(16)
    d.text((tx, y + X(2)), val, font=vf, fill=YEL if color == YEL else WHT)
    if tag:
        tf = f(22)
        tw = d.textlength(tag, font=tf)
        vx = tx + d.textlength(val, font=vf) + X(14)
        d.rounded_rectangle([vx, y + X(6), vx + tw + X(18), y + X(48)],
                            radius=X(8), fill=YEL)
        d.text((vx + X(9), y + X(9)), tag, font=tf, fill="#111111")
    return y + X(92)


def axis_hint(d, x, y, w, label_w=290):
    track_x = x + X(label_w)
    track_w = w - X(label_w) - X(310)
    d.text((track_x, y), "0%", font=f(22, bold=False), fill=DIM)
    d.text((track_x + track_w, y), "100%", font=f(22, bold=False), fill=DIM, anchor="ra")


def compact_bar(d, x, y, w, label, value, color, label_w=190):
    """Compact bar row for the multi-chart slide. Scale 0-100. Returns next y."""
    lf = f(22, bold=False)
    vf = f(22)
    d.text((x, y), label, font=lf, fill=WHT)
    track_x = x + X(label_w)
    track_w = w - X(label_w) - X(88)
    d.rounded_rectangle([track_x, y + X(2), track_x + track_w, y + X(20)],
                        radius=X(7), fill="#1B2540")
    bw = max(int(track_w * value / 100.0), X(8))
    d.rounded_rectangle([track_x, y + X(2), track_x + bw, y + X(20)],
                        radius=X(7), fill=color)
    val = f"{value:.1f}%"
    d.text((track_x + track_w + X(12), y - X(1)), val, font=vf,
           fill=YEL if color == YEL else WHT)
    return y + X(30)


def na_row(d, x, y, label):
    d.text((x, y), label + ": tidak diuji", font=f(22, bold=False), fill=DIM)
    return y + X(30)


def mini_group(d, x, y, w, title, rows, note_line=None):
    """rows: list of (label, value|None). note_line: small line under title.
    Returns next y."""
    d.text((x, y), title, font=f(28), fill=YEL)
    y += X(30)
    if note_line:
        d.text((x, y), note_line, font=f(22, bold=False), fill=DIM)
        y += X(24)
    for label, val in rows:
        if val is None:
            y = na_row(d, x, y, label)
        else:
            y = compact_bar(d, x, y, w, label, val, MODEL_COLORS[label])
    return y + X(8)


# ================= SLIDE 1: cover =================
def slide1():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([X(72), X(148), X(1008), X(150)], fill=PANEL_LINE)
    chip(d, X(72), X(56), "EDISI KHUSUS")
    lockup(img, d)
    d.text((X(72), X(196)), "CLAUDE", font=f(150), fill=WHT)
    d.text((X(72), X(348)), "FABLE 5.2", font=f(150), fill=YEL)
    d.text((X(72), X(520)), "Model coding terbaru Anthropic, rilis 9 Nov 2026.",
           font=f(40, bold=False), fill=MUT)
    y = para(d, X(72), X(610), "Lebih cepat, lebih murah, dan nomor 1 di coding.",
             f(46), WHT, X(936))
    y0 = X(760)
    pw, gap = X(296), X(24)
    stats = [
        ("30%", "output lebih cepat dari Fable 5.1"),
        ("$8 / $40", "per 1 jt token, dari $10 / $50"),
        ("49.1%", "FrontierCode 2.0, skor tertinggi"),
    ]
    for i, (big, small) in enumerate(stats):
        x = X(72) + i * (pw + gap)
        panel(d, [x, y0, x + pw, y0 + X(172)])
        d.text((x + X(28), y0 + X(22)), big, font=f(52), fill=YEL)
        para(d, x + X(28), y0 + X(88), small, f(26, bold=False), MUT, pw - X(56))
    footer(d, 1)
    return img


# ================= SLIDE 2: apa yang baru =================
def slide2():
    img, d = base("Apa yang baru")
    d.text((X(72), X(252)), "Bukan sekadar naik versi, ini lompatan besar.",
           font=f(32, bold=False), fill=MUT)
    cards = [
        ("30% LEBIH CEPAT", "Output sampai 30% lebih cepat dari Fable 5.1, buat kerja coding yang panjang."),
        ("20% LEBIH MURAH", "Harga $8 masuk / $40 keluar per 1 jt token, turun dari $10 / $50."),
        ("MODE CEPAT 2.5x", "Mode cepat opsional sampai 2.5x lebih cepat, $16 / $80 per 1 jt token."),
        ("FABLE VS MYTHOS", "Fable: pengaman aktif, buat semua orang. Mythos: pengaman lebih longgar, organisasi terverifikasi saja."),
    ]
    x0, y0 = X(72), X(312)
    cw, ch, gx, gy = X(456), X(222), X(24), X(24)
    for i, (t, body) in enumerate(cards):
        x = x0 + (i % 2) * (cw + gx)
        y = y0 + (i // 2) * (ch + gy)
        panel(d, [x, y, x + cw, y + ch])
        d.rectangle([x, y + X(18), x + X(10), y + ch - X(18)], fill=YEL)
        d.text((x + X(32), y + X(22)), t, font=f(32), fill=YEL)
        para(d, x + X(32), y + X(76), body, f(27, bold=False), WHT, cw - X(64), lh=1.3)
    y = X(804)
    panel(d, [X(72), y, X(1008), y + X(190)], fill="#101a2c")
    y = para(d, X(100), y + X(16),
             "Tersedia di Claude Platform, Claude Code, AWS, Google Cloud, Azure.",
             f(28), WHT, X(880))
    para(d, X(100), y + X(2),
         "Promo minggu peluncuran: reset limit 1-3x, Fable sampai 50% limit mingguan Pro dan Team.",
         f(26, bold=False), MUT, X(880))
    footer(d, 2, note="Blokir turun sekitar 55% dari 5.1 (60% cyber, 40% biologi).")
    return img

# ================= SLIDE 3: FrontierCode 2.0 (full chart) =================
def slide3():
    img, d = base("FrontierCode 2.0")
    d.text((X(72), X(252)), "Agentic coding, usaha tertinggi tiap model.",
           font=f(28, bold=False), fill=MUT)
    legend(d, X(72), X(296), size=18)
    axis_hint(d, X(72), X(344), X(936))
    fc = [
        ("Claude Fable 5.2", 49.1, "TERTINGGI"),
        ("Claude Opus 5.5", 45.5, None),
        ("GPT-6 Astra", 42.8, None),
        ("Gemini 4 Carbon", 41.1, None),
        ("Claude Fable 5.1", 32.4, None),
    ]
    y = X(388)
    for label, val, tag in fc:
        y = full_bar(d, X(72), y, X(936), label, val, MODEL_COLORS[label], tag=tag)
    para(d, X(72), X(872),
         "Fable 5.2 unggul 3.6 poin dari Opus 5.5 dan 16.7 poin dari Fable 5.1. Usaha Xhigh, kecuali Gemini 4 Carbon di Medium.",
         f(28), YEL, X(936))
    footer(d, 3)
    return img

# ================= SLIDE 4: FrontierSWE v2 (full chart) =================
def slide4():
    img, d = base("FrontierSWE v2")
    d.text((X(72), X(252)), "Software engineering, usaha tertinggi tiap model.",
           font=f(28, bold=False), fill=MUT)
    legend(d, X(72), X(296), size=18)
    axis_hint(d, X(72), X(344), X(936))
    swe = [
        ("Claude Fable 5.2", 69.9, "TERTINGGI"),
        ("GPT-6 Astra", 65.5, None),
        ("Claude Opus 5.5", 62.3, None),
        ("Gemini 4 Carbon", 61.2, None),
        ("Claude Fable 5.1", 56.3, None),
    ]
    y = X(388)
    for label, val, tag in swe:
        y = full_bar(d, X(72), y, X(936), label, val, MODEL_COLORS[label], tag=tag)
    para(d, X(72), X(872),
         "Fable 5.2 unggul 4.4 poin dari GPT-6 Astra dan 13.6 poin dari Fable 5.1.",
         f(28), YEL, X(936))
    footer(d, 4)
    return img

# ================= SLIDE 5: benchmark lain (charts) =================
def slide5():
    img, d = base("Bukan cuma coding")
    para(d, X(72), X(248), "Lima benchmark lain, plus penilaian independen.",
         f(28, bold=False), MUT, X(936))
    d.text((X(72), X(282)), "Skor dari Anthropic, belum diverifikasi independen.",
           font=f(22, bold=False), fill=DIM)
    legend(d, X(72), X(312), size=18)
    yL, yR = X(348), X(348)
    lw, rw = X(432), X(432)
    yL = mini_group(d, X(72), yL, lw, "AUTOMATIONBENCH", [
        ("Gemini 4 Carbon", 53.9),
        ("Claude Fable 5.2", 51.4),
        ("Claude Opus 5.5", 42.5),
        ("GPT-6 Astra", 41.4),
        ("Claude Fable 5.1", 31.4),
    ], note_line="Gemini 4 Carbon menang di benchmark ini")
    yL = mini_group(d, X(72), yL, lw, "REMOTE LABOR INDEX", [
        ("Claude Fable 5.2", 41.3),
        ("Claude Opus 5.5", 21.3),
        ("GPT-6 Astra", 20.8),
        ("Claude Fable 5.1", 17.9),
        ("Gemini 4 Carbon", None),
    ])
    yR = mini_group(d, X(552), yR, rw, "HUMANITY'S LAST EXAM", [
        ("Claude Fable 5.2", 74.2),
        ("Claude Opus 5.5", 67.7),
        ("Claude Fable 5.1", 65.6),
        ("GPT-6 Astra", 57.2),
        ("Gemini 4 Carbon", None),
    ], note_line="Dengan tools")
    yR = mini_group(d, X(552), yR, rw, "OSWORLD 2.1", [
        ("Claude Fable 5.2", 89.3),
        ("Claude Opus 5.5", 87.2),
        ("Claude Fable 5.1", 83.5),
        ("Gemini 4 Carbon", 81.5),
        ("GPT-6 Astra", 79.5),
    ])
    yR = mini_group(d, X(552), yR, rw, "ROBODOJO SIM", [
        ("Claude Fable 5.2", 64.9),
        ("Claude Opus 5.5", 39.4),
        ("GPT-6 Astra", 29.8),
        ("Claude Fable 5.1", 27.6),
        ("Gemini 4 Carbon", None),
    ])
    y = max(yL, yR) + X(6)
    d.text((X(72), y), "PENILAIAN INDEPENDEN", font=f(24), fill=YEL)
    y += X(28)
    d.text((X(72), y), "Artificial Analysis Index 65, nomor 1 dari 9 evaluasi gabungan.",
           font=f(22, bold=False), fill=WHT)
    y += X(26)
    d.text((X(72), y), "Biaya max effort rata-rata $26.54 per tugas, sekitar 2.6x Opus 5.5.",
           font=f(22, bold=False), fill=MUT)
    y += X(26)
    d.text((X(72), y), "Terminal-Bench 4.0: 60%, setara Opus 5.5, di belakang Kimi K3.1 Pro,",
           font=f(22, bold=False), fill=MUT)
    y += X(26)
    d.text((X(72), y), "Gemini 4 Carbon, dan Sonnet 5.5.",
           font=f(22, bold=False), fill=MUT)
    d.text((X(1008), X(1036)), f"5/{TOTAL}", font=f(24), fill=MUT, anchor="ra")
    return img

# ================= SLIDE 6: keputusan jujur =================
def slide6():
    img, d = base("Keputusan jujur")
    y = X(330)
    panel(d, [X(72), y, X(1008), y + X(156)], fill="#101a2c")
    d.rectangle([X(72), y + X(18), X(82), y + X(138)], fill=YEL)
    para(d, X(108), y + X(14),
         "Fable 5.2 paling kuat buat kerja teknis paling ambisius, tapi di usaha maksimal biayanya juga paling mahal. Buat kerja harian, Opus 5.5 tetap andalan.",
         f(28), WHT, X(864), lh=1.25)
    y += X(156) + X(20)
    d.text((X(72), y), "BUKTI KERJA NYATA DARI ANTHROPIC", font=f(30), fill=YEL)
    y += X(40)
    demos = [
        "Sistem operasi jalan dibuat dalam 8 hari, pakai 1,000+ subagent.",
        "3 perangkat elektronik bareng Diode, papan siap kurang dari sehari.",
        "2 soal fisika black hole yang terbuka berhasil dipecahkan.",
        "Teorema Terakhir Fermat diformalkan dalam 30 jam (dulu 11 hari).",
        "90% perubahan codebase inti Anthropic kini ditulis Claude.",
    ]
    for dm in demos:
        d.text((X(72), y), "»", font=f(24), fill=YEL)
        y = para(d, X(104), y, dm, f(24, bold=False), WHT, X(904), lh=1.25)
        y += X(4)
    y += X(12)
    panel(d, [X(72), y, X(1008), y + X(88)], fill="#101a2c")
    para(d, X(100), y + X(16),
         "Coba di Claude Code, Claude Platform (claude-fable-5-2), AWS, Google Cloud, atau Azure.",
         f(26, bold=False), WHT, X(880), lh=1.25)
    y += X(88) + X(16)
    panel(d, [X(72), y, X(1008), y + X(112)], fill=YEL)
    d.text((X(100), y + X(12)), "PENGUMUMAN RESMI ANTHROPIC:", font=f(26), fill="#111111")
    d.text((X(100), y + X(50)), SHORTLINK, font=mono(40), fill="#111111")
    y += X(112) + X(16)
    d.text((X(72), y), "Follow @peka.ai.id  |  Gabung grup WA: url.peka.ai.id",
           font=f(24), fill=WHT)
    d.text((X(1008), y), f"6/{TOTAL}", font=f(24), fill=MUT, anchor="ra")
    y += X(32)
    d.text((X(72), y), "Simpan dan bagikan kalau bermanfaat.",
           font=f(24, bold=False), fill=MUT)
    return img


def main():
    builders = [slide1, slide2, slide3, slide4, slide5, slide6]
    for i, fn in enumerate(builders, start=1):
        img = fn()
        assert img.size == (4096, 4096), (i, img.size)
        path = os.path.join(OUT, f"slide-{i}.png")
        img.save(path)
        print(f"saved {path} {img.size}")


if __name__ == "__main__":
    main()
