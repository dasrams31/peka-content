#!/usr/bin/env python3
"""Bansos ticket-design carousel generator (3 slides, 2048x2048).

Design identity for Peka bansos posts: a physical aid ticket / coupon.
Slide 1: cream ticket on black (perforation, stub with barcode, red
GRATIS stamp, ticket fields). Slide 2: requirements + claim steps on
ticket cards. Slide 3: yellow closing ticket with CTA rows.
Locked Peka lockup top-right on every slide.

Usage: python3 bansos_design.py <spec.json>
Spec: {"program": "...", "category": "VPS / CLOUD", "stamp": "100% GRATIS",
       "fields": {"nilai": "...", "deadline": "...", "untuk": "...",
                  "sumber": "..."},
       "syarat": ["...", ...], "steps": ["...", ...],
       "band": "VPS ORACLE - GRATIS SELAMANYA", "out_dir": "/abs/path"}
"""
import hashlib
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

S = 2048
YELLOW = (255, 214, 10)
BLACK = (17, 17, 17)
INK = (22, 22, 22)
CREAM = (255, 253, 244)
WHITE = (255, 255, 255)
GRAY = (150, 150, 142)
DGRAY = (105, 105, 98)
RED = (214, 48, 38)
SHADOW = (52, 52, 52)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FM = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FMB = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def f(sz):
    return ImageFont.truetype(FB, sz)


def fr(sz):
    return ImageFont.truetype(FR, sz)


def mono(sz, bold=False):
    return ImageFont.truetype(FMB if bold else FM, sz)


# --- mascot with chroma-key (same source as spill/spill.py) ---
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


def lockup(img, cy, mh, color, chip=None):
    d = ImageDraw.Draw(img)
    cr = _creature.resize((int(_creature.width * mh / _creature.height), mh), Image.LANCZOS)
    mr = _cmask.resize(cr.size, Image.LANCZOS)
    tf = f(int(mh * 0.74))
    label = "peka.ai.id"
    ascent, descent = tf.getmetrics()
    tx = 1938 - d.textlength(label, font=tf)
    ty = cy - (ascent + descent) // 2
    mx = int(tx - 26 - cr.width)
    my = cy - mh // 2
    if chip is not None:
        pad = 20
        d.rounded_rectangle([mx - pad, my - pad, mx + cr.width + pad, my + mh + pad],
                            radius=34, fill=chip)
    img.paste(cr, (mx, my), mr)
    d.text((tx, ty), label, font=tf, fill=color)


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


def dashed_v(d, x, y0, y1, color, dash=26, gap=18, width=5):
    y = y0
    while y < y1:
        d.line([x, y, x, min(y + dash, y1)], fill=color, width=width)
        y += dash + gap


def dashed_h(d, y, x0, x1, color, dash=26, gap=18, width=5):
    x = x0
    while x < x1:
        d.line([x, y, min(x + dash, x1), y], fill=color, width=width)
        x += dash + gap


def pill(d, x, y, text, font, fill=None, txt=None, outline=None, pad_x=32, pad_y=15):
    tw = d.textlength(text, font=font)
    ascent, descent = font.getmetrics()
    th = ascent + descent
    box = [x, y, x + tw + pad_x * 2, y + th + pad_y * 2]
    d.rounded_rectangle(box, radius=(box[3] - box[1]) // 2, fill=fill, outline=outline,
                        width=5 if outline else 1)
    d.text((x + pad_x, y + pad_y - 2), text, font=font, fill=txt)
    return box[2]


