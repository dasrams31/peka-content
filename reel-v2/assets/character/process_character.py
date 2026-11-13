#!/usr/bin/env python3
"""Post-process the generated anime character states.

- Flood-fills the connected near-black background (from the corners)
  to transparent, so the grid shows through and the character does not
  sit on a black box. Interior black areas (eye, mouth, P counter)
  are enclosed by yellow, so they stay opaque.
- Crops BOTH states with the SAME union bounding box so the two
  images stay pixel-aligned when the renderer swaps them per frame
  (otherwise the character would jitter when the mouth toggles).
- Saves clean assets: piko-anime-closed.png / piko-anime-open.png
"""
import os
from PIL import Image, ImageDraw

BASE = "/home/hatch/workspace/peka-content/reel-v2/assets/character"
SRC = {
    "closed": os.path.join(BASE, "media-generation-piko-anime-closed-0-b782a2cc-fca0-418d-87d8-80e5a2c0b243.png"),
    "open": os.path.join(BASE, "media-generation-piko-anime-open-0-fd7bf59a-9b73-4920-a3a7-5445a342e734.png"),
}
PAD = 16


def to_rgba(path):
    img = Image.open(path).convert("RGB")
    print(path, img.size, img.mode)
    # Sample the four corners: they must be (near) black background.
    w, h = img.size
    for xy in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1), (w // 2, 0)]:
        print("  corner", xy, img.getpixel(xy))
    mask = img.convert("L").copy()
    ImageDraw.floodfill(mask, (0, 0), 255, thresh=35)
    # Binary: flood-filled background (255) -> transparent, everything
    # else -> fully opaque. (A plain 255-v inversion would leak the
    # character's own grayscale shading into the alpha channel.)
    alpha = mask.point(lambda v: 0 if v == 255 else 255)
    rgba = img.convert("RGBA")
    rgba.putalpha(alpha)
    return rgba


def main():
    out = {}
    for name, path in SRC.items():
        out[name] = to_rgba(path)
    # Union bbox so both states share one crop box (pixel alignment).
    boxes = [im.getchannel("A").getbbox() for im in out.values()]
    print("bboxes:", boxes)
    x0 = min(b[0] for b in boxes) - PAD
    y0 = min(b[1] for b in boxes) - PAD
    x1 = max(b[2] for b in boxes) + PAD
    y1 = max(b[3] for b in boxes) + PAD
    box = (max(0, x0), max(0, y0), x1, y1)
    print("union crop box:", box)
    for name, im in out.items():
        cropped = im.crop(box)
        dest = os.path.join(BASE, f"piko-anime-{name}.png")
        cropped.save(dest)
        print("saved", dest, cropped.size)

    # Verification composite: character on a dark-grid background,
    # like the reel stage, to check readability + alignment.
    from PIL import Image as I
    grid = I.new("RGB", (1080, 1920), (10, 10, 16))
    d = ImageDraw.Draw(grid)
    for x in range(0, 1080, 60):
        d.line([(x, 0), (x, 1920)], fill=(28, 28, 36))
    for y in range(0, 1920, 60):
        d.line([(0, y), (1080, y)], fill=(28, 28, 36))
    for name in ("closed", "open"):
        im = Image.open(os.path.join(BASE, f"piko-anime-{name}.png"))
        w = 420
        im2 = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
        canvas = grid.copy()
        canvas.paste(im2, (600, 1150), im2)
        canvas.save(f"/tmp/char-check-{name}.jpg", quality=90)
        print(f"check /tmp/char-check-{name}.jpg")


main()
