# HM animated reel template

Motion-graphics reel for Peka Homeless Media (standard reels 2026-10-25:
animated, 4K, FYP). Same pipeline family as `peka-content/spill/animated/`
and `peka-content/bansos/animated/`, with the HM premium theme locked
2026-10-29 (warm paper #f7f4ed, wide margins, serif headline, one thin
gold line, no gradient/glow/large colour blocks).

## Files

- `scene.html` — 4 vertical scenes (16 s total, 4 s each):
  1. cover (AI NEWS header + lockup, hero image with slow zoom,
     serif headline, sub, GESER),
  2. Yang berubah (3 numbered points sliding in),
  3. Bisa langsung dicoba (3 numbered steps in a white card),
  4. closing (one question + follow/save/community + gold band).
  Built from a spec via `window.buildScene(spec)`, animated via
  `window.renderAt(t)` (deterministic frame-by-frame).
- `render.py` — Playwright frame renderer (4K via scale 2.0).
- `assets/` — Poppins + DejaVu + DejaVu Serif fonts and the P mascot.

## Reel spec format

```json
{"date": "JUMAT, 30 OKTOBER 2026", "source": "SUMBER: GOOGLE BLOG",
 "hero": "file:///abs/path/to/hero.webp",
 "headline": ["line 1", "line 2", "line 3"], "sub": "...",
 "points": ["...", "...", "..."], "steps": ["...", "...", "..."],
 "question": "...", "band": "GEMINI NOTEBOOK - BUKU TEKS GRATIS",
 "shortlink": "https://s.peka.ai.id/xxxxxx"}
```

`shortlink` (blog shortlink, no-link rule 31 Okt 2026) is printed in the
closing scene as `LINK BLOG: s.peka.ai.id/xxxxxx`. Omit it only for
editions with no link.

## Worker render commands (per edition)

```bash
cd ~/workspace/peka-content/hm/animated
TRACK=$(~/workspace/peka-content/brand/music/pick_reel_track.sh)  # ONCE per edition
~/workspace/megumi/venv/bin/python render.py <out_dir>/reel-spec.json <out_dir>/frames 24 16 2.0
ffmpeg -y -framerate 24 -i <out_dir>/frames/f%04d.png -ss 10 -t 16 -i "$TRACK" \
  -filter_complex "[0:v]scale=2160:3840[vout];[1:a]afade=t=in:st=0:d=0.5,afade=t=out:st=15.5:d=0.5[aout]" \
  -map "[vout]" -map "[aout]" -c:v libx264 -pix_fmt yuv420p -r 24 -c:a aac -b:a 160k -t 16 \
  <out_dir>/hm-reel-animated.mp4
ffmpeg -y -ss 1 -i <out_dir>/hm-reel-animated.mp4 -frames:v 1 -q:v 2 <out_dir>/hm-reel-animated-cover.jpg
rm -rf <out_dir>/frames
```

Music credit: `Music: <Judul> by Kevin MacLeod` (title = file name without
`-kevin-macleod.mp3`, dashes to spaces, title case).

## Note

The slideshow script `~/workspace/peka-content/tools/make_reel.sh` is only
a fallback. Animated is the default for HM reels; a slideshow render must
be disclosed in the report.
