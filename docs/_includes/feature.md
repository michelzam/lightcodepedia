{%- comment -%}
Feature (Gherkin BDD) widget + Python step runner + suite dashboard.

Two blocks, one visual card. The .steps block is removed from the DOM;
its Python chunks are distributed to the feature card's expandable step rows.

BASIC CARD
  ```gherkin
  Feature: My feature
    Scenario: A scenario
      Given some precondition
      When an action happens
      Then the result is correct
  ```
  {: .feature status="passing" tags="smoke" }

INLINE STEPS (:::python::: blocks inside the gherkin fence)
  ```gherkin
  Feature: My feature
    Scenario: A scenario
      Given some precondition
      :::python
      self.x: int = 42
      :::
      When an action happens
      :::python
      self.y: int = self.x * 2
      :::
      Then the result is correct
      :::python
      assert self.y == 84
      :::
  ```
  {: .feature status="pending" tags="example" }

  self is shared across all steps. self.page, Dataset, Datagrid, Chart, Feature
  are all available (injected from the steps runtime).

LEGACY: WITH RUNNABLE STEPS (separate .steps block, still supported)
  ```python
  # Given some precondition
  x = 42

  # When an action happens
  y = x * 2

  # Then the result is correct
  assert y == 84
  ```
  {: .steps }

SUITE DASHBOARD  — auto-injected before the first feature card when
  there are 2+ runnable features on the page. Shows each feature's
  name, tags, and live status; has a ▶ Run All button.

Knobs for .feature:
  status="…"   passing | failing | pending
  tags="…"     comma-separated chips
  visible="true"  SHOW the card. Default is HIDDEN: a .feature is a spec/test,
                  not learner-facing content, so it stays out of sight unless
                  the author opts in (a ".visible" class works too). The editor
                  preview always shows features so they can be authored.

Auto-included by docs/_layouts/default.html.
Registers with window.lcScanElement so the editor preview also renders cards.
{%- endcomment -%}

