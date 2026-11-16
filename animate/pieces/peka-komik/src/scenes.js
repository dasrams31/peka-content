// =====================================================================
//  SCENES — comic style, Peka palette, Piko as a vector hero.
//  Same story as peka-contoh ("Bingung pilih AI?"), same 2 eras joined by
//  the moon -> sun morph, same cues and score. Comic treatment: thick
//  black panel frame, halftone dots, action lines, speech bubbles,
//  onomatopoeia bursts. Piko = yellow letter P, one black eye, small
//  smile, antenna with a ball (redrawn from piko-idle.png, not pasted).
// =====================================================================
const MOON = () => [LX(0.72), LY(WIDE ? 0.26 : 0.22), 40 * UNIT];
const SUN = () => [LX(0.72), LY(WIDE ? 0.26 : 0.22), 80 * UNIT];
const INK = '#141210';
const PEKA_Y = '#ffd60a';
const PEKA_CREAM = '#f5f1e8';

// thick black comic panel frame, drawn over the whole scene
function panelFrame() {
  ctx.save();
  ctx.strokeStyle = INK; ctx.lineWidth = 16 * UNIT; ctx.lineJoin = 'round';
  ctx.strokeRect(14 * UNIT, 14 * UNIT, W - 28 * UNIT, H - 28 * UNIT);
  ctx.restore();
}
// halftone corner: rows of dots, denser toward the corner
function halftone(x0, y0, x1, y1, gap, maxR, color) {
  ctx.save(); ctx.fillStyle = color;
  let row = 0;
  for (let y = y0; y < y1; y += gap, row++) {
    for (let x = x0 + (row % 2) * gap / 2; x < x1; x += gap) {
      const d = Math.hypot(x - x0, y - y0) / Math.hypot(x1 - x0, y1 - y0);
      const r = maxR * (1 - d * 0.7);
      ctx.beginPath(); ctx.arc(x, y, Math.max(r, 0.6), 0, TAU); ctx.fill();
    }
  }
  ctx.restore();
}
// speech bubble: white rounded box + tail triangle + hand text
function bubble(cx, cy, w, h, str, size, tailX, tailY) {
  const x = cx - w / 2, y = cy - h / 2;
  cut([[x, y + 26], [tailX, tailY], [x + 90, y + h]], '#ffffff', { key: 'btail' + str, shadow: false, tear: 0, line: INK, lw: 7 * UNIT });
  cut(rect(x, y, w, h, 34), '#ffffff', { key: 'bub' + str, shadow: true, tear: 0, line: INK, lw: 7 * UNIT });
  handText(str, cx - handW(str, size, 700) / 2, cy + size * 0.36, size, INK, { weight: 700, key: 'btxt' + str });
}
// starburst shout (onomatopoeia), e.g. "BANYAK"
function burst(cx, cy, r, str, size) {
  const n = 12, pts = [];
  for (let i = 0; i < n * 2; i++) {
    const a = (i / (n * 2)) * TAU - Math.PI / 2, rr = i % 2 === 0 ? r : r * 0.62;
    pts.push([cx + Math.cos(a) * rr, cy + Math.sin(a) * rr]);
  }
  cut(pts, PEKA_Y, { key: 'burst' + str, shadow: true, tear: 0, line: INK, lw: 6 * UNIT });
  handText(str, cx - handW(str, size, 800) / 2, cy + size * 0.36, size, INK, { weight: 800, key: 'bt' + str });
}
// Piko, drawn as a vector: yellow P (strokeText + fillText), one black
// eye on the stem, small smile, antenna with a ball on top.
// mood: 'confused' (eye wide + sweat drop) or 'happy' (eye arc, smile)
function piko(x, y, s, mood) {
  const u = UNIT;
  const bob = Math.sin(TT * TAU * 0.9) * 8 * u;
  y += bob;
  const size = 340 * s;
  // antenna: thin line + ball, from the top of the stem
  ink([[x - size * 0.06, y - size * 0.46], [x - size * 0.06, y - size * 0.78]], { w: 10 * u, color: INK, key: 'pkant' });
  dot(x - size * 0.06, y - size * 0.84, 22 * s * u, PEKA_Y);
  ctx.save();
  ctx.strokeStyle = INK; ctx.lineWidth = 14 * u;
  ctx.beginPath(); ctx.arc(x - size * 0.06, y - size * 0.84, 22 * s * u, 0, TAU); ctx.stroke();
  ctx.restore();
  // the letter P itself
  ctx.save();
  ctx.font = `800 ${size}px "Arial Black", Arial, sans-serif`;
  ctx.textBaseline = 'alphabetic'; ctx.textAlign = 'center';
  ctx.lineJoin = 'round';
  ctx.strokeStyle = INK; ctx.lineWidth = 16 * u;
  ctx.strokeText('P', x, y + size * 0.42);
  ctx.fillStyle = PEKA_Y;
  ctx.fillText('P', x, y + size * 0.42);
  ctx.restore();
  // one eye on the stem (left bar of the P), smile below it
  const ex = x - size * 0.22, ey = y - size * 0.10;
  if (mood === 'happy') {
    ink(arcPts(ex, ey, 26 * s * u, Math.PI * 1.15, Math.PI * 1.85, 10), { w: 8 * u, color: INK, key: 'pkeye' });
  } else {
    dot(ex, ey, 30 * s * u, INK);
    dot(ex + 10 * s * u, ey - 10 * s * u, 9 * s * u, '#ffffff');
    // sweat drop, right of the head
    cut(ellipsePts(x + size * 0.42, y - size * 0.34, 16 * s * u, 24 * s * u, 0, 14), '#4c6fb5', { key: 'pksweat', shadow: false, tear: 0 });
  }
  ink(arcPts(x - size * 0.20, y + size * 0.10, 26 * s * u, Math.PI * 0.15, Math.PI * 0.85, 10), { w: 8 * u, color: INK, key: 'pksmile' });
}
function sceneNight() {
  const u = UNIT, [mx, my, mr] = MOON();
  cut(rect(-30, -30, W + 60, H + 60, 0), PAL.night, { key: 'wallN', shadow: false, tear: 0, shade: false, pat: pat.dots('rgba(255,214,10,0.16)', 5, 64) });
  halftone(LX(0.62), LY(0.02), W, LY(0.3), 46 * u, 7 * u, 'rgba(255,255,255,0.35)');
  cut(ellipsePts(mx, my, mr, mr, 0, 30), '#f6ecc8', { key: 'moon', line: INK, lw: 6 * u });
  // floating "?" bubbles: too many AI choices
  const qs = [[0.16, 0.24, 'AI?'], [0.56, 0.17, '?'], [0.80, 0.44, 'AI?'], [0.10, 0.46, '?']];
  qs.forEach(([fx, fy, str], i) => {
    const k = popS(TIMELINE.cues.wake + i * 0.15); if (k <= 0) return;
    const bx = LX(fx), by = LY(fy);
    ctx.save(); ctx.translate(bx, by); ctx.scale(k, k);
    cut(ellipsePts(0, 0, 62 * u, 62 * u, 0, 24), '#ffffff', { key: 'q' + i, shadow: true, tear: 0, line: INK, lw: 6 * u });
    handText(str, -handW(str, 58 * u, 800) / 2, 20 * u, 58 * u, INK, { weight: 800, key: 'qt' + i });
    ctx.restore();
  });
  // action lines around the confused hero
  const hx = LX(0.46), hy = LY(0.52);
  for (let i = 0; i < 8; i++) {
    const a = -Math.PI / 2 + (i - 3.5) * 0.22;
    ink([[hx + Math.cos(a) * 260 * u, hy + Math.sin(a) * 260 * u], [hx + Math.cos(a) * 330 * u, hy + Math.sin(a) * 330 * u]], { w: 7 * u, color: 'rgba(255,255,255,0.75)', key: 'act' + i });
  }
  piko(hx, hy, 1.05, 'confused');
  burst(LX(0.76), LY(0.66), 195 * u, 'BANYAK', 50 * u);
  bubble(LX(0.42), LY(0.30), 620 * u, 150 * u, 'Bingung pilih AI?!', 62 * u, hx - 60 * u, hy - 190 * u);
  panelFrame();
  yearTag('Bingung?');
  capStrip('Bingung pilih AI?');
}
function sceneMorning() {
  const u = UNIT, [sx, sy, sr] = SUN();
  cut(rect(-30, -30, W + 60, H + 60, 0), PEKA_CREAM, { key: 'wallM', shadow: false, tear: 0, shade: false, pat: pat.dots('rgba(20,18,16,0.10)', 5, 64) });
  halftone(0, LY(0.68), LX(0.4), H, 46 * u, 7 * u, 'rgba(20,18,16,0.25)');
  cut(ellipsePts(sx, sy, sr, sr, 0, 36), PEKA_Y, { key: 'sun', line: INK, lw: 6 * u });
  // sun rays, thick comic lines
  for (let i = 0; i < 10; i++) {
    const a = (i / 10) * TAU;
    ink([[sx + Math.cos(a) * (sr + 20 * u), sy + Math.sin(a) * (sr + 20 * u)], [sx + Math.cos(a) * (sr + 90 * u), sy + Math.sin(a) * (sr + 90 * u)]], { w: 9 * u, color: INK, key: 'ray' + i });
  }
  // checkmarks pop in one by one, spread across the frame
  const gy = LY(0.62);
  for (let i = 0; i < 5; i++) {
    const t0 = TIMELINE.cues.flowers + i * 0.25, k = popS(t0); if (k <= 0) continue;
    const x = LX([0.10, 0.26, 0.62, 0.78, 0.90][i]), y = gy + 90 * u + (i % 2) * 50 * u;
    ctx.save(); ctx.translate(x, y); ctx.scale(k, k);
    cut(ellipsePts(0, 0, 58 * u, 58 * u, 0, 24), '#ffffff', { key: 'ck' + i, shadow: true, tear: 0, line: INK, lw: 6 * u });
    ink([[-28 * u, 0], [-6 * u, 24 * u], [30 * u, -26 * u]], { w: 10 * u, color: '#3d7c46', key: 'ckm' + i });
    ctx.restore();
  }
  piko(LX(0.46), gy - 160 * u, 1.15, 'happy');
  bubble(LX(0.44), LY(0.28), 680 * u, 150 * u, 'Peka pilihkan!', 62 * u, LX(0.46) - 40 * u, gy - 330 * u);
  panelFrame();
  yearTag('peka.ai.id');
  capStrip('Peka pilihkan yang cocok.');
}
