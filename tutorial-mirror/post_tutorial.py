#!/usr/bin/env python3
"""Post one tutorial-mirror edition to Threads, IG, FB.

Usage: python3 post_tutorial.py <out_dir>
Run from an interactive chat session so approval cards surface.
Idempotent: completed steps are recorded in post-done.txt and skipped
on re-run, so a timed-out command that actually posted is never repeated.
Order: Threads root carousel + chained replies, IG reel, FB reel.
Then resolve URLs, patch the blog JSON links, write post-log.txt.
Exits non-zero on the first failed step.
DO NOT run during a dry-run: this script posts for real.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

THR = "17841417164011141"
IG = "17841426380826261"
FB = "1399217353266190"


def main():
    out = Path(sys.argv[1])
    spec = json.loads((out / "spec.json").read_text())
    slug = spec["slug"]
    slides = [out / f"slide-{i}.png" for i in range(1, 7)]
    for s in slides:
        assert s.exists(), f"missing slide {s}"
    reel = out / f"{slug}-reel.mp4"
    cover = out / f"{slug}-cover.jpg"
    assert reel.exists(), "missing reel"
    assert cover.exists(), "missing reel cover"
    blog_json = Path(f"/home/hatch/workspace/peka-content/blog/{slug}.json")
    done_file = out / "post-done.txt"

    def done_markers():
        if done_file.exists():
            return set(done_file.read_text().splitlines())
        return set()

    def log(line):
        with done_file.open("a") as f:
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
        print(f">>> {label}", flush=True)
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print(f"FAILED {label}\nSTDOUT: {r.stdout}\nSTDERR: {r.stderr}",
                  file=sys.stderr)
            sys.exit(3)
        print(f"<<< {label} OK: {r.stdout.strip()[:300]}")
        return r.stdout.strip()

    def read_caption(name):
        return (out / name).read_text().strip()

    def threads_resolve(post_id):
        res = run(["/opt/hatch/bin/threads-cli", "post", "--account-id", THR,
                   "--post-id", post_id], f"THREADS_RESOLVE {post_id}")
        try:
            return json.loads(res)["posts"][0]["url"]
        except (ValueError, KeyError, IndexError, TypeError):
            return post_id

    # --- Threads root carousel ---
    if not done_has("THREADS_ROOT_OK"):
        cmd = ["/opt/hatch/bin/threads-cli", "publish-post", "--account-id", THR]
        for s in slides:
            cmd += ["--media-item", json.dumps({"file": str(s)})]
        cmd += ["--text", read_caption("caption-threads.txt")]
        res = run(cmd, "THREADS_ROOT")
        root_id = json.loads(res)["post_id"]
        root_url = threads_resolve(root_id)
        log(f"THREADS_ROOT_OK {root_url}")
        log(f"THREADS_ROOT_ID {root_id}")
    else:
        root_id = done_value("THREADS_ROOT_ID")
        root_url = done_value("THREADS_ROOT_OK")

    # --- Threads replies, chained (only files that exist) ---
    parent = root_id
    i = 1
    while (out / f"caption-threads-reply-{i}.txt").exists():
        key = f"THREADS_REPLY_{i}_OK"
        if done_has(key):
            parent = done_value(f"THREADS_REPLY_{i}_ID")
            i += 1
            continue
        cmd = ["/opt/hatch/bin/threads-cli", "publish-post", "--account-id", THR,
               "--text", read_caption(f"caption-threads-reply-{i}.txt"),
               "--reply-to-post-fbid", parent]
        res = run(cmd, f"THREADS_REPLY_{i}")
        rid = json.loads(res)["post_id"]
        rurl = threads_resolve(rid)
        log(f"{key} {rurl}")
        log(f"THREADS_REPLY_{i}_ID {rid}")
        parent = rid
        i += 1

    # --- IG reel ---
    if not done_has("IG_OK"):
        cmd = ["/opt/hatch/bin/instagram-cli", "post-feed", "--account-id", IG,
               "--file", str(reel), "--cover", str(cover),
               "--caption", read_caption("caption-reel-ig.txt")]
        res = run(cmd, "IG_REEL")
        media = json.loads(res).get("media_fbid", "")
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
               "--page-id", FB, "--text", read_caption("caption-reel-fb.txt"),
               "--privacy", "PUBLIC", "--file", str(reel)]
        res = run(cmd, "FB_REEL")
        data = json.loads(res)
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
    blog = json.loads(blog_json.read_text())
    links = blog.get("links", {}) or {}
    links["threads"] = root_url
    links["instagram"] = ig_url
    links["facebook"] = fb_url
    blog["links"] = links
    blog_json.write_text(json.dumps(blog, indent=2, ensure_ascii=False))
    print(f"blog patched: https://blog.peka.ai.id/p/{slug}")

    short = json.loads((out / "shortlinks.json").read_text())
    code = short.get("code", "")
    with (out / "post-log.txt").open("w") as f:
        f.write(f"threads: {root_url}\n")
        f.write(f"instagram: {ig_url}\n")
        f.write(f"facebook: {fb_url}\n")
        f.write(f"shortlink: https://s.peka.ai.id/{code}\n")
        f.write(f"blog: https://blog.peka.ai.id/p/{slug}\n")
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "posted.log"), "a") as f:
        f.write(f"{spec['date']}|tutorial-mirror|{slug}|"
                f"https://s.peka.ai.id/{code}\n")
    print("DONE")


if __name__ == "__main__":
    main()
