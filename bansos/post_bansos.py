#!/usr/bin/env python3
"""Post one prepared bansos edition (ticket 3 slides + animated reel).

Usage: post_bansos.py <out_dir> <official_url> <slug> <date YYYY-MM-DD>

Order (locked rules):
1. Shorten the official URL via s.peka.ai.id FIRST. If shortening fails
   (e.g. guest quota exhausted), STOP before posting anything. Never
   publish the long URL in a caption, comment, or blog post.
2. Post Threads carousel (3 slides), IG reel, FB reel.
3. Post the shortlink comment as a Threads reply and an FB comment.
4. Copy slides to peka-content/images/, write the blog JSON, append logs.
Prints a summary for the cron report. Exits non-zero on any failure.
"""
import json
import shutil
import subprocess
import sys
import urllib.request

OUT, OFFICIAL, SLUG, DATE = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
HOME = "/home/hatch"
PC = f"{HOME}/workspace/peka-content"


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        print(f"FAILED: {' '.join(cmd)}\n{r.stdout}\n{r.stderr}", file=sys.stderr)
        sys.exit(3)
    return r.stdout.strip()


def shorten(url):
    req = urllib.request.Request(
        "http://127.0.0.1:8095/api/shorten",
        data=json.dumps({"url": url}).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.load(resp)
    except Exception as e:
        print(f"SHORTEN FAILED: {e} -- STOPPING, nothing posted", file=sys.stderr)
        sys.exit(2)
    code = data.get("code") or data.get("short") or ""
    if not code:
        print(f"SHORTEN FAILED: no code in {data} -- STOPPING", file=sys.stderr)
        sys.exit(2)
    return f"https://s.peka.ai.id/{code}"


def main():
    short = shorten(OFFICIAL)
    print(f"shortlink: {short}")
    comment = open(f"{OUT}/comment-link.txt").read().replace("__SHORTLINK__", short)
    open(f"{OUT}/comment-final.txt", "w").write(comment)

    threads_cap = open(f"{OUT}/caption-threads.txt").read().strip()
    ig_cap = open(f"{OUT}/caption-reel-ig.txt").read().strip()
    fb_cap = open(f"{OUT}/caption-reel-fb.txt").read().strip()

    # Threads carousel
    t_out = run([
        "/opt/hatch/bin/threads-cli", "publish-post",
        "--account-id", "17841417164011141",
        "--media-item", f'{{"file":"{OUT}/bansos-01.png"}}',
        "--media-item", f'{{"file":"{OUT}/bansos-02.png"}}',
        "--media-item", f'{{"file":"{OUT}/bansos-03.png"}}',
        "--text", threads_cap,
    ])
    t_id = json.loads(t_out)["post_id"]
    t_url = run([
        "/opt/hatch/bin/threads-cli", "post",
        "--account-id", "17841417164011141", "--post-id", t_id,
    ])
    t_link = json.loads(t_url)["posts"][0]["url"]
    print(f"threads: {t_link}")

    # IG reel
    ig_out = run([
        "/opt/hatch/bin/instagram-cli", "post-feed",
        "--account-id", "17841426380826261",
        "--file", f"{OUT}/bansos-reel.mp4",
        "--cover", f"{OUT}/bansos-reel-cover.jpg",
        "--caption", ig_cap,
    ])
    ig_media = json.loads(ig_out).get("media_fbid", "")
    print(f"instagram media: {ig_media} (shortcode not returned by CLI)")

    # FB reel
    fb_out = run([
        "/opt/hatch/bin/facebook-cli", "pages", "posts", "create",
        "--page-id", "1399217353266190", "--privacy", "PUBLIC",
        "--text", fb_cap, "--file", f"{OUT}/bansos-reel.mp4",
    ])
    fb = json.loads(fb_out)
    fb_link = fb.get("post_url", "")
    fb_post_id = fb.get("post_id", "")
    print(f"facebook: {fb_link}")

    # Comments with shortlink
    run([
        "/opt/hatch/bin/threads-cli", "publish-post",
        "--account-id", "17841417164011141",
        "--reply-to-post-fbid", t_id, "--text", comment,
    ])
    print("threads comment posted")
    if fb_post_id:
        run([
            "/opt/hatch/bin/facebook-cli", "post", "comments", "add",
            "--post-id", fb_post_id, "--text", comment,
        ])
        print("facebook comment posted")

    # Blog + images
    for i in range(1, 4):
        dst = f"{SLUG}.png" if i == 1 else f"{SLUG}-{i}.png"
        shutil.copy(f"{OUT}/bansos-0{i}.png", f"{PC}/images/{dst}")
    blog = json.load(open(f"{OUT}/blog-draft.json"))
    blog["links"] = {"threads": t_link, "facebook": fb_link, "instagram": ""}
    json.dump(blog, open(f"{PC}/blog/{SLUG}.json", "w"), indent=2, ensure_ascii=False)
    print(f"blog: https://blog.peka.ai.id/p/{SLUG}")

    with open(f"{PC}/bansos/posted.log", "a") as f:
        f.write(f"{DATE}|bansos|{SLUG}|{short}\n")
    with open(f"{PC}/posted.log", "a") as f:
        f.write(f"{DATE} 19:00|bansos|{SLUG}\n")
    with open(f"{OUT}/post-log.txt", "w") as f:
        f.write(f"threads: {t_link}\ninstagram media: {ig_media}\nfacebook: {fb_link}\nshortlink: {short}\nblog: https://blog.peka.ai.id/p/{SLUG}\n")
    print("DONE")


if __name__ == "__main__":
    main()
