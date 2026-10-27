#!/usr/bin/env python3
"""Prototype v4: SPILL repo slide, square 2048x2048, neat like yesterday's
SPILL #06 slides. Header/footer chrome identical to yesterday's design;
middle is the browser-window mockup + terminal panel. No crowded extras:
no separate URL line, no highlight paragraph, no caveat line.
Demo only (JuliusBrussee/caveman, data live from GitHub API 27 Oct 2026).
"""
from PIL import Image, ImageDraw, ImageFont, ImageOps

W, H = 2048, 2048
BG = (243, 243, 240)
YELLOW = (255, 214, 10)
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

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
MX = 154  # side margin, like yesterday's slides

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

# ---------- header (yesterday's chrome) ----------
SPILL_F = font(f"{FONTS}/Poppins-ExtraBold.ttf", 68)
box_layer = Image.new("RGBA", (360, 170), (0, 0, 0, 0))
bl = ImageDraw.Draw(box_layer)
bl.rectangle([6, 6, 354, 164], outline=DARK, width=6)
bl.text((36, 36), "SPILL", font=SPILL_F, fill=DARK)
box_layer = box_layer.rotate(-3, expand=True, resample=Image.BICUBIC)
img.paste(box_layer, (130, 110), box_layer)
d.text((MX, 320), "REPO 02 DARI 05 // CLAUDE",
       font=font(f"{DEJAVU}/DejaVuSansMono.ttf", 42), fill=WARM)
