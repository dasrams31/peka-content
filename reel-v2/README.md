# reel-v2 - Voiceover-led reels for Peka AI

A second reel system next to the v1 template reels (15-16s, music-led).
Reel-v2 is built for the longer voiceover-led explainer format: 45-60s,
one Indonesian voiceover driving the reel, word-by-word karaoke captions
synced to real TTS word boundaries, dark textured visuals, no music.

BUILD ONLY. Nothing in this folder posts anything. Do not wire it into
any cron until the user says so. SPILL #24 and the other running pillars
keep the v1 format.

## What is in here

- `themes.json` - the 3 themes. Each theme is a full color config:
  `dark-grid` (black + grid + red, closest to the reference reels),
  `peka-yellow` (Peka yellow #FFD60A on black #111111, current brand),
  `navy-tech` (dark navy + cyan, BLUEPRINT mood).
- `scene.html` - the single 1080x1920 stage template. Theme comes in as
  CSS variables. `buildScene(spec)` builds the scenes, `renderAt(t)`
  draws one deterministic frame: scene stagger, bar growth, mascot bob,
  karaoke line + active-word highlight, progress bar.
- `tts.py` - Edge TTS voice `id-ID-ArdiNeural` (the voice Piko uses),
  `boundary='WordBoundary'` so every word gets a real measured
  start/end. One synthesis per scene, joined with 0.3s silence gaps.
  Writes `narration.mp3`, `words.json`, `narration.txt`.
  Run with the Piko venv python (edge-tts lives there).
- `render.py` - Playwright frame renderer (megumi venv python,
  chromium_headless_shell-1243). Same deterministic pattern as the
  HM reel builder: `renderAt(t)` per frame, scale 2.0 = 2160x3840.
  Also has a `--still <t> <out.jpg>` mode for theme comparison.
- `encode.py` - ffmpeg: frames + narration to h264 2160x3840 yuv420p
  + aac, faststart; cover jpg from t=1s.
- `build_reel.py` - orchestrator: spec -> TTS -> render -> encode ->
  ffprobe verify (h264, 2160x3840, yuv420p, aac, 45-60s) -> delete frames.
- `demo-hydrogen/` - the demo edition (Gemini 4 Hydrogen, dark-grid).
  v1: flat Piko mascot, fixed bottom-right, voiceover aku/kamu +15%.
- `demo-hydrogen-v2/` - the same topic, second demo: anime Piko
  character that talks (two mouth states synced to the voiceover),
  per-scene mascot positions, voiceover register "lo" at +25%.
- `assets/character/` - the talking character (see below).
- `stills/` - hook-scene stills for the other two themes (v1).

## Talking character (v2)

`assets/character/` holds the anime version of the Piko mascot
(yellow letter-P body, one big eye, antenna, Piko yellow #FFD60A):

- `piko-anime-closed.png` - mouth closed (small smile), 804x1365,
  transparent background.
- `piko-anime-open.png` - mouth open (talking), same size, same
  crop box as the closed state, so swapping frames never jitters.
- `process_character.py` - how the two PNGs were made from the
  generated art: flood-fill the connected near-black background to
  transparent, crop both states with one union bounding box.
  (Raw generations are the `media-generation-*.png` files in the
  same folder.)

How it works in `scene.html`: the mascot is a container with the two
images stacked; `renderAt(t)` shows the open state while a word is
being spoken (word boundaries from `words.json`, with a 0.02s lead
and 0.06s tail so the mouth does not flicker on tiny gaps) and the
closed state in pauses, plus a gentle bob and a 1.035x swell while
speaking. Both images are preloaded in `buildScene`, so the toggle
never waits on a load mid-render.

Per-scene position: each scene in `spec.json` can carry
`mascot: {side: "right"|"left", bottom: <px>, width: <px>,
left|right: <px>, flip: <bool>}`. `flip` mirrors the character so
it faces the content when it sits on the left. Without a `mascot`
field the scene falls back to the v1 spot (right, bottom 470,
width 210). Demo v2 positions: hook right-bottom large (260),
stat/bars/xhigh left-bottom small (160-170, flipped), compare
right-bottom small (170), close right-center (bottom 620, 180).
Check a still per scene before a full render; the mascot must never
cover text, bars, or the shortlink chip.

### Swapping the character

To use a different presenter later (e.g. an anime girl/boy), drop
two same-size, same-crop PNGs (mouth closed + mouth open,
transparent background) into `assets/character/` and point the spec
at them:

```json
"character": {
  "closed": "assets/character/my-girl-closed.png",
  "open": "assets/character/my-girl-open.png",
  "aspect_ratio": 1.5
}
```

`aspect_ratio` is height / width of the art (the anime Piko is
1.6978). If both states use the SAME file (closed == open), the
mouth never changes but the bob + pulse still animate, which is the
fallback when two consistent states cannot be produced.

## How to render the next edition

1. Copy `demo-hydrogen/spec.json` to a new folder and edit it:
   - `theme`: one of `dark-grid`, `peka-yellow`, `navy-tech`.
   - `kicker`: top-left label (usually the topic, e.g. `GEMINI 4 HYDROGEN`).
   - `rate`: TTS speed. `+15%` matches the fast reference style and
     keeps ~130 words inside 60s. `+0%` is calmer but slower; then
     keep the narration under ~110 words. **v2 uses `+25%` with the
     informal "lo" register (like the aishift.id reference) and
     ~132 words for ~58s.** At +25% ArdiNeural still speaks
     ~0.42s/word, so do not assume a higher rate buys much time:
     the first v2 draft (146 words) ran 61.9s and had to be trimmed
     to 132 words. Keep the narration at or under ~135 words at
     +25%.
   - `scenes`: 5-6 scenes. Kinds:
     - `hook`: `badge` (chip), `headline` (2 lines), `sub`.
     - `beat`: `stat` (huge number), `stat_label`, `lines` (2-3 lines,
       `<b>` for accent, `<span class="mono">` for mono accent),
       optional `bars` (max 3, `{label, value, accent, tag}`) or
       `compare` (max 2 rows, `{label, a_label, a_value, b_label,
       b_value}`; the accent side is the HIGHER score, whoever it is).
     - `close`: `headline` (3 lines, the question), `follow`,
       `shortlink` (printed in the visual, e.g. `s.peka.ai.id/XXXXXX`).
   - `narration`: one Indonesian paragraph per scene, casual Peka
     voice (aku/kamu, udah, sampe, kalo, nggak). Never "lo".
     Target ~130 words total for 45-60s at `+15%`.
     **v2 register is "lo" instead of aku/kamu** (informal, like the
     reference reels); keep the visual text consistent with the
     spoken words (e.g. the closing headline says "Lo tim Hydrogen"
     because the voiceover says "lo").
2. Run: `python3 build_reel.py <spec.json> <out_dir> [--theme <name>]`
   (about 10-15 minutes: ~30s TTS, ~10 min frame render, ~1 min encode).
3. Check `build.log` + ffprobe output, then eyeball frames: extract
   with `ffmpeg -ss <t> -i <out>/reel.mp4 -frames:v 1 check.jpg`
   at the hook, mid-beat, and closing scene. **For a talking-
   character edition, render stills FIRST** (`render.py
   <render-spec.json> --still <t> <out.jpg>`) at one time per
   scene, including one mid-word time (mouth must be open) and one
   sentence-gap time (mouth must be closed), and check the mascot
   never covers text, bars, or the shortlink chip. Only then run
   the full render.
4. Write `caption-tiktok.txt` in the out dir (FYP pattern: hook fact
   first, ~35 words, 3 hashtags, exactly one forced-choice question,
   no link in the text; the link lives in the closing scene only).

## Rules that still apply (do not break)

- No em-dash in any text (narration, captions, files).
- No link in any caption text. Links only inside the visual as an
  admin-owned s.peka.ai.id shortlink.
- NO "komen X supaya link dikirim lewat DM" CTA (not approved by the
  user). Close with a question + follow, as usual.
- Reels are real motion graphics, 2160x3840 yuv420p, never a slideshow.
- Facts only from verified sources. Never invent numbers or features.
- Community footer `s.peka.ai.id/gabung` is on every frame.

## Known limitations (found while building the demo)

- Word boundaries are real, not estimated: Edge TTS is asked for
  `boundary='WordBoundary'`. The default is `SentenceBoundary`, which
  gives no per-word timings at all, so the parameter must be set.
- TTS tokenization is not identical to the script words. Examples from
  the demo: `12 November` arrives as one token, `GPT-6.1` splits into
  `GPT-6` + `1`, `@peka.ai.id` is spoken as just `peka`. The karaoke
  displays the TTS tokens, so: write `GPT 6.1` (not `GPT-6.1`) in
  narration, and write `Follow Peka AI` (not `Follow @peka.ai.id`) in
  the spoken line. The visual still shows `@peka.ai.id` as text.
- The ffmpeg concat demuxer with `-c copy` produces non-monotonic DTS
  warnings at the joins. `tts.py` re-encodes the join (libmp3lame)
  instead; do not switch it back to stream copy.
- At `+0%` rate, ArdiNeural speaks ~0.48s/word: ~130 words run past
  60s. At `+15%` the same script lands at ~57s. If a script runs long,
  speed up the rate before cutting facts.
- Render time is the bottleneck: 24fps x ~58s = ~1,400 Playwright
  screenshots at 2160x3840, roughly 10 minutes on this VM. Do not
  lower the fps to save time; the stagger/bar animations need it.
  If a render run is killed mid-way (happened once, SIGTERM at frame
  906/1384), just re-run it: `render.py` skips frames that already
  exist, so it resumes instead of starting over.
- x264 at 4K OOM-killed this VM (6 GB cgroup) with default threading.
  `encode.py` is capped to `-threads 2` + preset veryfast for that
  reason. Do not remove the caps without re-testing.
- In the demo, the compare-row name labels under the two values sit
  close together (`Sonnet 5.5 Hydrogen` at a glance). Fixed in
  `scene.html` after the demo render (a `lawan` separator is now
  inserted between the names); the demo mp4 still has the old
  spacing, the values themselves were always correctly attributed
  by position.
- The hook scene has a lot of empty middle space by design (headline +
  mascot + karaoke). That matches the reference look; do not fill it
  with extra text.
- The karaoke line wraps to two lines when a line has 7 long words.
  That is normal; the active word still highlights correctly.
- Talking-character notes (v2): the two mouth states must share one
  crop box or the character visibly jumps when the mouth toggles;
  `process_character.py` enforces this with a union bbox (the two
  v2 states differ by only 1-4 px before the union crop). The
  generated art carries two tiny dark specks (one on the head, one
  on the P bowl) that are barely visible at reel scale; they come
  from the generation, not the pipeline. The mouth is binary
  (open/closed per word), not syllable-shaped: at 24fps it reads as
  talking, but it is not lip-sync. The karaoke line grouping can
  split a sentence across lines (e.g. a 3-word line when the
  previous line hit the 7-word cap), which is cosmetic only.
