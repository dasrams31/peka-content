"""Peka katalog auto-watch.

Polls ~/workspace/peka-content/katalog/prices.json (the locked single
source of truth for Peka katalog prices) and rebuilds the katalog slides
ONLY when the price list itself changed:

  - product added or removed (by section + name)
  - duration / price / note changed

Stock-count changes do NOT trigger anything here (the katalog never
prints stock). Posting stays with the Tue/Fri 13:00 katalog cron; this
watcher is BUILD-ONLY: fresh slides + story + reel + draft captions are
delivered to chat, never posted.

Usage:
    python3 watch_peka_katalog.py [--dry-run] [--force]

- Normal run: diff prices.json vs auto/snapshot.json, rebuild on change.
  Prints NO_CHANGE or REBUILT <dir> + the change summary.
- --dry-run: diff only, change nothing.
- --force: rebuild regardless of the diff.

Editions go to katalog/auto-<YYYYMMDD-HHMM>/ (a direct child of katalog/
so the template's ../prices.json path resolves). Each edition holds the
slides (4096x4096), story-9x16.png, reel mp4 + cover, draft captions,
CHANGES.md and reel-spec.json. The Tue/Fri cron still owns posted.log,
performance.log and prices.json last_posted — this watcher never touches
them. Captions here are TEMPLATE DRAFTS (price range + order line +
forced-choice close, tag from current_tag.txt); the Tue/Fri cron writes
the final analysed captions when it airs.
"""
import json
import math
import os
import shutil
import subprocess
import sys
from datetime import datetime

KATALOG = "/home/hatch/workspace/peka-content/katalog"
PRICES = os.path.join(KATALOG, "prices.json")
AUTO_DIR = os.path.join(KATALOG, "auto")
SNAPSHOT = os.path.join(AUTO_DIR, "snapshot.json")
TEMPLATE_EDITION = os.path.join(KATALOG, "2026-10-31")
STORY_SOURCE = os.path.join(KATALOG, "2026-11-13", "compose_story.py")
BUILD_SPEC = os.path.join(KATALOG, "build_spec.py")
PICK_TRACK = "/home/hatch/workspace/peka-content/brand/music/pick_reel_track.sh"
CURRENT_TAG = "/home/hatch/workspace/peka-content/tag-watch/current_tag.txt"
MEGUMI_PY = "/home/hatch/workspace/megumi/venv/bin/python"


def run(cmd, cwd=None, capture=False):
    res = subprocess.run(
        cmd, cwd=cwd, check=True, capture_output=capture, text=True
    )
    return res.stdout.strip() if capture else ""


def load_prices():
    with open(PRICES, encoding="utf-8") as f:
        return json.load(f)


def product_key(p):
    # Variants share (sec, name): Wink 7/14 Hari, Viu 1 Tahun/Lifetime,
    # Gemini Pro 3/18 Bulan, and the two Muse Spark AI Lifetime entries
    # (told apart ONLY by note: "3-4 Milyar token" vs "1M Token").
    # dur + note belong in the identity; price does not.
    return (p["sec"], p["name"], p["dur"], p.get("note", ""))


def diff_products(old, new):
    old_by_key = {product_key(p): p for p in old}
    new_by_key = {product_key(p): p for p in new}
    added = [new_by_key[k] for k in new_by_key if k not in old_by_key]
    removed = [old_by_key[k] for k in old_by_key if k not in new_by_key]
    changed = []
    for k in old_by_key:
        if k in new_by_key:
            o, n = old_by_key[k], new_by_key[k]
            if o.get("price") != n.get("price") or \
                    o.get("price_num") != n.get("price_num"):
                changed.append((o, n))
    return added, removed, changed


def short_price(p):
    return p["price"]


