{%- comment -%}
X-ray edit — hover (or tap) any part of the page: its "ghost" outline appears
with a ⚙️ badge on the corner. Click the gear to edit that block in a modal.
Works for EVERY top-level markdown block (paragraphs, headings, lists, code)
and for components (knobs + content, re-rendered live). Nothing is saved —
"Keep changes" leads to account creation, which is the whole incentive; reload
loses everything. A component's editable source comes from window.lcSourceOf
(code_chrome); a plain block is edited in place. Auto-included by default.html.
{%- endcomment -%}

<style>
#lcx-ghost { position: fixed; z-index: 99995; display: none; pointer-events: none;
  border: 1.5px dashed rgba(0,102,204,.55); border-radius: 6px; background: rgba(0,102,204,.06); }
#lcx-gear { position: fixed; z-index: 100001; display: none; width: 26px; height: 26px; padding: 0;
  border-radius: 50%; border: 1px solid #0066cc; background: #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,.22); cursor: pointer; font-size: 14px; line-height: 24px; text-align: center; }
#lcx-gear:hover { background: #eef4ff; }
/* resizable: drag the corner to fit a long edit — width AND height */
#lcx-edit { width: min(560px, 92vw); max-height: 90vh; overflow: auto; padding: 0;
  border: none; border-radius: 12px; box-shadow: 0 18px 60px rgba(0,0,0,.32);
  resize: both; min-width: 320px; min-height: 240px; }
#lcx-edit::backdrop { background: rgba(15,23,42,.35); }
#lcx-edit h4 { margin: 0; padding: .7em 1em; background: #f3f4f6; border-bottom: 1px solid #e5e7eb;
  font-family: ui-monospace, Menlo, monospace; font-size: .9em; }
#lcx-edit .lcx-body { padding: .8em 1em; }
#lcx-edit label { display: block; color: #555; font-size: .8em; margin: .7em 0 .18em; }
#lcx-edit input, #lcx-edit textarea { width: 100%; box-sizing: border-box; padding: .45em .6em;
  border: 1px solid #cbd5e1; border-radius: 6px; font: inherit; }
#lcx-edit input[type=checkbox] { width: auto; height: 1.35em; margin: .2em 0; }
/* the editable content is a dark "workshop" surface — same as the page
   editor's Content/Raw field, so every text editor reads consistently */
#lcx-edit textarea { font-family: ui-monospace, Menlo, monospace; min-height: 120px; resize: vertical;
  background: #1e1e2e; color: #cdd6f4; caret-color: #89b4fa; border-color: #45475a; }
#lcx-edit textarea::placeholder { color: #6c7086; }
#lcx-edit .lcx-bar { display: flex; gap: .55em; padding: .7em 1em; border-top: 1px solid #e5e7eb; background: #fafafa; }
#lcx-edit button { font: inherit; padding: .45em .9em; border-radius: 7px; border: 1px solid #cbd5e1; background: #fff; cursor: pointer; }
#lcx-edit .lcx-apply { background: #0066cc; color: #fff; border-color: #0066cc; }
#lcx-edit .lcx-keep { color: #166534; background: #dcfce7; border-color: #86efac; margin-left: auto; }
#lcx-toast { position: fixed; top: 1em; left: 50%; transform: translateX(-50%);
  padding: 0.55em 1.1em; border-radius: 6px; font-size: 0.88em; font-weight: 500; color: #fff;
  z-index: 100002; display: none; box-shadow: 0 3px 10px rgba(0,0,0,0.15); pointer-events: none; }
</style>

<div id="lcx-ghost"></div>
<button id="lcx-gear" title="Edit this ✎" aria-label="Edit this block">⚙️</button>
<dialog id="lcx-edit">
  <h4 id="lcx-edit-title">Edit</h4>
  <div class="lcx-body" id="lcx-edit-body"></div>
  <div class="lcx-bar">
    <button type="button" class="lcx-apply" id="lcx-apply">Apply</button>
    <button type="button" id="lcx-close">Close</button>
    <button type="button" class="lcx-keep" id="lcx-keep" title="Save — commits to your repo when connected">💾 Save</button>
  </div>
</dialog>
<div id="lcx-toast"></div>

