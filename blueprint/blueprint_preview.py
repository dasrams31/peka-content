#!/usr/bin/env python3
"""BLUEPRINT series preview - technical-drawing theme for GitHub tool sharing.

Preview only: cover + one content slide (4096x4096) for the Cindy tool.
Design tokens: deep navy, white hairlines, faint grid, steel annotations,
Peka yellow for dimensions and the tool node. Poppins headlines,
DejaVu Sans Mono for annotations. Distinct from SPILL paper and from
Repo of the Week black/gold serif.
"""
import os

from PIL import Image, ImageDraw, ImageFont

OUT = os.path.dirname(os.path.abspath(__file__)) + "/preview"
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


# --- mascot with chroma-key (same source/threshold as spill.py) ---
_m = Image.open("/home/hatch/workspace/peka-logo/mascot-p.png").convert("RGB")
_mmask = Image.new("L", _m.size, 0)
_mp = _m.load()
_mk = _mmask.load()
for _yy in range(_m.size[1]):
    for _xx in range(_m.size[0]):
        _r, _g, _b = _mp[_xx, _yy]
        if _r > 30 or _g > 30 or _b > 30:
            _mk[_xx, _yy] = 255
_creature = _m.crop(_mmask.getbbox())
_cmask = _mmask.crop(_mmask.getbbox())


def lockup(img, d, cy=110, mh=46):
    cy_px, mh_px = X(cy), X(mh)
    cr = _creature.resize((int(_creature.width * mh_px / _creature.height), mh_px), Image.LANCZOS)
    mr = _cmask.resize(cr.size, Image.LANCZOS)
    tf = body(34, True)
    label = "peka.ai.id"
    ascent, descent = tf.getmetrics()
    tx = X(1008) - d.textlength(label, font=tf)
    ty = cy_px - (ascent + descent) // 2
    mx = tx - X(12) - cr.width
    my = cy_px - mh_px // 2 - int(mh_px * 0.03)
    img.paste(cr, (int(mx), int(my)), mr)
    d.text((tx, ty), label, font=tf, fill=WHITE)


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


def dashed_line(d, p0, p1, color, width=3, dash=16, gap=10):
    import math
    x0, y0 = p0
    x1, y1 = p1
    total = math.hypot(x1 - x0, y1 - y0)
    if total == 0:
        return
    step = X(dash + gap)
    done = 0
    while done < total:
        t0 = done / total
        t1 = min((done + X(dash)) / total, 1.0)
        d.line([(x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0),
                (x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1)],
               fill=color, width=X(width))
        done += step


