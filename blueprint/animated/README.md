# BLUEPRINT animated reel template

Spec-driven animated reel, one tool per edition: cover (3 s) +
repo-page scene (3 s) + repo scene (5 s) + question (2 s) + follow
(2 s) = 15 s, 2160x3840, yuv420p. The repo-page scene renders the
repo as a blueprint browser window (name, descriptions, star/fork/
contributor stats, language/license chips, topic chips, shortlink in
the titlebar); the repo scene keeps the og screenshot + typing panel.

## Spec

`reel-spec.json` in the edition output dir:

```json
{
  "agent": "CINDY",
  "episode": 1,
  "shortlink": "https://s.peka.ai.id/2y12kr",
  "sub": "AI agent open source yang jalan di laptop dan HP dalam satu session yang nyambung.",
  "note": "Komputermu jadi servernya sendiri, tanpa sewa server.",
  "question": "Kamu paling pengin Cindy bantuin kerjaan apa dulu?",
  "repos": [{
    "name": "makecindy/cindy",
    "stars": "8,7RB",
    "language": "TypeScript",
    "license": "Apache-2.0",
    "install": "Download gratis di cindy.app",
    "penjelasan": "...max 260 chars, no em-dash...",
    "cocok": "...",
    "shot": "shots/makecindy-cindy.png",
    "desc_en": "Consider it done. The open-source AI agent that works out of the box.",
    "desc_id": "AI agent open source yang jalan di semua perangkatmu.",
    "forks": "1.037",
    "contributors": "173",
    "topics": ["ai-agent", "claude-code", "codex", "electron", "macos", "windows"]
  }]
}
```

Relative `shot` paths resolve against the spec file's directory.

## Render + encode (4K)

```sh
cd ~/workspace/peka-content/blueprint/animated
~/workspace/megumi/venv/bin/python render.py <out>/reel-spec.json <out>/frames 24 15 2.0
ffmpeg -y -framerate 24 -i <out>/frames/f%04d.png -ss 10 -t 15 -i <track> \
  -filter_complex "[0:v]scale=2160:3840[vout];[1:a]afade=t=in:st=0:d=0.5,afade=t=out:st=14.5:d=0.5[aout]" \
  -map "[vout]" -map "[aout]" -c:v libx264 -pix_fmt yuv420p -r 24 -c:a aac -b:a 160k -t 15 \
  <out>/blueprint-reel.mp4
ffmpeg -y -ss 1 -i <out>/blueprint-reel.mp4 -frames:v 1 -q:v 2 <out>/blueprint-reel-cover.jpg
rm -rf <out>/frames
```

Music: exactly one call to `~/workspace/peka-content/brand/music/pick_reel_track.sh`
per new reel. Verify with ffprobe: h264, 2160x3840, yuv420p, 15.000 s.
Check frames at t=2/4.5/8.5/12/14 s before posting (t=4.5: repo-page
scene with shortlink in the titlebar; t=8.5: repo scene with shortlink
in the titlebar). No slideshow fallback.
