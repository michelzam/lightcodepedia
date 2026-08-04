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
/* resizable, and the CONTENT follows: drag the corner and the text field
   takes every pixel the header and the button bar do not need — a taller
   box that still showed a 120px slot was the wrong kind of resizable. */
#lcx-edit { width: min(560px, 92vw); height: 60vh; max-height: 90vh; max-width: 96vw;
  overflow: hidden; padding: 0;
  border: none; border-radius: 12px; box-shadow: 0 18px 60px rgba(0,0,0,.32);
  resize: both; min-width: 320px; min-height: 240px; }
#lcx-edit[open] { display: flex; flex-direction: column; }
#lcx-edit h4, #lcx-edit .lcx-bar { flex: none; }
#lcx-edit::backdrop { background: rgba(15,23,42,.35); }
#lcx-edit h4 { margin: 0; padding: .7em 1em; background: #f3f4f6; border-bottom: 1px solid #e5e7eb;
  font-family: ui-monospace, Menlo, monospace; font-size: .9em; }
#lcx-edit .lcx-body { padding: .8em 1em; flex: 1 1 auto; overflow: auto;
  display: flex; flex-direction: column; min-height: 0; }
#lcx-edit label { display: block; color: #555; font-size: .8em; margin: .7em 0 .18em; }
#lcx-edit input, #lcx-edit textarea { width: 100%; box-sizing: border-box; padding: .45em .6em;
  border: 1px solid #cbd5e1; border-radius: 6px; font: inherit; }
#lcx-edit input[type=checkbox] { width: auto; height: 1.35em; margin: .2em 0; }
/* the editable content is a dark "workshop" surface — same as the page
   editor's Content/Raw field, so every text editor reads consistently */
