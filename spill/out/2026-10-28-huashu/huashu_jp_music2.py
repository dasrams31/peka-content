#!/usr/bin/env python3
"""Second original Japanese-style track for the Huashu reel.

Different from v1: brighter 'yo' pentatonic scale (D major pentatonic),
a faster, more upbeat phrase, and a livelier taiko pattern. Still an
original composition, no licensed track, no credit line needed.
"""
import wave
import numpy as np

SR = 44100
DUR = 15.0
t = np.arange(int(SR * DUR)) / SR
out = np.zeros_like(t)

# Yo scale (D): D, E, G, A, B
NOTES = {"D4": 293.66, "E4": 329.63, "G4": 392.00, "A4": 440.00,
         "B4": 493.88, "D5": 587.33, "E5": 659.25, "G5": 783.99,
         "A5": 880.00, "B5": 987.77}


def pluck(start, freq, dur=0.6, amp=0.42):
    i0 = int(start * SR)
    n = int(dur * SR)
    if i0 + n > len(out):
        n = len(out) - i0
    tt = np.arange(n) / SR
    env = np.exp(-tt * 5.0)
    sig = (np.sin(2 * np.pi * freq * tt)
           + 0.35 * np.sin(2 * np.pi * freq * 2 * tt)) * env
    out[i0:i0 + n] += amp * sig


def taiko(start, amp=0.6):
    i0 = int(start * SR)
    n = int(0.3 * SR)
    tt = np.arange(n) / SR
    out[i0:i0 + n] += amp * np.sin(2 * np.pi * 70 * tt) * np.exp(-tt * 10)


# Brisk 8-note phrase, 2.5 s per bar, 6 bars.
phrase = [("D5", 0.0), ("E5", 0.3), ("G5", 0.6), ("A5", 0.9),
          ("G5", 1.2), ("E5", 1.5), ("D5", 1.8), ("B4", 2.1)]
for bar in range(6):
    base = bar * 2.5
    for name, off in phrase:
        pluck(base + off, NOTES[name], 0.55, 0.40)
    pluck(base, NOTES["D4"], 1.5, 0.22)
    taiko(base)
    taiko(base + 1.25, 0.35)

out = out / (np.max(np.abs(out)) + 1e-9) * 0.85
with wave.open("huashu-jp-music2.wav", "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((out * 32767).astype(np.int16).tobytes())
print("wrote huashu-jp-music2.wav", DUR, "s")
