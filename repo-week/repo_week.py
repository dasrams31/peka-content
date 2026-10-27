"""Repo of the Week: premium, exclusive single-repo carousel (2048x2048).

Dark editorial look, deliberately different from the paper SPILL style:
near-black canvas, muted gold rules, serif display type, generous air,
one repo per edition, four slides only.

Usage:
    python3 repo_week.py <spec.json> [out_dir]

Spec schema:
{
  "series": "REPO OF THE WEEK",
  "episode": "01",
  "repo": "browser-use",
  "owner": "browser-use",
  "url": "github.com/browser-use/browser-use",
  "stars": "119RB", "forks": "13,3RB", "issues": "616",
  "hook": "Browser yang bisa disuruh AI.",
  "why": ["paragraf 1", "paragraf 2"],
  "install": "pip install browser-use",
  "cocok": "yang bikin otomasi web atau AI agent yang harus klik dan isi halaman sendiri."
}

All facts in a spec must be observed from live GitHub/PyPI first.
"""
import json
import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 2048, 2048
BG = (11, 11, 13)
PANEL = (20, 20, 24)
GOLD = (212, 175, 55)
CREAM = (242, 239, 230)
MUTED = (154, 149, 138)
DEJAVU = "/usr/share/fonts/truetype/dejavu"
FONTDIR = "/home/hatch/workspace/sertiku-poster/fonts"
MARGIN = 160


def serif(size):
    return ImageFont.truetype(os.path.join(DEJAVU, "DejaVuSerif-Bold.ttf"), size)


def mono(size):
    return ImageFont.truetype(os.path.join(DEJAVU, "DejaVuSansMono.ttf"), size)


def sans(size, bold=True):
    name = "Poppins-Bold.ttf" if bold else "Poppins-SemiBold.ttf"
    return ImageFont.truetype(os.path.join(FONTDIR, name), size)


def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