#lcx-edit textarea { font-family: ui-monospace, Menlo, monospace; min-height: 120px;
  flex: 1 1 auto; resize: none;      /* the DIALOG is the handle now */
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
    /* Read-only is NEAREST-WINS, not any-ancestor: a vault lesson can hold
       a bench slot ({: .embed save="…" }), and inside that slot the nearest
       source is the learner's own repo. "Uneditable" must mean "unless a
       nearer source says otherwise" — the nearest source is the truth about
       what you are actually editing. */
    var near = el.closest(".lc-run[data-lc-src-path], .lc-run[data-lc-readonly]");
    if (near && near.hasAttribute("data-lc-readonly")) return null;
    if (!near && el.closest(".lc-run[data-lc-readonly]")) return null;
    /* DERIVED content (folder cards, unlocks…) is generated from other
       files — there is nothing here to edit. The gear offers the SLOT
       (the .folder line in the page source), never its derivatives. */
    if (el.closest("[data-lc-derived]")) return null;
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

  /* Un-heal the project base before touching the FILE.

     Under a project base — the lab, any fork — root-relative URLs are healed
     in the DOM: /assets/lab.jpg becomes /lightcodelab/assets/lab.jpg. The
     x-ray captures the block FROM the DOM, so its anchor described a string
     that never existed in the source: zero hits, refuse, red. Pedia never saw
     it, because its base is empty — which is why this hid for hours.

     Both directions matter. Un-heal the anchor, or nothing is ever found; and
     un-heal what we WRITE, or the lab's base is committed into the markdown
     and pedia then serves /lightcodelab/assets/... to the world. */
  function unhealBase(text) {
    var b = window.lcBaseUrl;
    if (!b || !text) return text;
    var esc = b.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    return String(text).replace(new RegExp("([(\"'\\s])" + esc + "/", "g"), "$1/");
  }

  /* ── the two source transforms ───────────────────────────────────────
     What the editor can change in a markdown file: the TEXT of a block,
     and the KNOBS on its IAL line. Both are pure string→string, so the
     same rewrite serves the page's own file and a learner's bench file
     without a second, subtly different code path. null = refuse. */
  function replaceBlockIn(src, before, after, ordinal) {
    /* POSITION is the identity, not the text. Markdown without a fence has
       no unique delimiter, so "the text appears twice" is ordinary, not an
       edge case — and refusing there made Keep unusable on plain prose.
       When the same text occurs more than once, the caller says WHICH one
       by ordinal (the block's rank among identical blocks on the page), and
       we splice that range. Zero occurrences still refuses: that means the
       rendered text is not what the file holds, and no position can be
       inferred from it. */
    var hits = [], from = 0, at;
    while ((at = src.indexOf(before, from)) >= 0) { hits.push(at); from = at + 1; }
    var i = hits.length === 1 ? hits[0]
          : (hits.length > 1 && ordinal != null && hits[ordinal] != null) ? hits[ordinal]
          : -1;
    replaceBlockIn.hits = hits.length;
    if (i < 0) return null;
    return src.slice(0, i) + after + src.slice(i + before.length);
  }

  /* A knob lives on the IAL line that names the component:
       {: .datagrid #wired source="ozaukee" height="180" }
     Find the line carrying #id and rewrite the values that moved (adding a
     knob the author never wrote, if the learner filled an empty one). This
     is the wiring itself — the one thing a "connect the parts" lesson asks
     a learner to change, and until now the only edit Keep refused. */
  function setKnobsIn(src, id, knobs) {
    if (!id) return null;
    var lines = String(src).split("\n");
    var idRe = new RegExp("#" + id.replace(/[^\w-]/g, "") + "(?![\\w-])");
    var hit = -1;
    for (var i = 0; i < lines.length; i++) {
      if (lines[i].indexOf("{:") < 0 || !idRe.test(lines[i])) continue;
      hit = i; break;
    }
    if (hit < 0) return null;
    var line = lines[hit];
    Object.keys(knobs).forEach(function (k) {
      var val = String(knobs[k]);
      var re = new RegExp("(\\b" + k + '=")[^"]*(")');
      if (re.test(line)) line = line.replace(re, function (m, a, b) { return a + val + b; });
      else line = line.replace(/\s*\}\s*$/, " " + k + '="' + val + '" }');
    });
    lines[hit] = line;
    return lines.join("\n");
  }

  /* ONE edit, ONE transform. Text and knobs are both string→string rewrites,
     so a single function describes the whole edit and can then be pointed at
     either file that might hold it — the page's own source or a learner's
     bench. It also makes "retitled the block AND rewired it" one commit
     instead of two that race for the same sha. */
  function editTransform(opts) {
    /* The diagnostics ride ON the transform. commitTransform cannot know what
       a refusal was looking for, and discarding that fact — "couldn't locate"
       fits a dozen causes — cost three rounds of guessing once already. */
    var xf = function (src) {
      var out = String(src);
      if (opts.text) {
        var before = unhealBase(opts.text.before), after = unhealBase(opts.text.after);
        out = replaceBlockIn(out, before, after, opts.text.ordinal);
        xf.diag = { anchor: before.slice(0, 200), hits: replaceBlockIn.hits,
                    ordinal: opts.text.ordinal };
        if (out == null) return null;
      }
      if (opts.knobs) {
        var wired = setKnobsIn(out, opts.id, opts.knobs);
        if (wired == null) {
          /* no IAL line carries this #id — the knobs have nowhere to land */
          xf.diag = { anchor: "{: #" + (opts.id || "") + " }", hits: 0, ordinal: null };
          return null;
        }
        out = wired;
      }
      return out;
    };
    return xf;
  }

  function commitTransform(pat, repo, path, transform, label, onOk) {
    var api = "https://api.github.com/repos/" + repo + "/contents/" + path;
    var H = { Authorization: "Bearer " + pat, Accept: "application/vnd.github+json" };
    /* no-store: the runner fetches this same URL with Accept raw — some
       browsers (FF desktop) serve that cached raw body to THIS json request
       (Vary mishandling), which read raw markdown where the envelope should
       be. A read-before-write must be fresh anyway. */
    fetch(api, { headers: H, cache: "no-store" }).then(jsonOf).then(function (d) {
      if (!d.content) throw new Error(d.message || "load failed");
      var src = decodeURIComponent(escape(atob(d.content.replace(/\n/g, ""))));
      var next;
      try { next = transform(src); } catch (e) { next = null; }
      if (next == null) {
        var tEl = document.getElementById("lcx-toast"), dg = transform.diag || {};
        if (tEl) {
          tEl.dataset.lcAnchor = JSON.stringify(dg.anchor == null ? "" : dg.anchor);
          tEl.dataset.lcHits = String(dg.hits);
          tEl.dataset.lcOrdinal = String(dg.ordinal);
        }
        lcxToast("Couldn't safely locate this block in the page source — save it via the ✏️ page editor.", false);
        return;
      }
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

  /* the text-only door, kept thin so every existing caller is unaffected */
  function commitInline(pat, repo, path, before, after, label, onOk, ordinal) {
    commitTransform(pat, repo, path,
      editTransform({ text: { before: before, after: after, ordinal: ordinal } }),
      label, onOk);
  }

  /* Shared so other components can write a block back without growing a
     second, subtly different commit path. lcSourceTarget resolves what a page
     actually IS: inside a runner render the true source is the RENDERED file,
     not the /run page, which knows nothing about itself. */
  window.lcCommitInline = commitInline;
  window.lcSourceTarget = function (fromEl) {
    var runRoot = fromEl && fromEl.closest ? fromEl.closest(".lc-run[data-lc-src-path]") : null;
    if (!runRoot) runRoot = document.querySelector(".lc-run[data-lc-src-path]");
    var fabEl = document.getElementById("ed-fab");
    var pagePath = fabEl && fabEl.dataset ? fabEl.dataset.pagePath : "";
    var repo = (runRoot && runRoot.dataset.lcSrcRepo) || localStorage.getItem("lc_ed_repo") || "";
    var path = runRoot ? runRoot.dataset.lcSrcPath : (pagePath ? "docs/" + pagePath : "");
    var readonly = !!(runRoot && runRoot.dataset.lcReadonly) ||
                   !!(window.lcFrame && window.lcFrame.editable === false);
    return { repo: repo, path: path, readonly: readonly,
             pat: localStorage.getItem("lc_ed_pat") || "" };
  };
  window.lcxToast = lcxToast;

  /* ── the bench door — the learner's OWN repo, whole files ────────────────
     lcCommitInline writes a block back into the page it came from; lcBench
     writes a FILE into the learner's connected repo. Different question:
     the page is the author's (vault — no student write), the work is the
     student's. save="my/cv.md" on a block means "this block's content
     persists HERE, in whoever-is-reading's bench". One reader/writer pair,
     used by every component with a save= knob, so the contract cannot
     drift: fence = the author's seed, bench file = the learner's truth. */
  window.lcBench = {
    /* WHICH bench? The learner's OWN connected space — ALWAYS, and never the
       repo the page happens to render from. Canvas gives the whole class ONE
       url (the session hub); prefer the render root and every student's save
       aims at a shared repo none of them may write. The page is where you
       stand; my/ is where you live. (A first version preferred the render
       root — reverted 2026-08-03 after exactly that Canvas failure.) The
       repo and key are a PAIR set together at join; if the key does not
       cover the repo, the write error below says so by name. */
    target: function (fromEl) {
      return { repo: localStorage.getItem("lc_ed_repo") || "",
               pat: localStorage.getItem("lc_ed_pat") || "" };
    },
    /* WHERE in the bench? The author's spelling decides the shelf:
         save="dogs.yaml"        → beside the lesson — the page's own folder,
                                   FULL course path (courses/…/module_00/),
                                   so two courses in one bench never collide
         save="../shared/x.md"   → climbs the course tree, like prereq hrefs
         save="/my/cv.md"        → bench root — the personal files that
                                   outlive one lesson
       One resolution grammar with the prerequisite links: relative means
       "against the rendered source". Outside a runner render there is no
       lesson folder, so relative falls back to the bench root. */
    resolve: function (path, fromEl) {
      path = String(path || "").trim();
      var abs = path.charAt(0) === "/";
      var runRoot = fromEl && fromEl.closest ? fromEl.closest(".lc-run[data-lc-src-path]") : null;
      var srcPath = (!abs && runRoot && runRoot.dataset.lcSrcPath) || "";
      var dir = srcPath.indexOf("/") >= 0 ? srcPath.replace(/\/[^\/]*$/, "") : "";
      var out = [];
      ((abs ? path : (dir ? dir + "/" + path : path)).split("/")).forEach(function (p) {
        if (!p || p === ".") return;
        if (p === "..") out.pop();
        else out.push(p);
      });
      return out.join("/");
    },
    read: function (path, fromEl) {    /* → {text, sha} | null (no file yet) */
      var t = this.target(fromEl);
      path = this.resolve(path, fromEl);
      if (!t.repo || !t.pat) return Promise.resolve(null);
      return fetch("https://api.github.com/repos/" + t.repo + "/contents/" + path,
        { headers: { Authorization: "Bearer " + t.pat, Accept: "application/vnd.github+json" } })
        .then(function (r) {
          if (r.status === 404) return null;
          if (!r.ok) throw new Error("HTTP " + r.status);
          return r.json();
        })
        .then(function (j) {
          if (!j || !j.content) return null;
          return { text: decodeURIComponent(escape(atob(String(j.content).replace(/\s/g, "")))),
                   sha: j.sha };
        });
    },
    /* ── versions ────────────────────────────────────────────────────────
       The learner's bench IS git, so the history already exists — it only
       lacked a door. Every 💾 is a commit; these two read them back, so a
       saved block can show what changed and when, and bring an old draft
       back. Learners watch version control exist before anyone says the
       word (and an audit can see that they iterated, which no screenshot
       can fake). */
    history: function (path, fromEl, limit) {   /* → [{sha, when, message}] */
      var t = this.target(fromEl);
      if (!t.repo || !t.pat) return Promise.resolve([]);
      var p = this.resolve(path, fromEl);
      return fetch("https://api.github.com/repos/" + t.repo + "/commits?path="
                   + encodeURIComponent(p) + "&per_page=" + (limit || 20),
        { headers: { Authorization: "Bearer " + t.pat, Accept: "application/vnd.github+json" } })
        .then(function (r) { return r.ok ? r.json() : []; })
        .then(function (list) {
          return (Array.isArray(list) ? list : []).map(function (c) {
            return { sha: c.sha,
                     when: ((c.commit || {}).author || {}).date || "",
                     message: ((c.commit || {}).message || "").split("\n")[0] };
          });
        })
        .catch(function () { return []; });
    },
    readAt: function (path, sha, fromEl) {      /* → text | null */
      var t = this.target(fromEl);
      if (!t.repo || !t.pat) return Promise.resolve(null);
      var p = this.resolve(path, fromEl);
      return fetch("https://api.github.com/repos/" + t.repo + "/contents/" + p
                   + "?ref=" + encodeURIComponent(sha),
        { headers: { Authorization: "Bearer " + t.pat,
                     Accept: "application/vnd.github.v3.raw" } })
        .then(function (r) { return r.ok ? r.text() : null; })
        .catch(function () { return null; });
    },
    write: function (path, text, message, sha, fromEl, _retried) {   /* → new sha */
      var t = this.target(fromEl), self = this;
      if (!t.repo || !t.pat) return Promise.reject(new Error("no bench connected"));
      path = this.resolve(path, fromEl);
      var body = { message: message || ("✍️ " + path),
                   content: btoa(unescape(encodeURIComponent(text))) };
      if (sha) body.sha = sha;
      return fetch("https://api.github.com/repos/" + t.repo + "/contents/" + path,
        { method: "PUT",
          headers: { Authorization: "Bearer " + t.pat, Accept: "application/vnd.github+json",
                     "Content-Type": "application/json" },
          body: JSON.stringify(body) })
        .then(function (r) {
          /* stale sha (saved from another device since we loaded): take the
             live sha once and lay this text on top — same file, same owner,
             last write wins is the RIGHT rule for a one-person file */
          if ((r.status === 409 || r.status === 422) && !_retried) {
            /* "/"-prefixed: the path is already resolved — re-resolving a
               relative spelling here would prefix the lesson folder twice */
            return self.read("/" + path, fromEl).then(function (f) {
              return self.write("/" + path, text, message, f && f.sha, fromEl, true);
            });
          }
          /* GitHub says 404 for "repo exists but your key can't see it" —
             to a learner that reads as a missing file. Name the repo, so a
             key-grant gap is visible instead of mystifying. */
          if (r.status === 404) throw new Error("your key can't write to " + t.repo + " — reconnect with a key that covers your space");
          if (!r.ok) throw new Error("HTTP " + r.status);
          return r.json().then(function (j) { return (j.content && j.content.sha) || ""; });
        });
    }
  };

  /* ── 🕘 versions panel — ONE implementation, attached by a component in
     a single call. Deliberately isolated and deliberately dull to remove:
     deleting the lcVersions.attach(...) line takes the feature out of a
     component entirely, and deleting this block takes it out everywhere.
     Nothing else in the engine knows it exists (Michel 2026-08-03: low
     intrusion, easy undo). */
  /* the message a first save writes for the author's untouched starter —
     shared so the panel can recognise it, and so it reads correctly on
     GitHub too, not only in our list */
  window.lcStarterMsg = "📄 starter — before my first change";

  window.lcVersions = {
    attach: function (o) {
      /* o = { path, el, anchor, current(), apply(text), css, diff? }
         o.diff(box, olderText) is OPTIONAL: a component that knows its data
         is not lines (a grid's rows) renders the difference its own way.
         Without it, the line diff below is used. */
      var css = o.css || "lc-ver";
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = css + "-btn";
      btn.hidden = true;                    /* no file yet, no history */
      btn.textContent = "🕘 Versions";
      btn.title = "Every version you saved — read it, compare it, bring it back";
      var panel = null;
      function close() {
        if (panel && panel.parentNode) panel.parentNode.removeChild(panel);
        panel = null;
      }
      function whenLabel(iso) {
        if (!iso) return "saved";
        var d = new Date(iso);
        return isNaN(d) ? iso : d.toLocaleString();
      }
      /* line diff by longest-common-subsequence — small enough to stay
         honest, and readable: what that version said vs what you hold now */
      function diffLines(a, b) {
        var A = String(a).split("\n"), B = String(b).split("\n");
        var m = A.length, n = B.length, i, j, L = [];
        for (i = 0; i <= m; i++) L.push(new Array(n + 1).fill(0));
        for (i = m - 1; i >= 0; i--)
          for (j = n - 1; j >= 0; j--)
            L[i][j] = A[i] === B[j] ? L[i + 1][j + 1] + 1 : Math.max(L[i + 1][j], L[i][j + 1]);
        var out = []; i = 0; j = 0;
        while (i < m && j < n) {
          if (A[i] === B[j]) { out.push(["same", A[i]]); i++; j++; }
          else if (L[i + 1][j] >= L[i][j + 1]) { out.push(["del", A[i]]); i++; }
          else { out.push(["add", B[j]]); j++; }
        }
        while (i < m) { out.push(["del", A[i]]); i++; }
        while (j < n) { out.push(["add", B[j]]); j++; }
        return out;
      }
      function showDiff(box, older) {
        var rows = diffLines(older, o.current());
        box.innerHTML = "";
        rows.forEach(function (r) {
          var line = document.createElement("span");
          line.className = r[0];
          line.textContent = (r[0] === "add" ? "+ " : r[0] === "del" ? "- " : "  ") + r[1];
          box.appendChild(line);
        });
        if (!rows.some(function (r) { return r[0] !== "same"; }))
          box.textContent = "Identical to what you have now.";
      }
      btn.addEventListener("click", function () {
        if (panel) { close(); return; }
        panel = document.createElement("div");
        panel.className = css + "-panel";
        panel.innerHTML = "<ol><li>⏳ reading your history…</li></ol>";
        var at = o.anchor || btn.parentNode;
        at.parentNode.insertBefore(panel, at.nextSibling);
        window.lcBench.history(o.path, o.el).then(function (list) {
          if (!panel) return;
          if (!list.length) {
            panel.innerHTML = "<ol><li>No versions yet — 💾 writes the first one.</li></ol>";
            return;
          }
          var ol = document.createElement("ol");
          var box = document.createElement("div");
          box.className = css + "-diff"; box.hidden = true;
          list.forEach(function (c, n) {
            var li = document.createElement("li");
            /* the starter is the AUTHOR's text, not the learner's first
               draft — say so, or the oldest row misattributes the lesson */
            var isStarter = String(c.message || "").indexOf(window.lcStarterMsg) === 0;
            li.className = isStarter ? "starter" : (n === 0 ? "now" : "");
            var when = document.createElement("span");
            when.className = css + "-when";
            when.textContent = isStarter
              ? "the lesson's starter · " + whenLabel(c.when)
              : whenLabel(c.when) + (n === 0 ? " · latest" : "");
            var sha = document.createElement("span");
            sha.className = css + "-sha";
            sha.textContent = String(c.sha).slice(0, 7);
            var cmp = document.createElement("button");
            cmp.type = "button"; cmp.textContent = "compare";
            var use = document.createElement("button");
            use.type = "button"; use.textContent = "bring back";
            cmp.addEventListener("click", function () {
              cmp.textContent = "…";
              window.lcBench.readAt(o.path, c.sha, o.el).then(function (t) {
                cmp.textContent = "compare";
                if (t == null) { window.lcxToast && window.lcxToast("Could not read that version.", false); return; }
                box.hidden = false;
                box.innerHTML = "";
                (o.diff || showDiff)(box, t);
              });
            });
            use.addEventListener("click", function () {
              window.lcBench.readAt(o.path, c.sha, o.el).then(function (t) {
                if (t == null) { window.lcxToast && window.lcxToast("Could not read that version.", false); return; }
                o.apply(t); close();
                window.lcxToast && window.lcxToast("Older version loaded — 💾 to keep it", true);
              });
            });
            li.appendChild(when); li.appendChild(sha);
            li.appendChild(cmp); li.appendChild(use);
            ol.appendChild(li);
          });
          panel.innerHTML = ""; panel.appendChild(ol); panel.appendChild(box);
        });
      });
      return { button: btn, close: close,
               reveal: function () { btn.hidden = false; } };
    }
  };

  /* The knobs the learner actually moved, as {name: value}. This is the same
     walk that used to answer only "did anything change?" — the map is what a
     commit needs, and the boolean threw it away. */
  function changedKnobs() {
    var out = {}, any = false;
    Array.prototype.forEach.call(
      document.querySelectorAll("#lcx-edit-body input[data-knob]"),
      function (inp) {
        var cur = inp.type === "checkbox" ? (inp.checked ? "true" : "false") : (inp.value || "").trim();
        if (cur === (inp.dataset.orig || "")) return;
        out[inp.getAttribute("data-knob")] = cur; any = true;
      });
    return any ? out : null;
  }

  function keepChanges() {
    /* Inside a runner render the true source is the RENDERED file (the /run
       page itself has no_edit and knows nothing) — the runner stamps it on
       its root. Resolve BEFORE apply(): re-rendering a component detaches
       curEl, and closest() on a detached node finds no ancestors. */
    var runRoot = curEl && curEl.closest ? curEl.closest(".lc-run[data-lc-src-path]") : null;
    /* Same trap, same reason, one question later: which file owns this block?
       Inside a bench slot the answer is the learner's own, and after apply()
       the detached curEl can no longer be asked. */
    var slot = (window.lcBenchSlotOf && curEl) ? window.lcBenchSlotOf(curEl) : null;
    apply();
    var pat = localStorage.getItem("lc_ed_pat"), repo = localStorage.getItem("lc_ed_repo");
    var fabEl = document.getElementById("ed-fab");
    var pagePath = fabEl && fabEl.dataset ? fabEl.dataset.pagePath : "";
    var ta = document.getElementById("lcx-content");
    var commitRepo = (runRoot && runRoot.dataset.lcSrcRepo) || repo;
    var commitPath = runRoot ? runRoot.dataset.lcSrcPath : (pagePath ? "docs/" + pagePath : "");

    var knobs = changedKnobs();
    /* _origVal must be non-empty to anchor on: an empty needle matches at
       every offset, which is not a position at all. */
    var textChanged = !!(ta && _origVal && ta.value !== _origVal);
    if (!knobs && !textChanged) { closeDlg(); return; }   // nothing moved

    /* Which one of the identical blocks is this? Rank it among the page's
       blocks whose source text matches, so an ambiguous file position is
       resolved by WHERE the learner clicked, not by hoping for uniqueness. */
    var ordinal = null;
    if (textChanged) {
      try {
        var same = Array.prototype.filter.call(
          (MAIN || document).querySelectorAll(curEl ? curEl.tagName : "p"),
          function (n) { return (n.textContent || "").trim() === _origVal; });
        var k = same.indexOf(curEl);
        if (k >= 0) ordinal = k;
      } catch (e) {}
    }
    var label = ((document.getElementById("lcx-edit-title") || {}).textContent || "block").replace(/^✏️\s*/, "");
    var xf = editTransform({
      id: curId,
      knobs: knobs,
      text: textChanged ? { before: _origVal, after: ta.value, ordinal: ordinal } : null
    });

    /* A bench slot OWNS its file, so it does the writing: it creates the file
       the learner has never had, lays the author's starter down first so the
       first change is readable in 🕘, and repaints from what was saved.
       Routing this through commitTransform instead 404s on that first save. */
    if (slot) {
      slot.save(xf, "Inline edit: " + label).then(function (sha) {
        lcxToast("Saved" + (sha ? " · " + String(sha).slice(0, 7) : "") + " ✓", true);
      }).catch(function (e) {
        lcxToast("Save failed: " + (e && e.message ? e.message : e), false);
      });
      closeDlg();
      return;
    }

    if (pat && commitRepo && commitPath) {
      /* on confirmed commit, refresh the fence snapshot so the NEXT edit
         anchors on the committed content — without this a second Keep after
         a successful one can't match the file until a reload (stale anchor),
         and a second ⚙️ hands back the wire the learner already replaced */
      var okId = curId, okSnap = curSnap, okVal = ta ? ta.value : "";
      var okKnobs = knobs, okText = textChanged;
      commitTransform(pat, commitRepo, commitPath, xf, label, function (sha) {
        lcxToast("Saved" + (sha ? " · " + String(sha).slice(0, 7) : "") + " ✓", true);
        if (!okId || !window.lcSetSourceOf) return;
        var s = parseSrc(okSnap); if (!s) return;
        if (okKnobs) Object.keys(okKnobs).forEach(function (n) { s.setAttribute(n, okKnobs[n]); });
        if (okText) {
          var c = s.querySelector("code");
          if (c) c.textContent = okVal + "\n"; else s.textContent = okVal;
        }
        window.lcSetSourceOf(okId, s.outerHTML);
      });
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
    /* Click the backdrop to close. The catch: a <dialog>'s own resize corner
       and its backdrop BOTH report the dialog as the click target, so
       dragging the corner made the editor vanish the moment you let go.
       Target alone cannot tell them apart — position can: the backdrop is
       everything OUTSIDE the dialog's box. */
    var _outside = function (e) {
      var r = dlg.getBoundingClientRect();
      return e.clientX < r.left || e.clientX > r.right ||
             e.clientY < r.top  || e.clientY > r.bottom;
    };
    var _pressedOut = false;
    dlg.addEventListener("pointerdown", function (e) {
      _pressedOut = (e.target === dlg) && _outside(e);
    });
    dlg.addEventListener("click", function (e) {
      /* both ends of the gesture on the backdrop — a resize starts on the
         corner (inside) and so never qualifies */
      if (e.target === dlg && _pressedOut && _outside(e)) closeDlg();
      _pressedOut = false;
    });

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
