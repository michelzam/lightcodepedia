<script>
if (location.search.indexOf('embed=true') >= 0) {
  document.documentElement.classList.add('lc-embed-mode');
}
</script>
<style>
#lc-topbar {
  position: fixed;
  top: 0; left: 0; right: 0;
  height: 48px;
  background: rgba(255,255,255,0.95);
  border-bottom: 1px solid #ddd;
  display: flex;
  align-items: center;
  padding: 0 1.2rem;
  gap: 1.4rem;
  z-index: 1000;
  font-size: 0.9rem;
  backdrop-filter: blur(4px);
}
#lc-topbar .lc-brand {
  font-weight: bold;
  text-decoration: none;
  color: #333;
  margin-right: auto;
}
/* ── user pill ── */
#lc-user-pill { position: relative; flex-shrink: 0; }
#lc-user-btn {
  background: none; border: 1px solid #ddd; border-radius: 50%;
  padding: 2px; cursor: pointer; display: flex; align-items: center; line-height: 1;
}
#lc-user-btn:hover { border-color: #0066cc; box-shadow: 0 0 0 2px #e8f0fe; }
#lc-user-btn img { width: 28px; height: 28px; border-radius: 50%; display: block; }
#lc-user-caret { display: none; }
#lc-user-drop {
  display: none; position: absolute; right: 0; top: calc(100% + 6px);
  background: #fff; border: 1px solid #ddd; border-radius: 10px;
  box-shadow: 0 6px 24px rgba(0,0,0,.12); min-width: 220px; z-index: 2000;
  overflow: hidden;
}
#lc-user-drop.open { display: block; }
.lc-ud-head {
  display: flex; align-items: center; gap: 10px;
  padding: 14px 16px; border-bottom: 1px solid #eee; background: #fafafa;
}
.lc-ud-head img { width: 40px; height: 40px; border-radius: 50%; }
.lc-ud-name { font-weight: 600; font-size: 0.9em; line-height: 1.3; }
.lc-ud-login { font-size: 0.8em; color: #888; }
.lc-ud-karma-row {
  color: #b36a00; background: #fffbf0; justify-content: space-between;
  border-bottom: 1px solid #f0e8d0;
}
.lc-ud-karma-row:hover { background: #fff3d0; }
.lc-ud-karma-pts { font-weight: 700; }
.lc-ud-row {
  display: flex; align-items: center; gap: 8px;
  padding: 9px 16px; font-size: 0.85em; color: #333; text-decoration: none;
  border-bottom: 1px solid #f0f0f0; cursor: pointer;
}
.lc-ud-row:hover { background: #f5f5f5; }
.lc-ud-row:last-child { border-bottom: none; }
.lc-ud-row.danger { color: #c00; }
.lc-ud-legal, .lc-sd-legal { font-size: 0.78em !important; color: #aaa !important;
  border-top: 1px solid #f0f0f0; padding: 7px 16px !important; }
.lc-ud-legal:hover, .lc-sd-legal:hover { color: #888 !important; }
.lc-ud-repo { font-family: monospace; font-size: 0.8em; color: #555; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
/* ── get-started dropdown (logged-out) ── */
#lc-start-pill { position: relative; flex-shrink: 0; display: none; }
#lc-start-btn {
  font-size: 0.82em; color: #0066cc; background: #fff; cursor: pointer;
  border: 1px solid #0066cc; border-radius: 20px; padding: 4px 12px;
}
#lc-start-btn:hover { background: #e8f0fe; }
#lc-start-drop {
  display: none; position: absolute; right: 0; top: calc(100% + 6px);
  background: #fff; border: 1px solid #ddd; border-radius: 10px;
  box-shadow: 0 6px 24px rgba(0,0,0,.12); min-width: 180px; z-index: 2000; overflow: hidden;
}
#lc-start-drop.open { display: block; }
.lc-sd-row {
  display: flex; align-items: center; gap: 8px; padding: 10px 16px;
  font-size: 0.85em; color: #333; text-decoration: none; cursor: pointer;
  border-bottom: 1px solid #f0f0f0;
}
.lc-sd-row:hover { background: #f5f5f5; }
.lc-sd-row:last-child { border-bottom: none; }
@media (max-width: 700px) {
  #lc-user-btn .lc-user-login-label { display: none; }
  #lc-user-caret { display: none; }
}
#lc-topbar .lc-links { display: flex; gap: 1.2rem; }
#lc-topbar .lc-links p { margin: 0; }
#lc-topbar .lc-links a {
  text-decoration: none;
  color: #333;
  margin-right: 1rem;
}
#lc-topbar .lc-links a:hover { color: #0066cc; }
#lc-topbar .lc-link-icon { margin-right: 0.35em; }
@media (max-width: 700px) {
  #lc-topbar { padding: 0 0.7rem; gap: 0.8rem; flex-wrap: nowrap; }
  #lc-topbar .lc-link-label { display: none; }
  #lc-topbar .lc-link-icon { margin-right: 0; font-size: 1.15em; }
  #lc-topbar .lc-links a { margin-right: 0.5rem; }
  /* phones: icons stay in ONE row (menu line breaks otherwise stack them),
     and the fork chip shrinks to its ⑂ glyph — the tooltip keeps the story */
  #lc-topbar .lc-links { gap: 0.6rem; flex-wrap: nowrap; }
  #lc-topbar .lc-links br { display: none; }
  #lc-fork-hint .lc-fork-label { display: none; }
}
body {
  padding-top: 56px;
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
  font-size: 16px;
  line-height: 1.5;
  color: #111;
  -webkit-font-smoothing: antialiased;
}
.markdown-body { max-width: 980px; margin: 0 auto; padding: 1em 1.2rem 2em; }
.markdown-body a { color: #2a7ae2; }
.markdown-body a:visited { color: #1756a9; }
.markdown-body code, .markdown-body pre { font-family: ui-monospace, "SFMono-Regular", Menlo, Consolas, "Liberation Mono", monospace; }
.markdown-body code { background: #eef; padding: 0.1em 0.35em; border-radius: 3px; font-size: 0.9em; }
.markdown-body pre code { background: transparent; padding: 0; }
.markdown-body pre:not([class*="lc-"]) { background: #f8f8f8; padding: 0.8em 1em; border-radius: 6px; overflow-x: auto; }
.markdown-body blockquote { border-left: 4px solid #ddd; padding: 0 1em; color: #555; margin: 1em 0; }
.markdown-body table { border-collapse: collapse; }
.markdown-body table th, .markdown-body table td { border: 1px solid #e0e0e0; padding: 0.4em 0.7em; }
.markdown-body table th { background: #f3f4f6; }
.markdown-body > h1:first-of-type {
  font-size: 1.9em;
  margin: 0.2em 0 0.8em;
  color: #222;
  border-bottom: 2px solid #0066cc;
  padding-bottom: 0.25em;
}
.lc-embed-mode #lc-topbar { display: none !important; }
.lc-embed-mode body { padding-top: 0 !important; }
.lc-embed-mode .markdown-body > h1:first-of-type { display: none !important; }
/* fork awareness — shown only when the site is served from a fork's Pages URL */
#lc-fork-hint {
  display: inline-flex; align-items: center; gap: 4px; margin-left: 10px;
  padding: 2px 10px; border-radius: 999px; font-size: 0.78em; font-weight: 600;
  color: #8a5a00; background: #fff5d6; border: 1px solid #f0d38a;
  text-decoration: none; white-space: nowrap;
}
#lc-fork-hint:hover { background: #ffeab0; }
/* ── bench mode: the student's safe playground gets its own sky ──
   engaged by the runner when it renders a bench (gh: source, not the vault):
   dark bar, the brand becomes the bench itself, links from the bench's own
   menu.md when it has one */
#lc-topbar.lc-bench-mode { background: rgba(241,243,246,0.97); border-bottom-color: #dfe3e9; flex-wrap: nowrap; align-items: baseline; }
#lc-topbar.lc-bench-mode .lc-brand { color: #1f2937; margin-right: 0; margin-left: 0.4em; white-space: nowrap; }
#lc-topbar .lc-bench-home { text-decoration: none; font-size: 1.1em; line-height: 1; align-self: center; }
#lc-topbar .lc-bench-file { font-family: monospace; font-size: 0.82em; color: #4b5563; margin-left: 0.5em; white-space: nowrap; }
#lc-topbar .lc-bench-refresh { margin-left: 0.7em; margin-right: auto; align-self: center; font-size: 0.78em;
  padding: 2px 9px; border-radius: 999px; border: 1px solid #c9d2de; background: #fff; color: #37506e; cursor: pointer; white-space: nowrap; }
#lc-topbar .lc-bench-refresh:hover:not(:disabled) { background: #eef2f7; }
#lc-topbar .lc-bench-refresh:disabled { opacity: 0.6; cursor: default; }
/* bench mode fills more of the left side — the menu goes icon-only well
   before it would wrap into a second (ugly) line; tooltips carry the labels */
@media (max-width: 1100px) {
  #lc-topbar.lc-bench-mode .lc-link-label { display: none; }
  #lc-topbar.lc-bench-mode .lc-link-icon { margin-right: 0; font-size: 1.15em; }
  #lc-topbar.lc-bench-mode .lc-links { gap: 0.6rem; flex-wrap: nowrap; }
  #lc-topbar.lc-bench-mode .lc-links a { margin-right: 0.5rem; }
}
@media (max-width: 480px) { #lc-topbar.lc-bench-mode .lc-bench-file { display: none; } }
</style>
{% comment %} The brand names the node you're on — dynamic, never static text.
   Rule: the repo's name, capitalized — no shortcuts. The emoji marks the
   node kind: 🧪 for the lab (HQ), 💡 everywhere else (pedia + forks). {% endcomment %}
{% assign _repo = site.github.repository_name | default: "lightcodepedia" %}
{% assign _brand = _repo | capitalize %}
{% if _repo == "lightcodelab" %}{% assign _brandmoji = "🧪" %}{% else %}{% assign _brandmoji = "💡" %}{% endif %}
<div id="lc-topbar">
  <a class="lc-brand" href="/">{{ _brandmoji }} {{ _brand }}</a>
  {% comment %} A folder's menu.md becomes the menu for that whole branch, but it
     must opt in with `menu: true` in its front matter — so pages that merely
     happen to be named menu.md (e.g. the .menu component's own doc page) are not
     picked up. Otherwise the site-root menu.md is used. {% endcomment %}
  {% assign _seg = page.path | split: "/" | first %}
  {% assign _fmpath = _seg | append: "/menu.md" %}
  {% assign _fm = site.pages | where: "path", _fmpath | first %}
  {% if _fm.menu %}{% assign _menu = _fm %}{% else %}{% assign _menu = site.pages | where: "path", "menu.md" | first %}{% endif %}
  <div class="lc-links">
    {{ _menu.content | markdownify }}
  </div>
  <div id="lc-start-pill">
    <button id="lc-start-btn">🔑 Get started ▾</button>
    <div id="lc-start-drop">
      <a class="lc-sd-row" href="/start"><span>🚀</span><span>Start here</span></a>
      <div class="lc-sd-row" id="lc-sd-record"><span>🎬</span><span>Record</span></div>
      <a class="lc-sd-row lc-sd-legal" href="/license"><span>⚖️</span><span>License</span></a>
    </div>
  </div>
  <div id="lc-user-pill" style="display:none">
    <button id="lc-user-btn" aria-label="User menu" title="">
      <img id="lc-user-avatar" src="" alt="">
    </button>
    <div id="lc-user-drop">
      <div class="lc-ud-head">
        <img id="lc-ud-avatar" src="" alt="">
        <div>
          <div class="lc-ud-name" id="lc-ud-name"></div>
          <div class="lc-ud-login" id="lc-ud-login"></div>
        </div>
      </div>
      <a class="lc-ud-row" href="/"><span>{{ _brandmoji }}</span><span>{{ _brand }}</span></a>
      <a class="lc-ud-row" id="lc-ud-repo-link" href="#" target="_blank">
        <span>📁</span><span class="lc-ud-repo" id="lc-ud-repo-label"></span>
      </a>
      <a class="lc-ud-row lc-ud-karma-row" id="lc-ud-karma-row" href="/nodes" style="display:none;flex-direction:column;align-items:flex-start;gap:2px">
        <div style="display:flex;justify-content:space-between;width:100%;align-items:center">
          <span>🌟 <span id="lc-ud-karma-pts">…</span> karma pts</span>
          <span style="font-size:0.75em;color:#bbb">network →</span>
        </div>
        <div id="lc-ud-karma-detail" style="font-size:0.75em;color:#c47900;opacity:0.75"></div>
      </a>
      <a class="lc-ud-row" href="/courses/join"><span>🎓</span><span>My course</span></a>
      <a class="lc-ud-row" href="/start"><span>🚀</span><span>Onboarding</span></a>
      <div class="lc-ud-row" id="lc-ud-sync" style="display:none"><span>🔄</span><span id="lc-ud-sync-label">Update from Lightcodepedia</span></div>
      {% if site.github.repository_name == "lightcodelab" %}
      {% comment %} HQ only: educator doors live HERE, behind the avatar —
         connected people only, zero menu pollution for learners. The rows
         are compiled out of pedia and fork builds entirely. {% endcomment %}
      <a class="lc-ud-row" href="/lab/"><span>🎓</span><span>HQ — classroom &amp; material</span></a>
      <div class="lc-ud-row" id="lc-ud-publish"><span>🚀</span><span id="lc-ud-publish-label">Publish to pedia</span></div>
      {% endif %}
      <a class="lc-ud-row" id="lc-ud-pages-link" href="#" target="_blank"><span>🌐</span><span id="lc-ud-pages-label">Your site</span></a>
      <div id="lc-ud-rate" style="display:none;padding:6px 16px;font-size:0.75em;border-bottom:1px solid #f0f0f0"></div>
      <div class="lc-ud-row" id="lc-ud-record"><span>🎬</span><span>Record screen</span></div>
      <div class="lc-ud-row" id="lc-ud-yt-upload"><span>📹</span><span>Upload to YouTube</span></div>
      <div class="lc-ud-row danger" id="lc-ud-disconnect"><span>🔓</span><span>Disconnect</span></div>
      <a class="lc-ud-row lc-ud-legal" href="/license"><span>⚖️</span><span>License</span></a>
    </div>
  </div>
</div>
<script>
/* ── Fork-aware base URL & internal links ───────────────────────────────────
   The canonical site is a custom domain (baseurl ""). A fork is served at
   <owner>.github.io/<repo>/ (baseurl "/<repo>"), so author-written root-relative
   links like "/pages/x" must gain the "/<repo>" segment or they 404 on the
   owner's root. LC_BASE is derived from the LIVE url (robust to a stray CNAME a
   fork inherits) and is "" on the canonical domain — so everything below is a
   pure no-op on the origin; only forks pay any cost or change behaviour. */
(function () {
  var LC_REPO_NAME   = {{ site.github.repository_name | default: "" | jsonify }};
  var LC_CANON_HOST  = {{ site.lc_canonical_host | default: "" | jsonify }};
  var LC_CANON_OWNER = {{ site.lc_canonical_owner | default: "" | jsonify }};

  // base = "/<repo>" only when the current path is actually served under it
  var p = location.pathname, LC_BASE = "";
  if (LC_REPO_NAME && (p === "/" + LC_REPO_NAME || p.indexOf("/" + LC_REPO_NAME + "/") === 0))
    LC_BASE = "/" + LC_REPO_NAME;
  window.lcBaseUrl = LC_BASE;

  // prepend the base to an internal, root-relative path — external links,
  // protocol-relative ("//host"), anchors and already-based paths pass through
  window.lcResolveUrl = function (href) {
    if (!href || typeof href !== "string") return href;
    if (href.charAt(0) !== "/" || href.charAt(1) === "/") return href;
    if (LC_BASE && (href === LC_BASE || href.indexOf(LC_BASE + "/") === 0)) return href;
    return LC_BASE + href;
  };

  function fixAnchor(a) {
    var h = a.getAttribute("href");
    if (!h || h.charAt(0) !== "/" || h.charAt(1) === "/") return;
    if (h === LC_BASE || h.indexOf(LC_BASE + "/") === 0) return;
    a.setAttribute("href", LC_BASE + h);
  }
  window.lcFixLinks = function (root) {
    if (!LC_BASE) return;
    (root || document).querySelectorAll('a[href^="/"]').forEach(fixAnchor);
  };

  if (LC_BASE) {
    var boot = function () {
      window.lcFixLinks(document);
      // widgets (sections, related, sitemap, blocks…) inject links later — fix
      // those too, so navigation stays on the fork everywhere.
      try {
        new MutationObserver(function (muts) {
          for (var i = 0; i < muts.length; i++) {
            var added = muts[i].addedNodes;
            for (var j = 0; j < added.length; j++) {
              var el = added[j];
              if (el.nodeType !== 1) continue;
              if (el.tagName === "A") fixAnchor(el);
              else if (el.querySelectorAll) el.querySelectorAll('a[href^="/"]').forEach(fixAnchor);
            }
          }
        }).observe(document.body, { childList: true, subtree: true });
      } catch (e) {}
    };
    if (document.readyState !== "loading") boot();
    else document.addEventListener("DOMContentLoaded", boot);
  }

  // ── "you're on a fork" hint ───────────────────────────────────────────────
  var hostOwner = /\.github\.io$/i.test(location.hostname)
    ? location.hostname.replace(/\.github\.io$/i, "") : "";
  var onCanonical = LC_CANON_HOST && location.hostname === LC_CANON_HOST;
  var isFork = !onCanonical && hostOwner &&
    (!LC_CANON_OWNER || hostOwner.toLowerCase() !== LC_CANON_OWNER.toLowerCase());
  if (isFork) {
    var addHint = function () {
      var bar = document.getElementById("lc-topbar");
      if (!bar || document.getElementById("lc-fork-hint")) return;
      var chip = document.createElement("a");
      chip.id = "lc-fork-hint";
      chip.href = "https://github.com/" + hostOwner + "/" + (LC_REPO_NAME || "");
      chip.target = "_blank"; chip.rel = "noopener";
      chip.title = "You're viewing " + hostOwner + "'s fork of Lightcodepedia — "
                 + "links stay on this fork, not the original site.";
      var glyph = document.createElement("span"); glyph.textContent = "⑂";
      var lbl = document.createElement("span"); lbl.className = "lc-fork-label";
      lbl.textContent = " " + hostOwner + "’s fork";
      chip.appendChild(glyph); chip.appendChild(lbl);
      var brand = bar.querySelector(".lc-brand");
      if (brand && brand.nextSibling) bar.insertBefore(chip, brand.nextSibling);
      else bar.appendChild(chip);
    };
    if (document.readyState !== "loading") addHint();
    else document.addEventListener("DOMContentLoaded", addHint);
  }
})();
</script>
{% include code_chrome.md %}
<script>
(function(){
  function splitIcons(scope) {
    (scope || document).querySelectorAll('#lc-topbar .lc-links a').forEach(function(a){
      var t = a.textContent.trim();
      var i = t.indexOf(' ');
      if (i > 0) {
        a.innerHTML = '<span class="lc-link-icon">' + t.substring(0, i) + '</span><span class="lc-link-label">' + t.substring(i + 1) + '</span>';
        a.title = t.substring(i + 1);   // icon-only widths keep the label as a tooltip
      }
    });
  }
  splitIcons();

  /* ── Bench mode ──────────────────────────────────────────────────────────
     Called by the runner when it renders a bench (gh: source outside the
     vault). The bar goes dark, the brand becomes 🔬 <bench>/ pointing home
     (the bench README), and if the bench ships a menu.md its links replace
     the site menu — relative hrefs resolve INTO the bench via the runner,
     so students stay in their playground. Same folder-menu convention as
     Jekyll (a menu.md governs its branch), applied at runtime. */
  /* Refresh a bench: merge-upstream syncs a fork with its parent hub. New
     hub files arrive, the student's own files stay; only a file edited on
     BOTH sides conflicts (409) — hence weekly modules are new files. */
  window.lcBenchRefresh = function (repo, btn) {
    var pat = ""; try { pat = localStorage.getItem("lc_ed_pat") || ""; } catch (e) {}
    if (!pat) { alert("Connect your course key first (Get started, top right)."); return; }
    var was = btn ? btn.textContent : ""; if (btn) { btn.disabled = true; btn.textContent = "🔄 Refreshing…"; }
    var H = { Authorization: "Bearer " + pat, Accept: "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28" };
    fetch("https://api.github.com/repos/" + repo, { headers: H, cache: "no-store" })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        return fetch("https://api.github.com/repos/" + repo + "/merge-upstream",
          { method: "POST", headers: H, body: JSON.stringify({ branch: d.default_branch || "main" }) });
      })
      .then(function (r) {
        if (r.ok) { if (btn) btn.textContent = "✅ Up to date"; setTimeout(function () { location.reload(); }, 700); return; }
        if (btn) { btn.disabled = false; btn.textContent = was; }
        if (r.status === 409) alert("⚠️ A file you changed also changed in the course — ask your teacher (a sync conflict). Your work is safe.");
        else r.json().then(function (x) { alert("Couldn't refresh: " + (x.message || ("HTTP " + r.status))); });
      })
      .catch(function () { if (btn) { btn.disabled = false; btn.textContent = was; } alert("Couldn't reach GitHub — try again."); });
  };

  window.lcBenchMode = function (repo, path) {
    var bar = document.getElementById("lc-topbar");
    if (!bar) return;
    var first = bar.dataset.benchMode !== repo;
    bar.dataset.benchMode = repo;
    bar.classList.add("lc-bench-mode");
    var runHome = (window.lcHref ? window.lcHref("/run.html") : "/run.html") + "#src=gh:" + repo + "/";
    var brand = bar.querySelector(".lc-brand");
    var home = bar.querySelector(".lc-bench-home");
    var file = bar.querySelector(".lc-bench-file");
    var runIndex = runHome + "index.md";         // the session root (index.md + .folder)
    if (!home && brand) {                        // 🏠 top-left, always → the root
      home = document.createElement("a"); home.className = "lc-bench-home"; home.textContent = "🏠";
      home.title = "Home — the session root";
      brand.parentNode.insertBefore(home, brand);   // BEFORE the brand → leftmost
      file = document.createElement("span"); file.className = "lc-bench-file";
      brand.parentNode.insertBefore(file, brand.nextSibling);
      /* 🔄 Refresh — pull the latest hub material into this bench
         (merge-upstream keeps the student's own work; new files arrive,
         existing untouched). Placed after the filename, before the menu. */
      var refresh = document.createElement("button");
      refresh.className = "lc-bench-refresh"; refresh.type = "button";
      refresh.textContent = "🔄 Refresh"; refresh.title = "Get the latest course material — keeps your work";
      refresh.addEventListener("click", function () { lcBenchRefresh(repo, refresh); });
      file.parentNode.insertBefore(refresh, file.nextSibling);
    }
    if (home) home.href = runIndex;
    if (brand && first) {
      /* the brand IS the class: <hub>-<login> → "Build Ai Summer26" (drop the
         student's own id, dashes→spaces, title case). It shares the home
         destination — one place, no surprise. */
      var name = repo.split("/")[1], login = "";
      try { login = (JSON.parse(localStorage.getItem("lc_gh_user") || "{}") || {}).login || ""; } catch (e) {}
      var session = login && name.slice(-(login.length + 1)) === "-" + login
        ? name.slice(0, -(login.length + 1)) : name;
      var title = session.split(/[-_]/).map(function (w) {
        return w ? w.charAt(0).toUpperCase() + w.slice(1) : w; }).join(" ");
      brand.textContent = "🔬 " + title;
      brand.href = runIndex;
      brand.title = repo;
    }
    if (file) { file.textContent = path || ""; file.title = repo + "/" + (path || ""); }
    if (!first) return;                       /* menu + brand set up once per repo */
    var links = bar.querySelector(".lc-links");
    var pat = ""; try { pat = localStorage.getItem("lc_ed_pat") || ""; } catch (e) {}
    if (!links) return;
    fetch("https://api.github.com/repos/" + repo + "/contents/menu.md",
          { headers: pat ? { Authorization: "Bearer " + pat, Accept: "application/vnd.github.v3.raw" }
                         : { Accept: "application/vnd.github.v3.raw" }, cache: "no-store" })
      .then(function (r) { if (!r.ok) throw 0; return r.text(); })
      .then(function (md) {
        if (md.indexOf("---") === 0) {          /* strip front matter */
          var e = md.indexOf("\n---", 3);
          if (e >= 0) { var nl = md.indexOf("\n", e + 1); md = nl >= 0 ? md.slice(nl + 1) : ""; }
        }
        if (!window.lcLoadMarked) return;
        window.lcLoadMarked(function () {
          links.innerHTML = marked.parse(md.trim());
          links.querySelectorAll("a").forEach(function (a) {
            var href = a.getAttribute("href") || "";
            if (href && !/^(https?:)?\/\//.test(href) && href.charAt(0) !== "/" && href.charAt(0) !== "#")
              a.href = runHome + href;          /* bench-relative → runner */
            else if (href.charAt(0) === "/" && window.lcHref)
              a.href = window.lcHref(href);     /* site-absolute → healed */
          });
          splitIcons();
        });
      })
      .catch(function () {});                    /* no menu.md → keep site links */
  };

  // ── User pill ──────────────────────────────────────────────────────────────
  // Named + exposed so onboarding can wake it the moment a key is accepted —
  // without this the avatar only appeared on the NEXT page load ("had to
  // onboard twice"). Signed-out runs attach no listeners, so one re-run
  // after connect initializes everything exactly once.
  function lcInitUserPill() {
    var pat  = localStorage.getItem('lc_ed_pat');
    var repo = localStorage.getItem('lc_ed_repo');
    if (!pat) { document.getElementById('lc-start-pill').style.display = 'block'; return; }
    document.getElementById('lc-start-pill').style.display = 'none';

    function showUser(u) {
      var pill = document.getElementById('lc-user-pill');
      pill.style.display = 'block';
      document.getElementById('lc-user-avatar').src = u.avatar_url;
      document.getElementById('lc-user-btn').title = '@' + u.login;
      document.getElementById('lc-ud-avatar').src = u.avatar_url;
      document.getElementById('lc-ud-name').textContent = u.name || u.login;
      document.getElementById('lc-ud-login').textContent = '@' + u.login;

      // karma: show cached value instantly, then verify from GitHub API
      var kRow = document.getElementById('lc-ud-karma-row');
      var kPts = document.getElementById('lc-ud-karma-pts');
      var _kCached = 0;
      if (localStorage.getItem('lc_karma_launch')) _kCached += 15;
      if (localStorage.getItem('lc_karma_bio'))    _kCached += 10;
      var _kForksCached  = parseInt(localStorage.getItem('lc_karma_forks')   || '0', 10);
      var _kStarsCached  = parseInt(localStorage.getItem('lc_karma_stars')   || '0', 10);
      var _kViewsCached  = parseInt(localStorage.getItem('lc_karma_traffic') || '0', 10);
      var _kPagesCached  = parseInt(localStorage.getItem('lc_karma_pages')   || '0', 10);
      var _kQuizCached   = parseInt(localStorage.getItem('lc_karma_quizzes') || '0', 10);
      _kCached += _kForksCached * 50 + _kStarsCached * 10 + _kViewsCached + _kPagesCached * 10 + _kQuizCached * 5;
      if (kPts) kPts.textContent = _kCached || '…';
      if (kRow && _kCached > 0) {
        kRow.style.display = 'flex';
        var _cachedParts = [];
        if (_kForksCached > 0) _cachedParts.push('🍴 ' + _kForksCached + ' forks');
        if (_kStarsCached > 0) _cachedParts.push('⭐ ' + _kStarsCached + ' stars');
        if (_kViewsCached > 0) _cachedParts.push('👥 ' + _kViewsCached + ' visitors');
        if (_kPagesCached > 0) _cachedParts.push('📄 ' + _kPagesCached + ' pages');
        if (_kQuizCached  > 0) _cachedParts.push('🧩 ' + _kQuizCached  + ' quizzes');
        if (localStorage.getItem('lc_karma_bio'))    _cachedParts.push('📝 bio');
        if (localStorage.getItem('lc_karma_launch')) _cachedParts.push('🚀 site');
        var _detCached = document.getElementById('lc-ud-karma-detail');
        if (_detCached) _detCached.textContent = _cachedParts.join('  ·  ');
      }

      // verify karma from GitHub API — skip if verified less than 1 hour ago
      var _ghHdrs = { Authorization: 'Bearer ' + pat, 'X-GitHub-Api-Version': '2022-11-28' };

      // Authoritative, non-consuming rate check — /rate_limit does NOT count
      // against your quota, so it's the reliable source of truth. Runs even when
      // the karma cache is fresh (before the early return below).
      fetch('https://api.github.com/rate_limit', { headers: _ghHdrs })
        .then(function(r){ return r.ok ? r.json() : null; })
        .then(function(d){
          var core = d && d.resources && d.resources.core;
          if (core) {
            localStorage.setItem('lc_rate_remaining', String(core.remaining));
            localStorage.setItem('lc_rate_limit',     String(core.limit));
            showRateLimit(core.remaining, core.limit);
          }
        })
        .catch(function(){});
      /* karma measures your PUBLIC LightNode (login/lightcodepedia) — never
         the node you happen to be browsing. On the lab this integrates the
         pedia numbers; on a student's fork it is their fork by the same rule. */
      var _repoBase = 'https://api.github.com/repos/' + u.login + '/lightcodepedia';
      var _karma = 0;
      var _rc = { forks: 0, stars: 0, visitors: 0, pages: 0, quizzes: 0, bio: false, site: false };

      var _karmaTs = parseInt(localStorage.getItem('lc_karma_ts') || '0', 10);
      var _karmaAge = Date.now() - _karmaTs;  // ms since last full API verification
      if (_karmaAge < 3600000) {
        // cached values are fresh — skip the 5 API calls, just re-render
        _rc.site     = !!localStorage.getItem('lc_karma_launch');
        _rc.bio      = !!localStorage.getItem('lc_karma_bio');
        _rc.forks    = _kForksCached; _rc.stars = _kStarsCached;
        _rc.visitors = _kViewsCached; _rc.pages = _kPagesCached; _rc.quizzes = _kQuizCached;
        _karma = _kCached;
        if (kPts) kPts.textContent = _karma;
        // age label so user can see how stale
        var _ageMin = Math.round(_karmaAge / 60000);
        var _detEl2 = document.getElementById('lc-ud-karma-detail');
        if (_detEl2 && _detEl2.textContent) _detEl2.textContent += '  ·  ⏱ ' + _ageMin + 'm ago';
        if (kRow) kRow.style.display = 'flex';
        // still show rate limit from last known value
        showRateLimit(parseInt(localStorage.getItem('lc_rate_remaining') || '-1', 10));
        return;  // ← skip all API calls
      }

      // helper: reads X-RateLimit-* from a Response and persists it
      function trackRate(r) {
        var rem = parseInt(r.headers.get('X-RateLimit-Remaining') || '-1', 10);
        var lim = parseInt(r.headers.get('X-RateLimit-Limit')     || '-1', 10);
        if (rem >= 0) {
          localStorage.setItem('lc_rate_remaining', String(rem));
          if (lim > 0) localStorage.setItem('lc_rate_limit', String(lim));
          showRateLimit(rem, lim);
        }
        return r;
      }
      function showRateLimit(rem, lim) {
        var el = document.getElementById('lc-ud-rate');
        if (!el || rem < 0) return;
        if (!lim || lim < 0) lim = parseInt(localStorage.getItem('lc_rate_limit') || '5000', 10) || 5000;
        var ratio = rem / lim;
        // battery emoji: full when plenty left, almost-empty when running low
        var batt = ratio < 0.2 ? '🪫' : '🔋';
        el.style.display = 'flex';
        el.textContent = batt + ' ' + rem + ' / ' + lim + ' API calls left this hour';
        el.style.color = ratio < 0.1 ? '#c00' : ratio < 0.25 ? '#c47900' : '#888';
      }

      fetch(_repoBase, { headers: _ghHdrs }).then(trackRate)
        .then(function(r) {
          if (!r.ok) { localStorage.removeItem('lc_karma_launch'); return Promise.reject('no-repo'); }
          return r.json();
        })
        .then(function(repoData) {
          _rc.site = true; _karma += 15;
          localStorage.setItem('lc_karma_launch', '1');
          _rc.forks = repoData.forks_count || 0;
          _rc.stars = repoData.stargazers_count || 0;
          if (_rc.forks > 0) { _karma += _rc.forks * 50; localStorage.setItem('lc_karma_forks', String(_rc.forks)); }
          else localStorage.removeItem('lc_karma_forks');
          if (_rc.stars > 0) { _karma += _rc.stars * 10; localStorage.setItem('lc_karma_stars', String(_rc.stars)); }
          else localStorage.removeItem('lc_karma_stars');
          return fetch(_repoBase + '/contents/docs/_profile.md', { headers: _ghHdrs });
        })
        .then(function(r) {
          if (r && r.ok) { _rc.bio = true; _karma += 10; localStorage.setItem('lc_karma_bio', '1'); }
          else localStorage.removeItem('lc_karma_bio');
          return Promise.all([
            fetch(_repoBase + '/traffic/views', { headers: _ghHdrs }).then(function(r){ return r.ok ? r.json() : null; }).catch(function(){ return null; }),
            fetch(_repoBase + '/contents/docs/pages', { headers: _ghHdrs }).then(function(r){ return r.ok ? r.json() : []; }).catch(function(){ return []; })
          ]);
        })
        .then(function(results) {
          var traffic = results[0];
          var pages   = results[1];
          _rc.visitors = (traffic && traffic.uniques) || 0;
          if (_rc.visitors > 0) { _karma += _rc.visitors; localStorage.setItem('lc_karma_traffic', String(_rc.visitors)); }
          else localStorage.removeItem('lc_karma_traffic');
          _rc.pages = Array.isArray(pages) ? pages.filter(function(f){ return f.type === 'file' && /\.md$/i.test(f.name) && !f.name.startsWith('_') && f.name !== 'index.md'; }).length : 0;
          if (_rc.pages > 0) { _karma += _rc.pages * 10; localStorage.setItem('lc_karma_pages', String(_rc.pages)); }
          else localStorage.removeItem('lc_karma_pages');
          _rc.quizzes = parseInt(localStorage.getItem('lc_karma_quizzes') || '0', 10);
          if (_rc.quizzes > 0) { _karma += _rc.quizzes * 5; }
          localStorage.setItem('lc_karma_ts', String(Date.now()));  // mark fresh
          if (kPts) kPts.textContent = _karma;
          var parts = [];
          if (_rc.forks    > 0) parts.push('🍴 ' + _rc.forks + ' forks');
          if (_rc.stars    > 0) parts.push('⭐ ' + _rc.stars + ' stars');
          if (_rc.visitors > 0) parts.push('👥 ' + _rc.visitors + ' visitors');
          if (_rc.pages    > 0) parts.push('📄 ' + _rc.pages + ' pages');
          if (_rc.quizzes  > 0) parts.push('🧩 ' + _rc.quizzes + ' quizzes');
          if (_rc.bio)          parts.push('📝 bio');
          if (_rc.site)         parts.push('🚀 site');
          var detEl = document.getElementById('lc-ud-karma-detail');
          if (detEl) detEl.textContent = parts.join('  ·  ') + '  ·  ⏱ just now';
          if (kRow) kRow.style.display = 'flex';
        })
        .catch(function(e) {
          if (e === 'no-repo') { if (kRow) kRow.style.display = 'none'; return; }
          if (kPts) kPts.textContent = _karma;
          var detEl = document.getElementById('lc-ud-karma-detail');
          if (detEl && detEl.textContent) detEl.textContent += '  ·  ⚠️ partial';
          if (kRow && _karma > 0) kRow.style.display = 'flex';
        });

      var repoLabel = repo || (u.login + '/lightcodepedia');
      document.getElementById('lc-ud-repo-label').textContent = repoLabel;
      document.getElementById('lc-ud-repo-link').href = 'https://github.com/' + repoLabel;
      var siteHost = u.login + '.github.io';
      var repoSlug = repoLabel.split('/')[1] || 'lightcodepedia';
      document.getElementById('lc-ud-pages-link').href = 'https://' + siteHost + '/' + repoSlug;
      document.getElementById('lc-ud-pages-label').textContent = siteHost + '/' + repoSlug;
    }

    var cached = null;
    try { cached = JSON.parse(localStorage.getItem('lc_gh_user') || 'null'); } catch(e){}
    var cachedFor = localStorage.getItem('lc_gh_user_for');
    if (cached && cachedFor === pat) { showUser(cached); }
    else {
      fetch('https://api.github.com/user', { headers: { Authorization: 'Bearer ' + pat } })
        .then(function(r){ var rem=parseInt(r.headers.get('X-RateLimit-Remaining')||'-1',10); if(rem>=0)localStorage.setItem('lc_rate_remaining',String(rem)); return r.ok ? r.json() : Promise.reject(r.status); })
        .then(function(u){
          localStorage.setItem('lc_gh_user', JSON.stringify(u));
          localStorage.setItem('lc_gh_user_for', pat);
          showUser(u);
        })
        .catch(function(){ document.getElementById('lc-start-pill').style.display = 'block'; });
    }

    /* ── 🔄 fork sync: one tap to receive the mother site's improvements ──
       Uses GitHub's own sync-fork endpoint (merge-upstream) with the PAT the
       editor already holds. Outcomes are honest: clean merge (student edits
       preserved), 409 = conflicting edits → manual merge link, or up to date.
       The row appears only when the connected repo is a fork that is BEHIND
       its parent (checked with a read-only compare when the menu opens). */
    var _syncRow = document.getElementById('lc-ud-sync');
    var _syncLabel = document.getElementById('lc-ud-sync-label');
    var _syncHdrs = { Authorization: 'Bearer ' + pat, 'X-GitHub-Api-Version': '2022-11-28' };
    // ── Publish gate trigger — the row only exists on lab builds ──────────
    var _pubRow = document.getElementById('lc-ud-publish');
    if (_pubRow) {
      var _pubLabel = document.getElementById('lc-ud-publish-label');
      var _pubRepo = {{ site.github.repository_nwo | default: "" | jsonify }};
      var _pubBusy = false;
      _pubRow.addEventListener('click', function () {
        if (_pubBusy || !pat || !_pubRepo) return;
        if (!window.confirm('Publish the lab to pedia now?\n\nThe gate copies docs (minus lab/), packages, tests and workflows; pedia then deploys and runs the full suite.')) return;
        _pubBusy = true;
        _pubLabel.textContent = '🚀 launching…';
        fetch('https://api.github.com/repos/' + _pubRepo + '/actions/workflows/publish.yml/dispatches', {
          method: 'POST',
          headers: { Authorization: 'Bearer ' + pat, Accept: 'application/vnd.github+json', 'Content-Type': 'application/json' },
          body: JSON.stringify({ ref: 'main' })
        }).then(function (r) {
          _pubLabel.textContent = (r.status === 204)
            ? '✔ Publishing — follow 🚀 Deploys on /nodes'
            : (r.status === 403 || r.status === 404)
              ? '❌ PAT lacks Actions read/write on the lab'
              : '❌ Failed (HTTP ' + r.status + ')';
        }).catch(function () {
          _pubLabel.textContent = '❌ network error — try again';
        }).finally(function () {
          setTimeout(function () { _pubLabel.textContent = 'Publish to pedia'; _pubBusy = false; }, 6000);
        });
      });
    }

    var _syncMeta = null, _syncBusy = false, _syncChecked = false;
    function checkSync() {
      if (_syncChecked || !pat || !repo) return;
      _syncChecked = true;
      fetch('https://api.github.com/repos/' + repo, { headers: _syncHdrs })
        .then(function (r) { return r.ok ? r.json() : null; })
        .then(function (meta) {
          if (!meta || !meta.fork || !meta.parent) return;
          var parent = meta.parent.full_name;
          var branch = meta.default_branch || 'main';
          var pbranch = meta.parent.default_branch || 'main';
          _syncMeta = { parent: parent, branch: branch };
          return fetch('https://api.github.com/repos/' + parent + '/compare/' +
              encodeURIComponent(pbranch) + '...' + encodeURIComponent(repo.split('/')[0] + ':' + branch),
              { headers: _syncHdrs })
            .then(function (r) { return r.ok ? r.json() : null; })
            .then(function (cmp) {
              if (!cmp || !cmp.behind_by) return;
              _syncLabel.textContent = 'Update from Lightcodepedia — ' + cmp.behind_by +
                ' new improvement' + (cmp.behind_by > 1 ? 's' : '');
              _syncRow.style.display = '';
            });
        })
        .catch(function () {});
    }
    _syncRow.addEventListener('click', function () {
      if (_syncBusy || !_syncMeta) return;
      _syncBusy = true;
      _syncLabel.textContent = '🔄 updating…';
      fetch('https://api.github.com/repos/' + repo + '/merge-upstream', {
        method: 'POST',
        headers: Object.assign({ 'Content-Type': 'application/json' }, _syncHdrs),
        body: JSON.stringify({ branch: _syncMeta.branch })
      }).then(function (r) {
        if (r.ok) {
          _syncLabel.textContent = '✔ Updated — your site is rebuilding';
          setTimeout(function () { _syncRow.style.display = 'none'; }, 6000);
        } else if (r.status === 409) {
          _syncLabel.innerHTML = '⚠ Your copy has clashing edits — ' +
            '<a href="https://github.com/' + repo + '" target="_blank" rel="noopener" style="color:inherit;text-decoration:underline">merge on GitHub</a>';
        } else {
          _syncLabel.textContent = '⚠ Update failed (HTTP ' + r.status + ') — try again';
          _syncBusy = false;
        }
      }).catch(function () {
        _syncLabel.textContent = '⚠ Network error — try again';
        _syncBusy = false;
      });
    });

    // dropdown toggle
    var btn = document.getElementById('lc-user-btn');
    var drop = document.getElementById('lc-user-drop');
    btn.addEventListener('click', function(e){ e.stopPropagation(); drop.classList.toggle('open'); checkSync(); });
    document.addEventListener('click', function(){ drop.classList.remove('open'); });
    drop.addEventListener('click', function(e){ e.stopPropagation(); });

    // disconnect
    document.getElementById('lc-ud-disconnect').addEventListener('click', function(){
      ['lc_ed_pat','lc_ed_repo','lc_gh_user','lc_gh_user_for'].forEach(function(k){ localStorage.removeItem(k); });
      location.reload();
    });
  }
  window.lcUserPillRefresh = lcInitUserPill;
  lcInitUserPill();

  // ── Recorder launchers (work in every auth state) ──────────────────────────
  function openRec(e) {
    if (e) e.stopPropagation();
    var d = document.getElementById('lc-start-drop'); if (d) d.classList.remove('open');
    var u = document.getElementById('lc-user-drop');  if (u) u.classList.remove('open');
    if (window.lcOpenRecorder) window.lcOpenRecorder();
    else alert('Recorder is still loading — please try again in a moment.');
  }
  ['lc-sd-record','lc-ud-record'].forEach(function(id){
    var el = document.getElementById(id);
    if (el) el.addEventListener('click', openRec);
  });

  var ytBtn = document.getElementById('lc-ud-yt-upload');
  if (ytBtn) ytBtn.addEventListener('click', function(e){
    e.stopPropagation();
    var u = document.getElementById('lc-user-drop'); if (u) u.classList.remove('open');
    if (window.lcOpenYtUpload) window.lcOpenYtUpload();
    else alert('Upload module still loading — try again in a moment.');
  });

  // get-started dropdown toggle (logged-out)
  var sBtn = document.getElementById('lc-start-btn');
  var sDrop = document.getElementById('lc-start-drop');
  if (sBtn && sDrop) {
    sBtn.addEventListener('click', function(e){ e.stopPropagation(); sDrop.classList.toggle('open'); });
    document.addEventListener('click', function(){ sDrop.classList.remove('open'); });
    sDrop.addEventListener('click', function(e){ e.stopPropagation(); });
  }
})();
</script>
