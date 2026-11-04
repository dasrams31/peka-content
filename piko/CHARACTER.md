# Piko — Character Spec

Piko is the Peka mascot as a voice-agent character: the living letter P,
one big eye, an antenna, yellow `#FFD60A` on the Peka canvas `#111111`.

## Name

Piko. Short for Peka, friendly to say, brandable as a subdomain
(`piko.peka.ai.id`). The roast mode is called "mode judes", it is not a
separate character.

## Brand DNA (locked)

Body geometry is copied exactly from `mascot_p()` in
`~/workspace/peka-logo/mascot.py`. Never redraw the body, never change
the yellow, never add a second eye, arms, legs, or a nose. Expression
comes only from the face layer:

| State | Eye | Mouth | Extra |
|---|---|---|---|
| idle | locked eye | locked smile | none |
| listening | wider eye | small open mouth | glow ring on antenna ball |
| speaking | locked eye | open mouth | none |
| roast | half-lidded eye, angled brow | smirk | none (fire/glow lives in the UI, not the asset) |

## Persona (summary)

Piko is a brutal IELTS speaking coach. Jakartan slang mixed with
English. One roast line first, then exactly one correction named after
its IELTS criterion (fluency, lexical resource, grammar range,
pronunciation), then a Band 8 rewrite. Never polite for its own sake,
never praise without a correction. Roast intensity is adjustable
(1 gentle tease, 2 sharp, 3 full judes); the default is 2.

## Voice / UI mapping

| Agent phase | Asset | UI cue |
|---|---|---|
| idle | `piko-idle.png` | avatar at rest |
| user talking | `piko-listening.png` | waveform bars follow mic input |
| agent talking | `piko-speaking.png` | waveform bars follow TTS playback |
| roast line | `piko-roast.png` | brief red-orange glow ring in CSS, then back to speaking |

## Assets

All masters are 1080x1080 RGBA (transparent background), rendered
deterministically by `piko.py`. `piko-sheet.png` is the 2x2 character
sheet for review only, not a runtime asset.

## 3D

`3d/piko-3d.js` renders Piko in real time with Three.js, from the same
locked geometry (extruded stem + half-disc bowl with the notch bite,
antenna, one eye). `3d/index.html` is the interactive viewer (CDN
import map); `3d/shot.html` uses the local `vendor/` copy for
deterministic screenshots (`shot.py`, Playwright + SwiftShader).

Animation lives in the render loop, not in baked clips:

- idle: gentle float + sway, blink every few seconds.
- listening: antenna ball glows, rings pulse, slight lean-in, wider eye.
- speaking: mouth opens following voice amplitude. The voice loop
  feeds it through `window.__piko.setSpeakingLevel(0..1)` (AnalyserNode
  on the TTS audio); without a feed it falls back to a sine pulse.
- roast: cocky tilt + sway, angled brow, half-lidded eye, smirk.
- The viewer supports orbit/zoom; states switch through
  `window.__piko.setState(name)`. No state may change the body geometry.
