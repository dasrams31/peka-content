#!/usr/bin/env python3
"""Peka.ai.id mascot - deterministic PIL rendering."""
from PIL import Image, ImageDraw
import math

BG = (0x11, 0x11, 0x11)
YL = (0xFF, 0xD6, 0x0A)
S = 1080

def spark(d, cx, cy, R, r, fill):
    pts = []
    for i in range(8):
        ang = math.pi / 2 + i * math.pi / 4
        rad = R if i % 2 == 0 else r
        pts.append((cx + rad * math.cos(ang), cy - rad * math.sin(ang)))
    d.polygon(pts, fill=fill)

def mascot(path):
    im = Image.new("RGB", (S, S), BG)
    d = ImageDraw.Draw(im)
    cx = S // 2
    # antenna
    d.rounded_rectangle([cx - 15, 215, cx + 15, 320], radius=15, fill=YL)
    d.ellipse([cx - 32, 150, cx + 32, 214], fill=YL)
    # arms (behind body)
    d.rounded_rectangle([cx - 195, 700, cx - 128, 815], radius=33, fill=YL)
    d.rounded_rectangle([cx + 128, 700, cx + 195, 815], radius=33, fill=YL)
    # body
    d.rounded_rectangle([cx - 120, 668, cx + 120, 884], radius=60, fill=YL)
    # spark emblem on chest
    spark(d, cx, 776, 46, 11, BG)
    # head
    d.rounded_rectangle([cx - 210, 300, cx + 210, 664], radius=120, fill=YL)
    # eyes
    for ex in (cx - 92, cx + 92):
        d.ellipse([ex - 56, 424, ex + 56, 536], fill=BG)
    # smile
    d.arc([cx - 66, 500, cx + 66, 632], start=25, end=155, fill=BG, width=24)
    im.save(path)

def mascot_p(path):
    """P-creature: the letter P itself as a mascot. One big eye, ownable."""
    im = Image.new("RGB", (S, S), BG)
    d = ImageDraw.Draw(im)
    # antenna
    d.rounded_rectangle([507, 232, 523, 332], radius=8, fill=YL)
    d.ellipse([487, 177, 543, 233], fill=YL)
    # stem (body)
    d.rounded_rectangle([450, 330, 580, 822], radius=65, fill=YL)
    # bowl: thinner, cleaner
    d.arc([600 - 140, 455 - 140, 600 + 140, 455 + 140], start=-90, end=90, fill=YL, width=100)
    # one big eye on the stem
    d.ellipse([465, 400, 555, 490], fill=BG)
    # smile
    d.arc([470, 515, 550, 595], start=25, end=155, fill=BG, width=18)
    im.save(path)

if __name__ == "__main__":
    mascot("/home/hatch/workspace/peka-logo/mascot.png")
    Image.open("/home/hatch/workspace/peka-logo/mascot.png").resize((96, 96), Image.LANCZOS).save("/home/hatch/workspace/peka-logo/mascot-96.png")
    mascot_p("/home/hatch/workspace/peka-logo/mascot-p.png")
    Image.open("/home/hatch/workspace/peka-logo/mascot-p.png").resize((96, 96), Image.LANCZOS).save("/home/hatch/workspace/peka-logo/mascot-p-96.png")
    print("done")
