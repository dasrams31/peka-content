#!/usr/bin/env python3
"""Post RuteStrip special edition (21 Nov 2026 18:00 WIB).

Idempotent via post-done.txt: each completed step is skipped on re-run.
Order: Threads carousel -> IG carousel -> FB carousel (gate may fail, tolerated)
-> blog links patch -> posted.log -> channel broadcast (type special).
Run with a generous timeout; approval cards pace the CLI calls.
"""
import json
import os
import re
import subprocess
import sys

OUT = os.path.dirname(os.path.abspath(__file__))
CAR = os.path.join(OUT, "carousel")
SLIDES = [os.path.join(CAR, f"slide-0{i}.png") for i in range(1, 7)]
DONE = os.path.join(OUT, "post-done.txt")
BLOG = "/home/hatch/workspace/peka-content/blog/rutestrip-ai-yang-ngerti-gunung.json"
BLOG_URL = "https://blog.peka.ai.id/p/rutestrip-ai-yang-ngerti-gunung"
POSTED_LOG = "/home/hatch/workspace/peka-content/posted.log"

THREADS_ACC = "17841417164011141"
IG_ACC = "17841426380826261"
FB_PAGE = "1399217353266190"


def done_markers():
    if not os.path.exists(DONE):
        return set()
    return set(l.strip() for l in open(DONE) if l.strip())


def mark(line):
    with open(DONE, "a") as f:
        f.write(line + "\n")


def read_caption(name):
    return open(os.path.join(OUT, name)).read().strip()


def run(cmd, timeout, logname):
    print("+", " ".join(cmd), flush=True)
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired as e:
        out = (e.stdout or b"").decode(errors="ignore") if isinstance(e.stdout, bytes) else (e.stdout or "")
        err = (e.stderr or b"").decode(errors="ignore") if isinstance(e.stderr, bytes) else (e.stderr or "")
        with open(os.path.join(OUT, logname), "w") as f:
            f.write(out + "\n" + err)
        return None, out + "\n" + err, "timeout"
    with open(os.path.join(OUT, logname), "w") as f:
        f.write(p.stdout + "\n" + p.stderr)
    return p.returncode, p.stdout + "\n" + p.stderr, "ok"


def extract_url(text, patterns):
    for pat in patterns:
        m = re.search(pat, text)
        if m:
            return m.group(0)
    return ""


