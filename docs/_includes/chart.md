{%- comment -%}
Chart — every chart variant, activated from md + IAL.

Inline (Chart.js), data in the code block:
  ```
  month,sales
  Jan,100
  Feb,150
  ```
  {: .chart type="bar" x="month" y="sales" }

Master/detail (Chart.js) — renders the row a bound datagrid publishes:
  [Chart](#)
  {: .chart bound-to="grid-id" type="bar" }

Dataset-bound (SVG) — re-renders on every dataset update:
  [Sales](#)
  {: .chart bind="sales" type="bar" x="month" y="sales" }

upgradeChartInline owns the first two; upgradeChartBound the third — they
were the duplicate `upgradeChart` pair split across code_chrome.md and
dataset.md (audit A2), now co-located here.

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-chart { margin: 1em 0; position: relative; }
.lc-chart svg { display: block; width: 100%; height: auto; }
.lc-chart-title { font-size: 0.82em; font-weight: 600; color: #374151; margin-bottom: 0.3em; }
</style>

<script>
(function () {
  if (window._lcChartReady) return;
  window._lcChartReady = true;

  /* ── Chart.js loader ─────────────────────────────────── */
  var _chartJsQ = null;
  function loadChartJs(cb) {
    if (window.Chart) { cb(); return; }
    if (_chartJsQ) { _chartJsQ.push(cb); return; }
    _chartJsQ = [cb];
    var s = document.createElement("script");
    s.src = "https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js";
    s.onload = function() { var q = _chartJsQ; _chartJsQ = null; q.forEach(function(f){ f(); }); };
    document.head.appendChild(s);
  }

  /* ── inline + master/detail variants (Chart.js) ──────── */
  function upgradeChartInline(el) {
    if (el.getAttribute("bind")) return; /* dataset-bound — upgradeChartBound below */
    var code = el.querySelector("code");
    var raw = (code ? code.textContent : el.textContent).trim();
    var lines = raw.split("\n").map(function(l){ return l.trim(); }).filter(Boolean);
    var type = el.getAttribute("type") || "bar";
    var h = parseInt(el.getAttribute("height") || "300", 10);
    var bound = el.getAttribute("bound-to");
    var gid = "lc-chart-" + Math.random().toString(36).slice(2, 7);
    var wrap = document.createElement("div");
    wrap.className = "lc-chart";
    /* carry the declared knobs + associations so the x-ray lens (which
       reads data-* off the upgraded element) sees what the IAL declared */
    wrap.setAttribute("data-type", type);
    if (el.getAttribute("x")) wrap.setAttribute("data-x", el.getAttribute("x"));
    if (el.getAttribute("y")) wrap.setAttribute("data-y", el.getAttribute("y"));
    if (bound) wrap.setAttribute("data-bound-to", bound);
    if (el.id) wrap.setAttribute("data-lc-id", el.id);
    el.parentNode.replaceChild(wrap, el);

    function chartColors(data) {
      var mn = Math.min.apply(null, data), mx = Math.max.apply(null, data), rng = mx - mn || 1;
      return data.map(function(v) {
        var t = (v - mn) / rng;
        return "rgb(" + Math.round(173 - 173*t) + "," + Math.round(216 - 160*t) + "," + Math.round(230 - 91*t) + ")";
      });
    }

    if (bound) {
      var xAttr = el.getAttribute("x") || (lines.length > 0 ? lines[0].split(",")[0].trim() : "");
      var placeholder = document.createElement("div");
      placeholder.style.cssText = "min-height:" + h + "px;display:flex;align-items:center;justify-content:center;color:#aaa;border:2px dashed #e0e0e0;border-radius:8px;font-style:italic;padding:1em;text-align:center";
      placeholder.textContent = "Select a row to visualize";
      wrap.appendChild(placeholder);
      loadChartJs(function() {
        var instance = null;
        if (window.lcRegisterCleanup) window.lcRegisterCleanup(wrap, function() { if (instance) { try { instance.destroy(); } catch(e) {} instance = null; } });
        window.lcMasterDetail.subscribe(bound, function(row) {
          if (!row) return;
          var title = String(row[xAttr] || "");
          var newLabels = [], newData = [];
          Object.keys(row).forEach(function(k) {
            if (k === xAttr) return;
            var v = parseFloat(row[k]);
            if (!isNaN(v)) { newLabels.push(k); newData.push(v); }
          });
          if (!newLabels.length) return;
          var colors = chartColors(newData);
          if (!instance) {
            placeholder.style.display = "none";
            var canvas = document.createElement("canvas");
            canvas.id = gid;
            wrap.appendChild(canvas);
            instance = new Chart(canvas, {
              type: type,
              data: { labels: newLabels, datasets: [{ label: title, data: newData, backgroundColor: colors, borderColor: colors, borderWidth: 1 }] },
              options: {
                responsive: true,
                plugins: { legend: { display: false }, title: { display: !!title, text: title } },
                scales: type === "pie" || type === "doughnut" ? {} : { y: { beginAtZero: true } }
              }
            });
          } else {
            instance.data.labels = newLabels;
            instance.data.datasets[0].data = newData;
            instance.data.datasets[0].label = title;
            instance.data.datasets[0].backgroundColor = colors;
            instance.data.datasets[0].borderColor = colors;
            if (instance.options.plugins.title) { instance.options.plugins.title.text = title; instance.options.plugins.title.display = !!title; }
            instance.update();
          }
        });
      });
      return;
    }

    // Static CSV mode
    if (lines.length < 2) return;
    var headers = lines[0].split(",").map(function(v){ return v.trim(); });
    var xAttrS = el.getAttribute("x") || headers[0];
    var yAttr = el.getAttribute("y") || headers[1];
    var xIdx = headers.indexOf(xAttrS); if (xIdx < 0) xIdx = 0;
    var yIdx = headers.indexOf(yAttr); if (yIdx < 0) yIdx = 1;
    var rows = lines.slice(1).map(function(l){ return l.split(",").map(function(v){ return v.trim(); }); });
    var labels = rows.map(function(r){ return r[xIdx] || ""; });
    var data = rows.map(function(r){ return parseFloat(r[yIdx]) || 0; });
    var colors = chartColors(data);
    wrap.innerHTML = "<canvas id=\"" + gid + "\"></canvas>";
    loadChartJs(function() {
      var ch = new Chart(document.getElementById(gid), {
        type: type,
        data: { labels: labels, datasets: [{ label: yAttr, data: data, backgroundColor: colors, borderColor: colors, borderWidth: 1 }] },
        options: {
          responsive: true,
          plugins: { legend: { display: false } },
          scales: type === "pie" || type === "doughnut" ? {} : {
            x: { title: { display: true, text: xAttrS } },
            y: { beginAtZero: true, title: { display: true, text: yAttr } }
          }
        }
      });
      if (window.lcRegisterCleanup) window.lcRegisterCleanup(wrap, function() { try { ch.destroy(); } catch(e) {} });
    });
  }

  /* ── dataset-bound variant (SVG) ─────────────────────── */
  function upgradeChartBound(el) {
    if (el.dataset.lcChDone) return;
    var bindId = el.getAttribute("bind");
    if (!bindId) return; /* inline/master-detail — upgradeChartInline above */
    el.dataset.lcChDone = "1";
    var type  = el.getAttribute("type") || "bar";
    var xCol  = el.getAttribute("x");
    var yCol  = el.getAttribute("y");
    var title = el.getAttribute("title") || "";

    var lcId2 = el.getAttribute("id") || "";
    var wrap = document.createElement("div");
    wrap.className = "lc-chart";
    wrap.setAttribute("data-bind", bindId);
    wrap.setAttribute("data-type", type);
    if (xCol)  wrap.setAttribute("data-x", xCol);
    if (yCol)  wrap.setAttribute("data-y", yCol);
    if (title) wrap.setAttribute("data-title", title);
    if (lcId2) wrap.setAttribute("data-lc-id", lcId2);
    el.parentNode.replaceChild(wrap, el);

    function render(data) {
      wrap.innerHTML = "";
      if (!data || !data.length || !xCol || !yCol) {
        wrap.innerHTML = "<p style='color:#888;font-size:.85em'>⚠ Chart needs bind, x, y</p>"; return;
      }
      if (title) { var h = document.createElement("div"); h.className = "lc-chart-title"; h.textContent = title; wrap.appendChild(h); }
      if (type === "line") renderLine(wrap, data, xCol, yCol);
      else                 renderBar(wrap, data, xCol, yCol);
    }

    window.lcDatasetListeners[bindId] = window.lcDatasetListeners[bindId] || [];
    window.lcDatasetListeners[bindId].push(render);

    if (window.lcDatasets[bindId]) render(window.lcDatasets[bindId]);
    else wrap.innerHTML = "<p style='color:#888;font-size:.85em;padding:.5em 0'>⏳ Loading…</p>";
  }

  function chartSVG(el, W, H) {
    var NS = "http://www.w3.org/2000/svg";
    var svg = document.createElementNS(NS, "svg");
    svg.setAttribute("width", W); svg.setAttribute("height", H);
    svg.setAttribute("viewBox", "0 0 " + W + " " + H);
    el.appendChild(svg);
    return { svg: svg, NS: NS };
  }
  function svgEl(c, NS, tag, attrs) {
    var el = document.createElementNS(NS, tag);
    Object.keys(attrs).forEach(function (k) { el.setAttribute(k, attrs[k]); });
    c.appendChild(el); return el;
  }

  function renderBar(el, data, xCol, yCol) {
    var W = Math.max(el.offsetWidth || 0, 300), H = 220;
    var pL = 44, pB = 36, pT = 14, pR = 10;
    var cW = W - pL - pR, cH = H - pT - pB;
    var vals = data.map(function (d) { return +d[yCol] || 0; });
    var maxV = Math.max.apply(null, vals) || 1;
    var barW = Math.max(4, cW / data.length * 0.6);
    var gap  = cW / data.length;
    var s = chartSVG(el, W, H), svg = s.svg, NS = s.NS;

    /* y-axis ticks */
    [0, 0.25, 0.5, 0.75, 1].forEach(function (f) {
      var v = maxV * f, y = pT + cH - f * cH;
      svgEl(svg, NS, "line", { x1: pL - 4, y1: y, x2: pL + cW, y2: y, stroke: f === 0 ? "#9ca3af" : "#f3f4f6", "stroke-width": 1 });
      svgEl(svg, NS, "text", { x: pL - 6, y: y + 4, "text-anchor": "end", "font-size": 9, fill: "#9ca3af" }).textContent = Math.round(v);
    });

    /* bars */
    data.forEach(function (d, i) {
      var val = +d[yCol] || 0;
      var bH  = (val / maxV) * cH, bX = pL + i * gap + (gap - barW) / 2, bY = pT + cH - bH;
      svgEl(svg, NS, "rect", { x: bX, y: bY, width: barW, height: Math.max(bH, 1), fill: "#0066cc", rx: 2, opacity: 0.82, "data-value": val });
      /* x label */
      svgEl(svg, NS, "text", { x: bX + barW / 2, y: pT + cH + 14, "text-anchor": "middle", "font-size": 9, fill: "#6b7280" })
        .textContent = String(d[xCol]).substring(0, 7);
    });

    /* y-axis label */
    svgEl(svg, NS, "text", { x: 8, y: pT + cH / 2, "text-anchor": "middle", "font-size": 9, fill: "#9ca3af",
      transform: "rotate(-90,8," + (pT + cH / 2) + ")" }).textContent = yCol;
  }

  function renderLine(el, data, xCol, yCol) {
    var W = Math.max(el.offsetWidth || 0, 300), H = 220;
    var pL = 44, pB = 36, pT = 14, pR = 10;
    var cW = W - pL - pR, cH = H - pT - pB;
    var vals = data.map(function (d) { return +d[yCol] || 0; });
    var maxV = Math.max.apply(null, vals) || 1, minV = Math.min.apply(null, vals);
    if (maxV === minV) { maxV += 1; minV -= 1; }
    var range = maxV - minV, step = cW / Math.max(data.length - 1, 1);
    var s = chartSVG(el, W, H), svg = s.svg, NS = s.NS;

    /* grid lines */
    [0, 0.25, 0.5, 0.75, 1].forEach(function (f) {
      var v = minV + range * f, y = pT + cH - f * cH;
      svgEl(svg, NS, "line", { x1: pL, y1: y, x2: pL + cW, y2: y, stroke: f === 0 ? "#9ca3af" : "#f3f4f6", "stroke-width": 1 });
      svgEl(svg, NS, "text", { x: pL - 6, y: y + 4, "text-anchor": "end", "font-size": 9, fill: "#9ca3af" }).textContent = Math.round(v);
    });

    var pts = data.map(function (d, i) {
      var val = +d[yCol] || 0;
      return (pL + i * step) + "," + (pT + cH - ((val - minV) / range) * cH);
    });
    svgEl(svg, NS, "polyline", { points: pts.join(" "), stroke: "#0066cc", fill: "none", "stroke-width": 2, "stroke-linejoin": "round" });

    /* dots + x labels */
    data.forEach(function (d, i) {
      var val = +d[yCol] || 0;
      var x = pL + i * step, y = pT + cH - ((val - minV) / range) * cH;
      svgEl(svg, NS, "circle", { cx: x, cy: y, r: 3, fill: "#0066cc" });
      svgEl(svg, NS, "text", { x: x, y: pT + cH + 14, "text-anchor": "middle", "font-size": 9, fill: "#6b7280" })
        .textContent = String(d[xCol]).substring(0, 7);
    });

    svgEl(svg, NS, "text", { x: 8, y: pT + cH / 2, "text-anchor": "middle", "font-size": 9, fill: "#9ca3af",
      transform: "rotate(-90,8," + (pT + cH / 2) + ")" }).textContent = yCol;
  }

  /* ── boot ────────────────────────────────────────────── */
  /* code_chrome.md (loaded first, via topbar) provides the scan registry.
     Inline registers before bound, preserving the historical scan order. */

  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader(".highlighter-rouge.chart, pre.chart, p.chart", upgradeChartInline);
    window.lcRegisterUpgrader(".chart", upgradeChartBound);
  }

})();
</script>
