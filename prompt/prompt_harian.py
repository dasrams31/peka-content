#!/usr/bin/env python3
"""Prompt Harian carousel generator (2 slides, 2048x2048).

Design: two-tone flip. Slide 1 = Peka yellow with giant black type and a
tilted chat-bubble teaser. Slide 2 = black with the full prompt inside a
yellow chat bubble (mono type), usage tips, and a comment trigger.
Locked Peka lockup top-right on both slides (mascot + peka.ai.id).

Usage: python3 prompt_harian.py <spec.json>
Spec: {"episode": 1, "category": "KONTEN", "title": "...", "prompt": "...",
       "tips": ["...", "...", "..."], "out_dir": "/abs/path"}
"""
import json
import sys

from PIL import Image, ImageDraw, ImageFont

S = 2048
YELLOW = (255, 214, 10)
BLACK = (17, 17, 17)
INK = (22, 22, 22)
WHITE = (255, 255, 255)
GRAY = (168, 168, 158)

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
    """Locked Peka lockup: mascot + 'peka.ai.id', right edge at x=1938."""
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


def pill(d, x, y, text, font, fill=None, txt=None, outline=None, pad_x=34, pad_y=16):
    tw = d.textlength(text, font=font)
    ascent, descent = font.getmetrics()
    th = ascent + descent
    box = [x, y, x + tw + pad_x * 2, y + th + pad_y * 2]
    d.rounded_rectangle(box, radius=(box[3] - box[1]) // 2, fill=fill, outline=outline, width=5 if outline else 1)
    d.text((x + pad_x, y + pad_y - 2), text, font=font, fill=txt)
    return box[2]


def slide1(spec):
    img = Image.new("RGB", (S, S), YELLOW)
    d = ImageDraw.Draw(img)
    lockup(img, cy=128, mh=104, color=INK, chip=BLACK)

    # chips row
    x = pill(d, 110, 300, f"EDISI #{spec['episode']:02d}", f(52), fill=BLACK, txt=YELLOW)
    pill(d, x + 26, 300, spec["category"].upper(), f(52), fill=None, txt=INK, outline=INK)

    # giant type
    d.text((104, 470), "PROMPT", font=f(330), fill=INK)
    d.text((104, 800), "HARIAN", font=f(330), fill=INK)

    # use-case headline
    hl = wrap(d, spec["title"], f(88), 1830)
    if len(hl) > 2:
        raise SystemExit("OVERFLOW: title wraps to >2 lines at 88px")
    y = 1210
    for ln in hl:
        d.text((110, y), ln, font=f(88), fill=INK)
        y += 112

    # tilted chat bubble teaser (drawn on its own layer, rotated -2 deg)
    bw, bh = 1560, 330
    layer = Image.new("RGBA", (bw + 80, bh + 80), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rounded_rectangle([40, 40, 40 + bw, 40 + bh], radius=54, fill=WHITE)
    ld.polygon([(180, 40 + bh - 2), (330, 40 + bh - 2), (215, 40 + bh + 62)], fill=WHITE)
    tag = "ISI PROMPT-NYA"
    tag_w = ld.textlength(tag, font=f(40)) + 76
    ld.rounded_rectangle([40, 40, 40 + tag_w, 118], radius=24, fill=BLACK)
    ld.text((78, 58), tag, font=f(40), fill=YELLOW)
    teaser = spec["prompt"]
    if len(teaser) > 118:
        teaser = teaser[:118].rsplit(" ", 1)[0] + "..."
    tl = wrap(ld, teaser, mono(47), bw - 110)
    ty = 150
    for ln in tl[:3]:
        ld.text((95, ty), ln, font=mono(47), fill=INK)
        ty += 64
    layer = layer.rotate(2, resample=Image.BICUBIC, expand=True)
    img.paste(layer, (150, 1435), layer)

    # bottom strip
    d.rectangle([0, S - 168, S, S], fill=BLACK)
    d.text((110, S - 122), "GESER BUAT PROMPT LENGKAPNYA →", font=f(58), fill=YELLOW)
    tail = "tiap hari 12:30"
    d.text((1938 - d.textlength(tail, font=fr(46)), S - 112), tail, font=fr(46), fill=WHITE)
    return img


def slide2(spec):
    img = Image.new("RGB", (S, S), BLACK)
    d = ImageDraw.Draw(img)
    lockup(img, cy=128, mh=104, color=YELLOW)

    pill(d, 110, 300, "PROMPT SIAP SALIN", f(52), fill=YELLOW, txt=INK)

    # prompt bubble, auto-fit font
    box_x, box_w = 110, 1828
    size = 50
    while size > 34:
        pf = mono(size, bold=True)
        lines = wrap(d, spec["prompt"], pf, box_w - 130)
        need = len(lines) * int(size * 1.42) + 215
        if need <= 920:
            break
        size -= 3
    else:
        raise SystemExit("OVERFLOW: prompt too long for the bubble")
    box_y = 470
    box_h = need
    d.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h], radius=56, fill=YELLOW)
    d.polygon([(box_x + 130, box_y + box_h - 2), (box_x + 300, box_y + box_h - 2),
               (box_x + 175, box_y + box_h + 64)], fill=YELLOW)
    # copy glyph lives in the band above the text so it never touches it
    gx, gy = box_x + box_w - 190, box_y + 36
    d.rounded_rectangle([gx + 26, gy, gx + 96, gy + 70], radius=12, outline=INK, width=7)
    d.rounded_rectangle([gx, gy + 26, gx + 70, gy + 96], radius=12, outline=INK, width=7, fill=YELLOW)
    ty = box_y + 160
    for ln in lines:
        d.text((box_x + 65, ty), ln, font=pf, fill=INK)
        ty += int(size * 1.42)

    # tips
    y = box_y + box_h + 130
    d.text((110, y), "CARA PAKAI", font=f(52), fill=YELLOW)
    y += 92
    for tip in spec["tips"][:3]:
        tl = wrap(d, tip, fr(56), 1690)
        d.rectangle([110, y + 22, 142, y + 54], fill=YELLOW)
        for ln in tl:
            d.text((185, y), ln, font=fr(56), fill=WHITE)
            y += 74
        y += 26

    # footer trigger
    d.line([110, S - 300, 1938, S - 300], fill=(70, 70, 70), width=3)
    d.text((110, S - 245), "Udah nyoba? Spill hasilnya di komentar.", font=f(62), fill=WHITE)
    foot = f"Prompt Harian #{spec['episode']:02d} - besok 12:30 prompt baru lagi"
    d.text((110, S - 140), foot, font=fr(46), fill=GRAY)
    return img


def main():
    spec = json.load(open(sys.argv[1]))
    out = spec["out_dir"]
    import os
    os.makedirs(out, exist_ok=True)
    slide1(spec).save(f"{out}/prompt-01.png")
    slide2(spec).save(f"{out}/prompt-02.png")
    print("OK", out)


if __name__ == "__main__":
    main()