<script>
(function () {
  if (window._lcxEditReady) return; window._lcxEditReady = true;
  var MAIN, ghost, gear, dlg, hideT = null, ghostEl = null;
  var curEl = null, curId = "", curSnap = "", isComponent = false;

  var FRIENDLY = { P: "text", H1: "heading", H2: "heading", H3: "heading", H4: "heading", H5: "heading", H6: "heading",
    LI: "list item", PRE: "code", BLOCKQUOTE: "quote", FIGURE: "figure", TABLE: "table", DT: "term", DD: "definition" };

  function parseSrc(html) { var t = document.createElement("div"); t.innerHTML = html; return t.firstElementChild; }
  // Render a knob as the control its value implies: bool → checkbox,
  // int/float → number (step from the decimals), everything else → text.
  function knobInput(name, value) {
    var v = (value || "").trim(), inp;
    if (/^(true|false)$/i.test(v)) {
      inp = document.createElement("input"); inp.type = "checkbox"; inp.checked = /^true$/i.test(v);
    } else if (/^-?\d+$/.test(v)) {
      inp = document.createElement("input"); inp.type = "number"; inp.step = "1"; inp.value = v; inp.inputMode = "numeric";
    } else if (/^-?\d*\.\d+$/.test(v)) {
      inp = document.createElement("input"); inp.type = "number"; inp.value = v; inp.inputMode = "decimal";
      inp.step = String(1 / Math.pow(10, v.split(".")[1].length));
    } else {
      inp = document.createElement("input"); inp.type = "text"; inp.value = value;
    }
    inp.setAttribute("data-knob", name);
    inp.dataset.orig = v;   // remembered so Keep knows whether knobs changed
    return inp;
  }
  function openDlg() { if (dlg.open) return; if (dlg.showModal) dlg.showModal(); else dlg.setAttribute("open", ""); }
  function closeDlg() { if (dlg.close) dlg.close(); else dlg.removeAttribute("open"); }
  // Fire on pointerdown (not click): a tap that dismisses the on-screen keyboard
  // shifts the layout, so the follow-up click can miss the button entirely.
  function onTap(btn, fn) {
    var lock = false;
    function run(e) { if (lock) return; lock = true; setTimeout(function () { lock = false; }, 400);
      e.preventDefault(); e.stopPropagation(); fn(); }
    btn.addEventListener("pointerdown", run);
    btn.addEventListener("click", run);   // fallback for engines without pointer events
  }

  // The tightest editable block under a node: a component if we're inside one,
  // otherwise the nearest basic block (paragraph, heading, list item, code…).
  // NOT the coarse <section>/<div> container that wraps them.
  var BLOCK_SEL = "p,h1,h2,h3,h4,h5,h6,li,pre,blockquote,figure,table,dt,dd";
  function blockAt(node) {
    if (!MAIN || !node) return null;
    if (node === gear || node === ghost || (dlg && dlg.contains(node))) return null;
    var el = node.nodeType === 1 ? node : node.parentElement;
    if (!el || !el.closest) return null;
    /* read-only render (the Library / vault): no gear, no editing at all */
    if (el.closest(".lc-run[data-lc-readonly]")) return null;
    var comp = el.closest("[data-lc-id]");
    if (comp && MAIN.contains(comp)) return comp;
    var blk = el.closest(BLOCK_SEL);
    if (!blk || !MAIN.contains(blk)) return null;
    var r = blk.getBoundingClientRect();
    if (r.width < 4 || r.height < 4) return null;   // skip collapsed/empty blocks
    return blk;
  }

  function showGhost(el) {
    ghostEl = el;
    var r = el.getBoundingClientRect();
    ghost.style.left = (r.left - 3) + "px";
    ghost.style.top = (r.top - 3) + "px";
    ghost.style.width = (r.width + 6) + "px";
    ghost.style.height = (r.height + 6) + "px";
    ghost.style.display = "block";
    gear.style.left = Math.min(window.innerWidth - 30, r.right - 13) + "px";   // badge on the corner
    gear.style.top = Math.max(2, r.top - 13) + "px";
    gear.style.display = "block";
  }
  function hideGhost() { ghost.style.display = "none"; gear.style.display = "none"; ghostEl = null; }
  function keep() { if (hideT) { clearTimeout(hideT); hideT = null; } }
  function scheduleHide() { keep(); hideT = setTimeout(hideGhost, 320); }

  // Edit affordance lives only inside X-ray mode: Option/Alt held (desktop) or
  // the X-ray toggle on (touch). Otherwise the page reads clean, no gears.
  function xrayActive(e) {
    if (e && e.altKey) return true;
    return !!(window.lcxIsActive && window.lcxIsActive());
  }
  function track(e) {
    if (dlg && dlg.open) return;
    if (!xrayActive(e)) { if (e.target !== gear) hideGhost(); return; }   // stay if the pointer is on the gear
    if (e.target === gear || e.target === ghost) { keep(); return; }
    var b = blockAt(e.target);
    if (b) { keep(); showGhost(b); } else scheduleHide();
  }

  function open(block) {
    if (!block) return;
    curEl = block;
    curId = (block.getAttribute && (block.getAttribute("data-lc-id") || block.id)) || "";
    curSnap = (curId && window.lcSourceOf && window.lcSourceOf(curId)) || "";
    isComponent = !!curSnap;
    var srcEl = isComponent ? parseSrc(curSnap) : block;
    if (!srcEl) return;

    var body = document.getElementById("lcx-edit-body"); body.innerHTML = "";
    if (isComponent) {
      Array.prototype.forEach.call(srcEl.attributes, function (a) {
        if (a.name === "id" || a.name === "class" || a.name.indexOf("data-") === 0) return;
        var lab = document.createElement("label"); lab.textContent = a.name;
        body.appendChild(lab); body.appendChild(knobInput(a.name, a.value));
      });
    }
    var clab = document.createElement("label"); clab.textContent = "content";
    var ta = document.createElement("textarea"); ta.id = "lcx-content"; ta.setAttribute("autofocus", "");
    if (isComponent) {
      var codeEl = srcEl.querySelector("code") || srcEl;
      ta.value = (codeEl.textContent || "").replace(/\n$/, "");
    } else {
      ta.value = (block.textContent || "").trim();   // plain text — never raw HTML
    }
    body.appendChild(clab); body.appendChild(ta);
    _origVal = ta.value;   // Keep's exact-match anchor into the page source

    var name = isComponent
      ? "." + ((srcEl.className || "").split(" ").filter(function (c) { return c && c !== "highlighter-rouge" && c.indexOf("language-") !== 0; })[0] || curId)
      : (FRIENDLY[block.tagName] || block.tagName.toLowerCase());
    document.getElementById("lcx-edit-title").textContent = "✏️ " + name + (isComponent && curId ? "  #" + curId : "");

    hideGhost();
    openDlg();                                     // modal top-layer → focus works, page handlers can't interfere
    setTimeout(function () { ta.focus(); }, 0);
  }

  function apply() {
    try {
      var val = document.getElementById("lcx-content").value;
      if (isComponent) {
        var srcEl = parseSrc(curSnap);
        Array.prototype.forEach.call(document.querySelectorAll("#lcx-edit-body input[data-knob]"), function (inp) {
          var val = inp.type === "checkbox" ? (inp.checked ? "true" : "false") : inp.value;
          srcEl.setAttribute(inp.getAttribute("data-knob"), val);
        });
        var code = srcEl.querySelector("code");
        if (code) code.textContent = val + "\n"; else srcEl.textContent = val;
        var widget = document.querySelector("[data-lc-id='" + curId + "']") || document.getElementById(curId);
        if (widget && widget.parentNode) {
          widget.parentNode.replaceChild(srcEl, widget);
          if (window.lcScanElement) window.lcScanElement(srcEl.parentNode);
        }
      } else if (curEl) {
        curEl.textContent = val;                  // plain block: edit its text in place
      }
    } catch (e) { if (window.console) console.warn("[lcx-edit]", e); }
  }

  var _origVal = null;

  /* Connected builders commit inline edits for real — fence surgery on the
     page's own source, exact-match-or-abort so it can never corrupt a page.
     The account invitation is only for anonymous learners (losing work is
     their incentive to sign up). */
  /* never let a non-JSON body (proxy page, empty response) crash as a bare
     JSON.parse alert — surface the HTTP status and a snippet instead, so a
     failure report is diagnosable */
  function jsonOf(r) {
    return r.text().then(function (t) {
      try { return JSON.parse(t); }
      catch (e) { throw new Error("HTTP " + r.status + (t ? " — " + t.slice(0, 120) : " (empty response)")); }
    });
  }

  /* same voice as the page editor: green = saved, red = why not */
  function lcxToast(msg, ok) {
    var el = document.getElementById("lcx-toast");
    if (!el) return;
    el.textContent = msg;
    el.style.background = ok ? "#28a745" : "#dc3545";
    el.style.display = "block";
    clearTimeout(el._t);
    el._t = setTimeout(function () { el.style.display = "none"; }, 3000);
  }

  function commitInline(pat, repo, path, before, after, label, onOk) {
    var api = "https://api.github.com/repos/" + repo + "/contents/" + path;
    var H = { Authorization: "Bearer " + pat, Accept: "application/vnd.github+json" };
    /* no-store: the runner fetches this same URL with Accept raw — some
       browsers (FF desktop) serve that cached raw body to THIS json request
       (Vary mishandling), which read raw markdown where the envelope should
       be. A read-before-write must be fresh anyway. */
    fetch(api, { headers: H, cache: "no-store" }).then(jsonOf).then(function (d) {
      if (!d.content) throw new Error(d.message || "load failed");
      var src = decodeURIComponent(escape(atob(d.content.replace(/\n/g, ""))));
      var i = src.indexOf(before);
      if (i < 0 || src.indexOf(before, i + 1) >= 0) {  // zero or many — never guess
        lcxToast("Couldn't safely locate this block in the page source — save it via the ✏️ page editor.", false);
        return;
      }
      var next = src.slice(0, i) + after + src.slice(i + before.length);
      return fetch(api, {
        method: "PUT", headers: H,
        body: JSON.stringify({ message: "Inline edit: " + label,
                               content: btoa(unescape(encodeURIComponent(next))), sha: d.sha })
      }).then(jsonOf).then(function (res) {
        if (!res.content) throw new Error(res.message || "unknown");
        if (onOk) onOk(res.commit && res.commit.sha);
      });
    }).catch(function (e) { lcxToast("Save failed: " + e.message, false); });
  }

  function keepChanges() {
    /* Inside a runner render the true source is the RENDERED file (the /run
       page itself has no_edit and knows nothing) — the runner stamps it on
       its root. Resolve BEFORE apply(): re-rendering a component detaches
       curEl, and closest() on a detached node finds no ancestors. */
    var runRoot = curEl && curEl.closest ? curEl.closest(".lc-run[data-lc-src-path]") : null;
    apply();
    var pat = localStorage.getItem("lc_ed_pat"), repo = localStorage.getItem("lc_ed_repo");
    var fabEl = document.getElementById("ed-fab");
    var pagePath = fabEl && fabEl.dataset ? fabEl.dataset.pagePath : "";
    var ta = document.getElementById("lcx-content");
    var commitRepo = (runRoot && runRoot.dataset.lcSrcRepo) || repo;
    var commitPath = runRoot ? runRoot.dataset.lcSrcPath : (pagePath ? "docs/" + pagePath : "");
    if (pat && commitRepo && commitPath && ta && _origVal) {
      var knobsChanged = Array.prototype.some.call(
        document.querySelectorAll("#lcx-edit-body input[data-knob]"),
        function (inp) {
          var cur = inp.type === "checkbox" ? (inp.checked ? "true" : "false") : (inp.value || "").trim();
          return cur !== (inp.dataset.orig || "");
        });
      if (ta.value !== _origVal) {
        var label = ((document.getElementById("lcx-edit-title") || {}).textContent || "block").replace(/^✏️\s*/, "");
        /* on confirmed commit, refresh the fence snapshot so the NEXT edit
           anchors on the committed content — without this a second Keep after
           a successful one can't match the file until a reload (stale anchor) */
        var okId = curId, okSnap = curSnap, okVal = ta.value;
        commitInline(pat, commitRepo, commitPath, _origVal, ta.value, label, function (sha) {
          lcxToast("Saved" + (sha ? " · " + String(sha).slice(0, 7) : "") + " ✓", true);
          if (!okId || !window.lcSetSourceOf) return;
          var s = parseSrc(okSnap); if (!s) return;
          var c = s.querySelector("code");
          if (c) c.textContent = okVal + "\n"; else s.textContent = okVal;
          window.lcSetSourceOf(okId, s.outerHTML);
        });
      }
      if (knobsChanged) alert("Knob changes aren't committed inline yet — keep them via the ✏️ page editor.");
      closeDlg();
      return;
    }
    var go = window.confirm("Your changes live only in this browser — reload and they're gone.\n\nCreate an account to keep them?");
    /* the onboarding journey moved to the private courses/ tier; the public
       entry for anonymous learners is now the courses landing */
    if (go) location.href = window.lcResolveUrl ? window.lcResolveUrl("/courses/") : "/courses/";
  }

  function boot() {
    MAIN = document.querySelector("main.markdown-body") || document.querySelector("main");
    ghost = document.getElementById("lcx-ghost");
    gear = document.getElementById("lcx-gear");
    dlg = document.getElementById("lcx-edit");
    onTap(document.getElementById("lcx-close"), closeDlg);
    onTap(document.getElementById("lcx-apply"), apply);
    onTap(document.getElementById("lcx-keep"), keepChanges);
    dlg.addEventListener("click", function (e) { if (e.target === dlg) closeDlg(); });   // click backdrop to close

    document.addEventListener("pointermove", track);
    document.addEventListener("pointerdown", track);   // reveal on tap (touch has no hover)
    gear.addEventListener("pointerenter", keep);
    gear.addEventListener("pointerleave", scheduleHide);
    function activate(e) { e.preventDefault(); e.stopPropagation(); if (ghostEl) open(ghostEl); }
    gear.addEventListener("pointerdown", activate);   // fire on pointerdown so nothing can swallow it
    gear.addEventListener("click", activate);         // fallback for engines without pointer events
    window.addEventListener("scroll", hideGhost, true);
    window.addEventListener("resize", hideGhost);
  }
  if (document.readyState !== "loading") boot(); else document.addEventListener("DOMContentLoaded", boot);
})();
</script>
