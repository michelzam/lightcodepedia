{%- comment -%}
X-ray lens — hold ⌥ Option/Alt and hover any rendered widget to see THROUGH it
to its component-model class: icon, typed knobs, behaviours and state machine.

Pure viewer over the SSOT: it reads the static assets/component-model.json
emitted by tools/gen_component_diagram.py (no MicroPython, no graphviz), and
maps the hovered DOM node to a class via the same lc-* token map (_WRAP).

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
  .lcx-box { position: fixed; pointer-events: none; z-index: 99998;
             border: 2px solid #4a76d4; background: rgba(74,118,212,.08);
             border-radius: 3px; transition: all .04s linear; display: none; }
  .lcx-card { position: fixed; pointer-events: none; z-index: 99999; display: none;
              max-width: 280px; background: #fff; color: #31333f;
              border: 1px solid #cfd4dc; border-radius: 6px;
              box-shadow: 0 6px 24px rgba(0,0,0,.18);
              font: 12px/1.45 "Source Sans Pro", sans-serif; overflow: hidden; }
  .lcx-card .h { font-weight: 600; padding: 6px 9px; background: #f6f7f9;
                 border-bottom: 1px solid #e6e8ec; }
  .lcx-card .h .root { color: #9aa0aa; font-weight: 400; }
  .lcx-card .sec { padding: 5px 9px; }
  .lcx-card .sec + .sec { border-top: 1px solid #eef0f3; }
  .lcx-card .r { white-space: nowrap; }
  .lcx-card .r .ic { display: inline-block; width: 1.5em; }
  .lcx-card .v { color: #2f7d32; }
  .lcx-card .assoc { color: #4a76d4; }
  .lcx-card .hint { padding: 4px 9px; font-size: 10px; color: #9aa0aa;
                    background: #fafbfc; border-top: 1px solid #eef0f3; }
  body.lcx-on, body.lcx-on * { cursor: crosshair !important; }
</style>

<script type="module">
  const URL = "{{ "/assets/component-model.json" | relative_url }}";
  const MP_URL = "https://cdn.jsdelivr.net/npm/@micropython/micropython-webassembly-pyscript@latest/micropython.mjs";
  let DATA = null;
  try { DATA = await (await fetch(URL)).json(); }
  catch (e) { console.warn("[lc-xray] model json not found", e); }

  if (DATA) {
    const { model: MODEL, wrap: WRAP, icons: IC } = DATA;
    const box = document.createElement("div"); box.className = "lcx-box";
    const card = document.createElement("div"); card.className = "lcx-card";
    document.body.appendChild(box); document.body.appendChild(card);

    const disp = s => String(s).replace(/_/g, " ");
    const attrIcon = a => (IC[a.t] || IC.ref || "📦") + (a.list ? (IC.list || "⦙") : "");
    const esc = s => String(s).replace(/[&<>]/g, c =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));

    // base chain root→leaf, deduped (so inherited attrs like id come first)
    function lineage(name) {
      const chain = []; let cur = name; const seen = new Set();
      while (cur && MODEL[cur] && !seen.has(cur)) {
        seen.add(cur); chain.push(cur); cur = (MODEL[cur].bases || [])[0];
      }
      chain.reverse();
      const pick = key => {
        const out = [], names = new Set();
        for (const c of chain) for (const it of (MODEL[c][key] || [])) {
          const n = it.n || it;
          if (!names.has(n)) { names.add(n); out.push(it); }
        }
        return out;
      };
      return { attrs: pick("attrs"), events: pick("events"),
               methods: pick("methods"), assoc: pick("assoc") };
    }

    const row = (ic, html, cls) =>
      '<div class="r ' + (cls || "") + '"><span class="ic">' + ic + "</span>" + html + "</div>";

    // live values + current state for an element (via MicroPython); null if not ready
    function inspect(el) {
      if (!window._lcxRun) return null;
      el.setAttribute("data-lcx-target", "");
      try {
        window._lcxRun("import js\njs.window._lcxData = lcx_inspect()\n");
        return JSON.parse(window._lcxData || "{}");
      } catch (e) { return null; } finally { el.removeAttribute("data-lcx-target"); }
    }

    function render(name, live) {
      const sp = MODEL[name]; if (!sp) return "";
      const L = lineage(name);
      const vals = (live && live.vals) || {};
      let html = '<div class="h">' + (sp.icon ? sp.icon + " " : "") + esc(name) + "</div>";
      let knobs = "";
      L.attrs.forEach(a => {
        const has = Object.prototype.hasOwnProperty.call(vals, a.n);
        const v = has ? '<span class="v"> = ' + esc(vals[a.n]) + "</span>" : "";
        knobs += row(attrIcon(a), esc(disp(a.n)) + v);
      });
      if (knobs) html += '<div class="sec">' + knobs + "</div>";
      let beh = "";
      L.events.forEach(e => beh += row(IC.event || "⚡", esc(disp(e))));
      L.methods.forEach(m => {
        const lead = (m.pre && m.pre.length) ? (IC.guard || "▹") : (IC.method || "▸");
        beh += row(lead, esc(disp(m.n)) + (m.post ? " " + (IC.trans || "▹") : ""));
      });
      if (beh) html += '<div class="sec">' + beh + "</div>";
      let asc = "";
      L.assoc.forEach(a =>
        asc += row("→", esc((a.list ? "⦙ " : "") + disp(a.n) + " : " + a.target), "assoc"));
      if (asc) html += '<div class="sec">' + asc + "</div>";
      if (sp.states && sp.states.length) {
        const cur = live && live.state;
        const seq = sp.states.map(s =>
          (s === cur ? "<b>" + esc(disp(s)) + "</b>" : esc(disp(s)))).join(" → ");
        html += '<div class="hint">' + (IC.fsm || "🎛️") + " " + seq + "</div>";
      }
      return html;
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

    // lazy MicroPython: load + run the preamble once, on first lens use
    function loadMP() {
      if (window._lcxMPp) return window._lcxMPp;
      window._lcxMPp = (async () => {
        const m = await (window._lcMpReady || (window._lcMpReady =
          import(MP_URL).then(x => x.loadMicroPython({ stdout(){}, stderr(){} }))));
        const run = m.runPython || m.exec || m.pyexec || m.run;
        run.call(m, (document.getElementById("lc-steps-preamble") || {}).textContent || "");
        window._lcxRun = (code) => run.call(m, code);
        if (curHit) draw(curHit, lastXY);   // fill in values once ready
      })().catch(e => console.warn("[lc-xray] micropython failed", e));
      return window._lcxMPp;
    }

    let curHit = null, lastXY = { x: 0, y: 0 };
    function hide() {
      box.style.display = card.style.display = "none";
      document.body.classList.remove("lcx-on"); curHit = null;
    }
    function place() {                       // position highlight box + card
      const r = curHit.el.getBoundingClientRect();
      box.style.display = "block";
      box.style.left = (r.left - 2) + "px"; box.style.top = (r.top - 2) + "px";
      box.style.width = r.width + "px"; box.style.height = r.height + "px";
      card.style.display = "block";
      const cw = card.offsetWidth, ch = card.offsetHeight;
      let cx = lastXY.x + 16, cy = lastXY.y + 16;
      if (cx + cw > innerWidth) cx = lastXY.x - cw - 16;
      if (cy + ch > innerHeight) cy = innerHeight - ch - 8;
      card.style.left = Math.max(8, cx) + "px";
      card.style.top = Math.max(8, cy) + "px";
    }
    function draw(hit, xy) {                  // re-inspect + render (element changed)
      curHit = hit; lastXY = xy;
      document.body.classList.add("lcx-on");
      card.innerHTML = render(hit.name, inspect(hit.el));
      place();
    }
    function show(e) {
      const hit = classAt(e.clientX, e.clientY);
      if (!hit) { hide(); return; }
      loadMP();
      lastXY = { x: e.clientX, y: e.clientY };
      if (curHit && curHit.el === hit.el) { place(); return; }  // same widget → reposition
      draw(hit, lastXY);
    }

    addEventListener("mousemove", e => { e.altKey ? show(e) : hide(); }, true);
    addEventListener("keyup", e => { if (e.key === "Alt" || !e.altKey) hide(); });
    addEventListener("blur", hide);
  }
</script>
