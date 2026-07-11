{%- comment -%}
X-ray edit — click a widget while X-ray is active to edit its knobs + content in
a small dialog. Applies live (re-render); does NOT save (no account) — reload
loses it, which is the incentive to create an account. Reads the pre-upgrade
source from window.lcSourceOf (code_chrome). Auto-included by default.html.
{%- endcomment -%}

<style>
#lcx-edit { position: fixed; right: 16px; bottom: 16px; width: 320px; max-height: 72vh; overflow: auto;
  background: #fff; border: 1px solid #d0d0d0; border-radius: 10px; box-shadow: 0 8px 30px rgba(0,0,0,.18);
  z-index: 10001; display: none; font-size: 0.9em; }
#lcx-edit.open { display: block; }
#lcx-edit h4 { margin: 0; padding: .55em .9em; background: #f3f4f6; border-bottom: 1px solid #e0e0e0;
  font-family: ui-monospace, Menlo, monospace; font-size: .85em; }
#lcx-edit .lcx-body { padding: .6em .9em; }
#lcx-edit label { display: block; color: #666; font-size: .78em; margin: .5em 0 .12em; }
#lcx-edit input, #lcx-edit textarea { width: 100%; box-sizing: border-box; padding: .35em .5em;
  border: 1px solid #d0d0d0; border-radius: 5px; font: inherit; }
#lcx-edit textarea { font-family: ui-monospace, Menlo, monospace; min-height: 84px; resize: vertical; }
#lcx-edit .lcx-bar { display: flex; gap: .5em; padding: .55em .9em; border-top: 1px solid #e0e0e0; }
#lcx-edit button { font: inherit; padding: .35em .8em; border-radius: 5px; border: 1px solid #cbd5e1; background: #fff; cursor: pointer; }
#lcx-edit .lcx-apply { background: #0066cc; color: #fff; border-color: #0066cc; }
#lcx-edit .lcx-save { color: #8a5a00; background: #fff5d6; border-color: #f0d38a; margin-left: auto; }
#lcx-gear { position: fixed; z-index: 9000; display: none; width: 26px; height: 26px; padding: 0;
  border-radius: 50%; border: 1px solid #cbd5e1; background: rgba(255,255,255,.92);
  box-shadow: 0 2px 8px rgba(0,0,0,.18); cursor: pointer; font-size: 14px; line-height: 24px; text-align: center; }
#lcx-gear:hover { background: #eef4ff; border-color: #0066cc; }
</style>
<button id="lcx-gear" title="Edit this ✎" aria-label="Edit this component">⚙️</button>
<div id="lcx-edit">
  <h4 id="lcx-edit-title">Edit</h4>
  <div class="lcx-body" id="lcx-edit-body"></div>
  <div class="lcx-bar">
    <button class="lcx-apply" id="lcx-apply">Apply</button>
    <button id="lcx-close">Close</button>
    <button class="lcx-save" id="lcx-save" title="Create an account to keep changes">🔒 Save</button>
  </div>
