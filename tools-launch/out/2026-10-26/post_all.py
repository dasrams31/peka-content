#!/usr/bin/env python3
"""Post the tools-launch package to IG, Threads, and FB.

Idempotent: each step writes an _OK marker (with its id/url) to
post-log.txt when it succeeds, and a re-run skips steps already marked
OK. A step that failed or was approval-denied has no marker, so a
manual re-run retries only the missing pieces. Never edit captions or
media here; they live next to this script.
"""
import json
import pathlib
import re
import subprocess

BASE = pathlib.Path("/home/hatch/workspace/peka-content/tools-launch/out/2026-10-26")
LOG = BASE / "post-log.txt"
IG = "17841426380826261"
THR = "17841417164011141"
FB = "1399217353266190"


def log(msg):
    print(msg, flush=True)
    with open(LOG, "a", encoding="utf-8") as fh:
        fh.write(msg + "\n")


def done_markers():
    if not LOG.exists():
        return set()
    text = LOG.read_text(encoding="utf-8", errors="replace")
    return set(re.findall(r"^([A-Z_]+_OK)\b", text, flags=re.M))


def read_caption(name):
    return (BASE / name).read_text(encoding="utf-8").strip()


def run(cmd, step):
    log(f"--- {step} ---")
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    except Exception as exc:  # noqa: BLE001 - report and continue
        log(f"ERROR {step}: {exc}")
        return None
    log(f"RC={r.returncode}")
    log("STDOUT: " + r.stdout[-1500:])
    if r.stderr:
        log("STDERR: " + r.stderr[-1500:])
    return r if r.returncode == 0 else None


def find_id(text, keys=("post_id", "id")):
    try:
        data = json.loads(text)
    except (ValueError, TypeError):
        data = None
    if isinstance(data, dict):
        for key in keys:
            if data.get(key):
                return str(data[key])
        posts = data.get("posts")
        if isinstance(posts, list) and posts and posts[0].get("id"):
            return str(posts[0]["id"])
    match = re.search(r'"post_id"\s*:\s*"([^"]+)"', text or "")
    if match:
        return match.group(1)
    match = re.search(r"pfbid[0-9A-Za-z]+", text or "")
    if match:
        return match.group(0)
    return None


def main():
    done = done_markers()
    slides = [str(BASE / f"tools-0{i}.png") for i in range(1, 7)]

    if "IG_CAROUSEL_OK" not in done:
        cmd = ["instagram-cli", "post-feed", "--account-id", IG]
        for f in slides:
            cmd += ["--file", f]
        cmd += ["--caption", read_caption("caption-ig.txt")]
        r = run(cmd, "IG_CAROUSEL")
        if r is not None:
            log("IG_CAROUSEL_OK " + (find_id(r.stdout) or "see stdout"))
    else:
        log("SKIP IG_CAROUSEL (already OK)")

    if "IG_REELS_OK" not in done:
        cmd = ["instagram-cli", "post-feed", "--account-id", IG,
               "--file", str(BASE / "tools-reel.mp4"),
               "--cover", str(BASE / "tools-reel-cover.jpg"),
               "--caption", read_caption("caption-reel-ig.txt")]
        r = run(cmd, "IG_REELS")
        if r is not None:
            log("IG_REELS_OK " + (find_id(r.stdout) or "see stdout"))
    else:
        log("SKIP IG_REELS (already OK)")

    if "THREADS_OK" not in done:
        cmd = ["threads-cli", "publish-post", "--account-id", THR]
        for f in slides:
            cmd += ["--media-item", json.dumps({"file": f})]
        cmd += ["--text", read_caption("caption-threads.txt")]
        r = run(cmd, "THREADS")
        if r is not None:
            pid = find_id(r.stdout)
            if pid:
                rp = run(["threads-cli", "post", "--account-id", THR,
                          "--post-id", pid], "THREADS_RESOLVE")
                if rp is not None:
                    url = None
                    try:
                        url = json.loads(rp.stdout)["posts"][0]["url"]
                    except (ValueError, KeyError, IndexError, TypeError):
                        url = None
                    log("THREADS_OK " + (url or pid))
                else:
                    log("THREADS_OK " + pid + " (url not resolved)")
            else:
                log("THREADS_OK (id not parsed, see stdout)")
    else:
        log("SKIP THREADS (already OK)")

    if "FB_CAROUSEL_OK" not in done:
        cmd = ["facebook-cli", "pages", "posts", "create", "--page-id", FB,
               "--text", read_caption("caption-fb.txt"), "--privacy", "PUBLIC"]
        for f in slides:
            cmd += ["--file", f]
        r = run(cmd, "FB_CAROUSEL")
        if r is not None:
            pid = find_id(r.stdout)
            if pid:
                rp = run(["facebook-cli", "post", "read", "--post-id", pid],
                         "FB_CAROUSEL_RESOLVE")
                if rp is not None:
                    url = None
                    try:
                        url = json.loads(rp.stdout).get("url")
                    except (ValueError, AttributeError):
                        url = None
                    log("FB_CAROUSEL_OK " + (url or pid))
                else:
                    log("FB_CAROUSEL_OK " + pid + " (url not resolved)")
            else:
                log("FB_CAROUSEL_OK (id not parsed, see stdout)")
    else:
        log("SKIP FB_CAROUSEL (already OK)")

    if "FB_REELS_OK" not in done:
        cmd = ["facebook-cli", "pages", "posts", "create", "--page-id", FB,
               "--text", read_caption("caption-reel-fb.txt"), "--privacy", "PUBLIC",
               "--file", str(BASE / "tools-reel.mp4")]
        r = run(cmd, "FB_REELS")
        if r is not None:
            pid = find_id(r.stdout)
            if pid:
                rp = run(["facebook-cli", "post", "read", "--post-id", pid],
                         "FB_REELS_RESOLVE")
                if rp is not None:
                    url = None
                    try:
                        url = json.loads(rp.stdout).get("url")
                    except (ValueError, AttributeError):
                        url = None
                    log("FB_REELS_OK " + (url or pid))
                else:
                    log("FB_REELS_OK " + pid + " (url not resolved)")
            else:
                log("FB_REELS_OK (id not parsed, see stdout)")
    else:
        log("SKIP FB_REELS (already OK)")

    log("DONE")


if __name__ == "__main__":
    main()
