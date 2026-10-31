#!/usr/bin/env python3
"""Peka Homeless Media - Designer: news carousel PNGs (4096x4096, 4K).

Usage:
    python3 designer.py --out <dir> --badge "AI NEWS" \\
        --headline "Headline utama berita" \\
        --points "Poin 1|Poin 2|Poin 3|Poin 4" \\
        --source "TechCrunch" [--sub "sub-headline"] [--url "https://..."]
        [--visual /path/to/hero.webp] [--layout auto] [--detail-style auto]

Layouts (cover): cinematic | split | frame | type. "auto" rotates daily.
Detail styles: dim | cards. "auto" rotates daily.

Peka header standard on every slide: badge kategori kuning top-left,
lockup maskot P + peka.ai.id top-right.
"""
import argparse
import datetime
import os

from PIL import Image, ImageDraw, ImageFont

S = 4096 / 1080
W = H = 4096
BG = "#111111"; YEL = "#ffd60a"; WHT = "#ffffff"; BLK = "#111111"; GRY = "#9a9a9a"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FM = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FSB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FSR = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"

LAYOUTS = ["cinematic", "split", "frame", "type"]
DETAIL_STYLES = ["dim", "cards"]
THEMES = ["frame", "koran", "majalah", "terminal"]
ALL_THEMES = THEMES + ["layar"]  # layar: explicit only, never in auto rotation
THEME = None  # set from --theme in main(); None = legacy layout behavior


def X(v):
    return int(round(v * S))


def f(sz, bold=True):
    return ImageFont.truetype(FB if bold else FR, X(sz))


def mono(sz):
    return ImageFont.truetype(FM, X(sz))


def fs(sz):
    return ImageFont.truetype(FSB, X(sz))


def fsr(sz):
    return ImageFont.truetype(FSR, X(sz))


def pick(name, options):
    """Explicit choice, or daily rotation when 'auto'/empty."""
    if name in options:
        return name
    return options[datetime.date.today().timetuple().tm_yday % len(options)]


# P creature with chroma-key (mascot-p.png is opaque RGB, black bg baked in)
_m = Image.open("/home/hatch/workspace/peka-logo/mascot-p.png").convert("RGB")
_mmask = Image.new("L", _m.size, 0)
_mp = _m.load(); _mk = _mmask.load()
for yy in range(_m.size[1]):
    for xx in range(_m.size[0]):
        r, g, b = _mp[xx, yy]
        if r > 30 or g > 30 or b > 30:
            _mk[xx, yy] = 255
_creature = _m.crop(_mmask.getbbox())
_cmask = _mmask.crop(_mmask.getbbox())


# Peka header lockup spec (locked 2026-10-20, user: "konsisten untuk kedepannya"):
# - Row: top-right, vertical center cy=95 (1080-space), aligned with badge center.
# - Right edge of text at x=1010. Mascot height mh=46, gap mascot-text = 12.
# - Text: 34px bold, yellow. Both mascot bbox and text em-box vertically
#   centered on cy via font metrics (no magic offsets).
# - Optical nudge: mascot shifted up 3% of mh (antenna makes bbox top-heavy).
LOCKUP_CY = 95
LOCKUP_MH = 46
LOCKUP_GAP = 12
LOCKUP_TEXT_X = 1010
LOCKUP_FONT = 34
LOCKUP_NUDGE = 0.03


def lockup(img, d, cy=LOCKUP_CY, mh=LOCKUP_MH, color=YEL, chip=False):
    cy_px, mh_px = X(cy), X(mh)
    cr = _creature.resize((int(_creature.width * mh_px / _creature.height), mh_px), Image.LANCZOS)
    mr = _cmask.resize(cr.size, Image.LANCZOS)
    tf = f(LOCKUP_FONT)
    label = "peka.ai.id"
    ascent, descent = tf.getmetrics()
    tx = X(LOCKUP_TEXT_X) - d.textlength(label, font=tf)
    ty = cy_px - (ascent + descent) // 2
    gap = X(LOCKUP_GAP)
    mx = tx - gap - cr.width
    my = cy_px - mh_px // 2 - int(mh_px * LOCKUP_NUDGE)
    if chip:
        pad = X(10)
        d.rounded_rectangle([mx - pad, my - pad, mx + cr.width + pad, my + mh_px + pad],
                            radius=X(16), fill=BLK)
    img.paste(cr, (int(mx), int(my)), mr)
    d.text((tx, ty), label, font=tf, fill=color)


BADGE_STYLE = "pill"  # pill | sharp | brutal | ghost (set from --badge-style)


def badge(d, label, style=None):
    style = style or BADGE_STYLE
    font = f(36)
    tw = d.textlength(label, font=font)
    x0, y0, h, pad_x = X(70), X(60), X(70), X(30)
    ty = y0 + X(14)
    if style == "pill":
        w = tw + X(60)
        d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=X(35), fill=YEL)
        d.text((x0 + X(30), ty), label, font=font, fill=BLK)
    elif style == "sharp":
        w = tw + pad_x * 2
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=YEL)
        d.text((x0 + pad_x, ty), label, font=font, fill=BLK)
    elif style == "brutal":
        w = tw + pad_x * 2
        off = X(8)
        d.rectangle([x0 + off, y0 + off, x0 + w + off, y0 + h + off], fill="#000000")
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=YEL)
        d.text((x0 + pad_x, ty), label, font=font, fill=BLK)
    elif style == "ghost":
        w = tw + pad_x * 2
        d.rectangle([x0, y0, x0 + w, y0 + h], outline=YEL, width=X(4))
        d.text((x0 + pad_x, ty), label, font=font, fill=YEL)
    else:
        w = tw + X(60)
        d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=X(35), fill=YEL)
        d.text((x0 + X(30), ty), label, font=font, fill=BLK)


