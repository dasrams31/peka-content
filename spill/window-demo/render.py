#!/usr/bin/env python3
"""Prototype: SPILL repo slide with a browser-window mockup (Peka branding).

Demo only: renders ONE slide for JuliusBrussee/caveman, 1440x1920.
Data below is live from the GitHub API (27 Oct 2026), not invented.
"""
from PIL import Image, ImageDraw, ImageFont, ImageOps

W, H = 1440, 1920
BG = (17, 17, 17)
YELLOW = (255, 214, 10)
WHITE = (255, 255, 255)
DIM = (170, 170, 170)
DARK = (17, 17, 17)
GRAY = (85, 85, 85)
LIGHT_GRAY = (153, 153, 153)

FONTS = "/home/hatch/workspace/sertiku-poster/fonts"
DEJAVU = "/usr/share/fonts/truetype/dejavu"

def font(path, size):
    return ImageFont.truetype(path, size)

F_TITLE = font(f"{FONTS}/Poppins-ExtraBold.ttf", 74)
F_TITLE_LIGHT = font(f"{FONTS}/Poppins-SemiBold.ttf", 74)
F_DESC = font(f"{FONTS}/Poppins-SemiBold.ttf", 34)
F_STAT_NUM = font(f"{FONTS}/Poppins-Bold.ttf", 40)
F_STAT_LBL = font(f"{FONTS}/Poppins-SemiBold.ttf", 26)
F_BADGE = font(f"{DEJAVU}/DejaVuSansMono-Bold.ttf", 34)
F_KICKER = font(f"{DEJAVU}/DejaVuSansMono-Bold.ttf", 30)
F_URL = font(f"{DEJAVU}/DejaVuSansMono-Bold.ttf", 42)
F_BODY = font(f"{FONTS}/Poppins-SemiBold.ttf", 42)
F_CAVEAT = font(f"{FONTS}/Poppins-SemiBold.ttf", 34)
F_INSTALL = font(f"{DEJAVU}/DejaVuSansMono-Bold.ttf", 32)
F_FOOT = font(f"{FONTS}/Poppins-Bold.ttf", 30)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

def rounded_mask(size, radius):
    m = Image.new("L", size, 0)
    md = ImageDraw.Draw(m)
    md.rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius=radius, fill=255)
    return m

