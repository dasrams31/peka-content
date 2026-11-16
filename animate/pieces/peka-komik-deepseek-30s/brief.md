# Brief: Komik Peka #02 — Ngoding pakai DeepSeek, bukan Claude? (terminal, 30 detik)

## The idea in one sentence

Piko bingung di depan jendela terminal ("ngoding pakai apa?"), lalu tujuh
kalimat menjawabnya satu per satu — harness open-source lisensi MIT, satu
perintah dan Web UI kebuka, benchmark 90,6 dengan label klaim vendor, Kimi
juga open-weight — lalu langkah coba konkret. Tanpa vonis "DeepSeek menang".

## Format and spec

- Format: F2 morph chain, same as the 8s version (cursor circle becomes a
  DONE check circle), morph at 14.0s. 30s = 720 frames.
- Size: 1080x1920, 24fps, 120 BPM, 30s
- Style: `peka-komik` (style, read-only) + variant `src/options.js`:
  `COMIC_MOTIF = 'terminal'`; palette terminal green — ground1 `#0a1f14`,
  ground2 `#0d2c1d`, accent `#3ddc84` (terminal green), accent2 `#ffd60a`
  (Piko yellow, locked — the local piko() draws Piko yellow, never the
  kit's comicPiko, or Piko renders green), ink `#141210`,
  paper `#f5f1e8`.
- Hero: Piko as a vector (yellow letter P, one eye, antenna), drawn by the
  local piko() in src/scenes.js (same drawing as the kit's comicPiko, but
  the fill is locked to Peka yellow instead of COMIC.accent).
- The story advances through the dialogue: the night bubble (bubble2, two
  lines) swaps at every night line, the morning bubble swaps at every
  morning line, and the caption strip carries one fact per line (`stripAt`
  in src/scenes.js). The terminal window stages its reveals with the
  voice: DONE + "1 file jadi" with l4, the benchmark line with l5. Panel
  layouts are the 8s layouts verbatim (same coordinates, same clearances,
  already verified). On-screen text (mandatory, all present): "DONE" +
  "1 file jadi", "Terminal-Bench 2.1: 90,6 - klaim vendor" (the benchmark
  always carries the vendor-claim label, on screen), one concrete try-step
  ("Coba dulu: npx @deepseek-ai/dsh web" on the caption strip). No
  URL/link on screen. No theme name printed on the final design (internal
  label only: "terminal / terminal green").

## Beats

| # | t (s) | what happens | bridge into the next | sound |
|---|---|---|---|---|
| 1 | 0.0-2.91 | Night panel (dark terminal green), terminal window ">_ ngoding pakai apa?" + blinking cursor block, Piko confused, "?" thought, bubble "Ngoding pakai DeepSeek, bukan Claude?!", strip "Ngoding pakai DeepSeek, bukan Claude?" | l2 | soft pad, rising fifth at the wake (1.0s) |
| 2 | 2.91-7.75 | Bubble "Harness open-source, lisensi MIT!", strip "Harness agen open-source, MIT" | l3 | pluck |
| 3 | 7.75-14.0 | Bubble "Satu perintah saja, Web UI kebuka!", strip "Satu perintah, Web UI kebuka", thought "MIT?" pops at 12.2s in the 3.1s quiet gap before the morph | cursor circle morphs into the DONE check circle at 14.0s | pluck, paper swish into the morph |
| 4 | 14.0-18.09 | Morning panel, DONE check circle + green rays, terminal shows DONE + "1 file jadi", Piko happy, bubble "Open-weight dan murah!", strip "Open-weight dan murah" | l5 | warm chord, plucks, payoff hit on the morph |
| 5 | 18.09-21.66 | Benchmark line fades into the terminal: "Terminal-Bench 2.1: 90,6 - klaim vendor", bubble "Klaim vendor, 90,6!", strip "Bench 90,6 - klaim vendor" | l6 | pluck |
| 6 | 21.66-25.46 | Bubble "Kimi juga open-weight!", strip "Kimi K3.1 Pro, 1 juta token" | l7 | pluck |
| 7 | 25.46-30.0 | Bubble "Coba sendiri dulu!", strip "Coba dulu: npx @deepseek-ai/dsh web", tail | loops | warm close, pluck |

## Sound plan

Same score as the 8s version, stretched: night pad 0-14.1, morning pad
14.0-30.05, hero motif at the wake, one pluck per dialogue pop, arpeggio
from the morph, paper swish into the morph at 13.7-14.05. Loudest hit the
morph at 14.0s, in the payoff act; the 3.1s gap before it (l3 ends 11.20,
l4 starts 14.28) is the silence before the payoff, with a late "MIT?"
thought at 12.2s as a mid-gap beat.
The score is kept for the review's story-arc measurement, but the
delivered mix is voice-over only: the score sits at -60 dB under the
voice (piece.json "voice.music"), inaudible. No background music track.

## Voice-over (Edge TTS id-ID-ArdiNeural, no music bed)

- Takes in voice/: l1-l7.mp3. l1-l6 at +0% rate, l7 at +15% (its +0% take
  ran 4.42s and would have pushed the voice past 30s). voice.mjs joins
  them into voice.wav. Generated with the `edge_tts` module from the
  piko-app venv (`~/workspace/piko-app/venv/bin/python -m edge_tts --voice
  id-ID-ArdiNeural --file <line>.txt --write-media <id>.mp3 --rate +X%`).
  No ElevenLabs.
- Timing (voice.json): l1 0.30-2.31 (2.49 w/s), l2 2.91-7.15 (2.13 w/s),
  l3 7.75-11.20 (2.89 w/s), l4 14.28-17.69 (2.06 w/s), l5 18.09-21.25
  (2.84 w/s), l6 21.66-25.16 (2.57 w/s), l7 25.46-29.31 (2.60 w/s); total
  voice 29.81s inside the 30.0s piece. The l3 `after` is 3.08s so l4
  starts 0.28s after the 14.0s morph. Word times are estimated
  (faster-whisper is not installed); no scene cues on individual words.
- The speech bubbles pop in sync with the lines: night 0.35 / 2.96 /
  7.80, morning 14.33 / 18.14 / 21.71 / 25.51 (line start + 0.05s,
  hardcoded in src/scenes.js, coupled to voice/voice.json — if the
  script timing changes, update both). Strips switch at the line starts.
- Mix: voice over the score at -60 dB, loudness corrected to -14.5 LUFS
  integrated (see LOG.md for the correction steps).

## Claims and sources (web-checked 16 Nov 2026, same as the 8s version)

- DeepSeek Harness (dsh): an open-source agent harness, MIT license,
  developer preview. Repo: github.com/deepseek-ai/deepseek-harness.
  Quick start: `npx @deepseek-ai/dsh web` (Web UI at 127.0.0.1:3080).
  Sources: the repo itself + DeepSeek's launch post (2026-11-04),
  checked 16 Nov 2026.
- DeepSeek-V4.1-Flash-1017: open weights, MIT license, 763B stored
  parameters, 1M context. Terminal-Bench 2.1 score 90.6 — a VENDOR CLAIM,
  always labelled "klaim vendor" on screen and in the voice.
- Kimi K3.1 Pro: open weights, released 4 Nov 2026, 2.8T total / 104B
  active parameters, 1M context, Terminal-Bench 4.0 score 65.7 — also a
  vendor claim (the piece does not state its score, only "juga
  open-weight, konteks satu juta token").
- No "DeepSeek menang" verdict anywhere: the V2EX thread and the Bug Hunt
  Bench (+3.6) sit inside the noise. The piece ends "Tidak ada yang jelas
  menang. Coba sendiri, satu tugas kecil."
- The try-step `npx @deepseek-ai/dsh web` is real (the harness quick
  start); the Web UI opens in the browser.