def texture(d):
    for i in range(0, X(420), X(52)):
        d.line([(W - i, 0), (W, i)], fill="#181818", width=X(16))


def footer(d, i, n):
    y = X(1015)
    d.text((X(70), y), "GABUNG KE KOMUNITAS KAMI: URL.PEKA.AI.ID", font=f(24, False), fill=GRY)
    pg = f"{i}/{n}"
    d.text((X(1010) - d.textlength(pg, font=f(24, False)), y), pg, font=f(24, False), fill=GRY)


def wrap(d, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def wrap_url(d, url, font, max_w):
    """Wrap a URL across lines, breaking after slashes or dashes."""
    lines, cur = [], ""
    for ch in url:
        if ch in "/-" and cur and d.textlength(cur + ch, font=font) > max_w:
            lines.append(cur + ch)  # keep the break char at end of line
            cur = ""
            continue
        cur += ch
        if d.textlength(cur, font=font) > max_w:  # last resort: break at last - or /
            cut = max(cur.rfind("/"), cur.rfind("-"))
            if cut > len(cur) * 0.4:
                lines.append(cur[:cut + 1])
                cur = cur[cut + 1:]
            else:
                lines.append(cur)
                cur = ""
    if cur:
        lines.append(cur)
    return lines


def load_visual(path):
    if path and os.path.exists(path):
        return Image.open(path).convert("RGB")
    return None


def cover_crop(vis, tw, th):
    """Resize-crop an image to exactly (tw, th)."""
    scale = max(tw / vis.width, th / vis.height)
    nw, nh = int(vis.width * scale + 0.5), int(vis.height * scale + 0.5)
    vis = vis.resize((nw, nh), Image.LANCZOS)
    left, top = (nw - tw) // 2, (nh - th) // 2
    return vis.crop((left, top, left + tw, top + th))


def rounded_paste(img, vis_img, box, radius):
    x0, y0, x1, y1 = box
    fw, fh = x1 - x0, y1 - y0
    crop = cover_crop(vis_img, fw, fh)
    mask = Image.new("L", (fw, fh), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, fw, fh], radius=radius, fill=255)
    img.paste(crop, (x0, y0), mask)


def swipe_button(d, y_top):
    """Sharp-corner yellow button 'GESER ->' at bottom of cover (y_top in 1080-space)."""
    yt = X(y_top)
    label, arrow = "GESER", "\u2192"
    font = f(32)
    tw = d.textlength(label, font=font)
    aw = d.textlength(arrow, font=font)
    pad, gap = X(30), X(14)
    x0 = X(70)
    bw = tw + aw + gap + pad * 2
    bh = X(78)
    d.rectangle([x0, yt, x0 + bw, yt + bh], fill=YEL)
    ty = yt + X(17)
    d.text((x0 + pad, ty), label, font=font, fill=BLK)
    d.text((x0 + pad + tw + gap, ty), arrow, font=font, fill=BLK)


def text_block(d, args, y_start, y_end, head_sizes=(72, 64, 56, 48, 40, 34, 30, 28),
               max_hl=3, sub_sz=32, show_sub=True):
    """Headline + sub + source name + swipe button, fitted into y_start..y_end.

    No source URL on cover (too crowded); the source name stays for credibility.
    Never overflows and never cuts a sentence mid-way: the sub is shown whole
    or not at all, then the headline shrinks, then an extra headline line.
    """
    max_w = W - X(140)
    sub_full = wrap(d, args.sub, f(sub_sz, False), max_w) if (args.sub and show_sub) else []
    sub_lh = sub_sz + 10
    BTN_H = 78
    base_fixed = 36 + 40 + 28 + BTN_H  # gap + sumber + gap + button

    def render(sz, lines, lh, sub_lines):
        y = X(y_start)
        for ln in lines:
            d.text((X(70), y), ln, font=f(sz), fill=WHT)
            y += X(lh)
        if sub_lines:
            y += X(26)
            for ln in sub_lines:
                d.text((X(70), y), ln, font=f(sub_sz, False), fill="#cfcfcf")
                y += X(sub_lh)
        y += X(36)
        d.text((X(70), y), "Sumber: " + args.source, font=f(28, False), fill="#cfcfcf")
        y += X(40 + 28)
        swipe_button(d, y / S)

    for n_sub in (len(sub_full), 0):
        sub_lines = sub_full[:n_sub]
        fixed = base_fixed + (26 + len(sub_lines) * sub_lh if sub_lines else 0)
        budget = (y_end - y_start) - fixed
        for extra in (0, 1):
            for sz in head_sizes:
                lines = wrap(d, args.headline, f(sz), max_w)
                lh = int(sz * 1.22)
                if len(lines) <= max_hl + extra and len(lines) * lh <= budget:
                    render(sz, lines, lh, sub_lines)
                    return
    # ultimate fallback: smallest of everything (may touch y_end, never the footer)
    sz = head_sizes[-1]
    lines = wrap(d, args.headline, f(sz), max_w)[:max_hl + 1]
    render(sz, lines, int(sz * 1.22), [])


