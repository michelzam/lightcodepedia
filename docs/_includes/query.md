{%- comment -%}
Query — a dataset computed by SQL over other datasets. A {: .query } IS a
dataset: it publishes its result under its id, so any grid / chart / stat
binds to it exactly like a hand-written {: .dataset }. The SQL runs in the
browser via AlaSQL (lazy-loaded, pinned). Reactive: it re-runs whenever an
input dataset changes, so editable-grid → query → chart updates live.

Usage:
  ```sql
  SELECT breed, AVG(cuteness) AS cuteness FROM dogs GROUP BY breed
  ```
  {: .query bind="dogs" #by_breed }

  [Cuteness by breed](#)
  {: .chart bind="by_breed" type="bar" x="breed" y="cuteness" }

IAL:
  bind="a,b"  input dataset id(s) — referenced as tables by id in the SQL
  id="..."    the result is published under this id (it's a dataset)

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-query {
  display: inline-flex; align-items: center; gap: 0.4em;
  font-size: 0.8em; color: #475569; background: #f1f5f9;
  border: 1px solid #e2e8f0; border-radius: 999px;
  padding: 0.12em 0.7em; margin: 0.3em 0;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
}
.lc-query.err { background: #fef2f2; border-color: #fecaca; color: #b91c1c; }
/* editable mode: a live SQL editor that publishes its result as a dataset */
.lc-query-wrap { margin: 0.6em 0; }
.lc-query-editor {
  width: 100%; box-sizing: border-box; resize: vertical;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 0.85em; line-height: 1.5; padding: 0.6em;
  border: 1px solid #d0d7de; border-radius: 6px; background: #fafafa; color: #111;
}
.lc-query-bar { display: flex; align-items: center; gap: 0.7em; margin-top: 0.4em; }
.lc-query-bar .button { font-size: 0.82em; padding: 0.3em 0.85em; }
</style>

<script>
(function () {
  if (window._lcQueryReady) return;
  window._lcQueryReady = true;
  window.lcDatasets = window.lcDatasets || {};
  window.lcDatasetListeners = window.lcDatasetListeners || {};

  var _p = null;
  function loadAlaSQL() {
    if (window.alasql) return Promise.resolve(window.alasql);
    if (_p) return _p;
    _p = new Promise(function (resolve) {
      var s = document.createElement("script");
      s.src = "https://cdn.jsdelivr.net/npm/alasql@4/dist/alasql.min.js";
      s.onload  = function () { resolve(window.alasql || null); };
      s.onerror = function () { resolve(null); };
      document.head.appendChild(s);
    });
    return _p;
  }

  /* AlaSQL is loaded once per page. After that, waiting on a promise buys
     nothing and costs determinism: a feature's steps all run in one tick,
     so a check that asks a query to run and then reads its result would
     read the PREVIOUS answer. Synchronous when the engine is already
     here, promised only the first time. */
  function withAlaSQL(cb) {
    if (window.alasql) { cb(window.alasql); return; }
    loadAlaSQL().then(cb);
  }

  function upgradeQuery(el) {
    if (el.dataset.lcQueryDone) return;
    el.dataset.lcQueryDone = "1";
    var seed  = (el.querySelector("code") || el).textContent.trim();
    var outId = el.id || el.getAttribute("id") || "query";
    var binds = (el.getAttribute("source") || el.getAttribute("bind") || "").split(",")
      .map(function (s) { return s.trim(); }).filter(Boolean);
    var editable = el.getAttribute("editable") === "true";

    var chip = document.createElement("span");
    chip.className = "lc-query";
    chip.setAttribute("data-lc-id", outId);
    if (binds.length) chip.setAttribute("data-bind", binds.join(","));
    chip.setAttribute("data-query", seed);
    chip.setAttribute("data-editable", editable ? "true" : "false");
    chip.title = seed;
    chip.textContent = "🔎 …";

    var ta = null;
    if (editable) {
      /* live SQL editor — edit, ▶ Run, and everything bound downstream moves */
      var wrap = document.createElement("div");
      wrap.className = "lc-query-wrap";
      ta = document.createElement("textarea");
      ta.className = "lc-query-editor";
      ta.spellcheck = false;
      ta.value = seed;
      ta.rows = Math.min(12, Math.max(3, seed.split("\n").length + 1));
      var bar = document.createElement("div");
      bar.className = "lc-query-bar";
      var runBtn = document.createElement("a");
      runBtn.href = "#"; runBtn.className = "button"; runBtn.textContent = "▶ Run";
      runBtn.addEventListener("click", function (e) { e.preventDefault(); run(); });
      bar.appendChild(runBtn); bar.appendChild(chip);
      wrap.appendChild(ta); wrap.appendChild(bar);
      el.parentNode.replaceChild(wrap, el);
    } else {
      el.parentNode.replaceChild(chip, el);
    }

    function currentSql() { return ta ? ta.value : seed; }
    function fail(msg) {
      chip.className = "lc-query err";
      chip.textContent = "🔎 ⚠ " + String(msg).slice(0, 70);
      if (window.lcSetDataset) window.lcSetDataset(outId, []);
    }
    function run() {
      var sql = currentSql();
      chip.setAttribute("data-query", sql);
      /* HALF THE INPUTS IS NO ANSWER. A source that has not been published
         yet used to become an empty table, and the join answered from it:
         "12 dog(s) still invisible" on Module 00 in Canvas (Michel,
         2026-09-16) — every dog, because the campuses list had not arrived
         when the report ran, and the proof repeated that number as if it
         were a fact about the data. Say what is missing instead, publish
         nothing, and let the listener below re-run the moment it lands.
         Missing means never published (undefined); an empty dataset is a
         real answer and still runs. */
      var missing = binds.filter(function (id) { return window.lcDatasets[id] === undefined; });
      if (missing.length) {
        chip.className = "lc-query";
        chip.setAttribute("data-waiting", missing.join(","));
        chip.textContent = "⏳ waiting for " + missing.join(", ");
        return;
      }
      chip.removeAttribute("data-waiting");
      withAlaSQL(function (alasql) {
        if (!alasql) { fail("AlaSQL failed to load"); return; }
        try {
          binds.forEach(function (id) {
            if (!alasql.tables[id]) alasql("CREATE TABLE [" + id + "]");
            alasql.tables[id].data = (window.lcDatasets[id] || []).slice();
          });
          var rows = alasql(sql);
          if (!Array.isArray(rows)) rows = [];
          chip.className = "lc-query";
          chip.textContent = "🔎 " + rows.length + " row" + (rows.length === 1 ? "" : "s");
          if (window.lcSetDataset) window.lcSetDataset(outId, rows);
        } catch (e) { fail(e.message || e); }
      });
    }

    /* THE READER'S OWN MOVE, REHEARSABLE. Typing other SQL in the editor
       and pressing ▶ Run is what a learner does; a page's check can now do
       the same and compare the answers — two ways of saying one question,
       one result (410 module 04: the WHERE rewritten as JOIN … ON, Michel
       2026-09-19). Same path as the button, so nothing can drift. */
    chip._lcRun = function (sql) {
      if (typeof sql === "string") { if (ta) ta.value = sql; else seed = sql; }
      run();
      return chip.getAttribute("data-query") || "";
    };

    /* reactive: re-run (with the current SQL) when any input changes */
    binds.forEach(function (id) {
      window.lcDatasetListeners[id] = window.lcDatasetListeners[id] || [];
      window.lcDatasetListeners[id].push(run);
    });
    run();
  }

  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader(".highlighter-rouge.query, pre.query, p.query", upgradeQuery);
  }
})();
</script>
