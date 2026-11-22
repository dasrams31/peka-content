#!/usr/bin/env python3
"""Orchestrator for one reel-v2 edition: TTS -> render -> encode -> verify.

Usage: python3 build_reel.py <spec.json> <out_dir> [--theme <name>] [--no-render] [--music-lane <cyberpunk|light>] [--no-music]

- Resolves the theme name from themes.json and embeds the theme object.
- Synthesizes the voiceover (Piko venv python + tts.py).
- Picks one background music track (pick_reel_track.sh, lane from
  --music-lane or spec "music_lane", default cyberpunk) and mixes it
  under the voiceover at low volume via encode.py. The picked track
  is recorded in <out_dir>/track.txt (full path + display title) for
  the caption music credit. --no-music builds without a bed track.
- Computes scene spans from measured word timings (scene starts 0.4s
  before its first word so the headline can stagger in).
- Renders frames with Playwright (megumi venv python + render.py),
  encodes with ffmpeg, verifies with ffprobe, deletes the frames.
- Writes render-spec.json (the exact input the renderer used) and
  build.log in the out dir.

Nothing is posted anywhere. This script only builds files.
"""
import json
import os
import shutil
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
PIKO_PY = "/home/hatch/workspace/piko-app/venv/bin/python"
MEGUMI_PY = "/home/hatch/workspace/megumi/venv/bin/python"
MUSIC_PICKER = "/home/hatch/workspace/peka-content/brand/music/pick_reel_track.sh"
FPS = 24
SCALE = 2.0
MUSIC_LANES = ("cyberpunk", "light")


def track_title(path):
    name = os.path.basename(path)
    if name.endswith("-kevin-macleod.mp3"):
        name = name[: -len("-kevin-macleod.mp3")]
    return name.replace("-", " ").title()


def pick_music_track(lane):
    r = subprocess.run([MUSIC_PICKER, lane], capture_output=True,
                       text=True, check=True)
    path = r.stdout.strip()
    if not os.path.isfile(path):
        raise RuntimeError(f"picked music track missing: {path}")
    return path


def run(cmd, log):
    log.write("$ " + " ".join(cmd) + "\n")
    log.flush()
    r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       text=True)
    log.write(r.stdout)
    log.flush()
    if r.returncode != 0:
        raise RuntimeError(f"command failed ({r.returncode}): {' '.join(cmd)}")
    return r.stdout


def main():
    spec_path = sys.argv[1]
    out_dir = sys.argv[2]
    args = sys.argv[3:]
    theme_name = "dark-grid"
    no_render = False
    music_lane = None
    no_music = False
    i = 0
    while i < len(args):
        if args[i] == "--theme":
            theme_name = args[i + 1]
            i += 2
        elif args[i] == "--no-render":
            no_render = True
            i += 1
        elif args[i] == "--music-lane":
            music_lane = args[i + 1]
            i += 2
        elif args[i] == "--no-music":
            no_music = True
            i += 1
        else:
            i += 1
    os.makedirs(out_dir, exist_ok=True)
    log = open(os.path.join(out_dir, "build.log"), "w", encoding="utf-8")

    with open(spec_path, encoding="utf-8") as fh:
        spec = json.load(fh)
    if music_lane is None:
        music_lane = spec.get("music_lane", "cyberpunk")
    assert music_lane in MUSIC_LANES, f"unknown music lane {music_lane}"
    spec["music_lane"] = music_lane
    with open(os.path.join(BASE, "themes.json"), encoding="utf-8") as fh:
        themes = json.load(fh)
    assert theme_name in themes, f"unknown theme {theme_name}"
    spec["theme_name"] = theme_name
    spec["theme"] = themes[theme_name]

    # 1. Voiceover + word timings.
    run([PIKO_PY, os.path.join(BASE, "tts.py"), spec_path, out_dir], log)
    with open(os.path.join(out_dir, "words.json"), encoding="utf-8") as fh:
        words_data = json.load(fh)

    # 1b. Background music: one track per build, lane from
    # --music-lane / spec "music_lane". Recorded in track.txt so the
    # caption can credit it ("Music: <Title> by Kevin MacLeod").
    music_path = None
    if not no_music:
        music_path = pick_music_track(music_lane)
        title = track_title(music_path)
        with open(os.path.join(out_dir, "track.txt"), "w",
                  encoding="utf-8") as fh:
            fh.write(f"{music_path}\nMusic: {title} by Kevin MacLeod\n")
        log.write(f"music lane={music_lane} track={music_path}\n")
        log.flush()
        print(f"music: {music_path} ({title} by Kevin MacLeod)")

    # 2. Scene spans: each scene starts 0.4s before its first word.
    spans = []
    for si, s in enumerate(words_data["scenes"]):
        start = max(0.0, s["first_word"] - 0.4)
        spans.append({"start": round(start, 3), "end": round(s["end"], 3)})
    total = words_data["duration"]
    render_spec = dict(spec)
    render_spec["words"] = words_data["words"]
    render_spec["scene_spans"] = spans
    render_spec["total"] = total
    render_spec_path = os.path.join(out_dir, "render-spec.json")
    with open(render_spec_path, "w", encoding="utf-8") as fh:
        json.dump(render_spec, fh, ensure_ascii=False, indent=2)
    log.write(f"total={total}s words={words_data['word_count']} "
              f"scenes={len(spans)}\n")
    log.flush()
    print(f"narration done: {words_data['word_count']} words, "
          f"audio {words_data['audio_duration']}s, total {total}s")

    if no_render:
        log.close()
        print("skipped render (--no-render)")
        return

    # 3. Render frames, encode, verify.
    frames_dir = os.path.join(out_dir, "frames")
    run([MEGUMI_PY, os.path.join(BASE, "render.py"), render_spec_path,
         frames_dir, str(FPS), str(SCALE)], log)
    out_mp4 = os.path.join(out_dir, "reel.mp4")
    cover = os.path.join(out_dir, "reel-cover.jpg")
    encode_cmd = ["python3", os.path.join(BASE, "encode.py"), frames_dir,
                  os.path.join(out_dir, "narration.mp3"), out_mp4, cover,
                  str(FPS)]
    if music_path:
        encode_cmd.append(music_path)
    run(encode_cmd, log)
    probe = subprocess.run([
        "ffprobe", "-v", "error",
        "-show_entries", "stream=codec_type,codec_name,width,height,pix_fmt",
        "-show_entries", "format=duration",
        "-of", "json", out_mp4,
    ], capture_output=True, text=True, check=True)
    info = json.loads(probe.stdout)
    log.write("ffprobe: " + json.dumps(info) + "\n")
    v = next(s for s in info["streams"] if s.get("codec_type") == "video")
    assert v["codec_name"] == "h264", v
    assert (v["width"], v["height"]) == (2160, 3840), v
    assert v["pix_fmt"] == "yuv420p", v
    dur = float(info["format"]["duration"])
    assert 45.0 <= dur <= 60.0, f"duration {dur}s outside 45-60s"
    has_audio = any(s.get("codec_type") == "audio" for s in info["streams"])
    assert has_audio, "no audio stream"
    print(f"verified: {v['codec_name']} {v['width']}x{v['height']} "
          f"{v['pix_fmt']} {dur:.1f}s audio={'yes' if has_audio else 'no'}")

    shutil.rmtree(frames_dir)
    log.write("frames deleted\n")
    log.close()
    print(f"done -> {out_mp4}")


main()
