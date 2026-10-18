# peka-content

Content engine behind Peka AI's public social accounts
(Instagram + Threads `@peka.ai.id`, Facebook Page PekaAI).

## What it does

Two scheduled runs a day (cron `peka-ai-content-siang` ~12:36 WIB and
`peka-ai-content-malam` ~19:36 WIB, Asia/Jakarta) produce and auto-post one
piece of content each:

1. **Pick a pillar** — rotation between AI info, AI tools, AI projects, and
   bansos (social-aid info). A selling pillar activates only when the owner
   drops product input in `sell-input.md`.
2. **Research the topic** — Threads trends + web news. Bansos items must come
   from official sources only (`kemensos.go.id`, government announcements);
   never invent program names, dates, or amounts.
3. **Write natural copy** — casual Indonesian social-media voice with a strong
   hook. Hard rule from the owner: *"jangan keliatan ai narasinya"* (must not
   read like AI wrote it). No "Sebagai AI...", no stiff formal prose, max
   1-2 emojis.
4. **Generate a 1080x1080 brand image** (black `#111111` background, yellow
   `#ffd60a` accent, P mascot) into `images/`.
5. **Auto-post** to Instagram (image + caption + hashtags), Threads (500-char
   limit: post + reply continuation, exactly 1 hashtag as topic tag), and the
   Facebook Page.
6. **Sync to the blog** — write `blog/<slug>.json`; `blog.peka.ai.id`
   (see `dasrams31/peka-blog`) picks it up automatically, no restart needed.
7. **Improvement loop** — read post insights, append metrics to
   `performance.log`, and distill 1-3 concrete lessons into `learnings.md`
   (`OBSERVED: ... / INFERRED: ...`). Every run reads `learnings.md` first,
   so the system keeps getting better.

## Layout

| Path             | Description                                              |
|------------------|----------------------------------------------------------|
| `learnings.md`   | Living playbook; read at the start of every run          |
| `blog/`          | Per-post JSON synced to the blog (generated, not in git) |
| `images/`        | Generated cover art (generated, not in git)              |
| `posted.log`     | `YYYY-MM-DD HH:MM\|pillar\|topic` (operational, not in git) |
| `performance.log`| Engagement metrics per platform (operational, not in git)|
| `brand/`         | P mascot logo assets + generator (approved 2026-10-18)   |

The cron job bodies (full step-by-step instructions) live in the scheduler,
not in this repo. Logs and generated assets are operational data and are
git-ignored on purpose.