def main():
    markers = done_markers()
    links = {"threads": "", "facebook": "", "instagram": ""}
    para = ("Aku tes langsung chatbot RuteStrip: tanya gunung buat pemula "
            "di Jawa Barat, jawabannya Papandayan, cuma 1,79 km dan 1,5 jam, "
            "jalurnya mudah. Chatbotnya juga bisa bikinin checklist logistik, "
            "itinerary 2 hari 1 malam, dan estimasi biaya. Coba sendiri di "
            "slide terakhir.")

    # --- Threads carousel ---
    if "THREADS_OK" not in markers:
        cmd = ["/opt/hatch/bin/threads-cli", "publish-post",
               "--account-id", THREADS_ACC]
        for s in SLIDES:
            cmd += ["--media-item", json.dumps({"file": s})]
        cmd += ["--text", read_caption("caption-threads.txt")]
        rc, out, status = run(cmd, 900, "threads-post.log")
        if status == "timeout" or rc != 0:
            print("THREADS FAILED (rc=%s status=%s); stop here for chat repair" % (rc, status))
            return 3
        post_id = extract_url(out, [r"\b\d{17,20}\b"])
        url = ""
        if post_id:
            rc2, out2, _ = run(["/opt/hatch/bin/threads-cli", "post",
                                "--post-id", post_id,
                                "--account-id", THREADS_ACC], 120, "threads-url-lookup.log")
            url = extract_url(out2, [r"https://www\.threads\.com/[^\"'\s]+",
                                     r"https://www\.threads\.net/[^\"'\s]+"])
            if not url:
                url = "https://www.threads.net/t/" + post_id
        with open(os.path.join(OUT, "threads-url.txt"), "w") as f:
            f.write(url + "\n")
        links["threads"] = url
        mark("THREADS_OK " + url)
        print("THREADS OK", url, flush=True)
    else:
        for line in markers:
            if line.startswith("THREADS_OK "):
                links["threads"] = line.split(" ", 1)[1]

    # --- IG carousel ---
    if "IG_OK" not in markers:
        cmd = ["/opt/hatch/bin/instagram-cli", "post-feed",
               "--account-id", IG_ACC]
        for s in SLIDES:
            cmd += ["--file", s]
        cmd += ["--caption", read_caption("caption-ig.txt")]
        rc, out, status = run(cmd, 900, "ig-post.log")
        if status == "timeout" or rc != 0:
            print("IG FAILED (rc=%s status=%s); stop here for chat repair" % (rc, status))
            return 3
        url = extract_url(out, [r"https://www\.instagram\.com/[^\"'\s]+"])
        with open(os.path.join(OUT, "instagram-url.txt"), "w") as f:
            f.write(url + "\n")
        links["instagram"] = url
        mark("IG_OK " + url)
        print("IG OK", url, flush=True)
    else:
        for line in markers:
            if line.startswith("IG_OK "):
                links["instagram"] = line.split(" ", 1)[1]

    # --- FB carousel (gate known-bad: tolerate failure, continue) ---
    if "FB_OK" not in markers and "FB_FAILED" not in markers:
        cmd = ["/opt/hatch/bin/facebook-cli", "pages", "posts", "create",
               "--page-id", FB_PAGE, "--privacy", "PUBLIC",
               "--text", read_caption("caption-fb.txt")]
        for s in SLIDES:
            cmd += ["--file", s]
        rc, out, status = run(cmd, 300, "fb-post.log")
        if status == "timeout" or rc != 0:
            print("FB FAILED (rc=%s status=%s); continuing without FB (gate)" % (rc, status))
            mark("FB_FAILED")
        else:
            url = extract_url(out, [r"https://www\.facebook\.com/[^\"'\s]+"])
            with open(os.path.join(OUT, "facebook-url.txt"), "w") as f:
                f.write(url + "\n")
            links["facebook"] = url
            mark("FB_OK " + url)
            print("FB OK", url, flush=True)
    else:
        for line in markers:
            if line.startswith("FB_OK "):
                links["facebook"] = line.split(" ", 1)[1]

    # --- Blog links patch ---
    if "BLOG_OK" not in markers:
        with open(BLOG) as f:
            blog = json.load(f)
        blog["links"] = links
        with open(BLOG, "w") as f:
            json.dump(blog, f, ensure_ascii=False, indent=2)
        mark("BLOG_OK")
        print("BLOG OK", BLOG_URL, flush=True)

    # --- posted.log ---
    if "LOG_OK" not in markers:
        with open(POSTED_LOG, "a") as f:
            f.write("2026-11-21 18:00|special|rutestrip-ai-yang-ngerti-gunung\n")
        mark("LOG_OK")

    # --- Channel broadcast (type special) ---
    if "CHANNEL_OK" not in markers:
        cmd = ["python3", "/home/hatch/workspace/peka-content/telegram_channel.py",
               "--type", "special",
               "--title", "RuteStrip: AI yang Ngerti Gunung",
               "--para", para,
               "--cover", SLIDES[0],
               "--blog", BLOG_URL]
        if links["threads"]:
            cmd += ["--threads", links["threads"]]
        if links["instagram"]:
            cmd += ["--instagram", links["instagram"]]
        if links["facebook"]:
            cmd += ["--facebook", links["facebook"]]
        rc, out, status = run(cmd, 300, "channel-broadcast.log")
        if status == "timeout" or rc != 0:
            print("CHANNEL FAILED (rc=%s status=%s); do NOT blind-retry, check PENDING" % (rc, status))
            return 4
        mid = extract_url(out, [r"message_id=(\d+)"])
        mark("CHANNEL_OK " + mid)
        print("CHANNEL OK", mid, flush=True)

    # --- Group broadcast (type special-group; PENDING-guarded, no double) ---
    if "GROUP_OK" not in markers:
        cmd = ["python3", os.path.join(OUT, "broadcast_group.py"),
               "--type", "special",
               "--title", "RuteStrip: AI yang Ngerti Gunung",
               "--para", para,
               "--cover", SLIDES[0],
               "--blog", BLOG_URL]
        if links["threads"]:
            cmd += ["--threads", links["threads"]]
        if links["instagram"]:
            cmd += ["--instagram", links["instagram"]]
        if links["facebook"]:
            cmd += ["--facebook", links["facebook"]]
        rc, out, status = run(cmd, 600, "group-broadcast.log")
        if status == "timeout" or rc != 0:
            print("GROUP FAILED (rc=%s status=%s); do NOT blind-retry, check PENDING" % (rc, status))
            return 4
        mid = extract_url(out, [r"message_id=(\d+)"])
        mark("GROUP_OK " + mid)
        print("GROUP OK", mid, flush=True)

    print("ALL DONE")
    print("threads:", links["threads"])
    print("instagram:", links["instagram"])
    print("facebook:", links["facebook"])
    print("blog:", BLOG_URL)
    return 0


if __name__ == "__main__":
    sys.exit(main())
