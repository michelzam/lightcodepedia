# 🐕🐠 Lucky & Wanda in 3D

The same two objects you met in [Tutorial 101](/tutorial101) — but alive. Every **attribute** you edit changes what you see. Every **method** you call makes them behave. That's all an object is: state you can read, behavior you can invoke.

**Try it:** change Lucky's `colour`, drag `weight_kg`, then call `lucky.run()` and watch his `top_speed_kmh` matter.

<div id="l3d-app">
<style>
#l3d-app { font-size: 0.92em; }
#l3d-stage { width: 100%; height: 440px; border-radius: 10px; overflow: hidden; background: linear-gradient(#bfe3f7, #e8f6e8); position: relative; }
#l3d-stage canvas { display: block; }
.l3d-cols { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 14px; }
@media (max-width: 760px) { .l3d-cols { grid-template-columns: 1fr; } }
.l3d-card { border: 1px solid #d8dee6; border-radius: 10px; padding: 12px 14px; background: #fff; }
.l3d-card h4 { margin: 0 0 8px; font-size: 1.02em; }
.l3d-row { display: flex; align-items: center; gap: 8px; margin: 5px 0; }
.l3d-row label { width: 118px; color: #475569; font-family: monospace; font-size: 0.86em; flex: none; }
.l3d-row input[type=range] { flex: 1; }
.l3d-row select, .l3d-row input[type=text] { flex: 1; padding: 2px 6px; border: 1px solid #cbd5e1; border-radius: 5px; font-size: 0.9em; }
.l3d-row output { width: 52px; text-align: right; font-family: monospace; font-size: 0.84em; color: #0369a1; }
.l3d-methods { display: flex; flex-wrap: wrap; gap: 7px; margin-top: 10px; }
.l3d-methods button { border: none; border-radius: 6px; padding: 5px 12px; font-family: monospace; font-size: 0.86em; cursor: pointer; background: #0066cc; color: #fff; }
.l3d-methods button:hover { background: #0052a3; }
.l3d-console { margin-top: 14px; background: #0f172a; color: #a5f3fc; border-radius: 8px; padding: 10px 14px; font-family: monospace; font-size: 0.82em; min-height: 86px; }
.l3d-console div { opacity: 0.55; }
.l3d-console div:last-child { opacity: 1; }
</style>

<div id="l3d-stage"></div>

<div class="l3d-cols">
  <div class="l3d-card">
    <h4>🐕 lucky : Dog</h4>
    <div class="l3d-row"><label>colour</label>
      <select id="lk-colour">
        <option value="#1a1a1a" selected>Black</option>
        <option value="#8b5a2b">Brown</option>
        <option value="#d4a24e">Golden</option>
        <option value="#ece8e1">White</option>
        <option value="#7a7d82">Grey</option>
      </select></div>
    <div class="l3d-row"><label>weight_kg</label>
      <input type="range" id="lk-weight" min="8" max="60" step="1" value="28"><output id="lk-weight-o">28</output></div>
    <div class="l3d-row"><label>top_speed_kmh</label>
      <input type="range" id="lk-speed" min="10" max="75" step="1" value="40"><output id="lk-speed-o">40</output></div>
    <div class="l3d-row"><label>adopted</label>
      <input type="checkbox" id="lk-adopted" checked> <span style="font-size:0.8em;color:#64748b">(adopted dogs wear a red collar)</span></div>
    <div class="l3d-methods">
      <button id="lk-bark">bark()</button>
      <button id="lk-run">run()</button>
      <button id="lk-wag">wag_tail()</button>
    </div>
  </div>

  <div class="l3d-card">
    <h4>🐠 wanda : Fish</h4>
    <div class="l3d-row"><label>colour</label>
      <select id="wa-colour">
        <option value="#e67e22" selected>Orange</option>
        <option value="#f1c40f">Gold</option>
        <option value="#e74c3c">Red</option>
        <option value="#3498db">Blue</option>
        <option value="#ecf0f1">White</option>
      </select></div>
    <div class="l3d-row"><label>weight_kg</label>
      <input type="range" id="wa-weight" min="0.01" max="0.5" step="0.01" value="0.03"><output id="wa-weight-o">0.03</output></div>
    <div class="l3d-row"><label>top_speed_kmh</label>
      <input type="range" id="wa-speed" min="1" max="15" step="1" value="6"><output id="wa-speed-o">6</output></div>
    <div class="l3d-row"><label>adopted</label>
      <input type="checkbox" id="wa-adopted"> <span style="font-size:0.8em;color:#64748b">(adopted fish get a castle)</span></div>
    <div class="l3d-methods">
      <button id="wa-swim">swim()</button>
      <button id="wa-bubble">blow_bubble()</button>
    </div>
  </div>
</div>

<div class="l3d-console" id="l3d-console"><div># edit an attribute or call a method…</div></div>

<script type="importmap">
{ "imports": {
  "three": "https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js",
  "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/"
} }
</script>
<script type="module">
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";

const stage = document.getElementById("l3d-stage");
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
camera.position.set(0, 4.2, 9.5);
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
stage.appendChild(renderer.domElement);
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 0.8, 0);
controls.maxPolarAngle = Math.PI * 0.49;
controls.enableDamping = true;

function resize() {
  const w = stage.clientWidth, h = stage.clientHeight;
  renderer.setSize(w, h); camera.aspect = w / h; camera.updateProjectionMatrix();
}
addEventListener("resize", resize);

scene.add(new THREE.AmbientLight(0xffffff, 0.75));
const sun = new THREE.DirectionalLight(0xfff4e0, 1.2);
sun.position.set(4, 8, 6);
scene.add(sun);

const grass = new THREE.Mesh(
  new THREE.CylinderGeometry(9, 9, 0.3, 40),
  new THREE.MeshLambertMaterial({ color: 0x8fcf7a }));
grass.position.y = -0.15;
scene.add(grass);

// ── the object console: every interaction prints its code form ─────────
const consoleEl = document.getElementById("l3d-console");
function logCode(line) {
  const d = document.createElement("div");
  d.textContent = line;
  consoleEl.appendChild(d);
  while (consoleEl.children.length > 6) consoleEl.removeChild(consoleEl.firstChild);
}

// ── Lucky: a low-poly dog built from primitives ─────────────────────────
function makeDog() {
  const g = new THREE.Group();
  const mat = new THREE.MeshLambertMaterial({ color: 0x1a1a1a });
  const dark = new THREE.MeshLambertMaterial({ color: 0x0c0c0c });

  const body = new THREE.Mesh(new THREE.BoxGeometry(1.9, 0.9, 0.85), mat);
  body.position.y = 1.0; g.add(body);
  const head = new THREE.Mesh(new THREE.BoxGeometry(0.75, 0.7, 0.7), mat);
  head.position.set(1.15, 1.55, 0); g.add(head);
  const snout = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.3, 0.4), mat);
  snout.position.set(1.62, 1.42, 0); g.add(snout);
  const nose = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.12, 0.18), dark);
  nose.position.set(1.84, 1.46, 0); g.add(nose);
  for (const s of [-1, 1]) {
    const ear = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.42, 0.22), dark);
    ear.position.set(1.0, 1.98, 0.24 * s); ear.rotation.x = 0.15 * s; g.add(ear);
    const eye = new THREE.Mesh(new THREE.SphereGeometry(0.055), dark);
    eye.position.set(1.5, 1.66, 0.2 * s); g.add(eye);
  }
  const legs = [];
  for (const [x, z] of [[-0.7, 0.3], [-0.7, -0.3], [0.65, 0.3], [0.65, -0.3]]) {
    const leg = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.75, 0.22), mat);
    leg.position.set(x, 0.38, z); g.add(leg); legs.push(leg);
  }
  const tail = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.14, 0.14), mat);
  tail.geometry.translate(-0.27, 0, 0);
  tail.position.set(-0.95, 1.25, 0); tail.rotation.z = 0.55; g.add(tail);
  const collar = new THREE.Mesh(
    new THREE.TorusGeometry(0.42, 0.06, 8, 20),
    new THREE.MeshLambertMaterial({ color: 0xd62828 }));
  collar.position.set(0.95, 1.25, 0); collar.rotation.y = Math.PI / 2; g.add(collar);
  return { group: g, mat, legs, tail, collar, head };
}

