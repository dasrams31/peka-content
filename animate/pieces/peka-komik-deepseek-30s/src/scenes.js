// =====================================================================
//  SCENES — Komik Peka #02 (30 detik), terminal variant of the
//  peka-komik style. Same F2 morph chain as the 8s version (cursor
//  circle -> DONE check circle at 14.0s), stretched to 30s: seven
//  voice lines, three in the night era, four in the morning era. The
//  story advances through the dialogue: the night bubble (bubble2,
//  two lines) swaps at every night line, the morning bubble swaps at
//  every morning line, and the caption strip carries one fact per line
//  (stripAt). The terminal window stages its reveals with the voice:
//  DONE + "1 file jadi" with l4, the benchmark line with l5. Panel
//  layouts are the 8s layouts verbatim (same coordinates, same
//  clearances, already verified).
//  Voice coupling (see voice/voice.json): night lines l1 0.30, l2 2.91,
//  l3 7.75; morph 14.0; morning lines l4 14.28, l5 18.09, l6 21.66,
//  l7 25.46. Bubbles pop at line start + 0.05s; strips switch at the
//  line start. If the script timing changes, update both.
//  Benchmark numbers always carry the "klaim vendor" label, on screen.
// =====================================================================
const CURSOR = () => [LX(0.80), LY(0.17), 40 * UNIT];
const DONE_CIRCLE = () => [LX(0.80), LY(0.17), 80 * UNIT];
const PIKO_Y = '#ffd60a';
const WIN = { x: 100, y: 700, w: 880, h: 450 };

