#!/usr/bin/env python3
"""Spill-repo carousel: cover + one slide per repo + closing.

Paper spill format (see spill.py). Driven by a JSON spec:
{"agent": "CLAUDE", "next": "Hermes", "date": "2026-10-20",
 "repos": [{"name": "owner/repo", "stars": "182RB",
            "desc": "...", "cocok": "..."}],
 "out_dir": "/abs/dir"}
Slides: 01 cover, 02..N+1 one per repo, last closing.

Repo slide format (locked 2026-10-27, revised same day per user feedback):
square 2048x2048, paper background, small tilted SPILL stamp + dark
mascot lockup + repo counter header, then a browser-window mockup
whose body is the repo's real GitHub social card (og:image, fetched
live), a terminal panel with the install command, then the full
Indonesian explanation below the terminal, then COCOK BUAT, then the
footer (community line + page number). Cover, closing, and follow
slides keep the old design.

Repo slides enrich the spec via public GitHub endpoints at render time
(API repo data, languages, owner avatar, og:image, install command
from the README). Any enrichment failure degrades gracefully: spec
text, spec stars, a generic `npx skills add` install, the drawn card
instead of the og screenshot, no avatar, no language bar, never a
failed edition. A spec repo may also carry an explicit "install"
field which wins over README extraction.
"""
import io
import json
import os
import re
import sys
import urllib.error
import urllib.request

from PIL import Image, ImageDraw, ImageFont, ImageOps

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spill import (DESC, GRY, HAIR, INK, PAPER, X, base, f, footer, highlight,
                   mono, wrap)

GHOST = "#e9dfc6"
UA = {"User-Agent": "peka-spill-carousel"}

POPPINS = "/home/hatch/workspace/sertiku-poster/fonts"
DEJAVU = "/usr/share/fonts/truetype/dejavu"


def _font(name, size):
    for path in (os.path.join(POPPINS, name),
                 os.path.join(DEJAVU, "DejaVuSans-Bold.ttf")):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _mono(size, bold=False):
    return ImageFont.truetype(
        os.path.join(DEJAVU, "DejaVuSansMono-Bold.ttf" if bold else "DejaVuSansMono.ttf"),
        size)


def _rounded_mask(size, radius):
    m = Image.new("L", size, 0)
    md = ImageDraw.Draw(m)
    md.rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius=radius, fill=255)
    return m


# ---------------------------------------------------------------- GitHub