// ── Wanda: a fish in a glass bowl ───────────────────────────────────────
function makeFish() {
  const root = new THREE.Group();
  const bowl = new THREE.Mesh(
    new THREE.SphereGeometry(1.5, 28, 20, 0, Math.PI * 2, 0.5),
    new THREE.MeshPhysicalMaterial({ color: 0xbfe8ff, transparent: true, opacity: 0.28, side: THREE.DoubleSide }));
  bowl.position.y = 1.45; root.add(bowl);
  const water = new THREE.Mesh(
    new THREE.SphereGeometry(1.38, 24, 16),
    new THREE.MeshLambertMaterial({ color: 0x7eccee, transparent: true, opacity: 0.35 }));
  water.scale.y = 0.72; water.position.y = 1.25; root.add(water);

  const g = new THREE.Group();
  const mat = new THREE.MeshLambertMaterial({ color: 0xe67e22 });
  const body = new THREE.Mesh(new THREE.SphereGeometry(0.34, 18, 14), mat);
  body.scale.set(1.35, 1, 0.7); g.add(body);
  const tail = new THREE.Mesh(new THREE.ConeGeometry(0.22, 0.4, 4), mat);
  tail.rotation.z = Math.PI / 2; tail.position.x = -0.55; g.add(tail);
  const fin = new THREE.Mesh(new THREE.ConeGeometry(0.12, 0.25, 4), mat);
  fin.position.set(0, 0.36, 0); g.add(fin);
  const eyeM = new THREE.MeshLambertMaterial({ color: 0x111111 });
  for (const s of [-1, 1]) {
    const eye = new THREE.Mesh(new THREE.SphereGeometry(0.045), eyeM);
    eye.position.set(0.3, 0.07, 0.21 * s); g.add(eye);
  }
  g.position.y = 1.35; root.add(g);

  const castle = new THREE.Group();
  const cMat = new THREE.MeshLambertMaterial({ color: 0xc9b18a });
  const keep = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.26, 0.5, 10), cMat);
  castle.add(keep);
  const roof = new THREE.Mesh(new THREE.ConeGeometry(0.26, 0.3, 10),
    new THREE.MeshLambertMaterial({ color: 0x9a6fb0 }));
  roof.position.y = 0.4; castle.add(roof);
  castle.position.set(0.5, 0.42, -0.4); castle.visible = false; root.add(castle);
  return { root, fish: g, mat, tail, castle };
}

