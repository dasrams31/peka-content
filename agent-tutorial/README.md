# Tutorial Agent Peka

Weekly step-by-step AI agent tutorials (e.g. build a research agent,
make a Claude skill, wire an agent to tools). One edition per week,
hands-on build alternating with concept explainer.

Working series name: **Tutorial Agent Peka** (folder slug
`agent-tutorial`). The name can be renamed later; the folder slug,
spec schema, and scripts do not depend on the display name.

Status: template system built 14 Nov 2026. Build-only: no cron exists
yet, nothing posts from this folder until a run is ordered from an
interactive chat session.

## Visual identity - agent-console

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
   (6 slides, 4096x4096). Slide 1 cover (title + goal + step count
   + prerequisites + a "COBA SEKARANG" panel with one concrete first
   action + a step preview + a "HASIL AKHIR" result panel), slides 2-5
   one step per slide (number rail, title, detail, optional terminal
   code panel), slide 6 closing (recap + tip panel + follow panel +
   shortlink printed + Follow + community). The closing shortlink is
   read from `shortlinks.json`; without it a placeholder
   `s.peka.ai.id/contoh` is printed and a warning is shown.
4. **Reel.** `python3 build_reel.py <spec.json> <out_dir>` (4 scenes,
   16 s, 2160x3840 yuv420p). Picks music EXACTLY ONCE via
   `brand/music/pick_reel_track.sh` (recorded in `track.txt`; a
   re-render reuses `track.txt` instead of picking a second track),
   renders frames with the megumi venv python, encodes with ffmpeg
   `-threads 2`, extracts the cover frame at 3.2 s as
   `<slug>-cover.jpg`. Scene 4 prints the blog shortlink.
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
- `carousel.py` - Threads carousel designer (PIL, 4096x4096, QA gate)
- `make_shortlink.py` - admin shortlink creator (direct DB insert)
- `make_blog.py` - blog JSON builder + per-edition backup (+ --local)
- `post_agent.py` - poster (Threads + IG reel + FB reel), idempotent
- `build_reel.py` - reel orchestrator (music once, render, encode, cover)
- `animated/scene.html` - 4-scene reel template (agent-console)
- `animated/render.py` - Playwright frame renderer (4K, scale 2.0)
- `animated/assets/` - Poppins + DejaVu fonts
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
# 4. reel
python3 build_reel.py out/<date>-<short>/spec.json out/<date>-<short>
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
- ffprobe reel: 2160x3840, yuv420p, ~15-16 s.
- All carousel slides 4096x4096; layout QA passes (no overflow,
  no box overlap, nothing in the footer strip).
- `post-done.txt` absent until posting; no channel broadcast sent
  during a dry-run.

## Sample edition (dry-run, 14 Nov 2026)

`out/2026-11-14-ai-agent-pertama/` (built from the ramadanadipa
blog article "AI Agent: Apa Itu dan Cara Bikin Agen AI Pertamamu"
(24 Okt 2026). Everything is marked SAMPLE in the spec. The blog
JSON lives in the out dir only (`make_blog.py --local`), the
shortlink is the placeholder `s.peka.ai.id/contoh` (no real DB
insert), nothing was posted or broadcast.