// Piko IS the Peka logo mark (~/workspace/peka-logo/mascot-p.png) —
// same drawing as the kit's comicPiko, but the fill is locked to Peka
// yellow instead of COMIC.accent (terminal green here). NEVER a font P.
// Geometry measured off mascot-p.png, logo px, origin at the stem's
// top-left, body box 290 x 502: stem capsule x 0-130, y 0-502, r 65;
// bowl D, flat edge x 150, y -5..275, semicircle r 140 at (150,135),
// 20px gap to the stem; black notch half-disc r 40 at (150,135);
// eye solid circle (60,125) r 45; smile solid half-disc (60,245)
// r 33; antenna line x 57-73, y -80..0, ball (65,-115) r 28.
// No outline on any yellow shape. See the kit's comicPiko comment.
function piko(x, y, s, mood, hopT) {
  const u = UNIT;
  const bob = Math.sin(TT * TAU * 0.9) * 8 * u;
  y += bob;
  if (hopT != null) {
    const hp = (TT - hopT) / 0.5;
    if (hp > 0 && hp < 1) y -= 70 * u * Math.sin(Math.PI * hp);
  }
  SPARK_AT = toScreen(x, y);
  const size = 340 * s;
  const Hb = size * 0.729, k = Hb / 502, Wb = 290 * k;
  const bx = x - Wb / 2, by = y + size * 0.42 - Hb;
  const Y = PIKO_Y;
  // antenna (behind the body): yellow line + ball, no outline
  ctx.save();
  ctx.strokeStyle = Y; ctx.lineWidth = 16 * k; ctx.lineCap = 'round';
  ctx.beginPath(); ctx.moveTo(bx + 65 * k, by - 80 * k); ctx.lineTo(bx + 65 * k, by); ctx.stroke();
  ctx.restore();
  dot(bx + 65 * k, by - 115 * k, 28 * k, Y);
  // stem: capsule, no outline
  ctx.save();
  trace(rect(bx, by, 130 * k, 502 * k, 65 * k), true);
  ctx.fillStyle = Y; ctx.fill();
  ctx.restore();
  // bowl: D, flat left edge + semicircular right edge, no outline
  ctx.save();
  ctx.beginPath();
  ctx.moveTo(bx + 150 * k, by - 5 * k);
  ctx.arc(bx + 150 * k, by + 135 * k, 140 * k, -Math.PI / 2, Math.PI / 2, false);
  ctx.closePath();
  ctx.fillStyle = Y; ctx.fill();
  ctx.restore();
  // the bowl's black notch: right half-disc on its flat edge, at eye height
  ctx.save();
  ctx.beginPath();
  ctx.arc(bx + 150 * k, by + 135 * k, 40 * k, -Math.PI / 2, Math.PI / 2, false);
  ctx.closePath();
  ctx.fillStyle = INK; ctx.fill();
  ctx.restore();
  // the face, exactly as on the logo: solid round eye, solid half-disc smile
  dot(bx + 60 * k, by + 125 * k, 45 * k, INK);
  ctx.save();
  ctx.beginPath();
  ctx.arc(bx + 60 * k, by + 245 * k, 33 * k, 0, Math.PI, false);
  ctx.closePath();
  ctx.fillStyle = INK; ctx.fill();
  ctx.restore();
  if (mood === 'confused') {
    // sweat drop, right of the head (unchanged from the old drawing)
    cut(ellipsePts(x + size * 0.42, y - size * 0.34, 16 * s * u, 24 * s * u, 0, 14), '#4c6fb5', { key: 'pksweat', shadow: false, tear: 0 });
  }
}
// two-line speech bubble (comicBubble is single-line). Lines are centred
// independently. The tail is a narrow triangle from the bubble's bottom
// edge to Piko (not the kit's wide left-side tail: that diagonal crossed
// the terminal text).
function bubble2(cx, cy, w, h, l1, l2, size, tailX, tailY, t0) {
  const k = popS(t0); if (k <= 0.01) return;
  ctx.save(); ctx.translate(cx, cy); ctx.scale(k, k); ctx.translate(-cx, -cy);
  const x = cx - w / 2, y = cy - h / 2;
  cut([[cx - 35, y + h - 4], [tailX, tailY], [cx + 35, y + h - 4]], '#ffffff', { key: 'btail2', shadow: false, tear: 0, line: INK, lw: 7 * UNIT });
  cut(rect(x, y, w, h, 34), '#ffffff', { key: 'bub2', shadow: true, tear: 0, line: INK, lw: 7 * UNIT });
  handText(l1, cx - handW(l1, size, 700) / 2, cy - size * 0.42, size, INK, { weight: 700, key: 'btxt2a' });
  handText(l2, cx - handW(l2, size, 700) / 2, cy + size * 0.62, size, INK, { weight: 700, key: 'btxt2b' });
  ctx.restore();
}
// single-line speech bubble with the same narrow bottom tail.
function bubble(cx, cy, w, h, str, size, tailX, tailY, t0) {
  const k = popS(t0); if (k <= 0.01) return;
  ctx.save(); ctx.translate(cx, cy); ctx.scale(k, k); ctx.translate(-cx, -cy);
  const x = cx - w / 2, y = cy - h / 2;
  cut([[cx - 35, y + h - 4], [tailX, tailY], [cx + 35, y + h - 4]], '#ffffff', { key: 'btail1', shadow: false, tear: 0, line: INK, lw: 7 * UNIT });
  cut(rect(x, y, w, h, 34), '#ffffff', { key: 'bub1', shadow: true, tear: 0, line: INK, lw: 7 * UNIT });
  handText(str, cx - handW(str, size, 700) / 2, cy + size * 0.36, size, INK, { weight: 700, key: 'btxt1' });
  ctx.restore();
}
// fade a drawing in (alpha 0 -> 1 over d seconds from t0)
function fadeIn(t0, d, fn) {
  const a = ev(t0, d); if (a <= 0) return;
  ctx.save(); ctx.globalAlpha = a; fn(); ctx.restore();
}
// the terminal window chrome: dark body, title bar with three dots.
// fill differs per era (night darker, morning "screen on").
function termWindow(fill) {
  cut(rect(WIN.x, WIN.y, WIN.w, WIN.h, 18), fill, { key: 'termwin', shadow: true, tear: 0, line: INK, lw: 7 * UNIT });
  dot(WIN.x + 50, WIN.y + 36, 13, '#ff5f57');
  dot(WIN.x + 92, WIN.y + 36, 13, '#febc2e');
  dot(WIN.x + 134, WIN.y + 36, 13, '#28c840');
  ink([[WIN.x + 20, WIN.y + 72], [WIN.x + WIN.w - 20, WIN.y + 72]], { w: 4 * UNIT, color: INK, key: 'termdiv' });
}
// dim code lines inside the window (drawn before Piko, so he covers the middle)
function codeLines() {
  const c = comicHexA(COMIC.accent, 0.45);
  ink([[150, 940], [520, 940]], { w: 8 * UNIT, color: c, key: 'code1' });
  ink([[150, 1010], [680, 1010]], { w: 8 * UNIT, color: c, key: 'code2' });
  ink([[150, 1080], [430, 1080]], { w: 8 * UNIT, color: c, key: 'code3' });
}
// The caption strip follows the voice: one fact per line. pairs are
// [line-start-time, text]; the latest one at or before TT wins.
function stripAt(pairs) {
  let cur = pairs[0][1];
  for (const [t0, str] of pairs) if (TT >= t0) cur = str;
  capStrip(cur);
}
function sceneNight() {
  const u = UNIT, [mx, my, mr] = CURSOR();
  comicGround('night');
  comicHalftone(LX(0.62), LY(0.02), W, LY(0.3), 46 * u, 7 * u, 'rgba(61,220,132,0.28)');
  // the cursor circle: the morph source (bridges.js A)
  cut(ellipsePts(mx, my, mr, mr, 0, 30), COMIC.accent2, { key: 'cursor', line: INK, lw: 6 * u });
  comicMotif(LX(0.50), LY(0.09), 0.8, TIMELINE.cues.wake + 0.3);
  termWindow('#06130c');
  handText('>_ ngoding pakai apa?', 150, 850, 52, COMIC.accent, { weight: 800, key: 'prompt' });
  cut(rect(668, 812, 24, 44, 4), COMIC.accent, { key: 'curblock', shadow: false, tear: 0 });
  codeLines();
  comicThought(LX(0.81), LY(0.48), '?', TIMELINE.cues.wake + 0.45, 56);
  // a late thought in the 3.1s quiet gap before the morph (l3 ends 11.20, l4 starts 14.28).
  // r=90: the "MIT?" text is ~120px wide at the fixed 58px thought font, so it needs a
  // 180px circle — r=56 (as in the 8s "?" thought) clips the text at the circle's edge.
  comicThought(LX(0.14), LY(0.30), 'MIT?', 12.2, 90);
  const hx = LX(0.72), hy = LY(0.60);
  piko(hx, hy, 1.0, 'confused');
  // the dialogue, one bubble per line: only the current line's bubble is
  // drawn (a later bubble pops over the earlier one, so drawing all of
  // them would stack hidden strings under the visible one and the review
  // would flag them as overlapping text). The swap is a hard cut + pop.
  if (TT < 2.96) bubble2(LX(0.56), LY(0.27), 620 * u, 210 * u, 'Ngoding pakai DeepSeek,', 'bukan Claude?!', 54 * u, hx - 8 * u, hy - 202 * u, 0.35);
  else if (TT < 7.80) bubble2(LX(0.56), LY(0.27), 620 * u, 210 * u, 'Harness open-source,', 'lisensi MIT!', 54 * u, hx - 8 * u, hy - 202 * u, 2.96);
  else bubble2(LX(0.56), LY(0.27), 620 * u, 210 * u, 'Satu perintah saja,', 'Web UI kebuka!', 54 * u, hx - 8 * u, hy - 202 * u, 7.80);
  comicPanelFrame();
  comicFlash(M1);
  yearTag('dsh');
  stripAt([[0.30, 'Ngoding pakai DeepSeek, bukan Claude?'], [2.91, 'Harness agen open-source, MIT'], [7.75, 'Satu perintah, Web UI kebuka']]);
}
function sceneMorning() {
  const u = UNIT, [sx, sy, sr] = DONE_CIRCLE();
  comicGround('day');
  comicHalftone(0, LY(0.68), LX(0.4), H, 46 * u, 7 * u, 'rgba(13,31,20,0.30)');
  // the DONE check circle: the morph target (bridges.js B), terminal-green rays
  cut(ellipsePts(sx, sy, sr, sr, 0, 36), COMIC.accent, { key: 'sun', line: INK, lw: 6 * u });
  ink([[sx - 34 * u, sy + 2 * u], [sx - 8 * u, sy + 28 * u], [sx + 38 * u, sy - 30 * u]], { w: 12 * u, color: INK, key: 'suncheck' });
  for (let i = 0; i < 10; i++) {
    const a = (i / 10) * TAU;
    ink([[sx + Math.cos(a) * (sr + 20 * u), sy + Math.sin(a) * (sr + 20 * u)], [sx + Math.cos(a) * (sr + 90 * u), sy + Math.sin(a) * (sr + 90 * u)]], { w: 9 * u, color: comicHexA(COMIC.accent, 0.85), key: 'ray' + i });
  }
  comicMotif(LX(0.50), LY(0.09), 0.8, M1 + 0.3);
  termWindow('#0a1f14');
  // the terminal stages its reveals with the voice: DONE + "1 file jadi" with l4, the benchmark with l5
  fadeIn(M1 + 0.45, 0.3, () => {
    cut(ellipsePts(186, 812, 32, 32, 0, 24), COMIC.accent, { key: 'doneck', shadow: false, tear: 0, line: INK, lw: 6 * u });
    ink([[172, 812], [182, 824], [202, 796]], { w: 9 * u, color: INK, key: 'doneckm' });
    handText('DONE', 236, 834, 72, COMIC.accent, { weight: 800, key: 'donetxt' });
  });
  fadeIn(M1 + 0.7, 0.3, () => {
    handText('1 file jadi', 150, 940, 48, '#c9f5d8', { weight: 700, key: 'onefile' });
  });
  fadeIn(18.2, 0.3, () => {
    const p1 = 'Terminal-Bench 2.1: 90,6';
    handText(p1, 150, 1042, 40, COMIC.accent, { weight: 800, key: 'bench' });
    handText('- klaim vendor', 150 + handW(p1, 40, 800) + 14, 1042, 40, 'rgba(255,255,255,0.75)', { weight: 700, key: 'benchv' });
  });
  const hx = LX(0.72), hy = LY(0.60);
  piko(hx, hy, 1.0, 'happy', M1);
  // the dialogue, one bubble per line (same gating as the night scene:
  // only the current line's bubble is drawn, so the review never sees
  // two bubbles stacked in the same box).
  if (TT < 18.14) bubble(LX(0.40), LY(0.29), 720 * u, 150 * u, 'Open-weight dan murah!', 54 * u, hx - 8 * u, hy - 202 * u, 14.33);
  else if (TT < 21.71) bubble(LX(0.40), LY(0.29), 720 * u, 150 * u, 'Klaim vendor, 90,6!', 54 * u, hx - 8 * u, hy - 202 * u, 18.14);
  else if (TT < 25.51) bubble(LX(0.40), LY(0.29), 720 * u, 150 * u, 'Kimi juga open-weight!', 54 * u, hx - 8 * u, hy - 202 * u, 21.71);
  else bubble(LX(0.40), LY(0.29), 720 * u, 150 * u, 'Coba sendiri dulu!', 54 * u, hx - 8 * u, hy - 202 * u, 25.51);
  comicPanelFrame();
  comicFlash(M1);
  yearTag('peka.ai.id');
  stripAt([[14.28, 'Open-weight dan murah'], [18.09, 'Bench 90,6 - klaim vendor'], [21.66, 'Kimi K3.1 Pro, 1 juta token'], [25.46, 'Coba dulu: npx @deepseek-ai/dsh web']]);
}
