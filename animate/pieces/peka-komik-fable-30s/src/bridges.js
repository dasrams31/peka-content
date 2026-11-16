
// =====================================================================
//  ERAS, CAMERAS, BRIDGES — read by kit/morph.js
//  ERA_BG: each era's dominant colour (the fade to blank paper during a morph).
//  pieceCam(era, t): null, push(t, a, b, { z, p, to }, pullA, pullB) or bump(t, t0, [x, y]).
//  BRIDGES: at tc the object A (end of the old era) morphs into B (start of the new one).
//    shape = { P: points, c: '#hex' } or SP(x, y, r, rays) for the spark hero itself.
//  Leave BRIDGES = [] for a beat-cut piece (every era boundary becomes a hard cut).
// =====================================================================
const ERA_BG = ['#0e1430', '#16204d'];
function pieceCam(era, t) { return null; }
const BRIDGES = [
  { tc: TIMELINE.morphs[0], A: () => { const [x, y, r] = MOON(); return { P: ellipsePts(x, y, r, r, 0, 64), c: '#e8b93c' }; }, B: () => { const [x, y, r] = SUN(); return { P: ellipsePts(x, y, r, r, 0, 64), c: '#ffd60a' }; } },   // the gold moon -> the yellow sun (shapes from src/scenes.js)
];
