// =====================================================================
//  SCENES — Komik Peka #02, terminal variant of the peka-komik style.
//  Night: Piko confused in front of a terminal window ("prompt:
//  ngoding pakai apa?"); the cursor circle morphs into a DONE check
//  circle at 4.0s. Morning: the terminal shows DONE + one file done,
//  Piko happy. Piko stays Peka yellow #ffd60a (local piko(): the kit's
//  comicPiko fills from COMIC.accent, which is terminal green here).
//  Benchmark numbers always carry the "klaim vendor" label, on screen.
// =====================================================================
const CURSOR = () => [LX(0.80), LY(0.17), 40 * UNIT];
const DONE_CIRCLE = () => [LX(0.80), LY(0.17), 80 * UNIT];
const PIKO_Y = '#ffd60a';
const WIN = { x: 100, y: 700, w: 880, h: 450 };

// Piko as a vector, yellow P (same drawing as the kit's comicPiko, but
// the fill is locked to Peka yellow instead of COMIC.accent).
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
  ink([[x - size * 0.06, y - size * 0.46], [x - size * 0.06, y - size * 0.78]], { w: 10 * u, color: INK, key: 'pkant' });
  dot(x - size * 0.06, y - size * 0.84, 22 * s * u, PIKO_Y);
  ctx.save();
  ctx.strokeStyle = INK; ctx.lineWidth = 14 * u;
  ctx.beginPath(); ctx.arc(x - size * 0.06, y - size * 0.84, 22 * s * u, 0, TAU); ctx.stroke();
  ctx.restore();
  ctx.save();
  ctx.font = `800 ${size}px "Arial Black", Arial, sans-serif`;
  ctx.textBaseline = 'alphabetic'; ctx.textAlign = 'center';
  ctx.lineJoin = 'round';
  ctx.strokeStyle = INK; ctx.lineWidth = 16 * u;
  ctx.strokeText('P', x, y + size * 0.42);
  ctx.fillStyle = PIKO_Y;
  ctx.fillText('P', x, y + size * 0.42);
  ctx.restore();
  const ex = x - size * 0.22, ey = y - size * 0.10;
  if (mood === 'happy' || mood === 'wow') {
    ink(arcPts(ex, ey, 26 * s * u, Math.PI * 1.15, Math.PI * 1.85, 10), { w: 8 * u, color: INK, key: 'pkeye' });
  } else {
    dot(ex, ey, 30 * s * u, INK);
    dot(ex + 10 * s * u, ey - 10 * s * u, 9 * s * u, '#ffffff');
    cut(ellipsePts(x + size * 0.42, y - size * 0.34, 16 * s * u, 24 * s * u, 0, 14), '#4c6fb5', { key: 'pksweat', shadow: false, tear: 0 });
  }
  ink(arcPts(x - size * 0.20, y + size * 0.10, 26 * s * u, Math.PI * 0.15, Math.PI * 0.85, 10), { w: 8 * u, color: INK, key: 'pksmile' });
}
// two-line speech bubble (comicBubble is single-line). Lines are centred
// independently; the tail points at Piko. t0 couples to the voice-over:
// 0.35s (line 1 starts 0.30s) — see voice/script.json.
function bubble2(cx, cy, w, h, l1, l2, size, tailX, tailY, t0) {
  const k = popS(t0); if (k <= 0.01) return;
  ctx.save(); ctx.translate(cx, cy); ctx.scale(k, k); ctx.translate(-cx, -cy);
  const x = cx - w / 2, y = cy - h / 2;
  cut([[x, y + 26], [tailX, tailY], [x + 90, y + h]], '#ffffff', { key: 'btail2', shadow: false, tear: 0, line: INK, lw: 7 * UNIT });
  cut(rect(x, y, w, h, 34), '#ffffff', { key: 'bub2', shadow: true, tear: 0, line: INK, lw: 7 * UNIT });
  handText(l1, cx - handW(l1, size, 700) / 2, cy - size * 0.42, size, INK, { weight: 700, key: 'btxt2a' });
  handText(l2, cx - handW(l2, size, 700) / 2, cy + size * 0.62, size, INK, { weight: 700, key: 'btxt2b' });
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
  comicThought(LX(0.80), LY(0.44), '?', TIMELINE.cues.wake + 0.45);
  const hx = LX(0.46), hy = LY(0.60);
  piko(hx, hy, 1.0, 'confused');
  bubble2(LX(0.42), LY(0.27), 700 * u, 210 * u, 'Ngoding pakai DeepSeek,', 'bukan Claude?!', 56 * u, hx - 40 * u, hy - 250 * u, 0.35);
  comicPanelFrame();
  comicFlash(M1);
  yearTag('dsh?');
  capStrip('Ngoding pakai DeepSeek, bukan Claude?');
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
  fadeIn(M1 + 0.45, 0.3, () => {
    cut(ellipsePts(186, 812, 32, 32, 0, 24), COMIC.accent, { key: 'doneck', shadow: false, tear: 0, line: INK, lw: 6 * u });
    ink([[172, 812], [182, 824], [202, 796]], { w: 9 * u, color: INK, key: 'doneckm' });
    handText('DONE', 236, 834, 72, COMIC.accent, { weight: 800, key: 'donetxt' });
  });
  fadeIn(M1 + 0.7, 0.3, () => {
    handText('1 file jadi', 150, 940, 48, '#c9f5d8', { weight: 700, key: 'onefile' });
  });
  fadeIn(M1 + 0.95, 0.3, () => {
    const p1 = 'Terminal-Bench 2.1: 90,6';
    handText(p1, 150, 1042, 40, COMIC.accent, { weight: 800, key: 'bench' });
    handText('- klaim vendor', 150 + handW(p1, 40, 800) + 14, 1042, 40, 'rgba(255,255,255,0.75)', { weight: 700, key: 'benchv' });
  });
  const hx = LX(0.46), hy = LY(0.60);
  piko(hx, hy, 1.0, 'happy', M1);
  comicBubble(LX(0.40), LY(0.29), 720 * u, 150 * u, 'Coba satu tugas kecil dulu!', 54 * u, hx - 40 * u, hy - 250 * u, 4.35);
  comicPanelFrame();
  comicFlash(M1);
  yearTag('peka.ai.id');
  capStrip('Coba dulu: npx @deepseek-ai/dsh web');
}
