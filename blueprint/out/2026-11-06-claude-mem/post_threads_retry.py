#!/usr/bin/env python3
"""Retry the BLUEPRINT #02 (thedotmack/claude-mem) Threads carousel.

Threads-only retry: IG + FB reels already LIVE since 6 Nov 2026, do NOT
re-post them. Idempotent: a marker file records the posted URL + post ID;
a re-run that finds the marker exits 0 without posting again, so a
timed-out command that actually posted is never repeated.

Usage: python3 post_threads_retry.py
Run from a session where the approval card surfaces. Exits non-zero
on the first failed step.
"""
import json
import subprocess
import sys
from pathlib import Path

OUT = Path("/home/hatch/workspace/peka-content/blueprint/out/2026-11-06-claude-mem")
CAROUSEL = OUT / "carousel"
SLIDES = [CAROUSEL / f"blueprint-0{i}.png" for i in range(1, 6)]
CAPTION = OUT / "caption-threads.txt"
DONE_FILE = OUT / "post-threads-done.txt"
THR = "17841417164011141"
CLI = "/opt/hatch/bin/threads-cli"


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


def main():
    for s in SLIDES:
        assert s.exists(), f"missing slide {s}"
    assert CAPTION.exists(), "missing caption-threads.txt"
    text = CAPTION.read_text().strip()
    assert len(text) <= 500, f"Threads caption {len(text)} chars > 500"
    assert "#AI" in text.splitlines()[-1], "closing tag must be #AI"
    assert "http" not in text, "no link allowed in Threads caption"

    if done_has("THREADS_ROOT_OK"):
        print("ALREADY POSTED:", done_value("THREADS_ROOT_OK"))
        print("POST_ID:", done_value("THREADS_ROOT_ID"))
        return

    cmd = [CLI, "publish-post", "--account-id", THR]
    for s in SLIDES:
        cmd += ["--media-item", json.dumps({"file": str(s)})]
    cmd += ["--text", text]
    out = run(cmd, "THREADS_ROOT")
    root_id = json.loads(out)["post_id"]
    out2 = run([CLI, "post", "--account-id", THR, "--post-id", root_id],
               f"THREADS_RESOLVE {root_id}")
    try:
        root_url = json.loads(out2)["posts"][0]["url"]
    except (ValueError, KeyError, IndexError, TypeError):
        root_url = root_id
    log(f"THREADS_ROOT_OK {root_url}")
    log(f"THREADS_ROOT_ID {root_id}")


if __name__ == "__main__":
    main()