def base(badge_label):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    texture(d); badge(d, badge_label); lockup(img, d)
    return img, d


# ---- cover layouts ----

def cover_cinematic(args, n):
    """Full-bleed visual + bottom scrim + headline overlay."""
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    vis = load_visual(args.visual)
    if vis:
        side = min(vis.size)
        left, top = (vis.width - side) // 2, (vis.height - side) // 2
        vis = vis.crop((left, top, left + side, top + side)).resize((W, H), Image.LANCZOS)
        vis = Image.blend(vis, Image.new("RGB", (W, H), BG), 0.25)
        img.paste(vis, (0, 0))
        scrim = Image.new("L", (1, H), 0)
        sp = scrim.load()
        y0 = int(H * 0.42)
        for yy in range(H):
            sp[0, yy] = 0 if yy <= y0 else int(255 * (yy - y0) / (H - y0))
        scrim = scrim.resize((W, H))
        img.paste(Image.new("RGB", (W, H), (0, 0, 0)), (0, 0), scrim)
        d = ImageDraw.Draw(img)
    else:
        texture(d)
    badge(d, args.badge)
    lockup(img, d)
    d = ImageDraw.Draw(img)
    text_block(d, args, 560, 1000)
    footer(d, 1, n)
    return img


def cover_split(args, n):
    """Visual top half, solid black bottom half, yellow divider."""
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    vis = load_visual(args.visual)
    if vis:
        img.paste(cover_crop(vis, W, X(560)), (0, 0))
    else:
        texture(d)
    d.rectangle([0, X(560), W, X(568)], fill=YEL)
    badge(d, args.badge)
    lockup(img, d)
    d = ImageDraw.Draw(img)
    text_block(d, args, 608, 1000, show_sub=False)
    footer(d, 1, n)
    return img


def cover_frame(args, n):
    """Magazine style: visual in rounded inset frame, headline below."""
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    texture(d)
    badge(d, args.badge)
    lockup(img, d)
    d = ImageDraw.Draw(img)
    fx0, fy0, fx1, fy1 = X(70), X(180), X(1010), X(600)
    vis = load_visual(args.visual)
    if vis:
        rounded_paste(img, vis, (fx0, fy0, fx1, fy1), X(28))
        d = ImageDraw.Draw(img)
    else:
        d.rounded_rectangle([fx0, fy0, fx1, fy1], radius=X(28),
                            outline="#2a2a2a", width=X(3))
        d.text((X(110), X(360)), "PEKA AI NEWS", font=f(64), fill="#2a2a2a")
    d.rounded_rectangle([fx0, fy0, fx1, fy1], radius=X(28),
                        outline="#2a2a2a", width=X(3))
    text_block(d, args, 648, 1000, show_sub=False)
    footer(d, 1, n)
    return img


def cover_type(args, n):
    """Type-led poster: visual banner strip + huge headline."""
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    texture(d)
    badge(d, args.badge)
    lockup(img, d)
    d = ImageDraw.Draw(img)
    vis = load_visual(args.visual)
    if vis:
        rounded_paste(img, vis, (X(70), X(170), X(1010), X(460)), X(24))
        d = ImageDraw.Draw(img)
    # yellow kicker
    d.text((X(70), X(500)), "TOPIK HARI INI", font=f(30), fill=YEL)
    text_block(d, args, 548, 1000, head_sizes=(88, 80, 72, 64, 56, 48), max_hl=4)
    footer(d, 1, n)
    return img


def cover(args, n):
    if THEME:
        img = {"frame": cover_frame, "koran": cover_koran,
               "majalah": cover_majalah, "terminal": cover_terminal,
               "layar": cover_layar, "premium": cover_premium}[THEME](args, n)
        print(f"[designer] theme: {THEME}")
        return img
    layout = pick(args.layout, LAYOUTS)
    img = {"cinematic": cover_cinematic, "split": cover_split,
           "frame": cover_frame, "type": cover_type}[layout](args, n)
    print(f"[designer] cover layout: {layout}")
    return img


# ---- theme sets (2026-10-20: daily rotating news identities) ----
# frame   = the locked magazine frame (anchor, unchanged)
# koran   = broadsheet: cream paper, serif headline, ink rules
# majalah = glossy magazine: full-bleed visual, black panel, yellow kicker
# terminal= dark data room: dotted grid, bracketed visual window, ticker
CREAM = "#f6f1e6"
INK = "#161616"
INK_SUB = "#57534a"

HARI_ID = ["SENIN", "SELASA", "RABU", "KAMIS", "JUMAT", "SABTU", "MINGGU"]
BULAN_ID = ["JANUARI", "FEBRUARI", "MARET", "APRIL", "MEI", "JUNI", "JULI",
            "AGUSTUS", "SEPTEMBER", "OKTOBER", "NOVEMBER", "DESEMBER"]


