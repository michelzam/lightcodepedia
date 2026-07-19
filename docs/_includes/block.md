{%- comment -%}
Block — card sections with optional lazy rendering and help badges.

Renders the ### sections of a code block as bordered cards, activated by
IAL: {: .block } or {: .blocks cols="2" lazy }. A section heading like
"Title [help text]" gets an (i) badge whose tooltip is body-anchored so
overflow:hidden cannot clip it. Lazy blocks render on first open and run
the full upgrade pipeline (lcScanElement) over their content, so nested
components work.

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-blocks { display: grid; gap: 18px; margin: 1em 0; }
.lc-block { border: 1px solid #ddd; border-radius: 8px; padding: 1.5em 2em; background: #fff; overflow: hidden; }
.lc-block > h3:first-child { margin-top: 0; margin-bottom: 0.6em; font-size: 1.1em; color: #222; display: flex; align-items: center; gap: 0.4em; }
.lc-block img { max-width: 100%; border-radius: 4px; display: block; margin: 0.6em auto; }
.lc-block p:last-child, .lc-block ul:last-child { margin-bottom: 0; }
.lc-help {
  display: inline-flex; align-items: center; justify-content: center;
  width: 15px; height: 15px; border-radius: 50%;
  border: 1.4px solid #0a84ff; color: #0a84ff;
  font: italic 700 10px/1 Georgia, "Times New Roman", serif;
  cursor: help; opacity: 0.75; vertical-align: super; user-select: none;
  position: relative; margin-left: 0.2em; flex-shrink: 0;
}
.lc-help:hover, .lc-help:focus { opacity: 1; outline: none; }
/* Tooltip lives on <body> (position:fixed) so the block's overflow:hidden can't clip it. */
.lc-help-tip {
  position: fixed; display: none; z-index: 2147483600;
  max-width: 280px; background: #1e1e2e; color: #eee;
  font: 400 12px/1.45 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  text-align: left; padding: 8px 11px; border-radius: 8px;
  box-shadow: 0 6px 22px rgba(0,0,0,.28); pointer-events: none;
  opacity: 0; transition: opacity .12s;
}
.lc-help-tip.show { opacity: 1; }
.lc-lazy-block { border: 1px solid #ddd; border-radius: 6px; margin: 0.5em 0; overflow: hidden; }
.lc-lazy-block > summary { padding: 0.65em 1em; background: #f5f5f5; cursor: pointer; font-weight: 600; list-style: none; user-select: none; }
.lc-lazy-block > summary::-webkit-details-marker { display: none; }
.lc-lazy-block[open] > summary { background: #e8f0fe; color: #0066cc; border-bottom: 1px solid #ddd; }
.lc-lazy-block .lc-lazy-content { padding: 0.3em 0 0; }
@media (max-width: 600px) { .lc-blocks { grid-template-columns: 1fr !important; } }
</style>

<script>
(function () {
  if (window._lcBlockReady) return;
  window._lcBlockReady = true;

  /* shared helpers from code_chrome.md (parsed earlier — topbar include) */
  var escapeHtml    = window.lcEscapeHtml;
  var loadMarked    = window.lcLoadMarked;
  var parseSections = window.lcParseSections;
  var markdownBody  = window.lcMarkdownBody;

  function _renderAndScanBlock(wrap, sections) {
    wrap.innerHTML = sections.map(function(s) {
      var html = '<div class="lc-block">';
      if (s.label) {
        var helpMatch = s.label.match(/^(.*?)\s*\[([^\]]+)\]\s*$/);
        var title = helpMatch ? helpMatch[1].trim() : s.label;
        var help = helpMatch ? helpMatch[2] : null;
        html += '<h3>' + title;
        if (help) html += ' <span class="lc-help" tabindex="0" role="note" aria-label="' + escapeHtml(help) + '" data-help="' + escapeHtml(help) + '">i</span>';
        html += '</h3>';
      }
      html += markdownBody(s.body);
      return html + '</div>';
    }).join("");
    /* Full subtree pipeline (IAL + every registered upgrader) instead of a
       hand-picked subset — the registry covers components that live in other
       includes (chart, dataset-bound widgets, scene3d…) too. */
    window.lcScanElement(wrap);
  }

  function upgradeBlock(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    var lazy = el.classList.contains("lazy");
    var cols = el.getAttribute("cols") || "1";
    var colStyle = cols === "1" ? "1fr" : "repeat(" + cols + ", 1fr)";
    var sections = parseSections(el);
    if (!sections.length) {
      var code = el.querySelector("code");
      var raw = (code ? code.textContent : el.textContent).trim();
      sections = [{ label: "", body: raw }];
    }

    if (lazy) {
      var titles = sections.filter(function(s){ return s.label; }).map(function(s){
        var m = s.label.match(/^(.*?)\s*\[([^\]]+)\]\s*$/);
        return m ? m[1].trim() : s.label;
      });
      var summaryText = titles.length ? titles.join(" · ") : "Section";
      var details = document.createElement("details");
      details.className = "lc-lazy-block";
      if (el.id) details.setAttribute("data-lc-id", el.id);
      var sumEl = document.createElement("summary");
      sumEl.textContent = summaryText;
      var content = document.createElement("div");
      content.className = "lc-lazy-content";
      details.appendChild(sumEl);
      details.appendChild(content);
      el.parentNode.replaceChild(details, el);
      details.addEventListener("toggle", function() {
        if (!details.open || details.dataset.lcReady) return;
        details.dataset.lcReady = "1";
        var wrap = document.createElement("div");
        wrap.className = "lc-blocks";
        wrap.style.gridTemplateColumns = colStyle;
        content.appendChild(wrap);
        loadMarked(function() { _renderAndScanBlock(wrap, sections); });
      });
      return;
    }

    var wrap = document.createElement("div");
    wrap.className = "lc-blocks";
    wrap.style.gridTemplateColumns = colStyle;
    /* carry the source id so xray finds the pre-upgrade fence snapshot
       (lcSourceOf) and edits the verbatim source, not the rendered text */
    if (el.id) wrap.setAttribute("data-lc-id", el.id);
    el.parentNode.replaceChild(wrap, el);
    loadMarked(function() { _renderAndScanBlock(wrap, sections); });
  }

  // ── Help tooltips (body-anchored, escapes any block's overflow:hidden) ──────
  (function setupHelpTips() {
    var tip = null;
    function ensure() {
      if (tip) return tip;
      tip = document.createElement("div");
      tip.className = "lc-help-tip";
      document.body.appendChild(tip);
      return tip;
    }
    function show(badge) {
      var text = badge.getAttribute("data-help");
      if (!text) return;
      var t = ensure();
      t.textContent = text;
      t.style.display = "block";
      var r = badge.getBoundingClientRect();
      var tw = t.offsetWidth, th = t.offsetHeight, pad = 8;
      var left = r.left + r.width / 2 - tw / 2;
      left = Math.max(pad, Math.min(window.innerWidth - tw - pad, left));
      var top = r.top - th - 8;                 // prefer above the badge…
      if (top < pad) top = r.bottom + 8;        // …flip below if no room
      t.style.left = Math.round(left) + "px";
      t.style.top  = Math.round(top) + "px";
      t.classList.add("show");
    }
    function hide() { if (tip) { tip.classList.remove("show"); tip.style.display = "none"; } }
    function badgeOf(e) { return e.target && e.target.closest ? e.target.closest(".lc-help") : null; }
    document.addEventListener("mouseover", function(e){ var b = badgeOf(e); if (b) show(b); });
    document.addEventListener("mouseout",  function(e){ if (badgeOf(e)) hide(); });
    document.addEventListener("focusin",   function(e){ var b = badgeOf(e); if (b) show(b); });
    document.addEventListener("focusout",  function(e){ if (badgeOf(e)) hide(); });
    document.addEventListener("click",     function(e){ var b = badgeOf(e); if (b) { (tip && tip.classList.contains("show")) ? hide() : show(b); } else hide(); });
    window.addEventListener("scroll", hide, true);
  })();

  /* ── boot ────────────────────────────────────────────── */
  /* code_chrome.md (loaded first, via topbar) provides the scan registry. */

  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader(".highlighter-rouge.block, .highlighter-rouge.blocks, pre.block, pre.blocks", upgradeBlock);
  }

})();
</script>
