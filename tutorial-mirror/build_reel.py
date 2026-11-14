#!/usr/bin/env python3
"""Build one tutorial-mirror reel: pick music, render frames, encode, cover.

Usage:
  python3 build_reel.py <edition spec.json> <out_dir> [--fps 24] [--duration 16] [--scale 2.0]

Reads the edition spec.json (fields: slug, reel: {date, source, hero,
headline, sub, points, steps, question, band}, shortlink from
shortlinks.json if present), writes a flat reel-spec.json into the out
dir, then:
  1. picks a music track EXACTLY ONCE via brand/music/pick_reel_track.sh
     and records it in track.txt (path + credit line),
  2. renders frames with the megumi venv python (animated/render.py),
  3. encodes 2160x3840 yuv420p with ffmpeg (-threads 2, RAM is tight),
  4. extracts the cover frame at 3.2s (scene 1 fully composed) as
     <slug>-cover.jpg (this is also the Peka blog cover image),
  5. deletes the frames dir.
Run from ~/workspace/peka-content/tutorial-mirror.
"""
import json
import os
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
MEGUMI_PY = "/home/hatch/workspace/megumi/venv/bin/python"
PICK_TRACK = "/home/hatch/workspace/peka-content/brand/music/pick_reel_track.sh"


def run(cmd, label):
    print(f">>> {label}", flush=True)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"FAILED {label}\nSTDOUT: {r.stdout}\nSTDERR: {r.stderr}", file=sys.stderr)
        sys.exit(3)
    print(r.stdout.strip()[-500:] if r.stdout.strip() else f"<<< {label} OK")
    return r.stdout.strip()


def music_credit(track_path):
    name = os.path.basename(track_path)
    title = name.replace("-kevin-macleod.mp3", "").replace("-", " ").title()
    return f"Music: {title} by Kevin MacLeod"


def main():
    spec_path = sys.argv[1]
    out_dir = sys.argv[2]
    fps = sys.argv[sys.argv.index("--fps") + 1] if "--fps" in sys.argv else "24"
    dur = sys.argv[sys.argv.index("--duration") + 1] if "--duration" in sys.argv else "16"
    scale = sys.argv[sys.argv.index("--scale") + 1] if "--scale" in sys.argv else "2.0"
    os.makedirs(out_dir, exist_ok=True)
    with open(spec_path, encoding="utf-8") as fh:
        spec = json.load(fh)
    slug = spec["slug"]
    reel = dict(spec["reel"])
    # hero lives at the top level of the edition spec; merge it in
    # (a missing hero used to render as a black box: src "undefined").
    reel.setdefault("hero", spec.get("hero", ""))
    assert reel.get("hero"), "spec needs a hero image path"
    short_path = os.path.join(out_dir, "shortlinks.json")
    if os.path.exists(short_path):
        with open(short_path, encoding="utf-8") as fh:
            reel["shortlink"] = json.load(fh)["blog"]
    flat_path = os.path.join(out_dir, "reel-spec.json")
    with open(flat_path, "w", encoding="utf-8") as fh:
        json.dump(reel, fh, ensure_ascii=False, indent=1)

    # 1. music, exactly once per edition (a re-render reuses track.txt)
    track_file = os.path.join(out_dir, "track.txt")
    if os.path.exists(track_file):
        track = open(track_file, encoding="utf-8").read().splitlines()[0].strip()
        print(f">>> PICK_TRACK (reuse): {track}")
    else:
        track = run([PICK_TRACK], "PICK_TRACK")
        with open(track_file, "w", encoding="utf-8") as fh:
            fh.write(track + "\n" + music_credit(track) + "\n")

    # 2. frames
    frames = os.path.join(out_dir, "frames")
    run([MEGUMI_PY, os.path.join(BASE, "animated", "render.py"),
         flat_path, frames, fps, dur, scale], "RENDER_FRAMES")

    # 3. encode (threads 2: the VPS has ~1 GB RAM free)
    mp4 = os.path.join(out_dir, slug + "-reel.mp4")
    run(["ffmpeg", "-y", "-framerate", fps, "-i", os.path.join(frames, "f%04d.png"),
         "-ss", "10", "-t", dur, "-i", track,
         "-filter_complex",
         "[0:v]scale=2160:3840[vout];"
         "[1:a]afade=t=in:st=0:d=0.5,afade=t=out:st=15.5:d=0.5[aout]",
         "-map", "[vout]", "-map", "[aout]",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast",
         "-threads", "2", "-r", fps, "-c:a", "aac", "-b:a", "160k",
         "-t", dur, mp4], "ENCODE")

    # 4. cover frame (scene 1 fully composed at 3.2s)
    cover = os.path.join(out_dir, slug + "-cover.jpg")
    run(["ffmpeg", "-y", "-ss", "3.2", "-i", mp4, "-frames:v", "1",
         "-q:v", "2", cover], "COVER")

    # 5. cleanup
    run(["rm", "-rf", frames], "CLEAN_FRAMES")
    print(f"reel: {mp4}")
    print(f"cover: {cover}")


if __name__ == "__main__":
    main()
