#!/usr/bin/env python3
"""Cindy special spotlight: 6 slides, SPILL paper design system.

Thin modification of the locked SPILL format for a single-product
spotlight (not a numbered edition; series.txt / posted.log untouched).
Reuses spill.py primitives + repo_header from spill_repo_carousel.py.
All copy verified against the repo README (2026-10-31).
"""
import json
import os
import sys
import urllib.request

sys.path.insert(0, "/home/hatch/workspace/peka-content/spill")
from PIL import Image, ImageDraw
from spill import PAPER, INK, DESC, GRY, HAIR, X, f, mono, base, footer, highlight, wrap
from spill_repo_carousel import repo_header, _font, _mono, GHOST

OUT = "/home/hatch/workspace/peka-content/spill/out/2026-10-31-cindy-spesial/carousel"
TOTAL = 6
SPEC = {"agent": "CINDY", "repos": [None] * 4}
MX = 308
W = H = 4096


def live_stars():
    try:
        req = urllib.request.Request(
            "https://api.github.com/repos/makecindy/cindy",
            headers={"User-Agent": "peka-spill-carousel"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.load(resp)
        n = int(data.get("stargazers_count") or 8706)
    except Exception as exc:
        print(f"warn: GitHub API failed: {exc} (fallback 8706)")
        n = 8706
    return f"{n / 1000:.1f}".replace(".", ",") + "RB"


def cover(stars):
    img, d = base(1)
    d.text((X(70), X(170)), "SPILL REPO // SPESIAL", font=mono(26), fill=GRY)
    tf = f(96)
    d.text((X(70), X(214)), "AI AGENT", font=tf, fill=INK)
    highlight(d, X(70), X(330), "CINDY", tf)
    sub = ("AI agent open source yang kerja di semua perangkatmu. "
           "Komputermu jadi servernya, tanpa sewa server.")
    sy = 478
    for ln in wrap(d, sub, f(30, False), X(930)):
        d.text((X(70), X(sy)), ln, font=f(30, False), fill=DESC)
        sy += 42
    gt = "Geser, dibedah satu satu >>>"
    d.text((X(1010) - d.textlength(gt, font=mono(26)), X(560)), gt,
           font=mono(26), fill=INK)
    cy = 606
    d.rectangle([X(70), X(cy), X(1010), X(cy + 62)], fill=INK)
    d.text((X(94), X(cy + 15)), "makecindy/cindy", font=f(27), fill="#ffffff")
    st = f"{stars} STAR"
    d.text((X(986) - d.textlength(st, font=f(24)), X(cy + 18)), st,
           font=f(24), fill="#ffd60a")
    facts = "Gratis, Apache-2.0, macOS, Windows, Linux, iOS, Android"
    d.text((X(70), X(cy + 92)), facts, font=f(26, False), fill=DESC)
    footer(d, 1, TOTAL)
    return img


def content_slide(page, idx, kick, headline, body):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    repo_header(img, d, SPEC, idx)
    d.text((MX, 880), kick, font=_mono(84), fill=GRY)
    hf = _font("Poppins-ExtraBold.ttf", 300)
    y = 1000
    for ln in headline:
        d.text((MX, y), ln, font=hf, fill=INK)
        y += 340
    d.line([(MX, 1800), (W - MX, 1800)], fill=HAIR, width=4)
    gf = _font("Poppins-ExtraBold.ttf", 480)
    ghost = f"{idx + 1:02d}"
    d.text((W - MX - d.textlength(ghost, font=gf), H - 736), ghost,
           font=gf, fill=GHOST)
    bf = _font("Poppins-SemiBold.ttf", 84)
    fy = 1900
    for ln in wrap(d, body, bf, W - 2 * MX):
        d.text((MX, fy), ln, font=bf, fill=(51, 51, 51))
        fy += 112
    footer(d, page, TOTAL)
    return img


def follow_slide():
    img, d = base(TOTAL)
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
    footer(d, TOTAL, TOTAL)
    return img


def main():
    os.makedirs(OUT, exist_ok=True)
    stars = live_stars()
    print("stars:", stars)
    slides = [
        cover(stars),
        content_slide(2, 0, "01 // SEMUA PERANGKAT",
                      ["SATU SESSION,", "SEMUA PERANGKAT."],
                      "Buka session yang sama dari laptop, desktop, atau HP. "
                      "Percakapan dan file-nya nyambung, tanpa disalin ke chat baru. "
                      "Dari HP pun kamu bisa buka remote desktop dan mengoperasikan "
                      "komputermu kalo chat saja nggak cukup."),
        content_slide(3, 1, "02 // HARNESS",
                      ["AGENT FAVORITMU,", "SATU TEMPAT."],
                      "Claude Code, Codex, sama Pi jalan bareng dalam satu tampilan. "
                      "Ganti harness sesuai kerjaan, session-nya tetap di Cindy. "
                      "Kalo satu agent nggak cukup, Cindy bisa memimpin tim: ada yang "
                      "merencanakan, ada yang mengerjakan paralel, ada yang mereview."),
        content_slide(4, 2, "03 // TOOL ASLI",
                      ["KERJA BENERAN,", "DI TOOL ASLIMU."],
                      "Kerja langsung di file, browser, sama aplikasimu. Jawabannya "
                      "bisa berupa chart, kontrol interaktif, sama HTML, bukan cuma teks. "
                      "Bikin rutinitas berulang dengan automasi, atau serahkan kerjaan "
                      "lewat Slack sama Telegram. Kemampuan baru datang dari Skills, "
                      "plugin, sama MCP."),
        content_slide(5, 3, "04 // MULAI GRATIS",
                      ["MULAI DARI YANG", "UDAH KAMU PUNYA."],
                      "Client-nya gratis. Pakai langganan Claude Code atau Codex yang "
                      "udah kamu bayar, sambungkan API key sendiri, atau pakai model lokal. "
                      "Download di cindy.app. Billing sama batas dari provider tetap "
                      "berlaku, ya."),
        follow_slide(),
    ]
    for i, img in enumerate(slides, 1):
        path = os.path.join(OUT, f"cindy-{i:02d}.png")
        img.save(path)
        print("saved", path, img.size)


if __name__ == "__main__":
    main()
