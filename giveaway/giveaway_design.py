#!/usr/bin/env python3
"""Giveaway Malam Minggu carousel generator v2 (3 slides, 2048x2048).

Usage: python3 giveaway_design.py <spec.json>
Spec fields: series, prize_top, prize_bottom, subline, subline2,
deadline_line, requirements[], note, deadline_lines[], announce_lines[],
closing, out_dir.
Brand: yellow #FFD60A on black #111111, Poppins, mascot lockup top-right,
locked footer (community line left, page number right).
"""
import json
import sys

from PIL import Image, ImageDraw, ImageFont

YELLOW = (255, 214, 10)
BLACK = (17, 17, 17)
CARD = (27, 32, 46)
BORDER = (58, 64, 82)
WHITE = (245, 245, 245)
GRAY = (154, 146, 127)
HAIRLINE = (56, 56, 56)
FOOTDIM = (90, 82, 60)

FD = "/home/hatch/workspace/sertiku-poster/fonts/"
PX = FD + "Poppins-ExtraBold.ttf"
PB = FD + "Poppins-Bold.ttf"
PS = FD + "Poppins-SemiBold.ttf"
FM = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FMB = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

W = 2048
MARGIN = 110
INNER = W - 2 * MARGIN


def F(path, sz):
    return ImageFont.truetype(path, sz)


def fit_font(d, text, path, max_w, start, floor=40):
    sz = start
    while sz > floor:
        f = F(path, sz)
        if d.textlength(text, font=f) <= max_w:
            return f
        sz -= 8
    return F(path, floor)


