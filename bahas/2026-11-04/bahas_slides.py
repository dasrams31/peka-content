#!/usr/bin/env python3
"""Bahas-bersama carousel: humanizer-lint SKILL discussion from the Prompt #13
comment thread (@yanstd888 + @meta.ai). 2 slides, 4096x4096.

Design: the locked Prompt Harian two-tone flip template, reused verbatim
(helpers copied from prompt/prompt_harian.py): slide 1 = Peka yellow with
giant black type, locked lockup top-right, chips row, tilted chat-bubble
teaser, black bottom strip. Slide 2 = black with the mechanics inside a
yellow chat bubble, honesty-boundary tips, footer trigger. Fonts are
DejaVu (Bold/regular/mono), mascot is the chroma-keyed mascot-p.png.

Content framing: the thread is about a SKILL (an agent skill repo file),
not generic writing tips. Nothing is claimed about the skill being public:
the comment says it is still being tinkered with.
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = HERE

S = 4096
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
    """Locked Peka lockup: mascot + 'peka.ai.id', right edge at x=3876."""
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


def pill(d, x, y, text, font, fill=None, txt=None, outline=None, pad_x=68, pad_y=32):
    tw = d.textlength(text, font=font)
    ascent, descent = font.getmetrics()
    th = ascent + descent
    box = [x, y, x + tw + pad_x * 2, y + th + pad_y * 2]
    d.rounded_rectangle(box, radius=(box[3] - box[1]) // 2, fill=fill, outline=outline, width=10 if outline else 2)
    d.text((x + pad_x, y + pad_y - 4), text, font=font, fill=txt)
    return box[2]


def giant_size(d, text, start=600, max_w=3656):
    size = start
    while size > 200:
        if d.textlength(text, font=f(size)) <= max_w:
            return size
        size -= 20
    raise SystemExit(f"OVERFLOW: giant word {text!r} does not fit")


def slide1():
    img = Image.new("RGB", (S, S), YELLOW)
    d = ImageDraw.Draw(img)
    lockup(img, cy=256, mh=208, color=INK, chip=BLACK)

    # chips row
    x = pill(d, 220, 600, "BAHAS BARENG", f(104), fill=BLACK, txt=YELLOW)
    pill(d, x + 52, 600, "KOMENTAR #13", f(104), fill=None, txt=INK, outline=INK)

    # giant type (auto-fit so HUMANIZER fits the template width)
    g1 = giant_size(d, "HUMANIZER")
    d.text((208, 940), "HUMANIZER", font=f(g1), fill=INK)
    d.text((208, 1600), "LINT.", font=f(660), fill=INK)

    # use-case headline
    hl = wrap(d, "Skill yang nge-lint tulisan AI biar gak kaku. Lagi diulik @meta.ai.",
              f(176), 3660)
    if len(hl) > 2:
        raise SystemExit("OVERFLOW: headline wraps to >2 lines at 176px")
    y = 2420
    for ln in hl:
        d.text((220, y), ln, font=f(176), fill=INK)
        y += 224

    # tilted chat bubble teaser (drawn on its own layer, rotated -2 deg)
    bw, bh = 3120, 660
    layer = Image.new("RGBA", (bw + 160, bh + 160), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rounded_rectangle([80, 80, 80 + bw, 80 + bh], radius=108, fill=WHITE)
    ld.polygon([(360, 80 + bh - 4), (660, 80 + bh - 4), (430, 80 + bh + 124)], fill=WHITE)
    tag = "SKILL ITU APA?"
    tag_w = ld.textlength(tag, font=f(80)) + 152
    ld.rounded_rectangle([80, 80, 80 + tag_w, 236], radius=48, fill=BLACK)
    ld.text((156, 116), tag, font=f(80), fill=YELLOW)
    teaser = ("Satu file SKILL.md berisi pola tulisan AI. Diinstall sekali, "
              "dipanggil pakai slash command.")
    if len(teaser) > 118:
        teaser = teaser[:118].rsplit(" ", 1)[0] + "..."
    tl = wrap(ld, teaser, mono(94), bw - 220)
    ty = 300
    for ln in tl[:3]:
        ld.text((190, ty), ln, font=mono(94), fill=INK)
        ty += 128
    layer = layer.rotate(2, resample=Image.BICUBIC, expand=True)
    img.paste(layer, (300, 2870), layer)

    # bottom strip
    d.rectangle([0, S - 336, S, S], fill=BLACK)
    d.text((220, S - 244), "GESER BUAT CARA KERJANYA →", font=f(116), fill=YELLOW)
    tail = "GABUNG KE KOMUNITAS KAMI: URL.PEKA.AI.ID"
    d.text((3876 - d.textlength(tail, font=fr(68)), S - 220), tail, font=fr(68), fill=YELLOW)
    return img


def slide2():
    img = Image.new("RGB", (S, S), BLACK)
    d = ImageDraw.Draw(img)
    lockup(img, cy=256, mh=208, color=YELLOW)

    pill(d, 220, 600, "CARA KERJA SKILL-NYA", f(104), fill=YELLOW, txt=INK)

    # mechanics bubble, auto-fit font
    mechanics = ("1 FILE: satu file SKILL.md, instruksi siap pakai. "
                 "2 PANGGIL: install sekali, panggil pakai slash command. "
                 "3 LINT: cek pola AI, tandai, kamu yang benerin.")
    box_x, box_w = 220, 3656
    size = 100
    while size > 68:
        pf = mono(size, bold=True)
        lines = wrap(d, mechanics, pf, box_w - 260)
        need = len(lines) * int(size * 1.42) + 430
        if need <= 1840:
            break
        size -= 6
    else:
        raise SystemExit("OVERFLOW: mechanics too long for the bubble")
    box_y = 940
    box_h = need
    d.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h], radius=112, fill=YELLOW)
    d.polygon([(box_x + 260, box_y + box_h - 4), (box_x + 600, box_y + box_h - 4),
               (box_x + 350, box_y + box_h + 128)], fill=YELLOW)
    ty = box_y + 320
    for ln in lines:
        d.text((box_x + 130, ty), ln, font=pf, fill=INK)
        ty += int(size * 1.42)

    # honesty boundary tips
    y = box_y + box_h + 260
    d.text((220, y), "BATAS JUJURNYA", font=f(104), fill=YELLOW)
    y += 184
    for tip in ["Lint itu nunjukin polanya, bukan nyamar.",
                "Fakta tetap, yang berubah cuma bahasanya.",
                "Kalau kampusmu melarang AI, jangan pakai."]:
        tl = wrap(d, tip, fr(112), 3380)
        d.rectangle([220, y + 44, 284, y + 108], fill=YELLOW)
        for ln in tl:
            d.text((370, y), ln, font=fr(112), fill=WHITE)
            y += 148
        y += 52

    # footer trigger
    d.line([220, S - 600, 3876, S - 600], fill=(70, 70, 70), width=6)
    d.text((220, S - 490), "Obrolan ini mulai dari komentar di edisi #13.",
           font=f(124), fill=WHITE)
    foot = "Bahas bareng - komentar edisi #13"
    d.text((220, S - 280), foot, font=fr(92), fill=GRAY)
    join = "GABUNG KE KOMUNITAS KAMI: URL.PEKA.AI.ID"
    d.text((3876 - d.textlength(join, font=fr(72)), S - 270), join, font=fr(72), fill=GRAY)
    return img


def main():
    os.makedirs(OUT, exist_ok=True)
    slide1().save(f"{OUT}/bahas-01.png")
    slide2().save(f"{OUT}/bahas-02.png")
    print("OK", OUT)


if __name__ == "__main__":
    main()
