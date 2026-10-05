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
  piano="true"   consecutive blocks banded in two shades of the source pane, the
              caret's block in a third — the "piano"
  numbers="true" a line number per source line in a gutter (wrapped lines keep one)
  replay="1.5"  seconds per frame when 🎞 Replay plays the saved versions (default 1.5);
              the button itself comes with save="<path>", once a version exists
  decorations="true"
              the preview renders the page the way the site does: block
              decorations ({: .red} under a paragraph, {: .pitch} under a
              yaml fence…) apply, and component fences come alive — a
              learner's résumé can carry a pitch, cards, a chart. Same
              pipeline as the runner. Debounced, not per keystroke: a
              component rebuilds, a word does not.
  id="..."    optional — names the pad for X-ray
  layout="rows"  preview ABOVE the source instead of beside it — for a
              landscape document (a story in colour) that would be squeezed
              in half a pane. DEFAULT: side by side (left/right).

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
/* an APP SCREEN: a pad that is both saved to the bench and decorated is a
   page of the learner's own app, so its preview wears app chrome — a title
   bar mirroring the page's own # line — instead of a bare rendering */
.lc-mdpad-app { padding: 0; border-radius: 12px; border: 1px solid #c7cdd6;
  box-shadow: 0 6px 18px rgba(15, 23, 42, 0.10); background: #fff; display: flex; flex-direction: column; }
.lc-mdpad-apphead { display: flex; align-items: center; gap: 0.5em; padding: 0.5em 0.9em;
  background: #1e293b; color: #f8fafc; font-weight: 600; font-size: 0.9em;
  border-radius: 12px 12px 0 0; letter-spacing: 0.01em; }
.lc-mdpad-apphead .lc-mdpad-appdots { display: inline-flex; gap: 4px; margin-right: 0.2em; }
.lc-mdpad-apphead .lc-mdpad-appdots i { width: 8px; height: 8px; border-radius: 50%; background: #64748b; display: inline-block; }
.lc-mdpad-appbody { padding: 0.8em; overflow: auto; flex: 1; }
/* phones: preview first, then the source under it — same order as wide */
@media (max-width: 640px) { .lc-mdpad { flex-direction: column; } }
/* layout="rows": the same stacking on every screen, for a landscape document */
.lc-mdpad.lc-mdpad-rows { flex-direction: column; }
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
.lc-ver-panel li.starter { background: #fffbeb; }
.lc-ver-panel li.starter .lc-ver-when { color: #92400e; font-style: italic; }
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
/* FOCUS — the caret's block, pulsed in the preview (Michel, 2026-10-05: "help
   students see where to focus when they make a change", as the page editor does) */
.lc-mdpad-out .lc-mdpad-focus { animation: lc-mdpad-pulse 1.4s ease-out; border-radius: 4px; }
@keyframes lc-mdpad-pulse {
  0%   { background: #dbeafe; box-shadow: 0 0 0 4px #dbeafe; }
  100% { background: transparent; box-shadow: 0 0 0 4px transparent; }
}
@media (prefers-reduced-motion: reduce) {
  .lc-mdpad-out .lc-mdpad-focus { animation: none; box-shadow: 0 0 0 3px #bfdbfe; }
}
/* PIANO + NUMBERS — a backdrop behind the source mirrors it line for line:
   consecutive blocks banded in two shades of the dark pane, the caret's block
   in a third; a gutter with one number per source line (wrapped lines keep
   theirs). The textarea goes transparent over it. */
.lc-mdpad-src { flex: 1; min-width: 0; position: relative; display: flex; }
.lc-mdpad-src .lc-mdpad-in { flex: 1; min-width: 0; background: transparent; position: relative; z-index: 1; }
.lc-mdpad-src[data-numbers] .lc-mdpad-in { padding-left: 3.4em; }
.lc-mdpad-piano { position: absolute; inset: 0; overflow: hidden; pointer-events: none; z-index: 0;
  box-sizing: border-box; background: #1e1e2e; border: 1px solid transparent; border-radius: 6px;
  color: transparent; white-space: pre-wrap; overflow-wrap: break-word; word-break: normal; }
.lc-mdpad-piano .k1 { background: #26263a; }
.lc-mdpad-piano .now { background: #30304c; box-shadow: inset 3px 0 0 #89b4fa; }
.lc-mdpad-piano[data-plain] .k1 { background: transparent; }
.lc-mdpad-piano[data-plain] .now { background: transparent; box-shadow: none; }
.lc-mdpad-piano .ln { position: relative; }
.lc-mdpad-src[data-numbers] .lc-mdpad-piano .ln::before {
  content: attr(data-n); position: absolute; left: -2.9em; width: 2.2em; text-align: right;
  color: #6c7086; font-size: 0.85em; line-height: inherit; }
.lc-mdpad-src[data-numbers] .lc-mdpad-piano .ln.here::before { color: #cdd6f4; }
/* the gutter itself: a grayer column, so numbers never read as text (Michel, 2026-10-05) */
.lc-mdpad-src[data-numbers] .lc-mdpad-piano::before { content: ""; position: absolute; left: 0; top: 0; bottom: 0;
  width: 3em; background: #2a2a38; border-right: 1px solid #3c3c50; }
/* 🎞 REPLAY — the source pane becomes a diff pane: + green, − red, the
   usual cues; a slider is the cursor; play runs forward, the moonwalk back */
.lc-mdpad-replay, .lc-mdpad-hist { font: inherit; font-size: 0.85em; padding: 0.35em 0.7em; border-radius: 6px;
  border: 1px solid #bbb; background: #fff; color: #555; cursor: pointer; }
.lc-mdpad-replay:hover { border-color: #888; color: #222; }
.lc-mdpad-replay:disabled { opacity: 0.6; cursor: default; }
.lc-mdpad-diff { flex: 1; min-width: 0; margin: 0; padding: 0.8em; overflow: auto; box-sizing: border-box;
  border: 1px solid #d0d0d0; border-radius: 6px; background: #1e1e2e; color: #9399b2;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; line-height: 1.5; white-space: pre-wrap; }
.lc-mdpad-diff span { display: block; }
.lc-mdpad-diff .add { background: #1f3b2a; color: #a6e3a1; }
.lc-mdpad-diff .del { background: #3b1f26; color: #f38ba8; }
/* word level: inside an edited line, the words that actually differ */
.lc-mdpad-diff .add b { font-weight: inherit; background: #2f6b3f; color: #d9ffd9; border-radius: 3px; }
.lc-mdpad-diff .del b { font-weight: inherit; background: #7a2f3f; color: #ffd9e0; border-radius: 3px; }
/* line by line, during play: removed lines fold away, added lines unfold, one after the other */
.lc-mdpad-diff .fold, .lc-mdpad-diff .unfold { overflow: hidden; transition: max-height .35s ease, opacity .35s ease; transition-delay: var(--d, 0s); max-height: 14em; }
.lc-mdpad-diff .unfold { max-height: 0; opacity: 0; }
.lc-mdpad-diff .unfold.go { max-height: 14em; opacity: 1; }
.lc-mdpad-diff .fold.go { max-height: 0; opacity: 0; }
/* the preview cross-fades: a ghost of the old render fades over the new one */
.lc-mdpad-ghost { position: absolute; pointer-events: none; opacity: 1; transition: opacity .3s ease; z-index: 2; }
.lc-mdpad-ghost.go { opacity: 0; }
@media (prefers-reduced-motion: reduce) {
  .lc-mdpad-diff .fold, .lc-mdpad-diff .unfold, .lc-mdpad-ghost { transition: none; }
}
.lc-mdpad-replaybar { display: flex; gap: 0.6em; align-items: center; margin: -0.4em 0 0.6em; font-size: 0.85em; color: #555; }
.lc-mdpad-replaybar button { font: inherit; padding: 0.3em 0.7em; border-radius: 6px; border: 1px solid #bbb; background: #fff; color: #444; cursor: pointer; }
.lc-mdpad-replaybar button:hover { border-color: #888; color: #222; }
.lc-mdpad-replaybar input[type=range] { flex: 1; min-width: 80px; accent-color: #0066cc; }
.lc-mdpad-replaybar .lc-mdpad-frame { white-space: nowrap; font-variant-numeric: tabular-nums; }
</style>

<script>
(function () {
  if (window._lcMdpadReady) return;
  window._lcMdpadReady = true;

  /* ── BLOCKS: the source as the preview counts it. Split at blank lines;
     a fence runs to its closing fence whatever it holds; a run of IAL lines
     ({: … }) belongs to the block above, as the preview merges it into that
     element. One block = one top-level element in the preview, which is
     what the focus below relies on; a heading is found by its words. */
  function blocksOf(src) {
    var lines = src.split("\n"), blocks = [], cur = null, fence = null;
    for (var i = 0; i < lines.length; i++) {
      var ln = lines[i], t = ln.trim();
      if (fence) {
        cur.end = i;
        if (t.charAt(0) === fence.charAt(0) && /^(`{3,}|~{3,})$/.test(t) && t.length >= fence.length) fence = null;
        continue;
      }
      if (t === "") { cur = null; continue; }
      if (!cur && blocks.length && /^\{:.*\}$/.test(t)) { blocks[blocks.length - 1].end = i; continue; }
      if (!cur) { cur = { start: i, end: i, head: ln }; blocks.push(cur); } else cur.end = i;
      var m = t.match(/^(`{3,}|~{3,})/);
      if (m) fence = m[1];
    }
    return blocks;
  }
  function blockAt(blocks, line) {
    for (var i = 0; i < blocks.length; i++) if (line >= blocks[i].start && line <= blocks[i].end) return i;
    return -1;
  }
  function escHtml(s) { return s.replace(/[&<>]/g, function (c) { return c === "&" ? "&amp;" : c === "<" ? "&lt;" : "&gt;"; }); }

  function upgradeMdpad(el) {
    if (el.dataset.lcMdpadDone) return;
    el.dataset.lcMdpadDone = "1";
    var seed = (el.querySelector("code") || el).textContent.replace(/\n+$/, "");
    var rows = parseInt(el.getAttribute("rows") || "12", 10);
    var deco = el.getAttribute("decorations") === "true";
    var id = el.id || "";

    var wrap = document.createElement("div");
    wrap.className = "lc-mdpad";
    if (deco) wrap.setAttribute("data-lc-decorations", "1");
    if ((el.getAttribute("layout") || "") === "rows") wrap.classList.add("lc-mdpad-rows");
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
    var piano = el.getAttribute("piano") === "true", numbers = el.getAttribute("numbers") === "true";
    var src = null, keysEl = null;
    if (piano || numbers) {
      src = document.createElement("div");
      src.className = "lc-mdpad-src";
      if (numbers) src.setAttribute("data-numbers", "1");
      keysEl = document.createElement("div");
      keysEl.className = "lc-mdpad-piano";
      keysEl.setAttribute("aria-hidden", "true");
      if (!piano) keysEl.setAttribute("data-plain", "1");
      src.appendChild(keysEl);
      src.appendChild(ta);
    }
    ta.setAttribute("aria-label", "Markdown editor");
    ta.spellcheck = false;
    ta.rows = rows;
    ta.value = seed;

    var out = document.createElement("div");
    out.className = "lc-mdpad-out";
    var body = out, appTitle = null;   /* app chrome, decided once save= is known */

    /* save="true" — commit straight from the pad, no x-ray, no page editor.
       It reuses the SAME commit path the x-ray Keep uses (lcCommitInline), so
       there is one way a block gets written back, not two that drift. The
       button only exists when a save is actually possible: a key, a resolved
       source, and a source that is not read-only. */
    /* save="my/cv.md" — the OTHER save: the page is the author's (vault,
       no learner write), the work is the learner's. The fence seeds; the
       learner's copy persists at this path in their own bench and, when it
       exists, replaces the seed on load. Same page, two repos, one writer
       per file — the author can republish forever without touching it. */
    var saveKnob = el.getAttribute("save") || "";
    var benchPath = saveKnob && saveKnob !== "true" ? saveKnob : "";
    if (benchPath) wrap.setAttribute("data-lc-save", benchPath);   /* named in a proof's verdict */
    var saveWrap = null, saveBtn = null, resetBtn = null, mineTag = null, histBtn = null, replayBtn = null;
    var pace = parseFloat(el.getAttribute("replay")) || 1.5;   /* seconds per replay frame */
    /* AN APP SCREEN (Michel, 2026-10-02): saved to the bench AND decorated,
       the pad is a page of the learner's own app — so the preview wears app
       chrome, a title bar that mirrors the page's # line (the file's name
       until there is one). The outer .lc-mdpad-out stays what proofs and
       the suite read; only the rendering moves into the body under the bar. */
    if (deco && benchPath) {
      out.classList.add("lc-mdpad-app");
      var head = document.createElement("div");
      head.className = "lc-mdpad-apphead";
      head.innerHTML = "<span class='lc-mdpad-appdots'><i></i><i></i><i></i></span>";
      appTitle = document.createElement("span");
      appTitle.className = "lc-mdpad-apptitle";
      appTitle.textContent = benchPath;
      head.appendChild(appTitle);
      body = document.createElement("div");
      body.className = "lc-mdpad-appbody";
      out.appendChild(head);
      out.appendChild(body);
    }
    /* the stripe every saved block wears — see lcBenchFrame in widgets.md */
    var frame = null;
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
        replayBtn = document.createElement("button");
        replayBtn.type = "button";
        replayBtn.className = "lc-mdpad-replay";
        replayBtn.hidden = true;        /* nothing to replay until a first save */
        replayBtn.textContent = "🎞 Replay";
        replayBtn.title = "Watch your document grow, version by version — read-only, nothing is written";
        saveWrap.appendChild(mineTag);
        saveWrap.appendChild(histBtn);
        saveWrap.appendChild(replayBtn);
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
    wrap.appendChild(src || ta);
    el.parentNode.replaceChild(wrap, el);
    if (saveWrap) wrap.parentNode.insertBefore(saveWrap, wrap.nextSibling);
    /* the stripe goes round BOTH the pad and its keep bar, so the frame
       reads as one owned thing rather than a box with a bar loose under it */
    if (benchPath && window.lcBenchFrame) {
      frame = window.lcBenchFrame(wrap, { path: benchPath, id: id, mine: false });
      if (frame && saveWrap) frame.el.appendChild(saveWrap);
    }

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
          if (frame) frame.setMine(true);
          revealVersions();                      /* a saved file HAS a history */
          render(); publish(true);
        }).catch(function () {});
      }
      saveBtn.addEventListener("click", function () {
        refreshBench();
        if (saveBtn.disabled) return;
        if (ta.value === bOrigin) { window.lcxToast && window.lcxToast("Nothing changed.", true); return; }
        saveBtn.disabled = true; saveBtn.textContent = "💾 Saving…";
        /* FIRST save writes the author's starter first, so the learner's
           opening change has something to compare against — otherwise
           version one IS their text and 🕘 shows a single row that differs
           from nothing. Written on the first save, never on load: a reader
           who never edits leaves no commits at all. Never allowed to block
           the real save. */
        var first = !bSha;
        (first
          ? window.lcBench.write(benchPath, seed, window.lcStarterMsg, null, wrap)
              .then(function (sha) { bSha = sha || bSha; })
              .catch(function () {})
          : Promise.resolve()
        ).then(function () {
        return window.lcBench.write(benchPath, ta.value, "✍️ " + (id || benchPath), bSha, wrap)
          .then(function (sha) {
            bOrigin = ta.value; bSha = sha || bSha;
            wrap.setAttribute("data-lc-mine", "1");
            wrap.removeAttribute("data-lc-dirty");
            try { document.dispatchEvent(new CustomEvent("lc-saved", { detail: { id: id } })); } catch (e2) {}
            if (mineTag) mineTag.hidden = false;
            if (frame) frame.setMine(true);
            revealVersions();
            closeVersions();                     /* the list just grew — re-open it fresh */
            window.lcxToast && window.lcxToast("Saved to your space ✓", true);
          })
          .catch(function (e) {
            window.lcxToast && window.lcxToast("Save failed: " + (e.message || e), false);
          })
          .finally(function () { saveBtn.textContent = "💾 Save"; refreshBench(); });
        });
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
      function revealVersions() { if (vers) vers.reveal(); if (replayBtn) replayBtn.hidden = false; }

      /* ── 🎞 REPLAY (Michel, 2026-10-05): every saved version as a frame, the
         author's starter first (the first save writes it, above), read-only.
         The source pane becomes a diff pane with the usual cues (+ green,
         − red) against the frame before; the block that changed pulses in
         the preview; a slider is the cursor; ▶ plays forward, ◀ backward
         (the moonwalk), replay="1.5" seconds per frame. Nothing is written:
         the learner's text waits under the pane, untouched. */
      var rp = { frames: null, at: 0, timer: null, dir: 1, ui: null, diffEl: null, on: false };
      function rpLoad() {
        if (rp.frames) return Promise.resolve(rp.frames);
        return window.lcBench.history(benchPath, wrap, 100).then(function (list) {
          list = list.slice().reverse();              /* oldest first: frame zero is the starter */
          return Promise.all(list.map(function (c) {
            return window.lcBench.readAt(benchPath, c.sha, wrap).then(function (t) {
              return { sha: c.sha, when: c.when, message: c.message, text: t == null ? "" : String(t),
                       starter: String(c.message || "").indexOf(window.lcStarterMsg || "📄 starter") === 0 };
            });
          }));
        }).then(function (frames) { rp.frames = frames; return frames; });
      }
      /* WORD LEVEL: an edited line is a − / + pair; the words that differ are
         the middle once the common head and tail are peeled off, backed off to
         word boundaries so a mark never starts mid-word. */
      function wordMarks(a, b) {
        var i = 0, n = Math.min(a.length, b.length);
        while (i < n && a.charAt(i) === b.charAt(i)) i++;
        while (i > 0 && /\S/.test(a.charAt(i - 1)) && /\S/.test(a.charAt(i) || " ")) i--;
        var j = 0;
        while (j < n - i && a.charAt(a.length - 1 - j) === b.charAt(b.length - 1 - j)) j++;
        while (j > 0 && /\S/.test(a.charAt(a.length - j)) && /\S/.test(a.charAt(a.length - j - 1) || " ")) j--;
        if (i + j < 2) return null;            /* nothing in common: a different line, not an edit */
        function mark(t) {
          var mid = t.slice(i, t.length - j);
          return escHtml(t.slice(0, i)) + (mid ? "<b>" + escHtml(mid) + "</b>" : "") + escHtml(t.slice(t.length - j));
        }
        return [mark(a), mark(b)];
      }
      var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      var rpAnimT = null;
      function rpShow(n, animate) {
        var f = rp.frames && rp.frames[n]; if (!f) return;
        rp.at = n;
        animate = !!animate && !reduced;
        clearTimeout(rpAnimT);
        var prev = n > 0 ? rp.frames[n - 1].text : f.text;
        var rows = window.lcDiffLines ? window.lcDiffLines(prev, f.text)
                 : f.text.split("\n").map(function (l) { return ["same", l]; });
        /* pair each run of − with the run of + right after it, line by line */
        var html = rows.map(function (r) { return escHtml(r[1]); });
        for (var a = 0; a < rows.length; a++) {
          if (rows[a][0] !== "del") continue;
          var d0 = a; while (a < rows.length && rows[a][0] === "del") a++;
          var p0 = a; while (a < rows.length && rows[a][0] === "add") a++;
          for (var q = 0; q < Math.min(p0 - d0, a - p0); q++) {
            var m = wordMarks(rows[d0 + q][1], rows[p0 + q][1]);
            if (m) { html[d0 + q] = m[0]; html[p0 + q] = m[1]; }
          }
          a--;
        }
        var changedRows = [];
        rp.diffEl.innerHTML = rows.map(function (r, i) {
          var cls = r[0];
          if (animate && r[0] !== "same") { cls += r[0] === "add" ? " unfold" : " fold"; changedRows.push(i); }
          return "<span class='" + cls + "'>" + (r[0] === "add" ? "+ " : r[0] === "del" ? "− " : "  ") + html[i] + "</span>";
        }).join("");
        /* the first changed line, as the NEW text counts lines */
        var changed = -1, firstRow = -1;
        for (var i = 0, ln = 0; i < rows.length; i++) {
          if (rows[i][0] !== "same") { changed = ln; firstRow = i; break; }
          ln++;
        }
        /* the preview: a ghost of the old render fades over the new one */
        var total = 0;
        if (animate && out.parentNode) {
          var ghost = out.cloneNode(true);
          ghost.classList.add("lc-mdpad-ghost");
          ghost.style.left = out.offsetLeft + "px"; ghost.style.top = out.offsetTop + "px";
          ghost.style.width = out.offsetWidth + "px"; ghost.style.height = out.offsetHeight + "px";
          wrap.style.position = "relative";
          wrap.appendChild(ghost);
          requestAnimationFrame(function () { ghost.classList.add("go"); });
          setTimeout(function () { if (ghost.parentNode) ghost.parentNode.removeChild(ghost); }, 400);
        }
        render(f.text);
        var fb = blocksOf(f.text), idx = changed < 0 ? -1 : blockAt(fb, changed);
        if (changed >= 0 && idx < 0) { for (var k = 0; k < fb.length; k++) if (fb[k].start > changed) { idx = k; break; } }
        if (changed >= 0 && idx < 0) idx = fb.length - 1;
        if (animate && changedRows.length) {
          /* one line after the other, the whole run inside half the frame */
          var step = Math.max(15, Math.min(80, (pace * 1000 * 0.5) / changedRows.length));
          changedRows.forEach(function (ri, k) { rp.diffEl.children[ri].style.setProperty("--d", (k * step / 1000) + "s"); });
          total = changedRows.length * step + 350;
          wrap.setAttribute("data-lc-animating", "1");
          requestAnimationFrame(function () {
            changedRows.forEach(function (ri) { var e = rp.diffEl.children[ri]; if (e) e.classList.add("go"); });
          });
          rpAnimT = setTimeout(function () {
            wrap.removeAttribute("data-lc-animating");
            focusPreview(idx, fb);                  /* the pulse lands as the last line settles */
          }, total);
        } else {
          focusPreview(idx, fb);
        }
        var sp = firstRow >= 0 ? rp.diffEl.children[firstRow] : null;
        rp.diffEl.scrollTop = sp ? Math.max(0, sp.offsetTop - rp.diffEl.offsetTop - 40) : 0;
        rp.ui.slider.value = String(n);
        rp.ui.label.textContent = (n + 1) + " / " + rp.frames.length + " · " +
          (f.starter ? "the lesson's starter" : (f.when ? new Date(f.when).toLocaleString() : "saved"));
        wrap.setAttribute("data-lc-frame", String(n));
      }
      function rpPause() {
        if (rp.timer) clearInterval(rp.timer);
        rp.timer = null;
        if (rp.ui) { rp.ui.play.textContent = "▶ Play"; rp.ui.back.textContent = "◀ Moonwalk"; }
        wrap.removeAttribute("data-lc-playing");
      }
      function rpStep() {
        var n = rp.at + rp.dir;
        if (n < 0 || n >= rp.frames.length) { rpPause(); return; }
        rpShow(n, true);
        /* landed on an end: stop there, now, not one silent tick later */
        if (n === 0 || n === rp.frames.length - 1) rpPause();
      }
      function rpPlay(dir) {
        rpPause();
        rp.dir = dir;
        /* pressed at an end: start again from the other end */
        if (dir > 0 && rp.at >= rp.frames.length - 1) rpShow(0);
        if (dir < 0 && rp.at <= 0) rpShow(rp.frames.length - 1);
        rp.timer = setInterval(rpStep, pace * 1000);
        if (dir > 0) rp.ui.play.textContent = "⏸ Pause"; else rp.ui.back.textContent = "⏸ Pause";
        wrap.setAttribute("data-lc-playing", dir > 0 ? "forward" : "backward");
      }
      function rpStart() {
        if (rp.on || !window.lcBench) return Promise.resolve();
        replayBtn.disabled = true; replayBtn.textContent = "⏳ reading your versions…";
        return rpLoad().then(function (frames) {
          replayBtn.disabled = false;
          if (!frames.length) {
            replayBtn.textContent = "🎞 Replay";
            if (window.lcxToast) window.lcxToast("No versions yet — 💾 writes the first one.", true);
            return;
          }
          rp.on = true;
          replayBtn.textContent = "■ Stop";
          wrap.setAttribute("data-lc-replay", "1");
          wrap.setAttribute("data-lc-frames", String(frames.length));
          closeVersions();
          [saveBtn, resetBtn, vers && vers.button].forEach(function (b) { if (b) b.disabled = true; });
          var pane = src || ta;
          rp.diffEl = document.createElement("pre");
          rp.diffEl.className = "lc-mdpad-diff";
          rp.diffEl.setAttribute("aria-label", "This version, with what changed since the one before");
          /* THE PANE KEEPS THE EDITOR'S HEIGHT (Michel, 2026-10-05): a frame's
             length must not move the bar under the pad — the pane scrolls
             inside, to the first change, as the editor would. */
          rp.diffEl.style.height = pane.offsetHeight + "px";
          rp.diffEl.style.flex = "1 1 0";
          wrap.insertBefore(rp.diffEl, pane);
          pane.style.display = "none";
          var box = document.createElement("div");
          box.className = "lc-mdpad-replaybar";
          function mk(text, cls) { var b = document.createElement("button"); b.type = "button"; b.className = cls; b.textContent = text; return b; }
          rp.ui = { box: box, back: mk("◀ Moonwalk", "lc-mdpad-back"), play: mk("▶ Play", "lc-mdpad-play"),
                    slider: document.createElement("input"), label: document.createElement("span") };
          rp.ui.slider.type = "range"; rp.ui.slider.min = "0"; rp.ui.slider.max = String(frames.length - 1);
          rp.ui.slider.step = "1"; rp.ui.slider.setAttribute("aria-label", "Version");
          rp.ui.label.className = "lc-mdpad-frame";
          box.appendChild(rp.ui.back); box.appendChild(rp.ui.play); box.appendChild(rp.ui.slider); box.appendChild(rp.ui.label);
          saveWrap.parentNode.insertBefore(box, saveWrap);
          rp.ui.slider.addEventListener("input", function () { rpPause(); rpShow(+rp.ui.slider.value); });
          rp.ui.play.addEventListener("click", function () { rp.timer && rp.dir > 0 ? rpPause() : rpPlay(1); });
          rp.ui.back.addEventListener("click", function () { rp.timer && rp.dir < 0 ? rpPause() : rpPlay(-1); });
          rpShow(0);
        });
      }
      function rpStop() {
        if (!rp.on) return;
        rpPause();
        clearTimeout(rpAnimT);
        wrap.removeAttribute("data-lc-animating");
        wrap.querySelectorAll(".lc-mdpad-ghost").forEach(function (g) { g.parentNode.removeChild(g); });
        rp.on = false;
        replayBtn.textContent = "🎞 Replay";
        ["data-lc-replay", "data-lc-frame", "data-lc-frames"].forEach(function (a) { wrap.removeAttribute(a); });
        if (rp.diffEl && rp.diffEl.parentNode) rp.diffEl.parentNode.removeChild(rp.diffEl);
        if (rp.ui && rp.ui.box.parentNode) rp.ui.box.parentNode.removeChild(rp.ui.box);
        rp.diffEl = null; rp.ui = null;
        (src || ta).style.display = "";
        [resetBtn, vers && vers.button].forEach(function (b) { if (b) b.disabled = false; });
        refreshBench();                 /* 💾 decides its own state again */
        rp.frames = null;               /* a save in between adds a frame: read again next time */
        lastFocus = -2; render(); focusNow();
      }
      if (replayBtn) replayBtn.addEventListener("click", function () { if (rp.on) rpStop(); else rpStart(); });
      /* a proof drives it as a person would: pad.replay(), pad.frame = n, pad.stop() */
      wrap._lcReplay = { start: rpStart, stop: rpStop, play: rpPlay, pause: rpPause,
                         go: function (n) { if (rp.on) { rpPause(); rpShow(n); } } };
    }

    function render(text) {
      var v = typeof text === "string" ? text : ta.value;   /* a replay frame, else the editor */
      if (!window.marked) {
        body.innerHTML = "<pre>" + v.replace(/[&<]/g, function (c) { return c === "&" ? "&amp;" : "&lt;"; }) + "</pre>";
        return;
      }
      var inline = window.lcInlineIAL || function (h) { return h; };
      if (!deco) { body.innerHTML = inline(window.marked.parse(v)); return; }
      /* decorations: the runner's pipeline on the preview — IAL on its own
         paragraph, block IAL applied, then the same scan that upgrades a
         page's fences into components, and the cells inside them */
      var norm = v.replace(/([^\n])\n(\{:)/g, "$1\n\n$2");
      body.innerHTML = inline(window.marked.parse(norm));
      if (window.lcApplyIAL) window.lcApplyIAL(body);
      if (window.lcScanElement) window.lcScanElement(body);
      if (window.lcCellsRescan) window.lcCellsRescan();
      if (appTitle) {
        var h1 = body.querySelector("h1");
        appTitle.textContent = (h1 && h1.textContent.trim()) || benchPath;
      }
    }
    /* ── FOCUS: the block under the caret, shown on both sides ── */
    var blocks = blocksOf(ta.value), lastFocus = -2;
    function caretLine() { return ta.value.slice(0, ta.selectionStart || 0).split("\n").length - 1; }
    function caretBlock() { return blockAt(blocks, caretLine()); }
    function focusPreview(idx, bl) {
      bl = bl || blocks;
      body.querySelectorAll(".lc-mdpad-focus").forEach(function (e) { e.classList.remove("lc-mdpad-focus"); });
      if (idx < 0 || !bl[idx]) return;
      var target = null, hm = bl[idx].head.match(/^\s*#{1,6}\s+(.*)$/);
      if (hm) {
        var want = hm[1].replace(/[*_`#]/g, "").trim().toLowerCase();
        var hs = body.querySelectorAll("h1,h2,h3,h4,h5,h6");
        for (var i = 0; i < hs.length && !target; i++)
          if (hs[i].textContent.trim().toLowerCase() === want) target = hs[i];
      }
      if (!target) target = body.children[idx] || null;
      if (!target) return;
      void target.offsetWidth;
      target.classList.add("lc-mdpad-focus");
      /* bring it into the preview's own view — never scroll the page */
      var scroller = body === out ? out : body;
      var box = scroller.getBoundingClientRect(), r = target.getBoundingClientRect();
      if (r.top < box.top) scroller.scrollTop -= (box.top - r.top) + 8;
      else if (r.bottom > box.bottom) scroller.scrollTop += (r.bottom - box.bottom) + 8;
    }
    function paintPiano() {
      if (!keysEl) return;
      var cs = getComputedStyle(ta);
      ["fontFamily", "fontSize", "lineHeight", "letterSpacing", "tabSize", "paddingTop", "paddingLeft",
       "paddingBottom", "borderTopWidth", "borderLeftWidth", "borderRightWidth", "borderBottomWidth"]
        .forEach(function (k) { keysEl.style[k] = cs[k]; });
      /* the textarea's scrollbar narrows ITS text; mirror that or long lines wrap apart */
      var bar = ta.offsetWidth - ta.clientWidth - parseFloat(cs.borderLeftWidth) - parseFloat(cs.borderRightWidth);
      keysEl.style.paddingRight = (parseFloat(cs.paddingRight) + Math.max(0, bar)) + "px";
      var lines = ta.value.split("\n"), now = caretBlock(), here = caretLine(), html = "", li = 0;
      function line(n) { return "<div class='ln" + (n === here ? " here" : "") + "' data-n='" + (n + 1) + "'>" + (escHtml(lines[n]) || "\u00a0") + "</div>"; }
      blocks.forEach(function (b, i) {
        for (; li < b.start; li++) html += line(li);
        html += "<div class='" + (i % 2 ? "k1" : "k0") + (i === now ? " now" : "") + "'>";
        for (; li <= b.end; li++) html += line(li);
        html += "</div>";
      });
      for (; li < lines.length; li++) html += line(li);
      keysEl.innerHTML = html;
      keysEl.scrollTop = ta.scrollTop;
    }
    function focusNow() {
      var idx = caretBlock();
      if (idx !== lastFocus) {
        lastFocus = idx;
        focusPreview(idx);
        if (idx >= 0) wrap.setAttribute("data-lc-focus", String(idx)); else wrap.removeAttribute("data-lc-focus");
      }
      paintPiano();
    }
    var _focT = null;
    function focusSoon() { clearTimeout(_focT); _focT = setTimeout(focusNow, 150); }
    ta.addEventListener("click", focusSoon);
    ta.addEventListener("keyup", focusSoon);
    ta.addEventListener("select", focusNow);
    ta.addEventListener("input", function () { blocks = blocksOf(ta.value); paintPiano(); });
    if (keysEl) {
      ta.addEventListener("scroll", function () { keysEl.scrollTop = ta.scrollTop; });
      if (window.ResizeObserver) new ResizeObserver(paintPiano).observe(ta);
    }
    /* a proof moves the caret the way a person would: pad.caret = n */
    wrap._lcCaret = function (pos) { ta.focus(); ta.setSelectionRange(pos, pos); blocks = blocksOf(ta.value); focusNow(); };

    var _renT = null;
    ta.addEventListener("input", deco
      ? function () { clearTimeout(_renT); _renT = setTimeout(render, 350); }
      : render);
    ta.addEventListener("input", function () {
      /* edited since the last save: a proof reading this pad says so */
      if (benchPath) {
        if (ta.value !== bOrigin) wrap.setAttribute("data-lc-dirty", "1");
        else wrap.removeAttribute("data-lc-dirty");
      }
      clearTimeout(_pubT);
      _pubT = setTimeout(function () { publish(true); }, 400);
    });
    publish(false);  /* the seed is data too — no recompute storm on load */
    render();  /* show the seed immediately (escaped) … */
    if (window.lcLoadMarked) window.lcLoadMarked(render);  /* … then with marked */
    if (keysEl) paintPiano();
  }

  /* code_chrome.md provides the scan registry; one registration covers the
     initial scan and every re-scan. */
  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader(".highlighter-rouge.mdpad, pre.mdpad", upgradeMdpad);
  }
})();
</script>
