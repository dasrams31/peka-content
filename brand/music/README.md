# Reel music library

All tracks are CC-BY Kevin MacLeod (incompetech.com), royalty-free.
Credit the track title in every reel caption:
`Music: <Title> by Kevin MacLeod` (title = filename without
`-kevin-macleod.mp3`, dashes to spaces, title case).

## Lanes (since 2026-11-22)

Music must differ per content, not one lane for everything.

- `CYBERPUNK_TRACKS.txt` (16 tracks) — tech/AI mood. Series:
  SPILL, Homeless Media (TikTok pkg), Tutorial Mirror, BLUEPRINT,
  Bandingin Model, AI Pekan Ini, Tutorial Agent, Bansos.
  Pick with `pick_reel_track.sh` or `pick_reel_track.sh cyberpunk`.
- `LIGHT_TRACKS.txt` (16 tracks) — cheerful/playful mood. Series:
  Gratisan AI, Gratisan Mahasiswa, Prompt Harian, Coba Dulu,
  Tanya Jawab Nyata.
  Pick with `pick_reel_track.sh light`.

Each lane has its own persistent counter (`reel_track_state.txt`
for cyberpunk, `reel_track_state_light.txt` for light), so the two
lanes never interfere. The picker cycles in order and always returns
a different track than the previous pick in that lane. Call it
EXACTLY ONCE per reel render (IG and FB publish the same file).

## Adding a new track ("cari baru")

```bash
./fetch_track.sh "<Track Name>" <cyberpunk|light>
```

Example: `./fetch_track.sh "Sneaky Adventure" light`

It downloads the track from incompetech, verifies it with ffprobe
(valid mp3, >= 30s), saves it as `<slug>-kevin-macleod.mp3`, and
appends it to the lane file. The new track enters the rotation on
the next cycle; no counter is reset. If the track name does not
exist on incompetech the download fails and nothing is added.

To remove a track: delete its line from the lane file (keep the
mp3 file in place; it is harmless). Do not reorder the lane files
by hand unless you also reset that lane's counter, or the next pick
may repeat the previous track.

## reel-v2 voiceover reels (since 2026-11-22)

Reel-v2 used to have no music at all. `build_reel.py` now mixes a
background track under the voiceover (music at low volume, faded
in/out, trimmed to the narration length) via `encode.py`.
The lane is chosen with `--music-lane <cyberpunk|light>` or the
`music_lane` field in `spec.json` (default cyberpunk). The picked
track is recorded in `<out_dir>/track.txt` (full path + display
title) — use that title for the caption music credit.