# mascot lockup, dark P variant for the cream background
mas = Image.open("mascot-p-dark.png").convert("RGBA")
bbox = mas.getchannel("A").getbbox()
mas = mas.crop(bbox)
mas = mas.resize((72, int(72 * mas.height / mas.width)))
F_LOCK = font(f"{FONTS}/Poppins-Bold.ttf", 36)
lock_txt = "peka.ai.id"
lock_w = d.textlength(lock_txt, font=F_LOCK)
lx = W - MX - 72 - 16 - int(lock_w)
img.paste(mas, (lx, 120), mas)
d.text((lx + 88, 120 + (mas.height - 36) // 2), lock_txt, font=F_LOCK, fill=DARK)

# ---------- window mockup ----------
WX, WY, WW = MX, 450, W - 2 * MX
TITLE_H = 120
BODY_PAD = 76
AVATAR = 280
win = Image.new("RGB", (WW, 900), (255, 255, 255))
wd = ImageDraw.Draw(win)
wd.rounded_rectangle([0, 0, WW - 1, TITLE_H + 40], radius=40, fill=(0, 0, 0))
wd.rectangle([0, TITLE_H, WW - 1, TITLE_H + 40], fill=(0, 0, 0))
for i, c in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
    wd.ellipse([48 + i * 60, 42, 48 + i * 60 + 36, 78], fill=c)
wd.text((240, 38), "JuliusBrussee/caveman",
        font=font(f"{DEJAVU}/DejaVuSansMono.ttf", 42), fill=(170, 170, 170))
# repo name, auto-shrunk to fit left of avatar
y = TITLE_H + BODY_PAD
name_w_max = WW - 2 * BODY_PAD - AVATAR - 56
size = 104
while size > 56:
    f_light = font(f"{FONTS}/Poppins-SemiBold.ttf", size)
    f_bold = font(f"{FONTS}/Poppins-ExtraBold.ttf", size)
    if wd.textlength("JuliusBrussee/", font=f_light) + wd.textlength("caveman", font=f_bold) <= name_w_max:
        break
    size -= 2
wd.text((BODY_PAD, y), "JuliusBrussee/", font=f_light, fill=(60, 60, 60))
w1 = wd.textlength("JuliusBrussee/", font=f_light)
wd.text((BODY_PAD + w1, y), "caveman", font=f_bold, fill=DARK)
av = Image.open("avatar.png").convert("RGB")
av = ImageOps.fit(av, (AVATAR, AVATAR))
av.putalpha(rounded_mask((AVATAR, AVATAR), 36))
win.paste(av, (WW - BODY_PAD - AVATAR, TITLE_H + BODY_PAD), av)
# description
F_DESC = font(f"{FONTS}/Poppins-SemiBold.ttf", 48)
desc = "Viral skill + proxy for coding agents that cuts 65% of tokens by talking like a caveman."
desc_lines = wrap_text(wd, desc, F_DESC, WW - 2 * BODY_PAD - AVATAR - 56)
y += 130 + 30
for line in desc_lines:
    wd.text((BODY_PAD, y), line, font=F_DESC, fill=GRAY)
    y += 68
# stats
y += 70
F_STAT_NUM = font(f"{FONTS}/Poppins-Bold.ttf", 56)
F_STAT_LBL = font(f"{FONTS}/Poppins-SemiBold.ttf", 36)
stats = [("115k", "Stars"), ("6.6k", "Forks"), ("112", "Issues")]
col_w = (WW - 2 * BODY_PAD) // 3
for i, (num, lbl) in enumerate(stats):
    x = BODY_PAD + i * col_w
    wd.text((x, y), num, font=F_STAT_NUM, fill=DARK)
    wd.text((x, y + 68), lbl, font=F_STAT_LBL, fill=LIGHT_GRAY)
y += 68 + 52 + 56
# language bar (rounded ends)
langs = [(("Go", (0, 173, 216)), 6987576), (("JavaScript", (241, 224, 90)), 3822208),
         (("TypeScript", (49, 120, 198)), 2067764), (("Python", (53, 114, 165)), 1437196)]
total = 14400000
bw_total = WW - 2 * BODY_PAD
bar_img = Image.new("RGB", (bw_total, 20), (255, 255, 255))
bd = ImageDraw.Draw(bar_img)
bx = 0
for (_, col), val in langs:
    seg = int(bw_total * val / total)
    bd.rectangle([bx, 0, bx + seg - 1, 19], fill=col)
    bx += seg
bar_img.putalpha(rounded_mask((bw_total, 20), 10))
win.paste(bar_img, (BODY_PAD, y), bar_img)
WH = y + 20 + BODY_PAD
win = win.crop((0, 0, WW, WH))
img.paste(win, (WX, WY), rounded_mask((WW, WH), 40))
d.rounded_rectangle([WX, WY, WX + WW - 1, WY + WH - 1], radius=40,
                    outline=(190, 185, 172), width=2)

# ---------- terminal panel ----------
ty = WY + WH + 60
PANEL_H = 180
panel = Image.new("RGB", (WW, PANEL_H), (20, 20, 26))
pd = ImageDraw.Draw(panel)
for i, c in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
    pd.ellipse([40 + i * 44, 30, 40 + i * 44 + 24, 54], fill=c)
pd.text((196, 26), "terminal", font=font(f"{DEJAVU}/DejaVuSansMono.ttf", 32), fill=(130, 130, 130))
F_TERM = font(f"{DEJAVU}/DejaVuSansMono-Bold.ttf", 44)
cmd = "npx skills add JuliusBrussee/caveman -g"
px, py = 44, 104
pd.text((px, py), "$ ", font=F_TERM, fill=YELLOW)
px += pd.textlength("$ ", font=F_TERM)
pd.text((px, py), cmd, font=F_TERM, fill=(255, 255, 255))
cx = px + pd.textlength(cmd, font=F_TERM) + 16
pd.rectangle([cx, py + 2, cx + 24, py + 50], fill=YELLOW)
img.paste(panel, (WX, ty), rounded_mask((WW, PANEL_H), 28))
d.rounded_rectangle([WX, ty, WX + WW - 1, ty + PANEL_H - 1], radius=28,
                    outline=(70, 70, 80), width=2)

# ---------- footer zone (yesterday's blocks) ----------
fy = ty + PANEL_H + 60
d.line([(MX, fy), (W - MX, fy)], fill=HAIR, width=2)
fy += 40
# faded repo number behind the cocok block
F_FADE = font(f"{FONTS}/Poppins-ExtraBold.ttf", 300)
d.text((W - MX - d.textlength("02", font=F_FADE), H - 348), "02", font=F_FADE, fill=FADE)
d.text((MX, fy), "COCOK BUAT:", font=font(f"{FONTS}/Poppins-Bold.ttf", 54), fill=DARK)
fy += 84
F_COCOK = font(f"{FONTS}/Poppins-SemiBold.ttf", 52)
cocok = "Yang tokennya sering jebol di sesi panjang dan mau agent tetap tajam dengan biaya lebih kecil."
for line in wrap_text(d, cocok, F_COCOK, W - 2 * MX):
    d.text((MX, fy), line, font=F_COCOK, fill=(51, 51, 51))
    fy += 74
fy += 60
F_FOOTM = font(f"{DEJAVU}/DejaVuSansMono.ttf", 36)
d.text((MX, fy), "GABUNG KE KOMUNITAS KAMI: URL.PEKA.AI.ID", font=F_FOOTM, fill=WARM)
pg = "03 / 08"
d.text((W - MX - d.textlength(pg, font=F_FOOTM), fy), pg, font=F_FOOTM, fill=WARM)

img.save("spill-window-demo4.png")
print("saved", img.size, "footer_y", fy)
