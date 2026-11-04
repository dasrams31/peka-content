import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// Piko in 3D. Body geometry matches the locked 2D mascot (mascot.py,
// mascot_p): 1080px space scaled by 1/100, origin at the P's visual
// center (595, 500), Y flipped. Only the face layer changes per state.

const params = new URLSearchParams(location.search);
const START_STATE = params.get('state') || 'idle';
const STILL = params.get('still') === '1';
const RY = parseFloat(params.get('ry') || '0');

const YELLOW = 0xffd60a;
const INK = 0x111111;

const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.setSize(innerWidth, innerHeight);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
document.getElementById('stage').appendChild(renderer.domElement);

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(38, innerWidth / innerHeight, 0.1, 100);
camera.position.set(0.3, 0.4, 11.0);

const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, -0.05, 0);
controls.enableDamping = true;
controls.dampingFactor = 0.06;
controls.minDistance = 5;
controls.maxDistance = 16;
controls.enablePan = false;
controls.autoRotate = !STILL;

scene.add(new THREE.HemisphereLight(0xffffff, 0x1a1a1a, 1.0));
const key = new THREE.DirectionalLight(0xffffff, 2.2);
key.position.set(3, 6, 8);
scene.add(key);
const rim = new THREE.DirectionalLight(YELLOW, 0.9);
rim.position.set(-6, 3, -5);
scene.add(rim);
const fill = new THREE.DirectionalLight(0xffffff, 0.5);
fill.position.set(-3, 0, 6);
scene.add(fill);

const matYellow = new THREE.MeshStandardMaterial({ color: YELLOW, roughness: 0.35, metalness: 0.05 });
const matInk = new THREE.MeshStandardMaterial({ color: INK, roughness: 0.5, metalness: 0.0 });
const matBall = new THREE.MeshStandardMaterial({ color: YELLOW, roughness: 0.3, metalness: 0.05, emissive: YELLOW, emissiveIntensity: 0 });

const EXTRUDE = { depth: 0.8, bevelEnabled: true, bevelThickness: 0.12, bevelSize: 0.12, bevelSegments: 4, curveSegments: 48 };

function roundedRectShape(x0, y0, x1, y1, r) {
  const s = new THREE.Shape();
  s.moveTo(x0 + r, y0);
  s.lineTo(x1 - r, y0);
  s.absarc(x1 - r, y0 + r, r, -Math.PI / 2, 0, false);
  s.lineTo(x1, y1 - r);
  s.absarc(x1 - r, y1 - r, r, 0, Math.PI / 2, false);
  s.lineTo(x0 + r, y1);
  s.absarc(x0 + r, y1 - r, r, Math.PI / 2, Math.PI, false);
  s.lineTo(x0, y0 + r);
  s.absarc(x0 + r, y0 + r, r, Math.PI, Math.PI * 1.5, false);
  return s;
}

function extrude(shape) {
  const g = new THREE.ExtrudeGeometry(shape, EXTRUDE);
  g.translate(0, 0, -EXTRUDE.depth / 2);
  return new THREE.Mesh(g, matYellow);
}

const piko = new THREE.Group();
scene.add(piko);

// Stem: 2D rect [450,330,580,822] -> x[-1.45,-0.15], y[-3.22,1.70]
piko.add(extrude(roundedRectShape(-1.45, -3.22, -0.15, 1.70, 0.65)));

// Bowl: half-disc, flat edge x=0.10, center (0.10, 0.45), radius 1.4
// Bowl: half-disc with the signature semicircular notch bitten out of
// the flat edge (the 2D black bite at (605, 455), r=36px).
const bowlShape = new THREE.Shape();
bowlShape.moveTo(0.10, 1.85);
bowlShape.absarc(0.10, 0.45, 1.4, Math.PI / 2, -Math.PI / 2, true);
bowlShape.lineTo(0.10, 0.81);
bowlShape.absarc(0.10, 0.45, 0.36, Math.PI / 2, -Math.PI / 2, true);
bowlShape.lineTo(0.10, -0.95);
bowlShape.closePath();
piko.add(extrude(bowlShape));

// Antenna
const antenna = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 1.0, 16), matYellow);
antenna.position.set(-0.8, 2.18, 0);
piko.add(antenna);
const ball = new THREE.Mesh(new THREE.SphereGeometry(0.28, 32, 24), matBall);
ball.position.set(-0.8, 2.95, 0);
piko.add(ball);

// Listening glow rings around the antenna ball
const ringMat = new THREE.MeshBasicMaterial({ color: YELLOW, transparent: true, opacity: 0.85 });
const ring1 = new THREE.Mesh(new THREE.TorusGeometry(0.42, 0.035, 12, 48), ringMat);
const ring2 = new THREE.Mesh(new THREE.TorusGeometry(0.56, 0.02, 12, 48), ringMat.clone());
ring1.position.copy(ball.position);
ring2.position.copy(ball.position);
piko.add(ring1, ring2);

// Eye (base mesh, scaled per state)
const eye = new THREE.Mesh(new THREE.SphereGeometry(0.45, 40, 28), matInk);
eye.position.set(-0.85, 0.55, 0.42);
eye.scale.set(1, 1, 0.45);
piko.add(eye);

// Smile (torus arc, bottom arc = smile)
const smile = new THREE.Mesh(new THREE.TorusGeometry(0.40, 0.09, 14, 48, 2.27), matInk);
smile.position.set(-0.85, -0.55, 0.52);
smile.rotation.z = THREE.MathUtils.degToRad(205);
piko.add(smile);

