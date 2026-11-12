#!/usr/bin/env python3
"""Post the prepared Bansos Freestyle VPS edition.

Usage: python3 post_freestyle.py
Run from an interactive chat session so approval cards surface.
Idempotent: completed steps are recorded in post-done.txt and skipped
on re-run, so a timed-out command that actually posted is never repeated.
Order: Threads root carousel + 2 chained replies, IG reel, FB reel.
Then resolve URLs, write the blog JSON (keeping links.source), write
post-log.txt and append to bansos/posted.log + posted.log.
Exits non-zero on the first failed step.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

OUT = Path("/home/hatch/workspace/peka-content/bansos/out/2026-11-13-freestyle")
PC = Path("/home/hatch/workspace/peka-content")
SLUG = "freestyle-vps-gratis-buat-ai-agent"
DATE = "2026-11-13"
SHORT = "https://s.peka.ai.id/geSjOs"
THR = "17841417164011141"
IG = "17841426380826261"
FB = "1399217353266190"
DONE_FILE = OUT / "post-done.txt"


def done_markers():
    if DONE_FILE.exists():
        return set(DONE_FILE.read_text().splitlines())
    return set()


def log(line):
    with DONE_FILE.open("a") as f:
        f.write(line + "\n")
    print(line)


def done_has(prefix):
    return any(m.startswith(prefix) for m in done_markers())


def done_value(prefix):
    for m in done_markers():
        if m.startswith(prefix):
            return m.split(" ", 1)[1] if " " in m else ""
    return ""


def run(cmd, label):
    print(f">>> {label}")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"FAILED {label}\nSTDOUT: {r.stdout}\nSTDERR: {r.stderr}", file=sys.stderr)
        sys.exit(3)
    print(f"<<< {label} OK: {r.stdout.strip()[:300]}")
    return r.stdout.strip()


def read_caption(name):
    return (OUT / name).read_text().strip()


def threads_resolve(post_id):
    out = run(["/opt/hatch/bin/threads-cli", "post", "--account-id", THR,
               "--post-id", post_id], f"THREADS_RESOLVE {post_id}")
    try:
        return json.loads(out)["posts"][0]["url"]
    except (ValueError, KeyError, IndexError, TypeError):
        return post_id


def main():
    for i in range(1, 4):
        assert (OUT / f"bansos-0{i}.png").exists(), f"missing slide {i}"
    assert (OUT / "bansos-reel.mp4").exists(), "missing reel"

    # --- Threads root carousel ---
    if not done_has("THREADS_ROOT_OK"):
        cmd = ["/opt/hatch/bin/threads-cli", "publish-post", "--account-id", THR]
        for i in range(1, 4):
            cmd += ["--media-item", json.dumps({"file": str(OUT / f"bansos-0{i}.png")})]
        cmd += ["--text", read_caption("caption-threads.txt")]
        out = run(cmd, "THREADS_ROOT")
        root_id = json.loads(out)["post_id"]
        root_url = threads_resolve(root_id)
        log(f"THREADS_ROOT_OK {root_url}")
        log(f"THREADS_ROOT_ID {root_id}")
    else:
        root_id = done_value("THREADS_ROOT_ID")
        root_url = done_value("THREADS_ROOT_OK")

    # --- Threads replies 1-2, chained ---
    parent = root_id
    for i in range(1, 3):
        key = f"THREADS_REPLY_{i}_OK"
        if done_has(key):
            parent = done_value(f"THREADS_REPLY_{i}_ID")
            continue
        cmd = ["/opt/hatch/bin/threads-cli", "publish-post", "--account-id", THR,
               "--text", read_caption(f"caption-threads-reply-{i}.txt"),
               "--reply-to-post-fbid", parent]
        out = run(cmd, f"THREADS_REPLY_{i}")
        rid = json.loads(out)["post_id"]
        rurl = threads_resolve(rid)
        log(f"{key} {rurl}")
        log(f"THREADS_REPLY_{i}_ID {rid}")
        parent = rid

    # --- IG reel ---
    if not done_has("IG_OK"):
        cmd = ["/opt/hatch/bin/instagram-cli", "post-feed", "--account-id", IG,
               "--file", str(OUT / "bansos-reel.mp4"),
               "--cover", str(OUT / "bansos-reel-cover.jpg"),
               "--caption", read_caption("caption-reel-ig.txt")]
        out = run(cmd, "IG_REEL")
        media = json.loads(out).get("media_fbid", "")
        ig_url = ""
        if media:
            uout = run(["/opt/hatch/bin/instagram-cli", "post", "--account-id", IG,
                        "--id", media], "IG_RESOLVE")
            try:
                ig_url = json.loads(uout).get("url", "")
            except ValueError:
                ig_url = ""
        log(f"IG_OK {ig_url or media}")
        log(f"IG_MEDIA {media}")
    else:
        ig_url = done_value("IG_OK")

    # --- FB reel ---
    if not done_has("FB_OK"):
        cmd = ["/opt/hatch/bin/facebook-cli", "pages", "posts", "create",
               "--page-id", FB, "--privacy", "PUBLIC",
               "--text", read_caption("caption-reel-fb.txt"),
               "--file", str(OUT / "bansos-reel.mp4")]
        out = run(cmd, "FB_REEL")
        data = json.loads(out)
        pid = data.get("post_id", "")
        fb_url = data.get("post_url", "")
        if pid and not fb_url:
            rout = run(["/opt/hatch/bin/facebook-cli", "post", "read",
                        "--post-id", pid], "FB_RESOLVE")
            try:
                fb_url = json.loads(rout).get("url", "")
            except ValueError:
                fb_url = ""
        log(f"FB_OK {fb_url or pid}")
        log(f"FB_POST_ID {pid}")
    else:
        fb_url = done_value("FB_OK")

    # --- Blog + images (keep links.source = shortlink) ---
    for i in range(1, 4):
        dst = f"{SLUG}.png" if i == 1 else f"{SLUG}-{i}.png"
        shutil.copy(OUT / f"bansos-0{i}.png", PC / "images" / dst)
    blog = json.loads((OUT / "blog-draft.json").read_text())
    blog["links"] = {"threads": root_url, "facebook": fb_url,
                     "instagram": ig_url, "source": SHORT}
    (PC / "blog" / f"{SLUG}.json").write_text(
        json.dumps(blog, indent=2, ensure_ascii=False))
    print(f"blog: https://blog.peka.ai.id/p/{SLUG}")

    # --- Logs (append once only) ---
    if not done_has("LOGS_OK"):
        with open(PC / "bansos" / "posted.log", "a") as f:
            f.write(f"{DATE}|bansos|{SLUG}|{SHORT}\n")
        with open(PC / "posted.log", "a") as f:
            f.write(f"{DATE} 18:00|bansos|{SLUG}\n")
        log("LOGS_OK")
    with (OUT / "post-log.txt").open("w") as f:
        f.write(f"threads: {root_url}\n")
        f.write(f"instagram: {ig_url}\n")
        f.write(f"facebook: {fb_url}\n")
        f.write(f"shortlink: {SHORT}\n")
        f.write(f"blog: https://blog.peka.ai.id/p/{SLUG}\n")
    print("DONE")


if __name__ == "__main__":
    main()
