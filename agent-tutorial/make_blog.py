#!/usr/bin/env python3
"""Build the Peka blog JSON for a Tutorial Agent Peka edition.

Usage:
  python3 make_blog.py <out_dir> [--instagram URL] [--threads URL]
                                 [--facebook URL] [--local]

Reads <out_dir>/spec.json (slug, title, date, excerpt, tags, faq) and
<out_dir>/article-body.html, writes the blog JSON and copies the reel
cover (<slug>-cover.jpg) plus the carousel slides into
~/workspace/peka-content/images/ as the blog gallery.
The Peka blog app reads the blog JSON dir on every request, so no
restart is needed. Prints the live blog URL on success.

Modes:
  default: writes ~/workspace/peka-content/blog/<slug>.json and backs
    the edition up to ~/workspace/backups/peka-blog-agent/<slug>/
    (blog JSON + spec.json), because peka-content/blog/ is gitignored
    and no backup covers it.
  --local (dry-run / sample): writes <out_dir>/<slug>.json only, no
    images copy, no backup, nothing leaves the out dir.

Slug: the edition slug, unchanged unless it collides with an existing
blog JSON (then spec must carry a different slug and say so).
"""
import json
import os
import shutil
import sys
from datetime import datetime, timezone, timedelta

BLOG_DIR = "/home/hatch/workspace/peka-content/blog"
IMG_DIR = "/home/hatch/workspace/peka-content/images"
BACKUP_ROOT = "/home/hatch/workspace/backups/peka-blog-agent"


def main():
    out_dir = sys.argv[1]
    local = "--local" in sys.argv
    links = {"instagram": "", "threads": "", "facebook": ""}
    args = [a for a in sys.argv[2:] if a != "--local"]
    for i in range(0, len(args) - 1, 2):
        key = args[i].lstrip("-")
        if key in links:
            links[key] = args[i + 1]

    with open(os.path.join(out_dir, "spec.json"), encoding="utf-8") as fh:
        spec = json.load(fh)
    with open(os.path.join(out_dir, "article-body.html"), encoding="utf-8") as fh:
        body = fh.read().strip()

    slug = spec["slug"]
    date = spec["date"]
    wib = datetime.now(timezone(timedelta(hours=7)))
    dt = wib.strftime("%Y-%m-%d %H:%M")

    # FAQ section rendered from spec (same shape as other Peka blog posts)
    faq = spec.get("faq", [])
    if faq:
        parts = ['<h2>Pertanyaan yang Sering Muncul</h2>']
        for q, a in faq:
            parts.append(f"<p><strong>{q}</strong> {a}</p>")
        body = body + "\n\n" + "\n".join(parts)

    cover = slug + "-cover.jpg"
    images = [cover]
    for i in range(1, 7):
        name = f"slide-{i}.png"
        if os.path.exists(os.path.join(out_dir, name)):
            images.append(f"{slug}-slide-{i}.png")

    post = {
        "slug": slug,
        "title": spec["title"],
        "date": date,
        "datetime": dt,
        "excerpt": spec["excerpt"],
        "image": cover,
        "images": images,
        "body_html": body,
        "tags": spec["tags"],
        "links": links,
    }

    # hard guard: no em-dash / en-dash anywhere
    blob = json.dumps(post, ensure_ascii=False)
    assert "\u2014" not in blob and "\u2013" not in blob, "dash terlarang ditemukan"

    if local:
        blog_path = os.path.join(out_dir, slug + ".json")
        with open(blog_path, "w", encoding="utf-8") as fh:
            json.dump(post, fh, ensure_ascii=False, indent=2)
        print(f"blog JSON (local only, tidak dipublish): {blog_path}")
        return

    os.makedirs(BLOG_DIR, exist_ok=True)
    blog_path = os.path.join(BLOG_DIR, slug + ".json")
    assert not os.path.exists(blog_path), f"slug tabrakan: {blog_path} sudah ada"
    with open(blog_path, "w", encoding="utf-8") as fh:
        json.dump(post, fh, ensure_ascii=False, indent=2)

    os.makedirs(IMG_DIR, exist_ok=True)
    shutil.copy(os.path.join(out_dir, cover), os.path.join(IMG_DIR, cover))
    for i in range(1, 7):
        src = os.path.join(out_dir, f"slide-{i}.png")
        if os.path.exists(src):
            shutil.copy(src, os.path.join(IMG_DIR, f"{slug}-slide-{i}.png"))

    # per-edition backup (blog JSON is gitignored, nothing else backs it up)
    backup_dir = os.path.join(BACKUP_ROOT, slug)
    os.makedirs(backup_dir, exist_ok=True)
    shutil.copy(blog_path, os.path.join(backup_dir, slug + ".json"))
    shutil.copy(os.path.join(out_dir, "spec.json"),
                os.path.join(backup_dir, "spec.json"))

    print(f"blog written: {slug}")
    print(f"https://blog.peka.ai.id/p/{slug}")
    print(f"backup: {backup_dir}")


if __name__ == "__main__":
    main()
