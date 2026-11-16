# Brief: Komik Peka #03 — Tier-list AI buat skripsi

## The idea in one sentence

Piko bingung dikepung nama-nama AI buat skripsi, lalu Peka kasih tier-list jujur: Elicit dan ChatGPT tier S, sisanya A/B/D — lengkap dengan batas gratis tiap tool, supaya penonton cek kuota dulu sebelum berharap.

## Format and spec

- Format: F2 morph chain, same as peka-komik (moon becomes sun at 4.0s).
- Size: 1080x1920, 24fps, 120 BPM, 8s = 192 frames
- Style: peka-komik (kit comic). Variant `tier`: cream ground #f5f1e8, episode accent red #c1272d (tier chips, limit lines, arrow); Piko keeps his Peka-yellow P #ffd60a (kit accent, unchanged).
- Hero: Piko vector (yellow letter P, one black eye, small smile, antenna with ball).
- Motif: tier bars S/A/B (comicMotif 'tier', top centre-right of the morning scene).

## Beats (same morph as peka-komik)

| # | t (s) | what happens | bridge into the next | sound |
|---|---|---|---|---|
| 1 | 0.0-4.0 | Night panel, Piko confused, six tool-name chips pop in one by one around him (Elicit, ChatGPT, NotebookLM, SciSpace, Gemini, Gamma), speech bubble "AI buat skripsi, mana yang tier S?" | moon morphs into the sun at 4.0s | soft pad, rising fifth at the wake (1.0s), paper swish into the morph |
| 2 | 4.0-8.0 | Cream morning panel, sun rays, tier rows pop in one by one (S, A, B, D), red arrow up to the S row, Piko happy, bubble "Cek batas gratisnya dulu!" | loops | warm chord, plucks per tier row, payoff hit on the sun |

## The tier list (on screen, scene 2)

| Tier | Tools | Free-limit line on screen |
|---|---|---|
| S | Elicit, ChatGPT | Cari jurnal + chat teks gratis |
| A | NotebookLM, SciSpace | 50 sumber/notebook · 100 kredit/bln |
| B | Gemini | Kuota refresh tiap 5 jam |
| D | Gamma | 400 kredit, sekali saja |

The ranking is Peka's editorial take, not a benchmark — no vendor claim is made, and nothing promises "skripsi selesai 1 hari". The angle is honest: check the free limit first.

## Sound plan

Same score as peka-komik (copied): loudest hit the morph at 4.0s.
The score is kept for the review's story-arc measurement, but the
delivered mix is voice-over only: the score sits at -60 dB under the
voice (piece.json "voice.music"), inaudible (gap/tail segments measure
mean -73 dB). No background music track was added.

## Voice-over (Edge TTS id-ID-ArdiNeural, no music bed)

- Takes in voice/: night.mp3 "AI buat skripsi, mana yang tier S?" (+0%), morning.mp3
  "Elicit dan ChatGPT tier S. Cek batas gratisnya." (+0%). voice.mjs joins them into voice.wav.
- Timing (voice.json): night 0.30-3.02s (7 words, 2.58 w/s), morning 4.30-7.26s
  (8 words, 2.70 w/s), total voice 7.0s inside the 8.0s piece. Line 2 starts
  0.30s after the 4.0s morph. Word times are estimated (faster-whisper
  is not installed); no scene cues on individual words.
- The speech bubbles pop in sync with the lines: night bubble 0.35s,
  morning bubble 4.35s (hardcoded in src/scenes.js, coupled to
  voice/script.json — if the script timing changes, update both).
- Mix: voice over the score at -60 dB, sidechain-ducked, loudness
  corrected to -14.5 LUFS integrated (the export's single-pass loudnorm
  landed at -14.2; a -0.3 dB trim on renders/audio.wav + remux of the
  three mp4s brought the review reading to -14.5), true peak -2.7 dBFS.

## Layout notes (extra polish pass, verified on the stills)

- Every right-hand element ends at x <= 940 (phone UI strip), except Piko
  himself (column x 770-958, same as peka-komik — hero drawing, not text).
- Top chip row sits 50px below the speech bubble; tier rows clear the bubble
  by 23px and the caption strip by ~190px; Piko's column never touches the
  tier strips (end x 740) or the sun rays.
- Morning bubble is drawn FIRST so the tier strips (drawn after) cover the
  band where its tail crosses rows S/A; the tail tip stays visible past the
  strips, pointing at Piko's antenna (verified on a 3x crop of the tail region).
- Night bubble tail points exactly at the top of Piko's antenna ball; its long
  white triangle clears the Elicit chip (verified on a crop).
- Sun/moon at (0.80, 0.17): the sun clears the morning bubble and the tier
  motif; all rays clear the bubble. No element is cut by the frame; no text
  touches the panel frame or another element.

## Claims and sources (web-checked 2026-11-16)

- NotebookLM free: 100 notebooks, 50 sources per notebook — Google's
  Gemini Notebook plans page, as read 15 Oct / 8 Nov 2026
  (aialleyway.com/notebooklm-pricing, whizi.io/resources/notebooklm-pricing).
- SciSpace Basic free: 100 Agent credits a month, no rollover — SciSpace
  pricing page, as read Oct 2026 (toolsworld.ai/scispace, freedom251.com/apps/scispace).
- Gemini app free: compute-based allowance refreshes every 5 hours until a
  weekly limit — Google Gemini Apps Help, as read Nov 2026
  (limitdigest.com/guides/gemini-usage-limit-reached, nixm.ai/learn/gemini-free-limits).
- Gamma free: 400 credits at signup, never refill — gamma.app pricing page,
  as read Oct-Nov 2026 (tovorify.com/blog/gamma-pricing-2026,
  aitoolversus.com/2026/10/gamma-free-or-plus-what-happens-after.html).
- S-row line "Cari jurnal + chat teks gratis" states no number; Elicit's free
  plan and ChatGPT's free tier both exist, so the line is a generic capability
  statement, not a vendor claim.
- All four limit figures above were re-checked on the web the morning of the
  build (16 Nov 2026); no line had to be removed.
