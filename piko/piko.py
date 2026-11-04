#!/usr/bin/env python3
"""Piko - the Peka mascot as a voice-agent character.

Deterministic PIL rendering. The body geometry is locked to mascot_p()
in ~/workspace/peka-logo/mascot.py (same coordinates, same yellow
#FFD60A). Only the face changes between states, so every state is
unmistakably the same character.

States:
  idle      - the locked mascot face, unchanged.
  listening - wider eye, small open mouth, glow ring on the antenna ball.
  speaking  - open mouth.
  roast     - angled brow, half-lidded eye, smirk (the "judes" mode).

Background is transparent; face features are drawn in INK (#111111),
the same dark tone as the Peka canvas, so the assets sit cleanly on
any dark UI surface.
"""
from PIL import Image, ImageDraw

S = 1080
YL = (0xFF, 0xD6, 0x0A)
INK = (0x11, 0x11, 0x11)

EYE = [465, 400, 555, 490]
SMILE = [470, 515, 550, 595]


def _body(d):
    """Locked P-creature body: antenna, stem, bowl. Identical in all states."""
    # antenna
    d.rounded_rectangle([507, 232, 523, 332], radius=8, fill=YL)
    d.ellipse([487, 177, 543, 233], fill=YL)
    # stem (body)
    d.rounded_rectangle([450, 330, 580, 822], radius=65, fill=YL)
    # bowl: thinner, cleaner
    d.arc([600 - 140, 455 - 140, 600 + 140, 455 + 140],
          start=-90, end=90, fill=YL, width=100)


def _face_idle(d):
    d.ellipse(EYE, fill=INK)
    d.arc(SMILE, start=25, end=155, fill=INK, width=18)


def _face_listening(d):
    # wider eye: alert, paying attention
    d.ellipse([458, 392, 562, 498], fill=INK)
    # small open mouth
    d.ellipse([498, 532, 532, 560], fill=INK)
    # glow ring around the antenna ball
    d.ellipse([477, 167, 553, 243], outline=YL, width=6)
    d.ellipse([467, 157, 563, 253], outline=YL, width=3)


def _face_speaking(d):
    d.ellipse(EYE, fill=INK)
    # open mouth
    d.pieslice([470, 505, 550, 600], start=15, end=165, fill=INK)


def _face_roast(d):
    # half-lidded eye: yellow lid covers the top third of the eye
    d.ellipse(EYE, fill=INK)
    d.rectangle([465, 400, 555, 430], fill=YL)
    # angled brow, slanting down toward the middle of the face
    d.polygon([(452, 362), (568, 390), (564, 410), (448, 382)], fill=INK)
    # smirk: short arc with the right corner lifted
    d.arc([472, 520, 548, 592], start=30, end=150, fill=INK, width=18)
    d.line([(544, 548), (562, 530)], fill=INK, width=18)


FACES = {
    "idle": _face_idle,
    "listening": _face_listening,
    "speaking": _face_speaking,
    "roast": _face_roast,
}


def piko(state, path):
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    _body(d)
    FACES[state](d)
    im.save(path)


def sheet(paths, out):
    """2x2 character sheet on the Peka canvas color."""
    from PIL import Image as _Image
    cell = 540
    canvas = _Image.new("RGB", (cell * 2, cell * 2), INK)
    for i, p in enumerate(paths):
        tile = _Image.open(p).resize((cell, cell), _Image.LANCZOS)
        canvas.paste(tile, ((i % 2) * cell, (i // 2) * cell), tile)
    canvas.save(out)


if __name__ == "__main__":
    import os
    outdir = os.path.expanduser("~/workspace/peka-content/piko")
    os.makedirs(outdir, exist_ok=True)
    states = ["idle", "listening", "speaking", "roast"]
    paths = []
    for st in states:
        p = os.path.join(outdir, f"piko-{st}.png")
        piko(st, p)
        paths.append(p)
    sheet(paths, os.path.join(outdir, "piko-sheet.png"))
    print("done", paths)
