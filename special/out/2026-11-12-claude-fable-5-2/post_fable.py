#!/usr/bin/env python3
"""Post the special Claude Fable 5.2 edition (carousel) to Threads, IG, FB.

Usage: python3 post_fable.py
Run from an interactive chat session so approval cards surface.
Idempotent: completed steps are recorded in post-done.txt and skipped
on re-run, so a timed-out command that actually posted is never repeated.
Order: Threads root + 4 chained replies, IG carousel, FB carousel.
Then resolve URLs, patch the blog JSON links, write post-log.txt.
Exits non-zero on the first failed step.
"""
import json
import subprocess
import sys
from pathlib import Path

OUT = Path("/home/hatch/workspace/peka-content/special/out/2026-11-12-claude-fable-5-2")
BLOG_JSON = Path("/home/hatch/workspace/peka-content/blog/claude-fable-5-2-benchmark-coding-terbaru.json")
SLIDES = [OUT / f"slide-{i}.png" for i in range(1, 7)]
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
    print(f">>> {label}: {' '.join(cmd[:4])} ...")
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
    for s in SLIDES:
        assert s.exists(), f"missing slide {s}"

    # --- Threads root carousel ---
    if not done_has("THREADS_ROOT_OK"):
        cmd = ["/opt/hatch/bin/threads-cli", "publish-post", "--account-id", THR]
        for s in SLIDES:
            cmd += ["--media-item", json.dumps({"file": str(s)})]
        cmd += ["--text", read_caption("caption-threads.txt")]
        out = run(cmd, "THREADS_ROOT")
        root_id = json.loads(out)["post_id"]
        root_url = threads_resolve(root_id)
        log(f"THREADS_ROOT_OK {root_url}")
        log(f"THREADS_ROOT_ID {root_id}")
    else:
        root_id = done_value("THREADS_ROOT_ID")
        root_url = done_value("THREADS_ROOT_OK")

    # --- Threads replies 1-4, chained ---
    parent = root_id
    for i in range(1, 5):
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

    # --- IG carousel ---
    if not done_has("IG_OK"):
        cmd = ["/opt/hatch/bin/instagram-cli", "post-feed", "--account-id", IG]
        for s in SLIDES:
            cmd += ["--file", str(s)]
        cmd += ["--caption", read_caption("caption-ig.txt")]
        out = run(cmd, "IG_CAROUSEL")
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

    # --- FB carousel ---
    if not done_has("FB_OK"):
        cmd = ["/opt/hatch/bin/facebook-cli", "pages", "posts", "create",
               "--page-id", FB, "--text", read_caption("caption-fb.txt"),
               "--privacy", "PUBLIC"]
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

    # --- Patch blog JSON links ---
    blog = json.loads(BLOG_JSON.read_text())
    links = blog.get("links", {}) or {}
    links["threads"] = root_url
    links["instagram"] = ig_url
    links["facebook"] = fb_url
    blog["links"] = links
    BLOG_JSON.write_text(json.dumps(blog, indent=2, ensure_ascii=False))
    print(f"blog patched: https://blog.peka.ai.id/p/claude-fable-5-2-benchmark-coding-terbaru")

    short = json.loads((OUT / "shortlinks.json").read_text())
    code = short.get("code", "y3ZY2I")
    with (OUT / "post-log.txt").open("w") as f:
        f.write(f"threads: {root_url}\n")
        f.write(f"instagram: {ig_url}\n")
        f.write(f"facebook: {fb_url}\n")
        f.write(f"shortlink: https://s.peka.ai.id/{code}\n")
        f.write("blog: https://blog.peka.ai.id/p/claude-fable-5-2-benchmark-coding-terbaru\n")
    with open("/home/hatch/workspace/peka-content/special/posted.log", "a") as f:
        f.write(f"2026-11-12|special|claude-fable-5-2|https://s.peka.ai.id/{code}\n")
    print("DONE")


if __name__ == "__main__":
    main()
