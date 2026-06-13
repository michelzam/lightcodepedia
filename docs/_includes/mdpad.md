{%- comment -%}
Mdpad — a live Markdown scratchpad: edit on the left, see the rendered
result on the right, updating on every keystroke. Seed it with a fenced
markdown block; the IAL upgrades it in place (P8), and rendering reuses
the shared marked loader from core (P9). No JS in the content (P5).

Usage:
  ````markdown
  ## Hello!
  **Bold** and *italic*, a [link](/), and a list:
  - one
  - two
  ````
  {: .mdpad rows="14" }

IAL knobs:
  rows="14"   editor height in text rows (default 12)
  id="..."    optional — names the pad for X-ray

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-mdpad { display: flex; gap: 0.75em; margin: 1em 0; min-height: 220px; }
.lc-mdpad-in {
  flex: 1; min-width: 0; resize: vertical;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 0.85em; line-height: 1.5; padding: 0.8em;
  border: 1px solid #d0d0d0; border-radius: 6px;
  background: #1e1e2e; color: #cdd6f4;
}
.lc-mdpad-out {
  flex: 1; min-width: 0; padding: 0.8em; overflow: auto;
  border: 1px solid #d0d0d0; border-radius: 6px;
  background: #fafafa; font-size: 0.95em;
}
@media (max-width: 640px) { .lc-mdpad { flex-direction: column; } }
</style>

<script>
(function () {
  if (window._lcMdpadReady) return;
  window._lcMdpadReady = true;

  function upgradeMdpad(el) {
    if (el.dataset.lcMdpadDone) return;
    el.dataset.lcMdpadDone = "1";
    var seed = (el.querySelector("code") || el).textContent.replace(/\n+$/, "");
    var rows = parseInt(el.getAttribute("rows") || "12", 10);
    var id = el.id || "";

    var wrap = document.createElement("div");
    wrap.className = "lc-mdpad";
    if (id) wrap.setAttribute("data-lc-id", id);

    var ta = document.createElement("textarea");
    ta.className = "lc-mdpad-in";
    ta.spellcheck = false;
    ta.rows = rows;
    ta.value = seed;

    var out = document.createElement("div");
    out.className = "lc-mdpad-out";

    wrap.appendChild(ta);
    wrap.appendChild(out);
    el.parentNode.replaceChild(wrap, el);

    function render() {
      out.innerHTML = window.marked
        ? window.marked.parse(ta.value)
        : "<pre>" + ta.value.replace(/[&<]/g, function (c) { return c === "&" ? "&amp;" : "&lt;"; }) + "</pre>";
    }
    ta.addEventListener("input", render);
    render();  /* show the seed immediately (escaped) … */
    if (window.lcLoadMarked) window.lcLoadMarked(render);  /* … then with marked */
  }

  /* code_chrome.md provides the scan registry; one registration covers the
     initial scan and every re-scan. */
  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader(".highlighter-rouge.mdpad, pre.mdpad", upgradeMdpad);
  }
})();
</script>
