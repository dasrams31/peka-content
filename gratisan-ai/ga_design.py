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
    bd.lockup(img, cy=128, mh=104, color=bd.YELLOW)
    d.text((110, 96), "GRATISAN AI", font=bd.mono(46, bold=True), fill=bd.YELLOW)
    d.text((110, 158), "gratis beneran, bukan trial yang ujungnya bayar",
           font=bd.fr(44), fill=bd.GRAY)

    TW, TH = 1830, 1150
    layer = Image.new("RGBA", (TW + 220, TH + 240), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ox, oy = 110, 100
    ld.rounded_rectangle([ox + 16, oy + 26, ox + TW + 16, oy + TH + 26], radius=40, fill=bd.SHADOW)
    ld.rounded_rectangle([ox, oy, ox + TW, oy + TH], radius=40, fill=bd.CREAM)
    perf_x = ox + TW - 470
    bd.dashed_v(ld, perf_x, oy + 60, oy + TH - 60, bd.DGRAY)
    for yy in (oy, oy + TH):
        ld.ellipse([perf_x - 36, yy - 36, perf_x + 36, yy + 36], fill=bd.BLACK)

    mx = ox + 80
    x = bd.pill(ld, mx, oy + 64, "GRATISAN", bd.f(50), fill=bd.BLACK, txt=bd.YELLOW)
    bd.pill(ld, x + 24, oy + 64, spec["category"].upper(), bd.f(50), fill=None,
            txt=bd.INK, outline=bd.INK)

    title_lines = bd.wrap(ld, spec["program"], bd.f(108), 1150)
    if len(title_lines) > 3:
        raise SystemExit("OVERFLOW: program title wraps to >3 lines")
    ty = oy + 190
    for ln in title_lines:
        ld.text((mx, ty), ln, font=bd.f(108), fill=bd.INK)
        ty += 132

    bd.dashed_h(ld, oy + 640, mx, perf_x - 70, bd.DGRAY)

    fields = [("NILAI", spec["fields"]["nilai"]), ("DEADLINE", spec["fields"]["deadline"]),
              ("BUAT SIAPA", spec["fields"]["untuk"]), ("SUMBER", spec["fields"]["sumber"])]
    col_w = (perf_x - 70 - mx) // 2
    fy = oy + 690
    for i, (lab, val) in enumerate(fields):
        fx = mx + (i % 2) * col_w
        yy = fy + (i // 2) * 205
        ld.text((fx, yy), lab, font=bd.mono(40, bold=True), fill=bd.DGRAY)
        size = 56
        while size > 38:
            vf = bd.f(size)
            vl = bd.wrap(ld, val, vf, col_w - 50)
            longest = max(ld.textlength(wd, font=vf) for wd in val.split())
            if len(vl) <= 2 and longest <= col_w - 50:
                break
            size -= 4
        else:
            raise SystemExit(f"OVERFLOW: field {lab} does not fit")
        for ln in vl:
            yy += 62
            ld.text((fx, yy), ln, font=vf, fill=bd.INK)

    lab_layer = Image.new("RGBA", (700, 90), (0, 0, 0, 0))
    lld = ImageDraw.Draw(lab_layer)
    lld.text((0, 10), "TIKET GRATISAN - PEKA", font=bd.mono(52, bold=True), fill=bd.INK)
    lab_layer = lab_layer.rotate(90, resample=Image.BICUBIC, expand=True)
    layer.paste(lab_layer, (perf_x + 378, oy + 150), lab_layer)
    bd.barcode(ld, perf_x + 70, oy + 150, 270, 600, spec["program"])
    ld.text((perf_x + 68, oy + 824), "verified", font=bd.fr(44), fill=bd.DGRAY)
    ld.text((perf_x + 68, oy + 898), "gabung ke", font=bd.mono(34), fill=bd.DGRAY)
    ld.text((perf_x + 68, oy + 950), "komunitas kami:", font=bd.mono(34), fill=bd.DGRAY)
    ld.text((perf_x + 68, oy + 1006), "url.peka.ai.id", font=bd.mono(36, bold=True), fill=bd.INK)

    layer = layer.rotate(1.5, resample=Image.BICUBIC, expand=True)
    img.paste(layer, ((S - layer.width) // 2, 330), layer)

    st, spos = bd.stamp(ImageDraw.Draw(img), 1300, 990, spec.get("stamp", "100% GRATIS"))
    img.paste(st, spos, st)

    d = ImageDraw.Draw(img)
    d.text((110, 1690), "Geser buat syarat dan cara klaimnya →", font=bd.f(60), fill=bd.WHITE)
    dl = spec["fields"]["deadline"]
    d.text((110, 1785), f"Deadline: {dl}", font=bd.fr(48), fill=bd.YELLOW)
    return img


def slide3_gratisan(spec):
    """bd.slide3 with honest pillar copy (no fake urgency, no deadline)."""
    img = Image.new("RGB", (S, S), bd.YELLOW)
    d = ImageDraw.Draw(img)
    m = 64
    x = m
    while x < S - m:
        d.line([x, m, min(x + 30, S - m), m], fill=bd.INK, width=5)
        d.line([x, S - m, min(x + 30, S - m), S - m], fill=bd.INK, width=5)
        x += 52
    y = m
    while y < S - m:
        d.line([m, y, m, min(y + 30, S - m)], fill=bd.INK, width=5)
        d.line([S - m, y, S - m, min(y + 30, S - m)], fill=bd.INK, width=5)
        y += 52
    bd.lockup(img, cy=190, mh=104, color=bd.INK, chip=bd.BLACK)

    d.text((150, 400), "AI GRATIS", font=bd.f(196), fill=bd.INK)
    d.text((150, 610), "BUAT KAMU", font=bd.f(196), fill=bd.INK)

    d.rounded_rectangle([150, 880, 1898, 1050], radius=28, fill=bd.BLACK)
    band = spec["band"].upper()
    bf = bd.mono(58, bold=True)
    d.text((150 + (1748 - d.textlength(band, font=bf)) / 2, 932), band, font=bf, fill=bd.YELLOW)

    ctas = ["Tag teman yang lagi belajar ngoding",
            "Save postingan ini, jatahnya reset tiap bulan",
            "Follow @peka.ai.id, gratisan AI baru tiap Rabu + Sabtu",
            "Gabung ke komunitas kami: url.peka.ai.id"]
    yy = 1180
    for c in ctas:
        cl = bd.wrap(d, c, bd.f(64), 1560)
        d.rectangle([150, yy + 20, 190, yy + 60], fill=bd.INK)
        for ln in cl:
            d.text((245, yy), ln, font=bd.f(64), fill=bd.INK)
            yy += 84
        yy += 44
    d.text((150, S - 190), "Info diverifikasi dari sumber resmi sebelum tayang.",
           font=bd.fr(46), fill=bd.INK)
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