</div>
<script>
(function () {
  if (window._lcxEditReady) return; window._lcxEditReady = true;
  var panel, curId, curSrc;

  function parseSrc(html) { var t = document.createElement("div"); t.innerHTML = html; return t.firstElementChild; }

  function open(el) {
    var id = el.getAttribute("data-lc-id") || el.id; if (!id) return;
    var src = window.lcSourceOf && window.lcSourceOf(id); if (!src) return;
    var srcEl = parseSrc(src); if (!srcEl) return;
    curId = id; curSrc = src;
    var body = document.getElementById("lcx-edit-body"); body.innerHTML = "";
    Array.prototype.forEach.call(srcEl.attributes, function (a) {
      if (a.name === "id" || a.name === "class" || a.name.indexOf("data-") === 0) return;
      var lab = document.createElement("label"); lab.textContent = a.name;
      var inp = document.createElement("input"); inp.value = a.value; inp.setAttribute("data-knob", a.name);
      body.appendChild(lab); body.appendChild(inp);
    });
    var codeEl = srcEl.querySelector("code") || srcEl;
    var clab = document.createElement("label"); clab.textContent = "content";
    var ta = document.createElement("textarea"); ta.id = "lcx-content";
    ta.value = (codeEl.textContent || "").replace(/\n$/, "");
    body.appendChild(clab); body.appendChild(ta);
    var cls = (srcEl.className || "").split(" ").filter(function (c) { return c && c !== "highlighter-rouge" && c.indexOf("language-") !== 0; })[0] || id;
    document.getElementById("lcx-edit-title").textContent = "✏️ ." + cls + "  #" + id;
    panel.classList.add("open");
  }

  function apply() {
    try {
      var srcEl = parseSrc(curSrc);
      Array.prototype.forEach.call(document.querySelectorAll("#lcx-edit-body input[data-knob]"), function (inp) {
        srcEl.setAttribute(inp.getAttribute("data-knob"), inp.value);
      });
      var code = srcEl.querySelector("code");
      var val = document.getElementById("lcx-content").value;
      if (code) code.textContent = val + "\n"; else srcEl.textContent = val;
      var widget = document.querySelector("[data-lc-id='" + curId + "']")
                || document.getElementById("lc-form-" + curId) || document.getElementById(curId);
      if (widget && widget.parentNode) {
        widget.parentNode.replaceChild(srcEl, widget);
        if (window.lcScanElement) window.lcScanElement(srcEl.parentNode);
      }
    } catch (e) { if (window.console) console.warn("[lcx-edit]", e); }
  }

  function boot() {
    panel = document.getElementById("lcx-edit");
    document.getElementById("lcx-close").addEventListener("click", function () { panel.classList.remove("open"); });
    document.getElementById("lcx-apply").addEventListener("click", apply);
    document.getElementById("lcx-save").addEventListener("click", function () {
      alert("Nothing's saved — reload and it's gone. Create an account to keep your changes.");
    });
    document.addEventListener("click", function (e) {
      if (!(window.lcxIsActive && window.lcxIsActive())) return;       // only while X-ray is on
      if (panel.contains(e.target)) return;
      var el = e.target.closest("[data-lc-id]"); if (!el) return;
      if (!(window.lcSourceOf && window.lcSourceOf(el.getAttribute("data-lc-id") || el.id))) return;
      e.preventDefault(); e.stopPropagation();
      open(el);
    }, true);

    // ── Gear affordance ──────────────────────────────────────────────────────
    // Hover any editable component → a ⚙️ appears at its top-right corner; click
    // it to open this dialog. No Alt-lens needed (the lens is transient on
    // desktop, so click-to-edit was effectively invisible there).
    var gear = document.getElementById("lcx-gear"), gearFor = null, hideT = null;
    function editableAt(node) {
      var el = node && node.closest ? node.closest("[data-lc-id]") : null;
      while (el) {
        var id = el.getAttribute("data-lc-id");
        if (id && window.lcSourceOf && window.lcSourceOf(id)) return el;
        var par = el.parentElement;
        el = par && par.closest ? par.closest("[data-lc-id]") : null;
      }
      return null;
    }
    function placeGear(el) {
      var r = el.getBoundingClientRect();
      gear.style.left = Math.min(window.innerWidth - 32, r.right - 30) + "px";
      gear.style.top  = Math.max(6, r.top + 6) + "px";
      gear.style.display = "block";
    }
    function hideGear() { gear.style.display = "none"; gearFor = null; }
    function keepGear() { if (hideT) { clearTimeout(hideT); hideT = null; } }
    function scheduleHide() { keepGear(); hideT = setTimeout(hideGear, 260); }
    document.addEventListener("pointermove", function (e) {
      if (panel.classList.contains("open")) return;      // dialog open: leave the gear alone
      if (e.target === gear) { keepGear(); return; }
      var comp = editableAt(e.target);
      if (comp) { keepGear(); gearFor = comp; placeGear(comp); }
      else scheduleHide();
    });
    gear.addEventListener("mouseenter", keepGear);
    gear.addEventListener("mouseleave", scheduleHide);
    gear.addEventListener("click", function (e) {
      e.preventDefault(); e.stopPropagation();
      if (gearFor) open(gearFor);
    });
    window.addEventListener("scroll", hideGear, true);
  }
  if (document.readyState !== "loading") boot(); else document.addEventListener("DOMContentLoaded", boot);
})();
</script>
