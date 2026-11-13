#!/usr/bin/env python3
"""Gemini 4 Hydrogen special edition - carousel designer (6 slides, 4096x4096).

Special dark "benchmark lab" theme, same pattern as Claude Fable 5.2
(2026-11-12): deep charcoal/navy, Peka yellow accents, high data density,
no gradients, no theme name printed on the design.
Bar charts are the hero: exact value at the end of each bar, model names
clear, 0-100 scale implied by bar length, longest bar = highest value,
models without a score in a benchmark are written "tidak diuji" with no bar.
Color legend is identical on every chart slide and in the reel:
  Hydrogen = Peka yellow, Sonnet 5.5 = white/slate, GPT-6.1 Terra = blue,
  Gemini 3.8 Flash = grey, Carbon = green, Argon = light purple.
All benchmark numbers are Google vendor-reported (blog.google 12 Nov 2026
announcement + official model card) except the Artificial Analysis rows,
which are labelled independent. Honest losses are printed on slides 3, 5, 6.
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
    "Gemini 4 Hydrogen": YEL,
    "Hydrogen": YEL,
    "Claude Sonnet 5.5": "#E8EDF5",
    "Sonnet 5.5": "#E8EDF5",
    "GPT-6.1 Terra": "#38BDF8",
    "Terra": "#38BDF8",
    "Gemini 3.8 Flash": "#8A99B5",
    "3.8 Flash": "#8A99B5",
    "Gemini 4 Carbon": "#34D399",
    "Carbon": "#34D399",
    "Gemini 4 Argon": "#C4B5FD",
    "Argon": "#C4B5FD",
}
LEGEND_SHORT = {
    "Gemini 4 Hydrogen": "Hydrogen",
    "Claude Sonnet 5.5": "Sonnet 5.5",
    "GPT-6.1 Terra": "Terra",
    "Gemini 3.8 Flash": "3.8 Flash",
    "Gemini 4 Carbon": "Carbon",
    "Gemini 4 Argon": "Argon",
}

SHORTLINK = "s.peka.ai.id/N4DgPp"
TOTAL = 6

# ---- programmatic QA: registered structural boxes must not overlap ----
BOXES = []


def X(v):
    return int(round(v * S))


def f(sz, bold=True):
    return ImageFont.truetype(FB if bold else FR, X(sz))


def mono(sz):
    return ImageFont.truetype(FM, X(sz))


def reg_box(name, box):
    BOXES.append((name, box))


def check_boxes(slide_no):
    """No two registered structural boxes may intersect; all must stay
    inside the content area (x 72..1008, y 148..1000 in 1080-space)."""
    for name, (x0, y0, x1, y1) in BOXES:
        assert X(72) <= x0 and x1 <= X(1008) + X(4), (slide_no, name, "x out of grid", x0, x1)
        assert X(148) <= y0 and y1 <= X(1000) + X(4), (slide_no, name, "y out of grid", y0, y1)
    for i in range(len(BOXES)):
        for j in range(i + 1, len(BOXES)):
            n1, (a0, b0, a1, b1) = BOXES[i]
            n2, (c0, d0, c1, d1) = BOXES[j]
            overlap = not (a1 <= c0 or c1 <= a0 or b1 <= d0 or d1 <= b0)
            assert not overlap, (slide_no, "BOX OVERLAP", n1, n2)
    BOXES.clear()


# ---- mascot lockup (same source asset as Fable designer) ----
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


def fit_size(d, text, start, minimum, max_w, bold=True):
    """Largest font size (1080-space) at which text fits max_w on one line."""
    size = start
    while size > minimum:
        ft = f(size, bold=bold)
        if d.textlength(text, font=ft) <= max_w:
            return ft
        size -= 2
    ft = f(minimum, bold=bold)
    assert d.textlength(text, font=ft) <= max_w, ("TEXT TOO WIDE", text)
    return ft


def para_fit(d, x, y, text, font, fill, max_w, max_h, lh=1.28):
    """Paragraph that must fit inside max_h: assert it does, then draw."""
    lines = wrap(d, text, font, max_w)
    ascent, descent = font.getmetrics()
    step = int((ascent + descent) * lh)
    assert len(lines) * step <= max_h, ("TEXT OVERFLOW", text, len(lines), max_h)
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


def footer(d, n, note="Skor dari Google, belum diverifikasi independen."):
    d.text((X(72), X(1008)), note, font=f(24, bold=False), fill=DIM)
    d.text((X(1008), X(1008)), f"{n}/{TOTAL}", font=f(24), fill=MUT, anchor="ra")


def panel(d, box, fill=PANEL, outline=PANEL_LINE, name=None):
    d.rounded_rectangle(box, radius=X(18), fill=fill, outline=outline, width=X(2))
    if name:
        reg_box(name, box)


def legend(d, x, y, names, size=18):
    """Identical color legend on every chart slide. Returns next y."""
    tf = f(size)
    cx = x
    for name in names:
        d.rounded_rectangle([cx, y, cx + X(20), y + X(20)], radius=X(5),
                            fill=MODEL_COLORS[name])
        cx += X(28)
        short = LEGEND_SHORT[name]
        d.text((cx, y - X(2)), short, font=tf, fill=MUT)
        cx += d.textlength(short, font=tf) + X(22)
    return y + X(34)


def full_bar(d, x, y, w, label, value, color, tag=None, label_w=320):
    """One large bar row for the full charts. Scale 0-100. Returns next y."""
    lf = f(30, bold=False)
    vf = f(36)
    assert d.textlength(label, font=lf) <= X(label_w), ("LABEL TOO WIDE", label)
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


def full_na_row(d, x, y, label, label_w=320):
    """Full-chart row for a model with no score in this benchmark."""
    lf = f(30, bold=False)
    assert d.textlength(label, font=lf) <= X(label_w), ("LABEL TOO WIDE", label)
    d.text((x, y), label, font=lf, fill=WHT)
    track_x = x + X(label_w)
    d.text((track_x, y), "tidak diuji", font=f(30, bold=False), fill=DIM)
    return y + X(92)


def axis_hint(d, x, y, w, label_w=320):
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
        assert d.textlength(note_line, font=f(22, bold=False)) <= w, ("NOTE TOO WIDE", note_line)
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
    d.text((X(72), X(196)), "GEMINI", font=fit_size(d, "GEMINI", 150, 100, X(936)), fill=WHT)
    d.text((X(72), X(348)), "4 HYDROGEN", font=fit_size(d, "4 HYDROGEN", 150, 100, X(936)), fill=YEL)
    d.text((X(72), X(520)), "Model Gemini 4 buat semua orang, rilis 12 Nov 2026.",
           font=fit_size(d, "Model Gemini 4 buat semua orang, rilis 12 Nov 2026.", 40, 30, X(936), bold=False), fill=MUT)
    y = para(d, X(72), X(610), "2.5x lebih cepat dari 3.8 Flash, dan sudah masuk Search.",
             f(46), WHT, X(936))
    y0 = X(760)
    pw, gap = X(296), X(24)
    stats = [
        ("2.5x", "lebih cepat dari 3.8 Flash"),
        ("$1.50", "masuk per 1 jt token"),
        ("57%", "Terminal-Bench 4.1"),
    ]
    for i, (big, small) in enumerate(stats):
        x = X(72) + i * (pw + gap)
        panel(d, [x, y0, x + pw, y0 + X(172)], name=f"stat-{i}")
        d.text((x + X(28), y0 + X(22)), big, font=f(52), fill=YEL)
        para_fit(d, x + X(28), y0 + X(88), small, f(26, bold=False), MUT,
                 pw - X(56), X(80))
    footer(d, 1)
    check_boxes(1)
    return img


# ================= SLIDE 2: apa yang baru =================
def slide2():
    img, d = base("Apa yang baru")
    d.text((X(72), X(252)), "Bukan sekadar naik versi, ini lompatan besar.",
           font=f(32, bold=False), fill=MUT)
    cards = [
        ("4 THINKING LEVEL", "Low, Medium, High (default), Xhigh. Makin tinggi makin pintar, makin mahal."),
        ("HARGA FLAT", "$1.50 masuk / $7.50 keluar per 1 jt token. Cache $0.075."),
        ("SEARCH GLOBAL", "Gemini API, AI Studio semua tier termasuk gratis, aplikasi Gemini, Google Search."),
        ("ORCHESTRATOR", "Di Antigravity, mendekati Carbon di Terminal-Bench 4.0, 24% lebih hemat kuota."),
    ]
    x0, y0 = X(72), X(312)
    cw, ch, gx, gy = X(456), X(222), X(24), X(24)
    for i, (t, body) in enumerate(cards):
        x = x0 + (i % 2) * (cw + gx)
        y = y0 + (i // 2) * (ch + gy)
        panel(d, [x, y, x + cw, y + ch], name=f"card-{i}")
        d.rectangle([x, y + X(18), x + X(10), y + ch - X(18)], fill=YEL)
        d.text((x + X(32), y + X(22)), t, font=f(32), fill=YEL)
        para_fit(d, x + X(32), y + X(76), body, f(27, bold=False), WHT,
                 cw - X(64), X(140), lh=1.3)
    y = X(804)
    panel(d, [X(72), y, X(1008), y + X(190)], fill="#101a2c", name="avail")
    y = para(d, X(100), y + X(16),
             "Konteks 1 jt token input, sampai 1 jt token output.",
             f(28), WHT, X(880))
    para(d, X(100), y + X(2),
         "Harga Flash lama $0.75 / $3.75 bertahan sampai 31 Des 2026, lalu naik ke tarif Hydrogen mulai 1 Jan 2027.",
         f(26, bold=False), MUT, X(880))
    footer(d, 2, note="Knowledge cutoff Maret 2026.")
    check_boxes(2)
    return img


# ================= SLIDE 3: Terminal-Bench 4.1 (full chart) =================
def slide3():
    img, d = base("Terminal-Bench 4.1")
    d.text((X(72), X(252)), "Agentic coding, cheating-adjusted. Hydrogen kalah di sini.",
           font=f(28, bold=False), fill=MUT)
    legend(d, X(72), X(296), ["Gemini 4 Hydrogen", "Claude Sonnet 5.5",
                               "Gemini 3.8 Flash", "GPT-6.1 Terra"], size=18)
    axis_hint(d, X(72), X(344), X(936))
    y = X(388)
    y = full_bar(d, X(72), y, X(936), "Claude Sonnet 5.5", 63.9,
                 MODEL_COLORS["Claude Sonnet 5.5"], tag="TERTINGGI")
    y = full_bar(d, X(72), y, X(936), "Gemini 4 Hydrogen", 57.0,
                 MODEL_COLORS["Gemini 4 Hydrogen"])
    y = full_bar(d, X(72), y, X(936), "Gemini 3.8 Flash", 18.2,
                 MODEL_COLORS["Gemini 3.8 Flash"])
    y = full_na_row(d, X(72), y, "GPT-6.1 Terra")
    para(d, X(72), y + X(44),
         "Sonnet 5.5 unggul 6.9 poin dari Hydrogen. 3.8 Flash jauh di belakang dengan 18.2%. Terra tidak diuji di benchmark ini.",
         f(28), YEL, X(936))
    footer(d, 3)
    check_boxes(3)
    return img


# ================= SLIDE 4: HLE-Diamond (full chart) =================
def slide4():
    img, d = base("HLE-Diamond")
    d.text((X(72), X(252)), "Pengetahuan expert, Hydrogen memimpin kelasnya.",
           font=f(28, bold=False), fill=MUT)
    legend(d, X(72), X(296), ["Gemini 4 Hydrogen", "Claude Sonnet 5.5",
                               "GPT-6.1 Terra"], size=18)
    axis_hint(d, X(72), X(344), X(936))
    y = X(388)
    y = full_bar(d, X(72), y, X(936), "Gemini 4 Hydrogen", 58.8,
                 MODEL_COLORS["Gemini 4 Hydrogen"], tag="TERTINGGI")
    y = full_bar(d, X(72), y, X(936), "Claude Sonnet 5.5", 53.3,
                 MODEL_COLORS["Claude Sonnet 5.5"])
    y = full_bar(d, X(72), y, X(936), "GPT-6.1 Terra", 47.3,
                 MODEL_COLORS["GPT-6.1 Terra"])
    para(d, X(72), y + X(44),
         "Hydrogen unggul 5.5 poin dari Sonnet 5.5 dan 11.5 poin dari Terra. Skor tertinggi di kelasnya.",
         f(28), YEL, X(936))
    footer(d, 4)
    check_boxes(4)
    return img


# ================= SLIDE 5: benchmark lain (charts) =================
def slide5():
    img, d = base("Bukan cuma coding")
    para(d, X(72), X(248), "Empat benchmark lain, plus penilaian independen.",
         f(28, bold=False), MUT, X(936))
    d.text((X(72), X(282)), "Skor dari Google, belum diverifikasi independen.",
           font=f(22, bold=False), fill=DIM)
    legend(d, X(72), X(312), ["Gemini 4 Hydrogen", "Gemini 4 Carbon",
                               "Gemini 4 Argon", "Claude Sonnet 5.5",
                               "GPT-6.1 Terra"], size=18)
    yL, yR = X(348), X(348)
    lw, rw = X(432), X(432)
    yL = mini_group(d, X(72), yL, lw, "SWE-SWEEP", [
        ("Hydrogen", 13.5),
        ("Carbon", 9.6),
        ("Terra", 5.8),
        ("Argon", 4.3),
        ("Sonnet 5.5", 3.1),
    ], note_line="Hydrogen menang")
    yL = mini_group(d, X(72), yL + X(10), lw, "AGENTS LAST EXAM", [
        ("Carbon", 77.4),
        ("Hydrogen", 71.6),
        ("Argon", 69.0),
    ], note_line="Carbon menang")
    yR = mini_group(d, X(552), yR, rw, "OSWORLD 2.1", [
        ("Sonnet 5.5", 83.9),
        ("Carbon", 81.5),
        ("Hydrogen", 77.6),
        ("Argon", 74.7),
    ], note_line="Sonnet 5.5 menang")
    yR = mini_group(d, X(552), yR + X(10), rw, "CHARTOGRAPHY", [
        ("Carbon", 72.5),
        ("Argon", 71.6),
        ("Hydrogen", 66.6),
    ], note_line="Carbon menang")
    y = max(yL, yR) + X(16)
    d.text((X(72), y), "PENILAIAN INDEPENDEN", font=f(24), fill=YEL)
    y += X(30)
    aa_lines = [
        "Artificial Analysis Index: Hydrogen 54 (xhigh), Sonnet 5.5 dan GPT-6.1 Sol 55.",
        "Di high (default) Hydrogen 51, di belakang Sol xhigh 52 dan Opus 5.5 high 52.",
        "AA Terminal-Bench 4.0: Hydrogen 54%, Sonnet 5.5 64%, GPT-6.1 Sol 56%.",
        "Biaya per tugas: xhigh $3.16, high $1.87, medium $0.80, low $0.29.",
        "Halusinasi AA-Omniscience 8%. Skor AA per level: medium 41, low 27.",
    ]
    for ln in aa_lines:
        d.text((X(72), y), ln, font=f(22, bold=False), fill=WHT if "Index" in ln else MUT)
        y += X(28)
    assert y <= X(1000), ("SLIDE 5 TOO LOW", y)
    d.text((X(1008), X(1036)), f"5/{TOTAL}", font=f(24), fill=MUT, anchor="ra")
    check_boxes(5)
    return img


# ================= SLIDE 6: keputusan jujur =================
def slide6():
    img, d = base("Keputusan jujur")
    y = X(320)
    panel(d, [X(72), y, X(1008), y + X(150)], fill="#101a2c", name="verdict")
    d.rectangle([X(72), y + X(18), X(82), y + X(132)], fill=YEL)
    para_fit(d, X(108), y + X(14),
             "Hydrogen buat semua orang: cepat, harganya masuk akal, dan sudah ada di Search. Tapi buat coding agentic paling berat, Sonnet 5.5 masih di depan.",
             f(28), WHT, X(864), X(130), lh=1.25)
    y += X(150) + X(18)
    d.text((X(72), y), "DI MANA HYDROGEN KALAH", font=f(30), fill=YEL)
    y += X(38)
    losses = [
        "Terminal-Bench 4.1: Sonnet 5.5 menang 63.9% vs 57.0%.",
        "OSWorld 2.1: Sonnet 5.5 menang 83.9% vs 77.6%.",
        "AA Index 54, kalah tipis dari Sonnet 5.5 dan GPT-6.1 Sol (55).",
        "Agents Last Exam: Carbon menang 77.4% vs 71.6%.",
        "Harga 2x Flash lama, penolakan tak beralasan naik 5.57 poin.",
    ]
    for dm in losses:
        d.text((X(72), y), "»", font=f(24), fill=YEL)
        y = para(d, X(104), y, dm, f(24, bold=False), WHT, X(904), lh=1.25)
        y += X(4)
    y += X(10)
    panel(d, [X(72), y, X(1008), y + X(96)], fill="#101a2c", name="try")
    para_fit(d, X(100), y + X(12),
             "Coba di Gemini API, AI Studio semua tier, aplikasi Gemini, atau Google Search.",
             f(24, bold=False), WHT, X(880), X(72), lh=1.25)
    y += X(96) + X(14)
    panel(d, [X(72), y, X(1008), y + X(104)], fill=YEL, name="shortlink")
    d.text((X(100), y + X(10)), "PENGUMUMAN RESMI GOOGLE:", font=f(26), fill="#111111")
    d.text((X(100), y + X(46)), SHORTLINK, font=mono(40), fill="#111111")
    y += X(104) + X(14)
    assert y <= X(1000), ("SLIDE 6 TOO LOW", y)
    d.text((X(72), y), "Follow @peka.ai.id  |  Gabung grup WA: url.peka.ai.id",
           font=f(24), fill=WHT)
    d.text((X(1008), y), f"6/{TOTAL}", font=f(24), fill=MUT, anchor="ra")
    check_boxes(6)
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
