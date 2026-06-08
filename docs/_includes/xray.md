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
  .lcx-card .assoc { color: #4a76d4; }
  .lcx-card .hint { padding: 4px 9px; font-size: 10px; color: #9aa0aa;
                    background: #fafbfc; border-top: 1px solid #eef0f3; }
  body.lcx-on, body.lcx-on * { cursor: crosshair !important; }
</style>

<script type="module">
  const URL = "{{ "/assets/component-model.json" | relative_url }}";
  let DATA = null;
  try { DATA = await (await fetch(URL)).json(); }
  catch (e) { console.warn("[lc-xray] model json not found", e); }

  if (DATA) {
    const { model: MODEL, wrap: WRAP, icons: IC, roots: ROOTS } = DATA;
    const box = document.createElement("div"); box.className = "lcx-box";
    const card = document.createElement("div"); card.className = "lcx-card";
    document.body.appendChild(box); document.body.appendChild(card);

    const disp = s => String(s).replace(/_/g, " ");
    const attrIcon = a => (IC[a.t] || IC.ref || "📦") + (a.list ? (IC.list || "⦙") : "");
    const row = (ic, name, cls) =>
      '<div class="r ' + (cls || "") + '"><span class="ic">' + ic + "</span>" +
      disp(name) + "</div>";

    function classAt(x, y) {
      let el = document.elementFromPoint(x, y);
      while (el && el !== document.body) {
        if (el.classList) {
          for (const [token, name] of WRAP)
            if (el.classList.contains(token)) return { el, name };
        }
        el = el.parentElement;
      }
      return null;
    }

    function render(name) {
      const sp = MODEL[name]; if (!sp) return "";
      let roots = "";
      (sp.bases || []).forEach(b => {
        if (ROOTS.indexOf(b) >= 0 && MODEL[b]) roots += " ➭ " + MODEL[b].icon;
      });
      let html = '<div class="h">' + (sp.icon ? sp.icon + " " : "") + name +
                 '<span class="root">' + roots + "</span></div>";
      let knobs = "";
      if (sp.states && sp.states.length) knobs += row(IC.fsm || "🎛️", "state");
      (sp.attrs || []).forEach(a => knobs += row(attrIcon(a), a.n));
      if (knobs) html += '<div class="sec">' + knobs + "</div>";
      let beh = "";
      (sp.events || []).forEach(e => beh += row(IC.event || "⚡", e));
      (sp.methods || []).forEach(m => {
        const lead = (m.pre && m.pre.length) ? (IC.guard || "▹") : (IC.method || "▸");
        beh += row(lead, m.n + (m.post ? " " + (IC.trans || "▹") : ""));
      });
      if (beh) html += '<div class="sec">' + beh + "</div>";
      let asc = "";
      (sp.assoc || []).forEach(a =>
        asc += row("→", (a.list ? "⦙ " : "") + a.n + " : " + a.target, "assoc"));
      if (asc) html += '<div class="sec">' + asc + "</div>";
      if (sp.states && sp.states.length)
        html += '<div class="hint">' + (IC.fsm || "🎛️") + " " +
                sp.states.join(" → ") + "</div>";
      return html;
    }

    let curName = null;
    function hide() {
      box.style.display = card.style.display = "none";
      document.body.classList.remove("lcx-on"); curName = null;
    }
    function show(e) {
      const hit = classAt(e.clientX, e.clientY);
      if (!hit) { hide(); return; }
      document.body.classList.add("lcx-on");
      const r = hit.el.getBoundingClientRect();
      box.style.display = "block";
      box.style.left = (r.left - 2) + "px"; box.style.top = (r.top - 2) + "px";
      box.style.width = r.width + "px"; box.style.height = r.height + "px";
      if (hit.name !== curName) { card.innerHTML = render(hit.name); curName = hit.name; }
      card.style.display = "block";
      const cw = card.offsetWidth, ch = card.offsetHeight;
      let cx = e.clientX + 16, cy = e.clientY + 16;
      if (cx + cw > innerWidth) cx = e.clientX - cw - 16;
      if (cy + ch > innerHeight) cy = innerHeight - ch - 8;
      card.style.left = Math.max(8, cx) + "px";
      card.style.top = Math.max(8, cy) + "px";
    }

    addEventListener("mousemove", e => { e.altKey ? show(e) : hide(); }, true);
    addEventListener("keyup", e => { if (e.key === "Alt" || !e.altKey) hide(); });
    addEventListener("blur", hide);
  }
</script>
