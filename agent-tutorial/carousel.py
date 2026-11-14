#!/usr/bin/env python3
"""Carousel designer for Tutorial Agent Peka editions (agent-console theme).

Square 4096x4096 PIL slides, driven by the "carousel" section of the
edition spec.json plus spec["steps"]:
  {"slides": [{"type": "cover", "title": [...], "sub": "...",
               "try_now": "COBA SEKARANG: ...", "result": "HASIL AKHIR: ..."},
              {"type": "step", "step": 1},
              ...
              {"type": "closing", "title": [...], "lines": [...]}]}
Usage: python3 carousel.py <spec.json> <out_dir>
Writes slide-1.png .. slide-6.png into the out dir.

Visual identity (agent-console, distinct from Peka yellow/black and from
HM premium warm paper):
  dark slate console #0D1117, flat panels #161B22 with 1px #30363D
  borders, emerald #10B981 for active/done steps, amber #F59E0B
  sparingly for warnings, white/slate text, monospace for code,
  commands and paths, numbered step rail on the left, fixed grid with
  a reserved footer strip, no gradients, no glows, no dead gaps.

Layout QA (special/DESIGN_RULES.md): every text/panel box is recorded
and checked before the PNG is saved: boxes must stay inside the content
area (above the reserved footer strip) and must not overlap each other.
One violation aborts the render. Max 3 text sizes per slide. Leftover
vertical space is shared out (cover/closing blocks are spaced to end
near the footer strip; step slides are vertically centred).
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "animated", "assets")
W = H = 4096
BG = "#0D1117"
PANEL = "#161B22"
BORDER = "#30363D"
INK = "#F0F6FC"
SLATE = "#8B949E"
EMERALD = "#10B981"
AMBER = "#F59E0B"
MARGIN = 240
CONTENT_W = W - 2 * MARGIN
HEADER_BOTTOM = 420
FOOTER_TOP = H - 340
TITLE = 170
COVER_TITLE = 200
BODY = 92
META = 56
CODE_FLOOR = 52


def _font(name, size):
    return ImageFont.truetype(os.path.join(ASSETS, name), size)


def f(sz):
    return _font("Poppins-Bold.ttf", sz)


def body(sz):
    return _font("DejaVuSans.ttf", sz)


def mono(sz, bold=False):
    return _font("DejaVuSansMono-Bold.ttf" if bold else "DejaVuSansMono.ttf", sz)


def check_clean(text):
    assert "\u2014" not in text and "\u2013" not in text, f"dash terlarang: {text[:60]}"


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

    def __init__(self):
        self.boxes = []

    def add(self, x0, y0, x1, y1, label):
        assert x0 >= MARGIN - 1, f"{label}: keluar kiri ({x0})"
        assert x1 <= W - MARGIN + 1, f"{label}: keluar kanan ({x1})"
        assert y0 >= HEADER_BOTTOM - 1, f"{label}: nabrak header ({y0})"
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
    bb = d.textbbox((x, y), text, font=font)
    return bb[0], bb[1], bb[2], bb[3]


def draw_lines(d, lay, x, y, lines, font, fill, lh, label):
    """Draw wrapped lines, register one box per line, return bottom y."""
    for ln in lines:
        check_clean(ln)
        d.text((x, y), ln, font=font, fill=fill)
        lay.add(*text_box(d, x, y, ln, font), label)
        y += lh
    return y


def title_lines(d, title, x, size):
    """Resolve a title to display lines (explicit list or wrapped),
    shrinking until it fits in 3 lines."""
    max_w = W - MARGIN - x
    lines = title if isinstance(title, list) else wrap(d, title, f(size), max_w)
    while len(lines) > 3 and size > 120:
        size -= 10
        lines = title if isinstance(title, list) else wrap(d, title, f(size), max_w)
        if isinstance(title, list):
            break
    return lines, size


def draw_title(d, lay, title, x, y, size, label="title"):
    lines, size = title_lines(d, title, x, size)
    return draw_lines(d, lay, x, y, lines, f(size), INK,
                      int(size * 1.12), label)


def base(page, total):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((MARGIN, 150), "TUTORIAL AGENT PEKA", font=mono(64, True), fill=EMERALD)
    d.rectangle([(W - MARGIN - 460, 158), (W - MARGIN - 420, 198)], fill=EMERALD)
    d.text((W - MARGIN - 400, 150), "peka.ai.id", font=f(72), fill=INK)
    d.line([(MARGIN, 380), (W - MARGIN, 380)], fill=BORDER, width=4)
    d.rectangle([(MARGIN, 380), (MARGIN + 320, 380)], fill=EMERALD, width=4)
    d.text((MARGIN, H - 200), "Follow @peka.ai.id  -  Gabung: s.peka.ai.id/gabung",
           font=body(META), fill=SLATE)
    d.text((W - MARGIN - 300, H - 200), f"{page}/{total}", font=mono(META, True), fill=SLATE)
    return img, d


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


def draw_code_panel(d, lay, x, y, code_lines, max_w):
    panel_h, size, lines = code_panel_height(d, code_lines, max_w)
    font = mono(size)
    lh = int(size * 1.45)
    assert y + panel_h <= FOOTER_TOP, "panel kode kepanjangan, pendekkan code di spec"
    d.rounded_rectangle([(x, y), (W - MARGIN, y + panel_h)], radius=32,
                        fill=PANEL, outline=BORDER, width=4)
    lay.add(x, y, W - MARGIN, y + panel_h, "code-panel")
    d.ellipse([(x + 70, y + 62), (x + 110, y + 102)], fill="#ff5f57")
    d.ellipse([(x + 140, y + 62), (x + 180, y + 102)], fill="#febc2e")
    d.ellipse([(x + 210, y + 62), (x + 250, y + 102)], fill="#28c840")
    d.text((x + 300, y + 52), "terminal", font=mono(64, True), fill=SLATE)
    ly = y + 180
    for ln in lines:
        d.text((x + 80, ly), ln, font=font, fill=EMERALD)
        ly += lh
    return y + panel_h


def slide_cover(spec, s, page, total, shortlink):
    img, d = base(page, total)
    lay = Layout()
    # --- measure pass: total content height, then centre vertically ---
    tlines, tsize = title_lines(d, s["title"], MARGIN, COVER_TITLE)
    sub_lines = wrap(d, s["sub"], body(BODY), CONTENT_W)
    try_lines = wrap(d, s["try_now"], body(BODY), CONTENT_W - 160)
    info = f"{len(spec['steps'])} LANGKAH   |   BUTUH: {'  -  '.join(spec['prerequisites'])}"
    info_lines = wrap(d, info, mono(64, True), CONTENT_W)
    result_lines = wrap(d, s["result"], body(BODY), CONTENT_W - 160) if s.get("result") else []
    total_h = (64 + 150 + len(tlines) * int(tsize * 1.12) + 40
               + len(sub_lines) * int(BODY * 1.45) + 60
               + (100 + len(try_lines) * int(BODY * 1.45)) + 90
               + len(info_lines) * 110 + 60 + (64 + 130)
               + len(spec["steps"]) * 185 + 140
               + (100 + len(result_lines) * int(BODY * 1.45)))
    avail = FOOTER_TOP - HEADER_BOTTOM
    y = HEADER_BOTTOM + max(0, (avail - total_h) // 2)
    # --- draw pass ---
    meta = f"EDISI #{spec['episode']:02d}  -  {spec['date']}"
    d.text((MARGIN, y), meta, font=mono(64, True), fill=AMBER)
    lay.add(*text_box(d, MARGIN, y, meta, mono(64, True)), "meta")
    y += 150
    y = draw_lines(d, lay, MARGIN, y, tlines, f(tsize), INK,
                   int(tsize * 1.12), "title") + 40
    for ln in sub_lines:
        check_clean(ln)
        d.text((MARGIN, y), ln, font=body(BODY), fill=SLATE)
        lay.add(*text_box(d, MARGIN, y, ln, body(BODY)), "sub")
        y += int(BODY * 1.45)
    y += 60
    # try-now panel: one concrete first action, emerald border
    check_clean(s["try_now"])
    panel_h = 100 + len(try_lines) * int(BODY * 1.45)
    d.rounded_rectangle([(MARGIN, y), (W - MARGIN, y + panel_h)], radius=32,
                        fill=PANEL, outline=EMERALD, width=5)
    lay.add(MARGIN, y, W - MARGIN, y + panel_h, "try-panel")
    ty = y + 50
    for ln in try_lines:
        d.text((MARGIN + 80, ty), ln, font=body(BODY), fill=INK)
        ty += int(BODY * 1.45)
    y += panel_h + 90
    for ln in info_lines:
        d.text((MARGIN, y), ln, font=mono(64, True), fill=SLATE)
        lay.add(*text_box(d, MARGIN, y, ln, mono(64, True)), "info")
        y += 110
    # step preview: what is inside this edition
    y += 60
    head = "DI EDISI INI"
    d.text((MARGIN, y), head, font=mono(64, True), fill=AMBER)
    lay.add(*text_box(d, MARGIN, y, head, mono(64, True)), "preview-head")
    y += 130
    for st in spec["steps"]:
        num = f"{st['n']:02d}"
        d.text((MARGIN, y), num, font=mono(BODY, True), fill=EMERALD)
        lay.add(*text_box(d, MARGIN, y, num, mono(BODY, True)), "preview-num")
        d.text((MARGIN + 220, y), st["title"], font=body(BODY), fill=INK)
        lay.add(*text_box(d, MARGIN + 220, y, st["title"], body(BODY)), "preview-title")
        y += 185
    # result panel follows the preview directly
    if result_lines:
        check_clean(s["result"])
        y += 140
        panel_h = 100 + len(result_lines) * int(BODY * 1.45)
        d.rounded_rectangle([(MARGIN, y), (W - MARGIN, y + panel_h)], radius=32,
                            fill=PANEL, outline=EMERALD, width=5)
        lay.add(MARGIN, y, W - MARGIN, y + panel_h, "result-panel")
        ty = y + 50
        for ln in result_lines:
            d.text((MARGIN + 80, ty), ln, font=body(BODY), fill=INK)
            ty += int(BODY * 1.45)
    lay.check()
    return img


def slide_step(spec, s, page, total, shortlink):
    step = spec["steps"][s["step"] - 1]
    assert step["n"] == s["step"], "nomor langkah tidak cocok dengan spec"
    img, d = base(page, total)
    lay = Layout()
    tx = MARGIN + 360
    tw = W - MARGIN - tx
    # --- measure pass: total content height, then centre vertically ---
    tlines, tsize = title_lines(d, step["title"], tx, TITLE)
    content_h = len(tlines) * int(tsize * 1.12) + 50
    detail = wrap(d, step["detail"], body(BODY), tw)
    content_h += len(detail) * int(BODY * 1.45)
    note = wrap(d, step["note"], body(BODY), tw) if step.get("note") else []
    if note:
        content_h += 30 + len(note) * int(BODY * 1.45)
    code_lines = None
    if step.get("code"):
        code_lines = step["code"].split("\n") if isinstance(step["code"], str) else step["code"]
        panel_h, _, _ = code_panel_height(d, code_lines, tw - 160)
        content_h += 60 + panel_h
    avail = FOOTER_TOP - HEADER_BOTTOM
    y = HEADER_BOTTOM + max(0, (avail - content_h) // 2)
    top = y
    # --- draw pass ---
    rail_x = MARGIN + 85
    num = f"{step['n']:02d}"
    d.text((MARGIN, y), num, font=f(TITLE), fill=EMERALD)
    lay.add(*text_box(d, MARGIN, y, num, f(TITLE)), "rail-num")
    y = draw_lines(d, lay, tx, y, tlines, f(tsize), INK,
                   int(tsize * 1.12), "step-title") + 50
    y = draw_lines(d, lay, tx, y, detail, body(BODY), INK,
                   int(BODY * 1.45), "detail")
    if note:
        y += 30
        y = draw_lines(d, lay, tx, y, note, body(BODY), SLATE,
                       int(BODY * 1.45), "note")
    if code_lines:
        y += 60
        y = draw_code_panel(d, lay, tx, y, code_lines, tw - 160)
    d.line([(rail_x, top + 240), (rail_x, min(y, FOOTER_TOP - 40))], fill=BORDER, width=4)
    lay.check()
    return img


def slide_closing(spec, s, page, total, shortlink):
    img, d = base(page, total)
    lay = Layout()
    # --- measure pass: total content height, then centre vertically ---
    tlines, tsize = title_lines(d, s["title"], MARGIN, TITLE)
    close_lines = []
    for ln in s["lines"]:
        close_lines.extend(wrap(d, ln, body(BODY), CONTENT_W))
    tip_lines = wrap(d, f"TIPS: {spec['tip']}", body(BODY), CONTENT_W - 160)
    follow = ["Follow @peka.ai.id, edisi Tutorial Agent berikutnya tiap minggu.",
              "Gabung komunitas lewat s.peka.ai.id/gabung.",
              "Save + share kalau tutorialnya kepakai."]
    total_h = (len(tlines) * int(tsize * 1.12) + 60 + (BODY + 4) + 260
               + len(close_lines) * int(BODY * 1.45) + 60 * len(s["lines"])
               + (100 + len(tip_lines) * int(BODY * 1.45)) + 90
               + (100 + len(follow) * int(BODY * 1.45)))
    avail = FOOTER_TOP - HEADER_BOTTOM
    y = HEADER_BOTTOM + max(0, (avail - total_h) // 2)
    # --- draw pass ---
    y = draw_lines(d, lay, MARGIN, y, tlines, f(tsize), INK,
                   int(tsize * 1.12), "title") + 60
    # proportional bold, not mono: a monospace font gives every "."
    # a full-width cell, so s.peka.ai.id renders spaced out
    short = shortlink.replace("https://", "")
    check_clean(short)
    d.text((MARGIN, y), short, font=f(BODY + 4), fill=EMERALD)
    lay.add(*text_box(d, MARGIN, y, short, f(BODY + 4)), "shortlink")
    y += 260
    for ln in s["lines"]:
        for wln in wrap(d, ln, body(BODY), CONTENT_W):
            check_clean(wln)
            d.text((MARGIN, y), wln, font=body(BODY), fill=INK)
            lay.add(*text_box(d, MARGIN, y, wln, body(BODY)), "closing-line")
            y += int(BODY * 1.45)
        y += 60
    # tip panel: the one tip from the spec
    check_clean(spec["tip"])
    panel_h = 100 + len(tip_lines) * int(BODY * 1.45)
    d.rounded_rectangle([(MARGIN, y), (W - MARGIN, y + panel_h)], radius=32,
                        fill=PANEL, outline=AMBER, width=5)
    lay.add(MARGIN, y, W - MARGIN, y + panel_h, "tip-panel")
    ty = y + 50
    for ln in tip_lines:
        d.text((MARGIN + 80, ty), ln, font=body(BODY), fill=INK)
        ty += int(BODY * 1.45)
    y += panel_h + 90
    # follow panel: the closing CTA
    for ln in follow:
        check_clean(ln)
    panel_h = 100 + len(follow) * int(BODY * 1.45)
    d.rounded_rectangle([(MARGIN, y), (W - MARGIN, y + panel_h)], radius=32,
                        fill=PANEL, outline=EMERALD, width=5)
    lay.add(MARGIN, y, W - MARGIN, y + panel_h, "follow-panel")
    ty = y + 50
    for ln in follow:
        d.text((MARGIN + 80, ty), ln, font=body(BODY), fill=INK)
        ty += int(BODY * 1.45)
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
