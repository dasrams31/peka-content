#!/usr/bin/env python3
"""Spill-repo carousel: cover + one slide per repo + closing.

Paper spill format (see spill.py). Driven by a JSON spec:
{"agent": "CLAUDE", "next": "Hermes", "date": "2026-10-20",
 "repos": [{"name": "owner/repo", "stars": "182RB",
            "desc": "...", "cocok": "..."}],
 "out_dir": "/abs/dir"}
Slides: 01 cover, 02..N+1 one per repo, last closing.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spill import (DESC, GRY, HAIR, INK, PAPER, X, base, f, footer, highlight,
                   mono, wrap)

GHOST = "#e9dfc6"


def fit_font(d, text, size, max_w, min_size=40):
    tf = f(size)
    while size > min_size and d.textlength(text, font=tf) > max_w:
        size -= 4
        tf = f(size)
    return tf


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
    img, d = base(page)
    # ghost index behind everything else on this slide
    gf = f(230)
    num = f"{idx + 1:02d}"
    d.text((X(1010) - d.textlength(num, font=gf), X(800)), num, font=gf, fill=GHOST)
    owner, name = repo["name"].split("/", 1)
    d.text((X(70), X(164)), f"REPO {idx + 1:02d} DARI {len(spec['repos']):02d} // {agent}",
           font=mono(26), fill=GRY)
    d.text((X(70), X(216)), owner + "/", font=mono(38), fill=GRY)
    nf = fit_font(d, name, 96, X(940))
    d.text((X(70), X(262)), name, font=nf, fill=INK)
    # star chip
    cf = f(26)
    label = f"{repo['stars']} STAR DI GITHUB"
    tw = d.textlength(label, font=cf)
    d.rectangle([X(70), X(392), X(70) + tw + X(44), X(450)], fill=INK)
    asc, des = cf.getmetrics()
    d.text((X(92), X(421) - (asc + des) / 2), label, font=cf, fill="#ffd60a")
    # description
    dy = 506
    for ln in wrap(d, repo["desc"], f(33, False), X(930)):
        d.text((X(70), X(dy)), ln, font=f(33, False), fill=DESC)
        dy += 48
    # cocok block
    cy = dy + 26
    d.line([X(70), X(cy), X(1010), X(cy)], fill=HAIR, width=X(2))
    d.text((X(70), X(cy + 26)), "COCOK BUAT:", font=f(28), fill=INK)
    wy = cy + 70
    for ln in wrap(d, repo["cocok"], f(30, False), X(930)):
        d.text((X(70), X(wy)), ln, font=f(30, False), fill=DESC)
        wy += 42
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
        "Save dan share postingan ini biar makin banyak yang kebantu.",
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
