#!/usr/bin/env python3
"""Prototype: SPILL repo slide with a browser-window mockup (Peka branding).

Demo only: renders ONE slide for JuliusBrussee/caveman, 1440x1920.
Data below is live from the GitHub API (27 Oct 2026), not invented.
"""
from PIL import Image, ImageDraw, ImageFont, ImageOps

W, H = 1440, 1920
BG = (243, 243, 240)
YELLOW = (255, 214, 10)
WHITE = (255, 255, 255)
DIM = (170, 170, 170)
DARK = (17, 17, 17)
GRAY = (85, 85, 85)
LIGHT_GRAY = (153, 153, 153)
WARM = (107, 101, 96)
FADE = (226, 219, 202)
HAIR = (216, 210, 196)

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
F_INSTALL = font(f"{DEJAVU}/DejaVuSansMono-Bold.ttf", 30)
F_FOOT = font(f"{FONTS}/Poppins-Bold.ttf", 30)
F_LOCK = font(f"{FONTS}/Poppins-Bold.ttf", 38)
F_FADE = font(f"{FONTS}/Poppins-ExtraBold.ttf", 270)
F_FOOTM = font(f"{DEJAVU}/DejaVuSansMono.ttf", 26)

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

# ---- header: tilted SPILL box left, mascot lockup right ----
SPILL_F = font(f"{FONTS}/Poppins-ExtraBold.ttf", 72)
box_layer = Image.new("RGBA", (360, 170), (0, 0, 0, 0))
bl = ImageDraw.Draw(box_layer)
bl.rectangle([8, 8, 352, 162], outline=(17, 17, 17), width=6)
bl.text((34, 38), "SPILL", font=SPILL_F, fill=(17, 17, 17))
box_layer = box_layer.rotate(-3, expand=True, resample=Image.BICUBIC)
img.paste(box_layer, (70, 62), box_layer)
d.text((90, 268), "REPO 02 DARI 05 // CLAUDE", font=font(f"{DEJAVU}/DejaVuSansMono.ttf", 30), fill=WARM)
# mascot lockup (black keyed out, yellow P on cream)
mas = Image.open("/home/hatch/workspace/peka-logo/mascot-p.png").convert("RGB")
lum = mas.convert("L")
bbox = lum.point(lambda p: 255 if p > 60 else 0).getbbox()
mas = mas.crop(bbox)
mas = mas.resize((74, int(74 * mas.height / mas.width)))
alpha = mas.convert("L").point(lambda p: 255 if p > 60 else 0)
lock_txt = "peka.ai.id"
lock_w = d.textlength(lock_txt, font=F_LOCK)
lx = W - 90 - 74 - 16 - int(lock_w)
img.paste(mas, (lx, 80), alpha)
d.text((lx + 90, 98), lock_txt, font=F_LOCK, fill=DARK)

# ---- window mockup ----
WX, WY, WW = 90, 340, 1260
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
y = TITLE_H + BODY_PAD
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
y += 48 + 28 + 40
langs = [(("Go", (0, 173, 216)), 6987576), (("JavaScript", (241, 224, 90)), 3822208),
         (("TypeScript", (49, 120, 198)), 2067764), (("Python", (53, 114, 165)), 1437196)]
total = 14400000
bw_total = WW - 2 * BODY_PAD
# language bar (rounded ends)
bar_img = Image.new("RGB", (bw_total, 14), (255, 255, 255))
bd = ImageDraw.Draw(bar_img)
bx = 0
for (_, col), val in langs:
    seg = int(bw_total * val / total)
    bd.rectangle([bx, 0, bx + seg - 1, 13], fill=col)
    bx += seg
bar_img.putalpha(rounded_mask((bw_total, 14), 7))
win.paste(bar_img, (BODY_PAD, y), bar_img)
img.paste(win, (WX, WY), rounded_mask((WW, WH), 30))
d.rounded_rectangle([WX, WY, WX + WW - 1, WY + WH - 1], radius=30, outline=(190, 185, 172), width=2)

# ---- text below window ----
ty = WY + WH + 80
TX = 90
TW = W - 2 * TX
d.text((TX, ty), "github.com/JuliusBrussee/caveman", font=F_URL, fill=DARK)
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
    i = 0
    while i < len(line):
        w, hl = line[i]
        if hl:
            # one continuous box over the whole highlighted run
            j, run_w = i, 0
            while j < len(line) and line[j][1]:
                run_w += d.textlength(line[j][0] + " ", font=F_BODY)
                j += 1
            run_w -= d.textlength(" ", font=F_BODY)
            d.rectangle([x - 4, ty - 2, x + run_w + 4, ty + 46], fill=YELLOW)
            while i < j:
                d.text((x, ty), line[i][0], font=F_BODY, fill=DARK)
                x += d.textlength(line[i][0] + " ", font=F_BODY)
                i += 1
        else:
            d.text((x, ty), w, font=F_BODY, fill=DARK)
            x += d.textlength(w + " ", font=F_BODY)
            i += 1
    ty += 58
ty += 18
caveat = "tapi gaya jawabannya singkat ala caveman, kurang cocok buat dokumen formal."
for line in wrap_text(d, caveat, F_CAVEAT, TW):
    d.text((TX, ty), line, font=F_CAVEAT, fill=WARM)
    ty += 46
ty += 44
# ---- terminal console panel ----
PANEL_H = 150
PANEL_W = 940
panel = Image.new("RGB", (PANEL_W, PANEL_H), (20, 20, 26))
pd = ImageDraw.Draw(panel)
for i, c in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
    pd.ellipse([28 + i * 32, 22, 28 + i * 32 + 18, 40], fill=c)
pd.text((140, 18), "terminal", font=font(f"{DEJAVU}/DejaVuSansMono.ttf", 24), fill=(130, 130, 130))
cmd = "npx skills add JuliusBrussee/caveman -g"
prompt = "$ "
px = 32
py = 76
pd.text((px, py), prompt, font=F_INSTALL, fill=YELLOW)
px += pd.textlength(prompt, font=F_INSTALL)
pd.text((px, py), cmd, font=F_INSTALL, fill=WHITE)
cx = px + pd.textlength(cmd, font=F_INSTALL) + 12
pd.rectangle([cx, py + 2, cx + 18, py + 36], fill=YELLOW)
img.paste(panel, (TX, ty), rounded_mask((PANEL_W, PANEL_H), 20))
d.rounded_rectangle([TX, ty, TX + PANEL_W - 1, ty + PANEL_H - 1], radius=20, outline=(70, 70, 80), width=2)

# ---- footer: faded repo number, hairline, community line, page ----
d.text((W - 90 - d.textlength("02", font=F_FADE), 1345), "02", font=F_FADE, fill=FADE)
d.line([(90, 1760), (W - 90, 1760)], fill=HAIR, width=2)
d.text((90, 1800), "GABUNG KE KOMUNITAS KAMI: URL.PEKA.AI.ID", font=F_FOOTM, fill=WARM)
pg = "03 / 08"
d.text((W - 90 - d.textlength(pg, font=F_FOOTM), 1800), pg, font=F_FOOTM, fill=WARM)

img.save("spill-window-demo3.png")
print("saved", img.size)
