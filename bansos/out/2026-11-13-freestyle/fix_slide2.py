#!/usr/bin/env python3
"""Re-render ONLY slide 2 for the Freestyle Bansos edition (2026-11-13).

Why a fix script (same precedent as the .pl edition's fix_slide2.py):
- bansos_design.py renders only syarat[:4] on slide 2 and never renders
  spec["catch"] anywhere. This edition needs all 5 syarat AND the honest
  catch printed on a slide (locked Bansos catch rule).
- This script reuses bansos_design.py helpers but renders slide 2 with
  tighter card metrics, all 5 syarat rows, the 4 claim steps, and a red
  catch band below the cards. Footers are kept and repositioned.
- Slides 1 and 3 are NOT touched (already verified good).

Usage: python3 fix_slide2.py <spec.json>
"""
import json
import sys

sys.path.insert(0, "/home/hatch/workspace/peka-content/bansos")
import bansos_design as bd

S = bd.S
RED = bd.RED
PAL = bd._THEMES["tiket"]


def wrap(d, text, font, max_w):
    return bd.wrap(d, text, font, max_w)


def card_tight(d, x, y, w, title, rows, numbered=False):
    """Same cream ticket card as bansos_design.card, tighter metrics
    (title +80, rows from +280, 140px/line, 24px row gap, +72 bottom)."""
    row_h = []
    for r in rows:
        row_h.append(len(wrap(d, r, bd.fr(112), w - 520)))
    total = 280 + sum(h * 140 + 24 for h in row_h) + 72
    d.rounded_rectangle([x, y, x + w, y + total], radius=72, fill=PAL["card"],
                        outline=PAL["card_outline"], width=6 if PAL["card_outline"] else 2)
    bd.dashed_v(d, x + 88, y + 80, y + total - 80, PAL["muted"], dash=40, gap=32, width=8)
    d.text((x + 220, y + 80), title, font=bd.mono(92, bold=True), fill=PAL["ink"])
    yy = y + 280
    for i, r in enumerate(rows):
        if numbered:
            d.ellipse([x + 220, yy + 4, x + 356, yy + 140], fill=PAL["num_bg"])
            n = str(i + 1)
            d.text((x + 288 - d.textlength(n, font=bd.f(88)) / 2, yy + 20), n,
                   font=bd.f(88), fill=PAL["num_text"])
        else:
            d.rectangle([x + 232, yy + 28, x + 320, yy + 116], fill=PAL["check"],
                        outline=PAL["ink"], width=6)
        for ln in wrap(d, r, bd.fr(112), w - 520):
            d.text((x + 430, yy), ln, font=bd.fr(112), fill=PAL["ink"])
            yy += 140
        yy += 24
    return total


def slide2_fix(spec):
    img = bd.Image.new("RGB", (S, S), PAL["bg"])
    d = bd.ImageDraw.Draw(img)
    bd.lockup(img, cy=256, mh=208, color=PAL["lockup"], chip=PAL["lockup_chip"])
    d.text((220, 560), "SYARAT & CARA KLAIM", font=bd.f(208), fill=PAL["text_bg"])
    d.rectangle([220, 840, 1280, 876], fill=PAL["underline"])
    y = 1040
    y += card_tight(d, 220, y, 3656, "SYARATNYA", spec["syarat"][:5]) + 60
    y += card_tight(d, 220, y, 3656, "CARA KLAIM", spec["steps"][:4], numbered=True) + 60

    # Honest-catch band (locked rule: catch must be printed on a slide).
    catch_lines = wrap(d, spec["catch"], bd.fr(104), 3560)
    assert len(catch_lines) <= 2, f"catch wraps to {len(catch_lines)} lines"
    band_y = y
    band_h = 36 + len(catch_lines) * 124 + 36
    d.rounded_rectangle([220, band_y, 3876, band_y + band_h], radius=48,
                        outline=RED, width=10)
    d.rounded_rectangle([238, band_y + 18, 3858, band_y + band_h - 18], radius=40,
                        outline=RED, width=4)
    ty = band_y + 36
    for ln in catch_lines:
        d.text((268, ty), ln, font=bd.fr(104), fill=PAL["text_bg"])
        ty += 124
    end = band_y + band_h
    assert end + 320 <= S, f"slide 2 content too tall (ends {end})"

    d.text((220, 3740), f"Sumber resmi: {spec['fields']['sumber']}", font=bd.fr(92),
           fill=PAL["subtitle"])
    d.text((220, 3876), "Save biar nggak lupa. Tag teman yang butuh.", font=bd.f(100),
           fill=PAL["text_bg"])
    return img


def main():
    spec = json.load(open(sys.argv[1]))
    out = spec["out_dir"]
    slide2_fix(spec).save(f"{out}/bansos-02.png")
    print("OK slide 2 fixed", out)


if __name__ == "__main__":
    main()
