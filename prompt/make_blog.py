#!/usr/bin/env python3
"""Build the blog JSON for a Prompt Harian edition.

Usage:
  python3 make_blog.py <out_dir> [--instagram URL] [--threads URL] [--facebook URL]

Reads <out_dir>/spec.json (episode, category, title, prompt, tips), writes
~/workspace/peka-content/blog/<slug>.json and copies the two carousel slides
to ~/workspace/peka-content/images/ as <slug>.png and <slug>-2.png.
The Peka blog app reads the blog JSON dir on every request, so no restart
is needed. Prints the live blog URL on success.

Slug: prompt-harian-<NN>-<slugified title>.
"""
import json
import os
import re
import shutil
import sys
from datetime import datetime, timezone, timedelta

BLOG_DIR = "/home/hatch/workspace/peka-content/blog"
IMG_DIR = "/home/hatch/workspace/peka-content/images"


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def main():
    out_dir = sys.argv[1]
    links = {"instagram": "", "threads": "", "facebook": ""}
    args = sys.argv[2:]
    for i in range(0, len(args) - 1, 2):
        key = args[i].lstrip("-")
        if key in links:
            links[key] = args[i + 1]

    with open(os.path.join(out_dir, "spec.json"), encoding="utf-8") as fh:
        spec = json.load(fh)

    episode = spec["episode"]
    category = spec["category"]
    title = spec["title"]
    prompt = spec["prompt"]
    tips = spec["tips"]
    date = os.path.basename(os.path.normpath(out_dir))

    slug = f"prompt-harian-{episode}-{slugify(title)}"
    wib = datetime.now(timezone(timedelta(hours=7)))
    dt = wib.strftime("%Y-%m-%d %H:%M")

    excerpt = (
        f"Prompt Harian #{episode}: salin prompt ini buat {title.lower()}. "
        "Tempel ke AI favoritmu, langsung dapat hasilnya, tinggal dipakai."
    )

    tips_html = "".join(f"<li>{t}</li>" for t in tips)
    body = f"""
<p>Bikin konten itu gampang-gampang susah. Idenya ada, tapi begitu mau nulis, bingung mulai dari mana. Prompt edisi hari ini beresin itu: satu prompt, tempel ke AI favoritmu, langsung dapat hasilnya, tinggal dipakai.</p>
<p>Prompt Harian #{episode} ini buat {title.lower()}. Cocok buat kamu yang lagi kejar konten tapi tidak mau buang waktu nulis dari nol.</p>

<h2>Promptnya, tinggal salin</h2>
<pre>{prompt}</pre>

<h2>Cara pakainya</h2>
<p>Prompt di atas punya dua bagian dalam kurung siku yang wajib kamu ganti. Isi [TOPIK] dengan satu topik spesifik, jangan topik umum. Misalnya "cara hemat kuota internet", bukan cuma "tips internet". Terus isi [PLATFORM] dengan tempat kamu mau posting, misalnya Reels, TikTok, atau Shorts.</p>
<p>Semakin spesifik topiknya, semakin nyambung hasilnya sama yang kamu mau. Kalau hasilnya masih terlalu umum, tambahin satu kalimat konteks di akhir prompt, misalnya siapa penontonnya atau gaya bahasa yang kamu mau.</p>

<h2>3 tips biar hasilnya maksimal</h2>
<ul>
{tips_html}
</ul>

<h2>Penutup</h2>
<p>Prompt Harian tayang tiap hari jam 12.30 WIB di Instagram, Threads, dan Facebook Peka. Follow @peka.ai.id biar tidak ketinggalan, dan simpan artikel ini buat dipakai lagi pas butuh.</p>
""".strip()

    post = {
        "slug": slug,
        "title": f"Prompt Harian #{episode}: {title}",
        "date": date,
        "datetime": dt,
        "excerpt": excerpt,
        "image": slug + ".png",
        "images": [slug + ".png", slug + "-2.png"],
        "body_html": body,
        "tags": ["Prompt AI", category.title(), "AI"],
        "links": links,
    }

    # hard guard: no em-dash / en-dash anywhere
    blob = json.dumps(post, ensure_ascii=False)
    assert "\u2014" not in blob and "\u2013" not in blob, "dash terlarang ditemukan"

    os.makedirs(BLOG_DIR, exist_ok=True)
    with open(os.path.join(BLOG_DIR, slug + ".json"), "w", encoding="utf-8") as fh:
        json.dump(post, fh, ensure_ascii=False, indent=2)

    shutil.copy(
        os.path.join(out_dir, "prompt-01.png"),
        os.path.join(IMG_DIR, slug + ".png"),
    )
    shutil.copy(
        os.path.join(out_dir, "prompt-02.png"),
        os.path.join(IMG_DIR, slug + "-2.png"),
    )

    print(f"blog written: {slug}")
    print(f"https://blog.peka.ai.id/p/{slug}")


if __name__ == "__main__":
    main()