def arrow(d, x0, y0, x1, y1, color, width=4):
    d.line([(x0, y0), (x1, y1)], fill=color, width=X(width))
    ah = X(16)
    d.polygon([(x1, y1), (x1 - ah, y1 - ah // 2), (x1 - ah, y1 + ah // 2)], fill=color)


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
    tf = mono(26)
    label = "4096 x 4096"
    d.text(((W - d.textlength(label, font=tf)) / 2, X(50)), label, font=tf, fill=MUTED)
    return img, d


def header(img, d):
    tf = mono(32, True)
    label = "BLUEPRINT"
    tw = d.textlength(label, font=tf)
    x0, y0 = X(72), X(88)
    x1, y1 = x0 + tw + X(36), y0 + X(56)
    dashed_rect(d, (x0, y0, x1, y1), WHITE, width=3)
    ascent, descent = tf.getmetrics()
    d.text((x0 + X(18), y0 + (X(56) - (ascent + descent)) // 2), label, font=tf, fill=WHITE)
    d.text((x1 + X(16), y0 + (X(56) - (ascent + descent)) // 2), "// TOOLS", font=mono(32), fill=MUTED)
    lockup(img, d)


def footer(d, page, total=2):
    d.line([(X(72), X(984)), (X(1008), X(984))], fill=HAIR, width=X(2))
    d.text((X(72), X(1000)), "GABUNG KE KOMUNITAS KAMI: URL.PEKA.AI.ID", font=mono(27), fill=MUTED)
    label = "%02d / %02d" % (page, total)
    d.text((X(1008) - d.textlength(label, font=mono(27)), X(1000)), label, font=mono(27), fill=MUTED)


def section_label(d, y, text):
    d.text((X(72), X(y)), text, font=mono(36, True), fill=YEL)
    tw = d.textlength(text, font=mono(36, True))
    d.line([(X(72) + tw + X(24), X(y + 24)), (X(1008), X(y + 24))], fill=HAIR, width=X(2))


def chip(d, x, y, text):
    tf = mono(32)
    tw = d.textlength(text, font=tf)
    x1, y1 = x + tw + X(52), y + X(64)
    dashed_rect(d, (x, y, x1, y1), MUTED, width=3)
    ascent, descent = tf.getmetrics()
    d.text((x + X(26), y + (X(64) - (ascent + descent)) // 2), text, font=tf, fill=WHITE)
    return x1


def cover():
    img, d = base()
    header(img, d)
    section_label(d, 212, "01 / GAMBAR KERJA")
    name = "CINDY"
    nf = xb(230)
    ny = X(290)
    d.text((X(72), ny), name, font=nf, fill=WHITE)
    nw = d.textlength(name, font=nf)
    ly = ny + X(268)
    d.line([(X(72), ly), (X(72) + nw, ly)], fill=YEL, width=X(5))
    d.line([(X(72), ly - X(12)), (X(72), ly + X(12))], fill=YEL, width=X(5))
    d.line([(X(72) + nw, ly - X(12)), (X(72) + nw, ly + X(12))], fill=YEL, width=X(5))
    d.text((X(72), ly + X(22)), "makecindy/cindy", font=mono(34), fill=MUTED)
    sub = ["AI agent open source yang jalan di laptop", "dan HP dalam satu session yang nyambung."]
    for i, line in enumerate(sub):
        d.text((X(72), X(640) + i * X(58)), line, font=body(46), fill=WHITE)
    cx = X(72)
    for text in ["TYPESCRIPT", "APACHE-2.0", "8,7RB STAR"]:
        cx = chip(d, cx, X(790), text) + X(28)
    labels = ["INPUT", "TOOL", "OUTPUT"]
    boxes = [("LAPTOP", 250), ("CINDY", 300), ("HP", 250)]
    total_w = sum(w for _, w in boxes) + 2 * 90
    by = X(912)
    x = X(72) + (X(936) - X(total_w)) // 2
    for i, ((text, w), lab) in enumerate(zip(boxes, labels)):
        d.text((x + (X(w) - d.textlength(lab, font=mono(26))) / 2, X(878)), lab, font=mono(26), fill=MUTED)
        if text == "CINDY":
            d.rectangle([x, by, x + X(w), by + X(56)], fill=YEL)
            tf = bold(34)
            d.text((x + (X(w) - d.textlength(text, font=tf)) / 2, by + X(8)), text, font=tf, fill=NAVYTXT)
        else:
            d.rectangle([x, by, x + X(w), by + X(56)], outline=WHITE, width=X(3))
            tf = bold(34)
            d.text((x + (X(w) - d.textlength(text, font=tf)) / 2, by + X(8)), text, font=tf, fill=WHITE)
        if i < 2:
            arrow(d, x + X(w) + X(12), by + X(28), x + X(w) + X(78), by + X(28), YEL, width=4)
        x += X(w) + X(90)
    footer(d, 1)
    img.save(OUT + "/blueprint-cover.png")


def content():
    img, d = base()
    header(img, d)
    section_label(d, 212, "02 / CARA KERJA")
    lines = ["SATU SESSION,", "SEMUA PERANGKAT."]
    size = 118
    while d.textlength(lines[1], font=xb(size)) > X(936) and size > 60:
        size -= 4
    hf = xb(size)
    for i, line in enumerate(lines):
        d.text((X(72), X(280) + i * X(size + 12)), line, font=hf, fill=WHITE)
    d.line([(X(72), X(512)), (X(72) + d.textlength(lines[0], font=hf), X(512))], fill=YEL, width=X(6))
    node = (X(440), X(580), X(640), X(668))
    devices = [
        ((X(80), X(548), X(330), X(636)), "LAPTOP", "komputer kerja"),
        ((X(750), X(548), X(1000), X(636)), "DESKTOP", "desktop rumah"),
        ((X(415), X(740), X(665), X(828)), "HP", "di jalan"),
    ]
    for (box, name, cap) in devices:
        dashed_line(d, ((box[0] + box[2]) // 2, (box[1] + box[3]) // 2),
                    ((node[0] + node[2]) // 2, (node[1] + node[3]) // 2), HAIR, width=3)
    for (box, name, cap) in devices:
        d.rectangle(box, fill=PANEL, outline=WHITE, width=X(3))
        tf = bold(34)
        d.text(((box[0] + box[2] - d.textlength(name, font=tf)) / 2, box[1] + X(10)), name, font=tf, fill=WHITE)
        cf = mono(22)
        d.text(((box[0] + box[2] - d.textlength(cap, font=cf)) / 2, box[1] + X(54)), cap, font=cf, fill=MUTED)
    d.rectangle(node, fill=YEL)
    tf = xb(44)
    d.text(((node[0] + node[2] - d.textlength("CINDY", font=tf)) / 2, node[1] + X(16)), "CINDY", font=tf, fill=NAVYTXT)
    d.text((X(72), X(856)), "Session yang sama lanjut di perangkat lain.", font=body(40), fill=WHITE)
    d.text((X(72), X(906)), "MULAI: download gratis di cindy.app", font=mono(30, True), fill=YEL)
    footer(d, 2)
    img.save(OUT + "/blueprint-cara-kerja.png")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    cover()
    content()
    print("slides OK")
