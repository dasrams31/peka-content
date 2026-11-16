# LOG: Komik Peka #02 — Ngoding pakai DeepSeek, bukan Claude? (terminal)

- 2026-11-16: Piece created from pieces/peka-komik (same story skeleton,
  cues, score, morph, voice pipeline). Variant: peka-komik style,
  COMIC_MOTIF 'terminal', terminal-green palette (ground #0a1f14 /
  #0f3d24, accent #3ddc84). Piko stays Peka yellow via a local piko()
  (kit comicPiko fills from COMIC.accent, which is green here).
  Voice: Edge TTS id-ID-ArdiNeural, night +0% (0.30-2.31s), morning
  +20% (4.30-7.15s; +0% ran 3.41s trimmed and left no tail room).
  Facts re-verified by web search 16 Nov 2026 (see brief.md): harness
  repo + `npx @deepseek-ai/dsh web` quick start, V4.1-Flash-1017 MIT /
  763B / Terminal-Bench 2.1 90.6 vendor claim, Kimi K3.1 Pro 2.8T /
  Terminal-Bench 4.0 65.7 vendor claim.
- 2026-11-16: Look check round 1 (stills 2.5s/7.0s) caught 2 defects,
  both fixed in code: the kit's wide left-side bubble tail crossed the
  terminal prompt text and the DONE text (replaced with narrow
  bottom-edge tails in local bubble()/bubble2()); the tail tip touched
  Piko's antenna ball (tip moved to hx-8, hy-202, beside the ball).
  Piko moved right (0.72, 0.60) and the "?" bubble to (0.86, 0.48) so
  the tail clears the prompt.
- 2026-11-16: Export OK: 192/192 frames in 40.8s, renders/final.mp4 +
  renders/share.mp4 (1080x1920 yuv420p 24fps 8.0s, aac).
- 2026-11-16: Review round 1 — cuts PASS, morph PASS, narration PASS
  (2.49 / 2.46 w/s), story arc PASS (2/2), text PASS (0 cut-off/overlap)
  with 1 WARN ("?" bubble under the phone UI strip, right edge 985 >
  940), loudness -13.2 LUFS. Fixed: "?" moved to (0.81, 0.48), right
  edge 931; loudness corrected with two-pass loudnorm (measured
  I -13.37 / TP -1.69 / LRA 3.80 / thresh -25.29 / offset -0.32) +
  remux into final.mp4 and share.mp4 (pre-correction mix kept as
  renders/audio-singlepass.wav).
- 2026-11-16: Review round 2 (final) — cuts on grid PASS, morph at 4s
  PASS, narration density PASS, story arc PASS (2/2), text PASS (0
  cut-off/overlap, 0 in safe zone), dead beats PASS, loudest 7.3s in
  payoff act, -14.3 LUFS integrated (review measure; ffmpeg measure on
  final.mp4 audio: -14.55 LUFS), true peak -2.8 dBFS. Known minor:
  silence before the loudest hit 0.0s (craft wants 0.5-4s), same as
  peka-komik — the voice fills the gap, so no silence is expected.
  Final stills (2.5s/7.0s) eyeballed: tails clear of prompt and DONE,
  antenna ball clear of the tail, rays clear of the bubble, no text
  cut off or overlapping. Polish pass lolos.
- 2026-11-16: Environment notes: a runtime restart mid-task wiped the
  global playwright npm package (browsers in ~/.cache/ms-playwright
  survived); reinstalled with `npm i -g playwright@1.65.1` (no
  `npx playwright install`, cache untouched). Export ran concurrently
  with the sibling tierlist piece's export; frames 40.8s, full export
  ~4-8 min wall time.
- 2026-11-16: NOT posted anywhere (build-only, per task). Awaits the
  user's posting decision.