def stamp(d, cx, cy, text):
    """Red double-outline GRATIS stamp, rotated -8 degrees, drawn in place."""
    tf = f(64)
    tw = d.textlength(text, font=tf)
    w, h = int(tw + 84), 138
    layer = Image.new("RGBA", (w + 60, h + 60), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rounded_rectangle([30, 30, 30 + w, 30 + h], radius=26, outline=RED, width=9)
    ld.rounded_rectangle([48, 48, 30 + w - 18, 30 + h - 18], radius=18, outline=RED, width=4)
    ld.text((30 + (w - tw) / 2, 30 + 34), text, font=tf, fill=RED)
    layer = layer.rotate(8, resample=Image.BICUBIC, expand=True)
    return layer, (int(cx - layer.width / 2), int(cy - layer.height / 2))


def barcode(d, x, y, w, h, seed_text):
    seed = int(hashlib.md5(seed_text.encode()).hexdigest()[:8], 16)
    cx = x
    i = 0
    while cx < x + w - 8:
        seed = (seed * 1103515245 + 12345) % (2 ** 31)
        bw = 4 + (seed % 4) * 4
        if i % 2 == 0:
            d.rectangle([cx, y, cx + bw, y + h], fill=INK)
        cx += bw + 5
        i += 1


def slide1_photo(spec):
    """Slide 1 variant for bansos items that ship with their own image:
    the ticket gains a framed photo window right of the title."""
    img = Image.new("RGB", (S, S), BLACK)
    d = ImageDraw.Draw(img)
    lockup(img, cy=128, mh=104, color=YELLOW)
    d.text((110, 96), "INFO BANTUAN GRATIS", font=mono(46, bold=True), fill=YELLOW)
    d.text((110, 158), "buat yang lagi butuh, bukan buat yang lagi iseng",
           font=fr(44), fill=GRAY)

    TW, TH = 1830, 1150
    layer = Image.new("RGBA", (TW + 220, TH + 240), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ox, oy = 110, 100
    ld.rounded_rectangle([ox + 16, oy + 26, ox + TW + 16, oy + TH + 26], radius=40, fill=SHADOW)
    ld.rounded_rectangle([ox, oy, ox + TW, oy + TH], radius=40, fill=CREAM)
    perf_x = ox + TW - 470
    dashed_v(ld, perf_x, oy + 60, oy + TH - 60, DGRAY)
    for yy in (oy, oy + TH):
        ld.ellipse([perf_x - 36, yy - 36, perf_x + 36, yy + 36], fill=BLACK)

    mx = ox + 80
    x = pill(ld, mx, oy + 64, "BANSOS", f(50), fill=BLACK, txt=YELLOW)
    pill(ld, x + 24, oy + 64, spec["category"].upper(), f(50), fill=None, txt=INK, outline=INK)

    title_lines = wrap(ld, spec["program"], f(92), 640)
    if len(title_lines) > 4:
        raise SystemExit("OVERFLOW: program title wraps to >4 lines (photo variant)")
    ty = oy + 196
    for ln in title_lines:
        ld.text((mx, ty), ln, font=f(92), fill=INK)
        ty += 114

    # photo window: crop the source image into a framed slot
    # (spec "photo_align": "top" for posters/screenshots, default center)
    px0, py0, pw, ph = ox + 880, oy + 196, perf_x - 70 - (ox + 880), 470
    src = Image.open(spec["photo"]).convert("RGB")
    scale = max(pw / src.width, ph / src.height)
    src = src.resize((int(src.width * scale) + 2, int(src.height * scale) + 2), Image.LANCZOS)
    cx0 = (src.width - pw) // 2
    cy0 = 0 if spec.get("photo_align") == "top" else (src.height - ph) // 2
    src = src.crop((cx0, cy0, cx0 + pw, cy0 + ph))
    mask = Image.new("L", (pw, ph), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, pw, ph], radius=26, fill=255)
    layer.paste(src, (px0, py0), mask)
    ld.rounded_rectangle([px0, py0, px0 + pw, py0 + ph], radius=26, outline=INK, width=7)
    chip = "FOTO PROGRAM"
    chw = ld.textlength(chip, font=mono(32, bold=True)) + 44
    ld.rounded_rectangle([px0 + 22, py0 + 22, px0 + 22 + chw, py0 + 78],
                         radius=14, fill=BLACK)
    ld.text((px0 + 44, py0 + 34), chip, font=mono(32, bold=True), fill=YELLOW)

    dashed_h(ld, oy + 700, mx, perf_x - 70, DGRAY)

    fields = [("NILAI", spec["fields"]["nilai"]), ("DEADLINE", spec["fields"]["deadline"]),
              ("BUAT SIAPA", spec["fields"]["untuk"]), ("SUMBER", spec["fields"]["sumber"])]
    col_w = (perf_x - 70 - mx) // 2
    fy = oy + 745
    for i, (lab, val) in enumerate(fields):
        fx = mx + (i % 2) * col_w
        yy = fy + (i // 2) * 180
        ld.text((fx, yy), lab, font=mono(40, bold=True), fill=DGRAY)
        size = 52
        while size > 36:
            vf = f(size)
            vl = wrap(ld, val, vf, col_w - 50)
            longest = max(ld.textlength(wd, font=vf) for wd in val.split())
            if len(vl) <= 2 and longest <= col_w - 50:
                break
            size -= 4
        else:
            raise SystemExit(f"OVERFLOW: field {lab} does not fit")
        for ln in vl:
            yy += 56
            ld.text((fx, yy), ln, font=vf, fill=INK)

    lab_layer = Image.new("RGBA", (700, 90), (0, 0, 0, 0))
    lld = ImageDraw.Draw(lab_layer)
    lld.text((0, 10), "TIKET BANSOS - PEKA", font=mono(52, bold=True), fill=INK)
    lab_layer = lab_layer.rotate(90, resample=Image.BICUBIC, expand=True)
    layer.paste(lab_layer, (perf_x + 378, oy + 150), lab_layer)
    barcode(ld, perf_x + 70, oy + 150, 270, 600, spec["program"])
    ld.text((perf_x + 68, oy + 810), "peka.ai.id", font=mono(44, bold=True), fill=INK)
    ld.text((perf_x + 68, oy + 880), "verified", font=fr(44), fill=DGRAY)

    layer = layer.rotate(1.5, resample=Image.BICUBIC, expand=True)
    img.paste(layer, ((S - layer.width) // 2, 330), layer)

    st, spos = stamp(ImageDraw.Draw(img), 1290, 1085, spec.get("stamp", "100% GRATIS"))
    img.paste(st, spos, st)

    d = ImageDraw.Draw(img)
    d.text((110, 1690), "Geser buat syarat dan cara klaimnya →", font=f(60), fill=WHITE)
    d.text((110, 1785), f"Deadline: {spec['fields']['deadline']}", font=fr(48), fill=YELLOW)
    return img


def slide1(spec):
    if spec.get("photo"):
        return slide1_photo(spec)
    img = Image.new("RGB", (S, S), BLACK)
    d = ImageDraw.Draw(img)
    lockup(img, cy=128, mh=104, color=YELLOW)
    d.text((110, 96), "INFO BANTUAN GRATIS", font=mono(46, bold=True), fill=YELLOW)
    d.text((110, 158), "buat yang lagi butuh, bukan buat yang lagi iseng",
           font=fr(44), fill=GRAY)

    # --- ticket on its own layer, tilted -1.5 deg ---
    TW, TH = 1830, 1150
    layer = Image.new("RGBA", (TW + 220, TH + 240), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ox, oy = 110, 100
    ld.rounded_rectangle([ox + 16, oy + 26, ox + TW + 16, oy + TH + 26], radius=40, fill=SHADOW)
    ld.rounded_rectangle([ox, oy, ox + TW, oy + TH], radius=40, fill=CREAM)
    perf_x = ox + TW - 470
    dashed_v(ld, perf_x, oy + 60, oy + TH - 60, DGRAY)
    for yy in (oy, oy + TH):
        ld.ellipse([perf_x - 36, yy - 36, perf_x + 36, yy + 36], fill=BLACK)

    mx = ox + 80
    x = pill(ld, mx, oy + 64, "BANSOS", f(50), fill=BLACK, txt=YELLOW)
    pill(ld, x + 24, oy + 64, spec["category"].upper(), f(50), fill=None, txt=INK, outline=INK)

    title_lines = wrap(ld, spec["program"], f(108), 1150)
    if len(title_lines) > 3:
        raise SystemExit("OVERFLOW: program title wraps to >3 lines")
    ty = oy + 190
    for ln in title_lines:
        ld.text((mx, ty), ln, font=f(108), fill=INK)
        ty += 132

    dashed_h(ld, oy + 640, mx, perf_x - 70, DGRAY)

    fields = [("NILAI", spec["fields"]["nilai"]), ("DEADLINE", spec["fields"]["deadline"]),
              ("BUAT SIAPA", spec["fields"]["untuk"]), ("SUMBER", spec["fields"]["sumber"])]
    col_w = (perf_x - 70 - mx) // 2
    fy = oy + 690
    for i, (lab, val) in enumerate(fields):
        fx = mx + (i % 2) * col_w
        yy = fy + (i // 2) * 205
        ld.text((fx, yy), lab, font=mono(40, bold=True), fill=DGRAY)
        size = 56
        while size > 38:
            vf = f(size)
            vl = wrap(ld, val, vf, col_w - 50)
            longest = max(ld.textlength(wd, font=vf) for wd in val.split())
            if len(vl) <= 2 and longest <= col_w - 50:
                break
            size -= 4
        else:
            raise SystemExit(f"OVERFLOW: field {lab} does not fit")
        for ln in vl:
            yy += 62
            ld.text((fx, yy), ln, font=vf, fill=INK)

    # stub: barcode left, vertical label right of it
    lab_layer = Image.new("RGBA", (700, 90), (0, 0, 0, 0))
    lld = ImageDraw.Draw(lab_layer)
    lld.text((0, 10), "TIKET BANSOS - PEKA", font=mono(52, bold=True), fill=INK)
    lab_layer = lab_layer.rotate(90, resample=Image.BICUBIC, expand=True)
    layer.paste(lab_layer, (perf_x + 378, oy + 150), lab_layer)
    barcode(ld, perf_x + 70, oy + 150, 270, 600, spec["program"])
    ld.text((perf_x + 68, oy + 810), "peka.ai.id", font=mono(44, bold=True), fill=INK)
    ld.text((perf_x + 68, oy + 880), "verified", font=fr(44), fill=DGRAY)

    layer = layer.rotate(1.5, resample=Image.BICUBIC, expand=True)
    img.paste(layer, ((S - layer.width) // 2, 330), layer)

    st, spos = stamp(ImageDraw.Draw(img), 1300, 990, spec.get("stamp", "100% GRATIS"))
    img.paste(st, spos, st)

    d = ImageDraw.Draw(img)
    d.text((110, 1690), "Geser buat syarat dan cara klaimnya →", font=f(60), fill=WHITE)
    dl = spec["fields"]["deadline"]
    d.text((110, 1785), f"Deadline: {dl}", font=fr(48), fill=YELLOW)
    return img


def card(d, x, y, w, title, rows, numbered=False):
    """One cream ticket card with check/numbered rows. Returns card height."""
    row_h = []
    for r in rows:
        row_h.append(len(wrap(d, r, fr(56), w - 260)))
    total = 150 + sum(h * 76 + 18 for h in row_h) + 46
    d.rounded_rectangle([x, y, x + w, y + total], radius=36, fill=CREAM)
    dashed_v(d, x + 44, y + 40, y + total - 40, DGRAY, dash=20, gap=16, width=4)
    d.text((x + 110, y + 44), title, font=mono(46, bold=True), fill=INK)
    yy = y + 150
    for i, r in enumerate(rows):
        if numbered:
            d.ellipse([x + 110, yy + 2, x + 178, yy + 70], fill=BLACK)
            n = str(i + 1)
            d.text((x + 144 - d.textlength(n, font=f(44)) / 2, yy + 10), n, font=f(44), fill=YELLOW)
        else:
            d.rectangle([x + 116, yy + 14, x + 160, yy + 58], fill=YELLOW, outline=INK, width=3)
        for ln in wrap(d, r, fr(56), w - 260):
            d.text((x + 215, yy), ln, font=fr(56), fill=INK)
            yy += 76
        yy += 18
    return total


def slide2(spec):
    img = Image.new("RGB", (S, S), BLACK)
    d = ImageDraw.Draw(img)
    lockup(img, cy=128, mh=104, color=YELLOW)
    d.text((110, 280), "SYARAT & CARA KLAIM", font=f(104), fill=WHITE)
    d.rectangle([110, 420, 640, 438], fill=YELLOW)
    y = 520
    y += card(d, 110, y, 1828, "SYARATNYA", spec["syarat"][:4]) + 60
    y += card(d, 110, y, 1828, "CARA KLAIM", spec["steps"][:4], numbered=True) + 40
    if y > S - 210:
        raise SystemExit("OVERFLOW: slide 2 content too tall")
    d.text((110, S - 168), f"Sumber resmi: {spec['fields']['sumber']}", font=fr(46), fill=GRAY)
    d.text((110, S - 100), "Save biar nggak lupa. Tag teman yang butuh.", font=f(50), fill=WHITE)
    return img


def slide3(spec):
    img = Image.new("RGB", (S, S), YELLOW)
    d = ImageDraw.Draw(img)
    # inset dashed ticket frame
    m = 64
    x = m
    while x < S - m:
        d.line([x, m, min(x + 30, S - m), m], fill=INK, width=5)
        d.line([x, S - m, min(x + 30, S - m), S - m], fill=INK, width=5)
        x += 52
    y = m
    while y < S - m:
        d.line([m, y, m, min(y + 30, S - m)], fill=INK, width=5)
        d.line([S - m, y, S - m, min(y + 30, S - m)], fill=INK, width=5)
        y += 52
    lockup(img, cy=190, mh=104, color=INK, chip=BLACK)

    d.text((150, 400), "JANGAN SAMPAI", font=f(196), fill=INK)
    d.text((150, 610), "KELEWATAN", font=f(196), fill=INK)

    d.rounded_rectangle([150, 880, 1898, 1050], radius=28, fill=BLACK)
    band = spec["band"].upper()
    bf = mono(58, bold=True)
    d.text((150 + (1748 - d.textlength(band, font=bf)) / 2, 932), band, font=bf, fill=YELLOW)

    ctas = ["Tag teman yang lagi butuh ini",
            "Save postingan ini buat pas daftar nanti",
            "Follow @peka.ai.id, bansos baru tiap ada yang verified"]
    yy = 1180
    for c in ctas:
        cl = wrap(d, c, f(64), 1560)
        d.rectangle([150, yy + 20, 190, yy + 60], fill=INK)
        for ln in cl:
            d.text((245, yy), ln, font=f(64), fill=INK)
            yy += 84
        yy += 44
    d.text((150, S - 190), "Info diverifikasi dari sumber resmi sebelum tayang.",
           font=fr(46), fill=INK)
    return img


def main():
    spec = json.load(open(sys.argv[1]))
    out = spec["out_dir"]
    os.makedirs(out, exist_ok=True)
    slide1(spec).save(f"{out}/bansos-01.png")
    slide2(spec).save(f"{out}/bansos-02.png")
    slide3(spec).save(f"{out}/bansos-03.png")
    print("OK", out)


if __name__ == "__main__":
    main()