def make_captions(products, tag):
    total = len(products)
    lo = min(p["price_num"] for p in products)
    hi = max(p["price_num"] for p in products)
    cheapest = sorted(products, key=lambda p: (p["price_num"], p["name"]))
    hook_bits = [
        f"{p['name']} {p['dur']} {p['price']}" for p in cheapest[:2]
    ]
    hook = ", ".join(hook_bits) + "."
    top3 = cheapest[:3]
    andalan = ", ".join(
        f"{p['name']} {p['dur']} {p['price']}" for p in top3
    )
    andalan = andalan.rsplit(", ", 1)
    andalan = " sama ".join(andalan) if len(andalan) == 2 else andalan[0]
    body = (
        f"{hook}\n\n"
        f"Total {total} akun premium, harganya {lo}K sampai {hi}K, "
        "semua ready hari ini.\n\n"
        f"Andalan edisi ini: {andalan}.\n\n"
        "Save dulu biar nggak hilang. Kamu mau yang mana dulu?\n\n"
        "Chat aja: MAU [nama produk]. Testimoni ada di profil."
    )
    threads = body + f"\n\n#{tag}\n"
    ig = body + f"\n\n#{tag}\n"
    fb = body + "\n"
    wa = (
        f"Katalog Peka hari ini sudah update, {total} produk ready, "
        f"harga {lo}K sampai {hi}K. Andalan: {andalan}. "
        "Mau order? Chat aja: MAU [nama produk]. "
        "Gabung grup: https://url.peka.ai.id\n"
    )
    return {
        "caption-threads.txt": threads,
        "caption-ig.txt": ig,
        "caption-fb.txt": fb,
        "caption-wa.txt": wa,
    }


def write_changes(out_dir, added, removed, changed, total):
    lines = [
        "# Katalog Peka — auto rebuild "
        f"{datetime.now().strftime('%d %b %Y %H:%M')} WIB",
        "",
        "Sumber: `prices.json` (pemicu = list harga berubah).",
        "Build-only: slide + story + reel + caption DRAF diantar ke chat, "
        "TIDAK diposting. Posting tetap lewat cron Selasa/Jumat 13:00.",
        "",
        "## Yang berubah",
        "",
    ]
    for p in added:
        lines.append(
            f"- DITAMBAH: {p['name']} {p['dur']} {p['price']} ({p['sec']})"
        )
    for o, n in changed:
        lines.append(
            f"- BERUBAH: {o['name']} {o['dur']} "
            f"(harga: {o.get('price')} -> {n.get('price')})"
        )
    for p in removed:
        lines.append(
            f"- DIHAPUS: {p['name']} {p['dur']} {p['price']} ({p['sec']})"
        )
    lines += [
        f"- Total: {total} produk.",
        "",
        "## Catatan caption",
        "",
        "Caption di folder ini adalah DRAF template (rentang harga + cara "
        "order + pertanyaan pilihan, tag penutup dari current_tag.txt). "
        "Caption final dengan analisis hook ditulis cron Selasa/Jumat "
        "saat edisi tayang.",
        "",
    ]
    with open(os.path.join(out_dir, "CHANGES.md"), "w") as f:
        f.write("\n".join(lines))


