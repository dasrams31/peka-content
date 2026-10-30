# BLUEPRINT — weekly GitHub tool series

Status: LIVE. Approved by user 2026-10-31 05:25 WIB (name BLUEPRINT,
Friday 20:00 WIB slot, edition 01 = Cindy). Edition 01 assets built and
verified 2026-10-31; posting scheduled via runonce cron the same day
20:00 WIB. Not a SPILL edition and not Repo of the Week. SPILL
`series.txt` / `posted.log` / live template untouched.

## Decisions (user, 2026-10-31)

- Theme direction 3: technical drawing / blueprint.
- Content: GitHub repos only, 1 repo per edition.
- Cadence: new dedicated series, once a week, Fridays 20:00 WIB.
- Name: BLUEPRINT.
- Edition 01: makecindy/cindy (facts verified from README + API,
  8,706 stars at render time; shortlink https://s.peka.ai.id/2y12kr,
  admin-owned; already in tools.json).
- No blog for BLUEPRINT.

## Design tokens

- Background `#0A1A30` (deep navy), panel `#10264A`, grid `#1A2E4E`,
  hairline `#3D5A80`, text `#F2F5F9`, muted `#8FA6C2`, accent `#FFD60A`.
- Headlines Poppins ExtraBold, annotations DejaVu Sans Mono.
- Motifs: faint 135-unit grid, frame with yellow corner crosses,
  dimension labels, dashed annotation boxes and chips, flow diagrams
  (INPUT -> TOOL -> OUTPUT, tool node filled yellow), section labels
  `NN / TITLE` with a hairline rule.
- Peka lockup (mascot + peka.ai.id) top right, community footer bottom.
  Mascot must be the chroma-keyed transparent PNG
  (`preview/mascot-keyed.png`, threshold 30, also copied to
  `animated/assets/mascot-keyed.png`); never use CSS
  `mix-blend-mode: screen` on the opaque source, it leaves a dark box.

## Files

- `blueprint.py` — spec-driven 4-slide generator (4096x4096).
  Headline rule position is computed from font metrics
  (`headline_block`), never a fixed y, so the rule never strikes
  through headline text. Step titles/descs are wrapped to the card
  width; slide 3 carries no separate note line (it collided with the
  footer) — the provider-cost note lives in the captions instead.
- `animated/` — spec-driven animated reel template (cover 3 s + repo
  8 s + question 2 s + follow 2 s = 15 s, 2160x3840, yuv420p).
  Same fade/slide/typing/progress engine as the SPILL template.
  `animated/README.md` has the render + encode commands.
- `blueprint_preview.py` + `preview/` — the original 2-slide + 1-scene
  preview (kept for reference; the final slides differ: rule position,
  wrapped steps, row-style follow slide).
- `series.txt` — next edition number (1 before edition 01 posts,
  2 after). `posted.log` — posted editions. `repos/posted.log` —
  repos already used, never repeat.

## Crons

- `peka-blueprint-weekly` — Fridays 20:00 WIB, owner
  goal:peka-ai-public-brand. Full build + post per edition.
- `peka-blueprint-cindy-31okt` — runonce 2026-10-31 20:00 WIB,
  posts the pre-built edition 01 assets only.

## Edition 01 output

`out/2026-10-31-cindy/`: `carousel/blueprint-01..04.png`,
`blueprint-reel.mp4` (Volatile Reaction by Kevin MacLeod, one
`pick_reel_track.sh` call), `blueprint-reel-cover.jpg`,
`reel-spec.json`, `spec.json`, `shortlinks.json`,
`caption-{ig,fb,threads,tiktok}.txt`, `comment-{threads,fb}.txt`,
`track.txt`, `shots/makecindy-cindy.png`.