<style>
/* ── card shell ────────────────────────────────────────────────── */
.lc-feature { border: 1px solid #e5e7eb; border-left: 4px solid #9ca3af; border-radius: 0 8px 8px 0; margin: 1.2em 0; background: #fff; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
.lc-feature-passing { border-left-color: #22c55e; }
.lc-feature-failing  { border-left-color: #ef4444; }
.lc-feature-pending  { border-left-color: #f59e0b; }
/* hidden by default — a .feature is a spec/test, shown only with visible="true" */
.lc-feature-hidden { display: none; }

/* ── header ──────────────────────────────────────────────────── */
.lc-feature-header { display: flex; align-items: center; gap: 0.6em; flex-wrap: wrap; padding: 0.55em 1em 0.5em; background: #f9fafb; border-bottom: 1px solid #e5e7eb; font-size: 0.88em; }
.lc-feature-name { font-weight: 600; color: #111827; flex: 1; min-width: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

.lc-feature-badge { display: inline-flex; align-items: center; gap: 0.3em; padding: 0.15em 0.6em; border-radius: 99px; font-size: 0.8em; font-weight: 500; line-height: 1.6; }
.lc-feature-badge::before { content: "●"; font-size: 0.75em; }
.lc-feature-badge-passing { background: #dcfce7; color: #15803d; }
.lc-feature-badge-failing  { background: #fee2e2; color: #b91c1c; }
.lc-feature-badge-pending  { background: #fef3c7; color: #92400e; }

.lc-feature-tags { display: flex; gap: 0.35em; flex-wrap: wrap; }
.lc-feature-tag { background: #e0f2fe; color: #075985; padding: 0.1em 0.55em; border-radius: 99px; font-size: 0.78em; font-weight: 500; }

.lc-feature-run { background: #0066cc; color: #fff; border: none; border-radius: 4px; padding: 0.25em 0.75em; font-size: 0.8em; font-weight: 500; cursor: pointer; flex-shrink: 0; }
.lc-feature-run:hover:not(:disabled) { background: #0052a3; }
.lc-feature-run:disabled { background: #9ca3af; cursor: progress; }

/* ── scenario / narrative ─────────────────────────────────────────────── */
.lc-feature-scenario { padding: 0.5em 1em 0.2em; font-size: 0.82em; font-weight: 600; color: #6b7280; letter-spacing: 0.03em; text-transform: uppercase; }
.lc-feature-narrative { padding: 0.1em 1em 0.1em 2.5em; font-size: 0.88em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; color: #9ca3af; }
.lc-feature-story { padding: 0.1em 1em 0.1em 2.5em; font-size: 0.88em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; display: flex; gap: 0.4em; align-items: baseline; flex-wrap: wrap; }
.lc-feature-story-keyword { color: #7c3aed; font-weight: 600; flex-shrink: 0; }
.lc-feature-story-text { color: #374151; }

/* ── step rows ──────────────────────────────────────────────────────────── */
.lc-feature-steps { padding: 0.35em 0; }
.lc-feature-step { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
.lc-feature-step.lc-step-and .lc-feature-step-keyword { padding-left: 1em; }
.lc-feature-step-row { display: flex; align-items: baseline; gap: 0.55em; padding: 0.28em 1em; font-size: 0.88em; line-height: 1.5; }
.lc-feature-step.has-impl > .lc-feature-step-row { cursor: pointer; }
.lc-feature-step.has-impl > .lc-feature-step-row:hover { background: #f3f4f6; }
.lc-feature-step-icon { flex-shrink: 0; width: 1.1em; text-align: center; color: #9ca3af; }
.lc-feature-step-icon.pass { color: #16a34a; }
.lc-feature-step-icon.fail { color: #dc2626; }
.lc-feature-step-icon.skip { color: #d1d5db; }
.lc-feature-step-keyword { color: #7c3aed; font-weight: 600; min-width: 3.5em; }
.lc-feature-step-text { color: #111827; }
/* a painted word wears the event flow's own background (.lc-ef-*), so the
   palette lives in one place — see event_flow.md */
.lc-gwt { padding: 0.05em 0.35em; border-radius: 3px; color: #1f2937; }
.lc-feature-step-text code { background: #f3f4f6; border-radius: 3px; padding: 0.05em 0.3em; font-size: 0.92em; }
.lc-feature-step-time { margin-left: auto; font-size: 0.75em; color: #9ca3af; }

/* ── expandable Python impl ────────────────────────────────────────────────── */
.lc-feature-step-impl { display: none; border-top: 1px solid #f3f4f6; border-bottom: 1px solid #f3f4f6; padding-left: 2.5em; }
.lc-feature-step-impl.open { display: block; }
.lc-feature-step-impl pre { margin: 0 !important; border-radius: 0 !important; border: none !important; box-shadow: none !important; max-height: 220px; overflow-y: auto; }
.lc-feature-step-impl pre code { font-size: 0.82em !important; line-height: 1.55 !important; }

/* ── error ──────────────────────────────────────────────────────────────── */
.lc-feature-step-err { padding: 0.2em 1em 0.4em 2.65em; font-size: 0.8em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; color: #dc2626; white-space: pre-wrap; }
.lc-feature-builtin-footer { border-top: 1px solid #f3f4f6; padding: 0.25em 1em 0.3em; }
.lc-feature-builtin-row { font-size: 0.75em; color: #9ca3af; line-height: 1.6; }
.lc-feature-builtin-row.fail { color: #dc2626; font-weight: 500; }

/* ── Prism token colours (One Dark–ish, scoped to feature impl panels) ── */
.lc-feature-step-impl .token.comment    { color: #6b7280; font-style: italic; }
.lc-feature-step-impl .token.string     { color: #86efac; }
.lc-feature-step-impl .token.number     { color: #fda4af; }
.lc-feature-step-impl .token.keyword    { color: #c084fc; font-weight: 600; }
.lc-feature-step-impl .token.builtin    { color: #67e8f9; }
.lc-feature-step-impl .token.operator   { color: #94a3b8; }
.lc-feature-step-impl .token.punctuation{ color: #94a3b8; }
.lc-feature-step-impl .token.function   { color: #93c5fd; }
.lc-feature-step-impl .token.boolean    { color: #fda4af; }
.lc-feature-step-impl pre               { background: #1e1e2e !important; }
.lc-feature-step-impl pre code          { color: #cdd6f4; }

/* ── fallback plain body (display-only) ──────────────────────────────────── */
.lc-feature-body pre { margin: 0; border-radius: 0; border: none; box-shadow: none; }
.lc-feature-body pre code { font-size: 0.83em; line-height: 1.6; }

/* ── suite dashboard ──────────────────────────────────────────────────────── */
.lc-feature-suite { border: 1px solid #e5e7eb; border-radius: 8px; margin: 0 0 0.5em; background: #fff; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
.lc-suite-header { display: flex; align-items: center; gap: 0.7em; padding: 0.55em 1em; background: #f9fafb; border-bottom: 1px solid #e5e7eb; font-size: 0.88em; }
.lc-suite-title { font-weight: 600; color: #111827; }
.lc-suite-summary { flex: 1; font-size: 0.82em; color: #6b7280; }
.lc-suite-summary .ok  { color: #16a34a; font-weight: 500; }
.lc-suite-summary .err { color: #dc2626; font-weight: 500; }
.lc-suite-run { background: #0066cc; color: #fff; border: none; border-radius: 4px; padding: 0.25em 0.85em; font-size: 0.8em; font-weight: 500; cursor: pointer; flex-shrink: 0; }
.lc-suite-run:hover:not(:disabled) { background: #0052a3; }
.lc-suite-run:disabled { background: #9ca3af; cursor: progress; }

.lc-suite-row { display: flex; align-items: center; gap: 0.6em; padding: 0.4em 1em; border-bottom: 1px solid #f3f4f6; font-size: 0.88em; cursor: pointer; transition: background 0.1s; }
.lc-suite-row:last-child { border-bottom: none; }
.lc-suite-row:hover { background: #f9fafb; }
.lc-suite-row-icon { flex-shrink: 0; width: 1.1em; text-align: center; color: #9ca3af; font-size: 1em; transition: color 0.2s; }
.lc-suite-row-icon.pass { color: #16a34a; }
.lc-suite-row-icon.fail { color: #dc2626; }
.lc-suite-row-icon.pending { color: #f59e0b; }
.lc-suite-row-name { font-weight: 500; color: #111827; flex: 1; min-width: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.lc-suite-row-tags { display: flex; gap: 0.3em; flex-shrink: 0; }
.lc-suite-row-tag { background: #e0f2fe; color: #075985; padding: 0.08em 0.45em; border-radius: 99px; font-size: 0.75em; font-weight: 500; }
.lc-suite-row-arrow { flex-shrink: 0; color: #9ca3af; font-size: 0.85em; padding-left: 0.3em; }
</style>

<script>
(function () {

  /* ── Shared MicroPython module promise ─────────────────────────────────── */
  var _mpModuleP = null;
  function getMpModule() {
    if (!_mpModuleP) {
      _mpModuleP = import("https://cdn.jsdelivr.net/npm/@micropython/micropython-webassembly-pyscript@latest/micropython.mjs");
    }
    return _mpModuleP;
  }

  /* ── Parse Gherkin rows ──────────────────────────────────────────────── */
  function parseGherkinRows(text) {
    var rows = [];
    var inPy = false, pyLines = [];
    text.split("\n").forEach(function(l) {
      var t = l.trim();
      if (inPy) {
        if (t === ":::") {
          rows.push({ kind: "python", code: pyLines.join("\n") });
          inPy = false;
        } else {
          pyLines.push(l);
        }
        return;
      }
      if (t === ":::python") { inPy = true; pyLines = []; return; }
      var hm = t.match(/^(Feature|Scenario(?:\s+Outline)?|Background|Examples)\s*:\s*(.*)/i);
      if (hm) { rows.push({ kind: /^feature$/i.test(hm[1]) ? "feature" : "scenario", keyword: hm[1], text: hm[2].trim() }); return; }
      var sm = t.match(/^(Given|When|Then|And|But)\s+(.*)/i);
      if (sm) { rows.push({ kind: "step", keyword: sm[1], text: sm[2].trim() }); return; }
      var um = t.match(/^(As an?\s+|I want\s+|So that\s+|In order to\s+)(.*)/i);
      if (um) { rows.push({ kind: "story", keyword: um[1].trimRight(), text: um[2].trim() }); return; }
      if (t && !/^#/.test(t)) rows.push({ kind: "narrative", text: t });
    });
    // attach :::python::: blocks to their preceding step
    for (var i = rows.length - 1; i > 0; i--) {
      if (rows[i].kind === "python" && rows[i-1].kind === "step") {
        rows[i-1].code = rows[i].code;
        rows.splice(i, 1);
      }
    }
    return rows;
  }

  /* ── Parse Python into per-step chunks ────────────────────────────────────────── */
  var PY_STEP_RE = /^\s*#\s*(Given|When|Then|And|But)\b/i;
  function parsePyChunks(pyText) {
    var chunks = [], cur = null;
    pyText.split("\n").forEach(function(l) {
      if (PY_STEP_RE.test(l)) {
        if (cur !== null) chunks.push(cur.join("\n").trim());
        cur = [];
      } else if (cur !== null) {
        cur.push(l);
      }
    });
    if (cur !== null) chunks.push(cur.join("\n").trim());
    return chunks.filter(function(c) { return c.length > 0; });
  }

  /* ── the learner's OWN results, remembered like karma ─────────────────
     status="…" in the page is the AUTHOR's declaration — one value for
     everyone, and never machine-set. What a LEARNER's run produced is
     theirs, and it used to evaporate on reload while their quiz score
     survived: the same page said "you scored 3/3" and "nothing has run
     here". Keyed by page + feature id, in the same store karma uses, so
     both halves of a page's evidence live or die together. */
  function cardName(card) {
    /* a named card keys on its name; an unnamed one on its position among
       the page's cards — the same "Nth .feature" convention the editor's
       write-back uses, so an author owes nothing extra for the memory */
    var id = card.getAttribute("data-lc-id") || card.id;
    if (id) return id;
    var all = document.querySelectorAll(".lc-feature");
    var i = Array.prototype.indexOf.call(all, card);
    return i >= 0 ? "n" + i : "";
  }
  function resultKey(card) {
    var page = window.lcPageScores ? window.lcPageScores.norm() : location.pathname;
    return page + "#" + cardName(card);
  }
  function loadResults() {
    try { return JSON.parse(localStorage.getItem("lc_features") || "{}"); }
    catch (e) { return {}; }
  }
  function rememberResult(card, status) {
    if (!status || status === "pending") return;   /* mid-run is not a result */
    if (!cardName(card)) return;
    try {
      var all = loadResults();
      all[resultKey(card)] = { status: status, ts: new Date().toISOString() };
      localStorage.setItem("lc_features", JSON.stringify(all));
      /* same debounced write as a quiz: the bench keeps the durable copy */
      document.dispatchEvent(new CustomEvent("lc-feature-result"));
    } catch (e) {}
  }
  /* on load, a card shows what the reader's last run made of it — the
     author's status is the starting point, their evidence outranks it */
  function restoreResult(card) {
    if (!cardName(card)) return;
    var rec = loadResults()[resultKey(card)];
    if (rec && rec.status) {
      card.setAttribute("data-lc-remembered", "1");
      setCardStatus(card, rec.status);
    }
  }
  window.lcFeatureResults = { all: loadResults, restore: restoreResult };

  /* ── Update badge + notify suite row ────────────────────────────────────────── */
  function setCardStatus(card, status) {
    var was = card.getAttribute("data-status") || "";
    card.classList.remove("lc-feature-passing", "lc-feature-failing", "lc-feature-pending");
    if (status) card.classList.add("lc-feature-" + status);
    /* the card IS page state: expose it, and let the cells recompute — a
       block gated with visible="= audit.passing" opens the moment the run
       turns green. Same event the forms fire; one recompute path. */
    card.setAttribute("data-status", status || "");
    rememberResult(card, status);
    if (was !== (status || "")) {
      try { document.dispatchEvent(new CustomEvent("lc-model-changed")); } catch (e) {}
      /* celebration="true": a burst for work that was EARNED. Every run
         dips through "pending", so the honest question is what the card's
         last SETTLED state was: failing → passing is a repair (celebrate),
         passing → passing is a re-run (nothing earned), and a first-ever
         pass counts too. Break it and fix it again and it celebrates
         again — a once-per-page latch would call the second repair
         worthless. */
      if (status === "passing" && (card.getAttribute("data-celebration") || "") === "true"
          && card._lcSettled !== "passing") {
        if (window.lcConfetti) window.lcConfetti(card);
      }
      if (status === "passing" || status === "failing") card._lcSettled = status;
    }
    var badge = card.querySelector("[data-lc-badge]");
    if (badge) {
      badge.className = "lc-feature-badge" + (status ? " lc-feature-badge-" + status : "");
      badge.style.display = status ? "" : "none";
      badge.textContent = status || "";
    }
    /* update linked suite row if present */
    if (card._lcSuiteRow) {
      var icon = card._lcSuiteRow.querySelector(".lc-suite-row-icon");
      if (icon) {
        icon.className = "lc-suite-row-icon" + (status === "passing" ? " pass" : status === "failing" ? " fail" : status === "pending" ? " pending" : "");
        icon.textContent = status === "passing" ? "✓" : status === "failing" ? "✗" : "●";
      }
    }
    if (card._lcSuiteEl) updateSuiteSummary(card._lcSuiteEl);

    /* write status back to editor source so the user can save the result.
       Works whether the feature was run in the main preview (#ed-preview)
       or the editor's Features tab (#ed-feat-preview): the card's position
       among its container's cards = the Nth {: .feature } in the source. */
    var host = card.closest && card.closest("#ed-preview, #ed-feat-preview");
    var inp = document.getElementById("ed-input");
    if (host && inp && status) {
      var allCards = host.querySelectorAll(".lc-feature");
      var idx = Array.prototype.indexOf.call(allCards, card);
      if (idx >= 0) {
        var count = -1;
        var newSrc = inp.value.replace(/(\{:\s*\.feature\b)([^}]*)(\})/g, function(m, open, attrs, close) {
          count++;
          if (count !== idx) return m;
          attrs = /\bstatus="[^"]*"/.test(attrs)
            ? attrs.replace(/\bstatus="[^"]*"/, 'status="' + status + '"')
            : attrs.trimRight() + ' status="' + status + '"';
          return open + attrs + close;
        });
        if (newSrc !== inp.value) {
          inp.value = newSrc;
          var ev = document.createEvent("Event");
          ev.initEvent("input", true, true);
          inp.dispatchEvent(ev);
        }
      }
    }
  }

  /* ── Update suite summary line ────────────────────────────────────────────────────── */
  function updateSuiteSummary(suiteEl) {
    var rows = suiteEl.querySelectorAll(".lc-suite-row");
    var pass = 0, fail = 0, pend = 0;
    rows.forEach(function(r) {
      var ic = r.querySelector(".lc-suite-row-icon");
      if (!ic) return;
      if (ic.classList.contains("pass"))    pass++;
      else if (ic.classList.contains("fail")) fail++;
      else                                   pend++;
    });
    var summary = suiteEl.querySelector(".lc-suite-summary");
    if (!summary) return;
    var parts = [];
    if (pass) parts.push("<span class='ok'>✓ " + pass + " passing</span>");
    if (fail) parts.push("<span class='err'>✗ " + fail + " failing</span>");
    if (pend && (pass || fail)) parts.push(pend + " pending");
    summary.innerHTML = parts.join(" &nbsp; ");
  }

  /* ── Run inline :::python::: steps via steps runtime ─────────────────────── */
  function runFeatureNew(card, runBtn) {
    var stepEls = card.querySelectorAll(".lc-feature-step.has-impl");
    stepEls.forEach(function(s) {
      s.querySelector(".lc-feature-step-icon").className = "lc-feature-step-icon";
      s.querySelector(".lc-feature-step-icon").textContent = "●";
      s.querySelector(".lc-feature-step-time").textContent = "";
      var err = s.querySelector(".lc-feature-step-err");
      if (err) err.parentNode.removeChild(err);
    });
    setCardStatus(card, "pending");
    if (runBtn) { runBtn.disabled = true; runBtn.textContent = "…"; }

    var scenarioParts = [];
    stepEls.forEach(function(s, i) {
      var kw  = (s.querySelector(".lc-feature-step-keyword") || {}).textContent || "";
      var txt = (s.querySelector(".lc-feature-step-text")    || {}).textContent || "";
      var label = (kw + " " + txt).trim();
      var body = (s._lcPyCode || "").replace(/^\n+|\n+$/g, "");
      var indented = body.split("\n").map(function(l) { return "    " + l; }).join("\n");
      scenarioParts.push("@scenario(" + JSON.stringify(label) + ")\ndef _s" + i + "(self):\n" + (indented || "    pass"));
    });

    var preamble = (document.getElementById("lc-steps-preamble") || {}).textContent || "";
    var fullCode = preamble + "\n" + scenarioParts.join("\n\n") + "\n_run_all()";

    if (!window._lcMpReady) {
      /* ONE interpreter per page (see pyrun's lcMpy): loading our own here
         would silently kill the cells/editor runtime — the wasm is a singleton */
      window._lcMpReady = window.lcMpy ? window.lcMpy() : getMpModule()
        .then(function(mjs) { return mjs.loadMicroPython({ stdout: function(){}, stderr: function(){} }); });
    }
    var mpP = window._lcMpReady;

    window._lcStepsResult = null;
    return mpP.then(function(mp) {
      var runFn = mp.runPython || mp.exec || mp.pyexec || mp.run;
      var jsonStr;
      try { if (runFn) jsonStr = runFn.call(mp, fullCode); } catch(e) {}
      if (jsonStr == null) jsonStr = window._lcStepsResult;
      var results = [];
      try { results = JSON.parse(jsonStr) || []; } catch(e) {}

      var builtinResults = results.slice(0, 2);
      var userResults    = results.slice(2);
      var allPass = true;

      /* show user step results */
      stepEls.forEach(function(s, i) {
        var r = userResults[i];
        var icon = s.querySelector(".lc-feature-step-icon");
        if (!r) { icon.className = "lc-feature-step-icon skip"; icon.textContent = "○"; return; }
        if (r.status === "pass") {
          icon.className = "lc-feature-step-icon pass"; icon.textContent = "✓";
        } else {
          allPass = false;
          icon.className = "lc-feature-step-icon fail"; icon.textContent = "✗";
          var errDiv = document.createElement("div");
          errDiv.className = "lc-feature-step-err";
          /* Two audiences, two failures (same rule as the legacy runner
             below): an AssertionError is the page talking to the LEARNER —
             show its message alone. Anything else is the ENGINE falling
             short of the page — a site serving an older runtime than the
             content expects. Never hand a learner that traceback. */
          var rawErr = (r.error || "failed").trim();
          if (rawErr.indexOf("AssertionError") >= 0) {
            errDiv.textContent = rawErr.replace(/^.*AssertionError:?\s*/, "") || "assertion failed";
          } else {
            errDiv.textContent = engineErrText(rawErr);
          }
          s.querySelector(".lc-feature-step-row").insertAdjacentElement("afterend", errDiv);
        }
      });

      /* A non-assertion failure is the page's CHECK falling over, not the learner
     failing. There are two reasons for that and they need different words:

       · the page asks the runtime for something it does not have — usually an
         author's slip (Datagrid has row_count, not count), sometimes a page
         genuinely newer than the deployed engine
       · anything else — a real error inside the check

     The old text asserted the first cause AND prescribed a cure: "after the
     next publish, reload and run again". When the cause was a typo, Michel
     published, nothing changed, and the message had sent him after a fix that
     could never work (2026-08-06). Never prescribe an action that may not
     help: name what happened and say whose problem it is. */
  function engineErrText(raw) {
    var e = String(raw || "").trim();
    if (/AttributeError|NameError|has no attribute/.test(e)) {
      return "\u2699\ufe0f Not you — this page's own check asks for something the engine "
           + "does not have, so it cannot run. That is the page's bug, not yours. "
           + "(" + e + ")";
    }
    return "\u2699\ufe0f Not you — this page's check could not run. That is the page's "
         + "bug, not yours. (" + e + ")";
  }

  /* show built-in check results as a footer — always, pass or fail */
      var body = card.querySelector("[data-lc-body]");
      var oldFooter = card.querySelector(".lc-feature-builtin-footer");
      if (oldFooter) oldFooter.parentNode.removeChild(oldFooter);
      var footer = document.createElement("div");
      footer.className = "lc-feature-builtin-footer";
      builtinResults.forEach(function(r) {
        var row = document.createElement("div");
        row.className = "lc-feature-builtin-row " + (r.status === "pass" ? "pass" : "fail");
        row.textContent = (r.status === "pass" ? "✓ " : "✗ ") + r.label;
        if (r.status !== "pass") { allPass = false; row.title = r.error; }
        footer.appendChild(row);
      });
      if (body) body.appendChild(footer);

      setCardStatus(card, allPass ? "passing" : "failing");
      if (runBtn) { runBtn.disabled = false; runBtn.textContent = "▶ Run"; }
    }).catch(function() {
      setCardStatus(card, "failing");
      if (runBtn) { runBtn.disabled = false; runBtn.textContent = "▶ Run"; }
    });
  }

  /* ── Run all step chunks for one card (returns Promise) ─────────────────────── */
  function runFeature(card, runBtn) {
    var stepEls = card.querySelectorAll(".lc-feature-step.has-impl");
    stepEls.forEach(function(s) {
      s.querySelector(".lc-feature-step-icon").className = "lc-feature-step-icon";
      s.querySelector(".lc-feature-step-icon").textContent = "●";
      s.querySelector(".lc-feature-step-time").textContent = "";
      var err = s.querySelector(".lc-feature-step-err");
      if (err) err.parentNode.removeChild(err);
    });
    setCardStatus(card, "pending");
    if (runBtn) { runBtn.disabled = true; runBtn.textContent = "…"; }

    return (window.lcMpy ? window.lcMpy() : getMpModule()
      .then(function(mjs) {
        return mjs.loadMicroPython({ stdout: function(){}, stderr: function(){} });
      }))
      .then(function(mp) {
        var allPass = true, stopped = false;
        stepEls.forEach(function(s) {
          var icon = s.querySelector(".lc-feature-step-icon");
          var timeEl = s.querySelector(".lc-feature-step-time");
          if (stopped) { icon.className = "lc-feature-step-icon skip"; icon.textContent = "○"; return; }
          var code = s._lcPyCode || "";
          var t0 = Date.now();
          try {
            mp.runPython(code);
            icon.className = "lc-feature-step-icon pass"; icon.textContent = "✓";
            timeEl.textContent = (Date.now() - t0) + "ms";
          } catch (e) {
            allPass = false; stopped = true;
            icon.className = "lc-feature-step-icon fail"; icon.textContent = "✗";
            timeEl.textContent = (Date.now() - t0) + "ms";
            var errDiv = document.createElement("div");
            errDiv.className = "lc-feature-step-err";
            /* Two audiences, two failures. An AssertionError is the page
               talking to the LEARNER — show its message, nothing else.
               Anything else (AttributeError, NameError…) is the ENGINE
               falling short of the page — usually a site serving an older
               runtime than the content expects. A learner must never face
               that as a traceback. */
            var raw = (e.message || String(e)).trim();
            var lines = raw.split("\n").filter(function(l){ return l.trim(); });
            var last = lines.length ? lines[lines.length - 1] : raw;
            if (last.indexOf("AssertionError") >= 0) {
              errDiv.textContent = last.replace(/^.*AssertionError:?\s*/, "") || "assertion failed";
            } else {
              errDiv.textContent = engineErrText(last);
            }
            s.querySelector(".lc-feature-step-row").insertAdjacentElement("afterend", errDiv);
          }
        });
        setCardStatus(card, allPass ? "passing" : "failing");
        if (runBtn) { runBtn.disabled = false; runBtn.textContent = "▶ Run"; }
        return allPass;
      })
      .catch(function() {
        setCardStatus(card, "failing");
        if (runBtn) { runBtn.disabled = false; runBtn.textContent = "▶ Run"; }
        return false;
      });
  }

  /* ── Build a <pre><code> with Prism highlighting ────────────────────────────────── */
  /* ── GIVEN / WHEN / THEN, IN THE FLOW'S OWN COLOURS ─────────────────
     Michel, 2026-08-11: a step's words carry the same grammar the event
     flow does, so they should wear the same paint. What is NOT done here
     is guessing which words mean what — that would be confidently wrong
     in front of a learner. The KEYWORD already says it:

         Given …  📦 data      When …  🗣️ command     Then …  ⚡ event

     and only MARKED words are painted — `backticked` or **bold** — so the
     author chooses what matters. An IAL after the mark overrides the
     default: **is open**{: .event } inside a Given. And/But inherit the
     last real keyword. Everything else renders as ordinary markdown. */
  var GWT = { given: "data", when: "command", then: "event" };
  var lastGwt = "";
  var MARK = /(?:\*\*([^*]+)\*\*|`([^`]+)`)(?:\{:\s*\.([a-z_]+)\s*\})?/g;

  function paintGwt(text, keyword) {
    var esc = window.lcEscapeHtml || function (x) { return String(x); };
    var fallback = GWT[String(keyword || "").toLowerCase()] || "";
    var kindOf = window.lcFlowKind || function () { return ""; };
    return esc(text).replace(MARK, function (m, bold, code, cls) {
      var word = bold != null ? bold : code;
      var kind = cls ? kindOf(cls) : fallback;
      if (!kind)
        return bold != null ? "<strong>" + word + "</strong>" : "<code>" + word + "</code>";
      return "<mark class='lc-gwt lc-ef-" + kind + "' data-kind='" + kind + "'>" +
             word + "</mark>";
    });
  }

  function buildPyPre(code) {
    var pre = document.createElement("pre");
    var codeEl = document.createElement("code");
    codeEl.className = "language-python";
    codeEl.textContent = code;
    pre.appendChild(codeEl);
    var loader = window.lcLoadPrism || function() { return Promise.resolve(); };
    loader().then(function() {
      if (window.Prism && window.Prism.languages && window.Prism.languages.python) {
        try { window.Prism.highlightElement(codeEl); } catch (e) {}
      }
    });
    return pre;
  }

  /* ── Upgrade a .feature element into a card ──────────────────────────────────────────── */
  function upgradeFeature(el) {
    if (el.dataset.lcFeatureUpgraded) return;
    el.dataset.lcFeatureUpgraded = "1";

    var status  = el.getAttribute("status") || "";
    var tagsRaw = el.getAttribute("tags") || "";
    var code    = el.querySelector("code");
    var text    = code ? code.textContent : el.textContent;
    var rows    = parseGherkinRows(text);

    var featureName = "";
    for (var ri = 0; ri < rows.length; ri++) {
      if (rows[ri].kind === "feature") { featureName = rows[ri].text; break; }
    }
    if (!featureName) featureName = text.trim().split("\n")[0].replace(/^Feature:\s*/i, "").trim() || "Feature";

    var badgeHtml = status
      ? "<span class='lc-feature-badge lc-feature-badge-" + status + "' data-lc-badge>" + status + "</span>"
      : "<span class='lc-feature-badge' data-lc-badge style='display:none'></span>";

    /* A tag NAMES a thing — a component, a concern — and the platform's names
       are snake_case (doctrine 2). "impact_map" is how the author writes it
       and how a filter matches it; "impact map" is how a reader reads it. The
       chip shows the reader's version, data-tag keeps the author's. */
    function tagLabel(t) { return t.replace(/_/g, " "); }

    var tagsHtml = "";
    if (tagsRaw) {
      tagsHtml = "<span class='lc-feature-tags'>"
        + tagsRaw.split(",").map(function(t) {
            var v = t.trim();
            return "<span class='lc-feature-tag' data-tag='" + v + "'>" + tagLabel(v) + "</span>";
          }).join("") + "</span>";
    }

    var lcId = el.getAttribute("id") || "";
    /* Hidden by default: a .feature is a spec/test, not learner-facing content.
       It only shows when the author opts in with visible="true" (or a .visible
       class). Inside the editor preview it always shows so authors can work. */
    var inEditor  = el.closest && el.closest("#ed-preview, #ed-feat-preview");
    var visAttr   = el.getAttribute("visible");
    var isVisible = !!inEditor || el.classList.contains("visible") || (visAttr != null && visAttr !== "false");
    var card = document.createElement("div");
    card.className = "lc-feature" + (status ? " lc-feature-" + status : "") + (isVisible ? "" : " lc-feature-hidden");
    card._lcHidden = !isVisible;
    if (lcId) card.setAttribute("data-lc-id", lcId);
    var celebration = el.getAttribute("celebration");
    if (celebration) card.setAttribute("data-celebration", celebration);
    /* grades="<slot id>": this check GRADES a bench slot. The learner owns
       the file in the slot, so a check living inside it could be weakened
       or deleted — self-assessment through the back door. The lesson's
       check is in the vault and cannot be edited by the person it marks,
       which is why the slot only turns green when THIS card passes
       (Michel, 2026-08-11). */
    var grades = el.getAttribute("grades");
    if (grades) card.setAttribute("data-grades", grades);
    card._lcFeatureName = featureName;
    card._lcFeatureTags = tagsRaw ? tagsRaw.split(",").map(function(t){ return t.trim(); }) : [];

    card.innerHTML =
      "<div class='lc-feature-header'>"
        + "<span class='lc-feature-name'>" + featureName + "</span>"
        + badgeHtml + tagsHtml
      + "</div>"
      + "<div class='lc-feature-body' data-lc-body></div>";

    var body = card.querySelector("[data-lc-body]");
    var hasSteps = rows.some(function(r) { return r.kind === "step"; });
    var hasInlineCode = rows.some(function(r) { return r.kind === "step" && r.code; });

    if (hasSteps) {
      var stepsDiv = document.createElement("div");
      stepsDiv.className = "lc-feature-steps";
      rows.forEach(function(r) {
        if (r.kind === "feature") return;
        if (r.kind === "scenario") {
          var sh = document.createElement("div"); sh.className = "lc-feature-scenario";
          sh.textContent = r.keyword + ": " + r.text; stepsDiv.appendChild(sh);
        } else if (r.kind === "story") {
          var sh2 = document.createElement("div"); sh2.className = "lc-feature-story";
          sh2.innerHTML = "<span class='lc-feature-story-keyword'>" + r.keyword + "</span><span class='lc-feature-story-text'>" + r.text + "</span>";
          stepsDiv.appendChild(sh2);
        } else if (r.kind === "narrative") {
          var nh = document.createElement("div"); nh.className = "lc-feature-narrative";
          nh.textContent = r.text; stepsDiv.appendChild(nh);
        } else if (r.kind === "step") {
          var isAnd = /^(And|But)$/i.test(r.keyword);
          if (!isAnd) lastGwt = r.keyword;
          var stepEl = document.createElement("div"); stepEl.className = "lc-feature-step" + (isAnd ? " lc-step-and" : "");
          stepEl.innerHTML =
            "<div class='lc-feature-step-row'>"
              + "<span class='lc-feature-step-icon'>●</span>"
              + "<span class='lc-feature-step-keyword'>" + r.keyword + "</span>"
              + "<span class='lc-feature-step-text'>" + paintGwt(r.text, isAnd ? lastGwt : r.keyword) + "</span>"
              + "<span class='lc-feature-step-time'></span>"
            + "</div>";
          if (r.code) {
            var bodyCode = r.code.replace(/^\n+|\n+$/g, "");
            var dedented = bodyCode.replace(/^(    |\t)/gm, "");
            stepEl.classList.add("has-impl");
            stepEl._lcPyCode = dedented;
            var implDiv = document.createElement("div");
            implDiv.className = "lc-feature-step-impl";
            implDiv.appendChild(buildPyPre(dedented));
            stepEl.appendChild(implDiv);
            stepEl.querySelector(".lc-feature-step-row").addEventListener("click", function() {
              implDiv.classList.toggle("open");
            });
          }
          stepsDiv.appendChild(stepEl);
        }
      });
      body.appendChild(stepsDiv);

      if (hasInlineCode) {
        var runBtn2 = document.createElement("button");
        runBtn2.className = "lc-feature-run lc-feature-run-btn";
        runBtn2.textContent = "▶ Run";
        card.querySelector(".lc-feature-header").appendChild(runBtn2);
        (function(btn) {
          btn.addEventListener("click", function() { runFeatureNew(card, btn); });
        })(runBtn2);
      } else {
        /* steps exist but none implemented — pending runner */
        var pendingBtn = document.createElement("button");
        pendingBtn.className = "lc-feature-run lc-feature-run-pending";
        pendingBtn.textContent = "▶ Run";
        card.querySelector(".lc-feature-header").appendChild(pendingBtn);
        (function(btn) {
          btn.addEventListener("click", function() {
            card.querySelectorAll(".lc-feature-step").forEach(function(s) {
              var icon = s.querySelector(".lc-feature-step-icon");
              if (icon) { icon.className = "lc-feature-step-icon"; icon.textContent = "○"; }
            });
            setCardStatus(card, "pending");
          });
        })(pendingBtn);
      }
    } else {
      var cloned = el.cloneNode(true);
      cloned.removeAttribute("status"); cloned.removeAttribute("tags"); cloned.classList.remove("feature");
      body.appendChild(cloned);
    }

    el.parentNode.replaceChild(card, el);
    /* the reader's own last run outranks the author's declaration — restore
       it once the card is in the document, so the position key is stable */
    restoreResult(card);
  }

  /* ── Upgrade a .steps element — attach to preceding card ────────────────────────── */
  function upgradeSteps(el) {
    var code   = el.querySelector("code");
    var pyText = code ? code.textContent : el.textContent;
    var chunks = parsePyChunks(pyText);

    var card = null, sib = el.previousElementSibling;
    while (sib) {
      if (sib.classList.contains("lc-feature")) { card = sib; break; }
      if (!sib.textContent.trim()) { sib = sib.previousElementSibling; continue; }
      break;
    }

    if (card && chunks.length) {
      var stepEls = card.querySelectorAll(".lc-feature-step");
      chunks.forEach(function(chunk, idx) {
        if (idx >= stepEls.length) return;
        var stepEl = stepEls[idx];
        stepEl.classList.add("has-impl");
        stepEl._lcPyCode = chunk;
        var implDiv = document.createElement("div");
        implDiv.className = "lc-feature-step-impl";
        implDiv.appendChild(buildPyPre(chunk));
        stepEl.appendChild(implDiv);
        stepEl.querySelector(".lc-feature-step-row").addEventListener("click", function() {
          implDiv.classList.toggle("open");
        });
      });

      var runBtn = document.createElement("button");
      runBtn.className = "lc-feature-run";
      runBtn.textContent = "▶ Run";
      card.querySelector(".lc-feature-header").appendChild(runBtn);
      runBtn.addEventListener("click", function() { runFeature(card, runBtn); });
    }

    el.parentNode.removeChild(el);
  }

  /* ── Build the suite dashboard ───────────────────────────────────────────────────────────── */
  function buildSuite(root) {
    /* collect all runnable cards in DOM order within this root */
    var allCards = (root || document).querySelectorAll(".lc-feature");
    var runnable = [];
    allCards.forEach(function(c) { if (c.querySelector(".lc-feature-run") && !c._lcHidden) runnable.push(c); });
    if (runnable.length < 2) return;

    var suite = document.createElement("div");
    suite.className = "lc-feature-suite";

    /* header */
    var hdr = document.createElement("div");
    hdr.className = "lc-suite-header";
    hdr.innerHTML =
      "<span class='lc-suite-title'>Test Suite</span>"
      + "<span class='lc-suite-summary'></span>"
      + "<button class='lc-suite-run'>▶ Run All</button>";
    suite.appendChild(hdr);

    /* one row per runnable card */
    runnable.forEach(function(card) {
      var tags = (card._lcFeatureTags || []);
      var tagsHtml = tags.map(function(t) {
        return "<span class='lc-suite-row-tag' data-tag='" + t + "'>"
          + t.replace(/_/g, " ") + "</span>";
      }).join("");

      var row = document.createElement("div");
      row.className = "lc-suite-row";
      row.innerHTML =
        "<span class='lc-suite-row-icon'>●</span>"
        + "<span class='lc-suite-row-name'>" + (card._lcFeatureName || "Feature") + "</span>"
        + (tagsHtml ? "<span class='lc-suite-row-tags'>" + tagsHtml + "</span>" : "")
        + "<span class='lc-suite-row-arrow'>↓</span>";
      suite.appendChild(row);

      /* scroll to card on click */
      row.addEventListener("click", function() {
        card.scrollIntoView({ behavior: "smooth", block: "center" });
      });

      /* cross-link card ↔ row for live status updates */
      card._lcSuiteRow = row;
      card._lcSuiteEl  = suite;

      /* reflect initial status in row icon */
      var initStatus = card.classList.contains("lc-feature-passing") ? "passing"
                     : card.classList.contains("lc-feature-failing")  ? "failing"
                     : card.classList.contains("lc-feature-pending")  ? "pending" : "";
      if (initStatus) setCardStatus(card, initStatus);
      /* …then the reader's own last run, which outranks the declaration */
      restoreResult(card);
    });

    /* Run All */
    hdr.querySelector(".lc-suite-run").addEventListener("click", function() {
      var runAllBtn = this;
      runAllBtn.disabled = true; runAllBtn.textContent = "…";
      var chain = Promise.resolve();
      runnable.forEach(function(card) {
        chain = chain.then(function() {
          var btn = card.querySelector(".lc-feature-run");
          if (btn && btn.classList.contains("lc-feature-run-pending")) {
            btn.click();
            return Promise.resolve();
          }
          var isNew = !!(btn && btn.classList.contains("lc-feature-run-btn"));
          return isNew ? runFeatureNew(card, btn) : runFeature(card, btn);
        });
      });
      chain.then(function() {
        runAllBtn.disabled = false; runAllBtn.textContent = "▶ Run All";
        updateSuiteSummary(suite);
      }).catch(function() {
        runAllBtn.disabled = false; runAllBtn.textContent = "▶ Run All";
      });
    });

    /* insert before the first runnable card */
    runnable[0].parentNode.insertBefore(suite, runnable[0]);
    updateSuiteSummary(suite);
  }

  /* ── Main init (accepts an optional root for preview) ────────────────────────────── */
  function init(root) {
    root = root || document;
    root.querySelectorAll(".feature").forEach(upgradeFeature);
    root.querySelectorAll(".steps").forEach(upgradeSteps);
    buildSuite(root);
  }

  /* ── Boot on the real page ─────────────────────────────────────────────────────────────── */
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function() { init(document); });
  } else {
    init(document);
  }

  /* ── Register with editor preview pipeline ───────────────────────────────────────── */
  var _origScan = window.lcScanElement;
  window.lcScanElement = function(root) {
    if (_origScan) _origScan(root);
    root.querySelectorAll(".feature").forEach(upgradeFeature);
    root.querySelectorAll(".steps").forEach(upgradeSteps);
    buildSuite(root);
  };

})();
</script>
