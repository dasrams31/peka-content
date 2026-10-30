# Prompt Harian animated reel template

Motion-graphics reel for Peka Prompt Harian (standard reels: animated,
fullscreen 4K, FYP). Same pipeline family as `hm/animated/`,
`spill/animated/` and `bansos/animated/`. Base design = the locked
2-slide carousel (`prompt_harian.py`): yellow/black flip, giant type,
chat-bubble teaser, yellow prompt bubble, tips, follow closing.
Adapted to vertical with slight modifications only, no redesign.

## Files

- `scene.html` — 4 vertical scenes (16 s total, 4 s each):
  1. cover (chips, giant PROMPT HARIAN, title, teaser bubble),
  2. prompt siap salin (yellow bubble, lines stagger in, shrink-to-fit),
  3. cara pakai (3 tips),
  4. closing (question + follow band + community line).
  Built from a spec via `window.buildScene(spec)`, animated via
  `window.renderAt(t)` (deterministic frame-by-frame).
- `render.py` — Playwright frame renderer (4K via scale 2.0).
- `assets/` — Poppins + DejaVu fonts and the P mascot.

## Reel spec format

The edition carousel spec works as-is:
`{"episode": 8, "category": "BISNIS", "title": "...",
"prompt": "...", "tips": ["...", "...", "..."]}`

## Worker render commands (per edition)

```bash
cd ~/workspace/peka-content/prompt/animated
TRACK=$(~/workspace/peka-content/brand/music/pick_reel_track.sh)  # ONCE per edition
~/workspace/megumi/venv/bin/python render.py <out_dir>/spec.json <out_dir>/frames 24 16 2.0
ffmpeg -y -framerate 24 -i <out_dir>/frames/f%04d.png -ss 10 -t 16 -i "$TRACK" \
  -filter_complex "[0:v]scale=2160:3840[vout];[1:a]afade=t=in:st=0:d=0.5,afade=t=out:st=15.5:d=0.5[aout]" \
  -map "[vout]" -map "[aout]" -c:v libx264 -pix_fmt yuv420p -r 24 -c:a aac -b:a 160k -t 16 \
  <out_dir>/prompt-reel.mp4
ffmpeg -y -ss 1 -i <out_dir>/prompt-reel.mp4 -frames:v 1 -q:v 2 <out_dir>/prompt-reel-cover.jpg
rm -rf <out_dir>/frames
```

Music credit: `Music: <Judul> by Kevin MacLeod` (title = file name without
`-kevin-macleod.mp3`, dashes to spaces, title case).
Threads keeps the 2-slide carousel; the animated reel goes to IG + FB.
