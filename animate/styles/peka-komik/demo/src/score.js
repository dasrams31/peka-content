  // SCORE BODY — peka-komik demo (inside buildScore(); see kit/score-head.js)
  const T = TIMELINE, cu = T.cues;
  to = 'm';
  pad(0.0, 3.1, ['D3', 'A3', 'Fs4'], 0.035, { type: 'triangle', cut: 900, att: 0.05, rel: 0.2 });
  [['D4', 0], ['A4', E8]].forEach(([n, dt], i) => pluck(cu.wake + dt, nz(n), 0.2, 0.1 - i * 0.1, 0.6, 2600, 0.35));
  pad(3.0, 6.05, ['D2', 'A2', 'F3', 'C4'], 0.045, { cut: 700, att: 0.3, rel: 0.3, send: 0.4 });
  to = 's';
  sweep(2.7, 3.05, 0.011, 500, 2600, 0);
  for (let i = 0; i < 5; i++) pluck(cu.flowers + i * E8, nz(['C4', 'E4', 'G4', 'A4', 'C5'][i]), 0.2, 0.1, 0.6, 2600, 0.3);   // plucks per checkmark
  noiseHit(3.0, 0.25, 'lowpass', 800, 1, 0.5, 0);   // the morph hit
