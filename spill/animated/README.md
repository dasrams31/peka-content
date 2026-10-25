# SPILL animated reel template

Motion-graphics reel for SPILL Repo (standard reels 2026-10-25: animated,
2K, FYP). Same pipeline family as `peka-content/hallmark/animated/`.

## Files

 - `scene.html` — 5 vertical scenes (18.75 s total, 3.75 s each):
  1. cover (kicker edisi + REPO SKILL + agent highlight),
  2. repos 1-2 as dark cards sliding in,
  3. repos 3-5 as dark cards sliding in,
  4. closing (question + "link ada di komentar" + next agent),
  5. follow + community (standing rule 2026-10-25).
  Built from a spec via `window.buildScene(spec)`, animated via
  `window.renderAt(t)` (deterministic frame-by-frame).
- `render.py` — Playwright frame renderer.
- `spec-example.json` — example spec (FAKE repos, test only).
- `test-render.mp4` — test render from the example spec (NOT a real edition).

## Reel spec format

```json
{"agent": "ANTIGRAVITY", "episode": 5, "next": "CLAUDE",
 "repos": [{"name": "owner/repo", "stars": "12RB",
            "short": "one short sentence, max 110 chars"}]}
```

Exactly 5 repos. `short` is a fresh 1-sentence summary (not a truncation).

## Worker render commands (per edition)

```bash
cd ~/workspace/peka-content/spill/animated
TRACK=$(~/workspace/peka-content/brand/music/pick_reel_track.sh)  # ONCE per edition
~/workspace/megumi/venv/bin/python render.py <out_dir>/reel-spec.json <out_dir>/frames 24 18.75 1.3333
ffmpeg -y -framerate 24 -i <out_dir>/frames/f%04d.png -ss 10 -t 18.75 -i "$TRACK" \
  -filter_complex "[0:v]scale=1440:2560[vout];[1:a]afade=t=in:st=0:d=0.5,afade=t=out:st=18.25:d=0.5[aout]" \
  -map "[vout]" -map "[aout]" -c:v libx264 -pix_fmt yuv420p -r 24 -c:a aac -b:a 160k -t 18.75 \
  <out_dir>/spill<NN>-reel.mp4
ffmpeg -y -ss 1 -i <out_dir>/spill<NN>-reel.mp4 -frames:v 1 -q:v 2 <out_dir>/spill<NN>-reel-cover.jpg
rm -rf <out_dir>/frames
```

Music credit: `Music: <Judul> by Kevin MacLeod` (title = file name without
`-kevin-macleod.mp3`, dashes to spaces, title case).

## Fallback

If the animated render fails for any reason, fall back to the slideshow
script `~/workspace/peka-content/tools/make_reel.sh` with the same picked
track, post as usual, and say so in the report. Never leave the reel slot
empty once the carousel is live.
