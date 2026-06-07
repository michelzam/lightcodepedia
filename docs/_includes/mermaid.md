{%- comment -%}
Live Mermaid rendering.

The site has no theme that renders ```mermaid fenced blocks, so kramdown/Rouge
emits them as plain <div class="language-mermaid"> code. This include loads
Mermaid (version pinned in _config.yml: site.mermaid.version) and converts those
blocks into rendered diagrams in the browser.

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<script type="module">
  import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@{{ site.mermaid.version | default: '10.9.1' }}/dist/mermaid.esm.min.mjs";

  // Rouge wraps unknown languages as <div class="language-mermaid …"><pre><code>…</code></pre></div>
  // (GFM uses <pre><code class="language-mermaid">). Normalise both to <pre class="mermaid">.
  var containers = new Set();
  document.querySelectorAll("div.language-mermaid, pre > code.language-mermaid").forEach(function (node) {
    var box = node.closest("div.language-mermaid") || node.closest("pre");
    if (box) containers.add(box);
  });

  containers.forEach(function (box) {
    var code = box.querySelector("code") || box;
    var pre = document.createElement("pre");
    pre.className = "mermaid";
    pre.textContent = code.textContent;
    box.parentNode.replaceChild(pre, box);
  });

  mermaid.initialize({ startOnLoad: false, theme: "neutral", securityLevel: "loose" });
  try {
    await mermaid.run({ querySelector: ".mermaid" });
  } catch (e) {
    console.error("[mermaid]", e);
  }
</script>
