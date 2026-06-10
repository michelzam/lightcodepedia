{%- comment -%}
Scene3D — Three.js interactive 3D object playground.

Usage:
  ```yaml
  lucky:
    colour: Black
    weight_kg: 28
    top_speed_kmh: 40
    adopted: true
  wanda:
    colour: Orange
    weight_kg: 0.03
    top_speed_kmh: 6
    adopted: false
  ```
  {: .scene3d height="440" }

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-scene3d { margin: 1em 0; font-size: 0.92em; }
.lc-s3d-stage { width: 100%; border-radius: 10px; overflow: hidden;
  background: linear-gradient(#bfe3f7, #e8f6e8); position: relative; }
.lc-s3d-stage canvas { display: block; }
.lc-s3d-loading { display: flex; align-items: center; justify-content: center;
  height: 100%; color: #64748b; font-family: monospace; font-size: 0.9em; }
.lc-s3d-panels { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 14px; }
@media (max-width: 760px) { .lc-s3d-panels { grid-template-columns: 1fr; } }
.lc-s3d-card { border: 1px solid #d8dee6; border-radius: 10px; padding: 12px 14px; background: #fff; }
.lc-s3d-card h4 { margin: 0 0 8px; font-size: 1.02em; }
.lc-s3d-row { display: flex; align-items: center; gap: 8px; margin: 5px 0; }
.lc-s3d-row label { width: 130px; color: #475569; font-family: monospace;
  font-size: 0.86em; flex: none; }
.lc-s3d-row input[type=range] { flex: 1; }
.lc-s3d-row select { flex: 1; padding: 2px 6px; border: 1px solid #cbd5e1;
  border-radius: 5px; font-size: 0.9em; }
.lc-s3d-row output { width: 52px; text-align: right; font-family: monospace;
  font-size: 0.84em; color: #0369a1; }
.lc-s3d-methods { display: flex; flex-wrap: wrap; gap: 7px; margin-top: 10px; }
.lc-s3d-methods button { border: none; border-radius: 6px; padding: 5px 12px;
  font-family: monospace; font-size: 0.86em; cursor: pointer;
  background: #0066cc; color: #fff; }
.lc-s3d-methods button:hover { background: #0052a3; }
.lc-s3d-console { margin-top: 14px; background: #0f172a; color: #a5f3fc;
  border-radius: 8px; padding: 10px 14px; font-family: monospace;
  font-size: 0.82em; min-height: 86px; }
.lc-s3d-console div { opacity: 0.55; }
.lc-s3d-console div:last-child { opacity: 1; }
</style>

<script>
(function () {
  if (window._lcScene3dReady) return;
  window._lcScene3dReady = true;

  /* ── library loaders ─────────────────────────────────── */

  var _threeP = null;
  function loadThree() {
    if (_threeP) return _threeP;
    _threeP = Promise.all([
      import("https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js"),
      import("https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/controls/OrbitControls.js")
    ]).then(function (mods) {
      return { THREE: mods[0], OrbitControls: mods[1].OrbitControls };
    });
    return _threeP;
  }

  var _yamlP = null;
  function loadYaml() {
    if (window.jsyaml) return Promise.resolve(window.jsyaml);
    if (_yamlP) return _yamlP;
    _yamlP = new Promise(function (resolve) {
      var s = document.createElement("script");
      s.src = "https://cdn.jsdelivr.net/npm/js-yaml@4/dist/js-yaml.min.js";
      s.onload = function () { resolve(window.jsyaml || null); };
      s.onerror = function () { resolve(null); };
      document.head.appendChild(s);
    });
    return _yamlP;
  }

  /* ── upgrader ────────────────────────────────────────── */

  function upgradeScene3d(el) {
    if (el.dataset.lcScene3dDone) return;
    el.dataset.lcScene3dDone = "1";

    var raw = (el.querySelector("code") || el).textContent.trim();
    var h = parseInt(el.getAttribute("height") || "440", 10);

    var wrap = document.createElement("div");
    wrap.className = "lc-scene3d";
    if (el.id) wrap.id = el.id;
    el.parentNode.replaceChild(wrap, el);

    var stage = document.createElement("div");
    stage.className = "lc-s3d-stage";
    stage.style.height = h + "px";
    stage.innerHTML = '<div class="lc-s3d-loading">⏳ Loading Three.js…</div>';
    wrap.appendChild(stage);

    var panels = document.createElement("div");
    panels.className = "lc-s3d-panels";
    wrap.appendChild(panels);

    var consoleEl = document.createElement("div");
    consoleEl.className = "lc-s3d-console";
    var hint = document.createElement("div");
    hint.textContent = "# edit an attribute or call a method…";
    consoleEl.appendChild(hint);
    wrap.appendChild(consoleEl);

    function log(line) {
      var d = document.createElement("div");
      d.textContent = line;
      consoleEl.appendChild(d);
      while (consoleEl.children.length > 6) consoleEl.removeChild(consoleEl.firstChild);
    }

    Promise.all([loadThree(), loadYaml()]).then(function (results) {
      var libs = results[0];
      var jsyaml = results[1];
      var THREE = libs.THREE;
      var OrbitControls = libs.OrbitControls;

      var cfg = {};
      try { cfg = (jsyaml ? jsyaml.load(raw) : JSON.parse(raw)) || {}; } catch (e) {}
      var LA = cfg.lucky || {};
      var WA = cfg.wanda || {};

      /* build attribute panels (before scene — no async needed) */
      var lPanel = buildDogPanel(LA, log);
      var wPanel = buildFishPanel(WA, log);
      panels.appendChild(lPanel.el);
      panels.appendChild(wPanel.el);

      /* Three.js scene */
      stage.innerHTML = "";
      var scene = new THREE.Scene();
      var camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
      camera.position.set(0, 4.2, 9.5);
      var renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
      renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
      stage.appendChild(renderer.domElement);
      var controls = new OrbitControls(camera, renderer.domElement);
      controls.target.set(0, 0.8, 0);
      controls.maxPolarAngle = Math.PI * 0.49;
      controls.enableDamping = true;

      function resize() {
        var w = stage.clientWidth;
        renderer.setSize(w, h);
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
      }
      window.addEventListener("resize", resize);

      scene.add(new THREE.AmbientLight(0xffffff, 0.75));
      var sun = new THREE.DirectionalLight(0xfff4e0, 1.2);
      sun.position.set(4, 8, 6);
      scene.add(sun);

      var grass = new THREE.Mesh(
        new THREE.CylinderGeometry(9, 9, 0.3, 40),
        new THREE.MeshLambertMaterial({ color: 0x8fcf7a }));
      grass.position.y = -0.15;
      scene.add(grass);

      /* build 3D models */
      var L3 = makeDog(THREE, LA);
      L3.group.position.set(-2.6, 0, 0);
      L3.group.rotation.y = 0.5;
      scene.add(L3.group);

      var W3 = makeFish(THREE, WA);
      W3.root.position.set(2.8, 0, 0);
      scene.add(W3.root);

      /* live state */
      var L = { weight: +(LA.weight_kg || 28), speed: +(LA.top_speed_kmh || 40),
                adopted: !!LA.adopted, state: "idle", t: 0, angle: 0 };
      var W = { weight: +(WA.weight_kg || 0.03), speed: +(WA.top_speed_kmh || 6),
                adopted: !!WA.adopted, boost: 0, angle: 0 };
      var bubbles = [];
      var woof = { mesh: null, t: 0 };

      function dogScale() { L3.group.scale.setScalar(0.55 + L.weight / 55); }
      function fishScale() { W3.fish.scale.setScalar(0.8 + W.weight * 1.6); }
      dogScale(); fishScale();
      L3.collar.visible = L.adopted;
      W3.castle.visible = W.adopted;

      /* wire Lucky panel */
      lPanel.onColour  = function (hex, name) { L3.mat.color.set(hex); log('lucky.colour = "' + name + '"'); };
      lPanel.onWeight  = function (v) { L.weight = v; dogScale(); log("lucky.weight_kg = " + v); };
      lPanel.onSpeed   = function (v) { L.speed = v;  log("lucky.top_speed_kmh = " + v); };
      lPanel.onAdopted = function (v) { L.adopted = v; L3.collar.visible = v; log("lucky.adopted = " + v); };
      lPanel.onBark    = function () {
        L.state = "bark"; L.t = 0;
        var c = document.createElement("canvas"); c.width = 256; c.height = 96;
        var ctx = c.getContext("2d");
        ctx.font = "bold 56px sans-serif"; ctx.strokeStyle = "#fff"; ctx.lineWidth = 8;
        ctx.strokeText("Woof!", 30, 62); ctx.fillStyle = "#1e293b"; ctx.fillText("Woof!", 30, 62);
        var sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(c), transparent: true }));
        sp.scale.set(1.8, 0.7, 1);
        sp.position.copy(L3.group.position).add(new THREE.Vector3(1.4, 2.6, 0));
        if (woof.mesh) scene.remove(woof.mesh);
        scene.add(sp); woof.mesh = sp; woof.t = 0;
        log('lucky.bark()  → "Woof! Woof!"');
      };
      lPanel.onRun  = function () { L.state = "run"; L.t = 0; log("lucky.run()  # speed = " + L.speed + " km/h"); };
      lPanel.onWag  = function () { L.state = "wag"; L.t = 0; log("lucky.wag_tail()"); };

      /* wire Wanda panel */
      wPanel.onColour  = function (hex, name) { W3.mat.color.set(hex); log('wanda.colour = "' + name + '"'); };
      wPanel.onWeight  = function (v) { W.weight = v; fishScale(); log("wanda.weight_kg = " + v); };
      wPanel.onSpeed   = function (v) { W.speed = v;  log("wanda.top_speed_kmh = " + v); };
      wPanel.onAdopted = function (v) { W.adopted = v; W3.castle.visible = v; log("wanda.adopted = " + v); };
      wPanel.onSwim    = function () { W.boost = 3; log("wanda.swim()  # speed = " + W.speed + " km/h"); };
      wPanel.onBubble  = function () {
        for (var i = 0; i < 5; i++) {
          var b = new THREE.Mesh(
            new THREE.SphereGeometry(0.035 + Math.random() * 0.04, 8, 8),
            new THREE.MeshLambertMaterial({ color: 0xe8faff, transparent: true, opacity: 0.75 }));
          b.position.copy(W3.root.position)
            .add(new THREE.Vector3(W3.fish.position.x + 0.4, 1.35, W3.fish.position.z));
          b.userData.v = 0.4 + Math.random() * 0.5;
          b.userData.x = (Math.random() - 0.5) * 0.3;
          scene.add(b); bubbles.push(b);
        }
        log("wanda.blow_bubble()");
      };

      /* animation loop */
      var clock = new THREE.Clock();
      var animId;
      function tick() {
        animId = requestAnimationFrame(tick);
        var dt = Math.min(clock.getDelta(), 0.05);
        var t = clock.elapsedTime;

        if (L.state === "run") {
          L.t += dt;
          var w = L.speed / 14;
          L.angle += w * dt;
          L3.group.position.set(-2.6 + Math.sin(L.angle) * 1.55, 0, Math.cos(L.angle) * 1.7);
          L3.group.rotation.y = L.angle + Math.PI / 2;
          L3.legs.forEach(function (leg, i) { leg.rotation.x = Math.sin(t * w * 6 + i * Math.PI) * 0.7; });
          L3.tail.rotation.y = Math.sin(t * 14) * 0.4;
          if (L.t > 4.5) { L.state = "idle"; L3.legs.forEach(function (l) { l.rotation.x = 0; }); }
        } else if (L.state === "bark") {
          L.t += dt;
          L3.head.rotation.z = Math.sin(L.t * 22) * 0.16;
          if (L.t > 1.1) { L.state = "idle"; L3.head.rotation.z = 0; }
        } else if (L.state === "wag") {
          L.t += dt;
          L3.tail.rotation.y = Math.sin(L.t * 18) * 0.9;
          if (L.t > 2) { L.state = "idle"; L3.tail.rotation.y = 0; }
        } else {
          L3.group.position.y = Math.sin(t * 1.6) * 0.02;
          L3.tail.rotation.y = Math.sin(t * 3) * 0.18;
        }

        if (woof.mesh) {
          woof.t += dt;
          woof.mesh.position.y += dt * 0.9;
          woof.mesh.material.opacity = Math.max(0, 1 - woof.t);
          if (woof.t > 1) { scene.remove(woof.mesh); woof.mesh = null; }
        }

        var boost = W.boost > 0 ? 2.2 : 1;
        if (W.boost > 0) W.boost -= dt;
        W.angle += dt * (0.4 + W.speed / 12) * boost;
        W3.fish.position.set(Math.cos(W.angle) * 0.78, 1.3 + Math.sin(t * 2) * 0.07, Math.sin(W.angle) * 0.55);
        W3.fish.rotation.y = -W.angle + Math.PI;
        W3.tail.rotation.y = Math.sin(t * 10 * boost) * 0.5;

        for (var i = bubbles.length - 1; i >= 0; i--) {
          var b = bubbles[i];
          b.position.y += b.userData.v * dt;
          b.position.x += b.userData.x * dt;
          if (b.position.y > 2.65) { scene.remove(b); bubbles.splice(i, 1); }
        }

        controls.update();
        renderer.render(scene, camera);
      }

      resize();
      tick();

    }).catch(function (e) {
      stage.innerHTML = '<p style="padding:1em;color:#b00;">⚠ Could not load scene: ' + (e && e.message || e) + '</p>';
    });
  }

  /* ── 3D model builders ───────────────────────────────── */

  var DOG_COLOURS = { Black: 0x1a1a1a, Brown: 0x8b5a2b, Golden: 0xd4a24e, White: 0xece8e1, Grey: 0x7a7d82 };
  var FISH_COLOURS = { Orange: 0xe67e22, Gold: 0xf1c40f, Red: 0xe74c3c, Blue: 0x3498db, White: 0xecf0f1 };

  function makeDog(THREE, attrs) {
    var g = new THREE.Group();
    var mat  = new THREE.MeshLambertMaterial({ color: DOG_COLOURS[attrs.colour] || 0x1a1a1a });
    var dark = new THREE.MeshLambertMaterial({ color: 0x0c0c0c });

    var body = new THREE.Mesh(new THREE.BoxGeometry(1.9, 0.9, 0.85), mat);
    body.position.y = 1.0; g.add(body);
    var head = new THREE.Mesh(new THREE.BoxGeometry(0.75, 0.7, 0.7), mat);
    head.position.set(1.15, 1.55, 0); g.add(head);
    var snout = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.3, 0.4), mat);
    snout.position.set(1.62, 1.42, 0); g.add(snout);
    var nose = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.12, 0.18), dark);
    nose.position.set(1.84, 1.46, 0); g.add(nose);
    [-1, 1].forEach(function (s) {
      var ear = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.42, 0.22), dark);
      ear.position.set(1.0, 1.98, 0.24 * s); ear.rotation.x = 0.15 * s; g.add(ear);
      var eye = new THREE.Mesh(new THREE.SphereGeometry(0.055), dark);
      eye.position.set(1.5, 1.66, 0.2 * s); g.add(eye);
    });
    var legs = [];
    [[-0.7, 0.3], [-0.7, -0.3], [0.65, 0.3], [0.65, -0.3]].forEach(function (xz) {
      var leg = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.75, 0.22), mat);
      leg.position.set(xz[0], 0.38, xz[1]); g.add(leg); legs.push(leg);
    });
    var tail = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.14, 0.14), mat);
    tail.geometry.translate(-0.27, 0, 0);
    tail.position.set(-0.95, 1.25, 0); tail.rotation.z = 0.55; g.add(tail);
    var collar = new THREE.Mesh(
      new THREE.TorusGeometry(0.42, 0.06, 8, 20),
      new THREE.MeshLambertMaterial({ color: 0xd62828 }));
    collar.position.set(0.95, 1.25, 0); collar.rotation.y = Math.PI / 2; g.add(collar);
    return { group: g, mat: mat, legs: legs, tail: tail, collar: collar, head: head };
  }

  function makeFish(THREE, attrs) {
    var root = new THREE.Group();
    var bowl = new THREE.Mesh(
      new THREE.SphereGeometry(1.5, 28, 20, 0, Math.PI * 2, 0.5),
      new THREE.MeshPhysicalMaterial({ color: 0xbfe8ff, transparent: true, opacity: 0.28, side: THREE.DoubleSide }));
    bowl.position.y = 1.45; root.add(bowl);
    var water = new THREE.Mesh(
      new THREE.SphereGeometry(1.38, 24, 16),
      new THREE.MeshLambertMaterial({ color: 0x7eccee, transparent: true, opacity: 0.35 }));
    water.scale.y = 0.72; water.position.y = 1.25; root.add(water);

    var g = new THREE.Group();
    var mat = new THREE.MeshLambertMaterial({ color: FISH_COLOURS[attrs.colour] || 0xe67e22 });
    var fbody = new THREE.Mesh(new THREE.SphereGeometry(0.34, 18, 14), mat);
    fbody.scale.set(1.35, 1, 0.7); g.add(fbody);
    var tail = new THREE.Mesh(new THREE.ConeGeometry(0.22, 0.4, 4), mat);
    tail.rotation.z = Math.PI / 2; tail.position.x = -0.55; g.add(tail);
    var fin = new THREE.Mesh(new THREE.ConeGeometry(0.12, 0.25, 4), mat);
    fin.position.set(0, 0.36, 0); g.add(fin);
    var eyeM = new THREE.MeshLambertMaterial({ color: 0x111111 });
    [-1, 1].forEach(function (s) {
      var eye = new THREE.Mesh(new THREE.SphereGeometry(0.045), eyeM);
      eye.position.set(0.3, 0.07, 0.21 * s); g.add(eye);
    });
    g.position.y = 1.35; root.add(g);

    var castle = new THREE.Group();
    var cMat = new THREE.MeshLambertMaterial({ color: 0xc9b18a });
    castle.add(new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.26, 0.5, 10), cMat));
    var roof = new THREE.Mesh(new THREE.ConeGeometry(0.26, 0.3, 10),
      new THREE.MeshLambertMaterial({ color: 0x9a6fb0 }));
    roof.position.y = 0.4; castle.add(roof);
    castle.position.set(0.5, 0.42, -0.4); castle.visible = false; root.add(castle);
    return { root: root, fish: g, mat: mat, tail: tail, castle: castle };
  }

  /* ── attribute panel DOM builders ───────────────────── */

  function buildDogPanel(attrs, log) {
    var h = {};
    var el = document.createElement("div");
    el.className = "lc-s3d-card";
    el.appendChild(makeH4("🐕 lucky : Dog"));
    el.appendChild(makeSelect("colour",
      [["#1a1a1a","Black"],["#8b5a2b","Brown"],["#d4a24e","Golden"],["#ece8e1","White"],["#7a7d82","Grey"]],
      attrs.colour || "Black",
      function (hex, name) { if (h.onColour) h.onColour(hex, name); }));
    el.appendChild(makeRange("weight_kg",    8, 60,  1,    +(attrs.weight_kg      || 28),   function (v) { if (h.onWeight)  h.onWeight(v); }));
    el.appendChild(makeRange("top_speed_kmh", 10, 75, 1,    +(attrs.top_speed_kmh || 40),   function (v) { if (h.onSpeed)   h.onSpeed(v); }));
    el.appendChild(makeCheck("adopted", !!attrs.adopted, "(adopted dogs wear a red collar)", function (v) { if (h.onAdopted) h.onAdopted(v); }));
    el.appendChild(makeMethods(["bark()", "run()", "wag_tail()"],
      [function () { if (h.onBark) h.onBark(); },
       function () { if (h.onRun)  h.onRun();  },
       function () { if (h.onWag)  h.onWag();  }]));
    return Object.assign(h, { el: el });
  }

  function buildFishPanel(attrs, log) {
    var h = {};
    var el = document.createElement("div");
    el.className = "lc-s3d-card";
    el.appendChild(makeH4("🐠 wanda : Fish"));
    el.appendChild(makeSelect("colour",
      [["#e67e22","Orange"],["#f1c40f","Gold"],["#e74c3c","Red"],["#3498db","Blue"],["#ecf0f1","White"]],
      attrs.colour || "Orange",
      function (hex, name) { if (h.onColour) h.onColour(hex, name); }));
    el.appendChild(makeRange("weight_kg",    0.01, 0.5,  0.01, +(attrs.weight_kg      || 0.03), function (v) { if (h.onWeight)  h.onWeight(v); }));
    el.appendChild(makeRange("top_speed_kmh",   1,  15,  1,    +(attrs.top_speed_kmh || 6),     function (v) { if (h.onSpeed)   h.onSpeed(v); }));
    el.appendChild(makeCheck("adopted", !!attrs.adopted, "(adopted fish get a castle)",           function (v) { if (h.onAdopted) h.onAdopted(v); }));
    el.appendChild(makeMethods(["swim()", "blow_bubble()"],
      [function () { if (h.onSwim)   h.onSwim();   },
       function () { if (h.onBubble) h.onBubble(); }]));
    return Object.assign(h, { el: el });
  }

  function makeH4(text) {
    var h4 = document.createElement("h4");
    h4.textContent = text;
    return h4;
  }

  function makeSelect(label, pairs, initName, onChange) {
    var row = document.createElement("div");
    row.className = "lc-s3d-row";
    var lbl = document.createElement("label"); lbl.textContent = label;
    var sel = document.createElement("select");
    pairs.forEach(function (p) {
      var opt = document.createElement("option");
      opt.value = p[0]; opt.textContent = p[1];
      if (p[1] === initName) opt.selected = true;
      sel.appendChild(opt);
    });
    sel.addEventListener("change", function () {
      var o = sel.options[sel.selectedIndex];
      onChange(o.value, o.textContent);
    });
    row.appendChild(lbl); row.appendChild(sel);
    return row;
  }

  function makeRange(label, min, max, step, init, onChange) {
    var row = document.createElement("div");
    row.className = "lc-s3d-row";
    var lbl = document.createElement("label"); lbl.textContent = label;
    var inp = document.createElement("input");
    inp.type = "range"; inp.min = min; inp.max = max; inp.step = step; inp.value = init;
    var out = document.createElement("output"); out.textContent = init;
    inp.addEventListener("input", function () {
      var v = parseFloat(inp.value); out.textContent = v; onChange(v);
    });
    row.appendChild(lbl); row.appendChild(inp); row.appendChild(out);
    return row;
  }

  function makeCheck(label, init, hint, onChange) {
    var row = document.createElement("div");
    row.className = "lc-s3d-row";
    var lbl = document.createElement("label"); lbl.textContent = label;
    var cb = document.createElement("input"); cb.type = "checkbox"; cb.checked = init;
    var span = document.createElement("span");
    span.style.cssText = "font-size:0.8em;color:#64748b"; span.textContent = hint;
    cb.addEventListener("change", function () { onChange(cb.checked); });
    row.appendChild(lbl); row.appendChild(cb); row.appendChild(span);
    return row;
  }

  function makeMethods(labels, handlers) {
    var wrap = document.createElement("div");
    wrap.className = "lc-s3d-methods";
    labels.forEach(function (lbl, i) {
      var btn = document.createElement("button");
      btn.textContent = lbl;
      btn.addEventListener("click", handlers[i]);
      wrap.appendChild(btn);
    });
    return wrap;
  }

  /* ── boot ────────────────────────────────────────────── */

  function init(root) {
    (root || document).querySelectorAll(".highlighter-rouge.scene3d, pre.scene3d").forEach(upgradeScene3d);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", function () { init(); });
  else init();

  var _os = window.lcScanElement;
  window.lcScanElement = function (root) {
    if (_os) _os(root);
    (root || document).querySelectorAll(".highlighter-rouge.scene3d, pre.scene3d").forEach(upgradeScene3d);
  };

})();
</script>
