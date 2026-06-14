{%- comment -%}
Live Graphviz DOT rendering — powered by @viz-js/viz (vendored, WASM inlined).

The Jekyll/kramdown pipeline emits ```dot fenced blocks as:
  <div class="language-dot highlighter-rouge"><div class="highlight"><pre><code>…</code></pre></div></div>

This include finds those blocks, runs them through the embedded graphviz engine,
and replaces them with inline SVG.  Plain <script> (no module, no top-level
await) for maximum browser compatibility.

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

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
  var blocks = [];
  document.querySelectorAll("div.language-dot").forEach(function (wrap) {
    var code = wrap.querySelector("code");
    if (code) blocks.push({ src: code.textContent, el: wrap });
  });
  document.querySelectorAll("pre > code.language-dot").forEach(function (code) {
    blocks.push({ src: code.textContent, el: code.closest("pre") });
  });
  if (!blocks.length) return;

  function showErr(el, msg) {
    var pre = document.createElement("pre");
    pre.style.cssText = "color:red;font-size:0.8em";
    pre.textContent = "[graphviz] " + msg;
    el.parentNode.replaceChild(pre, el);
  }

  function render(viz) {
    blocks.forEach(function (b) {
      try {
        var div = document.createElement("div");
        div.className = "lc-dot-diagram";
        div.style.cssText = "overflow:auto;line-height:1";
        div.innerHTML = viz.renderString(b.src, { format: "svg" });
        b.el.parentNode.replaceChild(div, b.el);
      } catch (e) { showErr(b.el, e); }
    });
  }

  ensureViz().then(render).catch(function (e) {
    console.error("[graphviz] init:", e);
    blocks.forEach(function (b) { showErr(b.el, "renderer failed: " + e); });
  });
})();
</script>
