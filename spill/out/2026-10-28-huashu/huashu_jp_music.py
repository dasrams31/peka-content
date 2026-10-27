#!/usr/bin/env python3
"""Original Japanese-style instrumental for the Huashu reel.

No licensed track is used: the Peka music library has no Japanese
track, so this is an original 15-second composition in the Japanese
'in' (miyako-bushi) pentatonic scale, with koto-like plucks and a
low taiko pulse. Safe to post, no credit line to a third party needed.
"""
import wave
import numpy as np

SR = 44100
DUR = 15.0
t = np.arange(int(SR * DUR)) / SR
out = np.zeros_like(t)

# In scale (D): D, Eb, G, A, Bb
NOTES = {"D4": 293.66, "Eb4": 311.13, "G4": 392.00, "A4": 440.00,
         "Bb4": 466.16, "D5": 587.33, "Eb5": 622.25, "G5": 783.99,
         "A5": 880.00}


def pluck(start, freq, dur=0.9, amp=0.5):
    i0 = int(start * SR)
    n = int(dur * SR)
    if i0 + n > len(out):
        n = len(out) - i0
    tt = np.arange(n) / SR
    env = np.exp(-tt * 3.5)
    sig = (np.sin(2 * np.pi * freq * tt)
           + 0.4 * np.sin(2 * np.pi * freq * 2 * tt)
           + 0.15 * np.sin(2 * np.pi * freq * 3 * tt)) * env
    out[i0:i0 + n] += amp * sig


def taiko(start, amp=0.7):
    i0 = int(start * SR)
    n = int(0.35 * SR)
    tt = np.arange(n) / SR
    sig = np.sin(2 * np.pi * 65 * tt) * np.exp(-tt * 9)
    out[i0:i0 + n] += amp * sig


# Melody: one phrase per 3.75 s, repeated with a small variation.
phrase = [("D5", 0.0, 0.9), ("Bb4", 0.6, 0.6), ("A4", 1.1, 0.6),
          ("G4", 1.6, 0.9), ("A4", 2.3, 0.6), ("Bb4", 2.8, 0.6),
          ("D5", 3.3, 0.45)]
for bar in range(4):
    base = bar * 3.75
    for name, off, dur in phrase:
        pluck(base + off, NOTES[name], dur, 0.42)
    # Low drone root on bar start, taiko pulse each bar + halfway.
    pluck(base, NOTES["D4"], 1.8, 0.25)
    taiko(base)
    taiko(base + 1.875, 0.4)

out = out / (np.max(np.abs(out)) + 1e-9) * 0.85
with wave.open("huashu-jp-music.wav", "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((out * 32767).astype(np.int16).tobytes())
print("wrote huashu-jp-music.wav", DUR, "s")
