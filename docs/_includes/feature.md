{%- comment -%}
Feature (Gherkin BDD) widget + Python step runner.

Two blocks, one visual card on the page. The .steps block is completely
removed from the DOM — its Python is distributed into the feature card's
expandable step rows.

  ```gherkin
  Feature: Temperature converter
    Scenario: Celsius to Fahrenheit
      Given a temperature of 100°C
      When converted to Fahrenheit
      Then the result is 212
  ```
  {: .feature status="pending" tags="math" }

  ```python
  # Given a temperature of 100°C
  celsius = 100

  # When converted to Fahrenheit
  fahrenheit = (celsius * 9 / 5) + 32

  # Then the result is 212
  assert fahrenheit == 212.0
  ```
  {: .steps }

Rules:
- The .steps block must immediately follow the .feature block.
- Each # Given/When/Then/And/But comment starts a new step chunk.
- Chunks are matched to Gherkin step rows by index (1st chunk → 1st step).
- State flows between steps — variables from earlier steps are available later.
- Clicking a step row expands/collapses its Python implementation.

Knobs for .feature:
  status="…"    passing | failing | pending
  tags="…"      comma-separated chips

Auto-included by docs/_layouts/default.html on every page.
{%- endcomment -%}

<style>
/* ── card shell ──────────────────────────────────────── */
.lc-feature { border: 1px solid #e5e7eb; border-left: 4px solid #9ca3af; border-radius: 0 8px 8px 0; margin: 1.2em 0; background: #fff; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
.lc-feature-passing { border-left-color: #22c55e; }
.lc-feature-failing  { border-left-color: #ef4444; }
.lc-feature-pending  { border-left-color: #f59e0b; }

/* ── header ──────────────────────────────────────────── */
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

/* ── scenario / narrative ────────────────────────────── */
.lc-feature-scenario { padding: 0.5em 1em 0.2em; font-size: 0.82em; font-weight: 600; color: #6b7280; letter-spacing: 0.03em; text-transform: uppercase; }
.lc-feature-narrative { padding: 0.1em 1em; font-size: 0.83em; color: #9ca3af; font-style: italic; }

/* ── step rows ───────────────────────────────────────── */
.lc-feature-steps { padding: 0.35em 0; }
.lc-feature-step { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
.lc-feature-step-row { display: flex; align-items: baseline; gap: 0.55em; padding: 0.28em 1em; font-size: 0.88em; line-height: 1.5; }
.lc-feature-step.has-impl > .lc-feature-step-row { cursor: pointer; }
.lc-feature-step.has-impl > .lc-feature-step-row:hover { background: #f3f4f6; }

.lc-feature-step-icon { flex-shrink: 0; width: 1.1em; text-align: center; color: #9ca3af; }
.lc-feature-step-icon.pass { color: #16a34a; }
.lc-feature-step-icon.fail { color: #dc2626; }
.lc-feature-step-icon.skip { color: #d1d5db; }
.lc-feature-step-keyword { color: #7c3aed; font-weight: 600; min-width: 3.5em; }
.lc-feature-step-text { color: #111827; }
.lc-feature-step-time { margin-left: auto; font-size: 0.75em; color: #9ca3af; }

/* ── expandable Python impl per step ─────────────────── */
.lc-feature-step-impl { display: none; border-top: 1px solid #f3f4f6; border-bottom: 1px solid #f3f4f6; }
.lc-feature-step-impl.open { display: block; }
.lc-feature-step-impl pre { margin: 0 !important; border-radius: 0 !important; border: none !important; box-shadow: none !important; max-height: 220px; overflow-y: auto; }
.lc-feature-step-impl pre code { font-size: 0.82em !important; line-height: 1.55 !important; }

/* ── error ───────────────────────────────────────────── */
.lc-feature-step-err { padding: 0.2em 1em 0.4em 2.65em; font-size: 0.8em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; color: #dc2626; white-space: pre-wrap; }

/* ── fallback plain body (no steps) ─────────────────── */
.lc-feature-body pre { margin: 0; border-radius: 0; border: none; box-shadow: none; }
.lc-feature-body pre code { font-size: 0.83em; line-height: 1.6; }
</style>

<script>
(function () {

  /* ── Shared MicroPython module promise ───────────────── */
  var _mpModuleP = null;
  function getMpModule() {
    if (!_mpModuleP) {
      _mpModuleP = import("https://cdn.jsdelivr.net/npm/@micropython/micropython-webassembly-pyscript@latest/micropython.mjs");
    }
    return _mpModuleP;
  }

  /* ── Parse Gherkin rows ──────────────────────────────── */
  function parseGherkinRows(text) {
    var rows = [];
    text.split("\n").forEach(function(l) {
      var t = l.trim();
      var hm = t.match(/^(Feature|Scenario(?:\s+Outline)?|Background|Examples)\s*:\s*(.*)/i);
      if (hm) { rows.push({ kind: /^feature$/i.test(hm[1]) ? "feature" : "scenario", keyword: hm[1], text: hm[2].trim() }); return; }
      var sm = t.match(/^(Given|When|Then|And|But)\s+(.*)/i);
      if (sm) { rows.push({ kind: "step", keyword: sm[1], text: sm[2].trim() }); return; }
      if (t && !/^#/.test(t)) rows.push({ kind: "narrative", text: t });
    });
    return rows;
  }

  /* ── Parse Python into per-step chunks ──────────────── */
  /* Split on lines that start with: # Given / # When / etc.  */
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

  /* ── Update badge ─────────────────────────────────────── */
  function setCardStatus(card, status) {
    card.classList.remove("lc-feature-passing", "lc-feature-failing", "lc-feature-pending");
    if (status) card.classList.add("lc-feature-" + status);
    var badge = card.querySelector("[data-lc-badge]");
    if (!badge) return;
    badge.className = "lc-feature-badge" + (status ? " lc-feature-badge-" + status : "");
    badge.style.display = status ? "" : "none";
    badge.textContent = status || "";
  }

  /* ── Run all step chunks ─────────────────────────────── */
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
    runBtn.disabled = true;
    runBtn.textContent = "…";

    getMpModule()
      .then(function(mjs) {
        return mjs.loadMicroPython({ stdout: function(){}, stderr: function(){} });
      })
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
            errDiv.textContent = (e.message || String(e)).replace(/^.*Error:\s*/, "");
            s.querySelector(".lc-feature-step-row").insertAdjacentElement("afterend", errDiv);
          }
        });
        setCardStatus(card, allPass ? "passing" : "failing");
        runBtn.disabled = false; runBtn.textContent = "▶ Run";
      })
      .catch(function() {
        setCardStatus(card, "failing");
        runBtn.disabled = false; runBtn.textContent = "▶ Run";
      });
  }

  /* ── Build a <pre><code> for inline Python display ───── */
  function buildPyPre(code) {
    var pre = document.createElement("pre");
    var codeEl = document.createElement("code");
    codeEl.className = "language-python";
    codeEl.textContent = code;
    pre.appendChild(codeEl);
    return pre;
  }

  /* ── Upgrade a .feature element into a card ──────────── */
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

    var tagsHtml = "";
    if (tagsRaw) {
      tagsHtml = "<span class='lc-feature-tags'>"
        + tagsRaw.split(",").map(function(t) {
            return "<span class='lc-feature-tag'>" + t.trim() + "</span>";
          }).join("")
        + "</span>";
    }

    var card = document.createElement("div");
    card.className = "lc-feature" + (status ? " lc-feature-" + status : "");
    card.innerHTML =
      "<div class='lc-feature-header'>"
        + "<span class='lc-feature-name'>" + featureName + "</span>"
        + badgeHtml + tagsHtml
      + "</div>"
      + "<div class='lc-feature-body' data-lc-body></div>";

    var body = card.querySelector("[data-lc-body]");
    var hasSteps = rows.some(function(r) { return r.kind === "step"; });

    if (hasSteps) {
      var stepsDiv = document.createElement("div");
      stepsDiv.className = "lc-feature-steps";
      rows.forEach(function(r) {
        if (r.kind === "feature") return;
        if (r.kind === "scenario") {
          var sh = document.createElement("div");
          sh.className = "lc-feature-scenario";
          sh.textContent = r.keyword + ": " + r.text;
          stepsDiv.appendChild(sh);
        } else if (r.kind === "narrative") {
          var nh = document.createElement("div");
          nh.className = "lc-feature-narrative";
          nh.textContent = r.text;
          stepsDiv.appendChild(nh);
        } else if (r.kind === "step") {
          var stepEl = document.createElement("div");
          stepEl.className = "lc-feature-step";
          stepEl.innerHTML =
            "<div class='lc-feature-step-row'>"
              + "<span class='lc-feature-step-icon'>●</span>"
              + "<span class='lc-feature-step-keyword'>" + r.keyword + "</span>"
              + "<span class='lc-feature-step-text'>" + r.text + "</span>"
              + "<span class='lc-feature-step-time'></span>"
            + "</div>";
          stepsDiv.appendChild(stepEl);
        }
      });
      body.appendChild(stepsDiv);
    } else {
      var cloned = el.cloneNode(true);
      cloned.removeAttribute("status"); cloned.removeAttribute("tags");
      cloned.classList.remove("feature");
      body.appendChild(cloned);
    }

    el.parentNode.replaceChild(card, el);
  }

  /* ── Upgrade a .steps element — attach to preceding card ─ */
  function upgradeSteps(el) {
    var code   = el.querySelector("code");
    var pyText = code ? code.textContent : el.textContent;
    var chunks = parsePyChunks(pyText);

    /* find nearest preceding .lc-feature card */
    var card = null, sib = el.previousElementSibling;
    while (sib) {
      if (sib.classList.contains("lc-feature")) { card = sib; break; }
      /* skip empty paragraphs between the two blocks */
      if (!sib.textContent.trim()) { sib = sib.previousElementSibling; continue; }
      break;
    }

    if (card && chunks.length) {
      var stepEls = card.querySelectorAll(".lc-feature-step");
      chunks.forEach(function(chunk, idx) {
        if (idx >= stepEls.length) return;
        var stepEl = stepEls[idx];
        stepEl.classList.add("has-impl");
        stepEl._lcPyCode = chunk;   /* store on DOM node — no attribute encoding issues */

        var implDiv = document.createElement("div");
        implDiv.className = "lc-feature-step-impl";
        implDiv.appendChild(buildPyPre(chunk));
        stepEl.appendChild(implDiv);

        stepEl.querySelector(".lc-feature-step-row").addEventListener("click", function() {
          implDiv.classList.toggle("open");
        });
      });

      /* inject Run button */
      var runBtn = document.createElement("button");
      runBtn.className = "lc-feature-run";
      runBtn.textContent = "▶ Run";
      card.querySelector(".lc-feature-header").appendChild(runBtn);
      runBtn.addEventListener("click", function() { runFeature(card, runBtn); });
    }

    /* always remove the .steps block from the page */
    el.parentNode.removeChild(el);
  }

  /* ── Boot ────────────────────────────────────────────── */
  function init() {
    /* feature first so cards exist before steps tries to find them */
    document.querySelectorAll(".feature").forEach(upgradeFeature);
    document.querySelectorAll(".steps").forEach(upgradeSteps);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

})();
</script>
