# Threads Carousel template (reel-v2 -> carousel)

Turns a reel-v2 `spec.json` (hook + beat scenes + close) into a square
4096x4096 carousel for Threads, in the spec's own theme. Built for the
question "konten video di Threads diganti carousel aja gimana?" — data
says yes: Threads carousels beat Threads reels in Peka's own numbers
(SPILL carousel median 12 likes / 604 views; BLUEPRINT #03 carousel
51 likes / 4.590 views; Komik #02 reel 1 like / 81 views; AI Pekan Ini
video 0 likes / 112 views).

## Usage

```bash
python3 carousel.py <spec.json> <out_dir> [--theme THEME] [--link SHORTLINK]
```

Example (test edition, AI Pekan Ini #02):

```bash
python3 carousel.py \
  ~/workspace/peka-content/weekly-ai/out/2026-11-22-agentic-ai/spec.json \
  ~/workspace/peka-content/threads-carousel/out/2026-11-22-ai-pekan-ini-02
```

With an edition shortlink printed on the closing slide:

```bash
python3 carousel.py <spec.json> <out_dir> --link "S.PEKA.AI.ID/XXXXXX"
```

Output: `threads-carousel-01.png` .. `threads-carousel-NN.png` + `manifest.json`.
No network, no browser — pure PIL, renders in ~20s for 6 slides.

## Slide system

| # | Kind | Content |
|---|------|---------|
| 1 | Cover | Series chip, headline (hook scene), sub, Piko mascot, "GESER BUAT BACA >>" |
| 2..N-1 | Beat (stat) | Ghost number, stat hero (e.g. `2,5x`), stat label, lines with `<b>` in accent |
| 2..N-1 | Beat (bars) | Stat hero + label, then horizontal bars with labels, values, `TERTINGGI` tag |
| 2..N-1 | Beat (lines) | Stacked statements with accent square bullets |
| N | Close | Question headline, follow line, community chip, optional `--link` chip, Piko mascot |

Every slide: kicker/number header with progress hairline, footer
`GABUNG KE KOMUNITAS KAMI: S.PEKA.AI.ID/GABUNG` + page number.
Themes come from `reel-v2/themes.json` (peka-yellow, dark-grid,
navy-tech, rute-green); grid background, chip, accent and mono colors
follow the theme. Mascot poses come from the spec
(`reel-v2/assets/character/piko-anime-*.png`).

## Design rules

- Slides carry the punchy facts only. The voiceover narration stays in
  the caption, which the posting cron writes.
- Decimal separator is the comma (`70,6%`), matching the stat hero.
- Tag chips never sit past a full-width bar: they go on the label row.
- No link in caption text except the single locked instruction sentence
  (`Linknya ada di slide terakhir.`); the edition shortlink lives only
  in the closing-slide chip (`--link`).

## Wiring (DONE 22 Nov 2026, user order "semua konten threads pake carousel")

WIRED into the crons — Threads video is gone everywhere:
- `peka-weekly-ai`, `peka-bandingin-model`, `peka-coba-dulu`,
  `peka-tanya-jawab`: build the carousel from the same spec.json the
  reel used (`carousel.py <spec> <out>/threads-carousel --link
  "S.PEKA.AI.ID/<blog shortlink>"`), QA slide 1 + one middle slide,
  then publish the slides. Theme/colors follow spec.json
  automatically (navy-tech / peka-yellow / dark-grid) — never pass
  `--theme` to override. Caption carries "Linknya ada di slide
  terakhir."
- `peka-agent-tutorial` (build-only cron): `post_agent.py` posts the
  6 slides the cron already built (`slide-1.png` .. `slide-6.png`)
  as the Threads root; chained replies unchanged.
- `peka-komik-peka`: 6 stills via ffmpeg (seconds 1, 6, 11, 16, 21,
  26) from share.mp4, QA each still, publish as carousel. Same art,
  so colors/theme match the reel by construction.

8 other pillars were already carousel on Threads (SPILL, HM chain,
Prompt, Gratisan, Gratisan Mahasiswa, Bansos, BLUEPRINT, Tutorial
Mirror). IG/FB keep the reel. Playbook rule updated.
