{%- comment -%}
Learning-path widgets.

{: .prerequisite }  on a list of links (or a fence containing links): checks
the learner's recorded score (localStorage lc_scores, shared with score.md)
for each linked page. All met → a slim "Prerequisites met" line. Any missing →
a gate card that sends the learner there and hides the rest of the page
(with a "show anyway" escape). Knob: pass="80" requires that percentage of a
page's points; default = any recorded point on that page.

Unlocks: every page automatically recommends, at its end, the pages that list
IT as a prerequisite — built at Jekyll time by scanning site pages, so the
learner is self-directed in both directions.

Knobs:
  pass="100"     percentage required on each linked page. DEFAULT 100 —
                 mastery, not a lucky point. pass="50" relaxes it.
  escape="true"  offer the "show it anyway" hatch (DEFAULT: none — the
                 author decides whether a gate can be waved away). Any
                 other value becomes the hatch's wording.

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
.lc-prereq-met a { color: inherit; text-decoration: underline; text-underline-offset: 2px; }
.lc-prereq-met a:hover { color: #1b5e20; }
.lc-prereq-sep { color: #9ca3af; }
.lc-prereq li.ok a { color: inherit; text-decoration: underline; text-underline-offset: 2px; }
.lc-prereq-hidden { display: none !important; }
/* (the lock itself is applied in JS — see lockAfter: a locked page has to
   stay locked while components replace their blocks AND while slides
   re-parent the whole body into sections) */
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
  /* Scores are sacred: the key names the CONTENT, not the vehicle. Inside a
     runner render (data-lc-src contract) a relative link means "my sibling
     file in the rendered repo" and must look up the gh: score bucket that
     page actually earns into — never /run. Site pages keep pathname keys. */
  function scoreKey(el, href) {
    var host = el.closest && el.closest("[data-lc-src-repo]");
    if (host && !/^([a-z][a-z0-9+.-]*:|\/|#)/i.test(href)) {
      var path = host.getAttribute("data-lc-src-path") || "";
      var parts = path.indexOf("/") >= 0 ? path.split("/").slice(0, -1) : [];
      href.split("#")[0].split("?")[0].split("/").forEach(function (seg) {
        if (!seg || seg === ".") return;
        if (seg === "..") parts.pop(); else parts.push(seg);
      });
      return ("gh:" + host.getAttribute("data-lc-src-repo") + "/" + parts.join("/"))
        .replace(/\/index\.md$/i, "").replace(/\.md$/i, "");
    }
    /* healed links (/run#src=gh:…) and site links share score.md's canon */
    if (window.lcPageScores) return window.lcPageScores.norm(href);
    return norm(href);
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
    /* Default: MASTERY. "You may pass when you have earned everything on
       the page before" — a prerequisite that opens on a single lucky point
       is not a prerequisite. pass="50" relaxes it deliberately. */
    var passPct = parseFloat(el.getAttribute("pass") || "") || 100;
    /* Default: NO WAY THROUGH. The escape hatch is the author's decision,
       not the platform's — a gate that anyone can wave away teaches that
       gates are decoration. escape="true" offers it with the standard
       wording; any other value IS the wording. */
    var escRaw = (el.getAttribute("escape") || "").trim();
    var escOff = !escRaw || /^(false|0|no|off)$/i.test(escRaw);
    var escLabel = (!escRaw || /^(true|1|yes|on)$/i.test(escRaw))
      ? "Show it anyway →" : escRaw;
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
      var ok = met(sc[scoreKey(el, l.href)], passPct);
      if (!ok) missing.push(l);
      /* A MET PAGE IS STILL A PAGE (Michel, 2026-08-13). Green used to turn
         the title into plain text, so the one list a learner would use to go
         back and re-read something was the one place they could not click. */
      return "<li class='" + (ok ? "ok" : "todo") + "'>" + (ok ? "✅ " : "➜ ")
        + "<a href='" + esc(l.href) + "'>" + esc(l.title) + "</a></li>";
    });
    var card = document.createElement("div");
    if (!missing.length) {
      card.className = "lc-prereq-met";
      card.innerHTML = "✅ Prerequisites met — " + links.map(function (l) {
        return "<a href='" + esc(l.href) + "'>" + esc(l.title) + "</a>";
      }).join(" <span class='lc-prereq-sep'>·</span> ");
      el.parentNode.replaceChild(card, el);
      return;
    }
    card.className = "lc-prereq";
    card.innerHTML = "<h4>📋 Before this page</h4><ul>" + items.join("") + "</ul>"
      + "<div class='lc-prereq-note'>"
      + (passPct >= 100 ? "Finish the pages above — every point — and this page unlocks itself."
                        : "Earn " + passPct + "% on the pages above and this page unlocks itself.")
      + (escOff ? "" : " <a data-show>" + esc(escLabel) + "</a>")
      + "</div>";
    el.parentNode.replaceChild(card, el);
    /* Hide the page body until earned or overridden. Two things fight this:
       components upgrade LATE and REPLACE their block (a csv fence becomes a
       grid), and slides re-parent everything into sections — so neither a
       one-shot walk nor a sibling CSS rule survives. Hide by DOCUMENT ORDER
       at every level up to the render root, and re-apply whenever the tree
       changes. */
    var root = (card.closest && (card.closest(".lc-run") || card.closest("main"))) || document.body;
    var locked = true;
    function lockAfter() {
      if (!locked) return;
      var node = card;
      while (node && node !== root && node.parentNode) {
        var n = node.nextElementSibling;
        while (n) { n.classList.add("lc-prereq-hidden"); n = n.nextElementSibling; }
        node = node.parentNode;
      }
    }
    lockAfter();
    var obs = null;
    if (window.MutationObserver) {
      obs = new MutationObserver(lockAfter);
      obs.observe(root, { childList: true, subtree: true });
    }
    var show = escOff ? null : card.querySelector("[data-show]");
    if (show) show.addEventListener("click", function () {
      locked = false;
      if (obs) obs.disconnect();
      root.querySelectorAll(".lc-prereq-hidden").forEach(function (h) {
        h.classList.remove("lc-prereq-hidden");
      });
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
