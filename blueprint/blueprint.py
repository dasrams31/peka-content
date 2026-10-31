#!/usr/bin/env python3
"""BLUEPRINT series - technical-drawing carousel (4096x4096, 4K).

One GitHub tool per edition, once a week. Spec-driven: all edition copy
comes from the spec JSON, never hardcoded here.
Design tokens: deep navy, faint grid, white hairlines, steel annotations,
Peka yellow for dimensions and the tool node. Poppins headlines,
DejaVu Sans Mono for annotations. Distinct from SPILL paper and from
Repo of the Week black/gold serif.

Usage: python3 blueprint.py <spec.json>
Spec: {"edition": 1, "agent": "CINDY", "name": "owner/repo",
  "stars": "8,7RB", "language": "TypeScript", "license": "Apache-2.0",
  "tagline": [...2 lines...], "how_headline": [...2 lines...],
  "how_body": "...", "how_start": "...",
  "devices": [{"name": "LAPTOP", "cap": "komputer kerja"}, ...],
  "steps": [{"title": "...", "desc": "..."}, x3],
  "note": "...", "out_dir": "/abs/path/carousel"}
"""
import json
import os
import sys

S = 4096 / 1080
W = H = 4096

NAVY = "#0A1A30"
PANEL = "#10264A"
GRID = "#1A2E4E"
HAIR = "#3D5A80"
WHITE = "#F2F5F9"
MUTED = "#8FA6C2"
YEL = "#FFD60A"
NAVYTXT = "#0A1A30"

POP_XB = "/home/hatch/workspace/sertiku-poster/fonts/Poppins-ExtraBold.ttf"
POP_B = "/home/hatch/workspace/sertiku-poster/fonts/Poppins-Bold.ttf"
POP_SB = "/home/hatch/workspace/sertiku-poster/fonts/Poppins-SemiBold.ttf"
DSANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DSANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
DMONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
DMONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

from PIL import Image, ImageDraw, ImageFont  # noqa: E402


def X(v):
    return int(round(v * S))


def xb(sz):
    return ImageFont.truetype(POP_XB, X(sz))


def bold(sz):
    return ImageFont.truetype(POP_B, X(sz))


def semibold(sz):
    return ImageFont.truetype(POP_SB, X(sz))


def body(sz, is_bold=False):
    return ImageFont.truetype(DSANS_B if is_bold else DSANS, X(sz))


def mono(sz, is_bold=False):
    return ImageFont.truetype(DMONO_B if is_bold else DMONO, X(sz))


# --- mascot with chroma-key (same source/threshold as spill.py) ---
_m = Image.open("/home/hatch/workspace/peka-logo/mascot-p.png").convert("RGB")
_mmask = Image.new("L", _m.size, 0)
_mp = _m.load()
_mk = _mmask.load()
for _yy in range(_m.size[1]):
    for _xx in range(_m.size[0]):
        _r, _g, _b = _mp[_xx, _yy]
        if _r > 30 or _g > 30 or _b > 30:
            _mk[_xx, _yy] = 255
_creature = _m.crop(_mmask.getbbox())
_cmask = _mmask.crop(_mmask.getbbox())


def lockup(img, d, cy=110, mh=46):
    cy_px, mh_px = X(cy), X(mh)
    cr = _creature.resize((int(_creature.width * mh_px / _creature.height), mh_px), Image.LANCZOS)
    mr = _cmask.resize(cr.size, Image.LANCZOS)
    tf = body(34, True)
    label = "peka.ai.id"
    ascent, descent = tf.getmetrics()
    tx = X(1008) - d.textlength(label, font=tf)
    ty = cy_px - (ascent + descent) // 2
    mx = tx - X(12) - cr.width
    my = cy_px - mh_px // 2 - int(mh_px * 0.03)
    img.paste(cr, (int(mx), int(my)), mr)
    d.text((tx, ty), label, font=tf, fill=WHITE)


def dashed_rect(d, box, color, width=3, dash=18, gap=12):
    x0, y0, x1, y1 = box
    w = X(width)
    x = x0
    while x < x1:
        d.line([(x, y0), (min(x + X(dash), x1), y0)], fill=color, width=w)
        d.line([(x, y1), (min(x + X(dash), x1), y1)], fill=color, width=w)
        x += X(dash + gap)
    y = y0
    while y < y1:
        d.line([(x0, y), (x0, min(y + X(dash), y1))], fill=color, width=w)
        d.line([(x1, y), (x1, min(y + X(dash), y1))], fill=color, width=w)
        y += X(dash + gap)


