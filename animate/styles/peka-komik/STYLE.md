# Style: peka-komik

The Peka comic look: a two-era comic panel — a dark navy night panel where
Piko is confused by too many AI choices, morphing into a cream morning
panel where Peka picks one. Thick black panel frames, halftone corners,
speech bubbles, a starburst shout, action lines, and Piko drawn as a
vector — he IS the Peka logo mark (capsule stem + detached D-bowl, solid
eye, half-disc smile, yellow antenna), never a font letter. Made from
the approved piece `pieces/peka-komik/` (look check + 2 revision
rounds + voice-over, user approved 2026-11-16). Built on the cut-paper
kit (torn cutouts, paper grain, hand text, paper tags) plus the comic
helpers below.

## Palette (locked)

| colour | hex | meaning |
|---|---|---|
| Peka yellow (accent) | `#ffd60a` | Piko, the sun, the burst — the hero colour, never the ground |
| ink | `#141210` | panel frame, outlines, hand text |
| cream paper | `#f5f1e8` | day ground, caption paper, `STYLE.paper` |
| night navy | `#141c40` | night ground (`PAL.night` from cut-paper) |
| moon cream | `#f6ecc8` | the moon |
| sweat blue | `#4c6fb5` | Piko's confused sweat drop |
| check green | `#3d7c46` | checkmarks |

