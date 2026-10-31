#!/usr/bin/env python3
"""Bansos ticket-design carousel generator (3 slides, 4096x4096).

Design identity for Peka bansos posts: a physical aid ticket / coupon.
Two themes, picked by spec["theme"] (default "tiket"):
- "tiket": the original identity. Slide 1: cream ticket on black
  (perforation, stub with barcode, red GRATIS stamp, ticket fields).
  Slide 2: requirements + claim steps on ticket cards. Slide 3:
  yellow closing ticket with CTA rows.
- "kertas": light editorial paper theme (HM premium palette).
  Slide 1: white ticket on warm paper with a thin gold line.
  Slide 2: white cards on paper. Slide 3: paper closing with a
  black band and gold text. The red GRATIS stamp stays in both.
Locked Peka lockup top-right on every slide.

Usage: python3 bansos_design.py <spec.json>
Spec: {"program": "...", "category": "VPS / CLOUD", "stamp": "100% GRATIS",
       "fields": {"nilai": "...", "deadline": "...", "untuk": "...",
                  "sumber": "..."},
       "syarat": ["...", ...], "steps": ["...", ...],
       "band": "VPS ORACLE - GRATIS SELAMANYA", "out_dir": "/abs/path",
       "theme": "tiket" | "kertas" (optional, default "tiket")}
"""
import hashlib
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

S = 4096
YELLOW = (255, 214, 10)
BLACK = (17, 17, 17)
INK = (22, 22, 22)
CREAM = (255, 253, 244)
WHITE = (255, 255, 255)
GRAY = (150, 150, 142)
DGRAY = (105, 105, 98)
RED = (214, 48, 38)
SHADOW = (52, 52, 52)

# Palette roles shared by every slide function. "tiket" reproduces the
# original hardcoded colors exactly; "kertas" is the light variant.
_THEMES = {
    "tiket": dict(bg=BLACK, card=CREAM, card_outline=None, header=YELLOW,
                  lockup=YELLOW, subtitle=GRAY, muted=DGRAY, ink=INK,
                  shadow=SHADOW, pill_bg=BLACK, pill_text=YELLOW,
                  text_bg=WHITE, deadline=YELLOW, underline=YELLOW,
                  closing_bg=YELLOW, band=BLACK, band_text=YELLOW,
                  check=YELLOW, num_bg=BLACK, num_text=YELLOW,
                  lockup_chip=None),
    "kertas": dict(bg=(247, 244, 237), card=WHITE, card_outline=(23, 23, 19),
                   header=(23, 23, 19), lockup=(23, 23, 19),
                   subtitle=(107, 103, 94), muted=(107, 103, 94),
                   ink=(23, 23, 19), shadow=(210, 205, 190),
                   pill_bg=(23, 23, 19), pill_text=(247, 244, 237),
                   text_bg=(23, 23, 19), deadline=(138, 109, 47),
                   underline=(185, 151, 91), closing_bg=(247, 244, 237),
                   band=(23, 23, 19), band_text=(185, 151, 91),
                   check=(185, 151, 91), num_bg=(23, 23, 19),
                   num_text=(247, 244, 237), lockup_chip=None),
    "kuning": dict(bg=YELLOW, card=BLACK, card_outline=None,
                   header=(23, 23, 19), lockup=(23, 23, 19),
                   subtitle=(60, 60, 60), muted=(180, 180, 170),
                   ink=(255, 253, 244), shadow=(200, 165, 0),
                   pill_bg=YELLOW, pill_text=(23, 23, 19),
                   text_bg=(23, 23, 19), deadline=(23, 23, 19),
                   underline=(23, 23, 19), closing_bg=(23, 23, 19),
                   band=YELLOW, band_text=(23, 23, 19),
                   check=YELLOW, num_bg=YELLOW, num_text=(23, 23, 19),
                   lockup_chip=BLACK),
}
PAL = _THEMES["tiket"]

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
    tx = 3876 - d.textlength(label, font=tf)
    ty = cy - (ascent + descent) // 2
    mx = int(tx - 52 - cr.width)
    my = cy - mh // 2
    if chip is not None:
        pad = 40
        d.rounded_rectangle([mx - pad, my - pad, mx + cr.width + pad, my + mh + pad],
                            radius=68, fill=chip)
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


