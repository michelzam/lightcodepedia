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
  features="true"  ALSO require the PROOFS: every .feature on each page above
                 must be green in this learner's own record, not just the
                 points earned. DEFAULT off — quizzes alone, as before. A
                 page whose proofs were never run counts as not done, so
                 nobody builds on a lesson they only read (Michel,
                 2026-08-13: "a more strict way to validate a page and a
                 module, and avoid learners to build on brittle knowledge").
                 Where the prerequisite's source is readable — a rendered
                 course page — the count is against what the page DECLARES,
                 so running one proof and skipping three is not passing.

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
  /* ── the proofs, as a gate (features="true") ─────────────────────────
     feature.md keys lc_features as "<page>#<feature>", on the same page key
     scores use — so "did they turn that page green?" is already in the
     browser. What the browser cannot know alone is how many proofs the page
     HAS: a learner who ran one and skipped three looks perfect. Where the
     source is readable we count what the page declares. */
  function featureTally(pageKey) {
    var all = {};
    try { all = JSON.parse(localStorage.getItem("lc_features") || "{}"); } catch (e) {}
    var green = 0, red = 0;
    Object.keys(all).forEach(function (k) {
      if (k.indexOf(pageKey + "#") !== 0) return;
      if ((all[k] || {}).status === "passing") green++; else red++;
    });
    return { green: green, red: red };
  }
  /* how many proofs that page declares — answerable only when we can read it
     (a rendered course page names its repo and path). Cached per session: the
     pages of a module ask about the same neighbour again and again. */
  function declaredFeatures(el, href) {
    var host = el.closest && el.closest("[data-lc-src-repo]");
    if (!host || /^([a-z][a-z0-9+.-]*:|\/|#)/i.test(href)) return Promise.resolve(null);
    var repo = host.getAttribute("data-lc-src-repo") || "";
    var path = host.getAttribute("data-lc-src-path") || "";
    var parts = path.indexOf("/") >= 0 ? path.split("/").slice(0, -1) : [];
    href.split("#")[0].split("?")[0].split("/").forEach(function (seg) {
      if (!seg || seg === ".") return;
      if (seg === "..") parts.pop(); else parts.push(seg);
    });
    var full = parts.join("/");
    var ck = "lc_declfeat:" + repo + "/" + full;
    try { var hit = sessionStorage.getItem(ck); if (hit !== null) return Promise.resolve(+hit); } catch (e) {}
    var pat = ""; try { pat = localStorage.getItem("lc_ed_pat") || ""; } catch (e) {}
    var h = { Accept: "application/vnd.github.v3.raw" };
    if (pat) h.Authorization = "Bearer " + pat;
    return fetch("https://api.github.com/repos/" + repo + "/contents/" + full, { headers: h })
      .then(function (r) { return r.ok ? r.text() : ""; })
      .then(function (t) {
        if (!t) return null;
        var n = (t.match(/\{:[^}]*\.feature\b/g) || []).length;
        try { sessionStorage.setItem(ck, String(n)); } catch (e) {}
        return n;
      }).catch(function () { return null; });
  }
  /* MET = every proof green. Never run is never met: reading is not doing. */
  function featuresMet(el, href) {
    var tally = featureTally(scoreKey(el, href));
    if (tally.red) return Promise.resolve(false);
    return declaredFeatures(el, href).then(function (declared) {
      if (declared === 0) return true;               /* a page with no proofs */
      if (declared == null) return tally.green > 0;  /* unreadable: what we saw */
      return tally.green >= declared;
    });
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
    /* STRICT (features="true") ALSO ASKS THE PROOFS, and that needs one read
       per prerequisite. So the decision is a promise; in the ordinary case it
       is already resolved, and the page paints exactly as before. */
    /* TWO LEVELS. ?strict=1 sets the frame's default — a whole course walked
       the strict way, with no page edited — and features= on the block is the
       local word, which wins either way: features="false" opens one page
       inside a strict frame, features="true" tightens one page outside it. */
    var featAttr = (el.getAttribute("features") || "").trim();
    var strict = featAttr
      ? /^(true|1|yes|on|all)$/i.test(featAttr)
      : !!(window.lcFrame && window.lcFrame.strict);
    var sc = scores();
    var verdicts = links.map(function (l) {
      if (!met(sc[scoreKey(el, l.href)], passPct)) return Promise.resolve(false);
      return strict ? featuresMet(el, l.href) : Promise.resolve(true);
    });
    /* CLOSED WHILE WE ASK. A gate that opens and then shuts has already shown
       what it was meant to withhold, so a strict gate hides the page from the
       first paint and reveals it only once every proof answered. */
    var preLock = null;
    if (strict) {
      preLock = document.createElement("div");
      preLock.className = "lc-prereq-met";
      preLock.textContent = "⏳ Checking the pages before this one…";
      el.parentNode.insertBefore(preLock, el);
      lockFrom(preLock, true);
    }
    Promise.all(verdicts).then(function (oks) {
      if (preLock) { unlockFrom(preLock); preLock.remove(); }
      paint(oks);
    });
    return;

    function paint(oks) {
    var missing = [];
    var items = links.map(function (l, i) {
      var ok = oks[i];
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
    }   /* paint */
  }

  /* the same hide-by-document-order the gate uses, borrowed for the moment a
     strict gate is still asking */
  function lockFrom(anchor) {
    var root = (anchor.closest && (anchor.closest(".lc-run") || anchor.closest("main"))) || document.body;
    var node = anchor;
    while (node && node !== root && node.parentNode) {
      var n = node.nextElementSibling;
      while (n) { n.classList.add("lc-prereq-hidden"); n = n.nextElementSibling; }
      node = node.parentNode;
    }
  }
  function unlockFrom(anchor) {
    var root = (anchor.closest && (anchor.closest(".lc-run") || anchor.closest("main"))) || document.body;
    root.querySelectorAll(".lc-prereq-hidden").forEach(function (h) {
      h.classList.remove("lc-prereq-hidden");
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
