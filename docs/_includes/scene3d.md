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

/* ── quest mode (goal="adopt_wanda") ─────────────────── */
.lc-s3d-goal { display: flex; flex-wrap: wrap; align-items: baseline; gap: 6px 10px;
  margin: 0 0 12px; padding: 11px 15px; border-radius: 10px;
  background: #fff7ed; border: 1px solid #fed7aa; color: #7c2d12;
  font-size: 0.98em; line-height: 1.45; }
.lc-s3d-goal code { background: #ffedd5; padding: 1px 6px; border-radius: 4px;
  font-size: 0.92em; color: #9a3412; }
.lc-s3d-goal-hint { color: #9a6a3c; font-size: 0.88em; }
.lc-s3d-row input[type=checkbox]:disabled { cursor: not-allowed; opacity: 0.5; }
.lc-s3d-chips { display: flex; flex-wrap: wrap; gap: 5px; margin: 8px 0 9px; align-items: center; }
.lc-s3d-chips::before { content: "state:"; font-size: 0.72em; color: #94a3b8; margin-right: 2px; }
.lc-s3d-chip { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.74em;
  padding: 2px 9px; border-radius: 999px; background: #e5e7eb; color: #6b7280; letter-spacing: 0.02em; }
.lc-s3d-chip.active { background: #dc2626; color: #fff; font-weight: 600; box-shadow: 0 0 0 2px rgba(220,38,38,0.18); }
.lc-s3d-methods button:disabled { background: #cbd5e1; color: #eef2f7; cursor: not-allowed; box-shadow: none; }
.lc-s3d-goal.lc-s3d-goal-done { background: #ecfdf5; border-color: #a7f3d0; color: #065f46; }
.lc-s3d-goal.lc-s3d-goal-done code { background: #d1fae5; color: #047857; }
.lc-s3d-win { display: none; margin-top: 14px; padding: 14px 18px; border-radius: 10px;
  background: linear-gradient(90deg, #dcfce7, #f0fdf4); border: 1px solid #86efac;
  color: #14532d; font-size: 1.18em; font-weight: 600; line-height: 1.4;
  animation: lc-s3d-pop 0.4s ease; }
.lc-s3d-win.lc-s3d-win-show { display: block; }
.lc-s3d-win .lc-s3d-win-sub { display: block; margin-top: 3px; font-size: 0.72em;
  font-weight: 500; color: #15803d; }
.lc-s3d-win code { background: #bbf7d0; padding: 1px 6px; border-radius: 4px; color: #166534; }
@keyframes lc-s3d-pop { 0% { transform: scale(0.96); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }

/* ── code trail (trail="true") ───────────────────────── */
.lc-s3d-trail { margin-top: 14px; border: 1px solid #1e293b; border-radius: 8px; overflow: hidden; }
.lc-s3d-trail-head { background: #1e293b; color: #e2e8f0; padding: 7px 14px;
  font-family: monospace; font-size: 0.8em; letter-spacing: 0.02em; }
.lc-s3d-trail-body { background: #0b1220; color: #7dd3fc; padding: 10px 14px;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.82em;
  line-height: 1.55; max-height: 190px; overflow-y: auto; white-space: pre-wrap; }
.lc-s3d-trail-body:empty::before { content: "# nothing yet — start experimenting…"; color: #475569; }
.lc-s3d-trail-body div { animation: lc-s3d-fadein 0.25s ease; }
.lc-s3d-trail-body .lc-s3d-trail-cmt { color: #94a3b8; font-style: italic; }
@keyframes lc-s3d-fadein { from { opacity: 0; transform: translateY(2px); } to { opacity: 1; transform: none; } }

</style>

<!-- The Three.js import map lives in _layouts/default.html <head>: an import
     map parsed after another include's module script starts loading throws a
     console error on every page. -->

<script>
(function () {
  if (window._lcScene3dReady) return;
  window._lcScene3dReady = true;

  /* ── library loaders ─────────────────────────────────── */

  var _threeP = null;
  function loadThree() {
    if (_threeP) return _threeP;
    /* OrbitControls imports the bare specifier "three" internally,
       resolved by the importmap above. */
    _threeP = Promise.all([
      import("three"),
      import("three/addons/controls/OrbitControls.js")
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
    /* optional quest layer — gated knobs, off for the plain playground */
    var quest = (el.getAttribute("goal") || "").trim() === "adopt_wanda";
    var wantTrail = el.hasAttribute("trail") && el.getAttribute("trail") !== "false";
    var trailBody = null;   /* assigned below; log() feeds it when present */
    /* console (the generated-code log): on for the plain playground, off for
       the quest unless explicitly forced with console="true" */
    var consoleAttr = el.getAttribute("console");
    var consoleOn = consoleAttr != null ? (consoleAttr !== "false") : !quest;

    var wrap = document.createElement("div");
    wrap.className = "lc-scene3d";
    if (el.id) { wrap.id = el.id; wrap.setAttribute("data-lc-id", el.id); }
    wrap.setAttribute("height", h);
    el.parentNode.replaceChild(wrap, el);

    var goalEl = null, winEl = null;
    if (quest) {
      goalEl = document.createElement("div");
      goalEl.className = "lc-s3d-goal";
      goalEl.innerHTML =
        '🎯 <b>Challenge — adopt Wanda:</b> get <code>wanda.adopted → True</code>.' +
        '<span class="lc-s3d-goal-hint">The checkbox is locked — only a <b>behaviour</b> can flip it.' +
        ' And dogs and fish don’t share a language: only Lucky can reach Wanda. Find the sequence.</span>';
      wrap.appendChild(goalEl);
    }

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
    hint.textContent = quest
      ? "# experiment — find out how to get Wanda adopted…"
      : "# edit an attribute or call a method…";
    consoleEl.appendChild(hint);
    wrap.appendChild(consoleEl);
    if (!consoleOn) consoleEl.style.display = "none";   /* hide the generated code */

    /* success banner (quest mode) */
    if (quest) {
      winEl = document.createElement("div");
      winEl.className = "lc-s3d-win";
      winEl.innerHTML = '🎉 <b>Wanda adopted!</b> She’s home at the castle.' +
        '<span class="lc-s3d-win-sub">goal reached — <code>wanda.adopted == True</code></span>';
      wrap.appendChild(winEl);
    }

    /* code trail (uncapped record of the whole journey) */
    if (wantTrail) {
      var trailEl = document.createElement("div");
      trailEl.className = "lc-s3d-trail";
      var trailHead = document.createElement("div");
      trailHead.className = "lc-s3d-trail-head";
      trailHead.textContent = "🧭 Code trail — every click, as code";
      trailBody = document.createElement("div");
      trailBody.className = "lc-s3d-trail-body";
      trailEl.appendChild(trailHead);
      trailEl.appendChild(trailBody);
      wrap.appendChild(trailEl);
    }

    function log(line) {
      var d = document.createElement("div");
      d.textContent = line;
      consoleEl.appendChild(d);
      while (consoleEl.children.length > 6) consoleEl.removeChild(consoleEl.firstChild);
      if (trailBody) {
        var t = document.createElement("div");
        t.textContent = line;
        if (line.charAt(0) === "#") t.className = "lc-s3d-trail-cmt";
        trailBody.appendChild(t);
        trailBody.scrollTop = trailBody.scrollHeight;
      }
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
      var lPanel = buildDogPanel(LA, log, quest);
      var wPanel = buildFishPanel(WA, log, quest);
      panels.appendChild(lPanel.el);
      panels.appendChild(wPanel.el);
      /* challenge mode: adoption is a consequence of behaviour, not a flag you
         tick — lock the checkboxes so only the method sequence can win */
      if (quest) {
        if (lPanel.disableAdopted) lPanel.disableAdopted();
        if (wPanel.disableAdopted) wPanel.disableAdopted();
      }

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
        if (!w) return;   /* hidden (slide / tab not active yet) — wait for it to show */
        renderer.setSize(w, h);
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
      }
      window.addEventListener("resize", resize);
      /* a second instance can boot inside a hidden slide (clientWidth 0); resize
         the moment the stage gains real width — e.g. its slide becomes active */
      if (window.ResizeObserver) {
        try { new ResizeObserver(function () { resize(); }).observe(stage); } catch (e) {}
      }

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
                adopted: !!LA.adopted, state: "idle", t: 0, angle: 0, grow: 1 };
      var W = { weight: +(WA.weight_kg || 0.03), speed: +(WA.top_speed_kmh || 6),
                adopted: !!WA.adopted, boost: 0, angle: 0 };
      var bubbles = [];
      var woof = { mesh: null, t: 0 };

      /* ── quest state machine (only live when goal="adopt_wanda") ── */
      var solved = false;
      function showWin() {
        if (solved) return;
        solved = true;
        if (winEl)  winEl.classList.add("lc-s3d-win-show");
        if (goalEl) goalEl.classList.add("lc-s3d-goal-done");
      }

      function dogScale() { L3.group.scale.setScalar((0.55 + L.weight / 55) * L.grow); }
      function fishScale() { W3.fish.scale.setScalar(0.8 + W.weight * 1.6); }
      dogScale(); fishScale();
      L3.collar.visible = L.adopted;
      W3.castle.visible = W.adopted;

      /* shared visual actions (playground and quest both use these) */
      function barkSprite() {
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
      }
      function spawnBubbles() {
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
      }

      /* attribute handlers — shared by both modes */
      lPanel.onColour = function (hex, name) { L3.mat.color.set(hex); log('lucky.colour = "' + name + '"'); };
      lPanel.onWeight = function (v) { L.weight = v; dogScale(); log("lucky.weight_kg = " + v); };
      lPanel.onSpeed  = function (v) { L.speed = v;  log("lucky.top_speed_kmh = " + v); };
      lPanel.onAdopted = function (v) { L.adopted = v; L3.collar.visible = v; log("lucky.adopted = " + v); };
      wPanel.onColour = function (hex, name) { W3.mat.color.set(hex); log('wanda.colour = "' + name + '"'); };
      wPanel.onWeight = function (v) { W.weight = v; fishScale(); log("wanda.weight_kg = " + v); };
      wPanel.onSpeed  = function (v) { W.speed = v;  log("wanda.top_speed_kmh = " + v); };

      if (quest) {
        /* Each pet is a tiny state machine; a behaviour only fires in the
           right state, and behaviours drive the next transition:
             lucky.eat()          hungry → fed (grows); Wanda bored → curious
             wanda.blow_bubble()  curious → ready
             lucky.bark()         fed + Wanda ready → adopted (castle appears)
           The order is the algorithm the learner discovers — and only Lucky
           can reach Wanda. */
        var sm = { lucky: "hungry", wanda: "bored" };
        function syncChips() {
          if (lPanel.chips) lPanel.chips.set(sm.lucky);
          if (wPanel.chips) wPanel.chips.set(sm.wanda);
        }
        function gate(btn, on) { if (btn) btn.disabled = !on; }
        function refreshGates() {
          var lb = lPanel.methodBtns || {}, wb = wPanel.methodBtns || {};
          gate(lb.eat,         sm.lucky === "hungry" && !solved);
          gate(lb.bark,        sm.lucky === "fed"    && !solved);
          gate(wb.blow_bubble, sm.wanda === "curious" && !solved);
        }
        lPanel.onEat = function () {
          if (sm.lucky !== "hungry") return;
          sm.lucky = "fed"; L.grow = 1.35; dogScale();
          log("lucky.eat()   # 🍖 fed — Lucky grows");
          if (sm.wanda === "bored") { sm.wanda = "curious"; log("# 🐠 Lucky perks up — Wanda: bored → curious"); }
          syncChips(); refreshGates();
        };
        lPanel.onBark = function () {
          barkSprite();
          log('lucky.bark()  → "Woof!"');
          if (sm.lucky === "fed" && sm.wanda === "ready") {
            sm.wanda = "adopted";
            log("# 📣 only Lucky can reach Wanda — his bark calls her home");
            log("wanda.adopted = True   # 🏰 adopted!");
            W.adopted = true; W3.castle.visible = true;
            if (wPanel.setAdopted) wPanel.setAdopted(true);
            showWin();
          }
          syncChips(); refreshGates();
        };
        lPanel.onRun = function () { L.state = "run"; L.t = 0; log("lucky.run()   # exploring…"); };
        lPanel.onWag = function () { L.state = "wag"; L.t = 0; log("lucky.wag_tail()   # exploring…"); };
        wPanel.onBubble = function () {
          spawnBubbles();
          log("wanda.blow_bubble()");
          if (sm.wanda === "curious") { sm.wanda = "ready"; log("# 🫧 a bubble! Wanda: curious → ready"); }
          syncChips(); refreshGates();
        };
        wPanel.onSwim = function () { W.boost = 3; log("wanda.swim()   # exploring…"); };
        syncChips(); refreshGates();
      } else {
        /* plain playground — every behaviour fires directly */
        lPanel.onBark = function () { barkSprite(); log('lucky.bark()  → "Woof! Woof!"'); };
        lPanel.onRun  = function () { L.state = "run"; L.t = 0; log("lucky.run()  # speed = " + L.speed + " km/h"); };
        lPanel.onWag  = function () { L.state = "wag"; L.t = 0; log("lucky.wag_tail()"); };
        wPanel.onAdopted = function (v) { W.adopted = v; W3.castle.visible = v; log("wanda.adopted = " + v); };
        wPanel.onSwim    = function () { W.boost = 3; log("wanda.swim()  # speed = " + W.speed + " km/h"); };
        wPanel.onBubble  = function () { spawnBubbles(); log("wanda.blow_bubble()"); };
      }

      /* animation loop */
      var clock = new THREE.Clock();
      var animId;
      function tick() {
        animId = requestAnimationFrame(tick);
        var dt = Math.min(clock.getDelta(), 0.05);
        if (!stage.clientWidth) return;   /* hidden slide — keep the loop alive, skip rendering */
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

        if (quest && solved) {
          /* adopted — glide to the castle and settle there with a gentle bob */
          var tgS = W3.castle.position;           /* local (0.5, 0.42, -0.4) */
          var fpS = W3.fish.position;
          var kS = Math.min(1, dt * 1.8);
          fpS.x += (tgS.x - fpS.x) * kS;
          fpS.z += (tgS.z - fpS.z) * kS;
          fpS.y += ((tgS.y + 0.55 + Math.sin(t * 2) * 0.04) - fpS.y) * kS;
          W3.fish.rotation.y += dt * 0.6;
          W3.tail.rotation.y = Math.sin(t * 8) * 0.4;
        } else {
          var boost = W.boost > 0 ? 2.2 : 1;
          if (W.boost > 0) W.boost -= dt;
          W.angle += dt * (0.4 + W.speed / 12) * boost;
          W3.fish.position.set(Math.cos(W.angle) * 0.78, 1.3 + Math.sin(t * 2) * 0.07, Math.sin(W.angle) * 0.55);
          W3.fish.rotation.y = -W.angle + Math.PI;
          W3.tail.rotation.y = Math.sin(t * 10 * boost) * 0.5;
        }

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

  function buildDogPanel(attrs, log, quest) {
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
    var adoptedRowD = makeCheck("adopted", !!attrs.adopted, "(adopted dogs wear a red collar)", function (v) { if (h.onAdopted) h.onAdopted(v); });
    el.appendChild(adoptedRowD);
    h.disableAdopted = function () { var cb = adoptedRowD.querySelector("input[type=checkbox]"); if (cb) { cb.disabled = true; cb.title = "locked — only a behaviour can change this"; } };
    if (quest) {
      h.chips = makeChips(["hungry", "fed"]);
      el.appendChild(h.chips.el);
      var mWd = makeMethods(["eat()", "bark()", "run()", "wag_tail()"],
        [function () { if (h.onEat)  h.onEat();  },
         function () { if (h.onBark) h.onBark(); },
         function () { if (h.onRun)  h.onRun();  },
         function () { if (h.onWag)  h.onWag();  }]);
      el.appendChild(mWd); h.methodBtns = mWd._byLabel;
    } else {
      el.appendChild(makeMethods(["bark()", "run()", "wag_tail()"],
        [function () { if (h.onBark) h.onBark(); },
         function () { if (h.onRun)  h.onRun();  },
         function () { if (h.onWag)  h.onWag();  }]));
    }
    return Object.assign(h, { el: el });
  }

  function buildFishPanel(attrs, log, quest) {
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
    var adoptedRow = makeCheck("adopted", !!attrs.adopted, "(adopted fish get a castle)",        function (v) { if (h.onAdopted) h.onAdopted(v); });
    el.appendChild(adoptedRow);
    h.setAdopted = function (v) { var cb = adoptedRow.querySelector("input[type=checkbox]"); if (cb) cb.checked = v; };
    h.disableAdopted = function () { var cb = adoptedRow.querySelector("input[type=checkbox]"); if (cb) { cb.disabled = true; cb.title = "locked — only a behaviour can change this"; } };
    if (quest) {
      h.chips = makeChips(["bored", "curious", "ready", "adopted"]);
      el.appendChild(h.chips.el);
      var mWf = makeMethods(["blow_bubble()", "swim()"],
        [function () { if (h.onBubble) h.onBubble(); },
         function () { if (h.onSwim)   h.onSwim();   }]);
      el.appendChild(mWf); h.methodBtns = mWf._byLabel;
    } else {
      el.appendChild(makeMethods(["swim()", "blow_bubble()"],
        [function () { if (h.onSwim)   h.onSwim();   },
         function () { if (h.onBubble) h.onBubble(); }]));
    }
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
    wrap._byLabel = {};
    labels.forEach(function (lbl, i) {
      var btn = document.createElement("button");
      btn.textContent = lbl;
      btn.addEventListener("click", handlers[i]);
      wrap.appendChild(btn);
      wrap._byLabel[lbl.replace(/\(\)\s*$/, "")] = btn;   /* key by method name */
    });
    return wrap;
  }

  /* state-machine chips: current state in red, the rest greyed out */
  function makeChips(states) {
    var row = document.createElement("div");
    row.className = "lc-s3d-chips";
    var chips = {};
    states.forEach(function (s) {
      var c = document.createElement("span");
      c.className = "lc-s3d-chip";
      c.textContent = s;
      row.appendChild(c);
      chips[s] = c;
    });
    return {
      el: row,
      set: function (name) {
        states.forEach(function (s) { chips[s].classList.toggle("active", s === name); });
      }
    };
  }

  /* ── boot ────────────────────────────────────────────── */
  /* code_chrome.md (loaded first, via topbar) provides the scan registry:
     one registration covers the initial page scan and all re-scans. */

  window.lcRegisterUpgrader &&
    window.lcRegisterUpgrader(".highlighter-rouge.scene3d, pre.scene3d", upgradeScene3d);

})();
</script>
