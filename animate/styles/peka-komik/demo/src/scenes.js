// =====================================================================
//  SCENES — peka-komik demo. Same story as pieces/peka-komik, drawn
//  with the style's own kit: comicGround, comicHalftone, comicThought,
//  comicActionLines, comicPiko, comicBurst, comicBubble, comicPanelFrame,
//  comicFlash, comicRays, comicCheck, comicMotif.
// =====================================================================
const MOON = () => [LX(0.80), LY(WIDE ? 0.20 : 0.17), 40 * UNIT];
const SUN = () => [LX(0.80), LY(WIDE ? 0.20 : 0.17), 80 * UNIT];
function sceneNight() {
  const u = UNIT, [mx, my, mr] = MOON();
  comicGround('night');
  comicHalftone(LX(0.62), LY(0.02), W, LY(0.3), 46 * u, 7 * u, 'rgba(255,255,255,0.35)');
  cut(ellipsePts(mx, my, mr, mr, 0, 30), COMIC.accent2, { key: 'moon', line: INK, lw: 6 * u });
  // floating "?" bubbles: too many AI choices
  const qs = [[0.16, 0.24, 'AI?'], [0.56, 0.17, '?'], [0.79, 0.44, 'AI?'], [0.12, 0.46, '?']];
  qs.forEach(([fx, fy, str], i) => comicThought(LX(fx), LY(fy), str, TIMELINE.cues.wake + i * 0.15));
  // the episode motif emblem (default: a small accent star), top centre
  comicMotif(LX(0.50), LY(0.09), 1, TIMELINE.cues.wake + 0.3);
  // action lines around the confused hero: grow in one by one from the wake
  const hx = LX(0.46), hy = LY(0.52);
  comicActionLines(hx, hy, TIMELINE.cues.wake);
  comicPiko(hx, hy, 1.05, 'confused');
  comicBurst(LX(0.76), LY(0.62), 180 * u, 'BANYAK', 50 * u, TIMELINE.cues.wake + 0.6);
  comicBubble(LX(0.42), LY(0.30), 620 * u, 150 * u, 'Bingung pilih AI?!', 62 * u, hx - 60 * u, hy - 190 * u, 0.35);
  comicPanelFrame();
  comicFlash(M1);
  yearTag('Bingung?');
  capStrip('Bingung pilih AI?');
}
function sceneMorning() {
  const u = UNIT, [sx, sy, sr] = SUN();
  comicGround('day');
  comicHalftone(0, LY(0.68), LX(0.4), H, 46 * u, 7 * u, 'rgba(20,18,16,0.25)');
  cut(ellipsePts(sx, sy, sr, sr, 0, 36), COMIC.accent, { key: 'sun', line: INK, lw: 6 * u });
  comicRays(sx, sy, sr, 10);
  // checkmarks pop in one by one, spread across the frame. Row sits
  // 76px clear of the caption tape (proven in pieces/peka-komik rev 2).
  const gy = LY(0.62);
  for (let i = 0; i < 5; i++) {
    const x = LX([0.12, 0.27, 0.64, 0.78, 0.88][i]), y = gy + 40 * u + (i % 2) * 40 * u;
    comicCheck(x, y, TIMELINE.cues.flowers + i * 0.25);
  }
  comicPiko(LX(0.46), gy - 160 * u, 1.15, 'happy', M1);
  comicBubble(LX(0.44), LY(0.28), 680 * u, 150 * u, 'Peka pilihkan!', 62 * u, LX(0.46) - 40 * u, gy - 330 * u, M1 + 0.35);
  comicPanelFrame();
  comicFlash(M1);
  yearTag('peka.ai.id');
  capStrip('Peka pilihkan yang cocok.');
}
