#!/usr/bin/env python3
"""Post the prepared Katalog Peka 2026-11-13 edition (edisi #5).

Usage: python3 post_katalog.py
Run from an interactive chat session so approval cards surface.
Idempotent: completed steps are recorded in post-done.txt and skipped
on re-run, so a timed-out command that actually posted is never repeated.
Order: Threads carousel, IG carousel, FB carousel, IG Story.
Exits non-zero on the first failed step.
"""
import json
import subprocess
import sys
from pathlib import Path

OUT = Path("/home/hatch/workspace/peka-content/katalog/2026-11-13")
THR = "17841417164011141"
IG = "17841426380826261"
FB = "1399217353266190"
DONE_FILE = OUT / "post-done.txt"
SLIDES = [OUT / f"peka-katalog-0{i}.png" for i in range(1, 8)]


def done_markers():
    if DONE_FILE.exists():
        return set(DONE_FILE.read_text().splitlines())
    return set()


def log(line):
    with DONE_FILE.open("a") as f:
        f.write(line + "\n")
    print(line, flush=True)


def done_has(prefix):
    return any(m.startswith(prefix) for m in done_markers())


def done_value(prefix):
    for m in done_markers():
        if m.startswith(prefix):
            return m.split(" ", 1)[1] if " " in m else ""
    return ""


def run(cmd, label):
    print(f">>> {label}", flush=True)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"FAILED {label}\nSTDOUT: {r.stdout}\nSTDERR: {r.stderr}",
              file=sys.stderr)
        sys.exit(3)
    print(f"<<< {label} OK: {r.stdout.strip()[:300]}", flush=True)
    return r.stdout.strip()


def read_caption(name):
    return (OUT / name).read_text().strip()


def main():
    for s in SLIDES:
        assert s.exists(), f"missing slide {s}"
    assert (OUT / "story-9x16.png").exists(), "missing story image"

    # --- Threads carousel ---
    if not done_has("THREADS_OK"):
        cmd = ["/opt/hatch/bin/threads-cli", "publish-post",
               "--account-id", THR]
        for s in SLIDES:
            cmd += ["--media-item", json.dumps({"file": str(s)})]
        cmd += ["--text", read_caption("caption-threads.txt")]
        out = run(cmd, "THREADS_CAROUSEL")
        pid = json.loads(out)["post_id"]
        uout = run(["/opt/hatch/bin/threads-cli", "post",
                    "--account-id", THR, "--post-id", pid],
                   "THREADS_RESOLVE")
        try:
            url = json.loads(uout)["posts"][0]["url"]
        except (ValueError, KeyError, IndexError, TypeError):
            url = pid
        log(f"THREADS_OK {url}")
        log(f"THREADS_POST_ID {pid}")
    else:
        url = done_value("THREADS_OK")

    # --- IG carousel ---
    if not done_has("IG_OK"):
        cmd = ["/opt/hatch/bin/instagram-cli", "post-feed",
               "--account-id", IG]
        for s in SLIDES:
            cmd += ["--file", str(s)]
        cmd += ["--caption", read_caption("caption-ig.txt")]
        out = run(cmd, "IG_CAROUSEL")
        media = json.loads(out).get("media_fbid", "")
        ig_url = ""
        if media:
            uout = run(["/opt/hatch/bin/instagram-cli", "post",
                        "--account-id", IG, "--id", media], "IG_RESOLVE")
            try:
                ig_url = json.loads(uout).get("url", "")
            except ValueError:
                ig_url = ""
        log(f"IG_OK {ig_url or media}")
        log(f"IG_MEDIA {media}")
    else:
        ig_url = done_value("IG_OK")

    # --- FB carousel ---
    if not done_has("FB_OK"):
        cmd = ["/opt/hatch/bin/facebook-cli", "pages", "posts", "create",
               "--page-id", FB, "--privacy", "PUBLIC",
               "--text", read_caption("caption-fb.txt")]
        for s in SLIDES:
            cmd += ["--file", str(s)]
        out = run(cmd, "FB_CAROUSEL")
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

    # --- IG Story (mandatory) ---
    if not done_has("STORY_OK"):
        cmd = ["/opt/hatch/bin/instagram-cli", "post-story",
               "--account-id", IG,
               "--file", str(OUT / "story-9x16.png")]
        out = run(cmd, "IG_STORY")
        media = json.loads(out).get("media_fbid", "")
        story_url = ""
        if media:
            try:
                uout = run(["/opt/hatch/bin/instagram-cli", "post",
                            "--account-id", IG, "--id", media],
                           "STORY_RESOLVE")
                story_url = json.loads(uout).get("url", "")
            except (ValueError, SystemExit):
                story_url = ""
            if not story_url:
                story_url = (
                    f"https://instagram.com/stories/peka.ai.id/{media}")
        log(f"STORY_OK {story_url or media}")
        log(f"STORY_MEDIA {media}")
    else:
        story_url = done_value("STORY_OK")

    print(f"THREADS {url}")
    print(f"IG {ig_url}")
    print(f"FB {fb_url}")
    print(f"STORY {story_url}")
    print("ALL POSTED")


main()
