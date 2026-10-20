#!/usr/bin/env python3
"""Single spill-repo card (paper spill format), driven by a JSON spec.

Usage:
    python3 spill_repo_card.py <spec.json>
    python3 spill_repo_card.py            # built-in Claude spec (2026-10-20)

Spec: {"agent": "CLAUDE", "next": "Hermes", "sub": "...",
       "rows": [{"name": "owner/repo", "desc": "one line"}],
       "out": "/abs/path/card.png"}
Max 5 rows so the layout never overflows the 2048x2048 canvas.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spill import (DESC, GRY, HAIR, INK, YEL, X, base, f, footer, highlight,
                   mono, wrap)

DEFAULT_SPEC = {
    "agent": "CLAUDE",
    "next": "Hermes",
    "sub": "Repo GitHub tempat ambil skill Claude siap pakai, semua sudah terverifikasi.",
    "rows": [
        {"name": "anthropics/skills",
         "desc": "Repo resmi Anthropic: skill dokumen Office + contoh skill standar."},
        {"name": "obra/superpowers",
         "desc": "Framework skill + metodologi ngoding buat Claude Code. 302rb star."},
        {"name": "alirezarezvani/claude-skills",
         "desc": "380+ skill dan plugin Claude Code dalam satu repo."},
        {"name": "kepano/obsidian-skills",
         "desc": "Skill biar agent jago ngurus catatan Obsidian."},
        {"name": "ComposioHQ/awesome-claude-skills",
         "desc": "Daftar kurasi buat berburu skill lainnya."},
    ],
    "out": os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "out", "2026-10-20", "spill-repo-claude.png"),
}


def render(spec):
    agent = spec["agent"].upper()
    rows = spec["rows"][:5]
    img, d = base(1)
    d.text((X(70), X(170)), f"SPILL REPO // HARI INI: {agent}", font=mono(26), fill=GRY)
    title = f"REPO SKILL {agent}"
    size = 88
    tf = f(size)
    while size > 40 and d.textlength(title, font=tf) > X(920):
        size -= 4
        tf = f(size)
    highlight(d, X(70), X(212), title, tf)
    sy = 330
    for ln in wrap(d, spec["sub"], f(29, False), X(930)):
        d.text((X(70), X(sy)), ln, font=f(29, False), fill=DESC)
        sy += 40
    name_f, desc_f, idx_f = f(30), f(27, False), mono(24)
    y = 436
    for i, row in enumerate(rows):
        desc_lines = wrap(d, row["desc"], desc_f, X(882))
        if i > 0:
            d.line([X(70), X(y), X(1010), X(y)], fill=HAIR, width=X(2))
        top = y + 8
        d.text((X(70), X(top + 4)), f"{i + 1:02d}", font=idx_f, fill=GRY)
        d.text((X(128), X(top)), row["name"], font=name_f, fill=INK)
        dy = top + 46
        for ln in desc_lines:
            d.text((X(128), X(dy)), ln, font=desc_f, fill=DESC)
            dy += 35
        y += 8 + 38 + len(desc_lines) * 35 + 8
    if y > 951:
        raise SystemExit(f"layout overflow: table ends at {y} (>951); shorten descs")
    d.rectangle([X(70), X(962), X(1010), X(1014)], fill=INK)
    tf2 = f(25)
    t = f"Save dulu, install belakangan. Besok giliran {spec['next']}."
    while d.textlength(t, font=tf2) > X(880):
        tf2 = f(22)
        break
    tw = d.textlength(t, font=tf2)
    asc, des = tf2.getmetrics()
    d.text((X(540) - tw / 2, X(988) - (asc + des) / 2), t, font=tf2, fill=YEL)
    footer(d, 1, 1)
    os.makedirs(os.path.dirname(spec["out"]), exist_ok=True)
    img.save(spec["out"])
    print("saved", spec["out"], "| table ends at", y)


def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as fh:
            spec = json.load(fh)
    else:
        spec = DEFAULT_SPEC
    render(spec)


if __name__ == "__main__":
    main()