const lucky = makeDog();
lucky.group.position.set(-2.6, 0, 0);
lucky.group.rotation.y = 0.5;
scene.add(lucky.group);

const wanda = makeFish();
wanda.root.position.set(2.8, 0, 0);
scene.add(wanda.root);

// ── live state — the attributes drive everything in the render loop ────
const L = { weight: 28, speed: 40, adopted: true, state: "idle", t: 0, angle: 0 };
const W = { weight: 0.03, speed: 6, adopted: false, boost: 0, angle: 0 };
const bubbles = [];

function dogScale() { const s = 0.55 + L.weight / 55; lucky.group.scale.setScalar(s); }
function fishScale() { const s = 0.8 + W.weight * 1.6; wanda.fish.scale.setScalar(s); }
dogScale(); fishScale();
lucky.collar.visible = L.adopted;

// "Woof!" floating sprite
function woofSprite() {
  const c = document.createElement("canvas"); c.width = 256; c.height = 96;
  const x = c.getContext("2d");
  x.font = "bold 56px sans-serif"; x.fillStyle = "#1e293b";
  x.strokeStyle = "#fff"; x.lineWidth = 8;
  x.strokeText("Woof!", 30, 62); x.fillText("Woof!", 30, 62);
  const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(c), transparent: true }));
  sp.scale.set(1.8, 0.7, 1);
  return sp;
}
let woof = null, woofT = 0;

// ── wire the attribute panel ────────────────────────────────────────────
function bind(id, fn) { document.getElementById(id).addEventListener("input", fn); }
function out(id, v) { document.getElementById(id).textContent = v; }

bind("lk-colour", e => {
  lucky.mat.color.set(e.target.value);
  logCode('lucky.colour = "' + e.target.selectedOptions[0].text + '"');
});
bind("lk-weight", e => { L.weight = +e.target.value; out("lk-weight-o", L.weight); dogScale();
  logCode("lucky.weight_kg = " + L.weight); });
bind("lk-speed", e => { L.speed = +e.target.value; out("lk-speed-o", L.speed);
  logCode("lucky.top_speed_kmh = " + L.speed); });
bind("lk-adopted", e => { L.adopted = e.target.checked; lucky.collar.visible = L.adopted;
  logCode("lucky.adopted = " + L.adopted); });

bind("wa-colour", e => {
  wanda.mat.color.set(e.target.value);
  logCode('wanda.colour = "' + e.target.selectedOptions[0].text + '"');
});
bind("wa-weight", e => { W.weight = +e.target.value; out("wa-weight-o", W.weight); fishScale();
  logCode("wanda.weight_kg = " + W.weight); });
bind("wa-speed", e => { W.speed = +e.target.value; out("wa-speed-o", W.speed);
  logCode("wanda.top_speed_kmh = " + W.speed); });
bind("wa-adopted", e => { W.adopted = e.target.checked; wanda.castle.visible = W.adopted;
  logCode("wanda.adopted = " + W.adopted); });

