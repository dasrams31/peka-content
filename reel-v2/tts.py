#!/usr/bin/env python3
"""Voiceover synthesis for reel-v2 (voiceover-led reels, no music).

Uses Edge TTS voice id-ID-ArdiNeural (same voice Piko uses) with
boundary='WordBoundary' so every spoken word gets a real measured
start/end timestamp. Each scene's narration is synthesized separately,
then joined with short silence gaps so scene boundaries stay exact.

Run with the Piko venv python (edge-tts lives there):
  ~/workspace/piko-app/venv/bin/python tts.py <spec.json> <out_dir>

Reads spec.json scenes[].narration. Writes:
  narration.mp3  - joined voiceover audio
  words.json     - {"words": [{text, start, end, scene, line}],
                    "scenes": [{start, end}], "duration": <seconds>,
                    "voice": ..., "gap": ...}
  narration.txt  - full narration text, one scene per block
"""
import asyncio
import json
import os
import subprocess
import sys

import edge_tts

VOICE = "id-ID-ArdiNeural"
GAP = 0.30  # seconds of silence between scenes
TAIL = 0.80  # seconds of silence after the last word
RATE = "+0%"  # overridden per spec ("rate" field)


def words_per_line(words, max_words=7):
    """Greedy line grouping for the karaoke bar. Breaks early at a
    sentence-ending token so a line never straddles two sentences."""
    lines = []
    cur = []
    for w in words:
        cur.append(w)
        end_sentence = w["text"].rstrip().endswith((".", "?", "!"))
        if len(cur) >= max_words or end_sentence:
            lines.append(cur)
            cur = []
    if cur:
        lines.append(cur)
    for li, line in enumerate(lines):
        for w in line:
            w["line"] = li
    return lines


async def synth_segment(text, rate):
    """Synthesize one segment. Returns (mp3_bytes, words) where words
    carry start/end in seconds relative to the segment start."""
    comm = edge_tts.Communicate(text, VOICE, rate=rate,
                                boundary="WordBoundary")
    audio = bytearray()
    words = []
    async for chunk in comm.stream():
        if chunk["type"] == "audio":
            audio.extend(chunk["data"])
        elif chunk["type"] == "WordBoundary":
            words.append({
                "text": chunk["text"],
                "start": chunk["offset"] / 1e7,
                "end": (chunk["offset"] + chunk["duration"]) / 1e7,
            })
    return bytes(audio), words


def probe_duration(path):
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "csv=p=0", path,
    ]).decode().strip()
    return float(out)


async def main():
    spec_path, out_dir = sys.argv[1], sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)
    with open(spec_path, encoding="utf-8") as fh:
        spec = json.load(fh)
    scenes = spec["scenes"]
    rate = spec.get("rate", RATE)
    assert all(s.get("narration") for s in scenes), "every scene needs narration"

    tmp = os.path.join(out_dir, "_tts_tmp")
    os.makedirs(tmp, exist_ok=True)
    concat_list = []
    all_words = []
    scene_spans = []
    cursor = 0.0
    # Silence gap file (same params as Edge TTS mp3: 24 kHz mono).
    silence = os.path.join(tmp, "silence.mp3")
    subprocess.run([
        "ffmpeg", "-y", "-v", "error", "-f", "lavfi",
        "-i", "anullsrc=r=24000:cl=mono", "-t", str(GAP),
        "-c:a", "libmp3lame", "-q:a", "4", silence,
    ], check=True)

    for si, scene in enumerate(scenes):
        seg_mp3 = os.path.join(tmp, f"seg{si}.mp3")
        audio, words = await synth_segment(scene["narration"], rate)
        with open(seg_mp3, "wb") as fh:
            fh.write(audio)
        seg_dur = probe_duration(seg_mp3)
        # Word offsets are relative to the mp3 start; shift to the
        # absolute timeline. The mp3 may carry a small encoder delay;
        # word boundaries are measured from the same stream, so the
        # shift is exact relative to the segment start.
        for w in words:
            w["scene"] = si
            w["start"] += cursor
            w["end"] += cursor
        all_words.extend(words)
        scene_spans.append({
            "start": cursor + (words[0]["start"] - cursor if words else 0.0),
            "end": cursor + seg_dur,
            "first_word": words[0]["start"] if words else cursor,
            "last_word_end": words[-1]["end"] if words else cursor,
        })
        concat_list.append(seg_mp3)
        cursor += seg_dur
        if si < len(scenes) - 1:
            concat_list.append(silence)
            cursor += GAP
    total = cursor + TAIL

    # Join with the concat demuxer and re-encode (plain -c copy leaves
    # non-monotonic DTS warnings at the joins; re-encoding is clean).
    list_path = os.path.join(tmp, "concat.txt")
    with open(list_path, "w", encoding="utf-8") as fh:
        for p in concat_list:
            # Absolute paths: ffmpeg resolves concat entries relative to
            # the list file, so relative paths would break.
            fh.write(f"file '{os.path.abspath(p)}'\n")
    narration_mp3 = os.path.join(out_dir, "narration.mp3")
    subprocess.run([
        "ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
        "-i", list_path, "-c:a", "libmp3lame", "-q:a", "4", narration_mp3,
    ], check=True)

    words_per_line(all_words)
    words_json = {
        "voice": VOICE,
        "rate": rate,
        "gap": GAP,
        "tail": TAIL,
        "duration": round(total, 3),
        "audio_duration": round(probe_duration(narration_mp3), 3),
        "words": all_words,
        "scenes": scene_spans,
        "word_count": len(all_words),
    }
    with open(os.path.join(out_dir, "words.json"), "w", encoding="utf-8") as fh:
        json.dump(words_json, fh, ensure_ascii=False, indent=2)
    with open(os.path.join(out_dir, "narration.txt"), "w", encoding="utf-8") as fh:
        for si, scene in enumerate(scenes):
            fh.write(f"[scene {si} - {scene.get('kind', '')}]\n")
            fh.write(scene["narration"] + "\n\n")
    print(f"words={len(all_words)} audio={words_json['audio_duration']}s "
          f"total={total:.2f}s -> {out_dir}")


asyncio.run(main())
