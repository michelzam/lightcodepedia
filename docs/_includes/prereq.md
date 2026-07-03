{%- comment -%}
Learning-path widgets.

{: .prerequisite }  on a list of links (or a fence containing links): checks
the learner's recorded score (localStorage lc_scores, shared with score.md)
for each linked page. All met → a slim "prerequisites met" line. Any missing →
a gate card that sends the learner there and hides the rest of the page
(with a "show anyway" escape). Knob: pass="80" requires that percentage of a
page's points; default = any recorded point on that page.

Unlocks: every page automatically recommends, at its end, the pages that list
IT as a prerequisite — built at Jekyll time by scanning site pages, so the
learner is self-directed in both directions.
{%- endcomment -%}

<style>
.lc-prereq { margin: 1em 0; border: 1px solid #f0c97a; border-radius: 10px; background: #fffdf5; padding: 12px 16px; }
.lc-prereq h4 { margin: 0 0 6px; font-size: 0.95em; color: #b45309; }
.lc-prereq ul { margin: 0; padding-left: 1.2em; }
.lc-prereq li { margin: 3px 0; }
.lc-prereq .ok { color: #2e7d32; }
.lc-prereq .todo a { color: #0066cc; font-weight: 600; }
.lc-prereq-note { font-size: 0.85em; color: #92600a; margin-top: 8px; }
.lc-prereq-note a { color: #92600a; text-decoration: underline; cursor: pointer; }
.lc-prereq-met { margin: 1em 0; font-size: 0.85em; color: #2e7d32; }
.lc-prereq-hidden { display: none !important; }
.lc-unlocks { margin: 2.5em 0 1em; border-top: 1px solid #e5e7eb; padding-top: 1em; }
.lc-unlocks h4 { margin: 0 0 6px; font-size: 0.95em; color: #334155; }
.lc-unlocks a { display: inline-block; margin: 2px 10px 2px 0; padding: 4px 12px; border: 1px solid #d0e3f5; border-radius: 16px; background: #f5f9ff; color: #0066cc; text-decoration: none; font-size: 0.9em; }
.lc-unlocks a:hover { border-color: #0066cc; }
</style>

{%- capture lc_needle -%}]({{ page.url | remove: '.html' }}){%- endcapture -%}
{%- capture lc_needle2 -%}]({{ page.url }}){%- endcapture -%}
<script type="application/json" id="lc-unlocks-data">[
{%- for p in site.pages -%}
  {%- if p.url != page.url and p.content contains '.prerequisite' -%}
    {%- if p.content contains lc_needle or p.content contains lc_needle2 -%}
      {"url": {{ p.url | remove: '.html' | jsonify }}, "title": {{ p.title | default: p.url | jsonify }}},
    {%- endif -%}
  {%- endif -%}
{%- endfor -%}
null]</script>

<script>
(function () {
  if (window._lcPrereqReady) return;
  window._lcPrereqReady = true;

  function norm(p) {
    try { p = new URL(p, location.origin).pathname; } catch (e) { return null; }
    p = p.replace(/index\.html?$/i, "").replace(/\.html?$/i, "");
    if (p.length > 1) p = p.replace(/\/+$/, "");
    return p || "/";
  }
  function scores() {
    try { return JSON.parse(localStorage.getItem("lc_scores") || "{}"); } catch (e) { return {}; }
  }
  function met(s, passPct) {
    if (!s || !s.total) return false;
    if (passPct) return (s.won / s.total) * 100 >= passPct;
    return s.won > 0;
  }
  function esc(t) {
    return String(t == null ? "" : t).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function upgradePrereq(el) {
    if (el.dataset.lcPrereqDone) return;
    el.dataset.lcPrereqDone = "1";
    var passPct = parseFloat(el.getAttribute("pass") || "") || 0;
    var links = [];
    var anchors = el.querySelectorAll("a[href]");
    if (anchors.length) {
      anchors.forEach(function (a) { links.push({ href: a.getAttribute("href"), title: a.textContent.trim() }); });
    } else {
      var re = /\[([^\]]+)\]\(([^)\s]+)\)/g, m, txt = el.textContent || "";
      while ((m = re.exec(txt))) links.push({ href: m[2], title: m[1] });
    }
    if (!links.length) { el.style.display = "none"; return; }
    var sc = scores(), missing = [];
    var items = links.map(function (l) {
      var ok = met(sc[norm(l.href)], passPct);
      if (!ok) missing.push(l);
      return "<li class='" + (ok ? "ok" : "todo") + "'>" + (ok ? "✅ " + esc(l.title)
        : "➜ <a href='" + esc(l.href) + "'>" + esc(l.title) + "</a>") + "</li>";
    });
    var card = document.createElement("div");
    if (!missing.length) {
      card.className = "lc-prereq-met";
      card.textContent = "✅ prerequisites met — " + links.map(function (l) { return l.title; }).join(" · ");
      el.parentNode.replaceChild(card, el);
      return;
    }
    card.className = "lc-prereq";
    card.innerHTML = "<h4>📋 Before this page</h4><ul>" + items.join("") + "</ul>"
      + "<div class='lc-prereq-note'>Earn points on the pages above and this page unlocks itself. "
      + "<a data-show>Show it anyway →</a></div>";
    el.parentNode.replaceChild(card, el);
    /* hide everything after the gate (the page body), until earned or overridden */
    var hidden = [];
    var n = card.nextElementSibling;
    while (n) { n.classList.add("lc-prereq-hidden"); hidden.push(n); n = n.nextElementSibling; }
    var show = card.querySelector("[data-show]");
    if (show) show.addEventListener("click", function () {
      hidden.forEach(function (h) { h.classList.remove("lc-prereq-hidden"); });
      show.remove();
    });
  }

  function renderUnlocks() {
    var main = document.querySelector("main.markdown-body") || document.querySelector(".markdown-body");
    var data = document.getElementById("lc-unlocks-data");
    if (!main || !data) return;
    var list = [];
    try { list = (JSON.parse(data.textContent) || []).filter(Boolean); } catch (e) {}
    if (!list.length) return;
    var div = document.createElement("div");
    div.className = "lc-unlocks nofragments";
    div.innerHTML = "<h4>🚀 This page unlocks</h4>" + list.map(function (u) {
      return "<a href='" + esc(u.url) + "'>" + esc(u.title) + "</a>";
    }).join("");
    main.appendChild(div);
  }

  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader("ul.prerequisite, ol.prerequisite, p.prerequisite, .highlighter-rouge.prerequisite, pre.prerequisite", upgradePrereq);
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", renderUnlocks);
  } else {
    renderUnlocks();
  }
})();
</script>