// ── methods ─────────────────────────────────────────────────────────────
document.getElementById("lk-bark").onclick = () => {
  L.state = "bark"; L.t = 0;
  woof = woofSprite();
  woof.position.copy(lucky.group.position).add(new THREE.Vector3(1.4, 2.6, 0));
  scene.add(woof); woofT = 0;
  logCode('lucky.bark()  → "Woof! Woof!"');
};
document.getElementById("lk-run").onclick = () => {
  L.state = "run"; L.t = 0;
  logCode("lucky.run()  # speed = " + L.speed + " km/h");
};
document.getElementById("lk-wag").onclick = () => {
  L.state = "wag"; L.t = 0;
  logCode("lucky.wag_tail()");
};
document.getElementById("wa-swim").onclick = () => {
  W.boost = 3;
  logCode("wanda.swim()  # speed = " + W.speed + " km/h");
};
document.getElementById("wa-bubble").onclick = () => {
  for (let i = 0; i < 5; i++) {
    const b = new THREE.Mesh(new THREE.SphereGeometry(0.035 + Math.random() * 0.04, 8, 8),
      new THREE.MeshLambertMaterial({ color: 0xe8faff, transparent: true, opacity: 0.75 }));
    b.position.copy(wanda.root.position)
      .add(new THREE.Vector3(wanda.fish.position.x + 0.4, 1.35, wanda.fish.position.z));
    b.userData.v = 0.4 + Math.random() * 0.5;
    b.userData.x = (Math.random() - 0.5) * 0.3;
    scene.add(b); bubbles.push(b);
  }
  logCode("wanda.blow_bubble()");
};

// ── render loop: state machine drives the animations ───────────────────
const clock = new THREE.Clock();
function tick() {
  requestAnimationFrame(tick);
  const dt = Math.min(clock.getDelta(), 0.05);
  const t = clock.elapsedTime;

  // Lucky
  if (L.state === "run") {
    L.t += dt;
    const w = L.speed / 14;                 // angular speed from top_speed_kmh
    L.angle += w * dt;
    const r = 3.1;
    lucky.group.position.set(-2.6 + Math.sin(L.angle) * r * 0.5 - r * 0.0,
      0, Math.cos(L.angle) * r * 0.55);
    lucky.group.rotation.y = L.angle + Math.PI / 2;
    lucky.legs.forEach((leg, i) => { leg.rotation.x = Math.sin(t * w * 6 + i * Math.PI) * 0.7; });
    lucky.tail.rotation.y = Math.sin(t * 14) * 0.4;
    if (L.t > 4.5) { L.state = "idle"; lucky.legs.forEach(l => l.rotation.x = 0); }
  } else if (L.state === "bark") {
    L.t += dt;
    lucky.head.rotation.z = Math.sin(L.t * 22) * 0.16;
    if (L.t > 1.1) { L.state = "idle"; lucky.head.rotation.z = 0; }
  } else if (L.state === "wag") {
    L.t += dt;
    lucky.tail.rotation.y = Math.sin(L.t * 18) * 0.9;
    if (L.t > 2) { L.state = "idle"; lucky.tail.rotation.y = 0; }
  } else {
    lucky.group.position.y = Math.sin(t * 1.6) * 0.02;   // idle breathing
    lucky.tail.rotation.y = Math.sin(t * 3) * 0.18;
  }

  if (woof) {
    woofT += dt;
    woof.position.y += dt * 0.9;
    woof.material.opacity = Math.max(0, 1 - woofT);
    if (woofT > 1) { scene.remove(woof); woof = null; }
  }

  // Wanda swims laps; swim() boosts her for a few seconds
  const boost = W.boost > 0 ? 2.2 : 1;
  if (W.boost > 0) W.boost -= dt;
  W.angle += dt * (0.4 + W.speed / 12) * boost;
  const wr = 0.78;
  wanda.fish.position.set(Math.cos(W.angle) * wr, 1.3 + Math.sin(t * 2) * 0.07, Math.sin(W.angle) * wr * 0.7);
  wanda.fish.rotation.y = -W.angle + Math.PI;
  wanda.tail.rotation.y = Math.sin(t * 10 * boost) * 0.5;

  for (let i = bubbles.length - 1; i >= 0; i--) {
    const b = bubbles[i];
    b.position.y += b.userData.v * dt;
    b.position.x += b.userData.x * dt;
    if (b.position.y > 2.65) { scene.remove(b); bubbles.splice(i, 1); }
  }

  controls.update();
  renderer.render(scene, camera);
}
resize();
tick();
</script>
</div>

## 🧠 What just happened?

| You did | In object terms |
|---|---|
| Picked a colour | `lucky.colour = "Golden"` — an **attribute assignment**, the object re-renders |
| Dragged weight_kg | same attribute, *continuous* value — state drives appearance |
| Clicked `bark()` | a **method call** — behavior that uses the object's own state |
| Clicked `run()` | the animation speed comes from `top_speed_kmh` — methods read attributes |
| Ticked adopted | a **boolean** attribute with a visible consequence (collar / castle) |

The YAML forms in [Tutorial 101](/tutorial101) and these 3D bodies are **the same objects** — one shows the state as text, the other as behavior. Alt-hover any component on this site (or use 📽️ → X-ray on mobile) to see this structure everywhere.