def today_id():
    t = datetime.date.today()
    return f"{HARI_ID[t.weekday()]}, {t.day} {BULAN_ID[t.month - 1]} {t.year}"


def koran_header(img, d, badge_label):
    font = f(36)
    tw = d.textlength(badge_label, font=font)
    d.rectangle([X(70), X(60), X(70) + tw + X(60), X(130)], fill=INK)
    d.text((X(100), X(74)), badge_label, font=font, fill=CREAM)
    lockup(img, d, color=INK, chip=True)
    d = ImageDraw.Draw(img)
    d.rectangle([X(70), X(158), X(1010), X(164)], fill=INK)
    d.rectangle([X(70), X(170), X(1010), X(172)], fill=INK)
    return d


def koran_footer(d, i, n):
    d.text((X(70), X(1015)), "GABUNG KE KOMUNITAS KAMI: URL.PEKA.AI.ID", font=f(24, False), fill=INK_SUB)
    pg = f"{i}/{n}"
    d.text((X(1010) - d.textlength(pg, font=f(24, False)), X(1015)), pg,
           font=f(24, False), fill=INK_SUB)


def swipe_button_ink(d, y_top):
    yt = X(y_top)
    font = f(32)
    tw = d.textlength("GESER", font=font)
    aw = d.textlength("\u2192", font=font)
    pad, gap = X(30), X(14)
    d.rectangle([X(70), yt, X(70) + tw + aw + gap + pad * 2, yt + X(78)], fill=INK)
    d.text((X(100), yt + X(17)), "GESER", font=font, fill=YEL)
    d.text((X(100) + tw + gap, yt + X(17)), "\u2192", font=font, fill=YEL)


def cover_koran(args, n):
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    d = koran_header(img, d, args.badge)
    d.text((X(70), X(196)), f"EDISI {today_id()}", font=mono(26), fill=INK_SUB)
    src = f"SUMBER: {args.source.upper()}"
    d.text((X(1010) - d.textlength(src, font=mono(26)), X(196)), src,
           font=mono(26), fill=INK_SUB)
    vx0, vy0, vx1, vy1 = X(70), X(250), X(1010), X(560)
    vis = load_visual(args.visual)
    if vis:
        img.paste(cover_crop(vis, vx1 - vx0, vy1 - vy0), (vx0, vy0))
        d = ImageDraw.Draw(img)
    d.rectangle([vx0, vy0, vx1, vy1], outline=INK, width=X(4))
    d.rectangle([vx0 + X(10), vy0 + X(10), vx1 - X(10), vy1 - X(10)],
                outline=INK, width=X(1))
    cap = "ILUSTRASI AI"
    d.text((X(70), X(578)), cap, font=mono(24), fill=INK_SUB)

    # Headline + sub must fit 650..884 (rule at 892, swipe 918..996, footer 1015)
    max_w = W - X(140)
    sub_full = wrap(d, args.sub, fsr(32), max_w) if args.sub else []
    chosen = None
    for sz in (68, 60, 52, 46, 40):
        lines = wrap(d, args.headline, fs(sz), max_w)
        if len(lines) > 3:
            continue
        lh = int(sz * 1.24)
        for n_sub in (len(sub_full), 1, 0):
            if n_sub > len(sub_full):
                continue
            need = len(lines) * lh + ((20 + n_sub * 44) if n_sub else 0)
            if need <= 232:
                chosen = (sz, lines, lh, sub_full[:n_sub])
                break
        if chosen:
            break
    if not chosen:
        sz = 40
        chosen = (sz, wrap(d, args.headline, fs(sz), max_w)[:3], int(sz * 1.24), [])
    sz, lines, lh, sub_lines = chosen
    y = X(650)
    for ln in lines:
        d.text((X(70), y), ln, font=fs(sz), fill=INK)
        y += X(lh)
    if sub_lines:
        y += X(20)
        for ln in sub_lines:
            d.text((X(70), y), ln, font=fsr(32), fill=INK_SUB)
            y += X(44)
    d.rectangle([X(70), X(892), X(1010), X(895)], fill=INK)
    swipe_button_ink(d, 918)
    koran_footer(d, 1, n)
    return img


def detail_koran(args, points, idx, n):
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    d = koran_header(img, d, args.badge)
    d.text((X(70), X(196)), "DETAIL BERITA", font=mono(26), fill=INK_SUB)
    y = X(280)
    base_num = (idx - 2) * 2
    for j, p in enumerate(points):
        num = f"{base_num + j + 1:02d}"
        d.text((X(70), y), num, font=fs(54), fill=INK)
        for sz in (40, 36, 32):
            lines = wrap(d, p, fsr(sz), W - X(330))
            if len(lines) <= 5:
                break
        ty = y + X(6)
        for ln in lines:
            d.text((X(230), ty), ln, font=fsr(sz), fill=INK)
            ty += X(int(sz * 1.4))
        y = ty + X(34)
        if j < len(points) - 1:
            d.rectangle([X(70), y, X(1010), y + X(2)], fill="#d8d2c2")
            y += X(34)
    koran_footer(d, idx, n)
    return img


