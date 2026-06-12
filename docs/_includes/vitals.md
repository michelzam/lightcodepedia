{%- comment -%}
Vitals — live page-health collector. Samples memory, DOM size, upgraded
LC components, transferred bytes, and web vitals (LCP/CLS) on an interval,
and publishes the rows as a standard dataset — display is the ordinary
grid/chart bound to it, so the whole chain shows up in X-ray.

Sampling is opt-in: the card renders with an on/off switch, OFF by
default (no background work); the choice persists in localStorage.
Inside an accordion, the card mirrors its counters into the section
title via data-acc-summary — visible even when the section is shut.

Usage:
  Page vitals collector.
  {: .vitals #page_vitals interval="2" max="120" }

  [Heap over time](#)
  {: .chart bind="page_vitals" type="line" x="t" y="heap_mb" }

  [Samples](#)
  {: .datagrid bind="page_vitals" rows="8" }

Columns: t (s since start), heap_mb (Chrome/Edge only — null elsewhere),
dom_nodes, lc_components (elements matching the component model's wrap
tokens), listeners (dataset subscriptions), transfer_kb, lcp_ms, cls.

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-vitals {
  display: flex; align-items: center; gap: 0.6em; flex-wrap: wrap;
  border: 1px solid #e2e8f0; border-radius: 8px;
  padding: 0.55em 0.9em; margin: 0.6em 0;
  font-size: 0.85em; color: #334155; background: #f8fafc;
}
.lc-vitals .lc-vitals-dot {
  width: 9px; height: 9px; border-radius: 50%;
  background: #94a3b8;
}
.lc-vitals.on .lc-vitals-dot {
  background: #22c55e; animation: lc-vitals-pulse 2s ease-in-out infinite;
}
@keyframes lc-vitals-pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }
.lc-vitals b { color: #0f172a; }
/* on/off switch */
.lc-vitals-switch {
  width: 34px; height: 18px; border-radius: 9px; border: none;
  background: #cbd5e1; cursor: pointer; position: relative; flex: none;
  transition: background 0.2s;
}
.lc-vitals-switch::after {
  content: ""; position: absolute; top: 2px; left: 2px;
  width: 14px; height: 14px; border-radius: 50%; background: #fff;
  transition: left 0.2s;
}
.lc-vitals.on .lc-vitals-switch { background: #22c55e; }
.lc-vitals.on .lc-vitals-switch::after { left: 18px; }
</style>

<script>
(function () {
  if (window._lcVitalsReady) return;
  window._lcVitalsReady = true;

  var MODEL_URL = "{{ "/assets/component-model.json" | relative_url }}?v={{ site.time | date: '%s' }}";
  var wrapTokens = null;
  function loadTokens() {
    if (wrapTokens) return;
    wrapTokens = [];
    fetch(MODEL_URL)
      .then(function (r) { return r.json(); })
      .then(function (d) { wrapTokens = (d.wrap || []).map(function (w) { return w[0]; }); })
      .catch(function () {});
  }

  /* web vitals: buffered observers report even when sampling starts late */
  var lcp = null, cls = 0, obsStarted = false;
  function startObservers() {
    if (obsStarted) return;
    obsStarted = true;
    try {
      new PerformanceObserver(function (l) {
        var es = l.getEntries();
        if (es.length) lcp = Math.round(es[es.length - 1].startTime);
      }).observe({ type: "largest-contentful-paint", buffered: true });
    } catch (e) {}
    try {
      new PerformanceObserver(function (l) {
        l.getEntries().forEach(function (e) {
          if (!e.hadRecentInput) cls += e.value;
        });
      }).observe({ type: "layout-shift", buffered: true });
    } catch (e) {}
  }

  function sample(t0) {
    var mem = performance.memory;  /* Chrome/Edge only */
    var transfer = 0;
    try {
      performance.getEntriesByType("resource").concat(
        performance.getEntriesByType("navigation")
      ).forEach(function (e) { transfer += e.transferSize || 0; });
    } catch (e) {}
    var comps = 0;
    (wrapTokens || []).forEach(function (tk) {
      comps += document.getElementsByClassName(tk).length;
    });
    var listeners = 0;
    var reg = window.lcDatasetListeners || {};
    Object.keys(reg).forEach(function (k) { listeners += (reg[k] || []).length; });
    return {
      t: Math.round((Date.now() - t0) / 100) / 10,
      heap_mb: mem ? Math.round(mem.usedJSHeapSize / 104857.6) / 10 : null,
      dom_nodes: document.getElementsByTagName("*").length,
      lc_components: comps,
      listeners: listeners,
      transfer_kb: Math.round(transfer / 1024),
      lcp_ms: lcp,
      cls: Math.round(cls * 1000) / 1000
    };
  }

  function upgradeVitals(el) {
    if (el.dataset.lcVitalsDone) return;
    el.dataset.lcVitalsDone = "1";
    var id = el.id || "vitals";
    var every = Math.max(0.5, parseFloat(el.getAttribute("interval") || "2"));
    var max = parseInt(el.getAttribute("max") || "120", 10);

    var wrap = document.createElement("div");
    wrap.className = "lc-vitals";
    /* the card IS the publisher of `id` — bind= declarations resolve
       against it even while the switch is off (no data published yet) */
    wrap.setAttribute("data-lc-id", id);
    wrap.innerHTML =
      '<button class="lc-vitals-switch" title="Start/stop sampling" aria-label="vitals on/off"></button>' +
      '<span class="lc-vitals-dot"></span><span class="lc-vitals-text"></span>';
    el.parentNode.replaceChild(wrap, el);
    var text = wrap.querySelector(".lc-vitals-text");

    var t0 = Date.now(), rows = [], timer = null;
    function tick() {
      var row = sample(t0);
      rows.push(row);
      if (rows.length > max) rows.shift();
      if (window.lcSetDataset) window.lcSetDataset(id, rows.slice());
      wrap.setAttribute("data-samples", rows.length);
      wrap.setAttribute("data-heap", row.heap_mb == null ? "" : row.heap_mb);
      wrap.setAttribute("data-dom", row.dom_nodes);
      wrap.setAttribute("data-acc-summary",
        "📊 " + (row.heap_mb == null ? "" : row.heap_mb + " MB · ") +
        row.dom_nodes + " nodes · " + row.lc_components + " comp");
      text.innerHTML =
        "📊 <b>" + (row.heap_mb == null ? "n/a" : row.heap_mb + " MB") + "</b> heap · " +
        "<b>" + row.dom_nodes + "</b> DOM nodes · " +
        "<b>" + row.lc_components + "</b> LC components · " +
        "<b>" + row.transfer_kb + "</b> KB transferred · " +
        "LCP <b>" + (row.lcp_ms == null ? "n/a" : row.lcp_ms + " ms") + "</b> · " +
        "CLS <b>" + row.cls + "</b>" +
        (row.heap_mb == null ? " <span style='color:#94a3b8'>(heap: Chrome/Edge only)</span>" : "");
    }
    function start() {
      if (timer) return;
      wrap.classList.add("on");
      loadTokens();
      startObservers();
      t0 = Date.now();
      tick();
      timer = setInterval(tick, every * 1000);
    }
    function stop() {
      clearInterval(timer); timer = null;
      wrap.classList.remove("on");
      text.textContent = "📊 vitals off — flip the switch to sample";
      wrap.setAttribute("data-acc-summary", "📊 off");
    }
    wrap.querySelector(".lc-vitals-switch").addEventListener("click", function () {
      var on = !timer;
      try { localStorage.setItem("lc_vitals_on", on ? "1" : ""); } catch (e) {}
      on ? start() : stop();
    });

    var remembered = "";
    try { remembered = localStorage.getItem("lc_vitals_on") || ""; } catch (e) {}
    remembered === "1" ? start() : stop();

    if (window.lcRegisterCleanup) {
      window.lcRegisterCleanup(wrap, function () { clearInterval(timer); });
    }
  }

  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader("p.vitals, div.vitals, li.vitals", upgradeVitals);
  }
})();
</script>
