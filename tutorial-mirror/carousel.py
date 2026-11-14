#!/usr/bin/env python3
"""Threads carousel designer for tutorial-mirror editions.

Peka yellow/black theme (NOT the HM premium paper theme, NOT the SPILL
paper theme). Square 4096x4096 PIL slides, driven by the "carousel"
section of the edition spec.json:
  {"slides": [{"type": "cover", "title": [...], "sub": "..."},
              {"type": "points", "title": "...",
               "items": [{"head": "...", "body": "..."}]},
              {"type": "text", "title": "...", "body": "...",
               "code": "posts.user_id REFERENCES users(id)"},
              {"type": "code", "title": "...", "code": [...lines],
               "note": "..."},
              {"type": "closing", "title": "...", "shortlink": "...",
               "lines": [...]}]}
Usage: python3 carousel.py <spec.json> <out_dir>
Writes slide-1.png .. slide-N.png into the out dir.
Guards: no em-dash / en-dash anywhere; code lines are shrunk to a
52px floor and wrapped onto a second line instead of being clipped
(same fix as spill_repo_carousel.py, Nov 2026).
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "animated", "assets")
W = H = 4096
BG = "#111111"
CARD = "#1b1b1b"
YELLOW = "#ffd60a"
INK = "#f5f1e8"
GRAY = "#8a8a8a"
HAIR = "#2a2a2a"
MARGIN = 240
CONTENT_W = W - 2 * MARGIN


def _font(name, size):
    return ImageFont.truetype(os.path.join(ASSETS, name), size)


def f(sz, bold=True):
    return _font("Poppins-Bold.ttf" if bold else "Poppins-SemiBold.ttf", sz)


def body(sz):
    return _font("DejaVuSans.ttf", sz)


def mono(sz, bold=False):
    return _font("DejaVuSansMono-Bold.ttf" if bold else "DejaVuSansMono.ttf", sz)


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


def check_clean(text):
    assert "\u2014" not in text and "\u2013" not in text, f"dash terlarang: {text[:60]}"


def base(page, total):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((MARGIN, 150), "TUTORIAL PEKA", font=mono(72, True), fill=YELLOW)
    # lockup mascot sized to fit fully above the rule (mascot is tall,
    # aspect h/w ~2.22, so width follows from a 230px height budget)
    mas = Image.open(os.path.join(ASSETS, "mascot-p-clear.png")).convert("RGBA")
    mas_h = 230
    mas_w = int(mas_h * mas.width / mas.height)
    mas = mas.resize((mas_w, mas_h))
    img.paste(mas, (W - MARGIN - mas_w - 420, 140), mas)
    d.text((W - MARGIN - 400, 165), "peka.ai.id", font=f(84), fill=INK)
    d.line([(MARGIN, 380), (W - MARGIN, 380)], fill=HAIR, width=6)
    d.rectangle([(MARGIN, 380), (MARGIN + 320, 380)], fill=YELLOW, width=6)
    d.text((MARGIN, H - 200), "Follow @peka.ai.id  -  Gabung: s.peka.ai.id/gabung",
           font=body(56), fill=GRAY)
    d.text((W - MARGIN - 300, H - 200), f"{page}/{total}", font=mono(56, True), fill=GRAY)
    return img, d


def draw_title(d, title, y, size=170):
    lines = title if isinstance(title, list) else wrap(d, title, f(size), CONTENT_W)
    for ln in lines:
        check_clean(ln)
        d.text((MARGIN, y), ln, font=f(size), fill=INK)
        y += int(size * 1.15)
    return y


def slide_cover(spec, page, total):
    img, d = base(page, total)
    y = 560
    y = draw_title(d, spec["title"], y, 200)
    for ln in wrap(d, spec["sub"], body(96), CONTENT_W):
        check_clean(ln)
        d.text((MARGIN, y + 40), ln, font=body(96), fill=GRAY)
        y += 140
    # big mascot, fully inside the canvas (bottom above the footer)
    mas = Image.open(os.path.join(ASSETS, "mascot-p-clear.png")).convert("RGBA")
    big_h = int(900 * mas.height / mas.width)
    mas = mas.resize((900, big_h))
    img.paste(mas, (W - MARGIN - 900, H - 260 - big_h), mas)
    d.text((MARGIN, H - 420), "Tutorial dari blog ramadanadipa.com,",
           font=body(72), fill=GRAY)
    d.text((MARGIN, H - 330), "ditulis ulang buat kamu.", font=body(72), fill=GRAY)
    return img


def slide_points(spec, page, total):
    img, d = base(page, total)
    y = draw_title(d, spec["title"], 520, 170) + 60
    for i, item in enumerate(spec["items"]):
        check_clean(item["head"])
        check_clean(item["body"])
        d.text((MARGIN, y), f"{i + 1}", font=f(150), fill=YELLOW)
        d.text((MARGIN + 260, y + 18), item["head"], font=f(110), fill=INK)
        y += 210
        for ln in wrap(d, item["body"], body(92), CONTENT_W - 260):
            d.text((MARGIN + 260, y), ln, font=body(92), fill=INK)
            y += 132
        y += 90
    return img


def slide_text(spec, page, total):
    img, d = base(page, total)
    y = draw_title(d, spec["title"], 520, 170) + 60
    for ln in wrap(d, spec["body"], body(96), CONTENT_W):
        check_clean(ln)
        d.text((MARGIN, y), ln, font=body(96), fill=INK)
        y += 140
    if spec.get("code"):
        code = spec["code"]
        check_clean(code)
        size = 88
        while size > 52 and d.textlength(code, font=mono(size, True)) > CONTENT_W - 160:
            size -= 4
        y += 60
        d.rounded_rectangle([(MARGIN, y), (W - MARGIN, y + 260)], radius=40, fill=CARD,
                            outline=YELLOW, width=6)
        d.text((MARGIN + 80, y + 78), code, font=mono(size, True), fill=YELLOW)
    return img


def fit_code_lines(d, lines, max_w):
    """Shrink mono size to a 52px floor; wrap any line still too wide.

    Returns (font_size, display_lines). Same no-clip rule as the
    spill_repo_carousel.py fix: never cut a command, wrap it instead.
    """
    size = 76
    while size > 52 and any(
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


def slide_code(spec, page, total):
    img, d = base(page, total)
    y = draw_title(d, spec["title"], 520, 170) + 60
    inner = CONTENT_W - 160
    size, lines = fit_code_lines(d, spec["code"], inner)
    font = mono(size)
    panel_h = 200 + len(lines) * int(size * 1.45)
    d.rounded_rectangle([(MARGIN, y), (W - MARGIN, y + panel_h)], radius=40,
                        fill=CARD, outline=YELLOW, width=6)
    d.ellipse([(MARGIN + 70, y + 62), (MARGIN + 110, y + 102)], fill="#ff5f57")
    d.ellipse([(MARGIN + 140, y + 62), (MARGIN + 180, y + 102)], fill="#febc2e")
    d.ellipse([(MARGIN + 210, y + 62), (MARGIN + 250, y + 102)], fill="#28c840")
    d.text((MARGIN + 300, y + 52), "terminal", font=mono(64, True), fill=GRAY)
    ly = y + 180
    for ln in lines:
        d.text((MARGIN + 80, ly), ln, font=font, fill=INK)
        ly += int(size * 1.45)
    if spec.get("note"):
        ny = y + panel_h + 70
        for ln in wrap(d, spec["note"], body(88), CONTENT_W):
            check_clean(ln)
            d.text((MARGIN, ny), ln, font=body(88), fill=GRAY)
            ny += 130
    return img


def slide_closing(spec, page, total):
    img, d = base(page, total)
    y = draw_title(d, spec["title"], 560, 190) + 40
    short = spec["shortlink"].replace("https://", "")
    # proportional bold, not mono: a monospace font gives every "." a
    # full-width cell, so s.peka.ai.id renders as "s . peka . ai . id"
    d.text((MARGIN, y + 60), short, font=f(120), fill=YELLOW)
    y += 320
    for ln in spec["lines"]:
        check_clean(ln)
        for wln in wrap(d, ln, body(96), CONTENT_W):
            d.text((MARGIN, y), wln, font=body(96), fill=INK)
            y += 140
        y += 30
    return img


RENDERERS = {
    "cover": slide_cover,
    "points": slide_points,
    "text": slide_text,
    "code": slide_code,
    "closing": slide_closing,
}


def main():
    spec_path, out_dir = sys.argv[1], sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)
    with open(spec_path, encoding="utf-8") as fh:
        spec = json.load(fh)
    slides = spec["carousel"]["slides"]
    total = len(slides)
    for i, s in enumerate(slides, 1):
        fn = RENDERERS[s["type"]]
        img = fn(s, i, total)
        path = os.path.join(out_dir, f"slide-{i}.png")
        img.save(path)
        assert Image.open(path).size == (W, H), f"bad size {path}"
        print(f"slide {i}/{total} ({s['type']}): {path}")


if __name__ == "__main__":
    main()
