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
    var saveWrap = null, saveBtn = null, resetBtn = null, mineTag = null;
    if (saveKnob) {
      saveWrap = document.createElement("div");
      saveWrap.className = "lc-mdpad-bar";
      if (benchPath) {
        mineTag = document.createElement("span");
        mineTag.className = "lc-mdpad-mine";
        mineTag.hidden = true;
        mineTag.textContent = "✓ yours — saved in your space";
        resetBtn = document.createElement("button");
        resetBtn.type = "button";
        resetBtn.className = "lc-mdpad-reset";
        resetBtn.textContent = "↺ Start over";
        resetBtn.title = "Bring back the lesson's starter — your saved copy stays until you 💾 again";
        saveWrap.appendChild(mineTag);
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
    } else if (saveBtn) {
      var origin = seed;   /* what the file holds right now — the anchor */
      var refresh = function () {
        var t = window.lcSourceTarget ? window.lcSourceTarget(wrap) : null;
        var why = !t || !t.pat ? "Connect your key to save"
                : t.readonly   ? "This source is read-only"
                : !t.repo || !t.path ? "No source file to save into" : "";
        saveBtn.disabled = !!why;
        saveBtn.title = why || "Commit this block back to the page source";
        return t;
      };
      refresh();
      saveBtn.addEventListener("click", function () {
        var t = refresh();
        if (saveBtn.disabled) return;
        if (ta.value === origin) { window.lcxToast && window.lcxToast("Nothing changed.", true); return; }
        saveBtn.disabled = true; saveBtn.textContent = "💾 Saving…";
        window.lcCommitInline(t.pat, t.repo, t.path, origin, ta.value, id || "mdpad", function (sha) {
          /* re-anchor on what the file now holds, or a second save cannot
             find its own text and fails with "couldn't locate" */
          origin = ta.value;
          saveBtn.textContent = "💾 Save";
          refresh();
          window.lcxToast && window.lcxToast("Saved" + (sha ? " · " + String(sha).slice(0, 7) : "") + " ✓", true);
        });
        setTimeout(function () { if (saveBtn.textContent !== "💾 Save") { saveBtn.textContent = "💾 Save"; refresh(); } }, 8000);
      });
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