def dashed_line(d, p0, p1, color, width=3, dash=16, gap=10):
    import math
    x0, y0 = p0
    x1, y1 = p1
    total = math.hypot(x1 - x0, y1 - y0)
    if total == 0:
        return
    step = X(dash + gap)
    done = 0
    while done < total:
        t0 = done / total
        t1 = min((done + X(dash)) / total, 1.0)
        d.line([(x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0),
                (x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1)],
               fill=color, width=X(width))
        done += step


def arrow(d, x0, y0, x1, y1, color, width=4):
    d.line([(x0, y0), (x1, y1)], fill=color, width=X(width))
    ah = X(16)
    d.polygon([(x1, y1), (x1 - ah, y1 - ah // 2), (x1 - ah, y1 + ah // 2)], fill=color)


def wrap(d, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def base():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    for gx in range(0, 1081, 135):
        d.line([(X(gx), 0), (X(gx), H)], fill=GRID, width=X(1))
    for gy in range(0, 1081, 135):
        d.line([(0, X(gy)), (W, X(gy))], fill=GRID, width=X(1))
    d.rectangle([X(36), X(36), X(1044), X(1044)], outline=HAIR, width=X(3))
    for cx, cy in [(36, 36), (1044, 36), (36, 1044), (1044, 1044)]:
        d.line([(X(cx - 14), X(cy)), (X(cx + 14), X(cy))], fill=YEL, width=X(3))
        d.line([(X(cx), X(cy - 14)), (X(cx), X(cy + 14))], fill=YEL, width=X(3))
    return img, d


def header(img, d):
    tf = mono(32, True)
    label = "BLUEPRINT"
    tw = d.textlength(label, font=tf)
    x0, y0 = X(72), X(88)
    x1, y1 = x0 + tw + X(36), y0 + X(56)
    dashed_rect(d, (x0, y0, x1, y1), WHITE, width=3)
    ascent, descent = tf.getmetrics()
    d.text((x0 + X(18), y0 + (X(56) - (ascent + descent)) // 2), label, font=tf, fill=WHITE)
    d.text((x1 + X(16), y0 + (X(56) - (ascent + descent)) // 2), "// TOOLS", font=mono(32), fill=MUTED)
    lockup(img, d)


def footer(d, page, total=4):
    d.line([(X(72), X(984)), (X(1008), X(984))], fill=HAIR, width=X(2))
    d.text((X(72), X(1000)), "GABUNG KE KOMUNITAS KAMI: URL.PEKA.AI.ID", font=mono(27), fill=MUTED)
    label = "%02d / %02d" % (page, total)
    d.text((X(1008) - d.textlength(label, font=mono(27)), X(1000)), label, font=mono(27), fill=MUTED)


def section_label(d, y, text):
    tf = mono(36, True)
    d.text((X(72), X(y)), text, font=tf, fill=YEL)
    tw = d.textlength(text, font=tf)
    d.line([(X(72) + tw + X(24), X(y + 24)), (X(1008), X(y + 24))], fill=HAIR, width=X(2))


def chip(d, x, y, text):
    tf = mono(32)
    tw = d.textlength(text, font=tf)
    x1, y1 = x + tw + X(52), y + X(64)
    dashed_rect(d, (x, y, x1, y1), MUTED, width=3)
    ascent, descent = tf.getmetrics()
    d.text((x + X(26), y + (X(64) - (ascent + descent)) // 2), text, font=tf, fill=WHITE)
    return x1


def fit_font(d, lines, start, font_fn, max_w):
    size = start
    while size > 60:
        f = font_fn(size)
        if all(d.textlength(ln, font=f) <= max_w for ln in lines):
            return f
        size -= 4
    return font_fn(60)


def headline_block(d, lines, y0, step, start_size, max_w):
    """Draw headline lines, return the y (1080-space) for the rule below."""
    hf = fit_font(d, lines, start_size, xb, max_w)
    for i, line in enumerate(lines):
        d.text((X(72), X(y0) + i * X(step)), line, font=hf, fill=WHITE)
    ascent, descent = hf.getmetrics()
    rule_y = y0 + (len(lines) - 1) * step + (ascent + descent) / S + 16
    d.line([(X(72), X(rule_y)), (X(72) + d.textlength(lines[0], font=hf), X(rule_y))],
           fill=YEL, width=X(6))
    return rule_y


def cover(spec, out_dir):
    img, d = base()
    header(img, d)
    ep = "%02d" % spec["edition"]
    section_label(d, 212, "EDISI #%s / GAMBAR KERJA" % ep)
    nf = fit_font(d, [spec["agent"]], 230, xb, X(936))
    ny = X(300)
    d.text((X(72), ny), spec["agent"], font=nf, fill=WHITE)
    nw = d.textlength(spec["agent"], font=nf)
    # Rule + repo name must sit below the headline's actual ink, not below
    # its full ascent+descent box (which leaves ~95u dead space and pushed
    # the repo name onto the tagline at y=660). textbbox bottom is the
    # ink bottom relative to the draw anchor.
    ink = d.textbbox((0, 0), spec["agent"], font=nf)
    ly = 300 + ink[3] / S + 16
    d.line([(X(72), X(ly)), (X(72) + nw, X(ly))], fill=YEL, width=X(5))
    d.line([(X(72), X(ly) - X(12)), (X(72), X(ly) + X(12))], fill=YEL, width=X(5))
    d.line([(X(72) + nw, X(ly) - X(12)), (X(72) + nw, X(ly) + X(12))], fill=YEL, width=X(5))
    d.text((X(72), X(ly) + X(22)), spec["name"], font=mono(34), fill=MUTED)
    for i, line in enumerate(spec["tagline"]):
        d.text((X(72), X(660) + i * X(58)), line, font=body(46), fill=WHITE)
    cx = X(72)
    for text in [spec["language"].upper(), spec["license"].upper(), spec["stars"] + " STAR"]:
        cx = chip(d, cx, X(800), text) + X(28)
    labels = ["INPUT", "TOOL", "OUTPUT"]
    boxes = [("LAPTOP", 250), (spec["agent"], 300), ("HP", 250)]
    total_w = sum(w for _, w in boxes) + 2 * 90
    by = X(912)
    x = X(72) + (X(936) - X(total_w)) // 2
    for i, ((text, w), lab) in enumerate(zip(boxes, labels)):
        d.text((x + (X(w) - d.textlength(lab, font=mono(26))) / 2, X(878)), lab, font=mono(26), fill=MUTED)
        tf = bold(34)
        if text == spec["agent"]:
            d.rectangle([x, by, x + X(w), by + X(56)], fill=YEL)
            d.text((x + (X(w) - d.textlength(text, font=tf)) / 2, by + X(8)), text, font=tf, fill=NAVYTXT)
        else:
            d.rectangle([x, by, x + X(w), by + X(56)], outline=WHITE, width=X(3))
            d.text((x + (X(w) - d.textlength(text, font=tf)) / 2, by + X(8)), text, font=tf, fill=WHITE)
        if i < 2:
            arrow(d, x + X(w) + X(12), by + X(28), x + X(w) + X(78), by + X(28), YEL, width=4)
        x += X(w) + X(90)
    footer(d, 1)
    img.save(out_dir + "/blueprint-01.png")


def how(spec, out_dir):
    img, d = base()
    header(img, d)
    section_label(d, 212, "02 / CARA KERJA")
    lines = spec["how_headline"]
    rule_y = headline_block(d, lines, 280, 114, 118, X(936))
    node = (X(440), X(rule_y + 56), X(640), X(rule_y + 144))
    devices = [
        ((X(80), X(rule_y + 28), X(330), X(rule_y + 116)), spec["devices"][0]["name"], spec["devices"][0]["cap"]),
        ((X(750), X(rule_y + 28), X(1000), X(rule_y + 116)), spec["devices"][1]["name"], spec["devices"][1]["cap"]),
        ((X(415), X(rule_y + 188), X(665), X(rule_y + 276)), spec["devices"][2]["name"], spec["devices"][2]["cap"]),
    ]
    for (box, name, cap) in devices:
        dashed_line(d, ((box[0] + box[2]) // 2, (box[1] + box[3]) // 2),
                    ((node[0] + node[2]) // 2, (node[1] + node[3]) // 2), HAIR, width=3)
    for (box, name, cap) in devices:
        d.rectangle(box, fill=PANEL, outline=WHITE, width=X(3))
        tf = bold(34)
        d.text(((box[0] + box[2] - d.textlength(name, font=tf)) / 2, box[1] + X(10)), name, font=tf, fill=WHITE)
        cf = mono(22)
        d.text(((box[0] + box[2] - d.textlength(cap, font=cf)) / 2, box[1] + X(54)), cap, font=cf, fill=MUTED)
    d.rectangle(node, fill=YEL)
    tf = xb(44)
    d.text(((node[0] + node[2] - d.textlength(spec["agent"], font=tf)) / 2, node[1] + X(16)),
           spec["agent"], font=tf, fill=NAVYTXT)
    d.text((X(72), X(rule_y + 304)), spec["how_body"], font=body(40), fill=WHITE)
    d.text((X(72), X(rule_y + 352)), spec["how_start"], font=mono(30, True), fill=YEL)
    footer(d, 2)
    img.save(out_dir + "/blueprint-02.png")


def steps(spec, out_dir):
    img, d = base()
    header(img, d)
    section_label(d, 212, "03 / LANGKAH MULAI")
    lines = ["MULAI DALAM", "3 LANGKAH."]
    rule_y = headline_block(d, lines, 272, 108, 118, X(936))
    y = X(rule_y + 22)
    for i, st in enumerate(spec["steps"]):
        dashed_rect(d, (X(72), y, X(1008), y + X(120)), HAIR, width=3)
        d.text((X(100), y + X(34)), "%02d" % (i + 1), font=mono(40, True), fill=YEL)
        title_lines = wrap(d, st["title"], bold(34), X(788))[:2]
        desc_lines = wrap(d, st["desc"], body(28), X(788))
        desc_lines = desc_lines[: max(1, 3 - len(title_lines))]
        ty = y + X(14)
        for tline in title_lines:
            d.text((X(196), ty), tline, font=bold(34), fill=WHITE)
            ty += X(42)
        for dline in desc_lines:
            d.text((X(196), ty + X(4)), dline, font=body(28), fill=MUTED)
            ty += X(34)
        y += X(134)
    footer(d, 3)
    img.save(out_dir + "/blueprint-03.png")


def follow(spec, out_dir):
    img, d = base()
    header(img, d)
    section_label(d, 212, "04 / FOLLOW + GABUNG")
    lines = ["FOLLOW DAN", "GABUNG."]
    rule_y = headline_block(d, lines, 272, 108, 118, X(936))
    rows = [
        ("FOLLOW", "@peka.ai.id di IG, Threads, TikTok."),
        ("GABUNG", "grup WhatsApp via url.peka.ai.id."),
        ("SAVE + SHARE", "biar makin banyak yang kebantu."),
    ]
    # Shortlink printed on the last slide (Threads no-link rule, 31 Okt
    # 2026): the edition's link lives here, not in a Threads comment.
    if spec.get("shortlink"):
        shown = spec["shortlink"].replace("https://", "").replace("http://", "")
        rows.append(("LINK REPO", shown))
    else:
        rows.append(("KOMENTAR", "link repo-nya ada di komentar."))
    y = X(rule_y + 24)
    for label, rest in rows:
        dashed_rect(d, (X(72), y, X(1008), y + X(88)), HAIR, width=3)
        lf = mono(30, True)
        d.text((X(100), y + X(26)), label, font=lf, fill=YEL)
        rx = X(100) + d.textlength(label, font=lf) + X(28)
        d.text((rx, y + X(22)), rest, font=semibold(38), fill=WHITE)
        y += X(106)
    footer(d, 4)
    img.save(out_dir + "/blueprint-04.png")


def main():
    with open(sys.argv[1], encoding="utf-8") as fh:
        spec = json.load(fh)
    out_dir = spec["out_dir"]
    os.makedirs(out_dir, exist_ok=True)
    assert len(spec["steps"]) == 3, "BLUEPRINT needs exactly 3 steps"
    assert len(spec["devices"]) == 3, "BLUEPRINT needs exactly 3 devices"
    cover(spec, out_dir)
    how(spec, out_dir)
    steps(spec, out_dir)
    follow(spec, out_dir)
    print("blueprint slides OK ->", out_dir)


if __name__ == "__main__":
    main()
