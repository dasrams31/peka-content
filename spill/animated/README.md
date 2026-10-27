# SPILL animated reel template

Motion-graphics reel for SPILL Repo (standard reels 2026-10-25: animated,
2K, FYP). Window design (locked 2026-10-27): same browser-window +
terminal + penjelasan format as the carousel slides.

## Files

 - `scene.html` — vertical scenes, total 3 + 4*repos + 4 seconds
   (27 s for 5 repos): cover (kicker edisi + REPO SKILL + agent
   highlight), one scene per repo (og screenshot in a browser window +
   typing terminal + penjelasan), closing question, follow + community
   (standing rule 2026-10-25). Built from a spec via
   `window.buildScene(spec)`, animated via `window.renderAt(t)`
   (deterministic frame-by-frame).
- `render.py` — Playwright frame renderer (2K via scale 1.3333).
- `fetch_shots.py` — downloads each repo's GitHub og:image into the
  edition shots dir and writes the path back into the reel spec.
  Retries 429/5xx with backoff, skips already-downloaded shots.

## Reel spec format

```json
{"agent": "ANTIGRAVITY", "episode": 5, "next": "CLAUDE",
 "repos": [{"name": "owner/repo", "stars": "12RB",
            "install": "npx skills add owner/repo -g",
            "penjelasan": "two sentences, max 260 chars",
            "shot": "/abs/path/to/shots/owner-repo.png"}]}
```

Exactly 5 repos. `penjelasan` is 2 sentences distilled from the
carousel desc (not a truncation). `install` comes from
`../install_cmd.py` (README extraction, generic `npx skills add`
fallback). `shot` is written by `fetch_shots.py`.

## Worker render commands (per edition)

```bash
cd ~/workspace/peka-content/spill/animated
TRACK=$(~/workspace/peka-content/brand/music/pick_reel_track.sh)  # ONCE per edition
python3 fetch_shots.py <out_dir>/reel-spec.json <out_dir>/shots
~/workspace/megumi/venv/bin/python render.py <out_dir>/reel-spec.json <out_dir>/frames 24 27 1.3333
ffmpeg -y -framerate 24 -i <out_dir>/frames/f%04d.png -ss 10 -t 27 -i "$TRACK" \
  -filter_complex "[0:v]scale=1440:2560[vout];[1:a]afade=t=in:st=0:d=0.5,afade=t=out:st=26.5:d=0.5[aout]" \
  -map "[vout]" -map "[aout]" -c:v libx264 -pix_fmt yuv420p -r 24 -c:a aac -b:a 160k -t 27 \
  <out_dir>/spill<NN>-reel.mp4
ffmpeg -y -ss 1 -i <out_dir>/spill<NN>-reel.mp4 -frames:v 1 -q:v 2 <out_dir>/spill<NN>-reel-cover.jpg
rm -rf <out_dir>/frames
```

Music credit: `Music: <Judul> by Kevin MacLeod` (title = file name without
`-kevin-macleod.mp3`, dashes to spaces, title case).

## Fallback

If the animated render fails for any reason (including shot downloads
still failing after retries), fall back to the slideshow script
`~/workspace/peka-content/tools/make_reel.sh` with the same picked
track, post as usual, and say so in the report. Never leave the reel
slot empty once the carousel is live.
