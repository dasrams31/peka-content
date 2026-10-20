#!/usr/bin/env python3
"""Peka Homeless Media - Designer: news carousel PNGs (2048x2048, 2K).

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

S = 2048 / 1080
W = H = 2048
BG = "#111111"; YEL = "#ffd60a"; WHT = "#ffffff"; BLK = "#111111"; GRY = "#9a9a9a"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FM = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

LAYOUTS = ["cinematic", "split", "frame", "type"]
DETAIL_STYLES = ["dim", "cards"]


def X(v):
    return int(round(v * S))


def f(sz, bold=True):
    return ImageFont.truetype(FB if bold else FR, X(sz))


def mono(sz):
    return ImageFont.truetype(FM, X(sz))


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


def lockup(img, d, cy=LOCKUP_CY, mh=LOCKUP_MH):
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
    img.paste(cr, (int(mx), int(my)), mr)
    d.text((tx, ty), label, font=tf, fill=YEL)


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


def footer(d, i, n, left="PEKA.AI.ID"):
    d.text((X(70), X(1015)), left, font=f(24, False), fill=GRY)
    pg = f"{i}/{n}"
    d.text((X(1010) - d.textlength(pg, font=f(24, False)), X(1015)), pg, font=f(24, False), fill=GRY)


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
    layout = pick(args.layout, LAYOUTS)
    img = {"cinematic": cover_cinematic, "split": cover_split,
           "frame": cover_frame, "type": cover_type}[layout](args, n)
    print(f"[designer] cover layout: {layout}")
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


def detail(args, points, idx, n):
    style = pick(args.detail_style, DETAIL_STYLES)
    img = {"dim": detail_dim, "cards": detail_cards}[style](args, points, idx, n)
    if idx == 2:
        print(f"[designer] detail style: {style}")
    return img


def cta(args, n):
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
    ap.add_argument("--visual", default="")
    ap.add_argument("--layout", default="auto",
                    help="cinematic|split|frame|type|auto (auto rotates daily)")
    ap.add_argument("--detail-style", default="auto",
                    help="dim|cards|auto (auto rotates daily)")
    ap.add_argument("--badge-style", default="pill",
                    help="pill|sharp|brutal|ghost")
    args = ap.parse_args()
    global BADGE_STYLE
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
