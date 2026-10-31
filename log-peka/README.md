# LOG PEKA — honest experiment log (weekly, Saturdays 16:00 WIB)

One running experiment per cycle, reported as a numbered day count.
The log reports what Peka actually tried that week and what the numbers
actually did. No personal-story fiction: the "days" are real days since
the experiment started, and every number must trace to `performance.log`
or a live platform read. If a number cannot be verified, the slide says
"belum terukur". Never invent metrics.

## Design

Same navy BLUEPRINT tokens (navy `#0A1A30`, grid, hairlines, mono
annotations, Peka yellow `#FFD60A`), but this is NOT Blueprint: no repo,
no repo-page scene. 4 slides (4096x4096) + 1 animated reel (15 s,
2160x3840, yuv420p). Stamp reads `LOG EKSPERIMEN`, not `BLUEPRINT`.

## Files

- `log_peka.py` — slide generator (spec-driven, all copy from spec).
- `animated/scene.html` + `animated/render.py` — reel template (4 scenes:
  cover / numbers / findings / question + follow). Same `renderAt`
  engine as the Blueprint template (fade/slide `data-in`, progress bar).
- `animated/assets/` — fonts + keyed mascot (copied from Blueprint).
- `experiment.json` — the running experiment (topic, hypothesis,
  start date, verdict due, status). Day count rule: the first full day
  under the experiment is day 1, so
  `day = (edition_date - start_date).days + 1`.
- `notes.md` — dated observations, appended by every edition run.
- `series.txt` — next edition number. `posted.log` — posting record.

## Spec format (slides + reel share one spec file)

```json
{
  "edition": 1,
  "day": 7,
  "date_range": "1 - 7 NOV 2026",
  "experiment": "TANPA LINK DI TEKS",
  "title": ["Views balik", "belum?"],
  "hypothesis": "Hipotesa: ...",
  "stats": [
    {"value": "21", "label": "VIEWS SPILL #10"},
    {"value": "88", "label": "VIEWS HM 30 OKT"},
    {"value": "0", "label": "KOMENTAR LINK TERKIRIM"}
  ],
  "compare": "vs minggu lalu: ...",
  "findings": [
    {"title": "...", "desc": "..."}
  ],
  "question": ["Lanjut tanpa link,", "atau balik pakai link?"],
  "out_dir": "/abs/path/out/<YYYY-MM-DD>/carousel"
}
```

Constraints: exactly 3 stats, exactly 3 findings, title max 2 lines,
question max 2 lines, no em/en-dash, casual + gentle plain language,
"AI" never "mesin". No external link: nothing is printed as a shortlink
and captions carry no link instruction sentence.

## Render

Slides: `python3 log_peka.py <spec.json>` (reads `out_dir` from spec).

Reel: `cd animated && <megumi venv python> render.py <reel-spec.json>
<frames dir> 24 15 2.0`, then ffmpeg encode like the other pillars
(`scale=2160:3840`, yuv420p, one music pick per edition via
`pick_reel_track.sh`, cover at 1 s, ffprobe + frame checks t=2/6/10/14).
The reel spec is the same JSON file as the slide spec.

## Schedule

Cron `peka-log-mingguan`, Saturdays 16:00 WIB, owner
`goal:peka-ai-public-brand`. Threads carousel first, then IG reel and
FB reel. No blog, no comments anywhere. HTTP 429 = total stop.
Delivery to chat: slides + reel + captions + TikTok caption.
