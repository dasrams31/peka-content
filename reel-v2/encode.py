#!/usr/bin/env python3
"""Encode rendered frames + voiceover into the final reel-v2 MP4.

Usage: python3 encode.py <frames_dir> <narration.mp3> <out.mp4> <cover.jpg> [fps] [music.mp3]

Output: h264 2160x3840 yuv420p + aac, faststart. Cover is the frame
at t=1s (same convention as the v1 reels).

Music (optional 6th arg, since 2026-11-22): one background track is
mixed under the voiceover at low volume (0.12), faded in over 1s and
out over the last 1s, trimmed to the narration length (looped if the
track is shorter). The voiceover stays at full volume and defines
the output length (amix duration=first). Without a music arg the
output is narration only, exactly as before.

Memory note (2026-11-13): plain x264 at 4K OOM-killed this VM (6 GB
cgroup) with default threading, so the encode is capped to 2 threads
and preset veryfast. Do not remove the caps without re-testing.
"""
import json
import subprocess
import sys


def run(cmd):
    subprocess.run(cmd, check=True)


def probe_duration(path):
    r = subprocess.run([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "json", path,
    ], capture_output=True, text=True, check=True)
    return float(json.loads(r.stdout)["format"]["duration"])


def main():
    frames_dir, audio, out_mp4, cover = sys.argv[1:5]
    fps = sys.argv[5] if len(sys.argv) > 5 else "24"
    music = sys.argv[6] if len(sys.argv) > 6 else None
    if music is None:
        run([
            "ffmpeg", "-y", "-v", "error",
            "-threads", "2",
            "-framerate", fps, "-i", f"{frames_dir}/f%04d.png",
            "-i", audio,
            "-c:v", "libx264", "-preset", "veryfast",
            "-pix_fmt", "yuv420p", "-r", fps,
            "-c:a", "aac", "-b:a", "192k",
            "-shortest", "-movflags", "+faststart", out_mp4,
        ])
    else:
        dur = probe_duration(audio)
        fade_out_start = max(0.0, dur - 1.0)
        run([
            "ffmpeg", "-y", "-v", "error",
            "-threads", "2",
            "-framerate", fps, "-i", f"{frames_dir}/f%04d.png",
            "-i", audio,
            "-stream_loop", "-1", "-i", music,
            "-filter_complex",
            f"[2:a]atrim=0:{dur:.3f},volume=0.12,"
            f"afade=t=in:st=0:d=1,"
            f"afade=t=out:st={fade_out_start:.3f}:d=1[mus];"
            f"[1:a][mus]amix=inputs=2:duration=first:normalize=0[aout]",
            "-map", "0:v", "-map", "[aout]",
            "-c:v", "libx264", "-preset", "veryfast",
            "-pix_fmt", "yuv420p", "-r", fps,
            "-c:a", "aac", "-b:a", "192k",
            "-shortest", "-movflags", "+faststart", out_mp4,
        ])
    run([
        "ffmpeg", "-y", "-v", "error", "-ss", "1",
        "-i", out_mp4, "-frames:v", "1", cover,
    ])
    print(f"encoded {out_mp4} + cover {cover}")


main()
