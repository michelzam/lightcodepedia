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

  function upgradeQuery(el) {
    if (el.dataset.lcQueryDone) return;
    el.dataset.lcQueryDone = "1";
    var sql   = (el.querySelector("code") || el).textContent.trim();
    var outId = el.id || el.getAttribute("id") || "query";
    var binds = (el.getAttribute("bind") || "").split(",")
      .map(function (s) { return s.trim(); }).filter(Boolean);

    var chip = document.createElement("span");
    chip.className = "lc-query";
    chip.setAttribute("data-lc-id", outId);
    if (binds.length) chip.setAttribute("data-bind", binds.join(","));
    chip.setAttribute("data-query", sql);
    chip.title = sql;
    chip.textContent = "🔎 …";
    el.parentNode.replaceChild(chip, el);

    function fail(msg) {
      chip.className = "lc-query err";
      chip.textContent = "🔎 ⚠ " + String(msg).slice(0, 70);
      if (window.lcSetDataset) window.lcSetDataset(outId, []);
    }
    function run() {
      loadAlaSQL().then(function (alasql) {
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

    /* reactive: re-run when any input dataset changes */
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
