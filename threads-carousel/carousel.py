#!/usr/bin/env python3
"""Threads carousel template for reel-v2 (voiceover) content.

Turns a reel-v2 spec.json (hook + beat scenes + close) into a square
4096x4096 carousel for Threads, in the spec's own theme
(peka-yellow / dark-grid / navy-tech / rute-green).

Slides carry the punchy facts (stat, bars, short lines); the voiceover
narration stays in the caption, written by the posting cron.

Usage:
    python3 carousel.py <spec.json> <out_dir> [--theme THEME]

Output: threads-carousel-01.png .. threads-carousel-NN.png + manifest.json
"""
import json
import os
import re
import sys

from PIL import Image, ImageDraw, ImageFont, ImageOps

SIZE = 4096
MARGIN = 280
CW = SIZE - 2 * MARGIN  # content width

PEKA = "/home/hatch/workspace/peka-content"
ASSETS = os.path.join(PEKA, "spill/animated/assets")
REEL2 = os.path.join(PEKA, "reel-v2")
COMMUNITY = "GABUNG KE KOMUNITAS KAMI: S.PEKA.AI.ID/GABUNG"


def _font(name, size):
    for path in (os.path.join(ASSETS, name),
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def F_XB(size):
    return _font("Poppins-ExtraBold.ttf", size)


def F_B(size):
    return _font("Poppins-Bold.ttf", size)


def F_SB(size):
    return _font("Poppins-SemiBold.ttf", size)


def F_MONO(size):
    return ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", size)


def hexcol(s):
    s = s.lstrip("#")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def parse_rgba(s):
    m = re.match(r"rgba\((\d+),\s*(\d+),\s*(\d+),\s*([\d.]+)\)", s)
    if not m:
        return None
    r, g, b, a = m.groups()
    return (int(r), int(g), int(b), int(float(a) * 255))


def load_theme(name):
    with open(os.path.join(REEL2, "themes.json")) as fh:
        themes = json.load(fh)
    t = themes[name]
    return {
        "bg": hexcol(t["bg"]),
        "bg2": hexcol(t["bg2"]),
        "card": hexcol(t["card"]),
        "border": hexcol(t["card_border"]),
        "accent": hexcol(t["accent"]),
        "accent2": hexcol(t["accent2"]),
        "text": hexcol(t["text"]),
        "dim": hexcol(t["dim"]),
        "mono": hexcol(t["mono"]),
        "bar_track": hexcol(t["bar_track"]),
        "bar_other": hexcol(t["bar_other"]),
        "chip_bg": hexcol(t["chip_bg"]),
        "chip_text": hexcol(t["chip_text"]),
        "grid": parse_rgba(t.get("grid", "rgba(255,255,255,0.05)")),
    }


def strip_tags(s):
    return re.sub(r"</?b>", "", s or "")


def rich_words(text):
    """Split text into (word, bold) tokens, honoring <b>...</b>."""
    out = []
    for part in re.split(r"(<b>.*?</b>)", text or ""):
        if not part:
            continue
        if part.startswith("<b>"):
            inner = part[3:-4]
            for w in inner.split(" "):
                if w:
                    out.append((w, True))
        else:
            for w in part.split(" "):
                if w:
                    out.append((w, False))
    return out


def wrap_rich(text, font_b, font_r, max_w):
    """Wrap rich text into lines of (word, bold) tokens."""
    words = rich_words(text)
    lines, cur, cur_w = [], [], 0
    space_b = font_b.getlength(" ")
    space_r = font_r.getlength(" ")
    for w, bold in words:
        f = font_b if bold else font_r
        ww = f.getlength(w)
        sp = (space_b if (cur and cur[-1][1]) else space_r) if cur else 0
        if cur and cur_w + sp + ww > max_w:
            lines.append(cur)
            cur, cur_w = [(w, bold)], ww
        else:
            cur.append((w, bold))
            cur_w += sp + ww
    if cur:
        lines.append(cur)
    return lines


def draw_rich(draw, x, y, line, font_b, font_r, color, accent=None):
    cx = x
    for w, bold in line:
        f = font_b if bold else font_r
        c = accent if (bold and accent) else color
        draw.text((cx, y), w, font=f, fill=c)
        cx += f.getlength(w) + f.getlength(" ")
    return cx


def line_width(line, font_b, font_r):
    return sum((font_b if b else font_r).getlength(w) +
               (font_b if b else font_r).getlength(" ") for w, b in line)


class Slide:
    def __init__(self, theme, idx, total):
        self.t = theme
        self.idx = idx
        self.total = total
        self.img = Image.new("RGB", (SIZE, SIZE), theme["bg"])
        self.d = ImageDraw.Draw(self.img)
        self._grid()

    def _grid(self):
        g = self.t["grid"]
        if not g:
            return
        ov = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
        od = ImageDraw.Draw(ov)
        step = 512
        for x in range(step, SIZE, step):
            od.line([(x, 0), (x, SIZE)], fill=g, width=2)
        for y in range(step, SIZE, step):
            od.line([(0, y), (SIZE, y)], fill=g, width=2)
        self.img.paste(Image.alpha_composite(self.img.convert("RGBA"), ov))

    def chip(self, x, y, text, size=92, bg=None, fg=None, pad_x=44, pad_y=26):
        bg = bg or self.t["chip_bg"]
        fg = fg or self.t["chip_text"]
        f = F_B(size)
        tw = f.getlength(text)
        h = size + 2 * pad_y
        self.d.rounded_rectangle([x, y, x + tw + 2 * pad_x, y + h],
                                 radius=h // 2, fill=bg)
        self.d.text((x + pad_x, y + pad_y - 6), text, font=f, fill=fg)
        return x + tw + 2 * pad_x

    def header(self, kicker):
        self.chip(MARGIN, 280, kicker)
        f = F_MONO(88)
        label = f"{self.idx:02d} / {self.total:02d}"
        self.d.text((SIZE - MARGIN - f.getlength(label), 300), label,
                    font=f, fill=self.t["dim"])
        # progress hairline
        y = 470
        self.d.line([(MARGIN, y), (SIZE - MARGIN, y)],
                    fill=self.t["border"], width=6)
        w = int(CW * self.idx / self.total)
        self.d.line([(MARGIN, y), (MARGIN + w, y)],
                    fill=self.t["accent"], width=6)

    def footer(self):
        y = 3850
        self.d.line([(MARGIN, y), (SIZE - MARGIN, y)],
                    fill=self.t["border"], width=4)
        f = F_MONO(72)
        self.d.text((MARGIN, y + 44), COMMUNITY, font=f, fill=self.t["dim"])
        label = f"{self.idx:02d} / {self.total:02d}"
        self.d.text((SIZE - MARGIN - f.getlength(label), y + 44), label,
                    font=f, fill=self.t["accent"])

    def ghost(self, text, x=None, y=560):
        ov = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
        od = ImageDraw.Draw(ov)
        f = F_XB(880)
        tw = f.getlength(text)
        xx = SIZE - MARGIN - tw if x is None else x
        od.text((xx, y), text, font=f, fill=(255, 255, 255, 26))
        self.img.paste(Image.alpha_composite(self.img.convert("RGBA"), ov))

    def mascot(self, pose, side="right", width=500, bottom=500, flip=False):
        for cand in (f"piko-anime-{pose}-open.png",
                     f"piko-anime-{pose}-closed.png",
                     "piko-anime-open.png"):
            p = os.path.join(REEL2, "assets/character", cand)
            if os.path.exists(p):
                break
        else:
            return
        im = Image.open(p).convert("RGBA")
        h = int(width * im.height / im.width)
        im = im.resize((width, h), Image.LANCZOS)
        if flip:
            im = ImageOps.mirror(im)
        x = SIZE - MARGIN - width if side == "right" else MARGIN
        y = SIZE - bottom - h
        self.img.paste(im, (x, y), im)


def render_cover(spec, theme, idx, total):
    s = Slide(theme, idx, total)
    title = spec.get("title", "")
    series = title.split(":")[0].upper() if ":" in title else title.upper()
    s.header(series)
    hook = spec["scenes"][0]
    lines = hook.get("headline", [])
    f = F_XB(330)
    y = 1080
    for ln in lines:
        s.d.text((MARGIN, y), ln, font=f, fill=theme["text"])
        y += 380
    sub = strip_tags(hook.get("sub", ""))
    if sub:
        s.d.text((MARGIN, y + 60), sub, font=F_SB(128),
                 fill=theme["dim"])
    m = hook.get("mascot", {})
    s.mascot(hook.get("pose", "wave"), m.get("side", "right"),
             width=820, bottom=560, flip=m.get("flip", False))
    f2 = F_MONO(92)
    s.d.text((MARGIN, 3300), "GESER BUAT BACA  >>", font=f2,
             fill=theme["accent"])
    s.footer()
    return s.img


def render_stat(spec, scene, theme, idx, total, num):
    s = Slide(theme, idx, total)
    badge = scene.get("badge")
    if badge:
        s.chip(MARGIN, 280, badge)
        s.d.text((SIZE - MARGIN - F_MONO(88).getlength(
            f"{idx:02d} / {total:02d}"), 300),
            f"{idx:02d} / {total:02d}", font=F_MONO(88), fill=theme["dim"])
        y = 470
        s.d.line([(MARGIN, y), (SIZE - MARGIN, y)], fill=theme["border"],
                 width=6)
        s.d.line([(MARGIN, y), (MARGIN + int(CW * idx / total), y)],
                 fill=theme["accent"], width=6)
    else:
        s.header(f"{num:02d}")
    s.ghost(f"{num:02d}", y=560)
    stat = scene.get("stat", "")
    y = 1150
    if stat:
        s.d.text((MARGIN, y), stat, font=F_XB(560), fill=theme["accent"])
        y += 640
    label = scene.get("stat_label", "")
    if label:
        for ln in wrap_rich(label, F_B(118), F_SB(118), CW):
            draw_rich(s.d, MARGIN, y, ln, F_B(118), F_SB(118),
                      theme["dim"])
            y += 168
        y += 60
    for text in scene.get("lines", []):
        for ln in wrap_rich(text, F_B(132), F_SB(132), CW):
            draw_rich(s.d, MARGIN, y, ln, F_B(132), F_SB(132),
                      theme["text"], accent=theme["accent"])
            y += 190
        y += 30
    m = scene.get("mascot", {})
    if m:
        s.mascot(scene.get("pose", "base"), m.get("side", "right"),
                 width=430, bottom=560, flip=m.get("flip", False))
    s.footer()
    return s.img


def render_bars(spec, scene, theme, idx, total, num):
    s = Slide(theme, idx, total)
    s.header(f"{num:02d}")
    s.ghost(f"{num:02d}", y=560)
    stat = scene.get("stat", "")
    y = 1150
    if stat:
        s.d.text((MARGIN, y), stat, font=F_XB(520), fill=theme["accent"])
        y += 610
    label = scene.get("stat_label", "")
    if label:
        for ln in wrap_rich(label, F_B(118), F_SB(118), CW):
            draw_rich(s.d, MARGIN, y, ln, F_B(118), F_SB(118),
                      theme["dim"])
            y += 168
    bars = scene.get("bars", [])
    maxv = max((b["value"] for b in bars), default=1)
    y = 2400
    for b in bars:
        lab = b["label"]
        val = b["value"]
        s.d.text((MARGIN, y), lab, font=F_B(118), fill=theme["text"])
        lx = MARGIN + F_B(118).getlength(lab)
        if b.get("tag"):
            s.chip(lx + 44, y - 6, b["tag"], size=76,
                   bg=theme["accent"], fg=theme["chip_text"])
        vtxt = f"{val:g}%".replace(".", ",")
        vf = F_MONO(140)
        s.d.text((SIZE - MARGIN - vf.getlength(vtxt), y - 10), vtxt,
                 font=vf, fill=theme["accent"] if b.get("accent")
                 else theme["dim"])
        y += 190
        track_h = 130
        fill_w = int(CW * val / maxv)
        s.d.rounded_rectangle([MARGIN, y, SIZE - MARGIN, y + track_h],
                              radius=track_h // 2, fill=theme["bar_track"])
        if fill_w > track_h:
            s.d.rounded_rectangle(
                [MARGIN, y, MARGIN + fill_w, y + track_h],
                radius=track_h // 2,
                fill=theme["accent"] if b.get("accent")
                else theme["bar_other"])
        y += track_h + 150
    s.footer()
    return s.img


def render_lines(spec, scene, theme, idx, total, num):
    s = Slide(theme, idx, total)
    s.header(f"{num:02d}")
    s.ghost(f"{num:02d}", y=560)
    y = 1400
    for text in scene.get("lines", []):
        # accent square bullet
        s.d.rectangle([MARGIN, y + 42, MARGIN + 56, y + 98],
                      fill=theme["accent"])
        yy = y
        for ln in wrap_rich(text, F_B(150), F_SB(150), CW - 140):
            draw_rich(s.d, MARGIN + 140, yy, ln, F_B(150), F_SB(150),
                      theme["text"], accent=theme["accent"])
            yy += 210
        y = yy + 90
    m = scene.get("mascot", {})
    if m:
        s.mascot(scene.get("pose", "base"), m.get("side", "right"),
                 width=430, bottom=560, flip=m.get("flip", False))
    s.footer()
    return s.img


def render_close(spec, scene, theme, idx, total, link=None):
    s = Slide(theme, idx, total)
    title = spec.get("title", "")
    series = title.split(":")[0].upper() if ":" in title else title.upper()
    s.header(series)
    lines = scene.get("headline", [])
    f = F_XB(250)
    y = 1000
    for ln in lines:
        s.d.text((MARGIN, y), ln, font=f, fill=theme["text"])
        y += 300
    follow = strip_tags(scene.get("follow", ""))
    if follow:
        for ln in wrap_rich(follow, F_B(120), F_SB(120), CW):
            draw_rich(s.d, MARGIN, y + 60, ln, F_B(120), F_SB(120),
                      theme["dim"])
            y += 170
    s.chip(MARGIN, 2650, "GABUNG KOMUNITAS: S.PEKA.AI.ID/GABUNG",
           size=96, bg=None, fg=None)
    if link:
        txt = f"BACA SELENGKAPNYA: {link}"
        lf = F_B(96)
        tw = lf.getlength(txt)
        pad_x, pad_y = 44, 26
        h = 96 + 2 * pad_y
        x0, y0 = MARGIN, 2900
        s.d.rounded_rectangle([x0, y0, x0 + tw + 2 * pad_x, y0 + h],
                              radius=h // 2, outline=theme["accent"],
                              width=6)
        s.d.text((x0 + pad_x, y0 + pad_y - 6), txt, font=lf,
                 fill=theme["accent"])
    m = scene.get("mascot", {})
    s.mascot(scene.get("pose", "wave"), m.get("side", "right"),
             width=760, bottom=560, flip=m.get("flip", False))
    s.footer()
    return s.img


def build(spec_path, out_dir, theme_name=None, link=None):
    with open(spec_path) as fh:
        spec = json.load(fh)
    theme = load_theme(theme_name or spec.get("theme", "peka-yellow"))
    scenes = spec["scenes"]
    total = len(scenes)
    os.makedirs(out_dir, exist_ok=True)
    files = []
    num = 0
    for i, scene in enumerate(scenes, 1):
        kind = scene.get("kind")
        if kind == "hook":
            img = render_cover(spec, theme, i, total)
        elif kind == "close":
            img = render_close(spec, scene, theme, i, total, link=link)
        elif kind == "beat":
            num += 1
            if scene.get("bars"):
                img = render_bars(spec, scene, theme, i, total, num)
            elif scene.get("stat"):
                img = render_stat(spec, scene, theme, i, total, num)
            else:
                img = render_lines(spec, scene, theme, i, total, num)
        else:
            num += 1
            img = render_lines(spec, scene, theme, i, total, num)
        path = os.path.join(out_dir, f"threads-carousel-{i:02d}.png")
        img.save(path)
        files.append(path)
        print(f"slide {i}/{total}: {path}")
    manifest = {"spec": os.path.abspath(spec_path),
                "theme": theme_name or spec.get("theme", "peka-yellow"),
                "title": spec.get("title", ""),
                "link": link,
                "slides": [os.path.basename(p) for p in files]}
    with open(os.path.join(out_dir, "manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=2, ensure_ascii=False)
    return files


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("out_dir")
    ap.add_argument("--theme", default=None)
    ap.add_argument("--link", default=None,
                    help="Edition shortlink printed on the closing slide, "
                         "e.g. S.PEKA.AI.ID/XXXXXX")
    args = ap.parse_args()
    build(args.spec, args.out_dir, args.theme, args.link)
