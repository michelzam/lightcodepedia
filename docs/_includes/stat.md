{%- comment -%}
Stat — a one-line headline number from a dataset. Renders a small inline
chip and stamps data-acc-summary, so inside an (eager) accordion section
the value also appears in the section title while it is shut.

Usage:
  [stat](#)
  {: .stat bind="fleet_trend" format="✅ {passed}/{scenarios}" }

  bind    dataset id (lcDatasets / lcSetDataset)
  format  template; {col} placeholders come from the picked row,
          {count} is the row count
  pick    which row feeds the template: "last" (default) or "first"
  stale-after="3600"  seconds. CI-published data goes STALE when a run dies
          before its publish step — the board then silently shows yesterday's
          numbers. If this site was built more than N seconds after the row's
          timestamp, the deployed code was never measured: say ⚠️ stale.
  stale-field="run"   which column carries that timestamp (default "run")

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-stat {
  display: inline-block; font-size: 0.85em; color: #334155;
  background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 999px;
  padding: 0.15em 0.7em; margin: 0.2em 0;
}
.lc-stat.lc-stat-bad { border-color: #fecaca; background: #fef2f2; }
/* stale wins the eye over pass/fail: the numbers themselves are not to be trusted */
.lc-stat.lc-stat-stale { border-color: #fcd34d; background: #fffbeb; color: #92400e; }
</style>

<script>
(function () {
  if (window._lcStatReady) return;
  window._lcStatReady = true;

  /* When THIS site was built. CI publishes its results, then the site rebuilds,
     so fresh data is always a few minutes older than the build. A run that dies
     before publishing (an infra 429 on the action download killed one on
     2026-07-24 — the job aborted before any step, so even `if: always()` steps
     never ran) leaves the OLD file in place while the site keeps rebuilding:
     the gap grows, and that gap is the honest staleness signal. No API, no key. */
  var SITE_BUILT = {{ site.time | date_to_xmlschema | jsonify }};

  function upgradeStat(el) {
    if (el.dataset.lcStatDone) return;
    el.dataset.lcStatDone = "1";
    var bindId = el.getAttribute("source") || el.getAttribute("bind") || "";
    var format = el.getAttribute("format") || "{count}";
    var pick   = el.getAttribute("pick") || "last";
    /* requires="col": show nothing meaningful until that column is truthy
       (placeholder/seed rows never reach the title) */
    var requires = el.getAttribute("requires") || "";
    /* ok-when="passed==scenarios": traffic light — ✅ when true, 🔴 when
       false; right side may be another column or a number */
    var okWhen = el.getAttribute("ok-when") || "";
    /* freshness guard — 0 (default) = never check */
    var staleAfter = parseInt(el.getAttribute("stale-after") || "0", 10) || 0;
    var staleField = el.getAttribute("stale-field") || "run";
    if (!bindId) return;

    /* how far this build postdates the data, once past the tolerance */
    function staleness(row) {
      if (!staleAfter) return null;
      var t = Date.parse(String(row[staleField] || "")), built = Date.parse(SITE_BUILT);
      if (isNaN(t) || isNaN(built)) return null;
      var gap = built - t;
      if (gap <= staleAfter * 1000) return null;
      var h = Math.floor(gap / 3600000);
      return h >= 24 ? Math.floor(h / 24) + "d" : (h >= 1 ? h + "h" : Math.round(gap / 60000) + "m");
    }

    function evalOk(row) {
      var m = okWhen.match(/^(\w+)\s*(==|>=|<=|>|<)\s*(\w+)$/);
      if (!m) return null;
      var a = +row[m[1]];
      var b = (m[3] in row) ? +row[m[3]] : +m[3];
      if (isNaN(a) || isNaN(b)) return null;
      switch (m[2]) {
        case "==": return a === b;
        case ">=": return a >= b;
        case "<=": return a <= b;
        case ">":  return a > b;
        default:   return a < b;
      }
    }

    var chip = document.createElement("span");
    chip.className = "lc-stat";
    chip.setAttribute("data-bind", bindId);
    if (el.id) chip.setAttribute("data-lc-id", el.id);
    chip.textContent = "…";
    el.parentNode.replaceChild(chip, el);

    function render(data) {
      if (!data || !data.length) { chip.textContent = "—"; return; }
      var row = pick === "first" ? data[0] : data[data.length - 1];
      if (requires && !row[requires]) {
        chip.style.display = "none";
        chip.removeAttribute("data-acc-summary");
        return;
      }
      chip.style.display = "";
      var out = format.replace(/\{(\w+)\}/g, function (_, k) {
        if (k === "count") return String(data.length);
        var v = row[k];
        return v == null ? "—" : String(v);
      });
      var ok = okWhen ? evalOk(row) : null;
      if (ok !== null) out = (ok ? "✅ " : "🔴 ") + out;
      /* stale beats the traffic light: a green ✅ from data that predates this
         build is the lie we are fixing — lead with the warning, keep the numbers */
      var stale = staleness(row);
      if (stale) {
        out = "⚠️ stale " + stale + " · " + out;
        chip.title = "These results predate this build by " + stale +
          " — the last run never published (check Actions). The numbers describe older code.";
      } else if (chip.title) { chip.removeAttribute("title"); }
      chip.classList.toggle("lc-stat-bad", ok === false && !stale);
      chip.classList.toggle("lc-stat-stale", !!stale);
      chip.textContent = out;
      chip.setAttribute("data-acc-summary", out);
    }

    window.lcDatasetListeners[bindId] = window.lcDatasetListeners[bindId] || [];
    window.lcDatasetListeners[bindId].push(render);
    if (window.lcDatasets && window.lcDatasets[bindId]) render(window.lcDatasets[bindId]);
  }

  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader("p.stat, a.stat, li.stat, div.stat", upgradeStat);
  }
})();
</script>