Ground rule (learned in the piece's look check round 1): the morning
ground must be cream, never yellow — on a yellow ground Piko renders
outline-only because he is the same yellow as the ground.

## Piko — the logo mark (locked, 2026-11-16)

Piko IS the Peka logo (`~/workspace/peka-logo/mascot-p.png`,
1080x1080), drawn in vector by `comicPiko`. He is never a font
letter: the old Arial Black `P` (stem and bowl connected, arc eye,
white eye highlight, ink outline on the yellow, black antenna line)
was not the logo and was replaced 2026-11-16 on the user's word
("maskot Peka harus sama dong sama logo Peka"). Geometry measured
off `mascot-p.png`, logo px, origin at the stem's top-left, body
box 290 x 502:

| part | geometry |
|---|---|
| stem | capsule x 0–130, y 0–502, corner radius 65 |
| bowl | D-shape: flat left edge x 150, y −5–275; right edge a semicircle of radius 140 centred at (150, 135); 20px gap to the stem (x 130–150) |
| notch | black half-disc on the bowl's flat edge, centre (150, 135), radius 40, right half only — the gap stays background |
| eye | solid black circle, centre (60, 125), radius 45 — no white highlight dot, the logo eye has none |
| smile | solid black half-disc (lower half), centre (60, 245), radius 33 — not a stroked arc |
| antenna | yellow line x 57–73 (centre 65), y −80–0, width 16; yellow ball centre (65, −115), radius 28 |
| colours | yellow `#ffd60a`, face ink `#111` (kit `INK`) |

Rules:

- No `fillText('P')` / `strokeText` anywhere in the style; no ink
  stroke around any yellow shape (stem, bowl, antenna line, ball).
- The kit accent must stay `#ffd60a` in every piece that uses
  `comicPiko` (it fills from `COMIC.accent`); a variant that recolours
  the accent must draw its own Piko locked to `#ffd60a`, as
  `peka-komik-deepseek-30s` does with its local `piko()`.
- Moods: `'happy'` / `'wow'` = the logo face exactly (round eye +
  half-disc smile); `'confused'` = the same face + the blue sweat drop.
- The body box is scaled to the old glyph's footprint (height
  `0.729 * size`, bottom at `y + 0.42 * size`) so scene layouts,
  bubble positions and tail anchors do not shift; the antenna extends
  above the body like before, at logo proportions (shorter than the
  old font-P antenna — the morning tail in `peka-komik-tierlist-30s`
  now ends ~90px above the ball instead of 15–31px; that is the
  logo's antenna, not a layout bug).

## Line and texture

Weights are relative to the frame (`UNIT` = min(W, H) / 1080; at
1080x1920 UNIT = 1):

| element | weight |
|---|---|
| panel frame (`comicPanelFrame`) | 16*UNIT, inset 14*UNIT, round joins |
| bubble / burst outline | 7*UNIT (bubble), 6*UNIT (burst, "?" bubbles, checks) |
| Piko (logo mark) | no outline on the yellow; antenna line 16*k, eye r 45*k, smile half-disc r 33*k, bowl notch r 40*k (k = body height / 502) |
| sun rays (`comicRays`) | 9*UNIT; action lines 7*UNIT |
| morph window rim (`STYLE.window`) | 12*UNIT ink |

Texture: halftone corner dots (`comicHalftone`, gap 46*UNIT, max radius
7*UNIT, denser toward the corner) + a faint dots pattern on the ground
(`pat.dots`, accent at 0.16 alpha on night, ink at 0.10 on day) + light
paper grain in `post()` (2200 specks). No gradients, no glow, no drop
shadow except the small cutout shadows on bubbles, bursts and checks.

Type: hand text (`handText`, the HAND stack) bold 700–800 for bubbles
and bursts, 62*UNIT bubble text, 50*UNIT burst text; Piko is vector
only, no text. Year tag 80, caption strip 50.

## Motion habits

- On 2s (`ones: false`): the boil steps every 2 frames.
- Speech bubbles and bursts pop in with a back-eased overshoot
  (`popS`, ~0.25s): bubble at the voice line start + 0.05s (night 0.35s,
  morning M1 + 0.35s), burst at wake + 0.6s.
- Action lines grow in one by one from the wake (staggered 0.04s,
  0.25s each).
- Piko idles with a sine bob (8*UNIT, 0.9 Hz) and hops 70px over 0.5s
  at the morph (`hopT`).
- The morph is marked by a brief white flash (`comicFlash(tMorph)`:
  window [tMorph − 0.1, tMorph + 0.3], peak 0.5 alpha at tMorph + 0.1).

## Frame checklist (on top of grammar/FRAME.md)

- 0 text cut off; no element hidden behind a bubble, the caption strip
  or the phone UI strip (right 140px, top 240px, bottom 420px).
- The burst clears the caption strip (≥ 30px) and the right frame edge
  (≥ 60px); the checkmark row clears the caption strip (≥ 70px).
- The sun/moon never hides behind the speech bubble (keep it at
  (0.80, 0.17), bubble centre ≤ 0.44 x).
- The panel frame is unbroken on all four sides; the halftone corner
  never covers the year tag.
- Piko's eye and sweat drop are visible at phone scale; his antenna
  ball never touches the bubble tail. Logo checks: capsule stem +
  detached D-bowl with a visible gap, solid round eye fully on the
  stem, black notch on the bowl's flat edge, yellow antenna centred on
  the stem and clearly visible (not hidden behind a bubble tail), no
  ink outline on any yellow shape.
- During a morph, stills taken within ~0.5s of the morph centre show
  the paper backdrop — pick sample times at least 0.6s away from it.

## Kit API

Inherited from cut-paper (same names, same behaviour): `PAL`,
`handText`, `handW`, `dot`, `cut`, `rect`, `pat`, `face`, `spark`,
`person`, `hand`, `clock`, `cat`, `mug`, `plant`, `books`, `sparkle`,
`tag`, `yearTag`, `capStrip`. Two differences from cut-paper: `tag`
defaults to comic paper (`#f5f1e8`) and comic ink (`#141210`), and
`COMIC` / `INK` / `PEKA_Y` / `PEKA_CREAM` are the palette aliases.

Comic helpers (all `comic`-prefixed — `burst` is a core name and must
never be redeclared):

| helper | what |
|---|---|
| `comicGround('night' \| 'day')` | full-bleed ground + faint dots pattern |
| `comicPanelFrame()` | thick black panel frame over the scene |
| `comicHalftone(x0, y0, x1, y1, gap, maxR, color)` | halftone corner, denser toward (x0, y0) |
| `comicBubble(cx, cy, w, h, str, size, tailX, tailY, t0)` | speech bubble, pops in at t0 |
| `comicThought(x, y, str, t0, r?)` | round "?" bubble, pops in at t0 |
| `comicBurst(cx, cy, r, str, size, t0)` | 12-point starburst shout, pops in at t0 |
| `comicFlash(tMorph)` | white flash at the morph |
| `comicActionLines(x, y, t0, n?, color?)` | action lines growing one by one |
| `comicCheck(x, y, t0)` | one checkmark circle, pops in at t0 |
| `comicRays(x, y, r, n?)` | thick sun rays |
| `comicPiko(x, y, s, mood, hopT?)` | the hero, drawn as the Peka logo mark (see "Piko — the logo mark"); mood `'confused'` \| `'happy'` \| `'wow'` (= happy) |
| `comicMotif(x, y, s, t0)` | the episode motif emblem (see Variants) |

`STYLE` hooks: `paper` = cream; `backdrop` = flat fill + faint dots;
`window` = the world seen through the bridge shape with a 12*UNIT ink
rim; `blob` = flat fill with a 6*UNIT ink outline; `hero` = `comicPiko`
(r/170 scale, mood from the bridge or `'happy'`); `heroColor` = accent;
`heroPts` = an ellipse outline; `post` = light grain; `ones: false`.

## Variants

A piece may list `src/options.js` in its `piece.json` `"build"` BEFORE
the style, defining either or both of:

```js
const COMIC_PALETTE = { ground1, ground2, accent, accent2, ink, paper };
const COMIC_MOTIF = 'trophy' | 'terminal' | 'tier' | 'default';
```

```json
"build": ["src/head.html", "kit/core.js", "src/options.js", "style",
          "src/scenes.js", "src/bridges.js", "kit/morph.js", "kit/board.js",
          "kit/score-head.js", "src/score.js", "kit/score-tail.js"]
```

The kit reads both with a `typeof` guard; any key left out keeps the
locked default. `COMIC_PALETTE` keys: `ground1` (night ground),
`ground2` (day ground), `accent` (Piko / sun / burst), `accent2`
(moon), `ink` (outlines / text), `paper` (caption paper, morph sheet).
`COMIC_MOTIF` picks the emblem `comicMotif` draws: `trophy` (a cup),
`terminal` (a dark window with an accent `>_` prompt), `tier` (S/A/B
bars), `default` (a small accent star). The batch episodes use:
Claude Fable 5.2 → dark navy + gold palette, `trophy`; DeepSeek
harness → terminal green accent, `terminal`; tier-list skripsi →
cream + red palette, `tier`.

Note: the kit's own constant for the motif is named `COMIC_MOTIF_SEL`
— a kit must not declare a `const` with the same name as the option it
reads, or the `typeof` guard hits the temporal dead zone and the build
fails with `Cannot access 'COMIC_MOTIF' before initialization`.

## Do / don't

- Do keep the palette locked per episode; change it only through
  `COMIC_PALETTE` in `src/options.js`, never by editing the kit.
- Do keep one hero colour (the accent) and one ink; a second accent
  turns the panel muddy.
- Do put the sun/moon top-right, the bubble top-centre, Piko centre,
  the burst lower-right, the checks in a row above the caption strip.
- Don't put yellow on yellow (Piko on a yellow ground, burst on the sun).
- Don't print theme names on the final design (internal labels only).
- Don't use the burst for plain text — it is a shout, one or two words.
- Don't add a second hero; `spark` from cut-paper is available but off-look here.

## Not matched

- The reference piece's scenes are hand-placed per episode; the kit
  does not auto-lay-out a panel (no grid, no auto-flow).
- The motif emblems are simple geometric marks, not detailed
  illustrations of a trophy / terminal / tier chart.
- The voice-over sync (bubble pop at line start + 0.05s) is a per-piece
  coupling to `voice/script.json`, not something the kit knows.

## Proven on

- `pieces/peka-komik/` (8s, 1080x1920, review PASS all checks,
  −14.5 LUFS, true peak −3.4 dBFS) — the look this style was ported from.
- `styles/peka-komik/demo/` (6s, two eras, one moon → sun morph):
  build OK, tile deterministic: true, stills eyeballed against
  `look-night.png` / `look-morning.png`.
