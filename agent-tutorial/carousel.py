#!/usr/bin/env python3
"""Carousel designer for Tutorial Agent Peka editions (Herlambang style).

Square 4096x4096 PIL slides, driven by the "carousel" section of the
edition spec.json plus spec["steps"]:
  {"slides": [{"type": "cover", "title": [...], "sub": "...",
               "try_now": "COBA SEKARANG: ...", "result": "HASIL AKHIR: ..."},
              {"type": "step", "step": 1},
              ...
              {"type": "closing", "title": [...], "lines": [...]}]}
Usage: python3 carousel.py <spec.json> <out_dir>
Writes slide-1.png .. slide-6.png into the out dir.

Visual identity (Herlambang variant, adapted to Peka colors; matches
animated/scene-herlambang.html frame-for-frame in spirit):
  alternating grid-paper backgrounds: cream #F5F1E8, dark slate
  #0D1117, Peka yellow #FFD60A; persistent top tab bar (KENAPA / ALAT /
  LANGKAH / JALANKAN, active tab yellow-filled) on the cover slide;
  huge condensed Anton titles with ONE Playfair-italic accent word
  (emerald #10B981 on cream/dark, deep green #065F46 on yellow);
  neo-brutalist chunky panels: thick black borders, hard offset
  shadows, square corners; terminal windows (dark panel, emerald mono,
  traffic-light dots, step label pill); Peka header lockup (mascot mark
  + peka.ai.id) on every slide, in a white pill on yellow backgrounds
  because the yellow mascot is invisible on yellow.

Per-slide backgrounds (debut #01; future episodes keep the same
tab -> theme mapping): cover cream / step 1 dark / step 2 yellow /
step 3 yellow / step 4 dark / closing cream.

Layout QA (special/DESIGN_RULES.md): every text/panel box is recorded
and checked before the PNG is saved: boxes must stay inside the content
area (below the header/tab bar, above the reserved footer strip) and
must not overlap each other. One violation aborts the render. Max 3
text sizes per slide. Leftover vertical space is shared out (blocks are
spaced to end near the footer strip; step slides are vertically
centred).

Step extras (from the step dict, so future episodes reuse the same
renderers): step["cards"] = 2x2 mini-card grid (component overview);
step["terminal"] = {"label": ..., "lines": [...]} run-output card.
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "animated", "assets")
W = H = 4096
MARGIN = 240
CONTENT_W = W - 2 * MARGIN
FOOTER_TOP = H - 340
HEADER_NO_TABS = 640
HEADER_WITH_TABS = 880
COVER_TITLE = 360
TITLE = 280
BODY = 96
META = 56
CODE_FLOOR = 52

EMERALD = "#10B981"
YELLOW = "#FFD60A"
DARK = "#0D1117"

THEMES = {
    "cream": {"bg": "#F5F1E8", "grid": (13, 17, 23, 0.07), "text": "#0D1117",
              "dim": "#5A5648", "accent": "#10B981", "card": "#FFFFFF",
              "card_text": "#0D1117", "chip_bg": "#FFD60A", "chip_text": "#0D1117",
              "term_bg": "#161B22", "border": "#0D1117", "shadow": "#0D1117",
              "footer": "#5A5648", "hot": "#FFD60A", "hot_text": "#0D1117",
              "hot_dim": "#3D3A00"},
    "dark": {"bg": "#0D1117", "grid": (255, 255, 255, 0.06), "text": "#F0F6FC",
             "dim": "#8B949E", "accent": "#FFD60A", "card": "#161B22",
             "card_text": "#F0F6FC", "chip_bg": "#FFD60A", "chip_text": "#0D1117",
             "term_bg": "#0B0D10", "border": "#000000", "shadow": "#000000",
             "footer": "#8B949E", "hot": "#FFD60A", "hot_text": "#0D1117",
             "hot_dim": "#3D3A00"},
    "yellow": {"bg": "#FFD60A", "grid": (13, 17, 23, 0.10), "text": "#0D1117",
               "dim": "#4A4200", "accent": "#065F46", "card": "#0D1117",
               "card_text": "#F0F6FC", "chip_bg": "#0D1117", "chip_text": "#FFD60A",
               "term_bg": "#0D1117", "border": "#0D1117", "shadow": "#0D1117",
               "footer": "#4A4200", "hot": "#FFFFFF", "hot_text": "#0D1117",
               "hot_dim": "#5A5648"},
}

# tab -> theme, per the reel (scene-herlambang.html).
TAB_THEMES = {"KENAPA": "cream", "ALAT": "dark", "LANGKAH": "yellow",
              "JALANKAN": "dark"}
TABS = ["KENAPA", "ALAT", "LANGKAH", "JALANKAN"]
# tab state colors per background theme: [active, visited, upcoming]
TAB_COLORS = {
    "cream": [("#FFD60A", "#0D1117"), ("#161B22", "#F0F6FC"), ("#FFFFFF", "#0D1117")],
    "dark": [("#FFD60A", "#0D1117"), ("#23272E", "#F0F6FC"), ("#FFFFFF", "#0D1117")],
    "yellow": [("#0D1117", "#FFD60A"), ("#FFFFFF", "#0D1117"),
               ("rgba(255,255,255,0.45)", "#0D1117")],
}
# slide index (0-based) -> active tab for the tab bar / seclabel.
SLIDE_TABS = ["KENAPA", "ALAT", "LANGKAH", "LANGKAH", "JALANKAN", "JALANKAN"]
# step number -> accent word in the step title (uppercased match).
STEP_ACCENTS = {1: "KOMPONEN", 2: "CUACA", 3: "LOOP", 4: "LOG"}

MASCOT_PATH = os.path.join(BASE, "..", "piko", "piko-idle.png")
MASCOT_H = 200
_MASCOT = None


def mascot_image():
    """Piko mascot, trimmed to its non-transparent content bbox."""
    global _MASCOT
    if _MASCOT is None:
        im = Image.open(MASCOT_PATH).convert("RGBA")
        _MASCOT = im.crop(im.getchannel("A").getbbox())
    return _MASCOT


def _font(name, size):
    return ImageFont.truetype(os.path.join(ASSETS, name), size)


def anton(sz):
    return _font("Anton-Regular.ttf", sz)


def playfair(sz):
    return _font("PlayfairDisplay-Italic.ttf", sz)


def f(sz):
    return _font("Poppins-Bold.ttf", sz)


def body(sz):
    return _font("Poppins-SemiBold.ttf", sz)


def mono(sz, bold=False):
    return _font("DejaVuSansMono-Bold.ttf" if bold else "DejaVuSansMono.ttf", sz)


def check_clean(text):
    assert "\u2014" not in text and "\u2013" not in text, f"dash terlarang: {text[:60]}"


def blend(bg_hex, rgba):
    """Blend an rgba grid color over a hex background (PIL draws on RGB)."""
    r = int(bg_hex[1:3], 16)
    g = int(bg_hex[3:5], 16)
    b = int(bg_hex[5:7], 16)
    a = rgba[3]
    return (round(r * (1 - a) + rgba[0] * a),
            round(g * (1 - a) + rgba[1] * a),
            round(b * (1 - a) + rgba[2] * a))


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


class Layout:
    """Record every drawn box; abort on overflow or overlap."""

    def __init__(self, header_bottom):
        self.header_bottom = header_bottom
        self.boxes = []

    def add(self, x0, y0, x1, y1, label):
        assert x0 >= MARGIN - 1, f"{label}: keluar kiri ({x0})"
        assert x1 <= W - MARGIN + 1, f"{label}: keluar kanan ({x1})"
        assert y0 >= self.header_bottom - 1, f"{label}: nabrak header ({y0})"
        assert y1 <= FOOTER_TOP + 1, f"{label}: masuk strip footer ({y1})"
        self.boxes.append((x0, y0, x1, y1, label))

    def check(self):
        boxes = self.boxes
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                a, b = boxes[i], boxes[j]
                ox = min(a[2], b[2]) - max(a[0], b[0])
                oy = min(a[3], b[3]) - max(a[1], b[1])
                assert not (ox > 8 and oy > 8), (
                    f"tabrakan: {a[4]} vs {b[4]} "
                    f"(overlap {ox}x{oy}px)")


def text_box(d, x, y, text, font):
    # x0 is the draw position: a glyph's negative left bearing (e.g. "P"
    # in Poppins) would otherwise report a 2-3px phantom overflow.
    bb = d.textbbox((x, y), text, font=font)
    return x, bb[1], bb[2], bb[3]


def chunky(d, box, fill, border, shadow, width=8):
    """Neo-brutalist panel: hard offset shadow, thick border, square corners."""
    x0, y0, x1, y1 = box
    d.rectangle([(x0 + 16, y0 + 16), (x1 + 16, y1 + 16)], fill=shadow)
    d.rectangle(box, fill=fill, outline=border, width=width)


def draw_grid(d, th):
    gc = blend(th["bg"], th["grid"])
    step = 256
    for x in range(0, W + 1, step):
        d.line([(x, 0), (x, H)], fill=gc, width=2)
    for y in range(0, H + 1, step):
        d.line([(0, y), (W, y)], fill=gc, width=2)


def draw_header(d, th, seclabel, page, total, theme_name):
    """Top bar: // section label left, Peka lockup right, footer strip.
    Returns the mascot paste position (x, y) for the caller to paste
    onto the image (keeps alpha handling in one place)."""
    d.text((MARGIN, 250), f"// {seclabel}", font=mono(96, True), fill=th["text"])
    m = mascot_image()
    mw = max(1, round(MASCOT_H * m.width / m.height))
    word = "peka.ai.id"
    wf = f(130)
    tw = d.textlength(word, font=wf)
    if theme_name == "yellow":
        # white pill: the yellow mascot is invisible on yellow.
        pw = 60 + mw + 40 + int(tw) + 60
        ph = 260
        px = W - MARGIN - pw
        py = 200
        d.rectangle([(px + 12, py + 12), (px + pw + 12, py + ph + 12)], fill="#0D1117")
        d.rounded_rectangle([(px, py), (px + pw, py + ph)], radius=130,
                            fill="#FFFFFF", outline="#0D1117", width=8)
        d.text((px + 60 + mw + 40, py + 62), word, font=wf, fill="#0D1117")
        mascot_xy = (px + 60, py + 30)
    else:
        # right-align the lockup to the margin (fixed offsets overflow
        # at the 130px wordmark size: the text alone is 663px wide).
        text_x = W - MARGIN - int(tw)
        mascot_xy = (text_x - 40 - mw, 200)
        d.text((text_x, 250), word, font=wf, fill=th["text"])
    d.text((MARGIN, H - 200), "Follow @peka.ai.id  -  Gabung: s.peka.ai.id/gabung",
           font=body(META), fill=th["footer"])
    d.text((W - MARGIN - 300, H - 200), f"{page}/{total}", font=mono(META, True),
           fill=th["footer"])
    return mascot_xy


def draw_tabs(d, th, active_idx, theme_name):
    """Persistent top tab bar (cover slide only in the carousel)."""
    colors = TAB_COLORS[theme_name]
    gap = 60
    tw = (CONTENT_W - 3 * gap) // 4
    y = 560
    h = 230
    for i, name in enumerate(TABS):
        x = MARGIN + i * (tw + gap)
        bg, fg = colors[0] if i == active_idx else (
            colors[1] if i < active_idx else colors[2])
        d.rectangle([(x + 16, y + 16), (x + tw + 16, y + h + 16)], fill=th["shadow"])
        d.rectangle([(x, y), (x + tw, y + h)], fill=bg, outline=th["border"], width=8)
        if i == active_idx:
            d.rectangle([(x, y + h - 24), (x + tw, y + h)], fill=th["accent"])
        nw = d.textlength(name, font=anton(100))
        d.text((x + (tw - nw) // 2, y + 52), name, font=anton(100), fill=fg)


def base(theme_name, seclabel, page, total, with_tabs, active_idx=0):
    th = THEMES[theme_name]
    img = Image.new("RGB", (W, H), th["bg"])
    d = ImageDraw.Draw(img)
    draw_grid(d, th)
    mascot_xy = draw_header(d, th, seclabel, page, total, theme_name)
    m = mascot_image()
    mw = max(1, round(MASCOT_H * m.width / m.height))
    img.paste(m.resize((mw, MASCOT_H), Image.LANCZOS), mascot_xy, m.resize((mw, MASCOT_H), Image.LANCZOS))
    if with_tabs:
        draw_tabs(d, th, active_idx, theme_name)
    return img, d, th


def draw_lines(d, lay, x, y, lines, font, fill, lh, label):
    """Draw wrapped lines, register one box per line, return bottom y."""
    for ln in lines:
        check_clean(ln)
        d.text((x, y), ln, font=font, fill=fill)
        lay.add(*text_box(d, x, y, ln, font), label)
        y += lh
    return y


def word_font(word, accent, size):
    return playfair(size) if accent else anton(size)


def big_title_lines(title_words, max_w, size, accent_word=None):
    """Wrap uppercased words into lines (Anton-measured, <=2 lines),
    marking the accent word. title_words: list of words (already upper).
    Returns lines: list of list of (word, is_accent)."""
    lines, cur, cur_w = [], [], 0
    gap = int(size * 0.22)
    for w_ in title_words:
        wf = playfair(size) if (accent_word and w_.strip(",.?!") == accent_word) else anton(size)
        ww = dummylength(wf, w_)
        add = ww if not cur else gap + ww
        if cur and cur_w + add > max_w:
            lines.append(cur)
            cur, cur_w = [], 0
            add = ww
        cur.append((w_, bool(accent_word and w_.strip(",.?!") == accent_word)))
        cur_w += add
    if cur:
        lines.append(cur)
    while len(lines) > 2 and size > 200:
        size -= 20
        return big_title_lines(title_words, max_w, size, accent_word)
    return lines, size


def dummylength(font, text):
    return font.getlength(text)


def draw_big_title(d, lay, lines, x, y, size, th, label="title"):
    """Draw mixed Anton / Playfair-italic-accent title lines."""
    lh = int(size * 1.08)
    gap = int(size * 0.22)
    for ln in lines:
        x0 = x
        widths = []
        for w_, acc in ln:
            wf = word_font(w_, acc, size)
            widths.append(d.textlength(w_, font=wf))
        total_w = sum(widths) + gap * (len(ln) - 1)
        cx = x
        for (w_, acc), ww in zip(ln, widths):
            check_clean(w_)
            d.text((cx, y), w_, font=word_font(w_, acc, size),
                   fill=th["accent"] if acc else th["text"])
            cx += ww + gap
        lay.add(x0, y, x0 + total_w, y + lh, label)
        y += lh
    return y


def title_from_spec(title, max_w, size, accent_word=None):
    """Resolve a spec title (explicit line list or plain string) to
    drawable (lines, size) via big_title_lines."""
    if isinstance(title, list):
        lines = []
        for ln in title:
            words = ln.split()
            lines.append([(w_, bool(accent_word and w_.strip(",.?!") == accent_word))
                          for w_ in words])
        return lines, size
    words = title.upper().split()
    return big_title_lines(words, max_w, size, accent_word)


def fit_code_lines(d, lines, max_w):
    """Shrink mono size to a 52px floor; wrap any line still too wide.
    Returns (font_size, display_lines). Never clip a command."""
    size = BODY
    while size > CODE_FLOOR and any(
            d.textlength(ln, font=mono(size)) > max_w for ln in lines):
        size -= 4
    font = mono(size)
    out = []
    for ln in lines:
        check_clean(ln)
        if d.textlength(ln, font=font) <= max_w:
            out.append(ln)
            continue
        words = ln.split(" ")
        half = len(ln) // 2
        cut = min(range(len(words) - 1),
                  key=lambda i: abs(len(" ".join(words[:i + 1])) - half)) + 1
        out.append(" ".join(words[:cut]))
        out.append("  " + " ".join(words[cut:]))
    return size, out


def code_panel_height(d, code_lines, max_w):
    size, lines = fit_code_lines(d, code_lines, max_w)
    return 200 + len(lines) * int(size * 1.45), size, lines


def draw_code_panel(d, lay, x, y, code_lines, max_w, th, label="terminal",
                    terminal=False):
    panel_h, size, lines = code_panel_height(d, code_lines, max_w)
    font = mono(size)
    lh = int(size * 1.45)
    assert y + panel_h <= FOOTER_TOP, "panel kode kepanjangan, pendekkan code di spec"
    chunky(d, (x, y, W - MARGIN, y + panel_h), th["term_bg"], th["border"],
           th["shadow"])
    lay.add(x, y, W - MARGIN, y + panel_h, "code-panel")
    d.ellipse([(x + 70, y + 62), (x + 110, y + 102)], fill="#ff5f57")
    d.ellipse([(x + 140, y + 62), (x + 180, y + 102)], fill="#febc2e")
    d.ellipse([(x + 210, y + 62), (x + 250, y + 102)], fill="#28c840")
    # label pill: white rounded rect, dark mono text
    lbl_w = d.textlength(label, font=mono(64, True)) + 72
    d.rounded_rectangle([(x + 300, y + 42), (x + 300 + lbl_w, y + 118)],
                        radius=38, fill="#FFFFFF", outline="#0D1117", width=4)
    d.text((x + 336, y + 52), label, font=mono(64, True), fill="#0D1117")
    ly = y + 180
    for ln in lines:
        if terminal and ln.startswith("$ "):
            d.text((x + 80, ly), "$", font=font, fill="#FF6B5E")
            d.text((x + 80 + d.textlength("$ ", font=font), ly), ln[2:],
                   font=font, fill=EMERALD)
        elif terminal and (ln.startswith("memanggil") or ln.startswith("Jawaban")):
            d.text((x + 80, ly), ln, font=font, fill="#8B949E")
        else:
            d.text((x + 80, ly), ln, font=font, fill=EMERALD)
        ly += lh
    return y + panel_h


def draw_panel(d, lay, x, y, lines, th, fill, border, text_fill, label,
               font=None, lh=None):
    """Chunky text panel; lines already wrapped. Returns bottom y."""
    font = font or body(BODY)
    lh = lh or int(BODY * 1.45)
    panel_h = 100 + len(lines) * lh
    chunky(d, (x, y, W - MARGIN, y + panel_h), fill, border, th["shadow"])
    lay.add(x, y, W - MARGIN, y + panel_h, label)
    ty = y + 50
    for ln in lines:
        check_clean(ln)
        d.text((x + 80, ty), ln, font=font, fill=text_fill)
        ty += lh
    return y + panel_h


def slide_cover(spec, s, page, total, shortlink):
    th_name = "cream"
    img, d, th = base(th_name, "kenapa", page, total, with_tabs=True, active_idx=0)
    lay = Layout(HEADER_WITH_TABS)
    # --- measure pass: total content height, then centre vertically ---
    tlines, tsize = title_from_spec(s["title"], CONTENT_W, COVER_TITLE, "PERTAMAMU")
    sub_lines = wrap(d, s["sub"], body(BODY), CONTENT_W)
    try_lines = wrap(d, s["try_now"], body(BODY), CONTENT_W - 160)
    info = f"{len(spec['steps'])} LANGKAH   |   BUTUH: {'  -  '.join(spec['prerequisites'])}"
    info_lines = wrap(d, info, mono(64, True), CONTENT_W)
    result_lines = wrap(d, s["result"], body(BODY), CONTENT_W - 160) if s.get("result") else []
    title_h = len(tlines) * int(tsize * 1.08)
    content_h = (200 + 60 + title_h + 60 + len(sub_lines) * int(BODY * 1.45) + 80
                 + (100 + len(try_lines) * int(BODY * 1.45)) + 80
                 + len(info_lines) * 110 + 80
                 + (100 + len(result_lines) * int(BODY * 1.45)))
    avail = FOOTER_TOP - HEADER_WITH_TABS
    y = HEADER_WITH_TABS + max(0, (avail - content_h) // 2)
    # --- draw pass ---
    chip = f"EDISI #{spec['episode']:02d}"
    chip_w = 160 + int(d.textlength(chip, font=mono(88, True)))
    d.rectangle([(MARGIN + 16, y + 16), (MARGIN + 16 + chip_w, y + 216)], fill=th["shadow"])
    d.rectangle([(MARGIN, y), (MARGIN + chip_w, y + 200)], fill=th["chip_bg"],
                outline=th["border"], width=8)
    d.text((MARGIN + 80, y + 52), chip, font=mono(88, True), fill=th["chip_text"])
    lay.add(MARGIN, y, MARGIN + chip_w + 16, y + 216, "chip")
    y += 200 + 60
    y = draw_big_title(d, lay, tlines, MARGIN, y, tsize, th, "title")
    y += 60
    y = draw_lines(d, lay, MARGIN, y, sub_lines, body(BODY), th["dim"],
                   int(BODY * 1.45), "sub")
    y += 80
    y = draw_panel(d, lay, MARGIN, y, try_lines, th, th["hot"], th["border"],
                   th["hot_text"], "try-panel")
    y += 80
    y = draw_lines(d, lay, MARGIN, y, info_lines, mono(64, True), th["dim"],
                   110, "info")
    y += 80
    if result_lines:
        y = draw_panel(d, lay, MARGIN, y, result_lines, th, th["card"],
                       EMERALD, th["card_text"], "result-panel")
    lay.check()
    return img


def slide_step(spec, s, page, total, shortlink):
    step = spec["steps"][s["step"] - 1]
    assert step["n"] == s["step"], "nomor langkah tidak cocok dengan spec"
    tab = SLIDE_TABS[page - 1]
    th_name = TAB_THEMES[tab]
    img, d, th = base(th_name, tab.lower(), page, total, with_tabs=False)
    lay = Layout(HEADER_NO_TABS)
    tx = MARGIN + 420
    tw = W - MARGIN - tx
    accent = STEP_ACCENTS.get(step["n"])
    # --- measure pass ---
    tlines, tsize = title_from_spec(step["title"], tw, TITLE, accent)
    title_h = len(tlines) * int(tsize * 1.08)
    detail = wrap(d, step["detail"], body(BODY), tw)
    note = wrap(d, step["note"], body(BODY), tw) if step.get("note") else []
    code_lines = None
    if step.get("code"):
        code_lines = step["code"].split("\n") if isinstance(step["code"], str) else step["code"]
        panel_h, _, _ = code_panel_height(d, code_lines, tw - 160)
    cards = step.get("cards")
    cards_h = 0
    if cards:
        cards_h = 2 * 380 + 48
    term = step.get("terminal")
    term_h = 0
    if term:
        term_h, _, _ = code_panel_height(d, term["lines"], tw - 160)
    content_h = (title_h + 50 + len(detail) * int(BODY * 1.45)
                 + (30 + len(note) * int(BODY * 1.45) if note else 0)
                 + (60 + panel_h if code_lines else 0)
                 + (60 + cards_h if cards else 0)
                 + (60 + term_h if term else 0))
    avail = FOOTER_TOP - HEADER_NO_TABS
    y = HEADER_NO_TABS + max(0, (avail - content_h) // 2)
    top = y
    # --- draw pass ---
    num = f"{step['n']:02d}"
    d.text((MARGIN, y), num, font=anton(TITLE), fill=EMERALD)
    lay.add(*text_box(d, MARGIN, y, num, anton(TITLE)), "rail-num")
    y = draw_big_title(d, lay, tlines, tx, y, tsize, th, "step-title")
    y += 50
    y = draw_lines(d, lay, tx, y, detail, body(BODY), th["text"],
                   int(BODY * 1.45), "detail")
    if note:
        y += 30
        y = draw_lines(d, lay, tx, y, note, body(BODY), th["dim"],
                       int(BODY * 1.45), "note")
    if code_lines:
        y += 60
        y = draw_code_panel(d, lay, tx, y, code_lines, tw - 160, th)
    if cards:
        y += 60
        gap = 48
        cw = (tw - gap) // 2
        for i, c in enumerate(cards):
            cx = tx + (i % 2) * (cw + gap)
            cy = y + (i // 2) * (380 + gap)
            hot = bool(c.get("hot"))
            fill = th["hot"] if hot else th["card"]
            chunky(d, (cx, cy, cx + cw, cy + 380), fill, th["border"], th["shadow"])
            lay.add(cx, cy, cx + cw, cy + 380, f"mini-card-{i}")
            d.text((cx + 48, cy + 36), c["title"], font=anton(110),
                   fill=th["hot_text"] if hot else th["card_text"])
            desc = wrap(d, c["desc"], body(72), cw - 96)
            dy = cy + 190
            for ln in desc:
                d.text((cx + 48, dy), ln, font=body(72),
                       fill=th["hot_dim"] if hot else th["dim"])
                dy += 104
        y += cards_h
    if term:
        y += 60
        y = draw_code_panel(d, lay, tx, y, term["lines"], tw - 160, th,
                            label=term.get("label", "terminal"), terminal=True)
    rail_x = MARGIN + 85
    d.line([(rail_x, top + 320), (rail_x, min(y, FOOTER_TOP - 40))], fill=th["border"], width=6)
    lay.check()
    return img


def slide_closing(spec, s, page, total, shortlink):
    th_name = "cream"
    img, d, th = base(th_name, "jalankan", page, total, with_tabs=False)
    lay = Layout(HEADER_NO_TABS)
    # --- measure pass ---
    tlines, tsize = title_from_spec(s["title"], CONTENT_W, COVER_TITLE, "GILIRANMU")
    close_lines = []
    for ln in s["lines"]:
        close_lines.extend(wrap(d, ln, body(BODY), CONTENT_W))
    tip_lines = wrap(d, f"TIPS: {spec['tip']}", body(BODY), CONTENT_W - 160)
    follow = ["Follow @peka.ai.id, edisi Tutorial Agent berikutnya tiap minggu.",
              "Gabung komunitas lewat s.peka.ai.id/gabung.",
              "Save + share kalau tutorialnya kepakai."]
    title_h = len(tlines) * int(tsize * 1.08)
    content_h = (title_h + 60 + (BODY + 4) + 120
                 + len(close_lines) * int(BODY * 1.45) + 60 * len(s["lines"])
                 + (100 + len(tip_lines) * int(BODY * 1.45)) + 80
                 + (100 + len(follow) * int(BODY * 1.45)))
    avail = FOOTER_TOP - HEADER_NO_TABS
    y = HEADER_NO_TABS + max(0, (avail - content_h) // 2)
    # --- draw pass ---
    y = draw_big_title(d, lay, tlines, MARGIN, y, tsize, th, "title")
    y += 60
    short = shortlink.replace("https://", "")
    check_clean(short)
    d.text((MARGIN, y), short, font=f(BODY + 4), fill=EMERALD)
    lay.add(*text_box(d, MARGIN, y, short, f(BODY + 4)), "shortlink")
    y += 120
    for ln in s["lines"]:
        for wln in wrap(d, ln, body(BODY), CONTENT_W):
            check_clean(wln)
            d.text((MARGIN, y), wln, font=body(BODY), fill=th["text"])
            lay.add(*text_box(d, MARGIN, y, wln, body(BODY)), "closing-line")
            y += int(BODY * 1.45)
        y += 60
    y = draw_panel(d, lay, MARGIN, y, tip_lines, th, th["card"], "#F59E0B",
                   th["card_text"], "tip-panel")
    y += 80
    y = draw_panel(d, lay, MARGIN, y, follow, th, th["card"], EMERALD,
                   th["card_text"], "follow-panel")
    lay.check()
    return img


RENDERERS = {
    "cover": slide_cover,
    "step": slide_step,
    "closing": slide_closing,
}


def main():
    spec_path, out_dir = sys.argv[1], sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)
    with open(spec_path, encoding="utf-8") as fh:
        spec = json.load(fh)
    short_path = os.path.join(out_dir, "shortlinks.json")
    if os.path.exists(short_path):
        with open(short_path, encoding="utf-8") as fh:
            shortlink = json.load(fh).get("blog", "https://s.peka.ai.id/contoh")
    else:
        shortlink = "https://s.peka.ai.id/contoh"
        print("WARNING: shortlinks.json tidak ada, pakai placeholder")
    slides = spec["carousel"]["slides"]
    total = len(slides)
    for i, s in enumerate(slides, 1):
        fn = RENDERERS[s["type"]]
        img = fn(spec, s, i, total, shortlink)
        path = os.path.join(out_dir, f"slide-{i}.png")
        img.save(path)
        assert Image.open(path).size == (W, H), f"bad size {path}"
        print(f"slide {i}/{total} ({s['type']}): {path}")


if __name__ == "__main__":
    main()
