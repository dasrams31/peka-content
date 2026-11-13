#!/usr/bin/env python3
"""Encode rendered frames + voiceover into the final reel-v2 MP4.

Usage: python3 encode.py <frames_dir> <narration.mp3> <out.mp4> <cover.jpg> [fps]

Output: h264 2160x3840 yuv420p + aac, faststart. Cover is the frame
at t=1s (same convention as the v1 reels).

Memory note (2026-11-13): plain x264 at 4K OOM-killed this VM (6 GB
cgroup) with default threading, so the encode is capped to 2 threads
and preset veryfast. Do not remove the caps without re-testing.
"""
import subprocess
import sys


def run(cmd):
    subprocess.run(cmd, check=True)


def main():
    frames_dir, audio, out_mp4, cover = sys.argv[1:5]
    fps = sys.argv[5] if len(sys.argv) > 5 else "24"
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
    run([
        "ffmpeg", "-y", "-v", "error", "-ss", "1",
        "-i", out_mp4, "-frames:v", "1", cover,
    ])
    print(f"encoded {out_mp4} + cover {cover}")


main()
