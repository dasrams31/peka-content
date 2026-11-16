// =====================================================================
//  ERAS, CAMERAS, BRIDGES — read by kit/morph.js
//  The cursor circle (night) morphs into the DONE check circle (day).
// =====================================================================
const ERA_BG = [COMIC.ground1, COMIC.ground2];
function pieceCam(era, t) { return null; }
const BRIDGES = [
  { tc: TIMELINE.morphs[0], A: () => { const [x, y, r] = CURSOR(); return { P: ellipsePts(x, y, r, r, 0, 64), c: COMIC.accent2 }; }, B: () => { const [x, y, r] = DONE_CIRCLE(); return { P: ellipsePts(x, y, r, r, 0, 64), c: COMIC.accent }; } },   // cursor -> DONE check circle
];