def wrap_text(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

# ---- top row: kicker left, stars badge right ----
d.text((90, 110), "SPILL #06  •  CLAUDE", font=F_KICKER, fill=YELLOW)
badge = "★ 115k stars"
bw = d.textlength(badge, font=F_BADGE)
d.text((W - 90 - bw, 110), badge, font=F_BADGE, fill=WHITE)

# ---- window mockup ----
WX, WY, WW = 90, 230, 1260
TITLE_H = 88
BODY_PAD = 64
AVATAR = 200
# measure body height
desc = "Viral skill + proxy for coding agents that cuts 65% of tokens by talking like a caveman."
desc_lines = wrap_text(d, desc, F_DESC, WW - 2 * BODY_PAD - AVATAR - 40)
body_h = BODY_PAD + 90 + 24 + len(desc_lines) * 48 + 70 + 116 + 14 + BODY_PAD
WH = TITLE_H + body_h
win = Image.new("RGB", (WW, WH), (255, 255, 255))
wd = ImageDraw.Draw(win)
# title bar
wd.rounded_rectangle([0, 0, WW - 1, TITLE_H + 30], radius=30, fill=(0, 0, 0))
wd.rectangle([0, TITLE_H, WW - 1, TITLE_H + 30], fill=(0, 0, 0))
for i, c in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
    wd.ellipse([36 + i * 44, 30, 36 + i * 44 + 26, 56], fill=c)
wd.text((170, 26), "JuliusBrussee/caveman", font=font(f"{DEJAVU}/DejaVuSansMono.ttf", 30), fill=(170, 170, 170))
# repo name, auto-shrunk to fit left of the avatar
name_w_max = WW - 2 * BODY_PAD - AVATAR - 40
size = 74
while size > 40:
    f_light = font(f"{FONTS}/Poppins-SemiBold.ttf", size)
    f_bold = font(f"{FONTS}/Poppins-ExtraBold.ttf", size)
    if wd.textlength("JuliusBrussee/", font=f_light) + wd.textlength("caveman", font=f_bold) <= name_w_max:
        break
    size -= 2
wd.text((BODY_PAD, y), "JuliusBrussee/", font=f_light, fill=(60, 60, 60))
w1 = wd.textlength("JuliusBrussee/", font=f_light)
wd.text((BODY_PAD + w1, y), "caveman", font=f_bold, fill=DARK)
# avatar, rounded
av = Image.open("avatar.png").convert("RGB").resize((AVATAR, AVATAR))
av = ImageOps.fit(av, (AVATAR, AVATAR))
av.putalpha(rounded_mask((AVATAR, AVATAR), 28))
win.paste(av, (WW - BODY_PAD - AVATAR, TITLE_H + BODY_PAD), av)
# description
y += 90 + 24
for line in desc_lines:
    wd.text((BODY_PAD, y), line, font=F_DESC, fill=GRAY)
    y += 48
# stats row
y += 70
stats = [("115k", "Stars"), ("6.6k", "Forks"), ("112", "Issues")]
col_w = (WW - 2 * BODY_PAD) // 3
for i, (num, lbl) in enumerate(stats):
    x = BODY_PAD + i * col_w
    wd.text((x, y), num, font=F_STAT_NUM, fill=DARK)
    wd.text((x, y + 48), lbl, font=F_STAT_LBL, fill=LIGHT_GRAY)
y += 48 + 44 + 40
# language bar
langs = [(("Go", (0, 173, 216)), 6987576), (("JavaScript", (241, 224, 90)), 3822208),
         (("TypeScript", (49, 120, 198)), 2067764), (("Python", (53, 114, 165)), 1437196)]
total = 14400000
bx, bw_total = BODY_PAD, WW - 2 * BODY_PAD
for (_, col), val in langs:
    seg = int(bw_total * val / total)
    wd.rectangle([bx, y, bx + seg - 2, y + 14], fill=col)
    bx += seg
img.paste(win, (WX, WY), rounded_mask((WW, WH), 30))

# ---- text below window ----
ty = WY + WH + 80
TX = 90
TW = W - 2 * TX
d.text((TX, ty), "github.com/JuliusBrussee/caveman", font=F_URL, fill=WHITE)
ty += 90

# benefit paragraph with one highlighted span
segs = [("ngirit token AI: ", False), ("potong token sampai 65%", True), (", tetap nyambung.", False)]
# wrap into lines keeping highlight info
words = []
for text, hl in segs:
    for w in text.split(" "):
        words.append((w, hl))
lines, cur, cur_w = [], [], 0
for w, hl in words:
    trial = cur + [(w, hl)]
    tw = d.textlength(" ".join(x[0] for x in trial), font=F_BODY)
    if tw <= TW:
        cur, cur_w = trial, tw
    else:
        lines.append(cur)
        cur = [(w, hl)]
if cur:
    lines.append(cur)
for line in lines:
    x = TX
    for w, hl in line:
        if hl:
            ww = d.textlength(w, font=F_BODY)
            d.rectangle([x - 4, ty - 2, x + ww + 4, ty + 46], fill=YELLOW)
            d.text((x, ty), w, font=F_BODY, fill=DARK)
        else:
            d.text((x, ty), w, font=F_BODY, fill=WHITE)
        x += d.textlength(w + " ", font=F_BODY)
    ty += 58
ty += 18
caveat = "tapi gaya jawabannya singkat ala caveman, kurang cocok buat dokumen formal."
for line in wrap_text(d, caveat, F_CAVEAT, TW):
    d.text((TX, ty), line, font=F_CAVEAT, fill=DIM)
    ty += 46
ty += 44
d.text((TX, ty), "pasang: npx skills add JuliusBrussee/caveman -g", font=F_INSTALL, fill=YELLOW)

# ---- footer ----
d.text((TX, H - 110), "peka.ai.id", font=F_FOOT, fill=WHITE)
handle = "@peka.ai.id"
d.text((W - TX - d.textlength(handle, font=F_FOOT), H - 110), handle, font=F_FOOT, fill=WHITE)

img.save("spill-window-demo.png")
print("saved", img.size)