def dashed_v(d, x, y0, y1, color, dash=52, gap=36, width=10):
    y = y0
    while y < y1:
        d.line([x, y, x, min(y + dash, y1)], fill=color, width=width)
        y += dash + gap


def dashed_h(d, y, x0, x1, color, dash=52, gap=36, width=10):
    x = x0
    while x < x1:
        d.line([x, y, min(x + dash, x1), y], fill=color, width=width)
        x += dash + gap


def pill(d, x, y, text, font, fill=None, txt=None, outline=None, pad_x=64, pad_y=30):
    tw = d.textlength(text, font=font)
    ascent, descent = font.getmetrics()
    th = ascent + descent
    box = [x, y, x + tw + pad_x * 2, y + th + pad_y * 2]
    d.rounded_rectangle(box, radius=(box[3] - box[1]) // 2, fill=fill, outline=outline,
                        width=10 if outline else 2)
    d.text((x + pad_x, y + pad_y - 4), text, font=font, fill=txt)
    return box[2]


def stamp(d, cx, cy, text):
    """Red double-outline GRATIS stamp, rotated -8 degrees, drawn in place."""
    tf = f(128)
    tw = d.textlength(text, font=tf)
    w, h = int(tw + 168), 276
    layer = Image.new("RGBA", (w + 120, h + 120), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rounded_rectangle([60, 60, 60 + w, 60 + h], radius=52, outline=RED, width=18)
    ld.rounded_rectangle([96, 96, 60 + w - 36, 60 + h - 36], radius=36, outline=RED, width=8)
    ld.text((60 + (w - tw) / 2, 60 + 68), text, font=tf, fill=RED)
    layer = layer.rotate(8, resample=Image.BICUBIC, expand=True)
    return layer, (int(cx - layer.width / 2), int(cy - layer.height / 2))


def barcode(d, x, y, w, h, seed_text):
    seed = int(hashlib.md5(seed_text.encode()).hexdigest()[:8], 16)
    cx = x
    i = 0
    while cx < x + w - 16:
        seed = (seed * 1103515245 + 12345) % (2 ** 31)
        bw = 8 + (seed % 4) * 8
        if i % 2 == 0:
            d.rectangle([cx, y, cx + bw, y + h], fill=PAL["ink"])
        cx += bw + 10
        i += 1


def slide1_photo(spec):
    """Slide 1 variant for bansos items that ship with their own image:
    the ticket gains a framed photo window right of the title."""
    img = Image.new("RGB", (S, S), PAL["bg"])
    d = ImageDraw.Draw(img)
    lockup(img, cy=256, mh=208, color=PAL["lockup"], chip=PAL["lockup_chip"])
    d.text((220, 192), "INFO BANSOS", font=mono(92, bold=True), fill=PAL["header"])
    d.text((220, 316), "buat yang lagi butuh, bukan buat yang lagi iseng",
           font=fr(88), fill=PAL["subtitle"])

    TW, TH = 3660, 2300
    layer = Image.new("RGBA", (TW + 440, TH + 480), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ox, oy = 220, 200
    ld.rounded_rectangle([ox + 32, oy + 52, ox + TW + 32, oy + TH + 52], radius=80, fill=PAL["shadow"])
    ld.rounded_rectangle([ox, oy, ox + TW, oy + TH], radius=80, fill=PAL["card"])
    perf_x = ox + TW - 940
    dashed_v(ld, perf_x, oy + 120, oy + TH - 120, PAL["muted"])
    for yy in (oy, oy + TH):
        ld.ellipse([perf_x - 72, yy - 72, perf_x + 72, yy + 72], fill=PAL["bg"])

    mx = ox + 160
    x = pill(ld, mx, oy + 128, "BANSOS", f(100), fill=PAL["pill_bg"], txt=PAL["pill_text"])
    pill(ld, x + 48, oy + 128, spec["category"].upper(), f(100), fill=None, txt=PAL["ink"], outline=PAL["ink"])

    title_lines = wrap(ld, spec["program"], f(184), 1280)
    if len(title_lines) > 4:
        raise SystemExit("OVERFLOW: program title wraps to >4 lines (photo variant)")
    ty = oy + 392
    for ln in title_lines:
        ld.text((mx, ty), ln, font=f(92), fill=PAL["ink"])
        ty += 228

    # photo window: crop the source image into a framed slot
    # (spec "photo_align": "top" for posters/screenshots, default center)
    px0, py0, pw, ph = ox + 1760, oy + 392, perf_x - 140 - (ox + 1760), 940
    src = Image.open(spec["photo"]).convert("RGB")
    scale = max(pw / src.width, ph / src.height)
    src = src.resize((int(src.width * scale) + 4, int(src.height * scale) + 4), Image.LANCZOS)
    cx0 = (src.width - pw) // 2
    cy0 = 0 if spec.get("photo_align") == "top" else (src.height - ph) // 2
    src = src.crop((cx0, cy0, cx0 + pw, cy0 + ph))
    mask = Image.new("L", (pw, ph), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, pw, ph], radius=52, fill=255)
    layer.paste(src, (px0, py0), mask)
    ld.rounded_rectangle([px0, py0, px0 + pw, py0 + ph], radius=52, outline=PAL["ink"], width=14)
    chip = "FOTO PROGRAM"
    chw = ld.textlength(chip, font=mono(64, bold=True)) + 88
    ld.rounded_rectangle([px0 + 44, py0 + 44, px0 + 44 + chw, py0 + 156],
                         radius=28, fill=PAL["pill_bg"])
    ld.text((px0 + 88, py0 + 68), chip, font=mono(64, bold=True), fill=PAL["pill_text"])

    dashed_h(ld, oy + 1400, mx, perf_x - 140, PAL["muted"])

    fields = [("NILAI", spec["fields"]["nilai"]), ("DEADLINE", spec["fields"]["deadline"]),
              ("BUAT SIAPA", spec["fields"]["untuk"]), ("SUMBER", spec["fields"]["sumber"])]
    col_w = (perf_x - 70 - mx) // 2
    fy = oy + 1490
    for i, (lab, val) in enumerate(fields):
        fx = mx + (i % 2) * col_w
        yy = fy + (i // 2) * 360
        ld.text((fx, yy), lab, font=mono(80, bold=True), fill=PAL["muted"])
        size = 104
        while size > 72:
            vf = f(size)
            vl = wrap(ld, val, vf, col_w - 100)
            longest = max(ld.textlength(wd, font=vf) for wd in val.split())
            if len(vl) <= 2 and longest <= col_w - 100:
                break
            size -= 8
        else:
            raise SystemExit(f"OVERFLOW: field {lab} does not fit")
        for ln in vl:
            yy += 112
            ld.text((fx, yy), ln, font=vf, fill=PAL["ink"])

    lab_layer = Image.new("RGBA", (1400, 180), (0, 0, 0, 0))
    lld = ImageDraw.Draw(lab_layer)
    lld.text((0, 20), "TIKET BANSOS - PEKA", font=mono(104, bold=True), fill=PAL["ink"])
    lab_layer = lab_layer.rotate(90, resample=Image.BICUBIC, expand=True)
    layer.paste(lab_layer, (perf_x + 756, oy + 300), lab_layer)
    barcode(ld, perf_x + 140, oy + 300, 540, 1200, spec["program"])
    ld.text((perf_x + 136, oy + 1648), "verified", font=fr(88), fill=PAL["muted"])
    ld.text((perf_x + 68, oy + 1796), "gabung ke", font=mono(68), fill=PAL["muted"])
    ld.text((perf_x + 68, oy + 1900), "komunitas kami:", font=mono(68), fill=PAL["muted"])
    ld.text((perf_x + 68, oy + 2012), "url.peka.ai.id", font=mono(72, bold=True), fill=PAL["ink"])

    layer = layer.rotate(1.5, resample=Image.BICUBIC, expand=True)
    img.paste(layer, ((S - layer.width) // 2, 660), layer)

    st, spos = stamp(ImageDraw.Draw(img), 2580, 2170, spec.get("stamp", "100% GRATIS"))
    img.paste(st, spos, st)

    d = ImageDraw.Draw(img)
    d.text((220, 3380), "Geser buat syarat dan cara klaimnya →", font=f(120), fill=PAL["text_bg"])
    d.text((220, 3570), f"Deadline: {spec['fields']['deadline']}", font=fr(96), fill=PAL["deadline"])
    return img


def slide1(spec):
    if spec.get("photo"):
        return slide1_photo(spec)
    img = Image.new("RGB", (S, S), PAL["bg"])
    d = ImageDraw.Draw(img)
    lockup(img, cy=256, mh=208, color=PAL["lockup"], chip=PAL["lockup_chip"])
    d.text((220, 192), "INFO BANSOS", font=mono(92, bold=True), fill=PAL["header"])
    d.text((220, 316), "buat yang lagi butuh, bukan buat yang lagi iseng",
           font=fr(88), fill=PAL["subtitle"])

    # --- ticket on its own layer, tilted -1.5 deg ---
    TW, TH = 3660, 2300
    layer = Image.new("RGBA", (TW + 440, TH + 480), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ox, oy = 220, 200
    ld.rounded_rectangle([ox + 32, oy + 52, ox + TW + 32, oy + TH + 52], radius=80, fill=PAL["shadow"])
    ld.rounded_rectangle([ox, oy, ox + TW, oy + TH], radius=80, fill=PAL["card"])
    perf_x = ox + TW - 940
    dashed_v(ld, perf_x, oy + 120, oy + TH - 120, PAL["muted"])
    for yy in (oy, oy + TH):
        ld.ellipse([perf_x - 72, yy - 72, perf_x + 72, yy + 72], fill=PAL["bg"])

    mx = ox + 160
    x = pill(ld, mx, oy + 128, "BANSOS", f(100), fill=PAL["pill_bg"], txt=PAL["pill_text"])
    pill(ld, x + 48, oy + 128, spec["category"].upper(), f(100), fill=None, txt=PAL["ink"], outline=PAL["ink"])

    title_lines = wrap(ld, spec["program"], f(216), 2300)
    if len(title_lines) > 3:
        raise SystemExit("OVERFLOW: program title wraps to >3 lines")
    ty = oy + 380
    for ln in title_lines:
        ld.text((mx, ty), ln, font=f(108), fill=PAL["ink"])
        ty += 264

    dashed_h(ld, oy + 1280, mx, perf_x - 140, PAL["muted"])

    fields = [("NILAI", spec["fields"]["nilai"]), ("DEADLINE", spec["fields"]["deadline"]),
              ("BUAT SIAPA", spec["fields"]["untuk"]), ("SUMBER", spec["fields"]["sumber"])]
    col_w = (perf_x - 70 - mx) // 2
    fy = oy + 1380
    for i, (lab, val) in enumerate(fields):
        fx = mx + (i % 2) * col_w
        yy = fy + (i // 2) * 410
        ld.text((fx, yy), lab, font=mono(80, bold=True), fill=PAL["muted"])
        size = 112
        while size > 76:
            vf = f(size)
            vl = wrap(ld, val, vf, col_w - 100)
            longest = max(ld.textlength(wd, font=vf) for wd in val.split())
            if len(vl) <= 2 and longest <= col_w - 100:
                break
            size -= 8
        else:
            raise SystemExit(f"OVERFLOW: field {lab} does not fit")
        for ln in vl:
            yy += 124
            ld.text((fx, yy), ln, font=vf, fill=PAL["ink"])

    # stub: barcode left, vertical label right of it
    lab_layer = Image.new("RGBA", (1400, 180), (0, 0, 0, 0))
    lld = ImageDraw.Draw(lab_layer)
    lld.text((0, 20), "TIKET BANSOS - PEKA", font=mono(104, bold=True), fill=PAL["ink"])
    lab_layer = lab_layer.rotate(90, resample=Image.BICUBIC, expand=True)
    layer.paste(lab_layer, (perf_x + 756, oy + 300), lab_layer)
    barcode(ld, perf_x + 140, oy + 300, 540, 1200, spec["program"])
    ld.text((perf_x + 136, oy + 1648), "verified", font=fr(88), fill=PAL["muted"])
    ld.text((perf_x + 68, oy + 1796), "gabung ke", font=mono(68), fill=PAL["muted"])
    ld.text((perf_x + 68, oy + 1900), "komunitas kami:", font=mono(68), fill=PAL["muted"])
    ld.text((perf_x + 68, oy + 2012), "url.peka.ai.id", font=mono(72, bold=True), fill=PAL["ink"])

    layer = layer.rotate(1.5, resample=Image.BICUBIC, expand=True)
    img.paste(layer, ((S - layer.width) // 2, 660), layer)

    st, spos = stamp(ImageDraw.Draw(img), 2600, 1980, spec.get("stamp", "100% GRATIS"))
    img.paste(st, spos, st)

    d = ImageDraw.Draw(img)
    d.text((220, 3380), "Geser buat syarat dan cara klaimnya →", font=f(120), fill=PAL["text_bg"])
    dl = spec["fields"]["deadline"]
    d.text((220, 3570), f"Deadline: {dl}", font=fr(96), fill=PAL["deadline"])
    return img


def card(d, x, y, w, title, rows, numbered=False):
    """One cream ticket card with check/numbered rows. Returns card height."""
    row_h = []
    for r in rows:
        row_h.append(len(wrap(d, r, fr(112), w - 520)))
    total = 300 + sum(h * 152 + 36 for h in row_h) + 92
    d.rounded_rectangle([x, y, x + w, y + total], radius=72, fill=PAL["card"],
                        outline=PAL["card_outline"], width=6 if PAL["card_outline"] else 2)
    dashed_v(d, x + 88, y + 80, y + total - 80, PAL["muted"], dash=40, gap=32, width=8)
    d.text((x + 220, y + 88), title, font=mono(92, bold=True), fill=PAL["ink"])
    yy = y + 300
    for i, r in enumerate(rows):
        if numbered:
            d.ellipse([x + 220, yy + 4, x + 356, yy + 140], fill=PAL["num_bg"])
            n = str(i + 1)
            d.text((x + 288 - d.textlength(n, font=f(88)) / 2, yy + 20), n, font=f(88), fill=PAL["num_text"])
        else:
            d.rectangle([x + 232, yy + 28, x + 320, yy + 116], fill=PAL["check"], outline=PAL["ink"], width=6)
        for ln in wrap(d, r, fr(112), w - 520):
            d.text((x + 430, yy), ln, font=fr(112), fill=PAL["ink"])
            yy += 152
        yy += 36
    return total


def slide2(spec):
    img = Image.new("RGB", (S, S), PAL["bg"])
    d = ImageDraw.Draw(img)
    lockup(img, cy=256, mh=208, color=PAL["lockup"], chip=PAL["lockup_chip"])
    d.text((220, 560), "SYARAT & CARA KLAIM", font=f(208), fill=PAL["text_bg"])
    d.rectangle([220, 840, 1280, 876], fill=PAL["underline"])
    y = 1040
    y += card(d, 220, y, 3656, "SYARATNYA", spec["syarat"][:4]) + 120
    y += card(d, 220, y, 3656, "CARA KLAIM", spec["steps"][:4], numbered=True) + 80
    if y > S - 420:
        raise SystemExit("OVERFLOW: slide 2 content too tall")
    d.text((220, S - 336), f"Sumber resmi: {spec['fields']['sumber']}", font=fr(92), fill=PAL["subtitle"])
    d.text((220, S - 200), "Save biar nggak lupa. Tag teman yang butuh.", font=f(100), fill=PAL["text_bg"])
    return img


def slide3(spec):
    img = Image.new("RGB", (S, S), PAL["closing_bg"])
    d = ImageDraw.Draw(img)
    # inset dashed ticket frame
    m = 128
    x = m
    while x < S - m:
        d.line([x, m, min(x + 60, S - m), m], fill=PAL["ink"], width=10)
        d.line([x, S - m, min(x + 60, S - m), S - m], fill=PAL["ink"], width=10)
        x += 104
    y = m
    while y < S - m:
        d.line([m, y, m, min(y + 60, S - m)], fill=PAL["ink"], width=10)
        d.line([S - m, y, S - m, min(y + 60, S - m)], fill=PAL["ink"], width=10)
        y += 104
    lockup(img, cy=380, mh=208, color=PAL["ink"], chip=BLACK)

    d.text((300, 800), "JANGAN SAMPAI", font=f(392), fill=PAL["ink"])
    d.text((300, 1220), "KELEWATAN", font=f(392), fill=PAL["ink"])

    d.rounded_rectangle([300, 1760, 3796, 2100], radius=56, fill=PAL["band"])
    band = spec["band"].upper()
    bf = mono(116, bold=True)
    d.text((300 + (3496 - d.textlength(band, font=bf)) / 2, 1864), band, font=bf, fill=PAL["band_text"])

    ctas = ["Tag teman yang lagi butuh ini",
            "Save postingan ini buat pas daftar nanti",
            "Follow @peka.ai.id, bansos baru tiap ada yang verified",
            "Gabung ke komunitas kami: url.peka.ai.id"]
    if spec.get("store_cta"):
        ctas.append(spec["store_cta"])
    # Edisi dengan CTA tambahan pakai spasi lebih rapat supaya muat.
    tight = len(ctas) > 4
    line_h = 156 if tight else 168
    gap = 72 if tight else 88
    yy = 2320 if tight else 2360
    for c in ctas:
        cl = wrap(d, c, f(128), 3120)
        d.rectangle([300, yy + 40, 380, yy + 120], fill=PAL["ink"])
        for ln in cl:
            d.text((490, yy), ln, font=f(128), fill=PAL["ink"])
            yy += line_h
        yy += gap
    # Shortlink printed on the slide (Threads no-link rule, 31 Okt 2026):
    # the edition's link lives here, not in a Threads reply/comment.
    if spec.get("shortlink"):
        label = spec.get("shortlink_label", "Link: ")
        shown = spec["shortlink"].replace("https://", "").replace("http://", "")
        d.text((300, yy + 16), label + shown, font=mono(108, bold=True), fill=PAL["band"])
    d.text((300, S - 320 if tight else S - 380), "Info diverifikasi dari sumber resmi sebelum tayang.",
           font=fr(92), fill=PAL["ink"])
    return img


def main():
    global PAL
    spec = json.load(open(sys.argv[1]))
    theme = spec.get("theme", "tiket")
    if theme not in _THEMES:
        raise SystemExit(f"Unknown bansos theme: {theme} (expected tiket, kertas, or kuning)")
    PAL = _THEMES[theme]
    out = spec["out_dir"]
    os.makedirs(out, exist_ok=True)
    slide1(spec).save(f"{out}/bansos-01.png")
    slide2(spec).save(f"{out}/bansos-02.png")
    slide3(spec).save(f"{out}/bansos-03.png")
    print("OK", out)


if __name__ == "__main__":
    main()
