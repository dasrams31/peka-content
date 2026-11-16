# Brief: Komik Peka #01 — Claude Fable 5.2: termurah, kok nomor satu?

## The idea in one sentence

Piko bingung: model termurah kok jadi nomor satu? Lalu trofi + angka raksasa
"65" menjawabnya — Fable 5.2, harga turun, skor naik — digambar gaya komik
navy + emas dengan motif trofi.

## Format and spec

- Format: F2 morph chain, same as peka-komik (gold moon becomes yellow sun at 4.0s).
- Size: 1080x1920, 24fps, 120 BPM, 8s = 192 frames
- Style: `peka-komik` (style, read-only) + variant `src/options.js`:
  `COMIC_MOTIF = 'trophy'`; palette dark navy + gold — ground1 `#0e1430`
  (deep navy), ground2 `#16204d` (lighter navy), accent `#ffd60a` (Piko
  yellow, locked — never changed, or Piko renders wrong), accent2 `#e8b93c`
  (gold: moon, giant "65"), ink `#141210`, paper `#f5f1e8`.
- Hero: Piko as a vector (yellow letter P, one eye, antenna), from the kit.
- On-screen text (mandatory, all present): giant gold "65", "$8/$40"
  (on the price tag "$10/$50 jadi $8/$40"), one concrete try-step
  ("Buka Claude, pilih Fable 5.2" on the caption strip). No URL/link on
  screen. No theme name printed on the final design (internal label only:
  "trophy / navy + gold").

## Beats

| # | t (s) | what happens | bridge into the next | sound |
|---|---|---|---|---|
| 1 | 0.0-4.0 | Night panel (deep navy), Piko confused, "?" bubbles pop in, price tag "$10/$50 jadi $8/$40", speech bubble "Model termurah, kok nomor satu?!" | gold moon morphs into the yellow sun at 4.0s | soft pad, rising fifth at the wake (1.0s), paper swish into the morph |
| 2 | 4.0-8.0 | Navy morning panel, sun rays, trophy motif + giant gold "65" + burst "NOMOR 1", Piko happy, bubble "Fable 5.2, cobain!", caption strip "Buka Claude, pilih Fable 5.2" | loops | warm chord, plucks per beat, payoff hit on the sun |

## Sound plan

Same score as peka-komik (copied): loudest hit the morph at 4.0s.
The score is kept for the review's story-arc measurement, but the
delivered mix is voice-over only: the score sits at -60 dB under the
voice (piece.json "voice.music"), inaudible. No background music track.

## Voice-over (Edge TTS id-ID-ArdiNeural, no music bed)

- Takes in voice/: night.mp3 "Model termurah, tapi jadi nomor satu?"
  (+0%), morning.mp3 "Fable 5.2, skor 65, harga lebih murah." (+30% rate —
  the default-rate take ran 3.79s and would have ended past 8.0s; at +30%
  it is 2.92s). voice.mjs joins them into voice.wav. Generated with the
  `edge_tts` module from the piko-app venv
  (`~/workspace/piko-app/venv/bin/python -m edge_tts`); no ElevenLabs.
- Timing (voice.json): night 0.30-2.58s (2.63 w/s), morning 4.30-7.22s
  (2.40 w/s), total voice 7.92s inside the 8.0s piece. Line 2 starts
  0.30s after the 4.0s morph. Word times are estimated (faster-whisper
  is not installed); no scene cues on individual words.
- The speech bubbles pop in sync with the lines: night bubble 0.35s,
  morning bubble 4.35s (hardcoded in src/scenes.js, coupled to
  voice/script.json — if the script timing changes, update both).
- Mix: voice over the score at -60 dB, loudness corrected to -14.5 LUFS
  integrated (export single-pass landed at -13.8 per review's ebur128;
  two-pass loudnorm to -14.5 + a -0.4 dB trim, then remux + share
  re-encode; review now reads -14.5 LUFS, true peak -3.6 dBFS).

## Polish pass (extra, on top of review.mjs — 2026-11-16, eyeballed stills)

- Still f60 (night): alignment/margins clean — price tag 33px below the
  year tag tape and 33px above the bubble; "?" thoughts clear of the year
  tag, price tag and bubble tail; Piko's eye + sweat drop visible; the
  bubble tail points at Piko's head. No element cut off.
- Still f168 (morning): burst "NOMOR 1" first rendered with its "1"
  spilling outside the star (text 50px in r170) — fixed to text 44px in
  r180, centre moved to (0.75, 0.615): the whole word now sits inside the
  star, 43px clear of the caption tape, 76px from the frame edge.
  Bubble tail re-aimed from the antenna ball to Piko's head
  (tail tip LX(0.46)+30, LY(0.62)-160). Sun rays clear the bubble;
  trophy clears the bubble tail by ~37px; "65" clears the bubble by 53px
  and the burst by ~200px; Piko's bottom sits 71px above the tape.

## Claims and sources (web-checked 16 Nov 2026)

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
  not benchmark-only (lesson: the 12 Nov benchmark-only special got
  Threads 5 likes / 80 views). No price or score is exaggerated: the
  per-task cost caveat (higher token use per task at Max effort) is real
  but out of scope for an 8s comic — the piece claims only list price
  and index score, both sourced above.
