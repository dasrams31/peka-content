# Tutorial Agent Peka

Weekly step-by-step AI agent tutorials (e.g. build a research agent,
make a Claude skill, wire an agent to tools). One edition per week,
hands-on build alternating with concept explainer.

Working series name: **Tutorial Agent Peka** (folder slug
`agent-tutorial`). The name can be renamed later; the folder slug,
spec schema, and scripts do not depend on the display name.

Status: template system built 14 Nov 2026. Cron `peka-agent-tutorial`
created 14 Nov 2026 (weekly, 19:00, build-only: it never runs
post_agent.py; posting happens from an interactive chat session).
Episode #01 debut is fully prepared in
`out/2026-11-16-ai-agent-pertama/` (real admin shortlink, blog live);
it posts from chat at 19:00 on 16 Nov 2026. Episode #02 is the
research-agent topic (topics.md). "Bikin skill Claude sendiri" is NOT
in the bank: it aired as AI Pekan Ini #01 on 15 Nov 2026 and must not
be built again in this series (the spec-template.json example topic
is illustrative only).

**Style change 15 Nov 2026 (user order: "oke pake ini tapi sesuaikan
dengan warna dari peka"):** the template was restyled to the
Herlambang variant (see below) and episode #01 was re-rendered in it
(voiceover reel + 6 slides; old-style assets backed up under
`out/2026-11-16-ai-agent-pertama/backup-old-style/`). The agent-console
v1 files are kept but no longer used for new episodes.

## Visual identity - Herlambang (current, since 15 Nov 2026)

Adapted from a 60s Herlambang Awn Facebook reel (reference video +
frames in `ref-herlambang/`; full breakdown in
`ref-herlambang/herlambang-style.md`). Same structure, Peka colors.

| Token | Value | Use |
|---|---|---|
| Cream grid paper | `#F5F1E8` | KENAPA + closing scenes/slides |
| Dark slate grid | `#0D1117` | ALAT + JALANKAN scenes/slides |
| Peka yellow grid | `#FFD60A` | LANGKAH scenes/slides |
| Active tab fill | `#FFD60A` | active tab (black text) |
| Accent (cream/dark) | `#10B981` | italic-serif accent word |
| Accent (yellow) | `#065F46` | italic-serif accent word |
| Terminal panel | `#161B22` / `#0B0D10` | code/terminal panels |
| Emerald mono | `#10B981` | terminal code text |
| Hard shadow | `#0D1117` (or `#000000` on dark) | chunky panel offset shadow |

- Persistent top tab bar on every reel scene and on carousel slide 1:
  `KENAPA -> ALAT -> LANGKAH -> JALANKAN` (mono `// <section>` label
  above it). Active tab yellow-filled; visited tabs dark slate;
  upcoming tabs white (pale yellow on yellow backgrounds). A thin
  accent underline marks the active tab.
- Alternating grid-paper backgrounds per section (cream / dark /
  yellow / dark / cream), 64px grid (256px on 4096 slides).
- Huge condensed bold type: Anton for headlines (132px at 1080 reel
  stage, 360px cover / 280px step titles on 4096 slides), with ONE
  Playfair Display Italic accent word per headline. Headline words
  are inline-block spans with a 0.22em right margin (a trailing space
  inside the span collapses, so the margin is what separates words).
- Neo-brutalist chunky panels: thick black borders (3px reel, 8px
  slides), hard offset shadows, square corners. Highlight card =
  yellow fill. Terminal windows: dark panel, traffic-light dots,
  white step-label pill, emerald mono code.
- Presenter: Piko (the yellow mascot; reel-v2 anime poses
  base/present/wave x closed/open mouth), bottom-right, talking
  mouth + lean/pulse while the narration speaks. No other mascot:
  the reference video's illustrated man is NOT used.
- Reel format: 45-60s voiceover-led (Edge TTS `id-ID-ArdiNeural`,
  rate +25%, ~120-135 words), sentence-first karaoke with the
  current word highlighted, progress bar at the bottom. No music.
  Voice decision 15 Nov 2026: ArdiNeural kept on the user's word
  (GadisNeural is the only other id-ID Edge voice, equally
  mainstream; local Meta MMS TTS was sampled but not chosen).
- Carousel: 6 slides, one card type per slide (cover: chip + big
  title + sub + yellow try-now panel + info line + result panel;
  steps: number rail + title + detail + note + code panel and/or
  mini-card grid / run terminal; closing: title + shortlink +
  recap lines + tip panel + follow panel).
- Brand mark: the header lockup (top-right, every slide + every reel
  scene) is the Peka mascot from peka.ai.id (`piko/piko-idle.png`,
  transparent, trimmed to its alpha bbox) + "peka.ai.id" — the same
  mark + wordmark as the site nav. On yellow backgrounds the lockup
  sits in a white pill (black border + hard shadow) because the
  yellow mascot is invisible on yellow.

## Visual identity - agent-console (v1, superseded 15 Nov 2026)

Distinct from Peka yellow/black and from HM premium warm paper.

| Token | Value | Use |
|---|---|---|
| Background | `#0D1117` | slide + reel canvas |
| Panel | `#161B22` | code/terminal panels, step cards |
| Border | `#30363D` | 1px panel borders, hairlines |
| Ink | `#F0F6FC` | headlines, body text |
| Slate | `#8B949E` | secondary text, meta, footer |
| Emerald | `#10B981` | active/done steps, step rail, shortlink, progress bar |
| Amber | `#F59E0B` | sparingly: edition meta, warnings |

- Type: Poppins Bold (headlines), Poppins SemiBold, DejaVu Sans
  (body), DejaVu Sans Mono (+ Bold) for code, commands, paths.
- Numbered step rail on the left (`01`, `02`, ...) with a vertical
  hairline; one step per slide.
- Fixed grid: margin 240px, header at 150px, rule at 380px, footer
  strip reserved below y=3756 (footer text at y=3896). Body content
  never enters the footer strip.
- Flat panels, 1px borders, no gradients, no glows, no dead gaps.
- Max 3 text sizes per slide (title 170/200, body 92, meta 56;
  code shrinks from 92 to a 52px floor, then wraps, never clipped).
- Shortlinks are rendered in proportional bold (Poppins), never
  monospace: a mono font gives every "." a full-width cell, so
  `s.peka.ai.id` reads as "s . peka . ai . id".
- Layout QA per `special/DESIGN_RULES.md`: `carousel.py` records
  every text/panel box and aborts on overflow or overlap before
  saving any PNG.
- Brand mark: the header lockup (top-right, every slide + every reel
  scene) is the Peka mascot from peka.ai.id (`piko/piko-idle.png`,
  transparent, trimmed to its alpha bbox) + "peka.ai.id" — the same
  mark + wordmark as the site nav (Nav.jsx: LogoMark 26px + "peka").
  A bottom-right mascot on cover/closing + reel scenes 1/4 was tried
  14 Nov 2026 and removed the same day on the user's word ("logo
  yang di peka.ai.id diatas, bukan nambah logo baru").

## Pipeline (one edition)

Edition out dir: `~/workspace/peka-content/agent-tutorial/out/<date>-<short>/`.

1. **Spec.** Copy `spec-template.json`, fill it in. Fields: episode,
   slug, title, date, hook (<= 60 chars), goal (1 line),
   prerequisites (list), steps[] (each: n, title, detail <= 140
   chars, code optional, note optional), tip (1), faq (3-4 pairs),
   tags, sources[], reel {date, source, code, headline[], sub,
   points[3], steps[3], question, band}, carousel {slides[]}.
   The reel `code` is the key snippet shown in the scene-1 terminal
   panel (the reel has no hero image; it is fully self-contained).
   Code in tutorials is kept technically correct: never paraphrase
   code into something wrong.
2. **Shortlink.** `python3 make_shortlink.py <out_dir>
   https://blog.peka.ai.id/p/<slug>` (admin user_id 1, direct DB
   insert, redirect verified 307). Writes `shortlinks.json`.
   The shortlink is created before the blog JSON exists (the reel and
   the carousel need the code printed inside the visual). Nothing is
   posted before the blog page is live.
3. **Threads carousel.** `python3 carousel.py <spec.json> <out_dir>`
   (6 slides, 4096x4096, Herlambang style). Slide 1 cover (tab bar +
   chip + big Anton title with one Playfair-italic accent word + sub
   + yellow "COBA SEKARANG" panel with one concrete first action +
   info line + "HASIL AKHIR" result panel), slides 2-5 one step per
   slide (number rail, title, detail, note, optional terminal code
   panel; step["cards"] renders a 2x2 mini-card grid and
   step["terminal"] a run-output card), slide 6 closing (title +
   shortlink printed + recap lines + tip panel + follow panel).
   Per-slide backgrounds: cover cream, step 1 dark, steps 2-3 yellow,
   step 4 dark, closing cream. The closing shortlink is read from
   `shortlinks.json`; without it a placeholder `s.peka.ai.id/contoh`
   is printed and a warning is shown.
4. **Reel.** `python3 build_reel_v2.py <reel-v2-spec.json> <out_dir>`
   (5 scenes, 45-60 s, 2160x3840 yuv420p, voiceover-led, no music).
   The edition reel spec (`reel-v2-spec.json`, in the out dir) holds
   the 5 scenes (narration text, headline, sub, cards/steps/terminal,
   Piko pose per scene, shortlink, slug). TTS runs via the reel-v2
   pipeline (`reel-v2/tts.py`, Edge TTS id-ID-ArdiNeural, rate +25%);
   `--skip-tts` reuses an existing `narration.mp3` + `words.json`
   in the out dir (e.g. when the voice was decided separately).
   The orchestrator computes scene spans + headline stagger delays
   from the measured word timings, renders frames with the megumi
   venv python (`animated/render-herlambang.py`, Playwright,
   `--still <t>` renders one QA still), encodes with ffmpeg
   `-threads 2` via `reel-v2/encode.py`, re-extracts the cover at
   3.0 s as `<slug>-cover.jpg`, verifies with ffprobe (h264
   2160x3840 yuv420p + aac, 45-60 s), then deletes the frames.
   Always render stills first (`render-herlambang.py <render-spec.json>
   --still <t> <out.jpg> 1.0`) and read them before the full render:
   check headline word spacing, terminal readability, Piko/lockup
   visibility on every theme, and no Piko/sub collisions.
5. **Blog.** `python3 make_blog.py <out_dir>` writes
   `peka-content/blog/<slug>.json`, copies the reel cover + slides
   into `peka-content/images/`, and backs the edition up to
   `~/workspace/backups/peka-blog-agent/<slug>/` (blog JSON is
   gitignored, nothing else backs it up). The blog app reads the
   JSON dir on every request: no restart. Verify live:
   `curl -s -o /dev/null -w "%{http_code}"
   https://blog.peka.ai.id/p/<slug>` must be 200.
   `--local` writes `<out_dir>/<slug>.json` only (dry-run/sample
   mode: nothing leaves the out dir).
6. **Captions.** `caption-threads.txt` (standalone, hook <= 60 chars,
   forced-choice closing question, closing tag #AI, <= 500 chars) +
   `caption-threads-reply-1.txt` (key Python code fragment, <= 500
   chars; never an install/terminal command) + `caption-reel-ig.txt`
   + `caption-reel-fb.txt` + `caption-tiktok.txt`. Follow
   `templates/` and the locked caption rules.
7. **Post (interactive chat session only, approval cards surface).**
   `python3 post_agent.py <out_dir>`: Threads carousel + reply,
   IG reel, FB reel, then patches the blog JSON links. Idempotent
   via `post-done.txt`. Never run from a cron worker.
8. **Channel + TikTok package.** Broadcast via `telegram_channel.py
   --type tutorial` (channel captions MAY contain links) and deliver
   the TikTok package (reel + caption) to chat, like other pillars.
   Note: `telegram_channel.py` has no `agent-tutorial` type yet; use
   `--type tutorial` until a dedicated type is added.
9. **Log.** `post_agent.py` appends one line to `posted.log`
   (`YYYY-MM-DD|agent-tutorial|<slug>|<shortlink>`).
10. **Report.** Episode, topic, track, links (IG/Threads/FB/blog),
    channel message id, TikTok package delivered.

## Files

- `README.md` (this file)
- `spec-template.json` - edition spec schema with example values
  (episode 1, bikin skill Claude sendiri)
- `carousel.py` - Threads carousel designer (PIL, 4096x4096, QA gate,
  Herlambang style)
- `make_shortlink.py` - admin shortlink creator (direct DB insert)
- `make_blog.py` - blog JSON builder + per-edition backup (+ --local)
- `post_agent.py` - poster (Threads + IG reel + FB reel), idempotent
- `build_reel_v2.py` - voiceover-reel orchestrator (TTS, render,
  encode, ffprobe verify; `--skip-tts` / `--no-render` flags)
- `build_reel.py` - v1 music-reel orchestrator (superseded; kept)
- `animated/scene-herlambang.html` - 5-scene Herlambang reel template
- `animated/render-herlambang.py` - Playwright frame renderer for it
  (4K scale 2.0, `--still` QA mode)
- `animated/scene.html` - v1 4-scene reel template (agent-console,
  superseded; kept)
- `animated/render.py` - v1 Playwright frame renderer (kept)
- `animated/assets/` - Anton + Playfair Display Italic + Poppins +
  DejaVu fonts; `character/` - Piko anime poses (base/present/wave
  x closed/open)
- `ref-herlambang/` - style reference video + 8 frames + style
  breakdown (`herlambang-style.md`, incl. the approved Peka mapping)
- `templates/` - caption templates with placeholders
- `topics.md` - bank of 8 starter topics (hands-on / concept)
- `series.txt` - next episode number (starts at 1)
- `posted.log` - one line per posted edition (written by post_agent.py)
- `out/<date>-<short>/` - per-edition work dir (spec.json,
  article-body.html, shortlinks.json, reel-spec.json, track.txt,
  slide-1..6.png, `<slug>-reel.mp4`, `<slug>-cover.jpg`, captions,
  post-log.txt when posted)

## Run one edition end to end

```bash
cd ~/workspace/peka-content/agent-tutorial
# 1. spec: copy spec-template.json to out/<date>-<short>/spec.json, fill it
# 2. shortlink
python3 make_shortlink.py out/<date>-<short> https://blog.peka.ai.id/p/<slug>
# 3. carousel
python3 carousel.py out/<date>-<short>/spec.json out/<date>-<short>
# 4. reel (voiceover; write reel-v2-spec.json in the out dir first)
python3 build_reel_v2.py out/<date>-<short>/reel-v2-spec.json out/<date>-<short>
#    (--skip-tts reuses narration.mp3 + words.json already in the out dir)
# 5. blog
python3 make_blog.py out/<date>-<short>
# 6. captions: write the 5 caption files in the out dir
# 7. post (chat session only, never from a cron worker)
python3 post_agent.py out/<date>-<short>
# 8. channel + TikTok package (telegram_channel.py --type tutorial)
```

## Gate discipline

- If one approval card hangs, is denied, or times out, DO NOT
  re-post blindly: check live first whether it already aired (an
  attempt that "timed out" may have posted, like FB Prompt #21).
- If it hangs, report and stop; re-post only from a chat session on
  the user's word, and only the stuck step.
- `post-done.txt` makes `post_agent.py` idempotent: completed steps
  are skipped on re-run.

## Locked Peka rules that apply here

- No link of any kind in post text on any platform. The blog
  shortlink is printed INSIDE the visual (carousel slide 6, reel
  scene 4) with exactly one instruction sentence in the caption.
- No install / terminal commands in any social caption. Install steps
  only inside the visual. The Threads reply carries a Python code
  fragment, never `pip install` / `curl` / `git clone`.
- Threads closing tag is #AI (locked). Threads caption stands alone,
  forced-choice closing question, root + max 1 reply.
- All reels are full animated motion graphics, 2160x3840 yuv420p.
  Slideshow / Ken Burns is not a reel.
- No em-dash / en-dash in any output file (code asserts on it).
- Every carousel/reels closes with Follow + community
  (Follow @peka.ai.id + s.peka.ai.id/gabung + save/share).
- Shortlinks are ALWAYS admin-owned (user_id 1) via direct DB insert,
  never the guest API.
- Captions in Peka casual voice ("AI" never "mesin", "udah", "kalo",
  "nggak", short sentences, gentle plain language).

## What is intentionally NOT included

- No cron yet. Scheduling (weekly slot, day, time) is the user's
  call; this build only prepares the system.
- No posting, no channel broadcast, no TikTok delivery in build.
- No dedicated `telegram_channel.py --type agent-tutorial` yet;
  broadcasts reuse `--type tutorial` for now.
- No backfill of old content. Editions start at episode 1.

## Verification checklist (every edition)

- `python3 -m py_compile` on all new/changed scripts.
- Blog JSON loads (`json.load`), no em/en dash in the JSON, all
  captions, or any slide text.
- Blog URL curls 200; shortlink redirects 307 to the blog URL.
- ffprobe reel: 2160x3840, yuv420p, h264 + aac, 45-60 s.
- All carousel slides 4096x4096; layout QA passes (no overflow,
  no box overlap, nothing in the footer strip).
- Stills QA: render one still per reel scene and read it (headline
  spacing, terminal readability, lockup + Piko visible on every
  theme, tab bar states correct) before the full render.
- `post-done.txt` absent until posting; no channel broadcast sent
  during a dry-run.

## Sample edition (dry-run, 14 Nov 2026)

`out/2026-11-14-ai-agent-pertama/` (built from the ramadanadipa
blog article "AI Agent: Apa Itu dan Cara Bikin Agen AI Pertamamu"
(24 Okt 2026). Everything is marked SAMPLE in the spec. The blog
JSON lives in the out dir only (`make_blog.py --local`), the
shortlink is the placeholder `s.peka.ai.id/contoh` (no real DB
insert), nothing was posted or broadcast.
