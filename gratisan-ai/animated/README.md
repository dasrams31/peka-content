# Gratisan AI animated reel template

Motion-graphics reel for Peka Gratisan AI (standard reels: animated,
fullscreen 4K, FYP). Same pipeline family as `hm/animated/`,
`spill/animated/` and `bansos/animated/`. Base design = the locked
ticket system (`ga_design.py` + `bansos_design.py` tiket theme):
cream ticket + red stamp, syarat/cara-klaim cards, yellow closing.
Adapted to vertical with slight modifications only, no redesign.

## Files

- `scene.html` — 4 vertical scenes (16 s total, 4 s each):
  1. ticket (cream card slides in, red stamp slams at ~2.6 s, fields),
  2. syaratnya (cream card, check rows stagger in),
  3. cara klaim (numbered rows + source line),
  4. closing (AI GRATIS BUAT KAMU + band + CTAs).
  Built from a spec via `window.buildScene(spec)`, animated via
  `window.renderAt(t)` (deterministic frame-by-frame).
- `render.py` — Playwright frame renderer (4K via scale 2.0).
- `assets/` — Poppins + DejaVu fonts and the P mascot.

## Reel spec format

The edition spec used by `ga_design.py` works as-is:
`{"program", "category", "stamp", "fields": {...}, "syarat": [...],
"steps": [...], "band", "subtitle", "ctas": [...]}`

## Worker render commands (per edition)

```bash
cd ~/workspace/peka-content/gratisan-ai/animated
TRACK=$(~/workspace/peka-content/brand/music/pick_reel_track.sh)  # ONCE per edition
~/workspace/megumi/venv/bin/python render.py <out_dir>/spec.json <out_dir>/frames 24 16 2.0
ffmpeg -y -framerate 24 -i <out_dir>/frames/f%04d.png -ss 10 -t 16 -i "$TRACK" \
  -filter_complex "[0:v]scale=2160:3840[vout];[1:a]afade=t=in:st=0:d=0.5,afade=t=out:st=15.5:d=0.5[aout]" \
  -map "[vout]" -map "[aout]" -c:v libx264 -pix_fmt yuv420p -r 24 -c:a aac -b:a 160k -t 16 \
  <out_dir>/ga-reel.mp4
ffmpeg -y -ss 1 -i <out_dir>/ga-reel.mp4 -frames:v 1 -q:v 2 <out_dir>/ga-reel-cover.jpg
rm -rf <out_dir>/frames
```

Music credit: `Music: <Judul> by Kevin MacLeod` (title = file name without
`-kevin-macleod.mp3`, dashes to spaces, title case).
Threads keeps the 3-slide carousel; the animated reel goes to IG + FB.