def cta_koran(args, n):
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    d = koran_header(img, d, args.badge)
    y = X(360)
    for ln in ["Jangan ketinggalan", "kabar AI terbaru."]:
        d.text((X(70), y), ln, font=fs(68), fill=INK)
        y += X(92)
    y += X(36)
    d.rectangle([X(70), y, X(1010), y + X(120)], fill=INK)
    d.text((X(110), y + X(30)), "Follow @peka.ai.id", font=f(54), fill=YEL)
    y += X(170)
    d.text((X(70), y), "Update tiap hari: info AI, bansos, dan tools terbaik.",
           font=fsr(32), fill=INK_SUB)
    koran_footer(d, n, n)
    return img


def cover_majalah(args, n):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    vis = load_visual(args.visual)
    if vis:
        img.paste(cover_crop(vis, W, H), (0, 0))
        img = Image.blend(img, Image.new("RGB", (W, H), BG), 0.10)
        d = ImageDraw.Draw(img)
    else:
        texture(d)
    badge(d, args.badge)
    lockup(img, d)
    d = ImageDraw.Draw(img)
    py0 = X(640)
    panel = Image.new("RGB", (W, H - py0), (10, 10, 10))
    img.paste(panel, (0, py0))
    d = ImageDraw.Draw(img)
    kick = f"{args.badge} - {args.source.upper()}"
    kf = mono(30)
    kw = d.textlength(kick, font=kf) + X(44)
    d.rectangle([X(70), py0 + X(36), X(70) + kw, py0 + X(36) + X(58)], fill=YEL)
    d.text((X(92), py0 + X(47)), kick, font=kf, fill=BLK)
    max_w = W - X(140)
    y = py0 + X(118)
    sub_lines = wrap(d, args.sub, f(30, False), max_w)[:1] if args.sub else []
    for sz in (66, 58, 50, 44, 38):
        lines = wrap(d, args.headline, f(sz), max_w)
        need = len(lines) * int(sz * 1.22) + (52 if sub_lines else 0)
        if len(lines) <= 3 and need <= 190:
            break
    for ln in lines:
        d.text((X(70), y), ln, font=f(sz), fill=WHT)
        y += X(int(sz * 1.22))
    if sub_lines:
        y += X(14)
        d.text((X(70), y), sub_lines[0], font=f(30, False), fill="#cfcfcf")
    swipe_button(d, 950)
    pg = f"1/{n}"
    d.text((X(1010) - d.textlength(pg, font=f(24, False)), X(1015)), pg,
           font=f(24, False), fill=GRY)
    return img


def cover_terminal(args, n):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    for gx in range(X(46), W, X(46)):
        for gy in range(X(46), H, X(46)):
            d.ellipse([gx, gy, gx + X(3), gy + X(3)], fill="#1e1e1e")
    badge(d, args.badge)
    lockup(img, d)
    d = ImageDraw.Draw(img)
    vx0, vy0, vx1, vy1 = X(70), X(180), X(1010), X(520)
    vis = load_visual(args.visual)
    if vis:
        img.paste(cover_crop(vis, vx1 - vx0, vy1 - vy0), (vx0, vy0))
        d = ImageDraw.Draw(img)
    d.rectangle([vx0, vy0, vx1, vy1], outline="#333333", width=X(2))
    bl, bw_ = X(34), X(6)
    for cx, cy, dx, dy in [(vx0, vy0, 1, 1), (vx1, vy0, -1, 1),
                           (vx0, vy1, 1, -1), (vx1, vy1, -1, -1)]:
        d.line([cx, cy, cx + dx * bl, cy], fill=YEL, width=bw_)
        d.line([cx, cy, cx, cy + dy * bl], fill=YEL, width=bw_)
    d.text((X(70), X(548)), "> HEADLINE", font=mono(30), fill=YEL)
    max_w = W - X(140)
    y = X(596)
    for sz in (52, 46, 40, 34):
        lines = wrap(d, args.headline, mono(sz), max_w)
        if len(lines) <= 4:
            break
    for ln in lines:
        d.text((X(70), y), ln, font=mono(sz), fill=WHT)
        y += X(int(sz * 1.3))
    if args.sub:
        y += X(16)
        for ln in wrap(d, args.sub, mono(28), max_w)[:2]:
            d.text((X(70), y), ln, font=mono(28), fill=GRY)
            y += X(40)
    y += X(24)
    d.text((X(70), y), f"// SUMBER: {args.source.upper()}", font=mono(28), fill=GRY)
    tick = f"PEKA NEWS +++ {args.source.upper()} +++ GESER BUAT DETAIL +++ "
    tick = tick * 3
    ty0 = X(972)
    d.rectangle([0, ty0, W, X(1080)], fill="#0a0a0a")
    d.line([0, ty0, W, ty0], fill=YEL, width=X(3))
    d.text((X(70), ty0 + X(26)), tick, font=mono(30), fill=YEL)
    pg = f"1/{n}"
    d.text((X(1010) - d.textlength(pg, font=f(24, False)), ty0 + X(66)), pg,
           font=f(24, False), fill=GRY)
    return img