class Renderer:
    def __init__(self, spec):
        self.s = spec

    def base(self, page, total):
        img = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(img)
        d.text((MARGIN, 96), self.s["series"], font=mono(34), fill=GOLD)
        # Peka lockup top-right: yellow P mascot (black keyed out) + wordmark
        mas = Image.open("/home/hatch/workspace/peka-logo/mascot-p.png").convert("RGB")
        alpha = mas.convert("L").point(lambda v: 255 if v > 60 else 0)
        bbox = alpha.getbbox()
        mas = mas.crop(bbox)
        alpha = alpha.crop(bbox)
        mh = 54
        mw = int(mas.width * mh / mas.height)
        mas = mas.resize((mw, mh))
        alpha = alpha.resize((mw, mh))
        wfont = sans(40, bold=True)
        wtxt = "peka.ai.id"
        tw = d.textlength(wtxt, font=wfont)
        lx = W - MARGIN - (mw + 16 + int(tw))
        img.paste(mas, (lx, 88), alpha)
        d.text((lx + mw + 16, 96), wtxt, font=wfont, fill=CREAM)
        d.line([(MARGIN, H - 190), (W - MARGIN, H - 190)], fill=GOLD, width=2)
        d.text((MARGIN, H - 140), f"EDISI {self.s['episode']}", font=mono(30), fill=MUTED)
        d.text((W - MARGIN - 200, H - 140), f"{page:02d} / {total:02d}",
               font=mono(30), fill=MUTED)
        return img, d

    def body(self, d, y, text, size=54, lh=84, color=CREAM, max_w=W - 2 * MARGIN):
        font = sans(size, bold=False)
        for ln in wrap(d, text, font, max_w):
            d.text((MARGIN, y), ln, font=font, fill=color)
            y += lh
        return y

    def render(self, kind, page, total):
        s = self.s
        img, d = self.base(page, total)
        if kind == "cover":
            d.text((MARGIN, 560), s["repo"], font=serif(210), fill=CREAM)
            d.line([(MARGIN, 830), (MARGIN + 220, 830)], fill=GOLD, width=4)
            y = self.body(d, 900, s["hook"], size=64, lh=92, color=GOLD)
            d.text((MARGIN, 1180),
                   f"{s['stars']} STARS   ·   {s['forks']} FORKS   ·   {s['issues']} ISSUES",
                   font=mono(38), fill=MUTED)
            d.text((MARGIN, 1300), s["url"], font=mono(40), fill=CREAM)
        elif kind == "why":
            d.text((MARGIN, 300), "KENAPA REPO INI", font=mono(36), fill=GOLD)
            if s.get("image"):
                from PIL import Image as _Image
                box = (MARGIN, 420, W - MARGIN, 1300)
                d.rectangle(box, outline=GOLD, width=2, fill=PANEL)
                # browser window title bar: exit / minimize / maximize + URL
                d.rectangle([box[0], box[1], box[2], box[1] + 90], fill=(26, 26, 30))
                d.line([(box[0], box[1] + 90), (box[2], box[1] + 90)], fill=GOLD, width=2)
                for i, col in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
                    cx = box[0] + 44 + i * 60
                    d.ellipse([cx - 18, box[1] + 45 - 18, cx + 18, box[1] + 45 + 18],
                              fill=col)
                url = s.get("url", "")
                uf = mono(30)
                d.text(((box[0] + box[2]) / 2 - d.textlength(url, font=uf) / 2,
                        box[1] + 28), url, font=uf, fill=MUTED)
                im = _Image.open(s["image"]).convert("RGB")
                bw, bh = box[2] - box[0], box[3] - (box[1] + 90)
                sc = min(bw / im.width, bh / im.height)
                im = im.resize((int(im.width * sc), int(im.height * sc)))
                img.paste(im, (box[0] + (bw - im.width) // 2,
                               box[1] + 90 + (bh - im.height) // 2))
                y = 1380
                for para in s["why"]:
                    y = self.body(d, y, para, size=56, lh=84) + 40
            else:
                y = 420
                for para in s["why"]:
                    y = self.body(d, y, para, size=58, lh=88) + 60
        elif kind == "install":
            d.text((MARGIN, 300), "INSTALL", font=mono(36), fill=GOLD)
            d.rectangle([MARGIN, 420, W - MARGIN, 660], outline=GOLD, width=2, fill=PANEL)
            d.text((MARGIN + 60, 500), "$", font=mono(64), fill=GOLD)
            d.text((MARGIN + 140, 500), s["install"], font=mono(58), fill=CREAM)
            d.text((MARGIN, 820), "COCOK BUAT", font=mono(36), fill=GOLD)
            self.body(d, 940, s["cocok"], size=58, lh=88)
        elif kind == "closing":
            d.text((MARGIN, 620), f"Edisi {s['episode']} selesai.",
                   font=serif(110), fill=CREAM)
            d.line([(MARGIN, 820), (MARGIN + 220, 820)], fill=GOLD, width=4)
            y = self.body(d, 900, f"Repo minggu ini: {s['url']}", size=52, lh=80)
            y = self.body(d, y + 40,
                          "Follow @peka.ai.id dan gabung ke komunitas kami "
                          "di url.peka.ai.id.", size=52, lh=80)
        else:
            raise ValueError(kind)
        return img


def main():
    if len(sys.argv) < 2:
        print("usage: python3 repo_week.py <spec.json> [out_dir]")
        raise SystemExit(2)
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    out_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "out")
    os.makedirs(out_dir, exist_ok=True)
    slug = spec.get("slug", "rotw-sample")
    kinds = ["cover", "why", "install", "closing"]
    r = Renderer(spec)
    for i, kind in enumerate(kinds, 1):
        r.render(kind, i, len(kinds)).save(os.path.join(out_dir, f"{slug}-{i:02d}.png"))
    print(f"saved {len(kinds)} slides to {out_dir}")


if __name__ == "__main__":
    main()
