# Tutorial Mirror (Peka)

Mirror of the daily ramadanadipa.com blog article into the Peka blog
(rewritten in Peka voice) plus concise tutorial content on all Peka
socials. One edition per source article, every day, all modes
(tutorial AND AI Trends). User decisions, 14 Nov 2026 (locked):

1. Mirror ALL daily articles (tutorial mode and AI Trends mode).
2. IG + FB = REELS (not carousel). Threads = carousel.
3. Peka blog cover = the reel cover frame (no separate cover).
4. Daily run in the afternoon, around 15:00 (cron created by parent).

## Pipeline (one edition)

Source: `~/workspace/blog/content/YYYY-MM-DD-<slug>.md` (written by the
`blog-daily-article` cron around 07:36). Edition out dir:
`~/workspace/peka-content/tutorial-mirror/out/<date>-<short>/`.

1. **Spec + rewrite.** Read the source markdown. Rewrite into Peka
   voice (casual chat style, "AI" never "mesin", no em-dash U+2014 /
   en-dash U+2013 anywhere): blog article 800-1200 words of prose,
   code examples kept technically correct (never paraphrase code into
   wrong code), FAQ 3-4 pairs, tags `["Tutorial", ...topic tags]`.
   Write `spec.json` (fields: slug, title, date, source_file,
   source_title, excerpt, tags, faq [[q, a]], hero, reel {date, source,
   headline[], sub, points[3], steps[3], question, band}, carousel
   {slides[]}) and `article-body.html`.
   Slug = source slug unchanged; if it collides with an existing
   `peka-content/blog/*.json`, append `-peka` and say so in the report.
2. **Shortlink.** `python3 make_shortlink.py <out_dir>
   https://blog.peka.ai.id/p/<slug>` (admin user_id 1, direct DB
   insert, redirect verified 307). Writes `shortlinks.json`.
   Note on ordering: the shortlink is created before the blog JSON
   exists (the reel and the carousel need the code printed inside the
   visual). The shortlink only redirects; nothing is posted before
   the blog page is live, and the final verification curls the blog
   URL for a 200.
3. **Threads carousel.** `python3 carousel.py <spec.json> <out_dir>`
   (6 slides, 4096x4096, Peka yellow/black). Slide 1 cover, slides
   2-4 core points, slide 5 short code example (never clipped:
   shrink to a 52px floor, then wrap), slide 6 shortlink + follow +
   community. Captions: `caption-threads.txt` (standalone, hook
   <= 60 chars, forced-choice closing question, closing tag #AI,
   <= 500 chars) + `caption-threads-reply-N.txt` (<= 500 chars each).
4. **Reel.** `python3 build_reel.py <spec.json> <out_dir>` (4 scenes,
   16 s, 2160x3840 yuv420p). Picks music EXACTLY ONCE via
   `brand/music/pick_reel_track.sh` (recorded in `track.txt`; a
   re-render reuses `track.txt` instead of picking a second track),
   renders frames with the megumi venv python, encodes with ffmpeg
   `-threads 2`, extracts the cover frame at 3.2 s as
   `<slug>-cover.jpg`. Scene 4 prints the blog shortlink. The hero
   image comes from the top-level `hero` field of spec.json;
   `build_reel.py` merges it into the flat reel-spec.json (a missing
   hero used to render as a black box: img src "undefined").
   Shortlinks are rendered in proportional bold (Poppins), never
   monospace: a mono font gives every "." a full-width cell, so
   `s.peka.ai.id` reads as "s . peka . ai . id".
5. **Blog.** `python3 make_blog_mirror.py <out_dir>` writes
   `peka-content/blog/<slug>.json`, copies the reel cover + slides
   into `peka-content/images/`, and backs the edition up (see below).
   The blog app reads the JSON dir on every request: no restart.
   Verify live: `curl -s -o /dev/null -w "%{http_code}"
   https://blog.peka.ai.id/p/<slug>` must be 200.
