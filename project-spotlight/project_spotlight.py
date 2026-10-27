"""Project spotlight carousel template (Peka paper style, 2048x2048).

Renders a project showcase carousel from a spec JSON file, so any future
project can reuse the Kata Wowo layout without writing a new script.

Usage:
    python3 project_spotlight.py <spec.json> [out_dir]

Spec schema:
{
  "project": "KATA WOWO",            # kicker in the header, uppercase
  "domain": "wowo.peka.ai.id",        # shown on the cover + CTA slide
  "slides": [
    {"type": "cover", "title": ["KATA", "WOWO"],
     "highlight": "Berapa persen pidato Wowo itu janji?",
     "body": "Bedah pidato Presiden Prabowo, per kalimat."},
    {"type": "text", "title": ["Papan skor", "pidato."],
     "body": ["paragraf 1", "paragraf 2"]},
    {"type": "chips", "title": ["6 label buat", "tiap kalimat."],
     "items": ["JANJI", "KLAIM DATA", ...],
     "footnote": "Satu kalimat, satu label."},
    {"type": "steps", "title": ["Tempel link,", "langsung dibedah."],
     "items": ["Tempel link YouTube pidato Prabowo.", ...]},
    {"type": "stats", "title": ["9 pidato sudah", "dianalisis."],
     "highlight": "2.709 kalimat.",
     "rows": [["Nota Keuangan dan RAPBN 2027", "893 kalimat"], ...],
     "footnote": "Plus 6 pidato lainnya di arsip."},
    {"type": "cta", "title": ["Coba", "sendiri."],
     "body": "Buka wowo.peka.ai.id, tempel link ...",
     "follow": "Follow @peka.ai.id dan gabung ke komunitas kami di url.peka.ai.id."}
  ]
}

Output files: <out_dir>/<slug>-01.png ... where slug defaults to the
lowercased project name with spaces removed, or "domain" stem if given.
All facts in a spec must be observed from the live project first; this
template never invents numbers, percentages, or claims.
"""
import json
import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 2048, 2048
PAPER = (246, 241, 230)
INK = (20, 20, 20)
GREY = (110, 105, 95)
YELLOW = (255, 214, 10)
FONTDIR = "/home/hatch/workspace/sertiku-poster/fonts"
ASSETS = "/home/hatch/workspace/peka-content/spill/animated/assets"
DEJAVU = os.path.join(ASSETS, "DejaVuSansMono-Bold.ttf")
MASCOT = os.path.join(ASSETS, "mascot-p-dark.png")


