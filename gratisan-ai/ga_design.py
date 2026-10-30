#!/usr/bin/env python3
"""Gratisan AI edition design wrapper.

Reuses the locked bansos ticket system (bansos/bansos_design.py) with the
pillar kicker "GRATISAN AI" (the locked "INFO BANSOS" kicker stays
exclusive to real bansos editions) and pillar-specific closing copy.
Slide 2 is the stock bansos slide2 (SYARAT & CARA KLAIM).

Usage: python3 ga_design.py <spec.json>
Spec: {"program": "...", "category": "...", "stamp": "...",
       "fields": {"nilai": "...", "deadline": "...", "untuk": "...",
                  "sumber": "..."},
       "syarat": [...], "steps": [...],
       "band": "...", "out_dir": "/abs/path"}
Output: ga-01.png .. ga-03.png in spec["out_dir"].
"""
import json
import os
import sys

sys.path.insert(0, "/home/hatch/workspace/peka-content/bansos")
import bansos_design as bd
from PIL import Image, ImageDraw

S = bd.S


def slide1_gratisan(spec):
    """bd.slide1 with the GRATISAN AI kicker + pillar subtitle."""
    img = Image.new("RGB", (S, S), bd.BLACK)
    d = ImageDraw.Draw(img)
    bd.lockup(img, cy=256, mh=208, color=bd.YELLOW)
    d.text((220, 192), "GRATISAN AI", font=bd.mono(92, bold=True), fill=bd.YELLOW)
    d.text((220, 316), spec.get("subtitle",
           "gratis beneran, bukan trial yang ujungnya bayar"),
           font=bd.fr(88), fill=bd.GRAY)

    TW, TH = 3660, 2300
    layer = Image.new("RGBA", (TW + 440, TH + 480), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ox, oy = 220, 200
    ld.rounded_rectangle([ox + 32, oy + 52, ox + TW + 32, oy + TH + 52], radius=80, fill=bd.SHADOW)
    ld.rounded_rectangle([ox, oy, ox + TW, oy + TH], radius=80, fill=bd.CREAM)
    perf_x = ox + TW - 940
    bd.dashed_v(ld, perf_x, oy + 120, oy + TH - 120, bd.DGRAY)
    for yy in (oy, oy + TH):
        ld.ellipse([perf_x - 72, yy - 72, perf_x + 72, yy + 72], fill=bd.BLACK)

    mx = ox + 160
    x = bd.pill(ld, mx, oy + 128, "GRATISAN", bd.f(100), fill=bd.BLACK, txt=bd.YELLOW)
    bd.pill(ld, x + 48, oy + 128, spec["category"].upper(), bd.f(100), fill=None,
            txt=bd.INK, outline=bd.INK)

    title_lines = bd.wrap(ld, spec["program"], bd.f(216), 2300)
    if len(title_lines) > 3:
        raise SystemExit("OVERFLOW: program title wraps to >3 lines")
    ty = oy + 380
    for ln in title_lines:
        ld.text((mx, ty), ln, font=bd.f(216), fill=bd.INK)
        ty += 264

    bd.dashed_h(ld, oy + 1280, mx, perf_x - 140, bd.DGRAY)

    fields = [("NILAI", spec["fields"]["nilai"]), ("DEADLINE", spec["fields"]["deadline"]),
              ("BUAT SIAPA", spec["fields"]["untuk"]), ("SUMBER", spec["fields"]["sumber"])]
    col_w = (perf_x - 70 - mx) // 2
    fy = oy + 1380
    for i, (lab, val) in enumerate(fields):
        fx = mx + (i % 2) * col_w
        yy = fy + (i // 2) * 410
        ld.text((fx, yy), lab, font=bd.mono(80, bold=True), fill=bd.DGRAY)
        size = 112
        while size > 76:
            vf = bd.f(size)
            vl = bd.wrap(ld, val, vf, col_w - 100)
            longest = max(ld.textlength(wd, font=vf) for wd in val.split())
            if len(vl) <= 2 and longest <= col_w - 100:
                break
            size -= 8
        else:
            raise SystemExit(f"OVERFLOW: field {lab} does not fit")
        for ln in vl:
            yy += 124
            ld.text((fx, yy), ln, font=vf, fill=bd.INK)

    lab_layer = Image.new("RGBA", (1400, 180), (0, 0, 0, 0))
    lld = ImageDraw.Draw(lab_layer)
    lld.text((0, 20), "TIKET GRATISAN - PEKA", font=bd.mono(104, bold=True), fill=bd.INK)
    lab_layer = lab_layer.rotate(90, resample=Image.BICUBIC, expand=True)
    layer.paste(lab_layer, (perf_x + 756, oy + 300), lab_layer)
    bd.barcode(ld, perf_x + 140, oy + 300, 540, 1200, spec["program"])
    ld.text((perf_x + 136, oy + 1648), "verified", font=bd.fr(88), fill=bd.DGRAY)
    ld.text((perf_x + 68, oy + 1796), "gabung ke", font=bd.mono(68), fill=bd.DGRAY)
    ld.text((perf_x + 68, oy + 1900), "komunitas kami:", font=bd.mono(68), fill=bd.DGRAY)
    ld.text((perf_x + 68, oy + 2012), "url.peka.ai.id", font=bd.mono(72, bold=True), fill=bd.INK)

    layer = layer.rotate(1.5, resample=Image.BICUBIC, expand=True)
    img.paste(layer, ((S - layer.width) // 2, 660), layer)

    st, spos = bd.stamp(ImageDraw.Draw(img), 2600, 1980, spec.get("stamp", "100% GRATIS"))
    img.paste(st, spos, st)

    d = ImageDraw.Draw(img)
    d.text((220, 3380), "Geser buat syarat dan cara klaimnya →", font=bd.f(120), fill=bd.WHITE)
    dl = spec["fields"]["deadline"]
    d.text((220, 3570), f"Deadline: {dl}", font=bd.fr(96), fill=bd.YELLOW)
    return img


def slide3_gratisan(spec):
    """bd.slide3 with honest pillar copy (no fake urgency, no deadline)."""
    img = Image.new("RGB", (S, S), bd.YELLOW)
    d = ImageDraw.Draw(img)
    m = 128
    x = m
    while x < S - m:
        d.line([x, m, min(x + 60, S - m), m], fill=bd.INK, width=10)
        d.line([x, S - m, min(x + 60, S - m), S - m], fill=bd.INK, width=10)
        x += 104
    y = m
    while y < S - m:
        d.line([m, y, m, min(y + 60, S - m)], fill=bd.INK, width=10)
        d.line([S - m, y, S - m, min(y + 60, S - m)], fill=bd.INK, width=10)
        y += 104
    bd.lockup(img, cy=380, mh=208, color=bd.INK, chip=bd.BLACK)

    d.text((300, 800), "AI GRATIS", font=bd.f(392), fill=bd.INK)
    d.text((300, 1220), "BUAT KAMU", font=bd.f(392), fill=bd.INK)

    d.rounded_rectangle([300, 1760, 3796, 2100], radius=56, fill=bd.BLACK)
    band = spec["band"].upper()
    bf = bd.mono(116, bold=True)
    d.text((300 + (3496 - d.textlength(band, font=bf)) / 2, 1864), band, font=bf, fill=bd.YELLOW)

    ctas = spec.get("ctas", ["Tag teman yang lagi belajar ngoding",
            "Save postingan ini, jatahnya reset tiap bulan",
            "Follow @peka.ai.id, gratisan AI baru tiap Rabu + Sabtu",
            "Gabung ke komunitas kami: url.peka.ai.id"])
    yy = 2360
    for c in ctas:
        cl = bd.wrap(d, c, bd.f(128), 3120)
        d.rectangle([300, yy + 40, 380, yy + 120], fill=bd.INK)
        for ln in cl:
            d.text((490, yy), ln, font=bd.f(128), fill=bd.INK)
            yy += 168
        yy += 88
    d.text((300, S - 380), "Info diverifikasi dari sumber resmi sebelum tayang.",
           font=bd.fr(92), fill=bd.INK)
    return img


def build(spec):
    return [slide1_gratisan(spec), bd.slide2(spec), slide3_gratisan(spec)]


def main():
    spec = json.load(open(sys.argv[1]))
    out = spec["out_dir"]
    os.makedirs(out, exist_ok=True)
    for i, img in enumerate(build(spec), start=1):
        img.save(f"{out}/ga-{i:02d}.png")
    print("OK", out)


if __name__ == "__main__":
    main()
