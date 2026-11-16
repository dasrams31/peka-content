// =====================================================================
//  SCENES — Komik Peka #03: tier-list AI buat skripsi.
//  F2 morph chain, same moon -> sun morph as peka-komik. Variant 'tier',
//  cream ground + red accent (RED, local: the kit accent stays Peka
//  yellow so Piko keeps his yellow P). Scene 1: Piko confused, ringed
//  by six tool-name chips. Scene 2: the tier list itself — four rows
//  (S/A/B/D) with a letter chip, the tools, and one short verified
//  free-limit line per row; Piko happy beside the list. The bubble tail
//  runs down the clear channel right of the rows to Piko's antenna (see
//  morningTail); there is no red arrow — it used to share that channel
//  with the tail and read as one confused gesture.
//  Layout notes (extra polish pass): every right-hand element ends
//  at x <= 940 (phone UI strip); the top chip row sits 50px below the
//  speech bubble; tier rows clear the bubble by 23px and the caption
//  strip by 125px; Piko's column (x 770-958) never touches the tier
//  strips (end x 740) or the sun rays.
// =====================================================================
const MOON = () => [LX(0.80), LY(WIDE ? 0.20 : 0.17), 40 * UNIT];
const SUN = () => [LX(0.80), LY(WIDE ? 0.20 : 0.17), 80 * UNIT];
const RED = '#c1272d';   // episode accent: tier chips, limit lines
// (INK / PEKA_Y / PEKA_CREAM come from the style kit — do not redeclare.)