def _get_json(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.load(resp)


def _get_text(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode("utf-8", "replace")


def fmt_count(n):
    # GitHub-style abbreviation: 115336 -> "115k", 6700 -> "6.7k"
    if n >= 1_000_000:
        v = f"{n / 1_000_000:.1f}".rstrip("0").rstrip(".")
        return v + "M"
    if n >= 100_000:
        return f"{n // 1000}k"
    if n >= 1000:
        v = f"{n / 1000:.1f}".rstrip("0").rstrip(".")
        return v + "k"
    return str(n)


def clean_desc(text):
    """Drop emoji/symbols the slide fonts cannot render (tofu boxes),
    keep letters, numbers, punctuation, marks, spaces, math/currency."""
    import unicodedata
    out = []
    for c in text:
        cat = unicodedata.category(c)
        if cat[0] in "LNPM" or cat in ("Zs", "Sm", "Sc"):
            out.append(c)
    return re.sub(r"\s+", " ", "".join(out)).strip()


def parse_spec_stars(s):
    m = re.match(r"(\d+)\s*RB", (s or "").upper())
    return int(m.group(1)) * 1000 if m else 0


LANG_COLORS = {
    "Go": (0, 173, 216), "JavaScript": (241, 224, 90), "TypeScript": (49, 120, 198),
    "Python": (53, 114, 165), "Rust": (222, 165, 132), "HTML": (227, 76, 38),
    "CSS": (86, 61, 124), "Shell": (137, 224, 81), "Ruby": (112, 21, 22),
    "Java": (176, 114, 25), "C++": (243, 75, 65), "C": (85, 85, 85),
    "PHP": (79, 93, 149), "Swift": (240, 81, 56), "Kotlin": (169, 123, 255),
    "Dockerfile": (56, 77, 84),
}

INSTALL_PATTERNS = [
    r"npx\s+skills\s+add\s+[^\s`'\"]+(?:\s+-[a-zA-Z]+)?",
    r"/plugin\s+marketplace\s+add\s+[^\s`'\"]+",
    r"\S+\s+plugin\s+add\s+[^\s`'\"]+",
    r"npm\s+(?:install|i)\s+-g\s+[^\s`'\"]+",
    r"pip\s+install\s+[^\s`'\"]+",
    r"go\s+install\s+[^\s`'\"]+",
    r"cargo\s+install\s+[^\s`'\"]+",
    r"brew\s+install\s+[^\s`'\"]+",
]


def readme_install(full):
    for branch in ("main", "master"):
        try:
            text = _get_text(f"https://raw.githubusercontent.com/{full}/{branch}/README.md")
        except Exception:
            continue
        for pat in INSTALL_PATTERNS:
            m = re.search(pat, text)
            if m:
                cmd = m.group(0).strip().strip("`$").strip()
                return re.sub(r"\s+", " ", cmd)[:60]
    return None


_ENRICH = {}


def enrich(repo):
    """Live GitHub data for one spec repo, with graceful fallbacks."""
    full = repo["name"]
    if full in _ENRICH:
        return _ENRICH[full]
    out = {"en_desc": clean_desc(repo["desc"]),
           "stars": fmt_count(parse_spec_stars(repo.get("stars"))),
           "forks": None, "issues": None, "langs": [], "avatar": None, "og": None,
           "install": repo.get("install") or f"npx skills add {full} -g"}
    try:
        data = _get_json(f"https://api.github.com/repos/{full}")
        out["en_desc"] = clean_desc(data.get("description") or repo["desc"])
        out["stars"] = fmt_count(data.get("stargazers_count") or 0)
        out["forks"] = fmt_count(data.get("forks_count") or 0)
        out["issues"] = fmt_count(data.get("open_issues_count") or 0)
        try:
            langs = _get_json(f"https://api.github.com/repos/{full}/languages")
            total = sum(langs.values()) or 1
            top = sorted(langs.items(), key=lambda kv: -kv[1])[:4]
            out["langs"] = [(LANG_COLORS.get(k, (153, 153, 153)), v / total) for k, v in top]
        except Exception as exc:
            print(f"warn: languages failed for {full}: {exc}")
        avatar_url = (data.get("owner") or {}).get("avatar_url")
        if avatar_url:
            sep = "&" if "?" in avatar_url else "?"
            req = urllib.request.Request(avatar_url + sep + "s=560", headers=UA)
            with urllib.request.urlopen(req, timeout=15) as resp:
                out["avatar"] = Image.open(io.BytesIO(resp.read())).convert("RGB")
    except Exception as exc:
        print(f"warn: GitHub API failed for {full}: {exc} (fallbacks used)")
    try:
        req = urllib.request.Request(f"https://github.com/{full}", headers=UA)
        html = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace")
        m = re.search(r'<meta property="og:image" content="([^"]+)"', html)
        if m:
            ireq = urllib.request.Request(m.group(1), headers=UA)
            with urllib.request.urlopen(ireq, timeout=20) as resp:
                out["og"] = Image.open(io.BytesIO(resp.read())).convert("RGB")
            # best-effort day cache so the reel step reuses this shot
            # instead of re-downloading (opengraph rate-limits bursts)
            try:
                import datetime
                cdir = f"/tmp/spill-shots/{datetime.date.today().isoformat()}"
                os.makedirs(cdir, exist_ok=True)
                out["og"].save(os.path.join(cdir, full.replace("/", "-") + ".png"))
            except Exception:
                pass
    except Exception as exc:
        print(f"warn: og image failed for {full}: {exc}")
    if not repo.get("install"):
        try:
            found = readme_install(full)
            if found:
                out["install"] = found
            else:
                print(f"warn: no install command in README for {full}, generic fallback used")
        except Exception as exc:
            print(f"warn: README fetch failed for {full}: {exc}")
    _ENRICH[full] = out
    return out


# ---------------------------------------------------------------- header

def _dark_mascot():
    """Dark P-mascot (transparent) for light backgrounds, same geometry
    as peka-logo/mascot.py::mascot_p."""
    if _dark_mascot.cache is not None:
        return _dark_mascot.cache
    S = 1080
    mask = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle([507, 232, 523, 332], radius=8, fill=255)
    d.ellipse([487, 177, 543, 233], fill=255)
    d.rounded_rectangle([450, 330, 580, 822], radius=65, fill=255)
    d.arc([600 - 140, 455 - 140, 600 + 140, 455 + 140], start=-90, end=90, fill=255, width=100)
    d.ellipse([465, 400, 555, 490], fill=0)
    d.arc([470, 515, 550, 595], start=25, end=155, fill=0, width=18)
    out = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    out.paste(Image.new("RGBA", (S, S), (17, 17, 17, 255)), mask=mask)
    _dark_mascot.cache = out
    return out


_dark_mascot.cache = None


def repo_header(img, d, spec, idx):
    """Small tilted SPILL stamp + dark lockup + counter (demo v4)."""
    spill_f = _font("Poppins-ExtraBold.ttf", 68)
    layer = Image.new("RGBA", (360, 170), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rectangle([6, 6, 354, 164], outline=INK, width=6)
    ld.text((36, 36), "SPILL", font=spill_f, fill=INK)
    layer = layer.rotate(-3, expand=True, resample=Image.BICUBIC)
    img.paste(layer, (130, 110), layer)
    d.text((154, 320), f"REPO {idx + 1:02d} DARI {len(spec['repos']):02d} // {spec['agent'].upper()}",
           font=_mono(42), fill=GRY)
    mas = _dark_mascot()
    bbox = mas.getchannel("A").getbbox()
    mas = mas.crop(bbox)
    mas = mas.resize((72, int(72 * mas.height / mas.width)))
    lock_f = _font("Poppins-Bold.ttf", 36)
    label = "peka.ai.id"
    lw = d.textlength(label, font=lock_f)
    lx = 2048 - 154 - 72 - 16 - int(lw)
    img.paste(mas, (lx, 120), mas)
    d.text((lx + 88, 120 + (mas.height - 36) // 2), label, font=lock_f, fill=INK)


# ---------------------------------------------------------------- slides

def cover(spec):
    agent = spec["agent"].upper()
    repos = spec["repos"]
    img, d = base(1)
    total = len(repos) + 3
    ep = spec.get("episode")
    kick = f"SPILL REPO // HARI INI: {agent}"
    if ep:
        kick = f"SPILL REPO // EDISI #{int(ep):02d} // {agent}"
    d.text((X(70), X(170)), kick, font=mono(26), fill=GRY)
    tf = f(96)
    d.text((X(70), X(214)), "REPO SKILL", font=tf, fill=INK)
    highlight(d, X(70), X(330), agent, tf)
    sub = f"{len(repos)} repo GitHub berisi skill siap pakai, dibedah satu satu."
    sy = 478
    for ln in wrap(d, sub, f(30, False), X(930)):
        d.text((X(70), X(sy)), ln, font=f(30, False), fill=DESC)
        sy += 42
    gf = f(26)
    gt = "Geser, dibedah satu satu >>>"
    d.text((X(1010) - d.textlength(gt, font=gf), X(560)), gt, font=gf, fill=INK)
    cy = 606
    for r in repos:
        d.rectangle([X(70), X(cy), X(1010), X(cy + 62)], fill=INK)
        d.text((X(94), X(cy + 15)), r["name"], font=f(27), fill="#ffffff")
        sf = f(24)
        st = f"{r['stars']} STAR"
        d.text((X(986) - d.textlength(st, font=sf), X(cy + 18)), st, font=sf, fill="#ffd60a")
        cy += 76
    footer(d, 1, total)
    return img


def repo_slide(spec, idx, repo):
    agent = spec["agent"].upper()
    total = len(spec["repos"]) + 3
    page = idx + 2
    en = enrich(repo)
    W = H = 2048
    MX = 154
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    repo_header(img, d, spec, idx)

    # ---- browser-window mockup ----
    WX, WY, WW = MX, 420, W - 2 * MX
    TITLE_H = 92
    if en["og"]:
        # real GitHub social card inside the window
        og = en["og"].resize((1200, 600), Image.LANCZOS)
        WH = TITLE_H + 600
        win = Image.new("RGB", (WW, WH), (255, 255, 255))
        wd = ImageDraw.Draw(win)
        wd.rectangle([0, 0, WW - 1, TITLE_H - 1], fill=(0, 0, 0))
        for i, c in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
            wd.ellipse([48 + i * 60, 30, 48 + i * 60 + 36, 66], fill=c)
        wd.text((240, 26), repo["name"], font=_mono(42), fill=(170, 170, 170))
        win.paste(og, ((WW - 1200) // 2, TITLE_H))
    else:
        # drawn fallback (same info, no screenshot)
        BODY_PAD, AVATAR = 76, 280
        win = Image.new("RGB", (WW, 1200), (255, 255, 255))
        wd = ImageDraw.Draw(win)
        wd.rectangle([0, 0, WW - 1, TITLE_H - 1], fill=(0, 0, 0))
        for i, c in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
            wd.ellipse([48 + i * 60, 30, 48 + i * 60 + 36, 66], fill=c)
        wd.text((240, 26), repo["name"], font=_mono(42), fill=(170, 170, 170))
        owner, name = repo["name"].split("/", 1)
        y = TITLE_H + BODY_PAD
        desc_w = WW - 2 * BODY_PAD - (AVATAR + 56 if en["avatar"] else 0)
        size = 104
        while size > 56:
            f_light = _font("Poppins-SemiBold.ttf", size)
            f_bold = _font("Poppins-ExtraBold.ttf", size)
            if wd.textlength(owner + "/", font=f_light) + wd.textlength(name, font=f_bold) <= desc_w:
                break
            size -= 4
        wd.text((BODY_PAD, y), owner + "/", font=f_light, fill=(60, 60, 60))
        w1 = wd.textlength(owner + "/", font=f_light)
        wd.text((BODY_PAD + w1, y), name, font=f_bold, fill=INK)
        if en["avatar"]:
            av = ImageOps.fit(en["avatar"], (AVATAR, AVATAR))
            av.putalpha(_rounded_mask((AVATAR, AVATAR), 36))
            win.paste(av, (WW - BODY_PAD - AVATAR, TITLE_H + BODY_PAD), av)
        f_desc = _font("Poppins-SemiBold.ttf", 48)
        desc_lines = wrap(wd, en["en_desc"], f_desc, desc_w)
        if len(desc_lines) > 3:
            desc_lines = desc_lines[:3]
            desc_lines[-1] = desc_lines[-1].rsplit(" ", 1)[0] + "…"
        y += 130 + 30
        for line in desc_lines:
            wd.text((BODY_PAD, y), line, font=f_desc, fill=(85, 85, 85))
            y += 68
        y += 70
        f_num = _font("Poppins-Bold.ttf", 56)
        f_lbl = _font("Poppins-SemiBold.ttf", 36)
        stats = [("Stars", en["stars"]), ("Forks", en["forks"]), ("Issues", en["issues"])]
        col_w = (WW - 2 * BODY_PAD) // 3
        for i, (lbl, val) in enumerate(stats):
            x = BODY_PAD + i * col_w
            wd.text((x, y), val if val else "–", font=f_num, fill=INK)
            wd.text((x, y + 68), lbl, font=f_lbl, fill=(153, 153, 153))
        y += 68 + 52 + 56
        if en["langs"]:
            bw_total = WW - 2 * BODY_PAD
            bar = Image.new("RGB", (bw_total, 20), (255, 255, 255))
            bd = ImageDraw.Draw(bar)
            bx = 0
            for col, frac in en["langs"]:
                seg = int(bw_total * frac)
                if seg <= 0:
                    continue
                bd.rectangle([bx, 0, min(bx + seg - 1, bw_total - 1), 19], fill=col)
                bx += seg
            bar.putalpha(_rounded_mask((bw_total, 20), 10))
            win.paste(bar, (BODY_PAD, y), bar)
            y += 20
        WH = y + BODY_PAD
        win = win.crop((0, 0, WW, WH))
    img.paste(win, (WX, WY), _rounded_mask((WW, WH), 40))
    d.rounded_rectangle([WX, WY, WX + WW - 1, WY + WH - 1], radius=40,
                        outline=(190, 185, 172), width=2)

    # ---- terminal panel ----
    ty = WY + WH + 36
    PANEL_H = 150
    panel = Image.new("RGB", (WW, PANEL_H), (20, 20, 26))
    pd = ImageDraw.Draw(panel)
    for i, c in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
        pd.ellipse([40 + i * 44, 26, 40 + i * 44 + 24, 50], fill=c)
    pd.text((196, 22), "terminal", font=_mono(32), fill=(130, 130, 130))
    cmd = en["install"]
    tsize = 44
    while tsize > 30 and pd.textlength("$ " + cmd, font=_mono(tsize, True)) > WW - 120:
        tsize -= 2
    tf = _mono(tsize, True)
    px, py = 44, 84
    pd.text((px, py), "$ ", font=tf, fill="#ffd60a")
    px += pd.textlength("$ ", font=tf)
    pd.text((px, py), cmd, font=tf, fill=(255, 255, 255))
    cx = px + pd.textlength(cmd, font=tf) + 16
    pd.rectangle([cx, py + 2, cx + 24, py + 50], fill="#ffd60a")
    img.paste(panel, (WX, ty), _rounded_mask((WW, PANEL_H), 28))
    d.rounded_rectangle([WX, ty, WX + WW - 1, ty + PANEL_H - 1], radius=28,
                        outline=(70, 70, 80), width=2)

    # ---- footer zone: full explanation, then COCOK BUAT ----
    fy = ty + PANEL_H + 36
    d.line([(MX, fy), (W - MX, fy)], fill=HAIR, width=2)
    fy += 24
    gf = _font("Poppins-ExtraBold.ttf", 240)
    d.text((W - MX - d.textlength(f"{idx + 1:02d}", font=gf), H - 368),
           f"{idx + 1:02d}", font=gf, fill=GHOST)
    f_pen = _font("Poppins-SemiBold.ttf", 42)
    f_cocok_lbl = _font("Poppins-Bold.ttf", 44)
    f_cocok = _font("Poppins-SemiBold.ttf", 42)
    cocok_lines = wrap(d, repo["cocok"], f_cocok, W - 2 * MX)
    cocok_h = 56 + len(cocok_lines) * 56 + 20
    pen_lines = wrap(d, repo["desc"], f_pen, W - 2 * MX)
    max_pen = max(1, (1930 - fy - cocok_h) // 56)
    if len(pen_lines) > max_pen:
        pen_lines = pen_lines[:max_pen]
        pen_lines[-1] = pen_lines[-1].rsplit(" ", 1)[0] + "…"
    for line in pen_lines:
        d.text((MX, fy), line, font=f_pen, fill=(51, 51, 51))
        fy += 56
    fy += 20
    d.text((MX, fy), "COCOK BUAT:", font=f_cocok_lbl, fill=INK)
    fy += 56
    for line in cocok_lines:
        d.text((MX, fy), line, font=f_cocok, fill=(51, 51, 51))
        fy += 56
    footer(d, page, total)
    return img


def closing(spec):
    agent = spec["agent"].upper()
    nxt = spec["next"]
    total = len(spec["repos"]) + 3
    img, d = base(total - 1)
    ep = spec.get("episode")
    kick = f"PENUTUP // SPILL REPO {agent}"
    if ep:
        kick = f"PENUTUP // SPILL REPO {agent} // EDISI #{int(ep):02d}"
    d.text((X(70), X(168)), kick, font=mono(26), fill=GRY)
    tf = f(80)
    d.text((X(70), X(210)), "UDAH,", font=tf, fill=INK)
    highlight(d, X(70), X(302), "ITU DULU.", tf)
    lines = [
        ("Link lengkap semua repo di atas aku spill di komentar postingan ini.", True),
        (f"Besok giliran repo skill {nxt}.", True),
        ("Follow @peka.ai.id biar nggak ketinggalan spill berikutnya.", False),
        ("Save postingan ini buat stok.", False),
    ]
    ly = 452
    for text, _ in lines:
        for ln in wrap(d, text, f(32, False), X(930)):
            d.text((X(70), X(ly)), ln, font=f(32, False), fill=DESC)
            ly += 46
        ly += 22
    footer(d, total - 1, total)
    return img


def follow(spec):
    """Closing CTA slide (standing rule 2026-10-25): follow + community."""
    total = len(spec["repos"]) + 3
    img, d = base(total)
    d.text((X(70), X(168)), "IKUTI PEKA AI", font=mono(26), fill=GRY)
    tf = f(80)
    d.text((X(70), X(210)), "FOLLOW", font=tf, fill=INK)
    highlight(d, X(70), X(302), "DAN GABUNG.", tf)
    lines = [
        "Follow @peka.ai.id di Instagram, Threads, dan TikTok.",
        "Gabung grup WhatsApp Peka AI lewat url.peka.ai.id.",
        "Save dan share postingan ini buat stok.",
    ]
    ly = 452
    for text in lines:
        for ln in wrap(d, text, f(32, False), X(930)):
            d.text((X(70), X(ly)), ln, font=f(32, False), fill=DESC)
            ly += 46
        ly += 22
    footer(d, total, total)
    return img


def main():
    with open(sys.argv[1]) as fh:
        spec = json.load(fh)
    out = spec["out_dir"]
    os.makedirs(out, exist_ok=True)
    cover(spec).save(os.path.join(out, "repo-01.png"))
    for i, repo in enumerate(spec["repos"]):
        repo_slide(spec, i, repo).save(os.path.join(out, f"repo-{i + 2:02d}.png"))
    closing(spec).save(os.path.join(out, f"repo-{len(spec['repos']) + 2:02d}.png"))
    follow(spec).save(os.path.join(out, f"repo-{len(spec['repos']) + 3:02d}.png"))
    print("done:", sorted(os.listdir(out)))


if __name__ == "__main__":
    main()
