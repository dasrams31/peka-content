#!/usr/bin/env python3
"""Orchestrator for one Herlambang-style Tutorial Agent reel: TTS -> render -> encode -> verify.

Usage:
  python3 build_reel_v2.py <reel-v2-spec.json> <out_dir> [--skip-tts] [--no-render]

- Reads the edition reel-v2 spec (scenes with narration + headline +
  terminal/cards/steps, character poses, shortlink).
- Synthesizes the voiceover (Piko venv python + reel-v2/tts.py) unless
  --skip-tts is given, in which case narration.mp3 + words.json already
  present in the out dir are reused (the voice may come from a different
  TTS source; words.json must carry the same schema as tts.py writes:
  {"words": [{text, start, end, scene, line}], "scenes": [{start, end,
  first_word, last_word_end}], "duration": <seconds>}).
- Computes scene spans from measured word timings (scene starts 0.4s
  before its first word) and per-word headline stagger delays by
  matching each headline token to the scene's narration words
  (prefix-tolerant, so "langkah" matches "langkahnya").
- Renders frames with Playwright (megumi venv python +
  animated/render-herlambang.py), encodes with ffmpeg via
  reel-v2/encode.py, verifies with ffprobe, deletes the frames.
- Writes render-spec.json (the exact input the renderer used) and
  build-v2.log in the out dir. Output files reuse the edition names:
  <slug>-reel.mp4 and <slug>-cover.jpg (cover re-extracted at t=3.0s,
  scene 1 fully composed).

Nothing is posted anywhere. This script only builds files.
"""
import json
import os
import re
import shutil
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
REEL_V2 = "/home/hatch/workspace/peka-content/reel-v2"
PIKO_PY = "/home/hatch/workspace/piko-app/venv/bin/python"
MEGUMI_PY = "/home/hatch/workspace/megumi/venv/bin/python"
FPS = 24
SCALE = 2.0


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


def _norm(s):
    return re.sub(r"[^0-9a-zA-Z]", "", s).lower()


def headline_delays(headline, scene_words, span_start):
    """Match each headline token to the scene's narration words in order
    (prefix-tolerant) and return its delay relative to the scene start.
    Unmatched tokens fall back to previous delay + 0.35s, so the render
    never breaks on a TTS token quirk."""
    tokens = [wd["t"] for ln in headline for wd in ln]
    delays = []
    wi = 0
    last = 0.0
    for tok in tokens:
        t = _norm(tok)
        found = None
        while wi < len(scene_words):
            w = _norm(scene_words[wi]["text"])
            wi += 1
            if w == t or w.startswith(t) or t.startswith(w):
                found = scene_words[wi - 1]["start"] - span_start
                break
        if found is None:
            last += 0.35
            delays.append(round(last, 3))
        else:
            last = found
            delays.append(round(found, 3))
    return delays


def main():
    spec_path = sys.argv[1]
    out_dir = sys.argv[2]
    args = sys.argv[3:]
    skip_tts = "--skip-tts" in args
    no_render = "--no-render" in args
    os.makedirs(out_dir, exist_ok=True)
    log = open(os.path.join(out_dir, "build-v2.log"), "w", encoding="utf-8")

    with open(spec_path, encoding="utf-8") as fh:
        spec = json.load(fh)
    slug = spec["slug"]

    # 1. Voiceover + word timings.
    words_path = os.path.join(out_dir, "words.json")
    narration_path = os.path.join(out_dir, "narration.mp3")
    if skip_tts:
        assert os.path.exists(narration_path), "skip-tts needs narration.mp3 in out dir"
        assert os.path.exists(words_path), "skip-tts needs words.json in out dir"
        print(">>> TTS skipped, reusing existing narration.mp3 + words.json")
        log.write("TTS skipped, reusing existing narration\n")
    else:
        run([PIKO_PY, os.path.join(REEL_V2, "tts.py"), spec_path, out_dir], log)
    with open(words_path, encoding="utf-8") as fh:
        words_data = json.load(fh)

    # 2. Scene spans + headline stagger delays.
    spans = []
    for si, s in enumerate(words_data["scenes"]):
        start = max(0.0, s["first_word"] - 0.4)
        spans.append({"start": round(start, 3), "end": round(s["end"], 3)})
    total = words_data["duration"]
    render_spec = dict(spec)
    render_spec["words"] = words_data["words"]
    render_spec["scene_spans"] = spans
    render_spec["total"] = total
    for si, scene in enumerate(render_spec["scenes"]):
        if scene.get("headline"):
            scene_words = [w for w in words_data["words"] if w["scene"] == si]
            scene["headline_delays"] = headline_delays(
                scene["headline"], scene_words, spans[si]["start"])
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
    run([MEGUMI_PY, os.path.join(BASE, "animated", "render-herlambang.py"),
         render_spec_path, frames_dir, str(FPS), str(SCALE)], log)
    out_mp4 = os.path.join(out_dir, slug + "-reel.mp4")
    cover = os.path.join(out_dir, slug + "-cover.jpg")
    run(["python3", os.path.join(REEL_V2, "encode.py"), frames_dir,
         narration_path, out_mp4, cover, str(FPS)], log)
    # Better cover: scene 1 fully composed (encode.py takes t=1s).
    log.write("COVER_3S\n")
    run(["ffmpeg", "-y", "-v", "error", "-ss", "3.0", "-i", out_mp4,
         "-frames:v", "1", "-q:v", "2", cover], log)
    probe = subprocess.run([
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=codec_name,width,height,pix_fmt",
        "-show_entries", "format=duration",
        "-of", "json", out_mp4,
    ], capture_output=True, text=True, check=True)
    info = json.loads(probe.stdout)
    log.write("ffprobe: " + json.dumps(info) + "\n")
    v = info["streams"][0]
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
