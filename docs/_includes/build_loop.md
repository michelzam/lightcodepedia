{%- comment -%}
Build Loop — a slowly turning hex hive where agents, blocks and apps move
through one continuous cycle. High-level on purpose: it shows the *mechanics*
of building with AI, not a literal construction site.

Usage:
  ```
  Spot the need: every build starts with someone's problem
  Shape it: turn the need into a design you can hold
  Assemble: snap the working blocks together
  Add AI: bring in the partner that thinks with you
  Ship it: put it in someone's hands
  Learn: what you shipped teaches the next loop
  ```
  {: .build_loop height="460" }

One station per line, `Label: blurb`. Three to eight lines.

Attributes:
  height   stage height in px            (default 460)
  speed    global animation rate         (default 1)
  spin     auto-rotate the scene         (default true, "false" to stop)
  agents   figures circulating the ring  (default 5)

Drag to rotate, scroll to zoom, hover a pod to preview it, click to pin a
legend that rides along with it.

Verbs (window.lcVerbs — an avatar can fire these mid-sentence):
  pin [label]       attach a station's legend, and leave it attached
  unpin [label]     close one, or all of them when given no label
  look_at [label]   ease the hive round until that station faces the viewer
  spin [on|off]     auto-rotation; bare `spin` toggles
  recentre          back to the opening framing

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-build-loop { margin: 1em 0; font-size: 0.92em; }
.lc-bl-stage { width: 100%; border-radius: 10px; overflow: hidden; position: relative;
  background: linear-gradient(#cfe9fa, #eef7ea); cursor: grab; }
.lc-bl-stage:active { cursor: grabbing; }
.lc-bl-stage canvas { display: block; }
.lc-bl-loading { display: flex; align-items: center; justify-content: center;
  height: 100%; color: #64748b; font-family: monospace; font-size: 0.9em; }
.lc-bl-bar { display: flex; flex-wrap: wrap; align-items: center; gap: 8px;
  margin-top: 10px; }
.lc-bl-bar button { border: none; border-radius: 6px; padding: 5px 12px;
  font-family: monospace; font-size: 0.86em; cursor: pointer;
  background: #0066cc; color: #fff; }
.lc-bl-bar button:hover { background: #0052a3; }
.lc-bl-hint { color: #64748b; font-size: 0.84em; margin-left: auto; }
@media (max-width: 620px) { .lc-bl-hint { margin-left: 0; width: 100%; } }
.lc-bl-read { margin-top: 10px; padding: 11px 15px; border-radius: 10px;
  background: #fff; border: 1px solid #d8dee6; min-height: 3.2em; line-height: 1.45; }
.lc-bl-read b { display: inline-block; padding: 1px 8px; border-radius: 999px;
  color: #fff; font-size: 0.86em; letter-spacing: 0.03em; margin-right: 7px; }
.lc-bl-read span { color: #475569; }
.lc-bl-read.lc-bl-idle span { color: #94a3b8; font-style: italic; }
.lc-bl-legend { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 9px; }
.lc-bl-legend button { border: none; border-radius: 999px; padding: 4px 12px;
  font-size: 0.8em; letter-spacing: 0.03em; cursor: pointer; color: #fff;
  opacity: 0.62; transition: opacity 0.15s ease, transform 0.15s ease; }
.lc-bl-legend button:hover, .lc-bl-legend button:focus-visible {
  opacity: 1; transform: translateY(-2px); outline: 2px solid #0f172a; outline-offset: 2px; }
.lc-bl-legend button.is-pinned { opacity: 1; box-shadow: 0 0 0 2px #0f172a inset; }
.lc-bl-pin { position: absolute; left: 0; top: 0; width: 186px; padding: 8px 10px 9px;
  border-radius: 10px; background: rgba(255,255,255,0.96); border: 1px solid #cdd6e0;
  border-top: 3px solid var(--pin, #0066cc); box-shadow: 0 8px 20px rgba(15,23,42,0.18);
  font-size: 0.82em; line-height: 1.4; pointer-events: auto; z-index: 2;
  transition: opacity 0.2s ease; }
.lc-bl-pin-head { display: flex; align-items: center; gap: 8px; }
.lc-bl-pin-head b { flex: 1; color: var(--pin, #0066cc); letter-spacing: 0.03em;
  font-size: 0.94em; text-transform: uppercase; }
.lc-bl-pin-head button { border: none; background: none; cursor: pointer; padding: 0 2px;
  font-size: 1.15em; line-height: 1; color: #94a3b8; }
.lc-bl-pin-head button:hover { color: #0f172a; }
.lc-bl-pin-body { display: block; margin-top: 2px; color: #475569; }
.lc-bl-pin-stem { position: absolute; left: 50%; bottom: -7px; width: 12px; height: 12px;
  margin-left: -6px; background: rgba(255,255,255,0.96); border-right: 1px solid #cdd6e0;
  border-bottom: 1px solid #cdd6e0; transform: rotate(45deg); }
</style>

<!-- The Three.js import map lives in _layouts/default.html <head>. -->

<script>
(function () {
  if (window._lcBuildLoopReady) return;
  window._lcBuildLoopReady = true;

  var PALETTE = [0xf2a007, 0xef5f4c, 0x7b6cf6, 0x2f9bd8, 0x29b18a, 0x97c93d,
                 0xe0568f, 0x4d6fe0];

  var _threeP = null;
  function loadThree() {
    if (_threeP) return _threeP;
    _threeP = Promise.all([
      import("three"),
      import("three/addons/controls/OrbitControls.js")
    ]).then(function (mods) {
      return { THREE: mods[0], OrbitControls: mods[1].OrbitControls };
    });
    return _threeP;
  }

  /* ── config ──────────────────────────────────────────── */
  /* One station per line: "Label: what happens here". */
  function parseStations(raw) {
    var out = [];
    raw.split("\n").forEach(function (line) {
      var t = line.trim();
      if (!t || t.charAt(0) === "#") return;
      var i = t.indexOf(":");
      if (i < 0) { out.push({ label: t, blurb: "" }); return; }
      out.push({ label: t.slice(0, i).trim(), blurb: t.slice(i + 1).trim() });
    });
    return out.slice(0, 8);
  }

  var FALLBACK = [
    { label: "Need", blurb: "Every build starts with someone's problem." },
    { label: "Design", blurb: "Turn the need into something you can hold." },
    { label: "Blocks", blurb: "Snap the working parts together." },
    { label: "AI", blurb: "Bring in the partner that thinks with you." },
    { label: "Ship", blurb: "Put it in someone's hands." },
    { label: "Learn", blurb: "What you shipped starts the next loop." }
  ];

  /* Text drawn to a canvas and hung on a sprite — no font loading, no FOUT. */
  function labelSprite(THREE, text, color) {
    var pad = 22, fs = 46;
    var probe = document.createElement("canvas").getContext("2d");
    probe.font = "700 " + fs + "px Inter, Helvetica, Arial, sans-serif";
    var w = Math.ceil(probe.measureText(text).width) + pad * 2;
    var hgt = fs + pad * 2;
    var cv = document.createElement("canvas");
    cv.width = w; cv.height = hgt;
    var ctx = cv.getContext("2d");
    var hex = "#" + color.toString(16).padStart(6, "0");
    ctx.fillStyle = "rgba(255,255,255,0.94)";
    ctx.beginPath();
    ctx.roundRect(0, 0, w, hgt, 26);
    ctx.fill();
    ctx.lineWidth = 6; ctx.strokeStyle = hex; ctx.stroke();
    ctx.font = "700 " + fs + "px Inter, Helvetica, Arial, sans-serif";
    ctx.fillStyle = "#1f2733";
    ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.fillText(text, w / 2, hgt / 2 + 2);

    var tex = new THREE.CanvasTexture(cv);
    tex.colorSpace = THREE.SRGBColorSpace;
    tex.anisotropy = 4;
    /* depthTest off: on a turning ring the far labels would otherwise
       disappear behind the core, and a label you cannot read is worse than
       one drawn slightly out of order. */
    var sprite = new THREE.Sprite(new THREE.SpriteMaterial({
      map: tex, transparent: true, depthWrite: false, depthTest: false
    }));
    sprite.renderOrder = 10;
    /* Small on purpose: six labels on one ring collide fast. */
    var scale = 0.0042;
    sprite.scale.set(w * scale, hgt * scale, 1);
    return sprite;
  }

  /* ── upgrader ────────────────────────────────────────── */

  function upgradeBuildLoop(el) {
    if (el.dataset.lcBuildLoopDone) return;
    el.dataset.lcBuildLoopDone = "1";

    var raw = (el.querySelector("code") || el).textContent.trim();
    var stations = parseStations(raw);
    if (stations.length < 3) stations = FALLBACK;

    var h = parseInt(el.getAttribute("height") || "460", 10);
    var speed = parseFloat(el.getAttribute("speed") || "1") || 1;
    var wantSpin = el.getAttribute("spin") !== "false";
    var agentCount = Math.max(0, Math.min(10,
      parseInt(el.getAttribute("agents") || "5", 10)));
    var calm = window.matchMedia &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    var wrap = document.createElement("div");
    wrap.className = "lc-build-loop";
    if (el.id) { wrap.id = el.id; wrap.setAttribute("data-lc-id", el.id); }
    el.parentNode.replaceChild(wrap, el);

    var stage = document.createElement("div");
    stage.className = "lc-bl-stage";
    stage.style.height = h + "px";
    stage.innerHTML = '<div class="lc-bl-loading">⏳ Loading the loop…</div>';
    wrap.appendChild(stage);

    var bar = document.createElement("div");
    bar.className = "lc-bl-bar";
    var spinBtn = document.createElement("button");
    spinBtn.type = "button";
    var resetBtn = document.createElement("button");
    resetBtn.type = "button";
    resetBtn.textContent = "recentre";
    var hint = document.createElement("span");
    hint.className = "lc-bl-hint";
    hint.textContent = "drag to turn · scroll to zoom · click a pod to pin it";
    bar.appendChild(spinBtn); bar.appendChild(resetBtn); bar.appendChild(hint);
    wrap.appendChild(bar);

    var read = document.createElement("p");
    read.className = "lc-bl-read lc-bl-idle";
    read.innerHTML = "<span>Hover a pod to preview it · click to pin a legend that rides along.</span>";
    wrap.appendChild(read);

    /* Keyboard path to the same information as hovering. */
    var legend = document.createElement("div");
    legend.className = "lc-bl-legend";
    wrap.appendChild(legend);

    function show(i) {
      if (i == null) {
        read.className = "lc-bl-read lc-bl-idle";
        read.innerHTML = "<span>Hover a pod to preview it · click to pin a legend that rides along.</span>";
        return;
      }
      var s = stations[i];
      var hex = "#" + PALETTE[i % PALETTE.length].toString(16).padStart(6, "0");
      read.className = "lc-bl-read";
      read.innerHTML = '<b style="background:' + hex + '"></b><span></span>';
      read.querySelector("b").textContent = s.label;
      read.querySelector("span").textContent = s.blurb || "—";
    }

    /* Chips do everything the 3D pods do: preview on hover or focus, pin on
       click. That is the whole keyboard path into the scene. */
    var chips = [];
    stations.forEach(function (s, i) {
      var b = document.createElement("button");
      b.type = "button";
      b.textContent = s.label;
      b.setAttribute("aria-pressed", "false");
      b.style.background = "#" + PALETTE[i % PALETTE.length].toString(16).padStart(6, "0");
      b.addEventListener("mouseenter", function () { show(i); highlight(i); });
      b.addEventListener("focus", function () { show(i); highlight(i); });
      b.addEventListener("mouseleave", function () { show(null); highlight(null); });
      b.addEventListener("blur", function () { show(null); highlight(null); });
      b.addEventListener("click", function () { togglePin(i); });
      legend.appendChild(b);
      chips.push(b);
    });

    /* replaced once the scene exists */
    var highlight = function () {};
    var togglePin = function () {};
    function syncChip(i, on) {
      if (!chips[i]) return;
      chips[i].setAttribute("aria-pressed", on ? "true" : "false");
      chips[i].classList.toggle("is-pinned", !!on);
    }

    loadThree().then(function (lib) {
      build(lib, stage, stations, {
        speed: speed, spin: wantSpin && !calm, agents: agentCount, calm: calm
      }, {
        spinBtn: spinBtn, resetBtn: resetBtn, show: show, syncChip: syncChip,
        chipAt: function (i) { return chips[i] || null; },
        expose: function (api) { wrap._lcLoopApi = api; },
        bind: function (hoverFn, toggleFn) { highlight = hoverFn; togglePin = toggleFn; }
      });
    }).catch(function (err) {
      stage.innerHTML = '<div class="lc-bl-loading">⚠️ Three.js failed to load.</div>';
      console.error("[build_loop]", err);
    });
  }

  /* ── the scene ───────────────────────────────────────── */

  function build(lib, stage, stations, opts, ui) {
    var THREE = lib.THREE, OrbitControls = lib.OrbitControls;
    var n = stations.length;
    var RING = 3.35;                       /* radius the loop runs on */

    stage.innerHTML = "";
    var renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(2, window.devicePixelRatio));
    renderer.setSize(stage.clientWidth, stage.clientHeight);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.NeutralToneMapping;
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    stage.appendChild(renderer.domElement);

    var scene = new THREE.Scene();
    var camera = new THREE.PerspectiveCamera(
      42, stage.clientWidth / Math.max(1, stage.clientHeight), 0.1, 120);
    camera.position.set(0, 5.4, 11.0);

    var controls = new OrbitControls(camera, renderer.domElement);
    controls.target.set(0, 1.5, 0);
    controls.enableDamping = true;
    controls.dampingFactor = 0.08;
    controls.enablePan = false;
    controls.minDistance = 8;
    controls.maxDistance = 20;
    controls.minPolarAngle = THREE.MathUtils.degToRad(22);
    controls.maxPolarAngle = THREE.MathUtils.degToRad(80);
    controls.autoRotate = opts.spin;
    controls.autoRotateSpeed = 0.55;
    controls.update();

    scene.add(new THREE.HemisphereLight(0xdff0ff, 0xd8cfbf, 1.1));
    var key = new THREE.DirectionalLight(0xfff3e2, 2.1);
    key.position.set(5, 9, 5);
    key.castShadow = true;
    key.shadow.mapSize.set(1024, 1024);
    key.shadow.camera.near = 1; key.shadow.camera.far = 30;
    key.shadow.camera.left = -8; key.shadow.camera.right = 8;
    key.shadow.camera.top = 8; key.shadow.camera.bottom = -8;
    key.shadow.bias = -0.0012;
    key.shadow.normalBias = 0.02;
    key.shadow.radius = 3;
    scene.add(key);
    var fill = new THREE.DirectionalLight(0xbcd8ff, 0.5);
    fill.position.set(-6, 4, -3);
    scene.add(fill);

    function mat(color, o) {
      o = o || {};
      return new THREE.MeshStandardMaterial({
        color: color,
        roughness: o.roughness == null ? 0.42 : o.roughness,
        metalness: o.metalness == null ? 0.05 : o.metalness,
        emissive: o.emissive == null ? 0x000000 : o.emissive,
        emissiveIntensity: o.emissiveIntensity == null ? 1 : o.emissiveIntensity,
        transparent: !!o.transparent,
        opacity: o.opacity == null ? 1 : o.opacity
      });
    }

    /* Everything sits on one rig, so the whole hive reads as one object. */
    var rig = new THREE.Group();
    scene.add(rig);

    /* --- the hive floor: a hex plate, ringed by hex cells -------------- */
    var base = new THREE.Mesh(
      new THREE.CylinderGeometry(RING + 1.5, RING + 1.6, 0.42, 6),
      mat(0xe9e3d6, { roughness: 0.85 }));
    base.position.y = -0.21;
    base.rotation.y = Math.PI / 6;
    base.receiveShadow = true;
    base.castShadow = true;
    rig.add(base);

    /* A honeycomb floor inside the ring — axial hex coordinates, keeping
       only the cells that fall inside the track. This is the "hive". */
    var HEX = 0.46;
    var cellGeo = new THREE.CylinderGeometry(HEX * 0.92, HEX * 0.92, 0.07, 6);
    var spots = [];
    for (var qq = -6; qq <= 6; qq++) {
      for (var rr = -6; rr <= 6; rr++) {
        var cx = HEX * 1.5 * qq;
        var cz = HEX * Math.sqrt(3) * (rr + qq / 2);
        var d = Math.sqrt(cx * cx + cz * cz);
        if (d > RING + 0.45 || d < 0.95) continue;   /* clear of the core */
        spots.push([cx, cz]);
      }
    }
    var cells = new THREE.InstancedMesh(cellGeo, mat(0xdcd5c5, { roughness: 0.92 }),
                                        Math.max(1, spots.length));
    var m4 = new THREE.Matrix4();
    var q0 = new THREE.Quaternion().setFromEuler(new THREE.Euler(0, Math.PI / 6, 0));
    var s1 = new THREE.Vector3(1, 1, 1);
    spots.forEach(function (p, i) {
      m4.compose(new THREE.Vector3(p[0], 0.035, p[1]), q0, s1);
      cells.setMatrixAt(i, m4);
    });
    cells.instanceMatrix.needsUpdate = true;
    cells.receiveShadow = true;
    rig.add(cells);

    /* --- the track the loop runs on ----------------------------------- */
    var track = new THREE.Mesh(
      new THREE.TorusGeometry(RING, 0.07, 8, 96),
      mat(0xffffff, { roughness: 0.5, emissive: 0x9fd7f5, emissiveIntensity: 0.35 }));
    track.rotation.x = Math.PI / 2;
    track.position.y = 0.09;
    rig.add(track);

    /* --- the core: what every loop turns around ------------------------ */
    var core = new THREE.Group();
    core.position.y = 0.02;
    rig.add(core);
    var pillar = new THREE.Mesh(
      new THREE.CylinderGeometry(0.52, 0.68, 1.6, 6),
      mat(0xf6f2e8, { roughness: 0.55 }));
    pillar.position.y = 0.8;
    pillar.castShadow = true; pillar.receiveShadow = true;
    core.add(pillar);
    var collar = new THREE.Mesh(
      new THREE.CylinderGeometry(0.6, 0.6, 0.13, 6),
      mat(0x2f9bd8, { roughness: 0.3 }));
    collar.position.y = 1.62;
    collar.castShadow = true;
    core.add(collar);
    var gem = new THREE.Mesh(
      new THREE.OctahedronGeometry(0.5, 0),
      mat(0x2f9bd8, { roughness: 0.18, metalness: 0.35,
                      emissive: 0x2f9bd8, emissiveIntensity: 0.45 }));
    gem.position.y = 2.5;
    gem.castShadow = true;
    core.add(gem);
    var halo = new THREE.Mesh(
      new THREE.TorusGeometry(0.84, 0.038, 8, 48),
      mat(0xffffff, { emissive: 0x8fd0ee, emissiveIntensity: 0.7, roughness: 0.3 }));
    halo.position.y = 2.5;
    halo.rotation.x = Math.PI / 2.4;
    core.add(halo);

    /* --- the stations ------------------------------------------------- */
    var podGeo = new THREE.CylinderGeometry(0.62, 0.68, 0.55, 6);
    var capGeo = new THREE.CylinderGeometry(0.66, 0.66, 0.12, 6);
    var pods = [];
    stations.forEach(function (s, i) {
      var a = (i / n) * Math.PI * 2 - Math.PI / 2;
      var color = PALETTE[i % PALETTE.length];
      var g = new THREE.Group();
      g.position.set(Math.cos(a) * RING, 0, Math.sin(a) * RING);
      g.rotation.y = -a;

      var body = new THREE.Mesh(podGeo, mat(0xf7f4ec, { roughness: 0.6 }));
      body.position.y = 0.28;
      body.castShadow = true; body.receiveShadow = true;
      g.add(body);

      var cap = new THREE.Mesh(capGeo, mat(color, { roughness: 0.3 }));
      cap.position.y = 0.6;
      cap.castShadow = true;
      g.add(cap);

      /* a token of what this station makes, floating just above it */
      var token = new THREE.Mesh(
        i % 3 === 0 ? new THREE.BoxGeometry(0.28, 0.28, 0.28)
        : i % 3 === 1 ? new THREE.TorusGeometry(0.17, 0.06, 8, 20)
        : new THREE.IcosahedronGeometry(0.2, 0),
        mat(color, { roughness: 0.25, emissive: color, emissiveIntensity: 0.22 }));
      token.position.y = 1.02;
      token.castShadow = true;
      g.add(token);

      var lbl = labelSprite(THREE, s.label, color);
      lbl.position.y = 1.56;
      g.add(lbl);

      /* generous invisible hit volume — pods are small on a phone */
      var hit = new THREE.Mesh(
        new THREE.CylinderGeometry(0.95, 0.95, 2.1, 6),
        new THREE.MeshBasicMaterial({ visible: false }));
      hit.position.y = 0.9;
      hit.userData.podIndex = i;
      g.add(hit);

      rig.add(g);
      pods.push({ group: g, cap: cap, token: token, angle: a, color: color, base: 1.02 });
    });

    /* --- blocks flowing from station to station ------------------------ */
    /* Each block belongs to one leg of the loop and repeats it forever, so
       the ring always looks like one continuous stream of work. */
    var blockGeo = new THREE.BoxGeometry(0.26, 0.26, 0.26);
    var blocks = [];
    for (var b = 0; b < n * 2; b++) {
      var from = b % n;
      var mesh = new THREE.Mesh(blockGeo, mat(PALETTE[from % PALETTE.length], { roughness: 0.3 }));
      mesh.castShadow = true;
      rig.add(mesh);
      blocks.push({ mesh: mesh, from: from, phase: (b / (n * 2)) });
    }

    /* --- agents: the people carrying the work around ------------------- */
    var agents = [];
    var bodyGeo = new THREE.CapsuleGeometry(0.19, 0.3, 4, 10);
    var headGeo = new THREE.SphereGeometry(0.17, 14, 10);
    for (var ai = 0; ai < opts.agents; ai++) {
      var g2 = new THREE.Group();
      var tone = PALETTE[(ai * 3) % PALETTE.length];
      var bod = new THREE.Mesh(bodyGeo, mat(tone, { roughness: 0.45 }));
      bod.position.y = 0.35;
      bod.castShadow = true;
      g2.add(bod);
      var head = new THREE.Mesh(headGeo, mat(0xf3d6b6, { roughness: 0.6 }));
      head.position.y = 0.74;
      head.castShadow = true;
      g2.add(head);
      rig.add(g2);
      agents.push({ group: g2, body: bod, phase: ai / Math.max(1, opts.agents),
                    rate: 0.055 + (ai % 3) * 0.006 });
    }

    /* --- apps: what the loop produces, rising and orbiting ------------- */
    var apps = [];
    var appGeo = new THREE.BoxGeometry(0.52, 0.68, 0.06);
    var screenGeo = new THREE.PlaneGeometry(0.4, 0.46);
    for (var q = 0; q < 3; q++) {
      var g3 = new THREE.Group();
      var card = new THREE.Mesh(appGeo, mat(0xf7f4ec, { roughness: 0.35 }));
      card.castShadow = true;
      g3.add(card);
      var screen = new THREE.Mesh(screenGeo, mat(0x1f6fd0, {
        roughness: 0.2, emissive: 0x2e86ff, emissiveIntensity: 0.55 }));
      screen.position.set(0, 0.06, 0.035);
      g3.add(screen);
      var back = new THREE.Mesh(screenGeo, screen.material);
      back.position.set(0, 0.06, -0.035);
      back.rotation.y = Math.PI;
      g3.add(back);
      rig.add(g3);
      apps.push({ group: g3, screen: screen, phase: q / 3 });
    }

    /* --- interaction --------------------------------------------------- */
    var ray = new THREE.Raycaster();
    var ptr = new THREE.Vector2();
    var hovered = null;
    var pins = {};                 /* pod index -> its pinned card element */

    function isPinned(i) { return i != null && !!pins[i]; }

    function paint() {
      pods.forEach(function (p, k) {
        var on = (k === hovered) || isPinned(k);
        p.cap.material.emissive.setHex(on ? p.color : 0x000000);
        p.cap.material.emissiveIntensity = on ? 0.55 : 0;
      });
    }

    function setHover(i) {
      if (hovered === i) return;
      hovered = i;
      paint();
    }

    /* A legend that belongs to the pod, not to the page: it is re-anchored
       every frame to wherever that pod currently projects on screen, so it
       rides along while the hive turns. */
    function pin(i) {
      if (pins[i]) return;
      var s = stations[i];
      var hex = "#" + PALETTE[i % PALETTE.length].toString(16).padStart(6, "0");
      var card = document.createElement("div");
      card.className = "lc-bl-pin";
      card.setAttribute("data-pod", i);
      card.innerHTML =
        '<span class="lc-bl-pin-head"><b></b><button type="button" ' +
        'aria-label="Close">×</button></span><span class="lc-bl-pin-body"></span>' +
        '<i class="lc-bl-pin-stem"></i>';
      card.style.setProperty("--pin", hex);
      card.querySelector("b").textContent = s.label;
      card.querySelector(".lc-bl-pin-body").textContent = s.blurb || "—";
      card.querySelector("button").addEventListener("click", function (ev) {
        ev.stopPropagation();
        unpin(i);
      });
      stage.appendChild(card);
      pins[i] = card;
      paint();
      ui.syncChip(i, true);
    }

    function unpin(i) {
      if (!pins[i]) return;
      pins[i].remove();
      delete pins[i];
      paint();
      ui.syncChip(i, false);
    }

    function togglePin(i) {
      if (i == null) return;
      if (pins[i]) unpin(i); else pin(i);
    }

    ui.bind(setHover, togglePin, isPinned);

    /* --- presentation verbs --------------------------------------------
       What an avatar may DO to this loop while it narrates. View state
       only — nothing here touches content, and there is deliberately no
       verb that could (doctrine 5: the tutor never acts). */
    function indexOf(which) {
      if (which == null || which === "") return -1;
      if (typeof which === "number") return (which >= 0 && which < n) ? which : -1;
      var t = String(which).trim().toLowerCase(), i;
      for (i = 0; i < n; i++) if (stations[i].label.toLowerCase() === t) return i;
      for (i = 0; i < n; i++) if (stations[i].label.toLowerCase().indexOf(t) >= 0) return i;
      return -1;
    }

    /* look_at turns the hive so a station faces the viewer. Eased, not
       snapped — a jump cut mid-sentence reads as a glitch. */
    var focus = null;
    function azimuth() {
      return Math.atan2(camera.position.z - controls.target.z,
                        camera.position.x - controls.target.x);
    }
    function setAzimuth(a) {
      var dx = camera.position.x - controls.target.x;
      var dz = camera.position.z - controls.target.z;
      var horiz = Math.sqrt(dx * dx + dz * dz) || 0.01;
      camera.position.x = controls.target.x + Math.cos(a) * horiz;
      camera.position.z = controls.target.z + Math.sin(a) * horiz;
      controls.update();
    }

    var api = {
      stations: function () {
        return stations.map(function (s) { return s.label; });
      },
      pin: function (which) {
        var i = indexOf(which); if (i < 0) return false; pin(i); return true;
      },
      unpin: function (which) {
        if (which == null || which === "") {      /* bare unpin: clear them all */
          var any = false, k;
          for (k in pins) { unpin(+k); any = true; }
          return any;
        }
        var i = indexOf(which);
        if (i < 0 || !pins[i]) return false;
        unpin(i); return true;
      },
      look_at: function (which) {
        var i = indexOf(which); if (i < 0) return false;
        var from = azimuth();
        var d = ((pods[i].angle - from + Math.PI) % (Math.PI * 2) + Math.PI * 2)
                % (Math.PI * 2) - Math.PI;
        focus = { from: from, to: from + d, t: 0, dur: 0.9, resume: controls.autoRotate };
        controls.autoRotate = false;              /* stop fighting the turn */
        return true;
      },
      spin: function (arg) {
        var want = (arg == null || arg === "")
          ? !controls.autoRotate
          : !/^(off|false|stop|no|0)$/i.test(String(arg));
        controls.autoRotate = want;
        if (want) focus = null;
        syncSpin();
        return true;
      },
      recentre: function () {
        focus = null; ui.resetBtn.click(); return true;
      },
      chipFor: function (which) {
        var i = indexOf(which); return i < 0 ? null : ui.chipAt(i);
      }
    };
    ui.expose(api);

    function pick(ev) {
      var r = renderer.domElement.getBoundingClientRect();
      ptr.x = ((ev.clientX - r.left) / r.width) * 2 - 1;
      ptr.y = -((ev.clientY - r.top) / r.height) * 2 + 1;
      ray.setFromCamera(ptr, camera);
      var hits = ray.intersectObjects(rig.children, true);
      for (var i = 0; i < hits.length; i++) {
        var ud = hits[i].object.userData;
        if (ud && ud.podIndex != null) return ud.podIndex;
      }
      return null;
    }

    /* Turning the hive is a drag, pinning is a click — tell them apart by
       how far the pointer travelled, or every orbit would pin something. */
    var downAt = null, downPod = null, dragged = false;

    renderer.domElement.addEventListener("pointermove", function (ev) {
      if (downAt && !dragged &&
          Math.abs(ev.clientX - downAt[0]) + Math.abs(ev.clientY - downAt[1]) > 6) {
        dragged = true;
      }
      var i = pick(ev);
      setHover(i);
      ui.show(i);
      renderer.domElement.style.cursor = i != null ? "pointer" : "";
    });
    renderer.domElement.addEventListener("pointerleave", function () {
      setHover(null); ui.show(null);
    });
    renderer.domElement.addEventListener("pointerdown", function (ev) {
      downAt = [ev.clientX, ev.clientY];
      downPod = pick(ev);
      dragged = false;
    });
    renderer.domElement.addEventListener("pointerup", function (ev) {
      if (!dragged && downPod != null && pick(ev) === downPod) togglePin(downPod);
      downAt = null; downPod = null; dragged = false;
    });

    function syncSpin() {
      ui.spinBtn.textContent = controls.autoRotate ? "⏸ pause spin" : "▶ spin";
    }
    ui.spinBtn.addEventListener("click", function () {
      controls.autoRotate = !controls.autoRotate;
      syncSpin();
    });
    syncSpin();
    ui.resetBtn.addEventListener("click", function () {
      camera.position.set(0, 5.4, 11.0);
      controls.target.set(0, 1.5, 0);
      controls.update();
    });

    /* --- the loop ------------------------------------------------------ */
    var clock = new THREE.Clock();
    var t = 0;
    var TAU = Math.PI * 2;

    function ringPoint(u, out) {
      var a = u * TAU - Math.PI / 2;
      out.set(Math.cos(a) * RING, 0, Math.sin(a) * RING);
      return a;
    }
    var tmp = new THREE.Vector3();

    function frame() {
      raf = requestAnimationFrame(frame);
      var raw = Math.min(0.05, clock.getDelta());
      var dt = raw * opts.speed;
      if (!opts.calm) t += dt;

      /* look_at runs on real time, so a paused or calmed scene still turns
         when the narration asks it to */
      if (focus) {
        focus.t += raw;
        var fk = Math.min(1, focus.t / focus.dur);
        setAzimuth(focus.from + (focus.to - focus.from) * (fk * fk * (3 - 2 * fk)));
        if (fk >= 1) { controls.autoRotate = focus.resume; syncSpin(); focus = null; }
      }

      /* the core turns, breathes, and its halo tips slowly */
      gem.rotation.y = t * 0.5;
      gem.rotation.x = Math.sin(t * 0.35) * 0.25;
      var pulse = 1 + Math.sin(t * 1.4) * 0.05;
      gem.scale.setScalar(pulse);
      halo.rotation.z = t * 0.32;
      halo.scale.setScalar(1 + Math.sin(t * 1.4 + 1) * 0.04);

      /* station tokens bob and turn, each on its own offset */
      pods.forEach(function (p, i) {
        p.token.position.y = p.base + Math.sin(t * 1.1 + i * 1.3) * 0.09;
        p.token.rotation.y = t * 0.6 + i;
        p.token.rotation.x = Math.sin(t * 0.5 + i) * 0.2;
      });

      /* work moves along the ring: a block leaves one pod, arcs over the
         gap, and lands on the next — taking that pod's colour with it */
      blocks.forEach(function (bl) {
        var u = ((t * 0.075) + bl.phase) % 1;
        var leg = u * n;                    /* which gap we are crossing */
        var seg = Math.floor(leg);
        var k = leg - seg;                  /* 0..1 across this gap */
        ringPoint(u, tmp);
        var lift = Math.sin(k * Math.PI) * 0.85;
        bl.mesh.position.set(tmp.x, 0.42 + lift, tmp.z);
        bl.mesh.rotation.set(t * 0.9 + bl.phase * 6, t * 0.7, 0);
        /* colour hands over at the midpoint of the gap: the block is
           changed by the station it just left */
        var fromC = PALETTE[seg % PALETTE.length];
        var toC = PALETTE[(seg + 1) % n % PALETTE.length];
        bl.mesh.material.color.setHex(k < 0.5 ? fromC : toC);
      });

      /* agents walk the ring, bobbing as they go */
      agents.forEach(function (ag, i) {
        var u = ((t * ag.rate) + ag.phase) % 1;
        var a = ringPoint(u, tmp);
        ag.group.position.set(tmp.x, 0.06, tmp.z);
        ag.group.rotation.y = -a + Math.PI / 2;
        ag.body.position.y = 0.35 + Math.abs(Math.sin(t * 4 + i * 2)) * 0.045;
        ag.group.rotation.z = Math.sin(t * 4 + i * 2) * 0.045;
      });

      /* finished apps rise off the core and orbit above it */
      apps.forEach(function (ap, i) {
        var u = ((t * 0.06) + ap.phase) % 1;
        var a = u * TAU;
        var r = 2.2;
        ap.group.position.set(Math.cos(a) * r, 3.45 + Math.sin(t * 0.9 + i * 2) * 0.14, Math.sin(a) * r);
        ap.group.rotation.y = -a + Math.PI / 2;
        ap.screen.material.emissiveIntensity =
          0.45 + Math.sin(t * 2.3 + i * 1.7) * 0.18;
      });

      controls.update();
      renderer.render(scene, camera);
      placePins();
    }
    var raf = requestAnimationFrame(frame);

    /* Re-anchor every pinned card to its pod's current screen position.
       Runs after render, so it uses the matrices the frame was drawn with. */
    var anchor = new THREE.Vector3();
    var camDist = new THREE.Vector3();
    function placePins() {
      var w = stage.clientWidth, hh = stage.clientHeight;
      if (!w || !hh) return;
      var placed = [];
      for (var key in pins) {
        var i = +key, card = pins[key], pod = pods[i];
        pod.group.getWorldPosition(anchor);
        anchor.y += 2.0;                       /* clear of the pod's label */
        camDist.copy(anchor);
        var depth = camDist.distanceTo(camera.position);
        anchor.project(camera);
        if (anchor.z > 1) { card.style.opacity = 0; continue; }  /* behind us */
        var x = (anchor.x * 0.5 + 0.5) * w;
        var y = (-anchor.y * 0.5 + 0.5) * hh;
        placed.push({ card: card, x: x, y: y, depth: depth });
      }

      /* Two stations on the far side project to nearly the same spot and
         their cards land on top of each other. Nearest first, then nudge
         any later card down until it clears the ones already placed. */
      placed.sort(function (a, b) { return a.depth - b.depth; });
      for (var p = 0; p < placed.length; p++) {
        var it = placed[p];
        for (var q = 0; q < p; q++) {
          var o = placed[q];
          if (Math.abs(it.x - o.x) < 180 && Math.abs(it.y - o.y) < 68) {
            it.y = o.y + 68;
          }
        }
        /* keep the card inside the stage — it is clipped otherwise */
        var cx = Math.max(96, Math.min(w - 96, it.x));
        var cy = Math.max(58, Math.min(hh - 12, it.y));
        it.card.style.transform =
          "translate(-50%, -100%) translate(" + cx.toFixed(1) + "px," + cy.toFixed(1) + "px)";
        /* pods on the far side of the hive fade, so the near ones lead */
        var far = it.depth > camera.position.length();
        it.card.style.opacity = far ? 0.55 : 1;
        it.card.style.zIndex = far ? 1 : 2;
      }
    }

    /* --- responsive ---------------------------------------------------- */
    function resize() {
      var w = stage.clientWidth, hh = stage.clientHeight;
      if (!w || !hh) return;
      renderer.setPixelRatio(Math.min(2, window.devicePixelRatio));
      renderer.setSize(w, hh);
      camera.aspect = w / hh;
      /* narrow viewports: pull back so the whole hive still fits */
      controls.maxDistance = w < 560 ? 20 : 17;
      if (w < 560 && camera.position.length() < 11) {
        camera.position.setLength(11.5);
      }
      camera.updateProjectionMatrix();
      controls.update();
    }
    if (window.ResizeObserver) new ResizeObserver(resize).observe(stage);
    window.addEventListener("resize", resize);
    resize();

    /* Stop burning frames when the loop scrolls out of view. */
    if (window.IntersectionObserver) {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting && !raf) raf = requestAnimationFrame(frame);
          else if (!e.isIntersecting && raf) { cancelAnimationFrame(raf); raf = 0; }
        });
      }, { threshold: 0.01 }).observe(stage);
    }
  }

  /* ── boot ────────────────────────────────────────────── */

  /* ── verbs ───────────────────────────────────────────── */
  /* An avatar line says   - do: look_at / with: "AI"   and the hive turns
     while it keeps talking. `at:` scopes to one loop when a page has more
     than one; without it the first loop on the page answers. */
  function loopApi(el) {
    var g = null;
    if (el && el.closest) {
      g = el.closest(".lc-build-loop") ||
          (el.querySelector && el.querySelector(".lc-build-loop"));
    }
    if (!g) g = document.querySelector(".lc-build-loop");
    return (g && g._lcLoopApi) || null;
  }
  /* the avatar walks to the station's chip, so it is standing by the thing
     it is talking about before the verb fires */
  function chipTarget(el, arg) {
    var api = loopApi(el);
    return (api && api.chipFor(arg)) || null;
  }
  if (window.lcVerbs) {
    [["pin", "pin"], ["unpin", "unpin"], ["look_at", "look_at"]].forEach(function (pair) {
      window.lcVerbs.register(pair[0], function (el, arg) {
        var api = loopApi(el);
        return api ? api[pair[1]](arg) : false;
      }, chipTarget);
    });
    window.lcVerbs.register("spin", function (el, arg) {
      var api = loopApi(el); return api ? api.spin(arg) : false;
    });
    window.lcVerbs.register("recentre", function (el) {
      var api = loopApi(el); return api ? api.recentre() : false;
    });
  }

  window.lcRegisterUpgrader &&
    window.lcRegisterUpgrader(".highlighter-rouge.build_loop, pre.build_loop", upgradeBuildLoop);

})();
</script>
