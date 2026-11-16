# LOG: Komik Peka #02 — Ngoding pakai DeepSeek, bukan Claude? (terminal, 30 detik)

- 2026-11-16: 30s rebuild of the 8s episode (user rejected 8s as too
  short, 09:41; chose 30s over 60s, 10:14). Same approved `peka-komik`
  look, same terminal-green variant, same panel layouts (verified in
  the 8s version). New: 7 voice lines (59 words), morph moved to 14.0s,
  dialogue advances through bubble swaps + caption-strip swaps
  (`stripAt`), the terminal stages DONE/"1 file jadi" with l4 and the
  benchmark line with l5, one pluck per dialogue pop, a late "MIT?"
  thought at 12.2s in the 3.1s quiet gap before the morph (l3 ends
  11.20, l4 starts 14.28). Facts unchanged from the 8s brief
  (web-checked 16 Nov 2026); no "DeepSeek menang" verdict anywhere.
- 2026-11-16: Voice-over: Edge TTS id-ID-ArdiNeural. l1-l6 at +0%, l7
  at +15% (its +0% take ran 4.42s and would have pushed the voice
  past 30s). Timing: l1 0.30-2.31, l2 2.91-7.15, l3 7.75-11.20,
  l4 14.28-17.69, l5 18.09-21.25, l6 21.66-25.16, l7 25.46-29.31;
  total voice 29.81s inside the 30.0s piece.
- 2026-11-16: Still check caught a real defect the review could not:
  the "MIT?" thought (12.2s) was drawn with r=56, but the fixed 58px
  thought font makes "MIT?" ~120px wide, so the text spilled past the
  112px circle. Fixed to r=90 (180px circle, clear of the bubble,
  year tag and terminal window); re-exported. Lesson: multi-character
  thoughts need r >= text width / 2; the review only checks frame-edge
  cut-off and text-text overlap, not text overflowing its own bubble.
- 2026-11-16: Mascot fix re-render (user: maskot harus sama dengan logo Peka): local piko() redrawn as the real logo mark (same geometry as the kit's comicPiko, yellow locked to PIKO_Y #ffd60a). Same 30.016s, same voice/script/facts. Review PASS: text 0 cut-off/overlap, narration 59w density PASS, story arc 2/2, dead beats PASS, -13.9 LUFS, true peak -1.7 dBFS. Mascot checks verified from the mp4 (incl. frame 300: "MIT?" thought still clean inside its circle): P = logo, eye solid on stem, antenna yellow/centred/visible, tail anchor clear of the ball.
