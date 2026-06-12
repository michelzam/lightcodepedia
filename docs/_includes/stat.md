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

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-stat {
  display: inline-block; font-size: 0.85em; color: #334155;
  background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 999px;
  padding: 0.15em 0.7em; margin: 0.2em 0;
}
</style>

<script>
(function () {
  if (window._lcStatReady) return;
  window._lcStatReady = true;

  function upgradeStat(el) {
    if (el.dataset.lcStatDone) return;
    el.dataset.lcStatDone = "1";
    var bindId = el.getAttribute("bind") || "";
    var format = el.getAttribute("format") || "{count}";
    var pick   = el.getAttribute("pick") || "last";
    if (!bindId) return;

    var chip = document.createElement("span");
    chip.className = "lc-stat";
    chip.setAttribute("data-bind", bindId);
    if (el.id) chip.setAttribute("data-lc-id", el.id);
    chip.textContent = "…";
    el.parentNode.replaceChild(chip, el);

    function render(data) {
      if (!data || !data.length) { chip.textContent = "—"; return; }
      var row = pick === "first" ? data[0] : data[data.length - 1];
      var out = format.replace(/\{(\w+)\}/g, function (_, k) {
        if (k === "count") return String(data.length);
        var v = row[k];
        return v == null ? "—" : String(v);
      });
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
