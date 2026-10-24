#!/usr/bin/env python3
"""Giveaway follow-up reminder carousel (3 slides, 2048x2048).

Reuses the brand system from giveaway_design.py (same header, prize panel,
footer, slide 2 requirements, slide 3 deadline cards) but replaces the slide 1
giant word with TERAKHIR / BESOK for the last-chance reminder.
Usage: python3 followup_design.py <spec.json>
"""
import json
import sys

sys.path.insert(0, "/home/hatch/workspace/peka-content/giveaway")
from giveaway_design import (  # noqa: E402
    BLACK, F, FMB, GRAY, HAIRLINE, INNER, MARGIN, PB, PS, PX, W, YELLOW,
    fit_font, footer, lockup, pill, slide2, slide3, wrap,
)
from PIL import Image, ImageDraw  # noqa: E402

FM = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def slide1_followup(spec):
    img = Image.new("RGB", (W, W), BLACK)
    d = ImageDraw.Draw(img)
    lockup(img, 150, 108, YELLOW)
    d.text((MARGIN, 116), "GIVEAWAY MALAM MINGGU", font=F(FMB, 60), fill=YELLOW)
    kw = d.textlength("GIVEAWAY MALAM MINGGU", font=F(FMB, 60))
    pill(d, MARGIN + kw + 40, 104, spec["series"], F(FMB, 52), YELLOW, BLACK)
    f1 = fit_font(d, "TERAKHIR", PX, INNER, 240)
    d.text((MARGIN, 240), "TERAKHIR", font=f1, fill=(245, 245, 245))
    f2 = fit_font(d, "BESOK", PX, INNER, 240)
    d.text((MARGIN, 530), "BESOK", font=f2, fill=YELLOW)
    # prize panel (same internal geometry as the original)
    py0, py1 = 850, 1492
    d.rounded_rectangle([MARGIN, py0, W - MARGIN, py1], radius=48, fill=YELLOW)
    d.text((MARGIN + 84, py0 + 58), "HADIAH UTAMA BUAT 2 PEMENANG",
           font=F(FMB, 48), fill=BLACK)
    d.line([MARGIN + 84, py0 + 148, W - MARGIN - 84, py0 + 148],
           fill=BLACK, width=4)
    pf1 = fit_font(d, spec["prize_top"], PX, INNER - 168, 240)
    d.text((MARGIN + 84, py0 + 182), spec["prize_top"], font=pf1, fill=BLACK)
    pf2 = fit_font(d, spec["prize_bottom"], PX, INNER - 560, 185)
    d.text((MARGIN + 84, py0 + 420), spec["prize_bottom"], font=pf2, fill=BLACK)
    pill(d, W - MARGIN - 84 - 300, py0 + 440, "GRATIS", F(FMB, 56), BLACK, YELLOW)
    y = 1576
    for line in wrap(d, spec["subline"], F(PS, 64), INNER):
        d.text((MARGIN, y), line, font=F(PS, 64), fill=(245, 245, 245))
        y += 90
    d.line([MARGIN, 1712, W - MARGIN, 1712], fill=HAIRLINE, width=3)
    d.text((MARGIN, 1752), spec["deadline_line"], font=F(FM, 46), fill=GRAY)
    gt = "GESER ->"
    gf2 = F(PB, 66)
    d.text((1938 - d.textlength(gt, font=gf2), 1740), gt, font=gf2, fill=YELLOW)
    footer(d, 1, 3, GRAY)
    return img


def main():
    spec = json.load(open(sys.argv[1]))
    out = spec["out_dir"]
    slide1_followup(spec).save(f"{out}/followup-01.png")
    slide2(spec).save(f"{out}/followup-02.png")
    slide3(spec).save(f"{out}/followup-03.png")
    print("OK", out)


if __name__ == "__main__":
    main()
