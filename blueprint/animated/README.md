# BLUEPRINT animated reel template

Spec-driven animated reel, one tool per edition: cover (3 s) + repo
scene (8 s) + question (2 s) + follow (2 s) = 15 s, 2160x3840, yuv420p.

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
    "shot": "shots/makecindy-cindy.png"
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
Check frames at t=2/7/13 s before posting. No slideshow fallback.