// Smirk (roast): shorter arc, rotated asymmetric
const smirk = new THREE.Mesh(new THREE.TorusGeometry(0.38, 0.09, 14, 48, 1.9), matInk);
smirk.position.set(-0.80, -0.52, 0.52);
smirk.rotation.z = THREE.MathUtils.degToRad(230);
piko.add(smirk);

// Small open mouth (listening)
const mouthSmall = new THREE.Mesh(new THREE.SphereGeometry(0.17, 24, 18), matInk);
mouthSmall.position.set(-0.80, -0.46, 0.52);
mouthSmall.scale.set(1, 0.8, 0.5);
piko.add(mouthSmall);

// Open mouth (speaking), pulsed in the animation loop
const mouthOpen = new THREE.Mesh(new THREE.SphereGeometry(0.38, 32, 24), matInk);
mouthOpen.position.set(-0.85, -0.44, 0.50);
mouthOpen.scale.set(1.25, 0.6, 0.35);
piko.add(mouthOpen);

// Angled brow (roast)
const brow = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.15, 0.12), matInk);
brow.position.set(-0.87, 1.14, 0.55);
brow.rotation.z = -0.25;
piko.add(brow);

// Soft blob shadow under the character
const blob = new THREE.Mesh(
  new THREE.CircleGeometry(1.9, 40),
  new THREE.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: 0.35 })
);
blob.rotation.x = -Math.PI / 2;
blob.position.set(0, -3.7, 0);
scene.add(blob);

let state = 'idle';
let eyeBaseScaleY = 1;
let eyeBaseY = 0.55;
let apiLevel = null;
let speakLevel = 0;
let nextBlink = 2.5;
const FACE = { smile, smirk, mouthSmall, mouthOpen, brow, ring1, ring2 };

function setState(name) {
  state = name;
  eyeBaseScaleY = 1;
  eyeBaseY = 0.55;
  eye.position.set(-0.85, eyeBaseY, 0.42);
  eye.scale.set(1, 1, 0.45);
  smile.visible = name === 'idle';
  smirk.visible = name === 'roast';
  mouthSmall.visible = name === 'listening';
  mouthOpen.visible = name === 'speaking';
  brow.visible = name === 'roast';
  ring1.visible = ring2.visible = name === 'listening';
  matBall.emissiveIntensity = name === 'listening' ? 0.9 : 0;
  if (name === 'listening') { eyeBaseScaleY = 1.15; eye.scale.set(1.15, 1.15, 0.45); }
  if (name === 'roast') {
    eyeBaseScaleY = 0.55;
    eyeBaseY = 0.42;
    eye.scale.set(1, 0.55, 0.45);
    eye.position.y = 0.42;
    piko.rotation.set(0, 0.15 + RY, -0.06);
  } else {
    piko.rotation.set(0, RY, 0);
  }
  document.querySelectorAll('[data-state]').forEach((b) => {
    b.classList.toggle('active', b.dataset.state === name);
  });
  const label = document.getElementById('state-label');
  if (label) label.textContent = { idle: 'Diam', listening: 'Mendengarkan', speaking: 'Berbicara', roast: 'Mode Judes' }[name];
}

document.querySelectorAll('[data-state]').forEach((b) => {
  b.addEventListener('click', () => setState(b.dataset.state));
});
window.__setState = setState;
window.__setSpeakingLevel = (v) => { apiLevel = Math.max(0, Math.min(1, v)); };
window.__piko = { setState, setSpeakingLevel: window.__setSpeakingLevel };
setState(START_STATE);

const clock = new THREE.Clock();
let rendered = 0;
function animate() {
  requestAnimationFrame(animate);
  const t = STILL ? 0.8 : clock.getElapsedTime();
  if (!STILL) {
    piko.position.y = Math.sin(t * 1.4) * 0.08;
    blob.material.opacity = 0.35 - Math.sin(t * 1.4) * 0.03;
  }
  // Idle sway, roast cocky sway, listening lean
  if (state === 'roast') {
    piko.rotation.set(0, 0.15 + RY + Math.sin(t * 0.8) * 0.03, -0.06 + Math.sin(t * 2) * 0.02);
  } else {
    piko.rotation.set(state === 'listening' ? 0.05 : 0, RY + Math.sin(t * 0.6) * 0.05, 0);
  }
  // Blink: brief eye dip every few seconds
  let blink = 1;
  if (t >= nextBlink) {
    const ph = (t - nextBlink) / 0.12;
    if (ph >= 1) { nextBlink = t + 2.2 + ((t * 997) % 1) * 2.0; }
    else blink = 1 - Math.sin(ph * Math.PI) * 0.9;
  }
  eye.scale.y = eyeBaseScaleY * blink;
  eye.scale.x = state === 'listening' ? 1.15 : 1;
  // Talking: mouth follows the voice amplitude (API) or a sine fallback
  const target = state === 'speaking' ? (apiLevel ?? (0.5 + 0.5 * Math.sin(t * 9))) : 0;
  speakLevel += (target - speakLevel) * 0.35;
  mouthOpen.scale.set(1.25, 0.15 + 0.55 * speakLevel, 0.35);
  if (state === 'listening') {
    const p = 1 + Math.sin(t * 3) * 0.12;
    ring1.scale.set(p, p, 1);
    ring2.scale.set(2 - p, 2 - p, 1);
  }
  controls.update();
  renderer.render(scene, camera);
  if (++rendered === 3) window.__pikoReady = true;
}
animate();

addEventListener('resize', () => {
  camera.aspect = innerWidth / innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(innerWidth, innerHeight);
});
