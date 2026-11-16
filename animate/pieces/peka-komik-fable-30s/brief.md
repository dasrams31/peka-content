# Brief: Komik Peka #01 — Claude Fable 5.2: termurah, kok nomor satu? (30 detik)

## The idea in one sentence

Piko bingung: model termurah kok jadi nomor satu? Tujuh kalimat menjawabnya
satu per satu — harga turun 20%, delapan dolar per juta token, skor 65
nomor satu, unggul 5 poin dari Gemini Carbon, konteks 1 juta token — lalu
langkah coba konkret. Digambar gaya komik navy + emas dengan motif trofi.

## Format and spec

- Format: F2 morph chain, same as the 8s version (gold moon becomes yellow
  sun), morph at 14.0s. 30s = 720 frames.
- Size: 1080x1920, 24fps, 120 BPM, 30s
- Style: `peka-komik` (style, read-only) + variant `src/options.js`:
  `COMIC_MOTIF = 'trophy'`; palette dark navy + gold — ground1 `#0e1430`
  (deep navy), ground2 `#16204d` (lighter navy), accent `#ffd60a` (Piko
  yellow, locked — never changed, or Piko renders wrong), accent2 `#e8b93c`
  (gold: moon, giant "65"), ink `#141210`, paper `#f5f1e8`.
- Hero: Piko as a vector (yellow letter P, one eye, antenna), from the kit.
- The story advances through the dialogue: the night bubble swaps text at
  every night line, the morning bubble swaps at every morning line, and the
  caption strip carries one fact per line (`stripAt` in src/scenes.js).
  Panel layouts are the 8s layouts verbatim (same coordinates, same
  clearances, already verified). On-screen text (mandatory, all present):
  giant gold "65", "$8/$40" (on the price tag "$10/$50 jadi $8/$40"), one
  concrete try-step ("Buka Claude, pilih Fable 5.2" on the caption strip).
  No URL/link on screen. No theme name printed on the final design
  (internal label only: "trophy / navy + gold").

## Beats

| # | t (s) | what happens | bridge into the next | sound |
|---|---|---|---|---|
| 1 | 0.0-3.18 | Night panel (deep navy), Piko confused, "?" bubbles pop in, bubble "Model termurah, kok nomor satu?!", strip "Termurah, kok nomor satu?!" | l2 | soft pad, rising fifth at the wake (1.0s) |
| 2 | 3.18-8.16 | Price tag "$10/$50 jadi $8/$40" pops, bubble "Baru rilis, harga turun 20%!", strip "Rilis 9 November 2026" | l3 | pluck |
| 3 | 8.16-14.0 | Bubble "Delapan dolar per juta token!", strip "Konteks 1 juta token", 2.0s of quiet before the morph | gold moon morphs into the yellow sun at 14.0s | pluck, paper swish into the morph |
| 4 | 14.0-18.34 | Navy morning panel, sun rays, trophy motif + giant gold "65" + burst "NOMOR 1", Piko happy, bubble "Skor 65, nomor satu!", strip "Skor 65, nomor satu" | l5 | warm chord, plucks, payoff hit on the morph |
| 5 | 18.34-22.50 | Bubble "Unggul 5 poin!", strip "Gemini Carbon: 60" | l6 | pluck |
| 6 | 22.50-26.67 | Bubble "Konteks 1 juta token!", strip "1 juta token konteks" | l7 | pluck |
| 7 | 26.67-30.0 | Bubble "Buka Claude, cobain!", strip "Buka Claude, pilih Fable 5.2", tail | loops | warm close, pluck |

## Sound plan

Same score as the 8s version, stretched: night pad 0-14.1, morning pad
14.0-30.05, hero motif at the wake, one pluck per dialogue pop, arpeggio
from the morph, paper swish into the morph at 13.7-14.05. Loudest hit the
morph at 14.0s, in the payoff act; the 2.0s gap before it (l3 ends 12.28,
l4 starts 14.28) is the silence before the payoff.
The score is kept for the review's story-arc measurement, but the
delivered mix is voice-over only: the score sits at -60 dB under the
voice (piece.json "voice.music"), inaudible. No background music track.

## Voice-over (Edge TTS id-ID-ArdiNeural, no music bed)

- Takes in voice/: l1-l7.mp3, all +0% rate. voice.mjs joins them into
  voice.wav. Generated with the `edge_tts` module from the piko-app venv
  (`~/workspace/piko-app/venv/bin/python -m edge_tts --voice
  id-ID-ArdiNeural --file <line>.txt --write-media <id>.mp3 --rate +0%`).
  No ElevenLabs.
- Timing (voice.json): l1 0.30-2.58 (2.63 w/s), l2 3.18-7.56 (2.74 w/s),
  l3 8.16-12.28 (2.91 w/s), l4 14.28-17.74 (2.60 w/s), l5 18.34-21.90
  (3.37 w/s), l6 22.50-26.17 (2.99 w/s), l7 26.67-29.09 (2.07 w/s); total
  voice 29.89s inside the 30.0s piece. The l3 `after` is 2.0s so l4
  starts 0.28s after the 14.0s morph. Word times are estimated
  (faster-whisper is not installed); no scene cues on individual words.
- The speech bubbles pop in sync with the lines: night 0.35 / 3.23 /
  8.21, morning 14.33 / 18.39 / 22.55 / 26.72 (line start + 0.05s,
  hardcoded in src/scenes.js, coupled to voice/voice.json — if the
  script timing changes, update both). Strips switch at the line starts.
- Mix: voice over the score at -60 dB, loudness corrected to -14.5 LUFS
  integrated (see LOG.md for the correction steps).

## Claims and sources (web-checked 16 Nov 2026, same as the 8s version)

- Anthropic released Claude Fable 5.2 (and Mythos 5.2, restricted) on
  9 Nov 2026; Fable 5.2 costs $8 per million input tokens and $40 per
  million output tokens, down from $10/$50 for Fable 5.1 (20% cut);
  1M-token context window; live on the Claude apps, Claude Code, API,
  AWS, Google Cloud and Azure. Sources: Anthropic launch post (via
  oguzhan.co deep-dive, bitsminds.com, devdaynotes.com, glonce.com —
  all cross-checked 16 Nov 2026, figures agree).
- Artificial Analysis Intelligence Index v5.0.1: Claude Fable 5.2 (Max)
  scores 65, ranked first, five points clear of Gemini 4 Carbon (60).
  Re-checked via the same reports 16 Nov 2026; the on-screen "65" and
  the spoken "skor 65" use this figure only.
- Mythos 5.2 is restricted to vetted organizations in Anthropic's
  Verification Programs — the piece never promises Mythos access.
- The try-step "Buka Claude, pilih Fable 5.2" is real: Fable 5.2 is
  selectable in the Claude apps (model ID `claude-fable-5-2`).
- Angle note: "model termurah yang jadi nomor 1" + one concrete try-step,
  not benchmark-only. No price or score is exaggerated.
