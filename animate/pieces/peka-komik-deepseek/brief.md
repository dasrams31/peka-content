# Brief: Komik Peka #02 — Ngoding pakai DeepSeek, bukan Claude? (terminal)

## The idea in one sentence

Piko bingung di depan jendela terminal ("ngoding pakai apa?"), lalu
kursor berubah jadi centang DONE: satu file jadi — coba satu tugas kecil
dulu. Digambar gaya komik terminal: ground hijau-hitam, panel jendela
kode, bubble dialog, Piko vektor kuning.

## Format and spec

- Format: F2 morph chain (cursor circle -> DONE check circle at 4.0s).
- Size: 1080x1920, 24fps, 120 BPM, 8s = 192 frames
- Style: peka-komik, variant `terminal` (src/options.js, COMIC_MOTIF
  'terminal'). Palette: ground malam #0a1f14, ground pagi #0f3d24,
  aksen hijau terminal #3ddc84, kursor #8df0b2, tinta #101210, kertas
  caption #dff0e2. Piko tetap huruf P kuning #ffd60a (local piko() di
  src/scenes.js — comicPiko dari kit mengisi dari COMIC.accent, yang di
  sini hijau terminal).
- Hero: Piko vektor (huruf P kuning, satu mata, antena), bingung ->
  happy, hop di morph.

## Beats

| # | t (s) | what happens | bridge into the next | sound |
|---|---|---|---|---|
| 1 | 0.0-4.0 | Panel malam hijau-hitam; jendela terminal (prompt ">_ ngoding pakai apa?" + baris kode), Piko bingung, bubble "?" , bubble "Ngoding pakai DeepSeek, bukan Claude?!" | lingkaran kursor morph jadi lingkaran centang DONE di 4.0s | soft pad, rising fifth at the wake (1.0s), paper swish into the morph |
| 2 | 4.0-8.0 | Ground hijau terminal lebih terang; lingkaran centang besar + rays hijau; jendela terminal menampilkan centang + "DONE" + "1 file jadi" + label benchmark; Piko happy, bubble "Coba satu tugas kecil dulu!" | loops | warm chord, plucks, payoff hit |

## Sound plan

Same score as peka-komik (copied): loudest hit the morph at 4.0s.
The score is kept for the review's story-arc measurement, but the
delivered mix is voice-over only: the score sits at -60 dB under the
voice (piece.json "voice.music"), inaudible. No background music track.

## Voice-over (Edge TTS id-ID-ArdiNeural, no music bed)

- Takes in voice/: night.mp3 "Ngoding pakai DeepSeek, bukan Claude?"
  (+0%), morning.mp3 "Open-weight dan murah. Coba satu tugas kecil."
  (+20% so the line fits: at +0% it ran 3.41s trimmed and would have
  ended at 7.71s with no tail room; at +20% it is 2.84s). voice.mjs
  joins them into voice.wav. Naskah TIDAK diubah, hanya rate baris 2.
- Timing (voice.json): night 0.30-2.31s (2.49 w/s), morning 4.30-7.15s
  (2.46 w/s), total voice 7.95s inside the 8.0s piece. Line 2 starts
  0.30s after the 4.0s morph. Word times are estimated (faster-whisper
  is not installed); no scene cues on individual words.
- The speech bubbles pop in sync with the lines: night bubble 0.35s,
  morning bubble 4.35s (hardcoded in src/scenes.js, coupled to
  voice/script.json — if the script timing changes, update both).
- Mix: voice over the score at -60 dB, sidechain-ducked, loudness
  corrected to -14.5 LUFS integrated (export single-pass landed -13.2;
  two-pass loudnorm with measured values, audio.wav now -14.52 LUFS,
  final.mp4 audio -14.55 LUFS, true peak -2.8 dBFS; the pre-correction
  mix is kept as renders/audio-singlepass.wav).

## Layout notes (polish pass)

- Bubble tails are narrow triangles from the bubble's bottom edge
  (local bubble()/bubble2()), NOT the kit's wide left-side tail: the
  wide tail's diagonal crossed the terminal prompt text and the DONE
  text. Tail tips land at (hx-8, hy-202), beside the antenna ball,
  never touching it; the tail passes right of the prompt text and the
  DONE block with >= 10px clearance.
- Piko stands right (0.72, 0.60) so the tail clears the prompt; the
  "?" bubble sits inside the window at (0.81, 0.48) r 56 (moved in from
  0.86 after review flagged it under the phone UI strip).
- Morning bubble (0.40, 0.29) w 720 clears the check-circle rays by
  ~19px; the DONE check circle (0.80, 0.17) r 80 clears the bubble by
  76px.
- Caption strips: night mirrors the voice line; morning carries the
  verified first step "Coba dulu: npx @deepseek-ai/dsh web".

## Claims and sources (web-checked 16 Nov 2026)

- DeepSeek Harness (dsh): open-source agent harness by DeepSeek,
  MIT licence, developer preview, repo github.com/deepseek-ai/deepseek-harness,
  quick start `npx @deepseek-ai/dsh web` (Web UI at 127.0.0.1:3080).
  Sources: repo README via sitepoint.com/deepseek-harness-developer-preview,
  vdf.ai/blog/deepseek-harness (checked 4 Nov 2026).
- DeepSeek-V4.1-Flash-1017: MIT, 763B stored parameters (552B backbone
  + 196.6B Engram), 8B active prefill / 16B decode, 1017 weight update
  17 Oct 2026. Terminal-Bench 2.1 90.6 is a VENDOR CLAIM (DeepSeek's
  own model card, run in DeepSeek's own harness, minimal mode) — shown
  on screen as "Terminal-Bench 2.1: 90,6 - klaim vendor".
  Sources: huggingface deepseek-ai/DeepSeek-V4.1-Flash-1017 via
  singularitybyte.com, vdf.ai, willitrunai.com.
- Kimi K3.1 Pro: open weights 4 Nov 2026 (repo created 2 Nov), 2.8T
  total / 104B active, 1M context, Terminal-Bench 4.0 65.7 VENDOR CLAIM
  (Moonshot model card; custom licence with a $20M revenue term, not
  MIT). Not shown on screen; context only.
  Sources: llms.blog, theainewsreport.com, dsebastien.net.
- V2EX thread (88 replies) on deep-seek harness real-project experience
  vs Claude Code: per trending.md 16 Nov 2026 (internal trend log).
  Independent runs agree there is no clear winner: on the same model
  (V4.1 Flash 1017) DeepSeek Harness led Claude Code by 3.6 points on
  Bug Hunt Bench, inside run-to-run noise (productcompass.pm, 5 Nov 2026).
  No "DeepSeek menang" verdict anywhere on screen or in the voice-over.
