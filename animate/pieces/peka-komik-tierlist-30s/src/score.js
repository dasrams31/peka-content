  // =====================================================================
  //  SCORE BODY — 30s version: same recipe as the 8s piece, stretched
  //  to the 12.0s morph. Night pad 0-12.1, morning pad 12.0-30.05; the
  //  hero's motif at the wake; one pluck per dialogue pop (l2/l3 in the
  //  night, l4-l7 in the morning); the tier-row arpeggio (4 plucks, one
  //  per row) from the morph (flowers 12.75); a paper swish into the
  //  morph at 11.7-12.05. The loudest moment is the morph at 12.0s, in
  //  the payoff act. The score sits at -60 dB under the voice in the
  //  delivered mix (piece.json "voice.music"), inaudible; it exists for
  //  the review's story-arc measurement. Pluck times couple to
  //  voice/voice.json line starts (+0.05s).
  // =====================================================================
  const T = TIMELINE, cu = T.cues;
  to = 'm';
  pad(0.0, 12.1, ['D3', 'A3', 'Fs4'], 0.035, { type: 'triangle', cut: 800, att: 0.05, rel: 0.2 });
  [['D4', 0], ['A4', E8]].forEach(([n, dt], i) => pluck(cu.wake + dt, nz(n), 0.2, 0.1 - i * 0.1, 0.6, 2600, 0.35));   // the hero's motif
  // one pluck per dialogue pop: l2 3.13, l3 6.79 (night); l4 12.33, l5 16.10, l6 20.38, l7 25.07 (morning).
  // Quieter than the morph arpeggio (0.08), so the morph stays the loudest moment.
  [[3.13, 'E5'], [6.79, 'Fs5'], [12.33, 'A5'], [16.10, 'B5'], [20.38, 'D6'], [25.07, 'E6']].forEach(([t, n], i) => pluck(t, nz(n), 0.06, 0.2 - i * 0.07, 0.5, 3200, 0.3));
  pad(12.0, 30.05, ['D3', 'A3', 'D4', 'Fs4'], 0.05, { cut: 1200, att: 0.3, rel: 0.3, send: 0.4 });
  for (let i = 0; i < 4; i++) pluck(cu.flowers + i * 0.25, nz(['D5', 'E5', 'Fs5', 'A5'][i]), 0.08, 0.3 - i * 0.12, 0.4, 4200, 0.3);   // one pluck per tier row
  to = 's';
  sweep(11.7, 12.05, 0.011, 500, 2600, 0);   // a paper swish into the morph
