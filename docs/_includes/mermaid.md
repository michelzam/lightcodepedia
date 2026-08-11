{%- comment -%}
Live Mermaid rendering.

The site has no theme that renders ```mermaid fenced blocks, so kramdown/Rouge
emits them as plain <div class="language-mermaid"> code. This include loads
Mermaid (version pinned in _config.yml: site.mermaid.version) and converts those
blocks into rendered diagrams in the browser.

TWO ARRIVAL PATHS, one renderer. Jekyll pages carry their fences at load
(the initial pass below). But a COURSE page is rendered by the runner AFTER
load — marked emits <pre><code class="language-mermaid"> into a scanned
region, and the one-shot pass had already come and gone: module 04's data
page showed its diagram as raw text (Michel, 2026-08-11). The upgrader
handles everything the scanner injects later — runner renders, embeds,
bench slots.

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<script type="module">
  const MERMAID_URL = "https://cdn.jsdelivr.net/npm/mermaid@{{ site.mermaid.version | default: '10.9.1' }}/dist/mermaid.esm.min.mjs";
  let _mermaid = null;
  async function ensure() {
    if (!_mermaid) {
      _mermaid = (await import(MERMAID_URL)).default;
      _mermaid.initialize({ startOnLoad: false, theme: "neutral", securityLevel: "loose" });
    }
    return _mermaid;
  }

  // Rouge wraps unknown languages as <div class="language-mermaid …"><pre><code>…</code></pre></div>
  // (marked/GFM uses <pre><code class="language-mermaid">). Normalise both to <pre class="mermaid">.
  function normalise(box) {
    const code = box.querySelector("code") || box;
    const pre = document.createElement("pre");
    pre.className = "mermaid";
    pre.textContent = code.textContent;
    box.parentNode.replaceChild(pre, box);
    return pre;
  }
  async function render(nodes) {
    if (!nodes.length) return;
    try { await (await ensure()).run({ nodes }); }
    catch (e) { console.error("[mermaid]", e); }
  }

  function collect(root) {
    const boxes = new Set();
    root.querySelectorAll("div.language-mermaid, pre > code.language-mermaid").forEach(function (node) {
      const box = node.closest("div.language-mermaid") || node.closest("pre");
      if (box) boxes.add(box);
    });
    return [...boxes].map(normalise);
  }

  // pass 1: fences the build put on the page
  render(collect(document));

  // pass 2+: fences the scanner injects later (runner, embeds, bench slots)
  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader("div.language-mermaid, pre.language-mermaid", function (el) {
      if (el.dataset.lcMermaid) return;
      el.dataset.lcMermaid = "1";
      render([normalise(el)]);
    });
    window.lcRegisterUpgrader("code.language-mermaid", function (el) {
      const box = el.closest("div.language-mermaid") || el.closest("pre");
      if (!box || box.dataset.lcMermaid) return;
      box.dataset.lcMermaid = "1";
      render([normalise(box)]);
    });
  }
</script>