def F(name, size):
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
        self.project = spec["project"]
        self.domain = spec.get("domain", "")
        self.total = len(spec["slides"])

    def base(self, page):
        img = Image.new("RGB", (W, H), PAPER)
        d = ImageDraw.Draw(img)
        mono = ImageFont.truetype(DEJAVU, 34)
        d.text((110, 92), f"{self.project}  //  PROJECT PEKA", font=mono, fill=GREY)
        mas = Image.open(MASCOT).convert("RGBA")
        mas.thumbnail((72, 72))
        img.paste(mas, (W - 110 - 72 - 300, 70), mas)
        d.text((W - 110 - 290, 84), "peka.ai.id", font=F("Poppins-Bold.ttf", 44), fill=INK)
        d.line([(110, H - 170), (W - 110, H - 170)], fill=(180, 174, 160), width=3)
        d.text((110, H - 130), "GABUNG KE KOMUNITAS KAMI: URL.PEKA.AI.ID", font=mono, fill=GREY)
        d.text((W - 110 - 200, H - 130), f"{page:02d} / {self.total:02d}", font=mono, fill=GREY)
        return img, d

    def title_block(self, d, y, lines, size=150):
        font = F("Poppins-ExtraBold.ttf", size)
        for ln in lines:
            d.text((110, y), ln, font=font, fill=INK)
            y += size + 18
        return y

    def body(self, d, y, text, size=52, lh=76, max_w=W - 220):
        font = F("Poppins-SemiBold.ttf", size)
        for ln in wrap(d, text, font, max_w):
            d.text((110, y), ln, font=font, fill=(51, 51, 51))
            y += lh
        return y

    def highlight(self, d, y, text, size=64):
        font = F("Poppins-ExtraBold.ttf", size)
        w = d.textlength(text, font=font) + 60
        d.rectangle([110, y, 110 + w, y + size + 44], fill=YELLOW)
        d.text((140, y + 16), text, font=font, fill=INK)
        return y + size + 44

    def render(self, slide, page):
        img, d = self.base(page)
        t = slide["type"]
        if t == "cover":
            y = self.title_block(d, 330, slide["title"], size=230)
            if slide.get("highlight"):
                y = self.highlight(d, y + 30, slide["highlight"])
            if slide.get("body"):
                self.body(d, y + 60, slide["body"], size=56, lh=82)
            if self.domain:
                d.text((110, 1560), self.domain, font=F("Poppins-ExtraBold.ttf", 72), fill=INK)
        elif t == "text":
            y = self.title_block(d, 300, slide["title"])
            y += 40
            for para in slide["body"]:
                if isinstance(para, dict):
                    y = self.body(d, y, para["text"],
                                  size=para.get("size", 54),
                                  lh=para.get("lh", 80)) + 50
                else:
                    y = self.body(d, y, para, size=54, lh=80) + 50
        elif t == "chips":
            y = self.title_block(d, 300, slide["title"])
            font = F("Poppins-ExtraBold.ttf", 56)
            y += 50
            items = slide["items"]
            for i in range(0, len(items), 2):
                for j, lab in enumerate(items[i:i + 2]):
                    x = 110 + j * 920
                    w = d.textlength(lab, font=font) + 80
                    d.rectangle([x, y, x + w, y + 120], fill=INK)
                    d.text((x + 40, y + 30), lab, font=font, fill=YELLOW)
                y += 180
            if slide.get("footnote"):
                self.body(d, y + 30, slide["footnote"], size=48, lh=72)
        elif t == "steps":
            y = self.title_block(d, 300, slide["title"])
            y += 50
            mono = ImageFont.truetype(DEJAVU, 60)
            for i, txt in enumerate(slide["items"], 1):
                d.text((110, y), str(i), font=mono, fill=GREY)
                y = self.body(d, y, "   " + txt, size=54, lh=80) + 40
        elif t == "stats":
            y = self.title_block(d, 300, slide["title"])
            if slide.get("highlight"):
                y = self.highlight(d, y + 30, slide["highlight"], size=80)
            y += 70
            for name, cnt in slide["rows"]:
                d.text((110, y), name, font=F("Poppins-Bold.ttf", 52), fill=INK)
                d.text((110, y + 66), cnt, font=F("Poppins-SemiBold.ttf", 44), fill=GREY)
                y += 170
            if slide.get("footnote"):
                self.body(d, y + 10, slide["footnote"], size=48, lh=72)
        elif t == "cta":
            y = self.title_block(d, 330, slide["title"])
            y = self.body(d, y + 40, slide["body"], size=56, lh=82)
            if self.domain:
                y = self.highlight(d, y + 60, self.domain, size=72)
            if slide.get("follow"):
                self.body(d, y + 60, slide["follow"], size=48, lh=72)
        else:
            raise ValueError(f"unknown slide type: {t}")
        return img


def main():
    if len(sys.argv) < 2:
        print("usage: python3 project_spotlight.py <spec.json> [out_dir]")
        raise SystemExit(2)
    spec_path = sys.argv[1]
    with open(spec_path, encoding="utf-8") as fh:
        spec = json.load(fh)
    out_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "out")
    os.makedirs(out_dir, exist_ok=True)
    slug = spec.get("slug") or spec["project"].lower().replace(" ", "")
    r = Renderer(spec)
    for i, slide in enumerate(spec["slides"], 1):
        img = r.render(slide, i)
        img.save(os.path.join(out_dir, f"{slug}-{i:02d}.png"))
    print(f"saved {len(spec['slides'])} slides to {out_dir}")


if __name__ == "__main__":
    main()