// a floating tool-name pill (white, ink outline), pops in at t0.
function chip(cx, cy, str, t0) {
  const k = popS(t0); if (k <= 0.01) return;
  const u = UNIT, size = 40 * u;
  const w = handW(str, size, 700) + 56 * u, h = 76 * u;
  ctx.save(); ctx.translate(cx, cy); ctx.scale(k, k); ctx.translate(-cx, -cy);
  cut(rect(cx - w / 2, cy - h / 2, w, h, 30), '#ffffff', { key: 'chip' + str, shadow: true, tear: 0, line: INK, lw: 6 * u });
  handText(str, cx - handW(str, size, 700) / 2, cy + size * 0.36, size, INK, { weight: 700, key: 'chipt' + str });
  ctx.restore();
}
// left- / right-aligned chip columns (shared edge, not shared centre,
// so different name lengths still line up): left edge x 60, right edge
// x 920 (phone UI strip starts at 940).
function chipL(xLeft, cy, str, t0) {
  const w = handW(str, 40 * UNIT, 700) + 56 * UNIT;
  chip(xLeft + w / 2, cy, str, t0);
}
function chipR(xRight, cy, str, t0) {
  const w = handW(str, 40 * UNIT, 700) + 56 * UNIT;
  chip(xRight - w / 2, cy, str, t0);
}
// Pops in (back-eased) at t0, scaled about the strip centre.
function tierRow(cy, letter, fill, fg, tools, limit, t0) {
  const k = popS(t0); if (k <= 0.01) return;
  const u = UNIT, cx = 396 * u, x0 = 52 * u, x1 = 740 * u, h = 148 * u;
  ctx.save(); ctx.translate(cx, cy); ctx.scale(k, k); ctx.translate(-cx, -cy);
  cut(rect(x0, cy - h / 2, x1 - x0, h, 12), '#ffffff', { key: 'tier' + letter, shadow: true, tear: 0, line: INK, lw: 5 * u });
  cut(rect(64 * u, cy - 42 * u, 84 * u, 84 * u, 12), fill, { key: 'tierchip' + letter, shadow: false, tear: 0, line: INK, lw: 5 * u });
  handText(letter, 106 * u - handW(letter, 52 * u, 800) / 2, cy + 52 * u * 0.36, 52 * u, fg, { weight: 800, key: 'tierl' + letter });
  handText(tools, 176 * u, cy - 6 * u, 46 * u, INK, { weight: 700, key: 'tiert' + letter });
  handText(limit, 176 * u, cy + 52 * u, 32 * u, RED, { weight: 700, key: 'tierlim' + letter });
  ctx.restore();
}
// Morning bubble tail, drawn BEFORE the bubble so the bubble rect covers
// the tail's base inside the body (same construction as comicBubble's own
// tail). Base (750,570)-(805,570) sits inside the bubble (x 94-814,
// y 453-583); the tail emerges from the bottom edge at y 583 and runs
// straight down the clear channel right of the tier strips (strips end
// x 740; the tail's left edge is x 760 at the S-row top, x 799 at the
// S-row bottom) to a tip at (853,960), on Piko's antenna axis (ball
// centre x 853), 15-31px above the antenna ball top (975-991 with the
// idle bob), so it points at Piko without touching the ball. Same
// popS(t0) transform about the bubble centre as comicBubble, so tail and
// bubble pop in together. The red arrow that used to run in this channel
// is removed: two near-parallel lines here read as one confused gesture.
function morningTail(t0) {
  const k = popS(t0); if (k <= 0.01) return;
  const u = UNIT, cx = LX(0.42), cy = LY(0.27);
  ctx.save(); ctx.translate(cx, cy); ctx.scale(k, k); ctx.translate(-cx, -cy);
  cut([[750 * u, 570 * u], [853 * u, 960 * u], [805 * u, 570 * u]], '#ffffff', { key: 'btailfix-morning', shadow: false, tear: 0, line: INK, lw: 7 * u });
  ctx.restore();
}
function sceneNight() {
  const u = UNIT, [mx, my, mr] = MOON();
  comicGround('night');
  comicHalftone(LX(0.62), LY(0.02), W, LY(0.3), 46 * u, 7 * u, 'rgba(255,255,255,0.35)');
  cut(ellipsePts(mx, my, mr, mr, 0, 30), COMIC.accent2, { key: 'moon', line: INK, lw: 6 * u });
  // six tool chips ringing the confused hero, popping in one by one
  const chips = [['L', 0.36, 'Elicit'], ['R', 0.36, 'ChatGPT'], ['L', 0.60, 'NotebookLM'], ['R', 0.60, 'SciSpace'], ['L', 0.70, 'Gemini'], ['R', 0.70, 'Gamma']];
  chips.forEach(([side, fy, str], i) => (side === 'L' ? chipL(60 * u, LY(fy), str, TIMELINE.cues.wake + i * 0.15) : chipR(920 * u, LY(fy), str, TIMELINE.cues.wake + i * 0.15)));
  // action lines around the confused hero: grow in one by one from the wake
  const hx = LX(0.46), hy = LY(0.52);
  comicActionLines(hx, hy, TIMELINE.cues.wake);
  comicPiko(hx, hy, 1.0, 'confused');
  // short tail to the top of Piko's antenna (hx-20, hy-290): a long tail
  // to the body reads as a black spike and clips the Elicit chip.
  comicBubble(LX(0.46), LY(0.28), 840 * u, 130 * u, 'AI buat skripsi, mana yang tier S?', 44 * u, hx - 20 * u, hy - 290 * u, 0.35);
  comicPanelFrame();
  comicFlash(M1);
  yearTag('Tier-list?');
  capStrip('Mana yang tier S?');
}
function sceneMorning() {
  const u = UNIT, [sx, sy, sr] = SUN();
  comicGround('day');
  comicHalftone(0, LY(0.68), LX(0.4), H, 46 * u, 7 * u, 'rgba(20,18,16,0.25)');
  cut(ellipsePts(sx, sy, sr, sr, 0, 36), COMIC.accent, { key: 'sun', line: INK, lw: 6 * u });
  comicRays(sx, sy, sr, 10);
  // the tier emblem (variant motif), top centre-right, clear of the
  // year tag (ends x 542) and the sun (starts x 784)
  comicMotif(LX(0.62), LY(0.10), 0.8, M1 + 0.3);
  // the speech bubble FIRST, with its built-in tail hidden inside the
  // bubble body: the tip sits at the bubble centre, 10px above its
  // bottom edge, so the bubble rect (drawn after the tail by
  // comicBubble) covers it completely. The visible tail is morningTail(),
  // drawn just before the bubble down the clear channel right of the
  // tier strips — the old long tail crossed rows S/A and the strips
  // covered its middle, so it looked cut off at the S row. Bubble body
  // (y 453-583) never touches the rows (from 606).
  morningTail(4.35);
  comicBubble(LX(0.42), LY(0.27), 720 * u, 130 * u, 'Cek batas gratisnya dulu!', 48 * u, LX(0.42), LY(0.27) + 55 * u, 4.35);
  // the tier list: one row per tier, popping in one by one
  const rows = [
    ['S', RED, '#ffffff', 'Elicit, ChatGPT', 'Cari jurnal + chat teks gratis'],
    ['A', INK, '#ffffff', 'NotebookLM, SciSpace', '50 sumber/notebook · 100 kredit/bln'],
    ['B', '#ffffff', INK, 'Gemini', 'Kuota refresh tiap 5 jam'],
    ['D', '#ffffff', RED, 'Gamma', '400 kredit, sekali saja'],
  ];
  rows.forEach(([letter, fill, fg, tools, limit], i) =>
    tierRow(LY([0.354, 0.445, 0.536, 0.628][i]), letter, fill, fg, tools, limit, TIMELINE.cues.flowers + i * 0.25));
  comicPiko(LX(0.80), LY(0.60), 0.55, 'happy', M1);
  comicPanelFrame();
  comicFlash(M1);
  yearTag('peka.ai.id');
  capStrip('Cek batas gratisnya dulu.');
}
