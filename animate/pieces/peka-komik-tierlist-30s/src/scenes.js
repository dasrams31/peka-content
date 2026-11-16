// =====================================================================
//  SCENES — Komik Peka #03 (30 detik): tier-list AI buat skripsi.
//  F2 morph chain, same moon -> sun morph as the 8s version, morph at
//  12.0s (the night era holds three short lines, so it ends earlier
//  than #01/#02's 14.0s). Variant 'tier', cream ground + red accent
//  (RED, local: the kit accent stays Peka yellow so Piko keeps his
//  yellow P). Scene 1: Piko confused, ringed by six tool-name chips
//  that pop in two per night line. Scene 2: the tier list itself —
//  four rows (S/A/B/D) with a letter chip, the tools, and one short
//  verified free-limit line per row, popping in one per morning line
//  (S with l4, A with l5, B and D with l6); Piko happy beside the
//  list. The bubble tail runs down the clear channel right of the rows
//  to Piko's antenna (see morningTail); there is no red arrow — it used
//  to share that channel with the tail and read as one confused gesture.
//  The story advances through the dialogue: the night bubble swaps at
//  every night line, the morning bubble swaps at every morning line,
//  and the caption strip carries one fact per line (stripAt). Panel
//  layouts are the 8s layouts verbatim (same coordinates, same
//  clearances, already verified).
//  Voice coupling (see voice/voice.json): night lines l1 0.30, l2 3.08,
//  l3 6.74; morph 12.0; morning lines l4 12.28, l5 16.05, l6 20.33,
//  l7 25.02. Bubbles pop at line start + 0.05s; strips switch at the
//  line start. If the script timing changes, update both.
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
// The caption strip follows the voice: one fact per line. pairs are
// [line-start-time, text]; the latest one at or before TT wins.
function stripAt(pairs) {
  let cur = pairs[0][1];
  for (const [t0, str] of pairs) if (TT >= t0) cur = str;
  capStrip(cur);
}
function sceneNight() {
  const u = UNIT, [mx, my, mr] = MOON();
  comicGround('night');
  comicHalftone(LX(0.62), LY(0.02), W, LY(0.3), 46 * u, 7 * u, 'rgba(255,255,255,0.35)');
  cut(ellipsePts(mx, my, mr, mr, 0, 30), COMIC.accent2, { key: 'moon', line: INK, lw: 6 * u });
  // six tool chips ringing the confused hero, two per night line
  const chips = [['L', 0.36, 'Elicit', 0.35], ['R', 0.36, 'ChatGPT', 0.50], ['L', 0.60, 'NotebookLM', 3.13], ['R', 0.60, 'SciSpace', 3.28], ['L', 0.70, 'Gemini', 6.79], ['R', 0.70, 'Gamma', 6.94]];
  chips.forEach(([side, fy, str, t0]) => (side === 'L' ? chipL(60 * u, LY(fy), str, t0) : chipR(920 * u, LY(fy), str, t0)));
  // action lines around the confused hero: grow in one by one from the wake
  const hx = LX(0.46), hy = LY(0.52);
  comicActionLines(hx, hy, TIMELINE.cues.wake);
  comicPiko(hx, hy, 1.0, 'confused');
  // the dialogue, one bubble per line: only the current line's bubble is
  // drawn (a later bubble pops over the earlier one, so drawing all of
  // them would stack hidden strings under the visible one and the review
  // would flag them as overlapping text). The swap is a hard cut + pop.
  // short tail to the top of Piko's antenna (hx-20, hy-290): a long tail
  // to the body reads as a black spike and clips the Elicit chip.
  if (TT < 3.13) comicBubble(LX(0.46), LY(0.28), 840 * u, 130 * u, 'AI buat skripsi, mana yang tier S?', 44 * u, hx - 20 * u, hy - 290 * u, 0.35);
  else if (TT < 6.79) comicBubble(LX(0.46), LY(0.28), 840 * u, 130 * u, 'Enam nama, batasnya beda!', 44 * u, hx - 20 * u, hy - 290 * u, 3.13);
  else comicBubble(LX(0.46), LY(0.28), 840 * u, 130 * u, 'Gratis selamanya, atau sekali pakai!', 44 * u, hx - 20 * u, hy - 290 * u, 6.79);
  comicPanelFrame();
  comicFlash(M1);
  yearTag('Tier-list?');
  stripAt([[0.30, 'Mana yang tier S?'], [3.08, 'Enam nama, batas beda-beda'], [6.74, 'Sekali pakai, langsung habis']]);
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
  morningTail(12.33);
  // the dialogue, one bubble per line (same gating as the night scene)
  if (TT < 16.10) comicBubble(LX(0.42), LY(0.27), 720 * u, 130 * u, 'Elicit dan ChatGPT tier S!', 48 * u, LX(0.42), LY(0.27) + 55 * u, 12.33);
  else if (TT < 20.38) comicBubble(LX(0.42), LY(0.27), 720 * u, 130 * u, 'NotebookLM, SciSpace A!', 48 * u, LX(0.42), LY(0.27) + 55 * u, 16.10);
  else if (TT < 25.07) comicBubble(LX(0.42), LY(0.27), 720 * u, 130 * u, 'Gemini B, Gamma D!', 48 * u, LX(0.42), LY(0.27) + 55 * u, 20.38);
  else comicBubble(LX(0.42), LY(0.27), 720 * u, 130 * u, 'Cek kuota dulu!', 48 * u, LX(0.42), LY(0.27) + 55 * u, 25.07);
  // the tier list: one row per tier, popping in with the line that names it
  // (S with l4, A with l5, B and D with l6 — D halfway through l6, after
  // "Gamma tier D" is spoken)
  tierRow(LY(0.354), 'S', RED, '#ffffff', 'Elicit, ChatGPT', 'Cari jurnal + chat teks gratis', 12.33);
  tierRow(LY(0.445), 'A', INK, '#ffffff', 'NotebookLM, SciSpace', '50 sumber/notebook · 100 kredit/bln', 16.10);
  tierRow(LY(0.536), 'B', '#ffffff', INK, 'Gemini', 'Kuota refresh tiap 5 jam', 20.38);
  tierRow(LY(0.628), 'D', '#ffffff', RED, 'Gamma', '400 kredit, sekali saja', 22.5);
  comicPiko(LX(0.80), LY(0.60), 0.55, 'happy', M1);
  comicPanelFrame();
  comicFlash(M1);
  yearTag('peka.ai.id');
  stripAt([[12.28, 'Elicit dan ChatGPT tier S'], [16.05, 'NotebookLM, SciSpace A'], [20.33, 'Gemini B, Gamma D'], [25.02, 'Cek kuota dulu, Peka pilihkan']]);
}
