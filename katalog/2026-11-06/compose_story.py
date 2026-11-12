"""Compose the 9:16 Instagram Story image for the katalog edition.

Canvas 1080x1920, background #111111. Cover slide (4096x4096) scaled to
1080x1080 in the middle; top band carries the Peka lockup + kicker,
bottom band carries the headline price + order line, so no band is an
empty letterbox. Output: story-9x16.png next to this script.
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1920
BLACK = (17, 17, 17)
YELLOW = (255, 214, 10)
CREAM = (246, 241, 230)
MUTED = (170, 165, 150)

FONTS = "/home/hatch/workspace/sertiku-poster/fonts"
FB = f"{FONTS}/Poppins-Bold.ttf"
FX = f"{FONTS}/Poppins-ExtraBold.ttf"
FS = f"{FONTS}/Poppins-SemiBold.ttf"
LOCKUP = "/home/hatch/workspace/peka-content/rea-custom/peka-lockup-white-text.png"


def centered(d, text, font, fill, y):
    w = d.textlength(text, font=font)
    d.text(((W - w) / 2, y), text, font=font, fill=fill)


def tracked_centered(d, text, font, fill, y, ls):
    w = sum(d.textlength(ch, font=font) + ls for ch in text) - ls
    cx = (W - w) / 2
    for ch in text:
        d.text((cx, y), ch, font=font, fill=fill)
        cx += d.textlength(ch, font=font) + ls


img = Image.new("RGB", (W, H), BLACK)
d = ImageDraw.Draw(img)

# ---- top band (0-420): Peka lockup + kicker ----
lockup = Image.open(LOCKUP).convert("RGBA")
lw = 620
lh = int(lw * lockup.height / lockup.width)
lockup = lockup.resize((lw, lh), Image.LANCZOS)
img.paste(lockup, ((W - lw) // 2, 72), lockup)
tracked_centered(d, "KATALOG HARI INI", ImageFont.truetype(FB, 46),
                 YELLOW, 300, 6)

# ---- middle: cover slide, full width ----
cover = Image.open(os.path.join(HERE, "peka-katalog-01.png")).convert("RGB")
cover = cover.resize((1080, 1080), Image.LANCZOS)
img.paste(cover, (0, 420))

# ---- bottom band (1500-1920): headline price + order ----
centered(d, "MULAI 4K.", ImageFont.truetype(FX, 96), YELLOW, 1540)
centered(d, "14 akun premium ready hari ini.",
         ImageFont.truetype(FS, 48), CREAM, 1670)
centered(d, "DM: MAU [nama produk]  ·  s.peka.ai.id/gabung",
         ImageFont.truetype(FS, 40), MUTED, 1760)

out = os.path.join(HERE, "story-9x16.png")
img.save(out)
print(f"saved {out} {img.size}")