# ---- premium theme (explicit only, never in auto rotation) ----
# Editorial, not generic dark-tech: warm paper, wide margins, serif headline,
# one thin gold rule, no gradient, no glow, no big colour block.
PAPER = "#f7f4ed"
INK2 = "#171713"
MUTED2 = "#6b675e"
GOLD = "#b9975b"


def premium_header(img, d):
    d.text((X(120), X(72)), "AI NEWS", font=mono(26), fill=INK2)
    lockup(img, d, color=INK2)
    d = ImageDraw.Draw(img)
    d.rectangle([X(120), X(132), X(960), X(134)], fill="#d8d2c2")
    d.rectangle([X(120), X(132), X(240), X(136)], fill=GOLD)
    return d


def premium_footer(d, i, n):
    d.text((X(120), X(1015)), "GABUNG KE KOMUNITAS KAMI: URL.PEKA.AI.ID",
           font=f(24, False), fill=MUTED2)
    pg = f"{i}/{n}"
    d.text((X(960) - d.textlength(pg, font=f(24, False)), X(1015)), pg,
           font=f(24, False), fill=MUTED2)


def cover_premium(args, n):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d = premium_header(img, d)
    d.text((X(120), X(162)), today_id(), font=mono(24), fill=MUTED2)
    src = f"SUMBER: {args.source.upper()}"
    d.text((X(960) - d.textlength(src, font=mono(24)), X(162)), src,
           font=mono(24), fill=MUTED2)
    vx0, vy0, vx1, vy1 = X(120), X(214), X(960), X(512)
    vis = load_visual(args.visual)
    if vis:
        img.paste(cover_crop(vis, vx1 - vx0, vy1 - vy0), (vx0, vy0))
        d = ImageDraw.Draw(img)
    d.rectangle([vx0, vy0, vx1, vy1], outline="#d8d2c2", width=X(2))
    d.text((X(120), X(530)), "ILUSTRASI AI", font=mono(22), fill=MUTED2)
    max_w = W - X(240)
    sub_full = wrap(d, args.sub, fsr(30), max_w) if args.sub else []
    chosen = None
    for sz in (62, 56, 50, 44):
        lines = wrap(d, args.headline, fs(sz), max_w)
        if len(lines) > 3:
            continue
        lh = int(sz * 1.28)
        for n_sub in (len(sub_full), 1, 0):
            if n_sub > len(sub_full):
                continue
            need = len(lines) * lh + ((18 + n_sub * 42) if n_sub else 0)
            if need <= 300:
                chosen = (sz, lines, lh, sub_full[:n_sub])
                break
        if chosen:
            break
    if not chosen:
        sz = 44
        chosen = (sz, wrap(d, args.headline, fs(sz), max_w)[:3], int(sz * 1.28), [])
    sz, lines, lh, sub_lines = chosen
    y = X(580)
    for ln in lines:
        d.text((X(120), y), ln, font=fs(sz), fill=INK2)
        y += X(lh)
    if sub_lines:
        y += X(18)
        for ln in sub_lines:
            d.text((X(120), y), ln, font=fsr(30), fill=MUTED2)
            y += X(42)
    d.rectangle([X(120), X(918), X(960), X(920)], fill="#d8d2c2")
    d.text((X(120), X(940)), "GESER", font=mono(28), fill=INK2)
    d.text((X(120) + d.textlength("GESER", font=mono(28)) + X(14), X(940)),
           "\u2192", font=mono(28), fill=GOLD)
    premium_footer(d, 1, n)
    return img


