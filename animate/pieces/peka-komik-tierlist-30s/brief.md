# Brief: Komik Peka #03 — Tier-list AI buat skripsi (30 detik)

## The idea in one sentence

Piko bingung dikepung enam nama AI buat skripsi, lalu tujuh kalimat
menjawabnya satu per satu — batas gratisnya beda-beda, ada yang gratis
selamanya, ada yang sekali pakai langsung habis — lalu tier-list jujur
tersusun baris demi baris: Elicit dan ChatGPT tier S, NotebookLM dan
SciSpace tier A, Gemini tier B, Gamma tier D, supaya penonton cek kuota
dulu sebelum berharap.

## Format and spec

- Format: F2 morph chain, same as the 8s version (moon becomes sun),
  morph at 12.0s (the night era holds three short lines, so it ends
  earlier than #01/#02's 14.0s). 30s = 720 frames.
- Size: 1080x1920, 24fps, 120 BPM, 30s
- Style: `peka-komik` (style, read-only) + variant `src/options.js`:
  `COMIC_MOTIF = 'tier'`; palette cream + red — ground1 `#f5f1e8`
  (cream), ground2 `#efe8d8`, accent `#ffd60a` (Piko yellow, locked —
  never changed, or Piko renders wrong), accent2 `#c1272d` (red: tier
  chips, limit lines), ink `#141210`, paper `#f5f1e8`.
- Hero: Piko as a vector (yellow letter P, one eye, antenna), from the kit.
- The story advances through the dialogue: the six tool chips pop in two
  per night line, the night bubble swaps at every night line, the tier
  rows pop in with the morning line that names them (S with l4, A with
  l5, B and D with l6), the morning bubble swaps at every morning line,
  and the caption strip carries one fact per line (`stripAt` in
  src/scenes.js). Panel layouts are the 8s layouts verbatim (same
  coordinates, same clearances, already verified). On-screen text
  (mandatory, all present): the four tier rows with their verified
  free-limit lines (S "Cari jurnal + chat teks gratis", A "50
  sumber/notebook · 100 kredit/bln", B "Kuota refresh tiap 5 jam", D
  "400 kredit, sekali saja"), one concrete try-step ("Cek kuota dulu,
  Peka pilihkan" on the caption strip). No URL/link on screen. No theme
  name printed on the final design (internal label only: "tier /
  cream + red").

## Beats

| # | t (s) | what happens | bridge into the next | sound |
|---|---|---|---|---|
| 1 | 0.0-3.08 | Night panel (cream), Piko confused, chips Elicit + ChatGPT pop in, bubble "AI buat skripsi, mana yang tier S?", strip "Mana yang tier S?" | l2 | soft pad, rising fifth at the wake (1.0s) |
| 2 | 3.08-6.74 | Chips NotebookLM + SciSpace pop in, bubble "Enam nama, batasnya beda!", strip "Enam nama, batas beda-beda" | l3 | pluck |
| 3 | 6.74-12.0 | Chips Gemini + Gamma pop in, bubble "Gratis selamanya, atau sekali pakai!", strip "Sekali pakai, langsung habis", 2.25s of quiet before the morph | moon morphs into the sun at 12.0s | pluck, paper swish into the morph |
| 4 | 12.0-16.05 | Morning panel, sun rays, tier emblem, S row pops in, Piko happy, bubble "Elicit dan ChatGPT tier S!", strip "Elicit dan ChatGPT tier S" | l5 | warm chord, plucks, payoff hit on the morph |
| 5 | 16.05-20.33 | A row pops in, bubble "NotebookLM, SciSpace A!", strip "NotebookLM, SciSpace A" | l6 | pluck |
| 6 | 20.33-25.02 | B row pops in, then D row halfway through l6 (22.5s), bubble "Gemini B, Gamma D!", strip "Gemini B, Gamma D" | l7 | pluck |
| 7 | 25.02-30.0 | Bubble "Cek kuota dulu!", strip "Cek kuota dulu, Peka pilihkan", tail | loops | warm close, pluck |

## Sound plan

Same score as the 8s version, stretched to the 12.0s morph: night pad
0-12.1, morning pad 12.0-30.05, hero motif at the wake, one pluck per
dialogue pop, the tier-row arpeggio (4 plucks, one per row) from the
morph, paper swish into the morph at 11.7-12.05. Loudest hit the morph
at 12.0s, in the payoff act; the 2.25s gap before it (l3 ends 10.03,
l4 starts 12.28) is the silence before the payoff.
The score is kept for the review's story-arc measurement, but the
delivered mix is voice-over only: the score sits at -60 dB under the
voice (piece.json "voice.music"), inaudible. No background music track.

## Voice-over (Edge TTS id-ID-ArdiNeural, no music bed)

- Takes in voice/: l1-l7.mp3, all +0% rate. voice.mjs joins them into
  voice.wav. Generated with the `edge_tts` module from the piko-app venv
  (`~/workspace/piko-app/venv/bin/python -m edge_tts --voice
  id-ID-ArdiNeural --file <line>.txt --write-media <id>.mp3 --rate +0%`).
  No ElevenLabs.
- Timing (voice.json): l1 0.30-2.48 (3.21 w/s), l2 3.08-6.14 (2.61 w/s),
  l3 6.74-10.03 (3.04 w/s), l4 12.28-15.25 (2.70 w/s), l5 16.05-19.53
  (2.87 w/s), l6 20.33-24.32 (2.75 w/s), l7 25.02-28.57 (2.26 w/s);
  total voice 29.37s inside the 30.0s piece. The l3 `after` is 2.25s so
  l4 starts 0.28s after the 12.0s morph. Word times are estimated
  (faster-whisper is not installed); no scene cues on individual words.
- The speech bubbles pop in sync with the lines: night 0.35 / 3.13 /
  6.79, morning 12.33 / 16.10 / 20.38 / 25.07 (line start + 0.05s,
  hardcoded in src/scenes.js, coupled to voice/voice.json — if the
  script timing changes, update both). Strips switch at the line starts.
- Mix: voice over the score at -60 dB, loudness corrected to -14.5 LUFS
  integrated (see LOG.md for the correction steps).

## Claims and sources (web-checked 16 Nov 2026, same as the 8s version)

- Tier-list (Peka editorial take, not a benchmark): S = Elicit, ChatGPT
  ("Cari jurnal + chat teks gratis"); A = NotebookLM, SciSpace ("50
  sumber/notebook · 100 kredit/bln"); B = Gemini ("Kuota refresh tiap
  5 jam"); D = Gamma ("400 kredit, sekali saja").
- Sources, all re-checked the morning of 16 Nov 2026: NotebookLM free
  tier 100 notebooks / 50 sources per notebook; SciSpace Basic 100
  Agent credits per month; Gemini app allowance refreshes every 5
  hours; Gamma 400 credits at signup, never refilled.
- The try-step "Cek kuota dulu" is the honest action: every limit on
  screen is a verified free-tier limit, so the viewer checks their own
  quota before expecting more.