def build(prices, out_dir):
    """Replicate the katalog cron BUILD steps (no posting)."""
    os.makedirs(out_dir, exist_ok=True)
    # 1. Template files from the 2026-10-31 edition.
    shutil.copy(
        os.path.join(TEMPLATE_EDITION, "katalog_slides.py"), out_dir
    )
    shutil.copytree(
        os.path.join(TEMPLATE_EDITION, "animated"),
        os.path.join(out_dir, "animated"),
    )
    shutil.copy(STORY_SOURCE, out_dir)
    # 2. reel-spec.json from the live prices.json.
    run(["python3", BUILD_SPEC, out_dir])
    # 3. Slides 4096x4096 (reads ../prices.json from the edition dir).
    run(["python3", "katalog_slides.py"], cwd=out_dir)
    slides = sorted(
        f for f in os.listdir(out_dir)
        if f.startswith("peka-katalog-") and f.endswith(".png")
    )
    assert len(slides) >= 2, f"expected >=2 slides, got {len(slides)}"
    print(f"slides: {len(slides)} ({slides[0]} .. {slides[-1]})")
    # 4. Music, exactly once.
    track = run(["bash", PICK_TRACK], capture=True)
    with open(os.path.join(out_dir, "track.txt"), "w") as f:
        f.write(track + "\n")
    print(f"track: {track}")
    # 5. Reel render (Playwright, scale 2.0) + encode + cover.
    n = len(prices["products"])
    dur = 3 + 5 * math.ceil(n / 3) + 3
    spec = os.path.join(out_dir, "reel-spec.json")
    frames = os.path.join(out_dir, "animated", "frames")
    run(
        [MEGUMI_PY, "animated/render.py", spec, frames, "24", str(dur), "2.0"],
        cwd=out_dir,
    )
    reel = os.path.join(out_dir, "peka-katalog-reel.mp4")
    run([
        "ffmpeg", "-y", "-threads", "2",
        "-framerate", "24", "-i", os.path.join(frames, "f%04d.png"),
        "-i", track,
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "24",
        "-preset", "veryfast", "-c:a", "aac", "-b:a", "128k",
        "-shortest", "-movflags", "+faststart", reel,
    ])
    run([
        "ffmpeg", "-y", "-i", os.path.join(frames, "f0024.png"),
        "-q:v", "2", os.path.join(out_dir, "peka-katalog-reel-cover.jpg"),
    ])
    probe = run([
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=codec_name,width,height,pix_fmt",
        "-of", "csv=p=0", reel,
    ], capture=True)
    print(f"reel probe: {probe}")
    assert "h264,2160,3840,yuv420p" in probe.replace(" ", ""), \
        f"reel is not 2160x3840 yuv420p h264: {probe}"
    shutil.rmtree(frames)
    # 6. Story 9:16 from the cover slide.
    run(["python3", "compose_story.py"], cwd=out_dir)
    assert os.path.exists(os.path.join(out_dir, "story-9x16.png"))
    # 7. Draft captions.
    with open(CURRENT_TAG, encoding="utf-8") as f:
        tag = f.read().strip()
    captions = make_captions(prices["products"], tag)
    music_name = os.path.splitext(os.path.basename(track))[0]
    music_credit = music_name.replace("-", " ").replace("_", " ").title()
    captions["caption-tiktok.txt"] = (
        captions["caption-threads.txt"].rstrip("\n").rsplit("#", 1)[0].rstrip()
        + f"\n\nMusik: {music_credit}\n"
    )
    for name, text in captions.items():
        with open(os.path.join(out_dir, name), "w") as f:
            f.write(text)
    print(f"captions: {', '.join(sorted(captions))} (draft)")
    return len(slides), dur


def main():
    dry_run = "--dry-run" in sys.argv
    force = "--force" in sys.argv
    prices = load_prices()
    try:
        with open(SNAPSHOT, encoding="utf-8") as f:
            old = json.load(f)
    except FileNotFoundError:
        old = None
    if old is None:
        if dry_run:
            print(
                f"NO_SNAPSHOT: would save baseline of "
                f"{len(prices['products'])} products"
            )
            return 0
        os.makedirs(AUTO_DIR, exist_ok=True)
        with open(SNAPSHOT, "w", encoding="utf-8") as f:
            json.dump(prices, f, ensure_ascii=False, indent=1)
        print(f"BASELINE saved: {len(prices['products'])} products, no rebuild")
        return 0
    added, removed, changed = diff_products(
        old["products"], prices["products"]
    )
    meta_changed = (
        old.get("updated") != prices.get("updated")
        or old.get("date_label") != prices.get("date_label")
    )
    if not added and not removed and not changed and not meta_changed \
            and not force:
        print(
            f"NO_CHANGE: {len(prices['products'])} products, "
            "snapshot up to date"
        )
        return 0
    if dry_run:
        print(
            f"WOULD_REBUILD: +{len(added)} -{len(removed)} ~{len(changed)}"
        )
        for p in added:
            print("  +", p["name"], p["dur"], p["price"])
        for p in removed:
            print("  -", p["name"], p["dur"], p["price"])
        for o, n in changed:
            print("  ~", o["name"], o["price"], "->", n["price"])
        return 0
    stamp = datetime.now().strftime("%Y%m%d-%H%M")
    out_dir = os.path.join(KATALOG, f"auto-{stamp}")
    n_slides, dur = build(prices, out_dir)
    write_changes(
        out_dir, added, removed, changed, len(prices["products"])
    )
    with open(SNAPSHOT, "w", encoding="utf-8") as f:
        json.dump(prices, f, ensure_ascii=False, indent=1)
    print(f"REBUILT {out_dir}")
    for p in added:
        print("  +", p["name"], p["dur"], p["price"])
    for p in removed:
        print("  -", p["name"], p["dur"], p["price"])
    for o, n in changed:
        print("  ~", o["name"], o["price"], "->", n["price"])
    print(f"  total: {len(prices['products'])} products, "
          f"{n_slides} slides, reel {dur}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
