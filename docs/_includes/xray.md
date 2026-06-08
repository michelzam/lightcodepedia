{%- comment -%}
X-ray lens — hold ⌥ Option/Alt and sweep the round lens over any rendered widget
to strip its surface and reveal the INNER inspector: the component class with
live attribute values and current state, shown only through the circular
aperture (clip-path disc). Add SHIFT to also draw connectors to the widget's
associated objects (a real arrow to a visible target, a ghost chip for hidden
ones like a Dataset).

Pure viewer over the SSOT: hover-detection + structure come from the static
assets/component-model.json (emitted by tools/gen_component_diagram.py); live
values/links come from lcx_inspect() in MicroPython (lazy-loaded on first use).

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
  .lcx-xray { position: fixed; pointer-events: none; z-index: 99996; display: none;
              align-items: flex-start; justify-content: flex-start; overflow: visible;
              background: rgba(8,18,28,.90); border-radius: 3px; box-sizing: border-box; }
  .lcx-body { color: #cdebff; padding: 6px 10px; white-space: nowrap;
              margin: 12px 0 0 16px;
              font: 11px/1.55 ui-monospace, "SF Mono", Menlo, monospace; }
  .lcx-body .t { font-weight: 700; color: #eaf6ff;
                 border-bottom: 1px solid rgba(120,200,255,.25);
                 padding-bottom: 3px; margin-bottom: 3px; }
  .lcx-body .r .ic { display: inline-block; width: 1.6em; }
  .lcx-body .v { color: #8effa6; }
  .lcx-body .as { color: #ffd479; }
  .lcx-body .st { margin-top: 4px; padding-top: 3px; color: #9fd0ff;
                  border-top: 1px solid rgba(120,200,255,.25); }
  .lcx-body .st b { color: #fff; }
  .lcx-ring { position: fixed; pointer-events: none; z-index: 100000;
              border-radius: 50%; border: 2px solid rgba(140,205,255,.9);
              box-shadow: 0 6px 22px rgba(0,0,0,.4),
                          inset 0 0 26px rgba(120,200,255,.28);
              background: radial-gradient(circle at 35% 28%,
                          rgba(255,255,255,.20), rgba(120,200,255,.05) 45%,
                          transparent 62%);
              display: none; }
  .lcx-svg { position: fixed; inset: 0; width: 100%; height: 100%;
             pointer-events: none; z-index: 99997; display: none; }
  .lcx-ghost { position: fixed; pointer-events: none; z-index: 99998; display: none;
               background: #102232; color: #cdebff; border: 1px solid #ffd479;
               border-radius: 4px; padding: 2px 7px; font: 11px/1.4 ui-monospace, monospace; }
  body.lcx-on, body.lcx-on * { cursor: crosshair !important; }
</style>

<script type="module">
  const URL = "{{ "/assets/component-model.json" | relative_url }}";
  const MP_URL = "https://cdn.jsdelivr.net/npm/@micropython/micropython-webassembly-pyscript@latest/micropython.mjs";
  const R = 95;                       // lens radius
  let DATA = null;
  try { DATA = await (await fetch(URL)).json(); }
  catch (e) { console.warn("[lc-xray] model json not found", e); }

  if (DATA) {
    const { model: MODEL, wrap: WRAP, icons: IC } = DATA;
    const NS = "http://www.w3.org/2000/svg";
    const xray = document.createElement("div"); xray.className = "lcx-xray";
    const ring = document.createElement("div"); ring.className = "lcx-ring";
    ring.style.width = ring.style.height = (R * 2) + "px";
    const svg = document.createElementNS(NS, "svg"); svg.setAttribute("class", "lcx-svg");
    svg.innerHTML = '<defs><filter id="lcxGlow" x="-40%" y="-40%" width="180%"' +
      ' height="180%"><feDropShadow dx="0" dy="1" stdDeviation="1.4"' +
      ' flood-color="#0a1620" flood-opacity="0.5"/></filter></defs>';
    const ghosts = [];
    document.body.append(xray, ring, svg);

    const disp = s => String(s).replace(/_/g, " ");
    const esc = s => String(s).replace(/[&<>]/g, c =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
    const attrIcon = a => (IC[a.t] || IC.ref || "📦") + (a.list ? (IC.list || "⦙") : "");
    const visible = el => {
      if (!el) return false;
      const r = el.getBoundingClientRect(), s = getComputedStyle(el);
      return r.width > 0 && r.height > 0 && s.display !== "none" && s.visibility !== "hidden";
    };

    function lineage(name) {                 // base chain root→leaf, deduped
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

    function schematic(name, live) {         // the x-ray content for a widget
      const sp = MODEL[name]; if (!sp) return "";
      const L = lineage(name), vals = (live && live.vals) || {};
      let h = '<div class="t">' + (sp.icon ? sp.icon + " " : "") + esc(name) + "</div>";
      L.attrs.forEach(a => {
        const has = Object.prototype.hasOwnProperty.call(vals, a.n);
        h += rrow(attrIcon(a), esc(disp(a.n)) +
          (has ? '<span class="v"> = ' + esc(vals[a.n]) + "</span>" : ""));
      });
      L.events.forEach(e => h += rrow(IC.event || "⚡", esc(disp(e))));
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

    // live values + links via MicroPython (null until loaded)
    function inspect(el) {
      if (!window._lcxRun) return null;
      el.setAttribute("data-lcx-target", "");
      try {
        window._lcxRun("import js\njs.window._lcxData = lcx_inspect()\n");
        return JSON.parse(window._lcxData || "{}");
      } catch (e) { return null; } finally { el.removeAttribute("data-lcx-target"); }
    }
    function loadMP() {
      if (window._lcxMPp) return window._lcxMPp;
      window._lcxMPp = (async () => {
        const m = await (window._lcMpReady || (window._lcMpReady =
          import(MP_URL).then(x => x.loadMicroPython({ stdout(){}, stderr(){} }))));
        const run = m.runPython || m.exec || m.pyexec || m.run;
        run.call(m, (document.getElementById("lc-steps-preamble") || {}).textContent || "");
        window._lcxRun = (code) => run.call(m, code);
        if (cur) update(cur, lastXY, lastShift);   // fill values/links once ready
      })().catch(e => console.warn("[lc-xray] micropython failed", e));
      return window._lcxMPp;
    }

    function connectors(srcRect, live, shift) {
      // clear previous
      [...svg.querySelectorAll(".lcx-edge")].forEach(n => n.remove());
      ghosts.forEach(g => g.style.display = "none");
      if (!shift || !live || !live.links || !live.links.length) { svg.style.display = "none"; return; }
      svg.style.display = "block";
      const sx = srcRect.left + srcRect.width / 2, sy = srcRect.top + srcRect.height / 2;
      live.links.forEach((lk, i) => {
        const tEl = document.querySelector("[data-lc-id='" + lk.id + "']");
        let bx, by;
        if (visible(tEl)) {
          const tr = tEl.getBoundingClientRect();
          bx = tr.left + tr.width / 2; by = tr.top + tr.height / 2;
          port("rect", tr);                                  // highlight target box
        } else {                                             // hidden target → ghost chip
          const g = ghosts[i] || (ghosts[i] = mkGhost());
          const tIcon = (MODEL[lk.target] || {}).icon || "📦";
          g.innerHTML = tIcon + " " + esc(lk.id);
          g.style.display = "block";
          g.style.left = (srcRect.left + 36 + i * 14) + "px";
          g.style.top = (srcRect.top - 48 - i * 34) + "px";
          const gr = g.getBoundingClientRect();
          bx = gr.left + gr.width / 2; by = gr.top + gr.height / 2;
        }
        pipe(sx, sy, bx, by);
        const mx = (sx + bx) / 2;
        plabel(mx, (sy + by) / 2, (lk.list ? "⦙ " : "") + disp(lk.role));
      });
    }
    function mkGhost() {
      const g = document.createElement("div"); g.className = "lcx-ghost";
      document.body.appendChild(g); return g;
    }
    function svgEl(tag, attrs) {
      const e = document.createElementNS(NS, tag);
      for (const k in attrs) e.setAttribute(k, attrs[k]);
      e.classList.add("lcx-edge"); svg.appendChild(e); return e;
    }
    // orthogonal (plumbing) route with rounded elbows
    function routePath(sx, sy, tx, ty, r) {
      const mx = (sx + tx) / 2;
      const pts = [{ x: sx, y: sy }, { x: mx, y: sy }, { x: mx, y: ty }, { x: tx, y: ty }];
      let d = "M" + sx + "," + sy;
      const near = (a, b, k) => {                 // point k px from corner a toward b
        const dx = b.x - a.x, dy = b.y - a.y, L = Math.hypot(dx, dy) || 1;
        const t = Math.min(k, L / 2) / L;
        return { x: a.x + dx * t, y: a.y + dy * t };
      };
      for (let i = 1; i < pts.length - 1; i++) {
        const a = near(pts[i], pts[i - 1], r), b = near(pts[i], pts[i + 1], r);
        d += " L" + a.x + "," + a.y + " Q" + pts[i].x + "," + pts[i].y + " " + b.x + "," + b.y;
      }
      return d + " L" + tx + "," + ty;
    }
    function pipe(sx, sy, tx, ty) {               // steel casing + glowing core + ports
      const d = routePath(sx, sy, tx, ty, 12), cap = "round";
      svgEl("path", { d, fill: "none", stroke: "#14303f", "stroke-width": 10,
        "stroke-linecap": cap, "stroke-linejoin": cap, filter: "url(#lcxGlow)" });
      svgEl("path", { d, fill: "none", stroke: "#3f8fd6", "stroke-width": 6,
        "stroke-linecap": cap, "stroke-linejoin": cap });
      svgEl("path", { d, fill: "none", stroke: "rgba(205,235,255,.75)", "stroke-width": 1.6,
        "stroke-linecap": cap, "stroke-linejoin": cap });
      flange(sx, sy); flange(tx, ty);
    }
    function flange(x, y) {
      svgEl("circle", { cx: x, cy: y, r: 7, fill: "#14303f" });
      svgEl("circle", { cx: x, cy: y, r: 3.4, fill: "#8fd0ff" });
    }
    function port(_, r) {                          // target component outline
      svgEl("rect", { x: r.left - 1, y: r.top - 1, width: r.width + 2, height: r.height + 2,
        rx: 4, fill: "none", stroke: "#3f8fd6", "stroke-width": 2, "stroke-dasharray": "5 4" });
    }
    function plabel(x, y, text) {                  // role tag clipped onto the pipe
      const w = text.length * 6.5 + 12;
      svgEl("rect", { x: x - w / 2, y: y - 9, width: w, height: 17, rx: 8.5,
        fill: "#0c1f2b", stroke: "#3f8fd6", "stroke-width": 1, filter: "url(#lcxGlow)" });
      const t = svgEl("text", { x, y: y + 3.5, fill: "#cdebff", "font-size": 11,
        "font-family": "ui-monospace, monospace", "text-anchor": "middle" });
      t.textContent = text;
    }

    let cur = null, lastXY = { x: 0, y: 0 }, lastShift = false, liveCache = null;
    function hide() {
      xray.style.display = ring.style.display = svg.style.display = "none";
      ghosts.forEach(g => g.style.display = "none");
      document.body.classList.remove("lcx-on"); cur = null; liveCache = null;
    }
    function update(hit, xy, shift) {
      document.body.classList.add("lcx-on");
      // 1) ALWAYS move the lens ring first — never blocked by inspect/render errors
      ring.style.display = "block";
      ring.style.left = (xy.x - R) + "px"; ring.style.top = (xy.y - R) + "px";
      lastXY = xy; lastShift = shift;
      // 2) (re)build the x-ray content only when the widget under the lens changes
      const rect = hit.el.getBoundingClientRect();
      if (!cur || cur.el !== hit.el) {
        try { liveCache = inspect(hit.el); } catch (e) { liveCache = null; }
        xray.innerHTML = '<div class="lcx-body">' + schematic(hit.name, liveCache) + "</div>";
      }
      cur = hit;
      // 3) overlay fills the widget box; aperture clips it to the disc at the cursor
      xray.style.left = rect.left + "px"; xray.style.top = rect.top + "px";
      xray.style.width = rect.width + "px"; xray.style.height = rect.height + "px";
      xray.style.display = "flex";
      const clip = "circle(" + R + "px at " + (xy.x - rect.left) + "px " +
        (xy.y - rect.top) + "px)";
      xray.style.clipPath = clip; xray.style.webkitClipPath = clip;
      try { connectors(rect, liveCache, shift); } catch (e) { /* keep tracking */ }
    }
    function show(e) {
      const hit = classAt(e.clientX, e.clientY);
      if (!hit) { hide(); return; }
      loadMP();
      update(hit, { x: e.clientX, y: e.clientY }, e.shiftKey);
    }

    addEventListener("pointermove", e => { e.altKey ? show(e) : hide(); }, true);
    addEventListener("keyup", e => { if (e.key === "Alt" || !e.altKey) hide(); });
    addEventListener("blur", hide);
  }
</script>
