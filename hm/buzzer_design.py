#!/usr/bin/env python3
"""Peka EDISI KHUSUS: Buzzer AI agent di Threads (one-off special, 2026-10-21).

8 slides, 2048x2048. User-supplied screenshots are embedded whole
(contain-fit, never cropped) as evidence. Peka black/yellow + red alert accent.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import designer as D
from PIL import Image, ImageDraw

X, f, mono, wrap = D.X, D.f, D.mono, D.wrap
W = H = D.W
YEL, WHT, GRY, BG = D.YEL, D.WHT, D.GRY, D.BG
RED = "#e5484d"
D.BADGE_STYLE = "ghost"

MEDIA = "/home/hatch/workspace/user/media_library/image"
SS_CREDIT = f"{MEDIA}/0c/0c0a7538bfa238a3efd058d86b429a69770ff1c182bb8e830cd6b32a9ca61c37.jpg"
SS_INJECT = f"{MEDIA}/17/1778b477ba3c1188493cfd222df13fdde8aac8b8941cd01b077c6cb590c8fe8f.jpg"
SS_HOWTO = f"{MEDIA}/2c/2c21d73fa65f9878e0e80941e79b3f13eadaf4c15e65ca1a84656499a20d5fd5.jpg"
SS_VIRAL = f"{MEDIA}/6c/6cdf5aa8d130e577313a2d1843d5e29a9cfc6240b0274c7fcc834648c05e8aa1.jpg"
SS_ACCUSE = f"{MEDIA}/62/62783486deccca23f4e374eb7afda19b4bb44b2dc46a61f80b560ed4fed7fd0c.jpg"
SS_METAAI = f"{MEDIA}/b4/b482739e72f5d8675bd93b53b494495670e022a833446b0ddcb1abb879c36520.jpg"
SS_IRONY = f"{MEDIA}/a6/a6273d83208857237de5950c697627eb144009c840f175a1e1d26ffd395a64d.jpg"

OUT = "/home/hatch/workspace/peka-content/edisi-khusus/buzzer-ai"
N = 5


def head(img, badge_label="FENOMENA AI"):
    d = ImageDraw.Draw(img)
    D.texture(d)
    D.lockup(img, d)
    return ImageDraw.Draw(img)


def red_chip(d, x, y, label):
    font = f(30)
    tw = d.textlength(label, font=font)
    d.rectangle([X(x), X(y), X(x) + tw + X(44), X(y) + X(58)], fill=RED)
    d.text((X(x) + X(22), X(y) + X(11)), label, font=font, fill=WHT)
    return tw + X(44)


def bracket_frame(d, box):
    x0, y0, x1, y1 = box
    d.rectangle([x0, y0, x1, y1], outline="#2e2e2e", width=X(3))
    bl, bw_ = X(36), X(7)
    for cx, cy, dx, dy in [(x0, y0, 1, 1), (x1, y0, -1, 1),
                           (x0, y1, 1, -1), (x1, y1, -1, -1)]:
        d.line([cx, cy, cx + dx * bl, cy], fill=RED, width=bw_)
        d.line([cx, cy, cx, cy + dy * bl], fill=RED, width=bw_)


def social_row(d, pg, y_units=1004):
    """Centered bottom row: IG / FB / Threads marks + website + page no."""
    col = "#d9d9d9"
    s = X(38)
    gap = X(24)
    fb_font, th_font, web_font = f(46), f(40, False), f(28, False)
    fb_w = d.textlength("f", font=fb_font)
    th_w = d.textlength("@", font=th_font)
    web_w = d.textlength("peka.ai.id", font=web_font)
    total = s + gap + fb_w + gap + th_w + gap + web_w
    x = (W - total) / 2
    y = X(y_units)
    d.rounded_rectangle([x, y, x + s, y + s], radius=X(10), outline=col,
                        width=X(3))
    d.ellipse([x + X(11), y + X(11), x + s - X(11), y + s - X(11)],
              outline=col, width=X(3))
    d.ellipse([x + s - X(12), y + X(8), x + s - X(8), y + X(12)], fill=col)
    x += s + gap
    d.text((x, y - X(7)), "f", font=fb_font, fill=col)
    x += fb_w + gap
    d.text((x, y - X(4)), "@", font=th_font, fill=col)
    x += th_w + gap
    d.text((x, y + X(5)), "peka.ai.id", font=web_font, fill=col)
    d.text((X(1010) - d.textlength(pg, font=f(24, False)), y + X(11)), pg,
           font=f(24, False), fill=GRY)


def cover():
    img = Image.new("RGB", (W, H), BG)
    d = head(img)
    inner = D.browser_window(img, d, (X(70), X(200), X(1010), X(574)),
                              "THREADS")
    vis = D.load_visual(SS_CREDIT)
    if vis:
        d = D.contain_fit(img, vis, inner)
    y = X(622)
    for sz in (74, 68, 62, 56):
        lines = wrap(d, "Buzzer Ini Bukan Manusia. Dia AI Agent.", f(sz), W - X(140))
        if len(lines) <= 2:
            break
    for ln in lines:
        d.text((X(70), y), ln, font=f(sz), fill=WHT)
        y += X(int(sz * 1.2))
    y += X(14)
    sub = ("Akun ibu laundry pendukung pemerintah ini lagi rame banget. "
           "Yang ngepost ternyata bukan manusia, tapi AI agent.")
    for ln in wrap(d, sub, f(29, False), W - X(140))[:2]:
        d.text((X(70), y), ln, font=f(29, False), fill="#cfcfcf")
        y += X(40)
    D.swipe_button(d, 918)
    D.footer(d, 1, N)
    return img


def evidence(ss_path, num, title):
    """Evidence slide: title + big screenshot + social row footer.
    No bottom caption (user: the caption band overlapped and got cut)."""
    img = Image.new("RGB", (W, H), BG)
    d = head(img)
    for sz in (38, 34, 31, 28):
        if d.textlength(title, font=f(sz)) <= W - X(140):
            break
    d.text((X(70), X(176)), title, font=f(sz), fill=WHT)
    box = (X(150), X(252), X(930), X(956))
    vis = D.load_visual(ss_path)
    if vis:
        d = D.contain_fit(img, vis, box, backdrop="#ffffff")
    bracket_frame(d, box)
    social_row(d, f"{num + 1}/{N}")
    return img


def cards_slide(idx, kicker, title, cards, check=False):
    img = Image.new("RGB", (W, H), BG)
    d = head(img)
    d.text((X(70), X(156)), kicker, font=mono(28), fill=RED)
    for sz in (54, 48, 44):
        if d.textlength(title, font=f(sz)) <= W - X(140):
            break
    d.text((X(70), X(202)), title, font=f(sz), fill=WHT)
    y = X(292)
    for head_t, body_t in cards:
        lines = wrap(d, body_t, f(27, False), W - X(300))
        card_h = X(24) + X(42) + len(lines) * X(35) + X(20)
        d.rounded_rectangle([X(70), y, X(1010), y + card_h], radius=X(20),
                            fill="#181818", outline="#262626", width=X(2))
        ty = y + X(24)
        if check:
            d.rectangle([X(106), ty + X(2), X(144), ty + X(40)], outline=YEL,
                        width=X(5))
            d.line([X(114), ty + X(21), X(123), ty + X(31)], fill=YEL, width=X(6))
            d.line([X(123), ty + X(31), X(137), ty + X(10)], fill=YEL, width=X(6))
        d.text((X(172), ty), head_t, font=f(33), fill=YEL)
        ty += X(44)
        for ln in lines:
            d.text((X(172), ty), ln, font=f(27, False), fill=WHT)
            ty += X(35)
        y += card_h + X(18)
    D.footer(d, idx, N)
    return img


def raw_slide(ss_path, idx):
    """Screenshot slide with the Peka design frame (header, red bracket
    frame, page number) but NO caption text (user request)."""
    img = Image.new("RGB", (W, H), BG)
    d = head(img)
    box = (X(150), X(196), X(930), X(962))
    vis = D.load_visual(ss_path)
    if vis:
        d = D.contain_fit(img, vis, box, backdrop="#ffffff")
    bracket_frame(d, box)
    D.footer(d, idx, N)
    return img


def closing():
    """Pure follow-invitation closing (user: previous closing did not
    connect; replace with a follow CTA for the latest AI info)."""
    img = Image.new("RGB", (W, H), BG)
    d = head(img)
    y = X(330)
    d.text((X(70), y), "Follow Peka AI", font=f(96), fill=YEL)
    y += X(118)
    d.text((X(70), y), "untuk informasi", font=f(80), fill=WHT)
    y += X(98)
    d.text((X(70), y), "AI terbaru.", font=f(80), fill=WHT)
    social_row(d, f"{N}/{N}")
    return img


def main():
    os.makedirs(OUT, exist_ok=True)
    slides = [
        cover(),
        evidence(SS_CREDIT, 1, "PESAN ERROR API BOCOR JADI POSTINGAN"),
        evidence(SS_INJECT, 2, "DIPANCING PROMPT JEBAKAN, DIA NGAKU"),
        evidence(SS_HOWTO, 3, "CARA BIKINNYA DIBOCORKAN SENDIRI"),
        closing(),
    ]
    for i, s in enumerate(slides, start=1):
        s.save(f"{OUT}/buzzer-{i:02d}.png")
    print(f"[buzzer] {len(slides)} slides -> {OUT}")


if __name__ == "__main__":
    main()
