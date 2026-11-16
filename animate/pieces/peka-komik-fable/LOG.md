# LOG: Komik Peka #01 — Claude Fable 5.2

- 2026-11-16: Episode #01 of the "Komik Peka" series, built from the
  approved `peka-komik` look (style + reference piece read-only, not
  modified). Variant: `COMIC_MOTIF = 'trophy'`, dark navy + gold palette
  (ground1 #0e1430, ground2 #16204d, accent #ffd60a locked for Piko,
  accent2 #e8b93c gold). Story: Piko confused by the price cut
  ("$10/$50 jadi $8/$40") and "Model termurah, kok nomor satu?!", then
  trophy + giant gold "65" + burst "NOMOR 1", bubble "Fable 5.2,
  cobain!", caption strip "Buka Claude, pilih Fable 5.2".
- 2026-11-16: Facts re-verified by web search before building (see
  brief.md): Fable 5.2 released 9 Nov 2026, $8/$40 per M tokens (from
  $10/$50), 1M context, AA Intelligence Index 65, first, ahead of
  Gemini 4 Carbon (60); Mythos 5.2 restricted, never promised.
- 2026-11-16: Voice-over: Edge TTS id-ID-ArdiNeural via the piko-app
  venv (`edge_tts` module; no ElevenLabs). Night line +0%, morning line
  +30% (default rate ran 3.79s, too long for the 8.0s piece; +30% =
  2.92s). Timing: night 0.30-2.58s (2.63 w/s), morning 4.30-7.22s
  (2.40 w/s); bubbles pop 0.35s / 4.35s in sync. Word times estimated
  (no faster-whisper).
- 2026-11-16: Polish pass on the eyeballed stills (f60/f168): burst
  "NOMOR 1" text spilled outside the star (50px in r170) — fixed to
  44px in r180 at (0.75, 0.615), now fully inside, 43px above the tape;
  morning bubble tail re-aimed from the antenna ball to Piko's head.
  Night still clean on first check. No text cut off, no unintended
  overlaps, margins consistent.
- 2026-11-16: Export note: the first `export.mjs --share` run was
  killed by a runtime restart after final.mp4 was written (192/192
  frames, 1080x1920 yuv420p 8.0s) but before share.mp4; share.mp4 was
  re-encoded from final.mp4 with the tool's own settings (libx264 CRF
  24, preset slow, yuv420p, aac 192k) instead of re-running the full
  export. No frames were re-rendered.
- 2026-11-16: Review PASS — cuts on grid PASS, morph at 4s on grid
  PASS, narration density PASS (2.63 / 2.40 w/s), story arc PASS (2/2,
  gift p90 -14.2 vs -15.2), text PASS (0 cut-off/overlap, 0 in safe
  zone), dead beats PASS, loudest 7.3s in payoff act. Loudness: export
  single-pass read -13.8 LUFS (review ebur128); corrected with two-pass
  loudnorm to -14.5 + a -0.4 dB trim, remux + share re-encode; review
  now reads -14.5 LUFS integrated, true peak -3.6 dBFS. Known minor:
  silence before the loudest hit 0.0s (craft wants 0.5-4s) — the voice
  fills the gap, same as peka-komik.
- 2026-11-16: Export OK: renders/final.mp4 (9.7 MB) + renders/share.mp4
  (3.5 MB, 1080x1920 yuv420p 24fps 8.0s, aac, 192/192 frames) +
  renders/final-captions.mp4 + narration.srt. Stills kept in renders/:
  still-night.png (f60) + still-morning.png (f168). NOT posted anywhere
  (per task); no commit/push.