6. **Captions.** `caption-reel-ig.txt` / `caption-reel-fb.txt` (hook
   + short body + exactly one link instruction sentence, "Link blognya
   ada di akhir video.", no link in the text, no install commands) and
   `caption-tiktok.txt`.
7. **Post (interactive chat session only, approval cards surface).**
   `python3 post_tutorial.py <out_dir>`: Threads carousel + replies,
   IG reel, FB reel, then patches the blog JSON links. Idempotent via
   `post-done.txt`. Never run from a cron worker.
8. **Channel + TikTok package.** Broadcast via `telegram_channel.py
   --type tutorial` (channel captions MAY contain links) and deliver
   the TikTok package (slides + caption) to chat, like other pillars.

## Files

- `README.md` (this file)
- `carousel.py` — Threads carousel designer (PIL, 4096x4096)
- `make_blog_mirror.py` — blog JSON builder + per-edition backup
- `make_shortlink.py` — admin shortlink creator (direct DB insert)
- `post_tutorial.py` — poster (Threads + IG reel + FB reel), idempotent
- `build_reel.py` — reel orchestrator (music once, render, encode, cover)
- `animated/scene.html` — 4-scene reel template (Peka yellow/black)
- `animated/render.py` — Playwright frame renderer (4K, scale 2.0)
- `animated/assets/` — Poppins + DejaVu fonts, P mascot
- `templates/` — caption templates with placeholders
- `out/<date>-<short>/` — per-edition work dir (spec.json,
  article-body.html, shortlinks.json, reel-spec.json, track.txt,
  slide-1..6.png, `<slug>-reel.mp4`, `<slug>-cover.jpg`, captions,
  post-log.txt when posted)
- `posted.log` — one line per posted edition (written by post_tutorial.py)

## Locked Peka rules that apply here

- No link of any kind in post text on any platform. The blog
  shortlink is printed INSIDE the visual (reel scene 4, carousel
  slide 6) with exactly one instruction sentence in the caption.
- No install / terminal commands in any social caption. Install steps
  only inside the visual.
- Threads closing tag is #AI (locked). Threads caption stands alone,
  forced-choice closing question, root + max 4 replies.
- All reels are full animated motion graphics, 2160x3840 yuv420p.
  Slideshow / Ken Burns is not a reel.
- No em-dash / en-dash in any output file (code asserts on it).
- Every carousel/reels closes with Follow + community
  (Follow @peka.ai.id + s.peka.ai.id/gabung + save/share).
- Shortlinks are ALWAYS admin-owned (user_id 1) via direct DB insert,
  never the guest API.

## Push (verified 14 Nov 2026, no change needed)

`peka-content` is already in the auto-push list
(`workspace-auto-push.sh`, GitHub + GitLab). `tutorial-mirror/` is NOT
ignored (only `blog/` is ignored in `peka-content/.gitignore`), so the
scripts and the edition `out/` dirs are committed and pushed by the
15-minute auto-push like every other pillar. Verified: 2521 tracked
`*/out/*` files in peka-content (78 mp4). Do NOT add `out/` to
`.gitignore`; the mirror follows the same convention as the other
pillars.

## Autobackup (per-edition, this pillar only)

Real gap, found 14 Nov 2026: `peka-content/blog/*.json` is gitignored
and NO backup covers it (same for all Peka blog articles). Closed for
this pillar only: `make_blog_mirror.py`, after the blog JSON is
written, copies the blog JSON + the edition `spec.json` to
`~/workspace/backups/peka-blog-mirror/<slug>/` (created if missing).
Other pillars are untouched.

## Autopulih (no new code needed)

The mirror needs no new service and recovers with the Peka stack:
`recover-after-reboot.sh` restarts `peka-blog` + `peka-blog-tunnel`
(lines 65, 274-275); `peka-blog.service` is active on 127.0.0.1:18102;
cron definitions persist in `~/workspace/goals`. Same as HM/SPILL.
Note: if a reel render fails after a VM reset because the Playwright
browser cache is gone, that is the same risk as every other reel;
there is no separate installer for this pillar.

## Draft cron (daily afternoon, for the parent to create)

```text
job: peka-tutorial-mirror
schedule: daily ~15:00 WIB
timeout: 86400s
owner: goal peka-ai-public-brand
steps:
  1. Read today's source article: ~/workspace/blog/content/<today>-*.md
     (if the blog cron has not published yet, stop and report).
  2. Write spec.json + article-body.html (rewrite, 800-1200 words,
     code kept correct, FAQ 3-4, no em/en dash).
  3. python3 make_shortlink.py <out_dir> https://blog.peka.ai.id/p/<slug>
  4. python3 carousel.py <spec.json> <out_dir> (verify 6 slides 4096x4096)
  5. python3 build_reel.py <spec.json> <out_dir>
     (verify ffprobe: 2160x3840, yuv420p, ~16 s; cover exists)
  6. python3 make_blog_mirror.py <out_dir>
     (verify blog URL live 200; backup dir exists)
  7. Write all captions (Threads root + replies, IG/FB reel, TikTok).
  8. Report the edition to chat with the assets. DO NOT post from the
     cron: posting runs from an interactive chat session via
     python3 post_tutorial.py <out_dir> so approval cards surface.
```

## Verification checklist (every edition)

- `python3 -m py_compile` on all new/changed scripts.
- Blog JSON loads (`json.load`), no em/en dash in the JSON, all
  captions, or any slide text.
- Blog URL curls 200; shortlink redirects 307 to the blog URL.
- ffprobe reel: 2160x3840, yuv420p, ~15-16 s.
- All carousel slides 4096x4096.
- `post-done.txt` absent until posting; no channel broadcast sent
  during a dry-run.
