{%- comment -%}
Live Graphviz DOT rendering — powered by @hpcc-js/wasm-graphviz (WASM).

The Jekyll/kramdown pipeline emits ```dot fenced blocks as:
  <div class="language-dot highlighter-rouge"><div class="highlight"><pre><code>…</code></pre></div></div>

This include finds those blocks, runs them through the WASM graphviz engine,
and replaces them with inline SVG (no copy-paste, no external server).

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<script type="module">
  // Normalise all DOT fenced blocks to {src, container} pairs.
  const blocks = [];

  // Rouge: div.language-dot > div.highlight > pre > code
  document.querySelectorAll("div.language-dot").forEach(function (wrap) {
    var code = wrap.querySelector("code");
    if (code) blocks.push({ src: code.textContent, el: wrap });
  });

  // GFM / fallback: pre > code.language-dot
  document.querySelectorAll("pre > code.language-dot").forEach(function (code) {
    blocks.push({ src: code.textContent, el: code.closest("pre") });
  });

  if (blocks.length) {
    var _err = function (el, msg) {
      var pre = document.createElement("pre");
      pre.style.cssText = "color:red;font-size:0.8em";
      pre.textContent = "[graphviz] " + msg;
      el.parentNode.replaceChild(pre, el);
    };
    try {
      var mod = await import("https://cdn.jsdelivr.net/npm/@viz-js/viz@3/dist/viz.js");
      var viz = await (mod.instance || mod.default.instance || mod.default)();
      blocks.forEach(function ({ src, el }) {
        try {
          var svg = viz.renderString(src);
          var div = document.createElement("div");
          div.className = "lc-dot-diagram";
          div.style.cssText = "overflow:auto;line-height:1";
          div.innerHTML = svg;
          el.parentNode.replaceChild(div, el);
        } catch (e) { _err(el, e); }
      });
    } catch (e) {
      console.error("[graphviz] init", e);
      blocks.forEach(function ({ src, el }) { _err(el, "renderer failed to load: " + e); });
    }
  }
</script>
