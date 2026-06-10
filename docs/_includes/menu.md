{%- comment -%}
Menu — horizontal nav from a markdown list of links ("icon Label"),
activated by IAL: {: .menu } on a <ul> or paragraph of links

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-menu { display: flex; flex-wrap: wrap; align-items: center; gap: 0.3em 1.5em; padding: 0.5em 0; margin: 0.5em 0 1.2em; border-bottom: 1px solid #eee; }
.lc-menu a { display: inline-flex; align-items: center; gap: 0.4em; text-decoration: none; color: #333; font-weight: 500; font-size: 0.96em; padding: 0.2em 0; }
.lc-menu a:hover { color: #0066cc; }
.lc-menu .lc-menu-ic { font-size: 1.1em; line-height: 1; }
</style>

<script>
(function () {
  if (window._lcMenuReady) return;
  window._lcMenuReady = true;

  var escapeHtml = window.lcEscapeHtml;

  function upgradeMenu(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    var links = el.querySelectorAll("a");
    if (!links.length) return;
    var nav = document.createElement("nav");
    nav.className = "lc-menu";
    Array.prototype.forEach.call(links, function(a) {
      var t = (a.textContent || "").trim();
      var sp = t.indexOf(" ");
      var icon = "", label = t;
      if (sp > 0) { icon = t.slice(0, sp); label = t.slice(sp + 1); }
      var na = document.createElement("a");
      na.href = a.getAttribute("href") || "#";
      if (a.getAttribute("target")) na.target = a.getAttribute("target");
      na.innerHTML = (icon ? '<span class="lc-menu-ic">' + escapeHtml(icon) + '</span>' : '')
        + '<span class="lc-menu-lb">' + escapeHtml(label) + '</span>';
      nav.appendChild(na);
    });
    el.parentNode.replaceChild(nav, el);
  }

  /* ── boot ────────────────────────────────────────────────────── */
  /* code_chrome.md (loaded first, via topbar) provides the scan registry. */

  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader("p.menu, ul.menu", upgradeMenu);
  }

})();
</script>
