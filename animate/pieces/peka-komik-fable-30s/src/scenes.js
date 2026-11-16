// =====================================================================
//  SCENES — Komik Peka #01 (30 detik): Claude Fable 5.2 (dark navy +
//  gold comic, trophy motif). Same F2 morph chain as the 8s version
//  (gold moon -> sun at 14.0s), stretched to 30s: seven voice lines,
//  three in the night era, four in the morning era. The story advances
//  through the dialogue: the night bubble and the caption strip swap
//  text at every line start, the morning bubble does the same; the
//  panel layouts themselves are the 8s layouts, already verified
//  (same coordinates, same clearances).
//  Voice coupling (see voice/voice.json): night lines l1 0.30, l2 3.18,
//  l3 8.16; morph 14.0; morning lines l4 14.28, l5 18.34, l6 22.50,
//  l7 26.67. Bubbles pop at line start + 0.05s; strips switch at the
//  line start. If the script timing changes, update both.
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
  // the price cut, on a cream paper tag above the speech bubble (pops at l2)
  tag('$10/$50 jadi $8/$40', CX, LY(0.245), 50, { rot: -0.02, s: popS(3.53) });
  // floating "?" bubbles: too cheap to be number one?
  const qs = [[0.62, 0.14, '?', 50], [0.82, 0.24, '?', 50], [0.12, 0.48, 'AI?'], [0.80, 0.50, '?'], [0.14, 0.66, 'AI?'], [0.80, 0.68, '?', 50]];
  qs.forEach(([fx, fy, str, r], i) => comicThought(LX(fx), LY(fy), str, TIMELINE.cues.wake + i * 0.15, r));
  // action lines around the confused hero: grow in one by one from the wake
  const hx = LX(0.46), hy = LY(0.58);
  comicActionLines(hx, hy, TIMELINE.cues.wake);
  comicPiko(hx, hy, 1.05, 'confused');
  // the dialogue, one bubble per line: only the current line's bubble is
  // drawn (a later bubble pops over the earlier one, so drawing all of
  // them would stack hidden strings under the visible one and the review
  // would flag them as overlapping text). The swap is a hard cut + pop:
  // the comic "new bubble" effect.
  if (TT < 3.23) comicBubble(LX(0.44), LY(0.32), 800 * u, 150 * u, 'Model termurah, kok nomor satu?!', 46 * u, hx - 60 * u, hy - 190 * u, 0.35);
  else if (TT < 8.21) comicBubble(LX(0.44), LY(0.32), 800 * u, 150 * u, 'Baru rilis, harga turun 20%!', 46 * u, hx - 60 * u, hy - 190 * u, 3.23);
  else comicBubble(LX(0.44), LY(0.32), 800 * u, 150 * u, 'Delapan dolar per juta token!', 46 * u, hx - 60 * u, hy - 190 * u, 8.21);
  comicPanelFrame();
  comicFlash(M1);
  yearTag('Fable 5.2');
  stripAt([[0.30, 'Termurah, kok nomor satu?!'], [3.18, 'Rilis 9 November 2026'], [8.16, 'Konteks 1 juta token']]);
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
  // the dialogue, one bubble per line (same gating as the night scene:
  // only the current line's bubble is drawn, so the review never sees
  // two bubbles stacked in the same box).
  if (TT < 18.39) comicBubble(LX(0.40), LY(0.28), 560 * u, 130 * u, 'Skor 65, nomor satu!', 50 * u, LX(0.46) + 30 * u, LY(0.62) - 160 * u, 14.33);
  else if (TT < 22.55) comicBubble(LX(0.40), LY(0.28), 560 * u, 130 * u, 'Unggul 5 poin!', 46 * u, LX(0.46) + 30 * u, LY(0.62) - 160 * u, 18.39);
  else if (TT < 26.72) comicBubble(LX(0.40), LY(0.28), 560 * u, 130 * u, 'Konteks 1 juta token!', 46 * u, LX(0.46) + 30 * u, LY(0.62) - 160 * u, 22.55);
  else comicBubble(LX(0.40), LY(0.28), 560 * u, 130 * u, 'Buka Claude, cobain!', 46 * u, LX(0.46) + 30 * u, LY(0.62) - 160 * u, 26.72);
  comicPanelFrame();
  comicFlash(M1);
  yearTag('peka.ai.id');
  stripAt([[14.28, 'Skor 65, nomor satu'], [18.34, 'Gemini Carbon: 60'], [22.50, '1 juta token konteks'], [26.67, 'Buka Claude, pilih Fable 5.2']]);
}