def detail_premium(args, points, idx, n):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d = premium_header(img, d)
    d.text((X(120), X(162)), "DETAIL BERITA", font=mono(24), fill=MUTED2)
    base_num = (idx - 2) * 2
    blocks = []
    for p in points:
        for sz in (36, 32, 30):
            lines = wrap(d, p, fsr(sz), W - X(380))
            if len(lines) <= 6:
                break
        blocks.append((sz, lines))
    total = sum(len(lines) * int(sz * 1.45) for sz, lines in blocks)
    total += (len(blocks) - 1) * (28 + 28 + 2)
    y = X(200) + max(0, (X(760) - total) // 2)
    for j, (sz, lines) in enumerate(blocks):
        num = f"{base_num + j + 1:02d}"
        d.text((X(120), y), num, font=fs(40), fill=GOLD)
        ty = y + X(4)
        for ln in lines:
            d.text((X(240), ty), ln, font=fsr(sz), fill=INK2)
            ty += X(int(sz * 1.45))
        y = ty + X(28)
        if j < len(blocks) - 1:
            d.rectangle([X(120), y, X(960), y + X(2)], fill="#e2ddd0")
            y += X(28)
    premium_footer(d, idx, n)
    return img


def cta_premium(args, n):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d = premium_header(img, d)
    y = X(340)
    for ln in ["Kabar AI terbaru,", "tanpa ribut."]:
        d.text((X(120), y), ln, font=fs(64), fill=INK2)
        y += X(88)
    y += X(28)
    d.rectangle([X(120), y, X(240), y + X(4)], fill=GOLD)
    y += X(36)
    d.text((X(120), y), "Follow @peka.ai.id", font=f(48), fill=INK2)
    y += X(84)
    d.text((X(120), y), "Satu topik AI setiap hari, plus prompt dan tools",
           font=fsr(30), fill=MUTED2)
    d.text((X(120), y + X(44)), "yang bisa langsung dipakai.",
           font=fsr(30), fill=MUTED2)
    # Blog shortlink printed on the last slide (Threads no-link rule,
    # 31 Okt 2026): the link lives here, not in a Threads reply.
    if getattr(args, "bloglink", ""):
        shown = args.bloglink.replace("https://", "").replace("http://", "")
        d.text((X(120), X(840)), "Link blog: " + shown, font=mono(30), fill=INK2)
    premium_footer(d, n, n)
    return img


# ---- detail styles ----

def detail_dim(args, points, idx, n):
    """Dimmed visual cover background + bullet text."""
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    vis = load_visual(args.visual)
    if vis:
        side = min(vis.size)
        left, top = (vis.width - side) // 2, (vis.height - side) // 2
        vis = vis.crop((left, top, left + side, top + side)).resize((W, H), Image.LANCZOS)
        vis = Image.blend(vis, Image.new("RGB", (W, H), BG), 0.72)
        img.paste(vis, (0, 0))
        d = ImageDraw.Draw(img)
    else:
        texture(d)
    badge(d, args.badge)
    lockup(img, d)
    d = ImageDraw.Draw(img)
    y = X(260)
    for p in points:
        d.ellipse([X(70), y + X(14), X(100), y + X(44)], fill=YEL)
        for sz in (44, 40, 36):
            lines = wrap(d, p, f(sz, False), W - X(240))
            if len(lines) <= 4:
                break
        for ln in lines:
            d.text((X(130), y), ln, font=f(sz, False), fill=WHT)
            y += X(int(sz * 1.35))
        y += X(50)
    footer(d, idx, n)
    return img


def detail_cards(args, points, idx, n):
    """Numbered cards on textured black."""
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    texture(d)
    badge(d, args.badge)
    lockup(img, d)
    d = ImageDraw.Draw(img)
    y = X(250)
    for i, p in enumerate(points):
        num = f"{i + 1:02d}"
        for sz in (44, 40, 36):
            lines = wrap(d, p, f(sz, False), W - X(360))
            if len(lines) <= 4:
                break
        lh = int(sz * 1.35)
        card_h = X(56) + len(lines) * X(lh) + X(40)
        d.rounded_rectangle([X(70), y, X(1010), y + card_h], radius=X(24),
                            fill="#181818", outline="#262626", width=X(2))
        ty = y + X(40)
        d.text((X(110), ty), num, font=f(52), fill=YEL)
        for ln in lines:
            d.text((X(270), ty), ln, font=f(sz, False), fill=WHT)
            ty += X(lh)
        y += card_h + X(36)
    footer(d, idx, n)
    return img


def contain_fit(img, vis, box, backdrop="#0b0b0b"):
    """Paste vis inside box (px coords) scaled to FIT entirely, never cropped."""
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    d = ImageDraw.Draw(img)
    d.rectangle([x0, y0, x1, y1], fill=backdrop)
    scale = min(bw / vis.width, bh / vis.height)
    nw, nh = max(1, int(vis.width * scale)), max(1, int(vis.height * scale))
    resized = vis.resize((nw, nh), Image.LANCZOS)
    img.paste(resized, (x0 + (bw - nw) // 2, y0 + (bh - nh) // 2))
    return ImageDraw.Draw(img)


def browser_window(img, d, box, label):
    """Browser chrome frame; returns the inner screenshot box (px coords)."""
    x0, y0, x1, y1 = box
    d.rounded_rectangle([x0, y0, x1, y1], radius=X(22), fill="#1b1b1d",
                        outline="#2e2e2e", width=X(2))
    bar_h = X(64)
    d.line([x0, y0 + bar_h, x1, y0 + bar_h], fill="#2e2e2e", width=X(2))
    for i, col in enumerate(["#3a3a3a", "#3a3a3a", YEL]):
        cx = x0 + X(34) + i * X(34)
        cy = y0 + bar_h // 2
        d.ellipse([cx - X(9), cy - X(9), cx + X(9), cy + X(9)], fill=col)
    if label:
        lf = mono(24)
        tw = d.textlength(label, font=lf)
        pw = tw + X(40)
        px0 = x0 + (x1 - x0 - pw) // 2
        d.rounded_rectangle([px0, y0 + X(13), px0 + pw, y0 + X(51)], radius=X(19),
                            fill="#26262a")
        d.text((px0 + X(20), y0 + X(19)), label, font=lf, fill="#cfcfcf")
    return (x0 + X(16), y0 + bar_h + X(14), x1 - X(16), y1 - X(16))


def cover_layar(args, n):
    """Screenshot theme: the source screenshot, whole and uncropped, in a
    browser window. Explicit only (--theme layar), never in auto rotation."""
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    texture(d)
    badge(d, args.badge)
    lockup(img, d)
    d = ImageDraw.Draw(img)
    inner = browser_window(img, d, (X(70), X(178), X(1010), X(648)),
                           args.source.upper())
    vis = load_visual(args.visual)
    if vis:
        d = contain_fit(img, vis, inner)
    else:
        d.text((X(120), X(400)), "TANGKAPAN LAYAR", font=f(44), fill="#2a2a2a")
    d.text((X(70), X(664)), f"TANGKAPAN LAYAR - {args.source.upper()}",
           font=mono(24), fill=GRY)
    text_block(d, args, 712, 1000)
    footer(d, 1, n)
    return img


def detail_layar(args, points, idx, n):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    texture(d)
    badge(d, args.badge)
    lockup(img, d)
    d = ImageDraw.Draw(img)
    inner = browser_window(img, d, (X(70), X(180), X(1010), X(516)),
                           args.source.upper())
    vis = load_visual(args.visual)
    if vis:
        d = contain_fit(img, vis, inner)
    y = X(580)
    for p in points:
        d.ellipse([X(70), y + X(14), X(100), y + X(44)], fill=YEL)
        for sz in (42, 38, 34):
            lines = wrap(d, p, f(sz, False), W - X(240))
            if len(lines) <= 4:
                break
        for ln in lines:
            d.text((X(130), y), ln, font=f(sz, False), fill=WHT)
            y += X(int(sz * 1.35))
        y += X(46)
    footer(d, idx, n)
    return img


def detail(args, points, idx, n):
    if THEME:
        if THEME == "frame":
            style = pick(args.detail_style, DETAIL_STYLES)
            img = {"dim": detail_dim, "cards": detail_cards}[style](args, points, idx, n)
        else:
            fn = {"koran": detail_koran, "majalah": detail_cards,
                  "terminal": detail_dim, "layar": detail_layar,
                  "premium": detail_premium}[THEME]
            img = fn(args, points, idx, n)
        if idx == 2:
            print(f"[designer] detail via theme: {THEME}")
        return img
    style = pick(args.detail_style, DETAIL_STYLES)
    img = {"dim": detail_dim, "cards": detail_cards}[style](args, points, idx, n)
    if idx == 2:
        print(f"[designer] detail style: {style}")
    return img


def cta(args, n):
    if THEME == "koran":
        return cta_koran(args, n)
    if THEME == "premium":
        return cta_premium(args, n)
    img, d = base(args.badge)
    y = X(380)
    for ln in ["Jangan ketinggalan", "kabar AI terbaru."]:
        d.text((X(70), y), ln, font=f(72), fill=WHT)
        y += X(95)
    y += X(40)
    d.text((X(70), y), "Follow @peka.ai.id", font=f(60), fill=YEL)
    y += X(110)
    d.text((X(70), y), "Update tiap hari: info AI,", font=f(36, False), fill=GRY)
    d.text((X(70), y + X(48)), "bansos, dan tools terbaik.", font=f(36, False), fill=GRY)
    # Blog shortlink printed on the last slide (Threads no-link rule,
    # 31 Okt 2026): the link lives here, not in a Threads reply.
    if getattr(args, "bloglink", ""):
        shown = args.bloglink.replace("https://", "").replace("http://", "")
        d.text((X(70), X(880)), "Link blog: " + shown, font=mono(28), fill=YEL)
    footer(d, n, n)
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--badge", default="AI NEWS")
    ap.add_argument("--headline", required=True)
    ap.add_argument("--sub", default="")
    ap.add_argument("--points", default="")
    ap.add_argument("--source", default="")
    ap.add_argument("--url", default="")
    ap.add_argument("--bloglink", default="",
                    help="shortlink blog edisi ini, dicetak di slide CTA "
                         "terakhir (aturan tanpa-link Threads 31 Okt 2026)")
    ap.add_argument("--visual", default="")
    ap.add_argument("--layout", default="auto",
                    help="cinematic|split|frame|type|auto (auto rotates daily)")
    ap.add_argument("--detail-style", default="auto",
                    help="dim|cards|auto (auto rotates daily)")
    ap.add_argument("--badge-style", default="pill",
                    help="pill|sharp|brutal|ghost")
    ap.add_argument("--theme", default=None,
                    help="frame|koran|majalah|terminal|premium|auto (set desain harian; "
                         "mengabaikan --layout/--detail-style). layar dan premium = "
                         "tema eksplisit, tidak ikut rotasi auto")
    args = ap.parse_args()
    global BADGE_STYLE, THEME
    if args.theme:
        THEME = args.theme if args.theme in ("layar", "premium") else pick(args.theme, THEMES)
        BADGE_STYLE = {"frame": "ghost", "koran": "sharp",
                       "majalah": "ghost", "terminal": "sharp",
                       "layar": "ghost", "premium": "sharp"}[THEME]
    else:
        BADGE_STYLE = args.badge_style

    points = [p.strip() for p in args.points.split("|") if p.strip()]
    chunks = [points[i:i + 2] for i in range(0, len(points), 2)] or [[]]
    n = 1 + len(chunks) + 1

    os.makedirs(args.out, exist_ok=True)
    cover(args, n).save(f"{args.out}/hm-01.png")
    for i, ch in enumerate(chunks, start=2):
        detail(args, ch, i, n).save(f"{args.out}/hm-{i:02d}.png")
    cta(args, n).save(f"{args.out}/hm-{n:02d}.png")
    print(f"[designer] {n} slides -> {args.out}/hm-01.png .. hm-{n:02d}.png")


if __name__ == "__main__":
    main()
