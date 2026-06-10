<!-- © 2026 KarmicSoft — LightCode Platform. Proprietary, All Rights Reserved. License: /license -->
{%- comment -%}
X-ray lens.

⌥ Option/Alt + hover: a round aperture you sweep over a widget to strip its
surface and reveal its inner inspector (class + live attribute values + state).

⌥ + ⇧ Shift: full reveal — the hovered widget AND every object it is connected
to are shown as semi-transparent inspector panels, wired by flowing pipes
(fluid runs target → source, binded → binder). Connected objects that are
invisible on the page (e.g. a hidden Dataset) get their own full inspector too.

Pure viewer over the SSOT: hover-detection + structure from the static
assets/component-model.json; live values/links from lcx_inspect()/lcx_target()
in MicroPython (lazy-loaded on first use).

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
  /* Scene container — panels + SVG live here so one transform scales everything */
  #lcx-scene { position: fixed; inset: 0; pointer-events: none; z-index: 99994;
               overflow: visible; }
  .lcx-xray { position: absolute; pointer-events: none; display: none;
              background: rgba(8,18,28,.93); color: #cdebff; border-radius: 5px;
              padding: 7px 11px; white-space: nowrap;
              box-shadow: 0 0 0 1px rgba(120,200,255,.35), 0 8px 26px rgba(0,0,0,.35);
              font: 11px/1.6 ui-monospace, "SF Mono", Menlo, monospace; }
  .lcx-xray.see { background: rgba(8,18,28,.74); }   /* ⇧ full reveal — semi-transparent */
  .lcx-xray .t { font-weight: 700; color: #eaf6ff;
                 border-bottom: 1px solid rgba(120,200,255,.25);
                 padding-bottom: 3px; margin-bottom: 3px; }
  .lcx-xray .r .ic { display: inline-block; width: 1.6em; }
  .lcx-xray .v { color: #8effa6; }
  .lcx-xray .as { color: #ffd479; }
  .lcx-xray .st { margin-top: 4px; padding-top: 3px; color: #9fd0ff;
                  border-top: 1px solid rgba(120,200,255,.25); }
  .lcx-xray .st b { color: #fff; }
  .lcx-xray .code { white-space: pre; margin: 1px 0 4px 1.6em; padding: 4px 7px;
                    color: #d7e7f5; background: rgba(0,0,0,.32);
                    border-left: 2px solid rgba(255,212,121,.5); border-radius: 3px;
                    font: 10px/1.45 ui-monospace, "SF Mono", Menlo, monospace; }
  /* Python syntax tokens (handler source) */
  .lcx-xray .code .c-k { color: #ff8fbf; font-weight: 600; }  /* keyword   */
  .lcx-xray .code .c-s { color: #9effa6; }                    /* string    */
  .lcx-xray .code .c-c { color: #6f8da3; font-style: italic; }/* comment   */
  .lcx-xray .code .c-n { color: #ffd479; }                    /* number    */
  .lcx-xray .code .c-b { color: #7ec8ff; font-style: italic; }/* self/button */
  .lcx-ring { position: fixed; pointer-events: none; z-index: 100000;
              border-radius: 50%; border: 2px solid rgba(140,205,255,.9);
              box-shadow: 0 6px 22px rgba(0,0,0,.4),
                          inset 0 0 26px rgba(120,200,255,.28);
              background: radial-gradient(circle at 35% 28%,
                          rgba(255,255,255,.20), rgba(120,200,255,.05) 45%,
                          transparent 62%);
              display: none; }
  .lcx-svg { position: absolute; inset: 0; width: 100%; height: 100%;
             pointer-events: none; display: none; }  /* behind panels, inside #lcx-scene */
  /* fluid flow: round globules travel target → source (binded → binder) */
  @keyframes lcxflow { to { stroke-dashoffset: 19; } }
  .lcx-flow { animation: lcxflow .8s linear infinite; }
  body.lcx-on, body.lcx-on * { cursor: crosshair !important; }
</style>

<script type="module">
  const URL = "{{ "/assets/component-model.json" | relative_url }}";
  const MP_URL = "https://cdn.jsdelivr.net/npm/@micropython/micropython-webassembly-pyscript@latest/micropython.mjs";
  const R = 95, OFF = 10;
  let DATA = null;
  try { DATA = await (await fetch(URL)).json(); }
  catch (e) { console.warn("[lc-xray] model json not found", e); }

  if (DATA) {
    const { model: MODEL, wrap: WRAP, icons: IC } = DATA;
    const NS = "http://www.w3.org/2000/svg";
    const svg = document.createElementNS(NS, "svg"); svg.setAttribute("class", "lcx-svg");
    svg.innerHTML = '<defs><filter id="lcxGlow" x="-40%" y="-40%" width="180%"' +
      ' height="180%"><feDropShadow dx="0" dy="1" stdDeviation="1.4"' +
      ' flood-color="#0a1620" flood-opacity="0.5"/></filter></defs>';
    const ring = document.createElement("div"); ring.className = "lcx-ring";
    ring.style.width = ring.style.height = (R * 2) + "px";
    // Scene container: panels + SVG live here — one transform scales the whole scene
    const scene = Object.assign(document.createElement("div"), { id: "lcx-scene" });
    scene.style.display = "none";
    scene.appendChild(svg);
    document.body.append(scene, ring);
    const panels = [];
    const panel = i => panels[i] || (panels[i] = scene.appendChild(
      Object.assign(document.createElement("div"), { className: "lcx-xray" })));

    const disp = s => String(s).replace(/_/g, " ");
    const esc = s => String(s).replace(/[&<>]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
    // Tiny self-contained Python highlighter for the event-handler block. Tokenise
    // the raw source first, then escape each piece, so HTML can't leak through.
    const PY_KW = new Set(("False None True and as assert async await break class " +
      "continue def del elif else except finally for from global if import in is " +
      "lambda nonlocal not or pass raise return try while with yield").split(" "));
    function pyHi(src) {
      const re = /(#[^\n]*)|('''[\s\S]*?'''|"""[\s\S]*?"""|'(?:\\.|[^'\\])*'|"(?:\\.|[^"\\])*")|(\b\d+(?:\.\d+)?\b)|([A-Za-z_]\w*)|(\s+)|([\s\S])/g;
      let out = "", m;
      while ((m = re.exec(src))) {
        if (m[1]) out += '<span class="c-c">' + esc(m[1]) + "</span>";        // comment
        else if (m[2]) out += '<span class="c-s">' + esc(m[2]) + "</span>";   // string
        else if (m[3]) out += '<span class="c-n">' + esc(m[3]) + "</span>";   // number
        else if (m[4]) {                                                      // word
          const w = m[4];
          if (PY_KW.has(w)) out += '<span class="c-k">' + esc(w) + "</span>";
          else if (w === "self" || w === "button") out += '<span class="c-b">' + esc(w) + "</span>";
          else out += esc(w);
        } else out += esc(m[5] || m[6]);                                      // whitespace / other
      }
      return out;
    }
    const attrIcon = a => (IC[a.t] || IC.ref || "📦") + (a.list ? (IC.list || "⦙") : "");
    const visible = el => {
      if (!el) return false;
      const r = el.getBoundingClientRect(), s = getComputedStyle(el);
      return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
    };
    const center = r => ({ x: r.left + r.width / 2, y: r.top + r.height / 2 });
    function edgePoint(r, tx, ty) {                 // border point toward (tx,ty)
      const c = center(r), dx = tx - c.x, dy = ty - c.y;
      if (!dx && !dy) return c;
      const s = Math.min(dx ? (r.width / 2) / Math.abs(dx) : Infinity,
                         dy ? (r.height / 2) / Math.abs(dy) : Infinity);
      return { x: c.x + dx * s, y: c.y + dy * s };
    }

    function lineage(name) {
      const chain = []; let cur = name; const seen = new Set();
      while (cur && MODEL[cur] && !seen.has(cur)) {
        seen.add(cur); chain.push(cur); cur = (MODEL[cur].bases || [])[0];
      }
      chain.reverse();
      const pick = key => {
        const out = [], names = new Set();
        for (const c of chain) for (const it of (MODEL[c][key] || [])) {
          const n = it.n || it; if (!names.has(n)) { names.add(n); out.push(it); }
        }
        return out;
      };
      return { attrs: pick("attrs"), events: pick("events"), methods: pick("methods") };
    }
    const rrow = (ic, html, cls) =>
      '<div class="r ' + (cls || "") + '"><span class="ic">' + ic + "</span>" + html + "</div>";
    function schematic(name, live) {
      const sp = MODEL[name]; if (!sp) return esc(name);
      const L = lineage(name), vals = (live && live.vals) || {},
            evts = (live && live.events) || {};
      let h = '<div class="t">' + (sp.icon ? sp.icon + " " : "") + esc(name) + "</div>";
      L.attrs.forEach(a => {
        const has = Object.prototype.hasOwnProperty.call(vals, a.n);
        h += rrow(attrIcon(a), esc(disp(a.n)) +
          (has ? '<span class="v"> = ' + esc(vals[a.n]) + "</span>" : ""));
      });
      L.events.forEach(e => {
        h += rrow(IC.event || "⚡", esc(disp(e)));
        const src = evts[e];                           // live handler body
        if (src) h += '<div class="code">' + pyHi(src.trim()) + "</div>";
      });
      L.methods.forEach(m => {
        const lead = (m.pre && m.pre.length) ? (IC.guard || "▹") : (IC.method || "▸");
        h += rrow(lead, esc(disp(m.n)) + (m.post ? " " + (IC.trans || "▹") : ""));
      });
      if (sp.states && sp.states.length) {
        const cur = live && live.state;
        h += '<div class="st">' + (IC.fsm || "🎛️") + " " + sp.states.map(s =>
          s === cur ? "<b>" + esc(disp(s)) + "</b>" : esc(disp(s))).join(" → ") + "</div>";
      }
      return h;
    }

    function classAt(x, y) {
      let el = document.elementFromPoint(x, y);
      while (el && el !== document.body) {
        if (el.classList) for (const [token, name] of WRAP)
          if (el.classList.contains(token)) return { el, name };
        el = el.parentElement;
      }
      return null;
    }

    // MicroPython bridges (null until loaded)
    function inspect(el) {
      if (!window._lcxRun) return null;
      el.setAttribute("data-lcx-target", "");
      try { window._lcxRun("import js\njs.window._lcxData = lcx_inspect()\n");
            return JSON.parse(window._lcxData || "{}"); }
      catch (e) { return null; } finally { el.removeAttribute("data-lcx-target"); }
    }
    function inspectTarget(cls, id) {
      if (!window._lcxRun) return null;
      try { window._lcxRun("import js\njs.window._lcxData = lcx_target('" + cls + "','" + id + "')\n");
            return JSON.parse(window._lcxData || "{}"); }
      catch (e) { return null; }
    }
    function loadMP() {
      if (window._lcxMPp) return window._lcxMPp;
      window._lcxMPp = (async () => {
        const m = await (window._lcMpReady || (window._lcMpReady =
          import(MP_URL).then(x => x.loadMicroPython({ stdout(){}, stderr(){} }))));
        const run = m.runPython || m.exec || m.pyexec || m.run;
        run.call(m, (document.getElementById("lc-steps-preamble") || {}).textContent || "");
        window._lcxRun = (code) => run.call(m, code);
        if (lastHit) { liveCache = null; cur = null; update(lastHit, lastXY, lastShift); }
      })().catch(e => console.warn("[lc-xray] micropython failed", e));
      return window._lcxMPp;
    }

    // ── pipes (steel casing + glowing core + flowing fluid) ──────────────────
    const clearPipes = () => [...svg.querySelectorAll(".lcx-edge")].forEach(n => n.remove());
    function svgEl(tag, attrs) {
      const e = document.createElementNS(NS, tag);
      for (const k in attrs) e.setAttribute(k, attrs[k]);
      e.classList.add("lcx-edge"); svg.appendChild(e); return e;
    }
    function routePath(sx, sy, tx, ty, r) {
      const mx = (sx + tx) / 2;
      const pts = [{ x: sx, y: sy }, { x: mx, y: sy }, { x: mx, y: ty }, { x: tx, y: ty }];
      let d = "M" + sx + "," + sy;
      const near = (a, b, k) => { const dx = b.x - a.x, dy = b.y - a.y, L = Math.hypot(dx, dy) || 1;
        const t = Math.min(k, L / 2) / L; return { x: a.x + dx * t, y: a.y + dy * t }; };
      for (let i = 1; i < pts.length - 1; i++) {
        const a = near(pts[i], pts[i - 1], r), b = near(pts[i], pts[i + 1], r);
        d += " L" + a.x + "," + a.y + " Q" + pts[i].x + "," + pts[i].y + " " + b.x + "," + b.y;
      }
      return d + " L" + tx + "," + ty;
    }
    function pipe(sx, sy, tx, ty) {
      const d = routePath(sx, sy, tx, ty, 12), cap = "round";
      svgEl("path", { d, fill: "none", stroke: "#14303f", "stroke-width": 10,
        "stroke-linecap": cap, "stroke-linejoin": cap, filter: "url(#lcxGlow)" });
      svgEl("path", { d, fill: "none", stroke: "#3f8fd6", "stroke-width": 6,
        "stroke-linecap": cap, "stroke-linejoin": cap });
      const flow = svgEl("path", { d, fill: "none", stroke: "#cdf3ff", "stroke-width": 5,
        "stroke-linecap": "round", "stroke-dasharray": "0.01 19" });
      flow.classList.add("lcx-flow");
      flange(sx, sy); flange(tx, ty);
    }
    function flange(x, y) {
      svgEl("circle", { cx: x, cy: y, r: 7, fill: "#14303f" });
      svgEl("circle", { cx: x, cy: y, r: 3.4, fill: "#8fd0ff" });
    }
    function plabel(x, y, text) {
      const w = text.length * 6.5 + 12;
      svgEl("rect", { x: x - w / 2, y: y - 9, width: w, height: 17, rx: 8.5,
        fill: "#0c1f2b", stroke: "#3f8fd6", "stroke-width": 1, filter: "url(#lcxGlow)" });
      const t = svgEl("text", { x, y: y + 3.5, fill: "#cdebff", "font-size": 11,
        "font-family": "ui-monospace, monospace", "text-anchor": "middle" });
      t.textContent = text;
    }

    // ── scene assembly ───────────────────────────────────────────────────────
    let cur = null, lastHit = null, lastXY = { x: 0, y: 0 }, lastShift = null, liveCache = null;
    function fitScene() {
      const vw = window.innerWidth, vh = window.innerHeight;
      const vis = panels.filter(p => p.style.display !== "none");
      if (!vis.length) return;
      let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
      vis.forEach(p => {
        x0 = Math.min(x0, p.offsetLeft);
        y0 = Math.min(y0, p.offsetTop);
        x1 = Math.max(x1, p.offsetLeft + p.offsetWidth);
        y1 = Math.max(y1, p.offsetTop + p.offsetHeight);
      });
      const pad = 12;
      const s = Math.min((vw - pad * 2) / (x1 - x0), (vh - pad * 2) / (y1 - y0), 1);
      if (s >= 0.99) { scene.style.transform = ""; return; }
      scene.style.transformOrigin = x0 + "px " + y0 + "px";
      scene.style.transform = "scale(" + s + ")";
    }
    function hideAll() {
      panels.forEach(p => p.style.display = "none");
      ring.style.display = "none"; svg.style.display = "none"; clearPipes();
      scene.style.display = "none"; scene.style.transform = "";
      document.body.classList.remove("lcx-on"); cur = null;
    }
    function place(p, x, y) {
      p.style.left = x + "px"; p.style.top = y + "px"; p.style.display = "block";
      p.style.clipPath = p.style.webkitClipPath = "none";
    }
    function buildScene(hit, data, shift) {
      clearPipes(); panels.forEach(p => p.style.display = "none");
      scene.style.transform = "";                          // reset scale before re-measuring
      scene.style.display = "block";
      const rect = hit.el.getBoundingClientRect();
      const p0 = panel(0);
      p0.innerHTML = schematic(hit.name, data);
      p0.classList.toggle("see", shift);
      place(p0, rect.left + OFF, rect.top + OFF);
      if (!shift) { svg.style.display = "none"; return; }   // lens mode: clip applied later
      svg.style.display = "block";
      // ── connected subgraph: transitive closure over the typed associations,
      //    both directions — forward links from each node's dump, plus a DOM
      //    scan for referrers (elements whose bind/bound-to/bound names it) ──
      const nodes = [], byId = new Map(), byEl = new Map(), edges = [], eSeen = new Set();
      function addNode(name, id, el, dump) {
        if (id && byId.has(id)) return byId.get(id);
        if (el && byEl.has(el)) return byEl.get(el);
        const n = { name, id: id || "", el: el || null, dump: dump || null, fresh: true };
        nodes.push(n);
        if (id) byId.set(id, n);
        if (el) byEl.set(el, n);
        return n;
      }
      function addEdge(a, b, role, list) {
        const k = nodes.indexOf(a) + ">" + nodes.indexOf(b) + ":" + role;
        if (eSeen.has(k)) return;
        eSeen.add(k); edges.push({ a, b, role, list });
      }
      const REF_ATTRS = [["data-bind", "bind"], ["data-bound-to", "bound_to"], ["data-bound", "bound"]];
      const wrapName = el => { if (el && el.classList) for (const [t, n] of WRAP)
        if (el.classList.contains(t)) return n; return null; };
      const root = addNode(hit.name, hit.el.getAttribute("data-lc-id") || "", hit.el, data);
      root.fresh = false;
      const queue = [root];
      while (queue.length && nodes.length < 24) {
        const n = queue.shift();
        ((n.dump && n.dump.links) || []).forEach(lk => {
          const tEl = document.querySelector("[data-lc-id='" + lk.id + "']");
          const t = addNode(lk.target, lk.id, tEl, null);
          if (t.fresh) { t.fresh = false; t.dump = inspectTarget(lk.target, lk.id); queue.push(t); }
          addEdge(n, t, lk.role, lk.list);
        });
        if (n.id) REF_ATTRS.forEach(([attr, role]) => {
          document.querySelectorAll("[" + attr + "='" + n.id + "']").forEach(rEl => {
            const rn = wrapName(rEl); if (!rn) return;
            const r = addNode(rn, rEl.getAttribute("data-lc-id") || "", rEl, null);
            if (r.fresh) { r.fresh = false; r.dump = inspect(rEl); queue.push(r); }
            addEdge(r, n, role, false);
          });
        });
      }
      let pi = 0, gi = 0;
      nodes.forEach(n => {
        if (n === root) { n.panel = p0; return; }
        const p = panel(++pi);
        p.innerHTML = schematic(n.name, n.dump);
        p.classList.add("see");
        if (n.el && visible(n.el)) {
          const tr = n.el.getBoundingClientRect();
          place(p, tr.left + OFF, tr.top + OFF);
        } else {                                            // hidden object → its own panel
          place(p, rect.right + 70, rect.top + gi * 104); gi++;
        }
        n.panel = p;
      });
      edges.forEach(eg => {
        const r0 = eg.a.panel.getBoundingClientRect(), r1 = eg.b.panel.getBoundingClientRect();
        const e0 = edgePoint(r0, center(r1).x, center(r1).y);
        const e1 = edgePoint(r1, center(r0).x, center(r0).y);
        pipe(e0.x, e0.y, e1.x, e1.y);
        plabel((e0.x + e1.x) / 2, (e0.y + e1.y) / 2, (eg.list ? "⦙ " : "") + disp(eg.role));
      });
      requestAnimationFrame(fitScene);                     // fit after browser lays out panels
    }
    function lensClip(hit, xy) {
      const rect = hit.el.getBoundingClientRect();
      const px = rect.left + OFF, py = rect.top + OFF;
      const clip = "circle(" + R + "px at " + (xy.x - px) + "px " + (xy.y - py) + "px)";
      const p0 = panel(0); p0.style.clipPath = p0.style.webkitClipPath = clip;
      ring.style.display = "block";
      ring.style.left = (xy.x - R) + "px"; ring.style.top = (xy.y - R) + "px";
    }
    function update(hit, xy, shift) {
      document.body.classList.add("lcx-on");
      const changed = !cur || cur.el !== hit.el;
      if (changed) { try { liveCache = inspect(hit.el); } catch (e) { liveCache = null; } }
      cur = hit; lastHit = hit; lastXY = xy;
      if (changed || shift !== lastShift) buildScene(hit, liveCache, shift);
      if (shift) ring.style.display = "none";
      else lensClip(hit, xy);
      lastShift = shift;
    }
    function show(e) {
      const hit = classAt(e.clientX, e.clientY);
      if (!hit) { hideAll(); return; }
      loadMP();
      update(hit, { x: e.clientX, y: e.clientY }, e.shiftKey);
    }

    addEventListener("pointermove", e => { e.altKey ? show(e) : hideAll(); }, true);
    addEventListener("keyup", e => { if (e.key === "Alt" || !e.altKey) hideAll(); });
    addEventListener("blur", hideAll);

    // ── Touch x-ray mode (toggled from the slides FAB popup on touch devices) ──
    let _touchOn = false;
    window.lcxIsActive  = () => _touchOn;
    window.lcxTouchOn   = () => { _touchOn = true;  loadMP(); };
    window.lcxTouchOff  = () => { _touchOn = false; hideAll(); };

    const isFAB = e => e.target.closest && e.target.closest('.lc-slides-fab, #lc-bl-popup');
    function showTouch(e) {
      if (!_touchOn || isFAB(e)) return;   // let FAB taps through so click fires
      e.preventDefault();
      const t = e.touches[0];
      const hit = classAt(t.clientX, t.clientY);
      if (!hit) { hideAll(); return; }
      update(hit, { x: t.clientX, y: t.clientY }, e.touches.length >= 2);
    }
    addEventListener("touchstart", showTouch, { passive: false, capture: true });
    addEventListener("touchmove",  showTouch, { passive: false, capture: true });
    addEventListener("touchend",   e => { if (_touchOn && !isFAB(e)) e.preventDefault(); }, { passive: false });
  }
</script>
