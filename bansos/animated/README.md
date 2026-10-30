# Bansos animated reel template

Motion-graphics reel for Peka bansos (standard reels 2026-10-25: animated,
2K, FYP). Same pipeline family as `peka-content/spill/animated/` and
`peka-content/hallmark/animated/`, with the bansos ticket identity
(kuning theme: yellow #ffd60a, black #111, red #D63026 stamp).

## Files

- `scene.html` — 4 vertical scenes (15 s total, 3.75 s each):
  1. cover (kicker INFO BANSOS + headline + nilai + 100% GRATIS stamp),
  2. syarat (4 rows sliding in),
  3. cara klaim (4 numbered steps sliding in),
  4. closing (jangan sampai kelewatan + kode + bonus Telegram +
     SATU pertanyaan penutup + follow/gabung/save).
  Built from a spec via `window.buildScene(spec)`, animated via
  `window.renderAt(t)` (deterministic frame-by-frame).
- `render.py` — Playwright frame renderer.
- `assets/` — Poppins + DejaVu fonts and the P mascot.

## Reel spec format

```json
{"program": "Claude Max Gratis 6 Bulan buat OSS",
 "headline": ["CLAUDE MAX", "GRATIS 6 BULAN", "BUAT OSS"],
 "headline_hl": 1,
 "nilai": "Claude Max 20x gratis 6 bulan",
 "syarat": ["...", "...", "...", "..."],
 "steps": ["...", "...", "...", "..."],
 "closing": ["...", "..."],
 "closing_q": "Kamu maintainer proyek apa?"}
```

Exactly 4 syarat and 4 steps. All on-screen copy comes from the spec:
headline, sub (from `nilai`), syarat, steps, closing lines and closing
question. Never hardcode edition copy in `scene.html` (the 2026-10-30
Claude OSS reel shipped with the previous edition's hardcoded
"VPS GRATIS TOKEN MUSE" headline and closing because of this).

Theme: kuning (yellow #ffd60a background, black cards, red GRATIS
stamp), matching the `kuning` slide theme.

## Render commands (per edition)

```bash
cd ~/workspace/peka-content/bansos/animated
# Music: ONE pick per reel via pick_reel_track.sh; reuse the same track
# if a slideshow was already rendered for this edition (no second pick).
~/workspace/megumi/venv/bin/python render.py <out_dir>/bansos-reel-spec.json <out_dir>/frames 24 15 1.3333
ffmpeg -y -framerate 24 -i <out_dir>/frames/f%04d.png -ss 10 -t 15 -i <track> \
  -filter_complex "[0:v]scale=1440:2560[vout];[1:a]afade=t=in:st=0:d=0.5,afade=t=out:st=14.5:d=0.5[aout]" \
  -map "[vout]" -map "[aout]" -c:v libx264 -pix_fmt yuv420p -r 24 -c:a aac -b:a 160k -t 15 \
  <out_dir>/bansos-reel.mp4
ffmpeg -y -ss 1 -i <out_dir>/bansos-reel.mp4 -frames:v 1 -q:v 2 <out_dir>/bansos-reel-cover.jpg
rm -rf <out_dir>/frames
```

Music credit: `Music: <Judul> by Kevin MacLeod` (title = file name without
`-kevin-macleod.mp3`, dashes to spaces, title case).

## Fallback

If the animated render fails for any reason, fall back to the slideshow
script `~/workspace/peka-content/tools/make_reel.sh` with the same picked
track, post as usual, and say so in the report. Never leave the reel slot
empty once the carousel is live.
