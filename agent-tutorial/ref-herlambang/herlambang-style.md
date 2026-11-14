# Herlambang Style Reference (FreeLLM API reel, 60s, 720x1280)

Source: https://www.facebook.com/reel/1496663065718486/ (Herlambang Awn, 14 Nov 2026)
Local copy: `ref-herlambang/video.mp4` + 8 frames (`f2/f8/f15/f22/f30/f38/f46/f54.jpg`)
Analyzed 15 Nov 2026 by watching the downloaded video frame by frame.

## Style breakdown

1. **Top tab bar (persistent)**: `// <section>` in monospace + 4 tabs
   (APA / MODEL / CARA / SETUP). Active tab = salmon fill (#E07856-ish),
   visited = dark navy, upcoming = white. Thin progress line under active tab.
   Small logo chip at the left.
2. **Backgrounds alternate per section**: light cream graph-paper grid
   (#F5F1E8-ish) and dark navy grid (#0F1030-ish); CARA section uses a
   purple grid (#5B2EE5-ish). Grid texture on every scene.
3. **Kinetic typography**: huge condensed bold sans (Anton/Oswald style) for
   keywords, with ONE accent word in red italic serif
   ("Claude", "top", "Gemini,", "berpura-pura"). Words appear in sync with
   the voiceover, one beat at a time.
4. **Illustrated avatar presenter**: bottom corner, comic-style man in suit
   with glasses, poses change per beat (pointing, thinking, thumbs up +
   "HAHA!" bubble, surprised). Pixel-art orange robot mascot floats around,
   sometimes sitting on his head.
5. **Neo-brutalist cards**: chunky cards, thick black borders, hard offset
   shadows. Types seen: info card (URL header + description + pills),
   comparison grid (active card solid + FREE pill, others grey dashed),
   terminal window (dark, `$ <command>`, step label "LANGKAH 1 · INSTALL"),
   server box ("FreeLLM API" + status dots).
6. **Structure**: 4 sections APA (what) -> MODEL -> CARA (how it works) ->
   SETUP (3 steps) + CTA. 60s voiceover-led, Indonesian.
7. **CTA**: follow + comment "REPO" to get the link via DM (DM-gated).

## Mapping to Peka Tutorial Agent template

- Tab bar maps to tutorial step groups, e.g. debut #01 "Bikin Agen AI
  Pertamamu dengan Python": KENAPA -> ALAT -> LANGKAH -> JALANKAN.
- Avatar presenter: use PIKO (existing anime mascot), NOT the creator's
  illustrated man. Need Piko poses: pointing, thinking, thumbs up,
  surprised. Existing reel-v2 Piko assets are a starting point.
- Colors: Peka yellow #FFD60A + black fits the neo-brutalist cards; cream
  grid paper matches Peka light aesthetic; dark navy grid matches the
  agent-console dark theme. Salmon accent can stay as the section accent
  or be swapped to Peka yellow.
- Terminal cards map directly to the agent tutorial's Python code steps.
- Voiceover + kinetic type maps to the existing reel-v2 pipeline
  (ArdiNeural TTS, 45-60s). Needs a new scene.html variant: tab bar,
  grid backgrounds, big-type scenes instead of karaoke captions.
- Carousel slides can reuse the same language (tab bar on slide 1,
  one card type per slide).

## What needs building (not started)

1. New reel-v2 theme variant (scene.html + CSS): tab bar, grid-paper
   backgrounds (light/dark/purple), chunky cards, condensed-bold +
   red-italic-serif type pair.
2. Piko presenter poses (4 expressions minimum).
3. Fonts: condensed bold (Anton/Oswald) + italic serif (Playfair italic).
4. Section/tab mapping per tutorial episode (4 tabs).

## Peka color mapping (approved by user 15 Nov 2026, "pake ini tapi sesuaikan dengan warna dari peka")

- Cream grid paper #F5F1E8: KEEP (Peka light aesthetic).
- Dark navy grid #0F1030 -> agent-console dark slate #0D1117.
- Purple grid #5B2EE5 (CARA section) -> Peka yellow #FFD60A grid, black text.
- Salmon active tab #E07856 -> Peka yellow #FFD60A fill, black text.
  Visited tabs dark slate, upcoming tabs white.
- Red italic serif accent word -> emerald #10B981 on light cream scenes,
  Peka yellow #FFD60A on dark scenes. The italic-serif form stays, the
  color becomes Peka.
- Chunky cards (black borders + hard shadows): keep. Highlight card =
  Peka yellow fill.
- Terminal window: dark slate #161B22 panel, emerald #10B981 accents,
  mono font (already agent-console).
- Avatar presenter: PIKO (anime chibi, existing reel-v2 assets), poses:
  pointing, thinking, thumbs up, surprised. NOT the creator's man.
- Fonts: condensed bold (Anton/Oswald) + italic serif (Playfair Italic).
- Header: Peka header lockup (mascot mark + peka.ai.id) on every slide
  and reel scene, per the locked agent-tutorial logo rule.
- Tabs for debut #01 "Bikin Agen AI Pertamamu dengan Python":
  KENAPA -> ALAT -> LANGKAH -> JALANKAN.
- Reel format changes for this style: 45-60s voiceover-led (reel-v2
  pipeline, ArdiNeural TTS), replacing the 16s music reel for the debut.
  Carousel stays 6 slides 4096x4096.

## Rules that still apply

- CTA stays Peka standard ("Follow dan gabung"). The video's DM-gated
  "comment REPO for link" CTA is NOT approved for Peka (same as the
  aishift DM-gated CTA rule).
- No link in caption text; shortlink printed inside the visual only.
- No install/terminal commands in captions; commands live inside the
  visual only (terminal cards are fine).
- No em-dash in any copy.
