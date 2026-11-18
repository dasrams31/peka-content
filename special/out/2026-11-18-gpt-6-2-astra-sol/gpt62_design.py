#!/usr/bin/env python3
"""GPT-6.2 Astra + Sol special edition - carousel designer (6 slides, 4096x4096).

Dark "benchmark lab" theme, same pattern as Gemini 4 Hydrogen (2026-11-13)
and Claude Fable 5.2 (2026-11-12): deep charcoal/navy, Peka yellow accents,
high data density, no gradients, no theme name printed on the design.
Bar charts are the hero: exact value at the end of each bar, model names
clear, longest bar = highest value, models without a score are written
"tidak diuji" with no bar.
Color legend is identical on every chart slide and in the reel:
  GPT-6.2 Astra = Peka yellow #FFD60A (hero), GPT-6.2 Sol = light blue,
  Claude Fable 5.2 = white/slate, Claude Opus 5.5 = grey, Gemini 4 Carbon = green.
All benchmark numbers are from the verified fact sheet (official OpenAI
announcement 17 Nov 2026 + Artificial Analysis Intelligence Index v5.0.1,
independent). OpenAI vendor claims are labelled as vendor claims.
Honest losses are printed on slides 2, 3, 4 and 6.
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
    "GPT-6.2 Astra": YEL,
    "Astra": YEL,
    "GPT-6.2 Sol": "#7DD3FC",
    "Sol": "#7DD3FC",
    "Claude Fable 5.2": "#E8EDF5",
    "Fable 5.2": "#E8EDF5",
    "Claude Opus 5.5": "#8A99B5",
    "Opus 5.5": "#8A99B5",
    "Gemini 4 Carbon": "#34D399",
    "Carbon": "#34D399",
}
LEGEND_SHORT = {
    "GPT-6.2 Astra": "Astra",
    "GPT-6.2 Sol": "Sol",
    "Claude Fable 5.2": "Fable 5.2",
    "Claude Opus 5.5": "Opus 5.5",
    "Gemini 4 Carbon": "Carbon",
}

SHORTLINK = "s.peka.ai.id/uzBjvq"
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


# ---- mascot lockup (same source asset as Fable/Hydrogen designers) ----
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
        d.text((X(72), X(178)), title, font=fit_size(d, title, 64, 44, X(936)), fill=WHT)
    return img, d


def footer(d, n, note="Skor dari OpenAI, belum diverifikasi independen."):
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


def value_bar(d, x, y, w, label, value, scale, color, fmt, tag=None, label_w=320):
    """One large bar row. Bar length = value/scale of track. Exact value
    printed at the end of the track. Returns next y."""
    lf = f(30, bold=False)
    vf = f(36)
    assert d.textlength(label, font=lf) <= X(label_w), ("LABEL TOO WIDE", label)
    d.text((x, y), label, font=lf, fill=WHT)
    track_x = x + X(label_w)
    track_w = w - X(label_w) - X(310)
    d.rounded_rectangle([track_x, y + X(4), track_x + track_w, y + X(60)],
                        radius=X(10), fill="#1B2540")
    bw = max(int(track_w * value / scale), X(10))
    d.rounded_rectangle([track_x, y + X(4), track_x + bw, y + X(60)],
                        radius=X(10), fill=color)
    val = fmt(value)
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


def axis_hint(d, x, y, w, lo, hi, label_w=320):
    track_x = x + X(label_w)
    track_w = w - X(label_w) - X(310)
    d.text((track_x, y), lo, font=f(22, bold=False), fill=DIM)
    d.text((track_x + track_w, y), hi, font=f(22, bold=False), fill=DIM, anchor="ra")


# ================= SLIDE 1: cover =================
def slide1():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([X(72), X(148), X(1008), X(150)], fill=PANEL_LINE)
    chip(d, X(72), X(56), "EDISI KHUSUS")
    lockup(img, d)
    d.text((X(72), X(196)), "GPT-6.2", font=fit_size(d, "GPT-6.2", 150, 100, X(936)), fill=WHT)
    d.text((X(72), X(348)), "ASTRA + SOL", font=fit_size(d, "ASTRA + SOL", 150, 100, X(936)), fill=YEL)
    d.text((X(72), X(520)), "Flagship baru OpenAI, rilis 17 Nov 2026.",
           font=fit_size(d, "Flagship baru OpenAI, rilis 17 Nov 2026.", 40, 30, X(936), bold=False), fill=MUT)
    y = para(d, X(72), X(610), "Astra buat proyek paling berat, Sol buat kerja harian.",
             f(46), WHT, X(936))
    y0 = X(760)
    pw, gap = X(296), X(24)
    stats = [
        ("62", "AA Index, #2 di bawah Fable 65"),
        ("1.318", "AA-3D Elo, peringkat 1"),
        ("$2 / $10", "Sol per 1 jt token"),
    ]
    for i, (big, small) in enumerate(stats):
        x = X(72) + i * (pw + gap)
        panel(d, [x, y0, x + pw, y0 + X(172)], name=f"stat-{i}")
        d.text((x + X(28), y0 + X(22)), big, font=f(52), fill=YEL)
        para_fit(d, x + X(28), y0 + X(88), small, f(26, bold=False), MUT,
                 pw - X(56), X(80))
    footer(d, 1, note="Skor independen Artificial Analysis v5.0.1.")
    check_boxes(1)
    return img


# ================= SLIDE 2: AA Intelligence Index (full chart) =================
def slide2():
    img, d = base("AA Intelligence Index")
    d.text((X(72), X(252)), "Penilaian independen Artificial Analysis v5.0.1, max effort.",
           font=f(28, bold=False), fill=MUT)
    legend(d, X(72), X(296), ["Claude Fable 5.2", "GPT-6.2 Astra",
                               "Gemini 4 Carbon", "Claude Opus 5.5",
                               "GPT-6.2 Sol"], size=18)
    axis_hint(d, X(72), X(344), X(936), "0", "100")
    y = X(388)
    fmt_int = lambda v: f"{v}"
    y = value_bar(d, X(72), y, X(936), "Claude Fable 5.2", 65, 100,
                  MODEL_COLORS["Claude Fable 5.2"], fmt_int, tag="TERTINGGI")
    y = value_bar(d, X(72), y, X(936), "GPT-6.2 Astra", 62, 100,
                  MODEL_COLORS["GPT-6.2 Astra"], fmt_int)
    y = value_bar(d, X(72), y, X(936), "Gemini 4 Carbon", 60, 100,
                  MODEL_COLORS["Gemini 4 Carbon"], fmt_int)
    y = value_bar(d, X(72), y, X(936), "Claude Opus 5.5", 59, 100,
                  MODEL_COLORS["Claude Opus 5.5"], fmt_int)
    y = value_bar(d, X(72), y, X(936), "GPT-6.2 Sol", 57, 100,
                  MODEL_COLORS["GPT-6.2 Sol"], fmt_int)
    para(d, X(72), y + X(40),
         "Astra 62, kalah 3 poin dari Fable 65. Tapi biaya Astra $4.00 per tugas, jauh di bawah Fable $26.54. Sol 57, setara GPT-6 Astra, cuma $1.01 per tugas.",
         f(28), YEL, X(936))
    footer(d, 2, note="Skor independen Artificial Analysis, bukan klaim OpenAI.")
    check_boxes(2)
    return img


# ================= SLIDE 3: AA-3D Elo + vendor delta claims =================
def slide3():
    img, d = base("AA-3D: Astra peringkat 1")
    d.text((X(72), X(252)), "Elo 3D generation, Artificial Analysis. Di sini Astra menang.",
           font=f(28, bold=False), fill=MUT)
    legend(d, X(72), X(296), ["GPT-6.2 Astra", "Claude Fable 5.2",
                               "GPT-6.2 Sol"], size=18)
    axis_hint(d, X(72), X(344), X(936), "0", "1.500")
    y = X(388)
    fmt_elo = lambda v: f"{v:,}".replace(",", ".")
    y = value_bar(d, X(72), y, X(936), "GPT-6.2 Astra", 1318, 1500,
                  MODEL_COLORS["GPT-6.2 Astra"], fmt_elo, tag="TERTINGGI")
    y = value_bar(d, X(72), y, X(936), "Claude Fable 5.2", 1271, 1500,
                  MODEL_COLORS["Claude Fable 5.2"], fmt_elo)
    y = value_bar(d, X(72), y, X(936), "GPT-6.2 Sol", 1259, 1500,
                  MODEL_COLORS["GPT-6.2 Sol"], fmt_elo)
    y = X(692)
    d.text((X(72), y), "KLAIM OPENAI (VENDOR, BELUM DIVERIFIKASI INDEPENDEN)",
           font=f(22), fill=DIM)
    y += X(30)
    cw, ch, gx, gy = X(456), X(116), X(24), X(14)
    cards = [
        ("AGENTS LAST EXAM", "+5.2 pts vs GPT-6 Astra, +5.5 vs Fable 5.2"),
        ("TERMINAL-BENCH-SCIENCE", "+9 pts vs GPT-6 Astra, rekor baru"),
        ("EXPLOITBENCH", "+22 pts vs GPT-6 Astra (internal port)"),
        ("GDPVAL V2", "+6.2 pts, token keluar 22% lebih sedikit"),
    ]
    for i, (t, body) in enumerate(cards):
        x = X(72) + (i % 2) * (cw + gx)
        yy = y + (i // 2) * (ch + gy)
        panel(d, [x, yy, x + cw, yy + ch], name=f"delta-{i}")
        d.text((x + X(24), yy + X(14)), t, font=f(22), fill=YEL)
        para_fit(d, x + X(24), yy + X(46), body, f(20, bold=False), WHT,
                 cw - X(48), X(64), lh=1.25)
    footer(d, 3, note="Elo independen Artificial Analysis; delta klaim OpenAI.")
    check_boxes(3)
    return img


# ================= SLIDE 4: honest losses =================
def slide4():
    img, d = base("Jujur saja: di mana kalah")
    d.text((X(72), X(252)), "Angka independen Artificial Analysis + pengakuan OpenAI sendiri.",
           font=f(28, bold=False), fill=MUT)
    losses = [
        "AA Index: Astra 62, kalah 3 poin dari Fable 5.2 (65). Sol 57.",
        "Coding Agent Index v2.1: Astra 53 di Codex, datar vs GPT-6 Astra, di bawah Fable 58. Sol turun 52 ke 49.",
        "Terminal-Bench 4.0: Astra 64.1%, di bawah Carbon 65.2%.",
        "AA-Briefcase Elo: Opus 5.5 1800, Fable 1785, Astra 1644, Sol 1612.",
        "Halusinasi AA-Omniscience: Astra 59%, Sol 55%.",
        "Dua tes: model lebih sering tidak menyebut hambatan kerja, misal file hilang atau tool tidak tersedia.",
        "Pengaman cyber lebih ketat, bisa batasi riset keamanan yang sah.",
    ]
    y = X(320)
    for dm in losses:
        d.text((X(72), y), "»", font=f(26), fill=YEL)
        y = para(d, X(108), y, dm, f(26, bold=False), WHT, X(900), lh=1.25)
        y += X(10)
    y += X(6)
    panel(d, [X(72), y, X(1008), y + X(96)], fill="#101a2c", name="verdict")
    para_fit(d, X(100), y + X(14),
             "Astra #2 di indeks independen. Murah, tapi kalahnya nyata.",
             f(26, bold=False), YEL, X(880), X(72), lh=1.25)
    footer(d, 4, note="Skor independen Artificial Analysis; sisanya pengakuan OpenAI.")
    check_boxes(4)
    return img


# ================= SLIDE 5: price + access =================
def slide5():
    img, d = base("Harga dan akses")
    d.text((X(72), X(252)), "Per 1 jt token. Astra 20% lebih murah dari GPT-6 Astra.",
           font=f(28, bold=False), fill=MUT)
    y0 = X(312)
    cw, gap = X(456), X(24)
    prices = [
        ("GPT-6.2 ASTRA", "$8", "$0.40 cache / $40 keluar",
         "Cache 60% lebih murah."),
        ("GPT-6.2 SOL", "$2", "$0.10 cache / $10 keluar",
         "Sama seperti GPT-6.1 Sol."),
    ]
    for i, (name, big, mid, note) in enumerate(prices):
        x = X(72) + i * (cw + gap)
        panel(d, [x, y0, x + cw, y0 + X(300)], name=f"price-{i}")
        d.text((x + X(28), y0 + X(20)), name, font=f(30),
               fill=YEL if i == 0 else "#7DD3FC")
        d.text((x + X(28), y0 + X(62)), big, font=f(72), fill=WHT)
        d.text((x + X(28), y0 + X(150)), "masuk per 1 jt token",
               font=f(24, bold=False), fill=MUT)
        para_fit(d, x + X(28), y0 + X(186), mid, f(24, bold=False), WHT,
                 cw - X(56), X(36))
        para_fit(d, x + X(28), y0 + X(232), note, f(22, bold=False), MUT,
                 cw - X(56), X(56))
    y = X(636)
    panel(d, [X(72), y, X(1008), y + X(336)], fill="#101a2c", name="access")
    d.text((X(100), y + X(18)), "DI MANA BISA DIPAKAI", font=f(28), fill=YEL)
    acc = [
        "ChatGPT Work dan Codex, pengguna Plus, Pro, Enterprise, Edu, mulai 17 Nov 2026.",
        "API: gpt-6.2-astra dan gpt-6.2-sol.",
        "Ultrafast: Pro 500 kedua model, Pro 200 Sol saja, pertama kalinya.",
        "Bukan di chat ChatGPT biasa.",
    ]
    yy = y + X(62)
    for ln in acc:
        d.text((X(100), yy), "»", font=f(26), fill=YEL)
        yy = para(d, X(132), yy, ln, f(26, bold=False), WHT, X(848), lh=1.25)
        yy += X(10)
    footer(d, 5, note="Harga resmi OpenAI. Cutoff: Astra 18 Mei 2026, Sol 1 Jun 2026.")
    check_boxes(5)
    return img


# ================= SLIDE 6: close =================
def slide6():
    img, d = base("Keputusan jujur")
    y = X(320)
    panel(d, [X(72), y, X(1008), y + X(170)], fill="#101a2c", name="verdict")
    d.rectangle([X(72), y + X(18), X(82), y + X(152)], fill=YEL)
    para_fit(d, X(108), y + X(14),
             "Astra kuat buat proyek berat, Sol murah buat harian. Tapi kalau patokannya indeks independen, Fable 5.2 masih #1. Pilih dari kebutuhan, bukan dari hype.",
             f(28), WHT, X(864), X(150), lh=1.25)
    y += X(170) + X(18)
    panel(d, [X(72), y, X(1008), y + X(96)], fill="#101a2c", name="try")
    para_fit(d, X(100), y + X(12),
             "Coba di ChatGPT Work atau Codex, atau lewat API gpt-6.2-astra dan gpt-6.2-sol.",
             f(24, bold=False), WHT, X(880), X(72), lh=1.25)
    y += X(96) + X(14)
    panel(d, [X(72), y, X(1008), y + X(104)], fill=YEL, name="shortlink")
    d.text((X(100), y + X(10)), "PENGUMUMAN RESMI OPENAI:", font=f(26), fill="#111111")
    d.text((X(100), y + X(46)), SHORTLINK, font=mono(40), fill="#111111")
    y += X(104) + X(14)
    assert y <= X(1000), ("SLIDE 6 TOO LOW", y)
    d.text((X(72), y), "Follow @peka.ai.id  |  Gabung grup WA: s.peka.ai.id/gabung",
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
