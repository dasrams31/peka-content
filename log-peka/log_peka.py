#!/usr/bin/env python3
"""LOG PEKA series - honest experiment-log carousel (4096x4096, 4K).

One running experiment per cycle, reported as a numbered day count.
Spec-driven: all edition copy comes from the spec JSON, never hardcoded
here. Design tokens: same navy BLUEPRINT family (deep navy, faint grid,
white hairlines, steel annotations, Peka yellow), but stamp reads
LOG EKSPERIMEN and there is no repo content anywhere.

Usage: python3 log_peka.py <spec.json>
Spec: {"edition": 1, "day": 7, "date_range": "1 - 7 NOV 2026",
  "experiment": "TANPA LINK DI TEKS",
  "title": [...2 lines...], "hypothesis": "...",
  "stats": [{"value": "21", "label": "..."}, x3],
  "compare": "...",
  "findings": [{"title": "...", "desc": "..."}, x3],
  "question": [...2 lines...],
  "out_dir": "/abs/path/carousel"}
Renders 4 slides: log-01.png .. log-04.png.
"""
import json
import os
import sys

S = 4096 / 1080
W = H = 4096

NAVY = "#0A1A30"
PANEL = "#10264A"
GRID = "#1A2E4E"
HAIR = "#3D5A80"
WHITE = "#F2F5F9"
MUTED = "#8FA6C2"
YEL = "#FFD60A"
NAVYTXT = "#0A1A30"

POP_XB = "/home/hatch/workspace/sertiku-poster/fonts/Poppins-ExtraBold.ttf"
POP_B = "/home/hatch/workspace/sertiku-poster/fonts/Poppins-Bold.ttf"
POP_SB = "/home/hatch/workspace/sertiku-poster/fonts/Poppins-SemiBold.ttf"
DSANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DSANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
DMONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
DMONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

from PIL import Image, ImageDraw, ImageFont  # noqa: E402


def X(v):
    return int(round(v * S))


def xb(sz):
    return ImageFont.truetype(POP_XB, X(sz))


def bold(sz):
    return ImageFont.truetype(POP_B, X(sz))


def semibold(sz):
    return ImageFont.truetype(POP_SB, X(sz))


def body(sz, is_bold=False):
    return ImageFont.truetype(DSANS_B if is_bold else DSANS, X(sz))


def mono(sz, is_bold=False):
    return ImageFont.truetype(DMONO_B if is_bold else DMONO, X(sz))


def dashed_rect(d, box, color, width=3, dash=18, gap=12):
    x0, y0, x1, y1 = box
    w = X(width)
    x = x0
    while x < x1:
        d.line([(x, y0), (min(x + X(dash), x1), y0)], fill=color, width=w)
        d.line([(x, y1), (min(x + X(dash), x1), y1)], fill=color, width=w)
        x += X(dash + gap)
    y = y0
    while y < y1:
        d.line([(x0, y), (x0, min(y + X(dash), y1))], fill=color, width=w)
        d.line([(x1, y), (x1, min(y + X(dash), y1))], fill=color, width=w)
        y += X(dash + gap)


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


def base():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    for gx in range(0, 1081, 135):
        d.line([(X(gx), 0), (X(gx), H)], fill=GRID, width=X(1))
    for gy in range(0, 1081, 135):
        d.line([(0, X(gy)), (W, X(gy))], fill=GRID, width=X(1))
    d.rectangle([X(36), X(36), X(1044), X(1044)], outline=HAIR, width=X(3))
    for cx, cy in [(36, 36), (1044, 36), (36, 1044), (1044, 1044)]:
        d.line([(X(cx - 14), X(cy)), (X(cx + 14), X(cy))], fill=YEL, width=X(3))
        d.line([(X(cx), X(cy - 14)), (X(cx), X(cy + 14))], fill=YEL, width=X(3))
    return img, d


