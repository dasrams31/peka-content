
// =====================================================================
//  ERAS, CAMERAS, BRIDGES — peka-komik demo (read by kit/morph.js)
// =====================================================================
const ERA_BG = [COMIC.ground1, COMIC.accent];
function pieceCam(era, t) { return null; }
const BRIDGES = [
  { tc: TIMELINE.morphs[0], A: () => { const [x, y, r] = MOON(); return { P: ellipsePts(x, y, r, r, 0, 64), c: COMIC.accent2 }; }, B: () => { const [x, y, r] = SUN(); return { P: ellipsePts(x, y, r, r, 0, 64), c: COMIC.accent }; } },   // the moon -> the sun
];
