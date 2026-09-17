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

  Follows a grid, like a detail grid does — master="grid-id" filter="col=col";
  a line can carry more (2026-09-15, the desk's activity chart):
    series="col"  one line per value; with a master, the selected one in
                  blue and the others grey (hover a line for its name)
    bars="col"    a second measure as bars behind the line, its own scale
    marks="col"   rows whose value is set become diamonds — a key point,
                  its text on hover
    hover="col"   extra text on every point's hover

upgradeChartInline owns the first two; upgradeChartBound the third — they
were the duplicate `upgradeChart` pair split across code_chrome.md and
dataset.md (audit A2), now co-located here.

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-chart { margin: 1em 0; position: relative; }
.lc-chart svg { display: block; width: 100%; height: auto; }
.lc-chart-title { font-size: 0.82em; font-weight: 600; color: #374151; margin-bottom: 0.3em; }
/* the hover legend: a browser's own <title> bubble is slow, and on some
   browsers never comes for a transparent hit circle (Michel, 2026-09-17:
   "nothing visible when I hover") — so the chart draws its own */
.lc-chart-tip { position: absolute; pointer-events: none; display: none; z-index: 5;
  background: #111827; color: #fff; font-size: 0.78em; line-height: 1.35; padding: 0.3em 0.55em;
  border-radius: 4px; white-space: pre; max-width: 260px; box-shadow: 0 2px 8px rgba(0,0,0,0.25); }
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
    if (el.getAttribute("source") || el.getAttribute("bind")) return; /* dataset-bound — upgradeChartBound below */
    var code = el.querySelector("code");
    var raw = (code ? code.textContent : el.textContent).trim();
    var lines = raw.split("\n").map(function(l){ return l.trim(); }).filter(Boolean);
    var type = el.getAttribute("type") || "bar";
    var h = parseInt(el.getAttribute("height") || "300", 10);
    var bound = el.getAttribute("master") || el.getAttribute("bound-to");
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
      placeholder.style.cssText = "min-height:" + h + "px;display:flex;align-items:center;justify-content:center;color:#767676;border:2px dashed #e0e0e0;border-radius:8px;font-style:italic;padding:1em;text-align:center";
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
          wrap.setAttribute("data-lc-bars", newData.length);
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
      /* A CANVAS HAS NO RECTS. The bound variant draws SVG, so a proof can
         count its bars; an inline Chart.js chart drew the same bars into a
         canvas and reported ZERO — a page's own check then failed on a chart
         everyone could see (Michel, 2026-08-13, module 06). So the count is
         recorded where the model can read it either way. */
      wrap.setAttribute("data-lc-bars", data.length);
      if (window.lcRegisterCleanup) window.lcRegisterCleanup(wrap, function() { try { ch.destroy(); } catch(e) {} });
    });
  }

  /* ── dataset-bound variant (SVG) ─────────────────────── */
  function upgradeChartBound(el) {
    if (el.dataset.lcChDone) return;
    var bindId = el.getAttribute("source") || el.getAttribute("bind");
    if (!bindId) return; /* inline/master-detail — upgradeChartInline above */
    el.dataset.lcChDone = "1";
    var type  = el.getAttribute("type") || "bar";
    var xCol  = el.getAttribute("x");
    var yCol  = el.getAttribute("y");
    var title = el.getAttribute("title") || "";
    /* empty=: what to say when the bind never resolves. Without it a chart
       whose source names a part that does not exist sits on "⏳ Loading…"
       for ever — which reads as "the page is slow" rather than "this wire is
       broken", and for a lesson about wiring that is exactly backwards
       (Michel, 2026-08-05). Same knob and same grace as the datagrid. */
    var emptyMsg = el.getAttribute("empty") || "";

    var lcId2 = el.getAttribute("id") || "";
    var masterId = el.getAttribute("master") || "", filterExpr = el.getAttribute("filter") || "";
    var fm = filterExpr.match(/^\s*([\w-]+)\s*=\s*([\w-]+)\s*$/);
    var knobs = { series: el.getAttribute("series") || "", bars: el.getAttribute("bars") || "",
                  marks: el.getAttribute("marks") || "", hover: el.getAttribute("hover") || "", focus: null };
    var masterRow = null;
    var wrap = document.createElement("div");
    wrap.className = "lc-chart";
    wrap.setAttribute("data-bind", bindId);
    wrap.setAttribute("data-type", type);
    if (xCol)  wrap.setAttribute("data-x", xCol);
    if (yCol)  wrap.setAttribute("data-y", yCol);
    if (title) wrap.setAttribute("data-title", title);
    if (lcId2) wrap.setAttribute("data-lc-id", lcId2);
    el.parentNode.replaceChild(wrap, el);

    /* the TITLE belongs to the frame, not to the data: an author who wrote
       one is telling the reader what should appear here, and that promise is
       most useful precisely when nothing has appeared yet */
    function paintTitle() {
      if (!title) return;
      var h = document.createElement("div");
      h.className = "lc-chart-title";
      h.textContent = title;
      wrap.appendChild(h);
    }
    function note(text) {
      wrap.innerHTML = "";
      paintTitle();
      var p = document.createElement("p");
      p.style.cssText = "color:var(--lc-ink-mute,#616161);font-size:.85em;padding:.5em 0";
      p.textContent = text;
      wrap.appendChild(p);
    }

    var painted = false;
    function render(data) {
      wrap.innerHTML = "";
      if (!xCol || !yCol) {
        paintTitle();
        var w = document.createElement("p");
        w.style.cssText = "color:var(--lc-ink-mute,#616161);font-size:.85em";
        w.textContent = "⚠ Chart needs bind, x, y";
        wrap.appendChild(w);
        return;
      }
      var rows = (data || []).slice();
      knobs.focus = null;
      if (masterId && fm) {
        /* the master's row narrows the data (filter) — or, with series,
           only picks which line is the blue one */
        if (masterRow) {
          var want = String(masterRow[fm[2]]);
          if (knobs.series) knobs.focus = want;
          else rows = rows.filter(function (r) { return String(r[fm[1]]) === want; });
        } else if (!knobs.series) {
          note(emptyMsg || "Select a row above."); return;
        }
      }
      if (!rows.length) { if (data && data.length === 0 && !painted) return; note(emptyMsg || "Nothing to draw yet."); return; }
      painted = true;
      paintTitle();
      if (type === "line") renderLine(wrap, rows, xCol, yCol, knobs);
      else                 renderBar(wrap, rows, xCol, yCol);
    }

    window.lcDatasetListeners[bindId] = window.lcDatasetListeners[bindId] || [];
    window.lcDatasetListeners[bindId].push(render);
    if (masterId && window.lcMasterDetail)
      window.lcMasterDetail.subscribe(masterId, function (row) { masterRow = row || null; render(window.lcDatasets[bindId] || []); });

    if (window.lcDatasets[bindId]) render(window.lcDatasets[bindId]);
    else {
      note("⏳ Loading…");
      /* a dataset that is merely slow arrives inside the grace; one that will
         never arrive stops pretending to load. Shared knob with the datagrid
         so a test can shorten both. */
      var grace = window.lcDatagridBindGrace;
      if (grace == null) grace = 4000;
      setTimeout(function () {
        if (!painted) note(emptyMsg || "Nothing arrives here yet.");
      }, grace);
    }
  }

  /* tick labels: integers collide when the axis range is narrow
     (e.g. a 4-7 MB heap) — show one decimal once steps drop below 2 */
  function tickLabel(v, span) {
    return span < 8 ? (Math.round(v * 10) / 10).toFixed(1).replace(/\.0$/, "") : String(Math.round(v));
  }

  function chartSVG(el, W, H) {
    var NS = "http://www.w3.org/2000/svg";
    var svg = document.createElementNS(NS, "svg");
    svg.setAttribute("width", W); svg.setAttribute("height", H);
    svg.setAttribute("viewBox", "0 0 " + W + " " + H);
    el.appendChild(svg);
    wireTip(el, svg);
    return { svg: svg, NS: NS };
  }
  /* every shape that carries a <title> shows it in a tip the moment the
     pointer arrives; the <title> itself stays for screen readers */
  function wireTip(el, svg) {
    var tip = el.querySelector(".lc-chart-tip");
    if (!tip) { tip = document.createElement("div"); tip.className = "lc-chart-tip"; el.appendChild(tip); }
    function titled(t) {
      while (t && t !== svg) { var c = t.querySelector && t.querySelector(":scope > title"); if (c) return c.textContent; t = t.parentNode; }
      return "";
    }
    function place(e) {
      var r = el.getBoundingClientRect(), x = e.clientX - r.left + 12, y = e.clientY - r.top + 12;
      if (x + tip.offsetWidth > r.width) x = Math.max(0, e.clientX - r.left - tip.offsetWidth - 12);
      tip.style.left = x + "px"; tip.style.top = y + "px";
    }
    svg.addEventListener("mouseover", function (e) {
      var text = titled(e.target);
      if (!text) { tip.style.display = "none"; return; }
      tip.textContent = text; tip.style.display = "block"; place(e);
    });
    svg.addEventListener("mousemove", function (e) { if (tip.style.display === "block") place(e); });
    svg.addEventListener("mouseleave", function () { tip.style.display = "none"; });
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
      svgEl(svg, NS, "text", { x: pL - 6, y: y + 4, "text-anchor": "end", "font-size": 9, fill: "#9ca3af" }).textContent = tickLabel(v, maxV);
    });

    /* bars */
    data.forEach(function (d, i) {
      var val = +d[yCol] || 0;
      var bH  = (val / maxV) * cH, bX = pL + i * gap + (gap - barW) / 2, bY = pT + cH - bH;
      var bar = svgEl(svg, NS, "rect", { x: bX, y: bY, width: barW, height: Math.max(bH, 1), fill: "#0066cc", rx: 2, opacity: 0.82, "data-value": val });
      svgEl(bar, NS, "title", {}).textContent = d[xCol] + " — " + yCol + ": " + val;
      /* x label */
      svgEl(svg, NS, "text", { x: bX + barW / 2, y: pT + cH + 14, "text-anchor": "middle", "font-size": 9, fill: "#6b7280" })
        .textContent = String(d[xCol]).substring(0, 7);
    });

    /* y-axis label */
    svgEl(svg, NS, "text", { x: 8, y: pT + cH / 2, "text-anchor": "middle", "font-size": 9, fill: "#9ca3af",
      transform: "rotate(-90,8," + (pT + cH / 2) + ")" }).textContent = yCol;
  }

  function renderLine(el, data, xCol, yCol, o) {
    o = o || {};
    var W = Math.max(el.offsetWidth || 0, 300), H = 220;
    var pL = 44, pB = 36, pT = 14, pR = 10;
    var cW = W - pL - pR, cH = H - pT - pB;
    /* one x axis shared by every series: the sorted set of x values */
    var xs = [];
    data.forEach(function (d) { var x = String(d[xCol]); if (xs.indexOf(x) < 0) xs.push(x); });
    xs.sort();
    var xi = {}; xs.forEach(function (x, i) { xi[x] = i; });
    var groups = {};
    data.forEach(function (d) { var g = o.series ? String(d[o.series]) : ""; (groups[g] = groups[g] || []).push(d); });
    var vals = data.map(function (d) { return +d[yCol] || 0; });
    var maxV = Math.max.apply(null, vals), minV = Math.min.apply(null, vals);
    if (o.bars || o.series) minV = Math.min(0, minV);
    if (maxV === minV) { maxV += 1; if (!o.bars && !o.series) minV -= 1; }
    var range = maxV - minV, step = cW / Math.max(xs.length - 1, 1);
    var s = chartSVG(el, W, H), svg = s.svg, NS = s.NS;
    function X(d) { return pL + xi[String(d[xCol])] * step; }
    function Y(v) { return pT + cH - ((v - minV) / range) * cH; }

    /* grid lines */
    [0, 0.25, 0.5, 0.75, 1].forEach(function (f) {
      var v = minV + range * f, y = pT + cH - f * cH;
      svgEl(svg, NS, "line", { x1: pL, y1: y, x2: pL + cW, y2: y, stroke: f === 0 ? "#9ca3af" : "#f3f4f6", "stroke-width": 1 });
      svgEl(svg, NS, "text", { x: pL - 6, y: y + 4, "text-anchor": "end", "font-size": 9, fill: "#9ca3af" }).textContent = tickLabel(v, range);
    });

    /* bars behind the line: a second measure on its own scale, for the
       focused series only */
    if (o.bars) {
      var bmax = Math.max.apply(null, data.map(function (d) { return +d[o.bars] || 0; })) || 1;
      var bw = Math.max(3, Math.min(18, step * 0.5));
      data.forEach(function (d) {
        if (o.series && o.focus != null && String(d[o.series]) !== o.focus) return;
        var v = +d[o.bars] || 0; if (!v) return;
        var h = v / bmax * cH * 0.6;
        var r = svgEl(svg, NS, "rect", { x: X(d) - bw / 2, y: pT + cH - h, width: bw, height: h, fill: "#93c5fd", opacity: 0.6, rx: 2, "data-bar": v });
        svgEl(r, NS, "title", {}).textContent = d[xCol] + " — " + o.bars + ": " + v + (o.hover && d[o.hover] ? "\n" + d[o.hover] : "");
      });
    }

    Object.keys(groups).sort().forEach(function (g) {
      var rows = groups[g].slice().sort(function (a, b) { return String(a[xCol]) < String(b[xCol]) ? -1 : 1; });
      var focused = !o.series || o.focus == null || g === o.focus;
      var color = focused ? "#0066cc" : "#c7d2e0";
      var pts = rows.map(function (d) { return X(d) + "," + Y(+d[yCol] || 0); });
      var pl = svgEl(svg, NS, "polyline", { points: pts.join(" "), stroke: color, fill: "none",
        "stroke-width": focused ? 2 : 1.2, "stroke-linejoin": "round", "data-series": g });
      if (o.series) svgEl(pl, NS, "title", {}).textContent = g;
      if (!focused) return;
      /* dots (hover for the exact value); a key point is a diamond */
      rows.forEach(function (d) {
        var val = +d[yCol] || 0, x = X(d), y = Y(val);
        var mark = o.marks ? String(d[o.marks] || "") : "";
        if (mark) svgEl(svg, NS, "path", { d: "M" + x + "," + (y - 6) + " l6,6 l-6,6 l-6,-6 z", fill: "#b45309", "data-mark": mark });
        else svgEl(svg, NS, "circle", { cx: x, cy: y, r: 3, fill: color });
        var hit = svgEl(svg, NS, "circle", { cx: x, cy: y, r: 9, fill: "transparent", "pointer-events": "all" });
        svgEl(hit, NS, "title", {}).textContent = xCol + " " + d[xCol] + " — " + yCol + ": " + val
          + (mark ? "\n" + mark : "") + (o.hover && d[o.hover] ? "\n" + d[o.hover] : "");
      });
    });

    /* x labels, thinned when dense */
    var lblEvery = Math.max(1, Math.ceil(xs.length / Math.max(2, Math.floor(cW / 40))));
    xs.forEach(function (x, i) {
      if (i % lblEvery === 0 || i === xs.length - 1)
        svgEl(svg, NS, "text", { x: pL + i * step, y: pT + cH + 14, "text-anchor": "middle", "font-size": 9, fill: "#6b7280" })
          .textContent = String(x).substring(0, 10);
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
