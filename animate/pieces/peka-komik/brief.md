# Brief: Peka AI — Bingung pilih AI? (komik)

## The idea in one sentence

Piko bingung dikepung terlalu banyak pilihan AI, lalu Peka pilihkan yang cocok — digambar gaya komik: panel berbingkai hitam tebal, halftone, bubble dialog, burst "BANYAK".

## Format and spec

- Format: F2 morph chain, same as peka-contoh (moon becomes sun at 4.0s).
- Size: 1080x1920, 24fps, 120 BPM, 8s = 192 frames
- Style: cut-paper kit with a comic treatment (not a shipped comic style yet — this piece is the look check for one). Palette locked to Peka: yellow #ffd60a, black #141210, cream #f5f1e8.
- Hero: Piko redrawn as a vector (yellow letter P, one black eye, small smile, antenna with ball), from piko-idle.png.

## Beats (same as peka-contoh)

| # | t (s) | what happens | bridge into the next | sound |
|---|---|---|---|---|
| 1 | 0.0-4.0 | Night panel, Piko confused, "?" bubbles pop in, speech bubble "Bingung pilih AI?!", burst "BANYAK" | moon morphs into the sun at 4.0s | soft pad, rising fifth at the wake (1.0s), paper swish into the morph |
| 2 | 4.0-8.0 | Yellow morning panel, sun rays, checkmarks pop one by one, Piko happy, bubble "Peka pilihkan!" | loops | warm chord, plucks per checkmark, payoff hit on the sun |

## Sound plan

Same score as peka-contoh (copied): loudest hit the morph at 4.0s.
The score is kept for the review's story-arc measurement, but the
delivered mix is voice-over only: the score sits at -60 dB under the
voice (piece.json "voice.music"), inaudible (gap/tail segments measure
mean -73 dB). No background music track was added.

## Voice-over (Edge TTS id-ID-ArdiNeural, no music bed)

- Takes in voice/: night.mp3 "Bingung pilih AI?" (+0%), morning.mp3
  "Peka pilihkan yang cocok buat kamu." (-10% so it stays under the
  3.5 words/s density cap). voice.mjs joins them into voice.wav.
- Timing (voice.json): night 0.30-1.24s (3.18 w/s), morning 4.30-6.08s
  (3.38 w/s), total voice 6.88s inside the 8.0s piece. Line 2 starts
  0.30s after the 4.0s morph. Word times are estimated (faster-whisper
  is not installed); no scene cues on individual words.
- The speech bubbles pop in sync with the lines: night bubble 0.35s,
  morning bubble 4.35s (hardcoded in src/scenes.js, coupled to
  voice/script.json — if the script timing changes, update both).
- Mix: voice over the score at -60 dB, sidechain-ducked, loudness
  corrected to -14.5 LUFS integrated (two-pass loudnorm + a -1.1 dB
  trim; the export's single-pass loudnorm landed at -12.7 LUFS).

## Revision 2 — look check round 2 + voiceover (2026-11-16)

Layout fixes (all verified on the new stills):
- Sun/moon moved (0.72, 0.22) -> (0.80, 0.17): the sun no longer hides
  behind the "Peka pilihkan!" bubble; all rays clear it.
- Checkmark row moved up (gy+90/+50 -> gy+40/+40, x spread widened):
  clearance to the caption tape is now 76px (was ~14px, when the drop
  shadow merged with the tape edge at phone scale and the row read as
  cut off). All 5 circles fully visible.
- Burst "BANYAK" moved up (LY 0.66 -> 0.62) and shrunk (r 195 -> 180):
  34px clear of the tape, 65px from the right frame edge.
- Edge "?" bubbles nudged inward (0.10 -> 0.12, 0.80 -> 0.79).

Motion polish:
- Speech bubbles pop in with a back-eased overshoot (night 0.35s,
  morning 4.35s, in sync with the voice lines).
- Burst scales in with overshoot at 1.6s (wake + 0.6).
- Action lines grow in one by one from the wake (staggered 0.04s).
- Piko hops (70px, 0.5s) at the morph; white flash (peak 0.5 alpha
  at 4.1s) marks the moon -> sun turn.

## Claims and sources (web-checked)

- No factual claims on screen; copy is brand copy for Peka AI (peka.ai.id).