def wrap(d, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# --- mascot lockup (same chroma-key source as bansos/spill generators) ---
_m = Image.open("/home/hatch/workspace/peka-logo/mascot-p.png").convert("RGB")
_mmask = Image.new("L", _m.size, 0)
_mp, _mk = _m.load(), _mmask.load()
for yy in range(_m.size[1]):
    for xx in range(_m.size[0]):
        r, g, b = _mp[xx, yy]
        if r > 30 or g > 30 or b > 30:
            _mk[xx, yy] = 255
_creature = _m.crop(_mmask.getbbox())
_cmask = _mmask.crop(_mmask.getbbox())


def lockup(img, cy, mh, color, chip=None):
    d = ImageDraw.Draw(img)
    cr = _creature.resize((int(_creature.width * mh / _creature.height), mh), Image.LANCZOS)
    mr = _cmask.resize(cr.size, Image.LANCZOS)
    tf = F(FMB, int(mh * 0.72))
    label = "peka.ai.id"
    ascent, descent = tf.getmetrics()
    tx = 1938 - d.textlength(label, font=tf)
    ty = cy - (ascent + descent) // 2
    mx, my = int(tx - 26 - cr.width), cy - mh // 2
    if chip is not None:
        pad = 20
        d.rounded_rectangle([mx - pad, my - pad, mx + cr.width + pad, my + mh + pad],
                            radius=34, fill=chip)
    img.paste(cr, (mx, my), mr)
    d.text((tx, ty), label, font=tf, fill=color)


def footer(d, page, total, color):
    d.text((MARGIN, 1932), "GABUNG KE KOMUNITAS KAMI: URL.PEKA.AI.ID",
           font=F(FM, 40), fill=color)
    t = f"{page}/{total}"
    d.text((1938 - d.textlength(t, font=F(FMB, 44)), 1926), t, font=F(FMB, 44), fill=color)


def pill(d, x, y, text, font, fill, txt_color):
    tw = d.textlength(text, font=font)
    h = 88
    d.rounded_rectangle([x, y, x + tw + 64, y + h], radius=h // 2, fill=fill)
    d.text((x + 32, y + h // 2 - 30), text, font=font, fill=txt_color)
    return x + tw + 64


def slide1(spec):
    img = Image.new("RGB", (W, W), BLACK)
    d = ImageDraw.Draw(img)
    lockup(img, 150, 108, YELLOW)
    d.text((MARGIN, 116), "GIVEAWAY MALAM MINGGU", font=F(FMB, 60), fill=YELLOW)
    kw = d.textlength("GIVEAWAY MALAM MINGGU", font=F(FMB, 60))
    pill(d, MARGIN + kw + 40, 104, spec["series"], F(FMB, 52), YELLOW, BLACK)
    gf = fit_font(d, "GIVEAWAY", PX, INNER, 320)
    d.text((MARGIN, 320), "GIVEAWAY", font=gf, fill=WHITE)
    # prize panel
    py0, py1 = 690, 1332
    d.rounded_rectangle([MARGIN, py0, W - MARGIN, py1], radius=48, fill=YELLOW)
    d.text((MARGIN + 84, py0 + 58), "HADIAH UTAMA BUAT 2 PEMENANG", font=F(FMB, 48), fill=BLACK)
    d.line([MARGIN + 84, py0 + 148, W - MARGIN - 84, py0 + 148], fill=BLACK, width=4)
    pf1 = fit_font(d, spec["prize_top"], PX, INNER - 168, 240)
    d.text((MARGIN + 84, py0 + 182), spec["prize_top"], font=pf1, fill=BLACK)
    pf2 = fit_font(d, spec["prize_bottom"], PX, INNER - 560, 185)
    d.text((MARGIN + 84, py0 + 420), spec["prize_bottom"], font=pf2, fill=BLACK)
    pill(d, W - MARGIN - 84 - 300, py0 + 440, "GRATIS", F(FMB, 56), BLACK, YELLOW)
    y = 1416
    for line in wrap(d, spec["subline"], F(PS, 64), INNER):
        d.text((MARGIN, y), line, font=F(PS, 64), fill=WHITE)
        y += 90
    d.text((MARGIN, y + 14), spec["subline2"], font=F(PS, 58), fill=GRAY)
    d.line([MARGIN, 1712, W - MARGIN, 1712], fill=HAIRLINE, width=3)
    d.text((MARGIN, 1752), spec["deadline_line"], font=F(FM, 46), fill=GRAY)
    gt = "GESER ->"
    gf2 = F(PB, 66)
    d.text((1938 - d.textlength(gt, font=gf2), 1740), gt, font=gf2, fill=YELLOW)
    footer(d, 1, 3, GRAY)
    return img


def slide2(spec):
    img = Image.new("RGB", (W, W), YELLOW)
    d = ImageDraw.Draw(img)
    lockup(img, 150, 108, BLACK, chip=BLACK)
    d.text((MARGIN, 116), "SYARAT IKUT", font=F(FMB, 60), fill=BLACK)
    tf = fit_font(d, "CARA IKUTNYA", PX, INNER, 190)
    d.text((MARGIN, 236), "CARA IKUTNYA", font=tf, fill=BLACK)
    d.text((MARGIN, 472), "Lima langkah, dua menit beres.", font=F(PS, 60), fill=BLACK)
    y = 600
    rf = F(PS, 62)
    for i, req in enumerate(spec["requirements"], 1):
        lines = wrap(d, req, rf, INNER - 320)
        rh = max(152, 48 + len(lines) * 84)
        d.rounded_rectangle([MARGIN, y, W - MARGIN, y + rh], radius=36, fill=BLACK)
        cx, cy, r = MARGIN + 108, y + rh // 2, 48
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=YELLOW)
        nf = F(PX, 56)
        nw = d.textlength(str(i), font=nf)
        d.text((cx - nw / 2, cy - 42), str(i), font=nf, fill=BLACK)
        ly = y + (rh - len(lines) * 84) // 2 + 4
        for line in lines:
            d.text((MARGIN + 250, ly), line, font=rf, fill=WHITE)
            ly += 84
        y += rh + 30
    ny = y + 26
    for line in wrap(d, spec["note"], F(FM, 44), INNER):
        d.text((MARGIN, ny), line, font=F(FM, 44), fill=BLACK)
        ny += 62
    footer(d, 2, 3, FOOTDIM)
    return img


def info_card(d, y, label, lines):
    h = 362
    d.rounded_rectangle([MARGIN, y, W - MARGIN, y + h], radius=40, fill=CARD, outline=BORDER, width=3)
    d.text((MARGIN + 64, y + 50), label, font=F(FMB, 50), fill=YELLOW)
    ly = y + 126
    for line in lines:
        lf = fit_font(d, line, PB, INNER - 128, 80, floor=58)
        d.text((MARGIN + 64, ly), line, font=lf, fill=WHITE)
        ly += 108
    return y + h


def slide3(spec):
    img = Image.new("RGB", (W, W), BLACK)
    d = ImageDraw.Draw(img)
    lockup(img, 150, 108, YELLOW)
    d.text((MARGIN, 116), "DEADLINE + PENGUMUMAN", font=F(FMB, 60), fill=YELLOW)
    tf = fit_font(d, "CATAT TANGGALNYA", PX, INNER, 175)
    d.text((MARGIN, 236), "CATAT TANGGALNYA", font=tf, fill=WHITE)
    y = info_card(d, 520, "DEADLINE IKUT", spec["deadline_lines"])
    y = info_card(d, y + 44, "PENGUMUMAN PEMENANG", spec["announce_lines"])
    cy0 = y + 58
    d.rounded_rectangle([MARGIN, cy0, W - MARGIN, cy0 + 430], radius=48, fill=YELLOW)
    cf = fit_font(d, "GABUNG GRUP WHATSAPP", PX, INNER - 160, 118)
    d.text((MARGIN + 80, cy0 + 64), "GABUNG GRUP WHATSAPP", font=cf, fill=BLACK)
    uf = fit_font(d, "url.peka.ai.id", PX, INNER - 160, 118)
    d.text((MARGIN + 80, cy0 + 224), "url.peka.ai.id", font=uf, fill=BLACK)
    d.text((MARGIN, cy0 + 500), spec["closing"], font=F(PS, 58), fill=GRAY)
    footer(d, 3, 3, GRAY)
    return img


def main():
    spec = json.load(open(sys.argv[1]))
    out = spec["out_dir"]
    slide1(spec).save(f"{out}/giveaway-01.png")
    slide2(spec).save(f"{out}/giveaway-02.png")
    slide3(spec).save(f"{out}/giveaway-03.png")
    print("OK", out)


if __name__ == "__main__":
    main()