def header(img, d):
    tf = mono(32, True)
    label = "LOG EKSPERIMEN"
    tw = d.textlength(label, font=tf)
    x0, y0 = X(72), X(88)
    x1, y1 = x0 + tw + X(36), y0 + X(56)
    dashed_rect(d, (x0, y0, x1, y1), WHITE, width=3)
    ascent, descent = tf.getmetrics()
    d.text((x0 + X(18), y0 + (X(56) - (ascent + descent)) // 2), label, font=tf, fill=WHITE)
    rf = mono(32, True)
    rlabel = "peka.ai.id"
    d.text((X(1008) - d.textlength(rlabel, font=rf), y0 + (X(56) - (ascent + descent)) // 2),
           rlabel, font=rf, fill=WHITE)


def footer(d, page, total=4):
    d.line([(X(72), X(984)), (X(1008), X(984))], fill=HAIR, width=X(2))
    d.text((X(72), X(1000)), "GABUNG KE KOMUNITAS KAMI: URL.PEKA.AI.ID", font=mono(27), fill=MUTED)
    label = "%02d / %02d" % (page, total)
    d.text((X(1008) - d.textlength(label, font=mono(27)), X(1000)), label, font=mono(27), fill=MUTED)


def section_label(d, y, text):
    tf = mono(36, True)
    d.text((X(72), X(y)), text, font=tf, fill=YEL)
    tw = d.textlength(text, font=tf)
    d.line([(X(72) + tw + X(24), X(y + 24)), (X(1008), X(y + 24))], fill=HAIR, width=X(2))


def fit_font(d, lines, start, font_fn, max_w):
    size = start
    while size > 60:
        f = font_fn(size)
        if all(d.textlength(ln, font=f) <= max_w for ln in lines):
            return f
        size -= 4
    return font_fn(60)


def cover(spec, out_dir, page, total):
    img, d = base()
    header(img, d)
    ep = "%02d" % spec["edition"]
    section_label(d, 212, "LOG PEKA / EDISI #%s" % ep)
    dayline = "HARI KE-%d" % spec["day"]
    nf = fit_font(d, [dayline], 230, xb, X(936))
    d.text((X(72), X(300)), dayline, font=nf, fill=WHITE)
    ink = d.textbbox((0, 0), dayline, font=nf)
    ly = 300 + ink[3] / S + 16
    nw = d.textlength(dayline, font=nf)
    d.line([(X(72), X(ly)), (X(72) + nw, X(ly))], fill=YEL, width=X(5))
    d.line([(X(72), X(ly) - X(12)), (X(72), X(ly) + X(12))], fill=YEL, width=X(5))
    d.line([(X(72) + nw, X(ly) - X(12)), (X(72) + nw, X(ly) + X(12))], fill=YEL, width=X(5))
    d.text((X(72), X(ly) + X(22)), "EKSPERIMEN: " + spec["experiment"], font=mono(34), fill=MUTED)
    for i, line in enumerate(spec["title"]):
        d.text((X(72), X(660) + i * X(58)), line, font=body(46), fill=WHITE)
    hyp = wrap(d, "HIPOTESA: " + spec["hypothesis"], mono(28), X(880))[:3]
    box_h = X(24 + len(hyp) * 40 + 24)
    y0 = X(800)
    dashed_rect(d, (X(72), y0, X(1008), y0 + box_h), HAIR, width=3)
    for i, line in enumerate(hyp):
        d.text((X(72) + X(28), y0 + X(24) + i * X(40)), line, font=mono(28), fill=MUTED)
    d.text((X(72), X(948)), spec["date_range"], font=mono(28, True), fill=YEL)
    footer(d, page, total)
    img.save(out_dir + "/log-%02d.png" % page)


def numbers(spec, out_dir, page, total):
    img, d = base()
    header(img, d)
    section_label(d, 212, "ANGKA %s" % spec["date_range"])
    y = 280
    for i, st in enumerate(spec["stats"]):
        vf = fit_font(d, [st["value"]], 120, xb, X(380))
        ascent, descent = vf.getmetrics()
        d.text((X(72), X(y) + (X(150) - (ascent + descent)) // 2), st["value"], font=vf, fill=YEL)
        lab = wrap(d, st["label"], body(40), X(488))[:3]
        for j, line in enumerate(lab):
            d.text((X(500), X(y) + X(28) + j * X(48)), line, font=body(40), fill=WHITE)
        if i < 2:
            d.line([(X(72), X(y + 170)), (X(1008), X(y + 170))], fill=HAIR, width=X(2))
        y += 180
    comp = wrap(d, spec["compare"], mono(30), X(880))[:2]
    box_h = X(24 + len(comp) * 42 + 24)
    y0 = X(830)
    dashed_rect(d, (X(72), y0, X(1008), y0 + box_h), HAIR, width=3)
    for i, line in enumerate(comp):
        d.text((X(72) + X(28), y0 + X(24) + i * X(42)), line, font=mono(30), fill=WHITE)
    footer(d, page, total)
    img.save(out_dir + "/log-%02d.png" % page)


def findings(spec, out_dir, page, total):
    img, d = base()
    header(img, d)
    section_label(d, 212, "YANG KAMI TEMUIN")
    y = 290
    for i, f in enumerate(spec["findings"]):
        d.text((X(72), X(y)), "%02d" % (i + 1), font=mono(40, True), fill=YEL)
        d.text((X(190), X(y)), f["title"], font=bold(44), fill=WHITE)
        desc = wrap(d, f["desc"], body(38), X(818))[:3]
        for j, line in enumerate(desc):
            d.text((X(190), X(y) + X(62) + j * X(46)), line, font=body(38), fill=MUTED)
        if i < 2:
            d.line([(X(72), X(y + 205)), (X(1008), X(y + 205))], fill=HAIR, width=X(2))
        y += 225
    footer(d, page, total)
    img.save(out_dir + "/log-%02d.png" % page)


def closing(spec, out_dir, page, total):
    img, d = base()
    header(img, d)
    section_label(d, 212, "LANJUT?")
    qf = fit_font(d, spec["question"], 120, xb, X(936))
    for i, line in enumerate(spec["question"]):
        d.text((X(72), X(300) + i * X(132)), line, font=qf, fill=WHITE)
    rows = [
        ("FOLLOW", "Follow @peka.ai.id di IG, Threads, TikTok."),
        ("GABUNG", "Gabung grup WA lewat url.peka.ai.id."),
        ("SAVE", "Save dan share biar makin banyak yang kebantu."),
    ]
    y = 620
    for label, text in rows:
        dashed_rect(d, (X(72), X(y), X(1008), X(y + 88)), HAIR, width=3)
        tf = mono(30, True)
        ascent, descent = tf.getmetrics()
        ty = X(y) + (X(88) - (ascent + descent)) // 2
        lx = X(72) + X(28)
        d.text((lx, ty), label, font=tf, fill=YEL)
        tx = lx + d.textlength(label, font=tf) + X(28)
        size = 34
        rf = body(size)
        while size > 26 and d.textlength(text, font=rf) > X(1008) - X(28) - tx:
            size -= 2
            rf = body(size)
        d.text((tx, ty), text, font=rf, fill=WHITE)
        y += 112
    footer(d, page, total)
    img.save(out_dir + "/log-%02d.png" % page)


def main():
    with open(sys.argv[1], encoding="utf-8") as fh:
        spec = json.load(fh)
    assert len(spec["stats"]) == 3, "LOG PEKA needs exactly 3 stats"
    assert len(spec["findings"]) == 3, "LOG PEKA needs exactly 3 findings"
    assert len(spec["title"]) <= 2, "title max 2 lines"
    assert len(spec["question"]) <= 2, "question max 2 lines"
    out_dir = spec["out_dir"]
    os.makedirs(out_dir, exist_ok=True)
    cover(spec, out_dir, 1, 4)
    numbers(spec, out_dir, 2, 4)
    findings(spec, out_dir, 3, 4)
    closing(spec, out_dir, 4, 4)
    print("done 4 slides -> %s" % out_dir)


main()
