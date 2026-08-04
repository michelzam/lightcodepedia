{%- comment -%}
Mdpad — a live Markdown scratchpad: read the rendered result on the LEFT,
type the source on the RIGHT, updating on every keystroke. Seed it with a fenced
markdown block; the IAL upgrades it in place (P8), and rendering reuses
the shared marked loader from core (P9). No JS in the content (P5).

Usage:
  ````markdown
  ## Hello!
  **Bold** and *italic*, a [link](/), and a list:
  - one
  - two
  ````
  {: .mdpad rows="14" }

IAL knobs:
  rows="14"   editor height in text rows (default 12)
  save="true" show a 💾 Save button that commits straight to the source file
  save="cv.md"
              the two-repo contract: the fence is the AUTHOR's seed, the
              learner's saved copy lives in their OWN bench — relative =
              beside the lesson (the page's folder, FULL course path, so two
              courses in one bench never collide), "/my/cv.md" = bench root
              for files that outlive one lesson
              (the repo they connected at join). On load the bench copy —
              when it exists — replaces the seed; 💾 commits back to it;
              ↺ restores the seed (their file survives until they 💾 over
              it). The author can republish the page forever: seed and
              saved copy are different files in different repos, so
              nothing ever collides.
  id="..."    optional — names the pad for X-ray

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-mdpad { display: flex; gap: 0.75em; margin: 1em 0; min-height: 220px; }
.lc-mdpad-in {
  flex: 1; min-width: 0; resize: vertical;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 0.85em; line-height: 1.5; padding: 0.8em;
  border: 1px solid #d0d0d0; border-radius: 6px;
  background: #1e1e2e; color: #cdd6f4;
}
.lc-mdpad-out {
  flex: 1; min-width: 0; padding: 0.8em; overflow: auto;
  border: 1px solid #d0d0d0; border-radius: 6px;
  background: #fafafa; font-size: 0.95em;
}
/* phones: preview first, then the source under it — same order as wide */
@media (max-width: 640px) { .lc-mdpad { flex-direction: column; } }
.lc-mdpad-bar { margin: -0.4em 0 1em; display: flex; justify-content: flex-end; gap: 0.5em; align-items: center; }
.lc-mdpad-mine { margin-right: auto; font-size: 0.78em; color: #2e7d32; }
.lc-mdpad-reset { font: inherit; font-size: 0.85em; padding: 0.35em 0.7em; border-radius: 6px;
  border: 1px solid #bbb; background: #fff; color: #555; cursor: pointer; }
.lc-mdpad-reset:hover { border-color: #888; color: #222; }
/* 🕘 versions — styling for the SHARED panel (lcVersions) in a pad's bar */
.lc-mdpad-bar .lc-ver-btn { font: inherit; font-size: 0.85em; padding: 0.35em 0.7em;
  border-radius: 6px; border: 1px solid #bbb; background: #fff; color: #555; cursor: pointer; }
.lc-mdpad-bar .lc-ver-btn:hover { border-color: #888; color: #222; }
.lc-ver-panel { border: 1px solid #d0d0d0; border-radius: 8px; margin: -0.6em 0 1em;
  background: #fafafa; overflow: hidden; font-size: 0.88em; }
.lc-ver-panel ol { list-style: none; margin: 0; padding: 0; max-height: 220px; overflow: auto; }
.lc-ver-panel li { display: flex; align-items: center; gap: 0.6em; padding: 0.45em 0.9em;
  border-bottom: 1px solid #eee; }
.lc-ver-panel li:last-child { border-bottom: none; }
.lc-ver-panel li.now { background: #eef6ff; }
.lc-ver-when { flex: 1; color: #444; }
.lc-ver-sha { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; color: #94a3b8; font-size: 0.85em; }
.lc-ver-panel button { font: inherit; font-size: 0.85em; padding: 0.2em 0.6em; border-radius: 5px;
  border: 1px solid #cbd5e1; background: #fff; color: #334155; cursor: pointer; }
.lc-ver-panel button:hover { border-color: #0066cc; color: #0066cc; }
.lc-ver-diff { margin: 0; padding: 0.7em 0.9em; background: #fff; border-top: 1px solid #eee;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.82em;
  line-height: 1.5; white-space: pre-wrap; overflow: auto; max-height: 260px; }
.lc-ver-diff .add { background: #dcfce7; color: #166534; display: block; }
.lc-ver-diff .del { background: #fee2e2; color: #991b1b; display: block; }
.lc-ver-diff .same { color: #64748b; display: block; }
.lc-mdpad-save { font: inherit; font-size: 0.85em; padding: 0.35em 1em; border-radius: 6px;
  border: 1px solid #0066cc; background: #0066cc; color: #fff; cursor: pointer; }
.lc-mdpad-save:hover:not(:disabled) { background: #0052a3; }
.lc-mdpad-save:disabled { opacity: 0.45; cursor: default; }
</style>

<script>
(function () {
  if (window._lcMdpadReady) return;
  window._lcMdpadReady = true;

  function upgradeMdpad(el) {
    if (el.dataset.lcMdpadDone) return;
    el.dataset.lcMdpadDone = "1";
    var seed = (el.querySelector("code") || el).textContent.replace(/\n+$/, "");
    var rows = parseInt(el.getAttribute("rows") || "12", 10);
    var id = el.id || "";

    var wrap = document.createElement("div");
    wrap.className = "lc-mdpad";
    if (id) wrap.setAttribute("data-lc-id", id);
    /* a named pad is page data: it publishes {source} as a cell scope, so
       expressions can read what the learner typed — {=cv1.source} in prose,
       in a visible= gate, or handed to an agent through bound="{=…}".
       Debounced: cells recompute in MicroPython, not per keystroke. */
    var _pubT = null;
    function publish(fire) {
      if (!id) return;
      wrap.setAttribute("data-lc-value", JSON.stringify({ source: ta.value }));
      if (fire) {
        try { document.dispatchEvent(new CustomEvent("lc-model-changed")); } catch (e) {}
      }
    }

    var ta = document.createElement("textarea");
    ta.className = "lc-mdpad-in";
    ta.spellcheck = false;
    ta.rows = rows;
    ta.value = seed;

    var out = document.createElement("div");
    out.className = "lc-mdpad-out";

    /* save="true" — commit straight from the pad, no x-ray, no page editor.
       It reuses the SAME commit path the x-ray Keep uses (lcCommitInline), so
       there is one way a block gets written back, not two that drift. The
       button only exists when a save is actually possible: a key, a resolved
       source, and a source that is not read-only. */
    /* save="my/cv.md" — the OTHER save: the page is the author's (vault,
       no student write), the work is the learner's. The fence seeds; the
       learner's copy persists at this path in their own bench and, when it
       exists, replaces the seed on load. Same page, two repos, one writer
       per file — the author can republish forever without touching it. */
    var saveKnob = el.getAttribute("save") || "";
    var benchPath = saveKnob && saveKnob !== "true" ? saveKnob : "";
    var saveWrap = null, saveBtn = null, resetBtn = null, mineTag = null, histBtn = null;
    if (saveKnob) {
      saveWrap = document.createElement("div");
      saveWrap.className = "lc-mdpad-bar";
      if (benchPath) {
        mineTag = document.createElement("span");
        mineTag.className = "lc-mdpad-mine";
        mineTag.hidden = true;
        mineTag.textContent = "✓ yours — saved in your space";
        histBtn = document.createElement("button");
        histBtn.type = "button";
        histBtn.className = "lc-mdpad-hist";
        histBtn.hidden = true;          /* nothing to show until a first save */
        histBtn.textContent = "🕘 Versions";
        histBtn.title = "Every version you saved — read it, compare it, bring it back";
        resetBtn = document.createElement("button");
        resetBtn.type = "button";
        resetBtn.className = "lc-mdpad-reset";
        resetBtn.textContent = "↺ Start over";
        resetBtn.title = "Bring back the lesson's starter — your saved copy stays until you 💾 again";
        saveWrap.appendChild(mineTag);
        saveWrap.appendChild(histBtn);
        saveWrap.appendChild(resetBtn);
      }
      saveBtn = document.createElement("button");
      saveBtn.type = "button";
      saveBtn.className = "lc-mdpad-save";
      saveBtn.textContent = "💾 Save";
      saveWrap.appendChild(saveBtn);
    }

    /* Preview LEFT, source RIGHT — and appended in that order, so the DOM
       order matches what the eye sees. Reversing this with CSS alone would
       leave a keyboard and a screen reader walking it the other way round. */
    wrap.appendChild(out);
    wrap.appendChild(ta);
    el.parentNode.replaceChild(wrap, el);
    if (saveWrap) wrap.parentNode.insertBefore(saveWrap, wrap.nextSibling);

    if (saveBtn && benchPath) {
      var bOrigin = seed, bSha = null;
      var refreshBench = function () {
        var t = window.lcBench ? window.lcBench.target(wrap) : {};
        var why = !window.lcBench ? "Saving needs a newer engine"
                : !t.pat || !t.repo ? "Join the course (connect your key) to keep your work" : "";
        saveBtn.disabled = !!why;
        saveBtn.title = why || "Keep this in your own space (" +
          (window.lcBench ? window.lcBench.resolve(benchPath, wrap) : benchPath) + ")";
      };
      refreshBench();
      if (window.lcBench) {
        window.lcBench.read(benchPath, wrap).then(function (f) {
          if (!f) return;
          bOrigin = f.text; bSha = f.sha;
          ta.value = f.text;
          wrap.setAttribute("data-lc-mine", "1");
          if (mineTag) mineTag.hidden = false;
          revealVersions();                      /* a saved file HAS a history */
          render(); publish(true);
        }).catch(function () {});
      }
      saveBtn.addEventListener("click", function () {
        refreshBench();
        if (saveBtn.disabled) return;
        if (ta.value === bOrigin) { window.lcxToast && window.lcxToast("Nothing changed.", true); return; }
        saveBtn.disabled = true; saveBtn.textContent = "💾 Saving…";
        window.lcBench.write(benchPath, ta.value, "✍️ " + (id || benchPath), bSha, wrap)
          .then(function (sha) {
            bOrigin = ta.value; bSha = sha || bSha;
            wrap.setAttribute("data-lc-mine", "1");
            if (mineTag) mineTag.hidden = false;
            revealVersions();
            closeVersions();                     /* the list just grew — re-open it fresh */
            window.lcxToast && window.lcxToast("Saved to your space ✓", true);
          })
          .catch(function (e) {
            window.lcxToast && window.lcxToast("Save failed: " + (e.message || e), false);
          })
          .finally(function () { saveBtn.textContent = "💾 Save"; refreshBench(); });
      });
      resetBtn.addEventListener("click", function () {
        ta.value = seed;
        render(); publish(true);
        window.lcxToast && window.lcxToast("Starter restored — 💾 to make it yours", true);
      });

      /* 🕘 versions — the SHARED panel (lcVersions), the same one the grid
         uses. One implementation, two call sites; removing this call takes
         the feature out of the pad and nothing else. */
      var vers = window.lcVersions ? window.lcVersions.attach({
        path: benchPath, el: wrap, anchor: saveWrap,
        current: function () { return ta.value; },
        apply: function (t) { ta.value = t; render(); publish(true); }
      }) : null;
      if (vers) histBtn.parentNode.replaceChild(vers.button, histBtn);
      function closeVersions() { if (vers) vers.close(); }
      function revealVersions() { if (vers) vers.reveal(); }
    }

    function render() {
      out.innerHTML = window.marked
        ? (window.lcInlineIAL || function (h) { return h; })(window.marked.parse(ta.value))
        : "<pre>" + ta.value.replace(/[&<]/g, function (c) { return c === "&" ? "&amp;" : "&lt;"; }) + "</pre>";
    }
    ta.addEventListener("input", render);
    ta.addEventListener("input", function () {
      clearTimeout(_pubT);
      _pubT = setTimeout(function () { publish(true); }, 400);
    });
    publish(false);  /* the seed is data too — no recompute storm on load */
    render();  /* show the seed immediately (escaped) … */
    if (window.lcLoadMarked) window.lcLoadMarked(render);  /* … then with marked */
  }

  /* code_chrome.md provides the scan registry; one registration covers the
     initial scan and every re-scan. */
  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader(".highlighter-rouge.mdpad, pre.mdpad", upgradeMdpad);
  }
})();
</script>
