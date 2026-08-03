{%- comment -%}
Live Graphviz DOT rendering — powered by @viz-js/viz (vendored, WASM inlined).

The Jekyll/kramdown pipeline emits ```dot fenced blocks as:
  <div class="language-dot highlighter-rouge"><div class="highlight"><pre><code>…</code></pre></div></div>

This include finds those blocks, runs them through the embedded graphviz engine,
and replaces them with inline SVG.  Plain <script> (no module, no top-level
await) for maximum browser compatibility.

Knob (IAL on the fence): zoom="fit" (default) | a number | "none"
  fit    — scale down to the page width; never blow a small graph up
  1.4    — that multiple of the graph's natural size (scroll if it spills)
  none   — natural size, exactly as graphviz drew it

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
/* Fit by default: a diagram wider than the page shrinks to it, so reading a
   map never starts with a horizontal scroll. A graph SMALLER than the page is
   left alone — blowing it up would only blur the type. */
.lc-dot-diagram { overflow: auto; line-height: 1; margin: 1em 0; }
.lc-dot-diagram svg { max-width: 100%; height: auto; }
/* zoom="<number>" and zoom="none" opt out of the fit and may scroll */
.lc-dot-diagram.lc-dot-zoomed svg { max-width: none; }
</style>

<script>
(function () {
  var VIZ_URL = "{{ "/assets/js/viz-global.js" | relative_url }}";

  // Lazy-load the WASM engine on first use (page diagram or editor tab).
  function ensureViz() {
    return window._lcVizReady || (window._lcVizReady = new Promise(function (resolve, reject) {
      if (window.Viz) { window.Viz.instance().then(resolve).catch(reject); return; }
      var s = document.createElement("script");
      s.src = VIZ_URL;
      s.onload = function () { window.Viz.instance().then(resolve).catch(reject); };
      s.onerror = function () { reject(new Error("failed to load " + VIZ_URL)); };
      document.head.appendChild(s);
    }));
  }
  // Reusable DOT string → SVG string. Used by the page editor's Diagram tab to
  // render a per-page class diagram without needing a .diagram block on the page.
  window.lcDotToSvg = function (src) {
    return ensureViz().then(function (viz) { return viz.renderString(src, { format: "svg" }); });
  };

  // Collect DOT blocks already in the DOM (script is at end of body).
  function findBlock(el) {
    // the two shapes a dot fence arrives in: kramdown's wrapper div, or a
    // bare pre>code from marked (runner renders, embeds, folder previews)
    if (el.matches && el.matches("div.language-dot")) {
      var code = el.querySelector("code");
      return code ? { src: code.textContent, el: el } : null;
    }
    var c = el.querySelector ? el.querySelector("code.language-dot") : null;
    if (c) return { src: c.textContent, el: el };
    return null;
  }

  function upgradeDot(el) {
    if (el.dataset && el.dataset.lcDotDone) return;
    var b = findBlock(el);
    if (!b) return;
    if (el.dataset) el.dataset.lcDotDone = "1";
    var zoom = (el.getAttribute && el.getAttribute("zoom") || "").trim();
    ensureViz().then(function (viz) {
      var div = document.createElement("div");
      div.className = "lc-dot-diagram";
      div.innerHTML = viz.renderString(b.src, { format: "svg" });
      var svg = div.querySelector("svg");
      if (svg && zoom && zoom !== "fit") {
        div.className += " lc-dot-zoomed";
        var n = parseFloat(zoom);
        if (n > 0) {
          /* scale the graph's OWN size — graphviz emits pt; a viewBox is
             always present, so setting width alone keeps the aspect */
          var vb = (svg.getAttribute("viewBox") || "").split(/[\s,]+/);
          var natural = parseFloat(svg.getAttribute("width")) || parseFloat(vb[2]) || 0;
          if (natural) { svg.setAttribute("width", (natural * n) + "pt"); svg.removeAttribute("height"); }
        }
      }
      if (b.el.parentNode) b.el.parentNode.replaceChild(div, b.el);
    }).catch(function (e) { showErr(b.el, "renderer failed: " + e); });
  }

  function showErr(el, msg) {
    var pre = document.createElement("pre");
    pre.style.cssText = "color:red;font-size:0.8em";
    pre.textContent = "[graphviz] " + msg;
    if (el.parentNode) el.parentNode.replaceChild(pre, el);
  }

  /* the scan registry covers the initial page AND every re-scan — which is
     how a dot fence inside a RUNNER render (course pages, benches) finally
     upgrades: the content lands after this script ran, and only the
     registry walks it again. The direct pass below stays for pages where
     the registry is absent. */
  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader("div.language-dot, pre.language-dot, pre:has(> code.language-dot)", upgradeDot);
  }
  document.querySelectorAll("div.language-dot").forEach(upgradeDot);
  document.querySelectorAll("pre > code.language-dot").forEach(function (code) {
    upgradeDot(code.closest("pre"));
  });
})();
</script>
