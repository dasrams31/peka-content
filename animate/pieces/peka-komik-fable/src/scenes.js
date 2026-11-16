// =====================================================================
//  SCENES — Komik Peka #01: Claude Fable 5.2 (dark navy + gold comic,
//  trophy motif). Same F2 morph chain as peka-komik (gold moon -> sun
//  at 4.0s), same cues and score. Scene 1: Piko confused by the price
//  cut ("$10/$50 jadi $8/$40") and the question "Model termurah, kok
//  nomor satu?!". Scene 2: Piko happy, trophy + giant gold "65" +
//  burst "NOMOR 1", one concrete try-step on the caption strip.
//  Voice coupling (see voice/script.json): night bubble pops 0.35s
//  (line 1 starts 0.30s), morning bubble pops 4.35s (line 2 starts
//  4.30s). If the script timing changes, update both.
//  Layout notes (1080x1920, safe top 240 / bottom 420 / right 140):
//  - bubble night: x 75-875, price tag above it (gap 33px), year tag
//    above that (gap 46px incl. tape); "?" thoughts kept clear of the
//    year tag, the price tag and the bubble tail.
//  - morning: bubble top-left (x 152-712, clear of the sun rays),
//    giant "65" right (x ~705-935, below the bubble, above the burst),
//    trophy left (x 103-285, clear of the bubble tail by 37px),
//    burst lower-right (75px from the frame edge, 44px above the tape),
//    Piko centre (bottom 1333, 71px above the tape).
// =====================================================================
const MOON = () => [LX(0.80), LY(WIDE ? 0.20 : 0.17), 40 * UNIT];
const SUN = () => [LX(0.80), LY(WIDE ? 0.20 : 0.17), 80 * UNIT];
const GOLD = '#e8b93c';

function sceneNight() {
  const u = UNIT, [mx, my, mr] = MOON();
  comicGround('night');
  comicHalftone(LX(0.62), LY(0.02), W, LY(0.3), 46 * u, 7 * u, 'rgba(255,255,255,0.35)');
  cut(ellipsePts(mx, my, mr, mr, 0, 30), COMIC.accent2, { key: 'moon', line: INK, lw: 6 * u });
  // the price cut, on a cream paper tag above the speech bubble
  tag('$10/$50 jadi $8/$40', CX, LY(0.245), 50, { rot: -0.02, s: popS(TIMELINE.cues.wake + 0.3) });
  // floating "?" bubbles: too cheap to be number one?
  const qs = [[0.62, 0.14, '?', 50], [0.82, 0.24, '?', 50], [0.12, 0.48, 'AI?'], [0.80, 0.50, '?'], [0.14, 0.66, 'AI?'], [0.80, 0.68, '?', 50]];
  qs.forEach(([fx, fy, str, r], i) => comicThought(LX(fx), LY(fy), str, TIMELINE.cues.wake + i * 0.15, r));
  // action lines around the confused hero: grow in one by one from the wake
  const hx = LX(0.46), hy = LY(0.58);
  comicActionLines(hx, hy, TIMELINE.cues.wake);
  comicPiko(hx, hy, 1.05, 'confused');
  comicBubble(LX(0.44), LY(0.32), 800 * u, 150 * u, 'Model termurah, kok nomor satu?!', 46 * u, hx - 60 * u, hy - 190 * u, 0.35);
  comicPanelFrame();
  comicFlash(M1);
  yearTag('Fable 5.2');
  capStrip('Termurah, kok nomor satu?!');
}
function sceneMorning() {
  const u = UNIT, [sx, sy, sr] = SUN();
  comicGround('day');
  comicHalftone(0, LY(0.68), LX(0.4), H, 46 * u, 7 * u, 'rgba(20,18,16,0.25)');
  cut(ellipsePts(sx, sy, sr, sr, 0, 36), COMIC.accent, { key: 'sun', line: INK, lw: 6 * u });
  comicRays(sx, sy, sr, 10);
  // the trophy (episode motif, left) and the giant gold score (right)
  comicMotif(LX(0.18), LY(0.42), 1.3, M1 + 0.6);
  const big = '65', bigSize = 210 * u;
  handText(big, LX(0.76) - handW(big, bigSize, 800) / 2, LY(0.42), bigSize, GOLD, { weight: 800, key: 'big65' });
  comicPiko(LX(0.46), LY(0.62), 1.0, 'happy', M1);
  comicBurst(LX(0.75), LY(0.615), 180 * u, 'NOMOR 1', 44 * u, M1 + 0.6);
  comicBubble(LX(0.40), LY(0.28), 560 * u, 130 * u, 'Fable 5.2, cobain!', 50 * u, LX(0.46) + 30 * u, LY(0.62) - 160 * u, M1 + 0.35);
  comicPanelFrame();
  comicFlash(M1);
  yearTag('peka.ai.id');
  capStrip('Buka Claude, pilih Fable 5.2');
}
