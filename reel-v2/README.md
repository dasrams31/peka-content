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
- `stills/` - hook-scene stills for the other two themes.

## How to render the next edition

1. Copy `demo-hydrogen/spec.json` to a new folder and edit it:
   - `theme`: one of `dark-grid`, `peka-yellow`, `navy-tech`.
   - `kicker`: top-left label (usually the topic, e.g. `GEMINI 4 HYDROGEN`).
   - `rate`: TTS speed. `+15%` matches the fast reference style and
     keeps ~130 words inside 60s. `+0%` is calmer but slower; then
     keep the narration under ~110 words.
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
2. Run: `python3 build_reel.py <spec.json> <out_dir> [--theme <name>]`
   (about 10-15 minutes: ~30s TTS, ~10 min frame render, ~1 min encode).
3. Check `build.log` + ffprobe output, then eyeball frames: extract
   with `ffmpeg -ss <t> -i <out>/reel.mp4 -frames:v 1 check.jpg`
   at the hook, mid-beat, and closing scene.
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
