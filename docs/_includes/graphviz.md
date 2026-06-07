{%- comment -%}
Live Graphviz DOT rendering — powered by @hpcc-js/wasm-graphviz (WASM).

The Jekyll/kramdown pipeline emits ```dot fenced blocks as:
  <div class="language-dot highlighter-rouge"><div class="highlight"><pre><code>…</code></pre></div></div>

This include finds those blocks, runs them through the WASM graphviz engine,
and replaces them with inline SVG (no copy-paste, no external server).

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<script type="module">
  import { Graphviz } from
    "https://cdn.jsdelivr.net/npm/@hpcc-js/wasm-graphviz@1/dist/graphvizBundle.js";

  const gv = await Graphviz.load();

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

  blocks.forEach(function ({ src, el }) {
    try {
      var svg = gv.dot(src);
      var div = document.createElement("div");
      div.className = "lc-dot-diagram";
      div.style.cssText = "overflow:auto;line-height:1";
      div.innerHTML = svg;
      el.parentNode.replaceChild(div, el);
    } catch (e) {
      var pre = document.createElement("pre");
      pre.style.cssText = "color:red;font-size:0.8em";
      pre.textContent = "[graphviz] " + e;
      el.parentNode.replaceChild(pre, el);
    }
  });
</script>
