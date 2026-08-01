{%- comment -%}
Folder — card grid of a docs/ subfolder's pages, with per-page
feature-status dots and a 📅 date tag (front-matter `date:` if present, else the
file's last-commit date). Fetches the folder listing and page front matter
from the repository. Activated by IAL: {: .folder } on a link paragraph.

Knobs:
  cols="auto"       grid columns (default auto-fit) or a fixed number
  sort="name"       initial order: "name" (default, alphabetical) or "recent"
  show-private      include _-prefixed files
  open="runner"     scan a repo path OUTSIDE docs/ (courses/, hubs/…) via the
                    API (author key) and open every card in the runner —
                    the same cards, pointed at unrendered material

One control bar. Sort (Name / 🕒 Recent) only ORDERS. Tag/state chips filter in
both sorts. The 📅 date tags and "Modified: hour/day/week/month" filters belong to
Recent — they appear when you switch to Recent (git dates load lazily then, so Name
stays cheap) and disappear when you go back to Name (initial state). Within Recent,
tag and Modified filters compose (AND). Every chip shares one look; active = blue.

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-card-footer { display: flex; align-items: center; gap: 0.5em; margin-top: 0.65em; flex-wrap: wrap; }
.lc-card-features { display: flex; gap: 0.35em; align-items: center; flex-wrap: wrap; margin-left: auto; }
.lc-card-tags { display: flex; gap: 0.3em; flex-wrap: wrap; }
.lc-card-tag { font-size: 0.7em; font-weight: 600; padding: 0.1em 0.5em; border-radius: 99px; background: #e0f2fe; color: #075985; line-height: 1.6; }
.lc-card-tag[data-tag] { cursor: pointer; }
.lc-card-tag[data-tag]:hover { background: #bae6fd; }
.lc-card-date { font-size: 0.72em; color: #6b7280; margin-top: 0.3em; }
/* ⚙️ workbench affordances — X-ray mode only */
.lc-card:has(> .lc-card-workrow) { display: flex; flex-direction: column; }
.lc-card-workrow { display: flex; align-items: center; justify-content: space-between; gap: 0.5em; margin-top: auto; padding-top: 0.5em; border-top: 1px dashed #e5e7eb; }
.lc-card-fname { font: 500 0.72em ui-monospace, SFMono-Regular, Menlo, monospace; color: #6b7280; background: #f3f4f6; border-radius: 6px; padding: 0.15em 0.5em; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.lc-card-gear { border: 1px solid #d1d5db; background: #fff; border-radius: 8px; padding: 0.1em 0.4em; cursor: pointer; font-size: 0.85em; flex: none; }
.lc-card-gear:hover { border-color: #0066cc; background: #eef4ff; }
.lc-folder-menu { position: absolute; bottom: 34px; right: 6px; z-index: 1000; background: #fff; border: 1px solid #d1d5db; border-radius: 10px; box-shadow: 0 6px 20px rgba(0,0,0,0.15); display: flex; flex-direction: column; min-width: 150px; overflow: hidden; }
.lc-folder-menu button { border: 0; background: none; text-align: left; padding: 0.55em 0.9em; cursor: pointer; font-size: 0.9em; }
.lc-folder-menu button:hover { background: #f3f4f6; }
.lc-folder-move { display: flex; gap: 0.35em; align-items: center; padding: 0.5em; }
.lc-folder-move input { flex: 1; min-width: 180px; border: 1px solid #d1d5db; border-radius: 6px; padding: 0.35em 0.5em; font: 0.85em ui-monospace, SFMono-Regular, Menlo, monospace; }
.lc-folder-move button { border: 1px solid #d1d5db; border-radius: 6px; background: #fff; padding: 0.3em 0.6em; cursor: pointer; font-size: 0.85em; }
/* ── tag filter bar (clickable chips above the grid) ── */
.lc-card-filter { display: flex; align-items: center; flex-wrap: wrap; gap: 0.4em; margin: 0 0 0.9em; }
.lc-card-filter-label { font-size: 0.75em; font-weight: 600; color: #6b7280; margin-right: 0.1em; }
/* every chip (sort, tag, work-state, time) shares ONE look: neutral pill, filled
   blue when active. Meaning is carried by the group label + icons, not by colour. */
.lc-card-filter-chip { font-size: 0.72em; font-weight: 600; padding: 0.2em 0.7em; border-radius: 99px; border: 1px solid #d1d5db; background: #f3f4f6; color: #374151; cursor: pointer; line-height: 1.6; }
.lc-card-filter-chip:hover { background: #e5e7eb; }
.lc-card-filter-on { background: #0369a1; color: #fff; border-color: #0369a1; }
.lc-card-filter-on:hover { background: #075985; }
.lc-card-filter-n { color: var(--lc-ink-mute, #616161); font-weight: 500; }
.lc-card-filter-on .lc-card-filter-n { color: #e0f2fe; opacity: 0.9; }
.lc-card-filter-clear { background: #fff; border-color: #e5e7eb; color: #6b7280; }
.lc-feat-dot { display: inline-flex; align-items: center; gap: 0.2em; font-size: 0.72em; font-weight: 600; padding: 0.1em 0.45em; border-radius: 99px; line-height: 1.6; }
.lc-feat-passing { background: #dcfce7; color: #15803d; }
.lc-feat-failing  { background: #fee2e2; color: #b91c1c; }
.lc-feat-pending  { background: #fef3c7; color: #92400e; }
.lc-feat-none     { background: #f3f4f6; color: #6b7280; }
</style>

<script>
(function () {
  if (window._lcFolderReady) return;
  window._lcFolderReady = true;

  var _lcSiteRepo = {{ site.github.repository_nwo | default: "" | jsonify }};
  var escapeHtml = window.lcEscapeHtml;

  function extractPageMeta(text) {
    var lines = text.split("\n");
    var i = 0, fmDate = null;
    if (lines[0] && lines[0].trim() === "---") {
      i = 1;
      while (i < lines.length && lines[i].trim() !== "---") {
        var dm = lines[i].match(/^date:\s*(.+?)\s*$/);
        if (dm) fmDate = dm[1].replace(/^['"]|['"]$/g, "");
        i++;
      }
      i++;
    }
    /* IAL ({: … }) is OPERATIONAL page content — never touched in pages.
       But a card shows prose, not notation: derived views strip it. */
    function deIAL(t) { return t.replace(/\{:[^}]*\}/g, "").trim(); }
    var title = null, snippet = "";
    for (; i < lines.length; i++) {
      var line = lines[i].trim();
      if (!title && /^#{1,2}\s/.test(line)) { title = deIAL(line.replace(/^#+\s+/, "")); continue; }
      if (title && line && !/^[#{`\->|]/.test(line) && !/^\{:/.test(line) && line !== "---" && !/^[\-*+] /.test(line)) {
        snippet = deIAL(line.replace(/\[([^\]]*)\]\([^)]*\)/g, "$1").replace(/[*_`!]/g, "")).substring(0, 140);
        if (snippet.length >= 140) snippet += "…";
        break;
      }
    }
    return { title: title, snippet: snippet, date: fmDate };
  }

  /* date → human bucket for the card's tag: today / this week / this month /
     this year / "" (older pages carry no tag). Sorting and the Modified
     filters keep the raw data-date — only the label is humanized. */
  function fmtDate(d) {
    var t = new Date(String(d || "")); if (isNaN(t)) return "";
    var now = new Date();
    if (t.toDateString() === now.toDateString()) return "today";
    if (now - t >= 0 && now - t < 7 * 86400000) return "this week";
    if (t.getFullYear() === now.getFullYear() && t.getMonth() === now.getMonth()) return "this month";
    if (t.getFullYear() === now.getFullYear()) return "this year";
    return "";
  }

  /* ── shared card pipeline (also used by related.md) ─────────────── */
  /* scan a page's markdown for its hidden .feature blocks → [{status, tags}] */
  function scanFeatures(text) {
    var scanText = text
      .replace(/(`{3,})[^\n]*\n[\s\S]*?\1/g, "")
      .replace(/`[^`\n]+`/g, "``");
    var features = [], fRe = /\{:\s*\.feature\b([^}]*)\}/g, fm;
    while ((fm = fRe.exec(scanText)) !== null) {
      var sm = fm[1].match(/\bstatus="(\w+)"/);
      var tm = fm[1].match(/\btags="([^"]*)"/);
      features.push({ status: sm ? sm[1] : "", tags: tm ? tm[1] : "" });
    }
    return features;
  }

  /* count the .quiz widgets on a page (skip code fences / inline code) so a
     card can show how many quizzes are still unanswered even before you visit */
  function countQuizzes(text) {
    var scanText = text
      .replace(/(`{3,})[^\n]*\n[\s\S]*?\1/g, "")
      .replace(/`[^`\n]+`/g, "``");
    var n = 0, qRe = /\{:\s*\.quiz\b[^}]*\}/g;
    while (qRe.exec(scanText) !== null) n++;
    return n;
  }

  /* distinct theme tags across a card's features (order preserved) */
  function cardTagList(features) {
    var seen = {}, list = [];
    (features || []).forEach(function(f) {
      (((f && f.tags) || "").split(",")).forEach(function(t) {
        t = t.trim(); if (t && !seen[t]) { seen[t] = 1; list.push(t); }
      });
    });
    return list;
  }

  /* one card's HTML from an item {title, url, snippet, features, isSubdir}.
     opts.clickableTags=false renders plain (non-filtering) tag chips. */
  function buildCardHtml(item, opts) {
    opts = opts || {};
    var tagList = cardTagList(item.features);
    var feats = item.features || [];
    var nonpassing = feats.filter(function(f) { return ((f && f.status) || "none") !== "passing"; }).length;
    var tagsAttr = tagList.length ? ' data-tags="' + escapeHtml(tagList.join(" ")) + '"' : '';
    var style = item.isSubdir ? ' style="background:#f0f2f5"' : '';
    var card = '<div class="lc-card" data-url="' + item.url + '"' + (item.path ? (item.isSubdir ? ' data-dirpath="' : ' data-path="') + escapeHtml(item.path) + '"' : '') + tagsAttr + ' data-nonpassing="' + nonpassing + '" data-quizzes="' + (item.quizzes || 0) + '"' + (item.date ? ' data-date="' + escapeHtml(item.date) + '"' : '') + style + '><h3><a href="' + item.url + '">' + escapeHtml(item.title) + '</a></h3>';
    if (item.snippet) card += '<p style="font-size:0.85em;color:#555;margin:0.3em 0 0">' + escapeHtml(item.snippet) + '</p>';
    var dateLbl = fmtDate(item.date);
    if (dateLbl) card += '<div class="lc-card-date">📅 ' + escapeHtml(dateLbl) + '</div>';
    if (item.features && item.features.length) {
      var counts = {};
      item.features.forEach(function(f) { var s = (f && f.status) || "none"; counts[s] = (counts[s] || 0) + 1; });
      var dots = "";
      if (counts.passing) dots += "<span class='lc-feat-dot lc-feat-passing' title='" + counts.passing + " passing feature" + (counts.passing > 1 ? "s" : "") + "'>● " + counts.passing + "</span>";
      if (counts.failing)  dots += "<span class='lc-feat-dot lc-feat-failing'  title='" + counts.failing  + " failing feature"  + (counts.failing  > 1 ? "s" : "") + "'>✗ " + counts.failing  + "</span>";
      if (counts.pending)  dots += "<span class='lc-feat-dot lc-feat-pending'  title='" + counts.pending  + " pending feature"  + (counts.pending  > 1 ? "s" : "") + "'>◑ " + counts.pending  + "</span>";
      if (counts.none && !counts.passing && !counts.failing && !counts.pending)
        dots += "<span class='lc-feat-dot lc-feat-none' title='" + counts.none + " feature" + (counts.none > 1 ? "s" : "") + " (no status set)'>● " + counts.none + "</span>";
      var clickable = opts.clickableTags !== false;
      var tagsHtml = tagList.length ? "<div class='lc-card-tags'>" + tagList.map(function(t) {
        return "<span class='lc-card-tag'" + (clickable ? " data-tag='" + escapeHtml(t) + "' title='Filter by " + escapeHtml(t) + "'" : "") + ">" + escapeHtml(t) + "</span>";
      }).join("") + "</div>" : "";
      var dotsHtml = dots ? "<div class='lc-card-features'>" + dots + "</div>" : "";
      if (tagsHtml || dotsHtml) card += "<div class='lc-card-footer'>" + tagsHtml + dotsHtml + "</div>";
    }
    return card + '</div>';
  }

  window.lcExtractPageMeta = extractPageMeta;
  window.lcScanFeatures = scanFeatures;
  window.lcCardTagList = cardTagList;
  window.lcBuildCardHtml = buildCardHtml;

  function upgradeFolder(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    var a = el.querySelector("a");
    if (!a) return;
    var cols = el.getAttribute("cols") || "auto";
    var showPrivate = el.getAttribute("show-private") === "true";
    var sortMode = (el.getAttribute("sort") || "name").toLowerCase();   // "name" (default) | "recent"
    /* Rendered INSIDE a bench (a runner render stamps its repo/path on the
       root)? Then scan THAT repo, not the site — a bench's index.md lists its
       own course/ folder, per viewer, regardless of where the page lives. */
    var runRoot = el.closest && el.closest(".lc-run[data-lc-src-repo]");
    /* open="runner" OR simply rendered inside a runner render: the folder lives
       OUTSIDE docs/ (course material, benches), so cards enumerate via the API
       and open in the runner. Inside a render the mode is implied — a bare
       `{: .folder }` "just shows what's here", no knob needed. */
    var runnerMode = (el.getAttribute("open") || "") === "runner" || !!runRoot;
    /* Repo path to enumerate: prefer an explicit path="…" (a repo path, never
       base-healed). With no path, default to the CURRENT folder (".") — a bare
       `{: .folder }` lists the folder it lives in; a placeholder href ("#") is
       not a path. Otherwise the link href with any project base stripped. */
    var _pathAttr = el.getAttribute("path");
    var _href = a.getAttribute("href") || "";
    var _rawAttr = (_pathAttr != null && _pathAttr !== "") ? _pathAttr
                 : (_href && _href !== "#") ? _href
                 : ".";
    var path = "";   // resolved below — the knob may be a "= get_var('NAME','default')" cell
    var scanRepo = (runRoot && runRoot.dataset.lcSrcRepo) || _lcSiteRepo;
    var runBaseDir = "";
    if (runRoot && runRoot.dataset.lcSrcPath) {
      var sp = runRoot.dataset.lcSrcPath;
      runBaseDir = sp.indexOf("/") >= 0 ? sp.split("/").slice(0, -1).join("/") : "";
    }
    var colStyle = cols === "auto"
      ? "repeat(auto-fit, minmax(200px, 1fr))"
      : "repeat(" + cols + ", 1fr)";
    var wrap = document.createElement("div");
    wrap.className = "lc-cards";
    wrap.setAttribute("data-lc-derived", "1");   /* generated, not authored: no text-edit gears */
    wrap.style.gridTemplateColumns = colStyle;
    wrap.innerHTML = "<div style='padding:1em;color:#888'>⏳ Loading…</div>";
    el.parentNode.replaceChild(wrap, el);
    /* No hard requirement on _lcSiteRepo any more: the manifest path lists a
       folder with no API. _lcSiteRepo is only needed for the API fallback and
       the lazy git-date enrichment (ensureDates); both degrade gracefully. */
    var _folderPat = localStorage.getItem('lc_ed_pat') || '';
    var _folderHdrs = _folderPat ? { Authorization: 'Bearer ' + _folderPat, 'X-GitHub-Api-Version': '2022-11-28' } : {};
    function apiFetch(url) {
      /* Authorization forces a CORS preflight and some networks kill the
         OPTIONS (see deploys.md — WebKit reports just "Load failed"). On a
         PUBLIC repo we retry bare: no headers → simple request → no preflight.
         NOT on a private one: there the bare retry is unauthenticated → 404, so
         a network hiccup reads as "folder not found" and the shelf empties
         (that is what killed panels on iPad/cellular). With a key, retry the
         AUTHORIZED request and let a real failure report itself. */
      var go = function (h) {
        return fetch(url, h ? { headers: h } : undefined)
          .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); });
      };
      if (!_folderPat) return go(null);
      return go(_folderHdrs).catch(function () { return go(_folderHdrs); });
    }
    /* ── enumerate from the build-time manifest, not the GitHub API ──────
       The lab repo is private, so api.github.com/contents 404s for anonymous
       visitors. The manifest (assets/pages_index.json) and every page's raw
       .md are served from the public Pages site, so the listing works with no
       API and no PAT. The API stays as a PAT-only enrichment (git dates, in
       ensureDates). If a build has no manifest, fall back to the old API path
       so nothing regresses (pedia keeps working during a transition). */
    var mdUrl   = function (rp) { return "/" + rp.replace(/^docs\//, ""); };      // static .md on Pages
    var runUrl  = function (rp) { return "/run.html#src=gh:" + scanRepo + "/" + rp; };
    var cardUrl = function (rp) { return runnerMode ? runUrl(rp) : mdUrl(rp).replace(/\.md$/i, ""); };
    var titleCase = function (s) { return s.replace(/\.md$/i, "").replace(/[-_]/g, " ").replace(/\b\w/g, function (c) { return c.toUpperCase(); }); };
    function fetchText(url) {
      return fetch(window.lcHref ? window.lcHref(url) : url).then(function (r) { return r.ok ? r.text() : null; });
    }
    function pageItem(rp) {
      return fetchText(mdUrl(rp)).then(function (text) {
        var name = rp.split("/").pop();
        if (!text) return { title: titleCase(name), snippet: "", url: cardUrl(rp), path: rp };
        var meta = extractPageMeta(text);
        var cleanLinks = text.replace(/(`{3,})[^\n]*\n[\s\S]*?\1/g, "").replace(/`[^`\n]+`/g, "");
        var pageSlug = rp.replace(/^docs\//, "").replace(/\.md$/i, "");
        var rawHrefs = [], lRe = /\]\(([^)#\s]+)/g, lm;
        while ((lm = lRe.exec(cleanLinks)) !== null) { var h = lm[1]; if (/^https?:|^mailto:/.test(h)) continue; rawHrefs.push({ h: h, base: pageSlug }); }
        return { title: meta.title || titleCase(name), snippet: meta.snippet, url: cardUrl(rp), features: scanFeatures(text), quizzes: countQuizzes(text), rawHrefs: rawHrefs, date: meta.date || null, path: rp };
      });
    }
    function subdirItem(slug) {   // slug like "components/examples"
      var pretty = titleCase(slug.split("/").pop());
      var fallback = { title: "📁 " + pretty, snippet: "", url: "/" + slug, isSubdir: true };
      return fetchText("/" + slug + "/index.md").then(function (text) {
        if (!text) return fallback;
        var meta = extractPageMeta(text);
        /* a folder card IS its index.md — it wears that page's quiz census
           and score chip like any page card (Michel, 2026-07-31) */
        return { title: "📁 " + (meta.title || pretty), snippet: meta.snippet, url: "/" + slug, isSubdir: true, date: meta.date, quizzes: countQuizzes(text) };
      }).catch(function () { return fallback; });
    }
    function buildFromManifest(all) {
      if (!Array.isArray(all)) throw new Error("bad manifest");
      var prefix = path + "/", slugBase = path.replace(/^docs\//, "");
      var pagePaths = [], subSet = {};
      all.forEach(function (rp) {
        if (rp.indexOf(prefix) !== 0) return;
        var rest = rp.slice(prefix.length);
        if (rest.indexOf("/") >= 0) {
          var _seg = rest.split("/")[0];
          /* underscore folders (_trash, _archive…) are private like
             underscore files — readers never see them, the workbench does */
          if (showPrivate || _lastXray || _seg.charAt(0) !== "_") subSet[_seg] = 1;
          return;
        }
        if (!/\.md$/i.test(rest) || rest === "index.md") return;
        if (!showPrivate && !_lastXray && rest.charAt(0) === "_") return;
        pagePaths.push(rp);
      });
      pagePaths.sort();
      var subdirSlugs = Object.keys(subSet).sort().map(function (s) { return slugBase + "/" + s; });
      return Promise.all(pagePaths.map(pageItem)).then(function (pageItems) {
        return Promise.all(subdirSlugs.map(subdirItem)).then(function (subItems) {
          return pageItems.concat(subItems.filter(Boolean));
        });
      });
    }
    function apiListing() {
      /* inside a bench, a relative path resolves against the rendered file's
         dir (index.md at root → "course" scans <bench>/course) */
      var rel = (path === "." || path === "") ? "" : path;
      var apiPath = (runBaseDir && (rel === "" || rel.charAt(0) !== "/"))
        ? (rel ? runBaseDir + "/" + rel : runBaseDir) : rel;
      return apiFetch("https://api.github.com/repos/" + scanRepo + "/contents/" + apiPath)
      .then(function(files) {
        if (!Array.isArray(files)) throw new Error("Not a directory: " + escapeHtml(path));
        var pages = files.filter(function(f) {
          if (f.type !== "file" || !/\.md$/i.test(f.name) || f.name === "index.md") return false;
          if (!showPrivate && !_lastXray && f.name.startsWith("_")) return false;
          return true;
        }).sort(function(a, b) { return a.name.localeCompare(b.name); });
        var subdirs = files.filter(function(f) {
            return f.type === "dir" && (showPrivate || _lastXray || !f.name.startsWith("_"));
          })
          .sort(function(a, b) { return a.name.localeCompare(b.name); });

        // fetch index.md for each subdir; always emit a card (fallback to dir name on any error)
        var subdirFetches = subdirs.map(function(d) {
          var slug   = d.path.replace(/^docs\//, "");
          var pretty = d.name.replace(/[-_]/g, " ").replace(/\b\w/g, function(c){ return c.toUpperCase(); });
          var subUrl = runnerMode ? runUrl(d.path + "/index.md") : "/" + slug;
          var fallback = { title: "📁 " + pretty, snippet: "", url: subUrl, isSubdir: true, path: d.path };
          return apiFetch(d.url)
            .then(function(entries) {
              var idx = Array.isArray(entries) && entries.find(function(e) {
                return e.type === "file" && e.name.toLowerCase() === "index.md";
              });
              if (!idx || !idx.download_url) return fallback;
              return fetch(idx.download_url)
                .then(function(r) { return r.ok ? r.text() : null; })
                .then(function(text) {
                  if (!text) return fallback;
                  var meta = extractPageMeta(text);
                  return { title: "📁 " + (meta.title || pretty), snippet: meta.snippet, url: subUrl, isSubdir: true, date: meta.date, path: d.path, quizzes: countQuizzes(text) };
                })
                .catch(function() { return fallback; });
            })
            .catch(function() { return fallback; });
        });

        var pageFetches = pages.map(function(f) {
          return fetch(f.download_url)
            .then(function(r) { return r.text(); })
            .then(function(text) {
              var meta = extractPageMeta(text);
              var title = meta.title || f.name.replace(/\.md$/i, "").replace(/[-_]/g, " ").replace(/\b\w/g, function(c){ return c.toUpperCase(); });
              var features = scanFeatures(text);
              var quizzes = countQuizzes(text);
              /* collect internal links for hover ribbons */
              var cleanLinks = text.replace(/(`{3,})[^\n]*\n[\s\S]*?\1/g, "").replace(/`[^`\n]+`/g, "");
              var pageSlug = f.path.replace(/^docs\//, "").replace(/\.md$/i, "");
              var rawHrefs = [], lRe = /\]\(([^)#\s]+)/g, lm;
              while ((lm = lRe.exec(cleanLinks)) !== null) {
                var h = lm[1]; if (/^https?:|^mailto:/.test(h)) continue; rawHrefs.push({ h: h, base: pageSlug });
              }
              /* date: front-matter date now (free); git last-commit date fetched
                 lazily only when the viewer sorts/filters by date (path kept). */
              return { title: title, snippet: meta.snippet, url: cardUrl(f.path), features: features, quizzes: quizzes, rawHrefs: rawHrefs, date: meta.date || null, path: f.path };
            })
            .catch(function() {
              var title = f.name.replace(/\.md$/i, "").replace(/[-_]/g, " ").replace(/\b\w/g, function(c){ return c.toUpperCase(); });
              return { title: title, snippet: "", url: cardUrl(f.path), path: f.path };
            });
        });

        return Promise.all(subdirFetches.concat(pageFetches)).then(function(results) {
          var subdirItems = results.slice(0, subdirs.length).filter(Boolean);
          var pageItems   = results.slice(subdirs.length);
          return pageItems.concat(subdirItems);
        });
      });
    }
    /* knob-cells first (node variables), then enumerate. Runner mode scans
       unrendered material: the manifest only knows site pages, so it goes
       straight to the API (author key raises private repos). */
    /* ── two postures, one component (Michel, 2026-07-31) ─────────────
       READ (default): the listing as always, minus every writing affordance.
       X-RAY (the mode, and not editable=0): the shelf becomes a workbench —
       ➕ New returns, EVERY file shows (underscore ones included), and each
       file card grows a ⚙️ menu: rename / move to… / trash. Trash is a move
       into _trash/ with a _deleted_<timestamp> suffix — recoverable. */
    var _lastXray = null, _lastModeX = null, _bar = null, _menuEl = null;
    function _xrayRW() {
      return !!(window.lcMode && window.lcMode.current() === "xray") &&
             !(window.lcFrame && window.lcFrame.editable === false);
    }
    /* pedagogical access is not ownership: a learner inspecting someone
       else's material gets X-ray's LENS, never its tools. The workbench
       (New, gears, private files) opens only on a repo the viewer can
       PUSH to (Michel, 2026-07-31). */
    var _permP = null;
    function repoWritable() {
      if (!_folderPat) return Promise.resolve(false);
      if (!_permP) _permP = apiFetch("https://api.github.com/repos/" + scanRepo)
        .then(function (d) { return !!(d && d.permissions && d.permissions.push); })
        .catch(function () { return false; });
      return _permP;
    }
    var _treeP = null;
    function repoTree() {
      /* ONE recursive tree call answers every subfolder's census — walking
         directory by directory would cost a request per nesting level */
      if (!_treeP) _treeP = apiFetch("https://api.github.com/repos/" + scanRepo + "/git/trees/HEAD?recursive=1")
        .then(function (d) { return (d && d.tree) || []; })
        .catch(function () { return []; });
      return _treeP;
    }
    function enumerate() {
      return runnerMode
        ? apiListing()
        : fetchText("/assets/pages_index.json")
            .then(function (t) { return buildFromManifest(JSON.parse(t)); })
            .catch(function () { return apiListing(); });   // no/invalid manifest → legacy API path
    }
    function refresh() {
      _lastModeX = _xrayRW();
      closeCardMenu();
      if (_bar && _bar.parentNode) _bar.parentNode.removeChild(_bar);
      _bar = null;
      wrap.innerHTML = "<div style='padding:1em;color:#888'>⏳ Loading…</div>";
      (_lastModeX ? repoWritable() : Promise.resolve(false)).then(function (w) {
        _lastXray = _lastModeX && w;
        enumerate().then(renderItems).catch(_renderFail);
      });
    }
    function closeCardMenu() {
      if (_menuEl && _menuEl.parentNode) _menuEl.parentNode.removeChild(_menuEl);
      _menuEl = null;
    }
    /* git has no rename: a move is copy + delete, two commits, honest and
       recoverable at every step (the copy lands before the original goes) */
    function ghMoveQuiet(from, to, msg) {
      var H = { Authorization: "Bearer " + _folderPat, Accept: "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28" };
      var API = "https://api.github.com/repos/" + scanRepo + "/contents/";
      return fetch(API + from, { headers: H, cache: "no-store" })
        .then(function (r) { if (!r.ok) throw new Error("read HTTP " + r.status); return r.json(); })
        .then(function (f) {
          return fetch(API + to, { method: "PUT", headers: Object.assign({ "Content-Type": "application/json" }, H),
              body: JSON.stringify({ message: msg, content: (f.content || "").replace(/\n/g, "") }) })
            .then(function (r) {
              if (r.status !== 201 && r.status !== 200) {
                if (r.status === 422) throw new Error("destination already exists");
                throw new Error("write HTTP " + r.status);
              }
              return fetch(API + from, { method: "DELETE", headers: Object.assign({ "Content-Type": "application/json" }, H),
                body: JSON.stringify({ message: msg, sha: f.sha }) });
            })
            .then(function (r) { if (!r.ok) throw new Error("delete HTTP " + r.status); });
        });
    }
    function ghMove(from, to, msg) {
      return ghMoveQuiet(from, to, msg)
        .then(function () { _treeP = null; refresh(); })
        .catch(function (e) { alert("Couldn't complete: " + e.message); });
    }
    /* every folder is born as its index.md — including _trash, which is
       born implicitly the first time something lands in it. The quiet PUT
       is a no-op when the index already exists (422). */
    function ensureFolderIndex(dirPath, title) {
      var H = { Authorization: "Bearer " + _folderPat, Accept: "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28", "Content-Type": "application/json" };
      var body = "# " + title + "\n\n[in this folder](#)\n{: .folder }\n";
      return fetch("https://api.github.com/repos/" + scanRepo + "/contents/" + dirPath + "/index.md",
        { method: "PUT", headers: H,
          body: JSON.stringify({ message: "New: " + dirPath + "/index.md", content: btoa(unescape(encodeURIComponent(body))) }) })
        .catch(function () {})
        .then(function () {});
    }
    /* a folder IS its files: moving one moves every blob beneath it,
       sequentially — kind to rate limits, recoverable mid-way */
    function ghMoveDir(fromDir, toDir, msg) {
      return repoTree().then(function (tree) {
        var files = tree.filter(function (t) { return t.type === "blob" && String(t.path).indexOf(fromDir + "/") === 0; });
        if (!files.length) { alert("Empty folder — nothing to move."); return; }
        var chain = Promise.resolve();
        files.forEach(function (t) {
          var rest = String(t.path).slice(fromDir.length + 1);
          chain = chain.then(function () { return ghMoveQuiet(t.path, toDir + "/" + rest, msg); });
        });
        return chain
          .then(function () { _treeP = null; refresh(); })
          .catch(function (e) { alert("Couldn't complete (folder partly moved — refresh and retry): " + e.message); _treeP = null; refresh(); });
      });
    }
    function slugName(raw) {
      return raw.trim().toLowerCase().replace(/\.md$/i, "").replace(/[^a-z0-9]+/g, "_").replace(/^_+|_+$/g, "");
    }
    function showMovePicker(m, p, dir, name, isDir) {
      /* an input with a datalist: the repo's own folders autocomplete the
         destination — type a few letters, pick, Move */
      m.innerHTML = "<div class='lc-folder-move'>" +
        "<input type='text' list='lc-move-dirs' placeholder='destination folder' value='" + escapeHtml(dir) + "'>" +
        "<datalist id='lc-move-dirs'></datalist>" +
        "<button type='button' data-go='1'>📦 Move</button>" +
        "<button type='button' data-cancel='1'>✕</button></div>";
      var inp = m.querySelector("input");
      repoTree().then(function (tree) {
        var dl = m.querySelector("datalist");
        if (!dl) return;
        tree.forEach(function (t) {
          if (t.type !== "tree") return;
          var tp = String(t.path);
          if (isDir && (tp === p || tp.indexOf(p + "/") === 0)) return;   /* not into itself */
          var o = document.createElement("option");
          o.value = tp;
          dl.appendChild(o);
        });
      });
      function go() {
        var dest = (inp.value || "").trim().replace(/^\/+|\/+$/g, "");
        closeCardMenu();
        if (dest === dir) return;
        var to = (dest ? dest + "/" : "") + name;
        var msg = "Move: " + p + " → " + to;
        if (isDir) ghMoveDir(p, to, msg); else ghMove(p, to, msg);
      }
      m.addEventListener("click", function (e) {
        if (e.target.getAttribute && e.target.getAttribute("data-go")) { e.stopPropagation(); go(); }
        else if (e.target.getAttribute && e.target.getAttribute("data-cancel")) { e.stopPropagation(); closeCardMenu(); }
      });
      inp.addEventListener("keydown", function (e) { if (e.key === "Enter") go(); });
      inp.focus();
    }
    function openCardMenu(card, anchor) {
      closeCardMenu();
      var isDir = card.hasAttribute("data-dirpath");
      var p = card.getAttribute(isDir ? "data-dirpath" : "data-path");
      var dir = p.indexOf("/") >= 0 ? p.split("/").slice(0, -1).join("/") : "";
      var name = p.split("/").pop();
      var m = document.createElement("div");
      m.className = "lc-folder-menu";
      m.innerHTML = "<button type='button' data-act='open'>🔬 Open</button>" +
                    "<button type='button' data-act='rename'>✏️ Rename</button>" +
                    "<button type='button' data-act='move'>📦 Move to…</button>" +
                    "<button type='button' data-act='trash'>🗑 Trash</button>";
      m.addEventListener("click", function (e) {
        var act = e.target.getAttribute && e.target.getAttribute("data-act");
        if (!act) return;
        e.preventDefault(); e.stopPropagation();
        if (act === "open") {
          /* stay in the workbench: the target opens straight in X-ray
             (?xray=1 rides the URL, same door that survives refresh) */
          closeCardMenu();
          var target = isDir ? p + "/index.md" : p;
          location.href = (window.lcHref ? window.lcHref("/run.html") : "/run.html") + "?xray=1#src=gh:" + scanRepo + "/" + target;
          return;
        }
        if (act === "move") { showMovePicker(m, p, dir, name, isDir); return; }
        closeCardMenu();
        if (act === "rename") {
          var nn = window.prompt("New name for " + name + ":", name.replace(/\.md$/i, ""));
          if (!nn) return;
          var slug = slugName(nn); if (!slug) return;
          if (isDir) ghMoveDir(p, (dir ? dir + "/" : "") + slug, "Rename: " + name + " → " + slug);
          else ghMove(p, (dir ? dir + "/" : "") + slug + ".md", "Rename: " + name + " → " + slug + ".md");
        } else if (act === "trash") {
          if (!window.confirm("Trash " + name + "? It moves to _trash/ (recoverable).")) return;
          var ts = new Date().toISOString().replace(/[-:TZ]/g, "").slice(0, 14);
          var trashDir = (dir ? dir + "/" : "") + "_trash";
          ensureFolderIndex(trashDir, "🗑 Trash").then(function () {
            if (isDir) ghMoveDir(p, trashDir + "/" + name + "_deleted_" + ts, "Trash: " + name + "/");
            else ghMove(p, trashDir + "/" + name.replace(/\.md$/i, "") + "_deleted_" + ts + ".md", "Trash: " + name);
          });
        }
      });
      card.appendChild(m);
      _menuEl = m;
    }
    document.addEventListener("click", function (e) {
      if (_menuEl && !_menuEl.contains(e.target)) closeCardMenu();
    });
    document.addEventListener("lc-mode-changed", function () {
      /* the shelf re-lists when X-ray opens or closes — hidden files and
         write affordances appear and retire with the mode */
      if (document.body.contains(wrap) && _xrayRW() !== _lastModeX) refresh();
    });
    function renderItems(items) {
        if (!items || !items.length) {
          var _where = (path === "." || path === "") ? "this folder yet" : escapeHtml(path);
          /* the hint matches the posture: read mode has no ➕ New to point at */
          wrap.innerHTML = "<div style='padding:1em;color:#888'>No pages in " + _where + ".&nbsp;</div>";
          if (_lastXray && runnerMode && _folderPat) {
            var mk = document.createElement("button");
            mk.type = "button"; mk.className = "lc-card-filter-chip";
            mk.setAttribute("data-newpage", "1");
            mk.style.cssText = "background:#e8f5e9;border-color:#a5d6a7;color:#1b5e20";
            mk.textContent = "➕ New";
            mk.addEventListener("click", function () { newPagePrompt(mk); });
            wrap.firstChild.appendChild(mk);
          }
          return;
        }
        /* resolve internal links between items */
        var urlSet = {};
        items.forEach(function(it) { urlSet[it.url] = it; });
        items.forEach(function(it) {
          it.links = [];
          (it.rawHrefs || []).forEach(function(ref) {
            var resolved;
            if (/^\//.test(ref.h)) {
              resolved = ref.h.replace(/\.md$/i, "");
            } else {
              var parts = ref.base.split("/"); parts.pop();
              ref.h.split("/").forEach(function(p) { if (p === "..") parts.pop(); else if (p && p !== ".") parts.push(p); });
              resolved = "/" + parts.join("/").replace(/\.md$/i, "");
            }
            if (urlSet[resolved] && resolved !== it.url) it.links.push(resolved);
          });
        });

        var allTags = {};
        wrap.innerHTML = items.map(function(item) {
          cardTagList(item.features).forEach(function(t) { allTags[t] = (allTags[t] || 0) + 1; });
          return buildCardHtml(item, { clickableTags: true });
        }).join("");
        /* cards land AFTER the page-level rebase — heal their root-absolute
           links now or every card 404s under /lightcodelab (data-url attrs
           stay canonical: filtering and ribbons key on them) */
        if (window.lcRebase) window.lcRebase(wrap);

        /* X-ray workbench: each FILE card gets its ⚙️ (subfolders keep
           their card clean — moving whole trees is not a card gesture) */
        if (_lastXray && runnerMode && _folderPat) {
          wrap.querySelectorAll(".lc-card[data-path]").forEach(function (c) {
            /* an APPENDED workbench row — the card's own preview, tags,
               feature dots and score chip stay exactly as in read mode;
               X-ray only ADDS. The real filename sits before the gear so
               rename/move/trash hold no surprises. */
            var row = document.createElement("div");
            row.className = "lc-card-workrow";
            var fn = document.createElement("span");
            fn.className = "lc-card-fname";
            fn.textContent = (c.getAttribute("data-path") || "").split("/").pop();
            fn.title = c.getAttribute("data-path") || "";
            var g = document.createElement("button");
            g.type = "button"; g.className = "lc-card-gear"; g.textContent = "⚙️";
            g.title = "Rename · Move · Trash";
            g.addEventListener("click", function (e) { e.preventDefault(); e.stopPropagation(); openCardMenu(c, g); });
            row.appendChild(fn); row.appendChild(g);
            c.appendChild(row);
          });
          /* subfolder census: how much lives below — public/total files,
             sub-sub-folders included (an underscore anywhere on the path
             means private). The author sees the weight of every branch. */
          var _dirCards = wrap.querySelectorAll(".lc-card[data-dirpath]");
          if (_dirCards.length) repoTree().then(function (tree) {
            _dirCards.forEach(function (c) {
              if (c.querySelector(".lc-card-workrow")) return;
              var dp = c.getAttribute("data-dirpath") + "/";
              var tot = 0, pub = 0;
              tree.forEach(function (t) {
                if (t.type !== "blob" || String(t.path).indexOf(dp) !== 0) return;
                tot++;
                var hidden = String(t.path).slice(dp.length).split("/").some(function (sg) { return sg.charAt(0) === "_"; });
                if (!hidden) pub++;
              });
              var row = document.createElement("div");
              row.className = "lc-card-workrow";
              var fn = document.createElement("span");
              fn.className = "lc-card-fname";
              fn.textContent = dp.split("/").filter(Boolean).pop() + "/";
              fn.title = c.getAttribute("data-dirpath");
              var ct = document.createElement("span");
              ct.className = "lc-card-fname lc-card-fcount";
              ct.textContent = "📄 " + pub + "/" + tot;
              ct.title = pub + " public of " + tot + " files, subfolders included";
              var g = document.createElement("button");
              g.type = "button"; g.className = "lc-card-gear"; g.textContent = "⚙️";
              g.title = "Open · Rename · Move · Trash";
              g.addEventListener("click", function (e) { e.preventDefault(); e.stopPropagation(); openCardMenu(c, g); });
              row.appendChild(fn); row.appendChild(ct); row.appendChild(g);
              c.appendChild(row);
            });
          });
        }

        /* ── tag filter bar: clickable chips that show/hide cards by tag ── */
        var tagNames = Object.keys(allTags).sort();

        /* state filters ("remaining work"): unanswered quizzes (from the
           per-page score in localStorage) and not-yet-passing features. */
        var cardsArr = Array.prototype.slice.call(wrap.querySelectorAll(".lc-card[data-url]"));
        function cardUnanswered(c) {
          var total = parseInt(c.getAttribute("data-quizzes") || "0", 10);
          var s = window.lcPageScores && window.lcPageScores.get(c.getAttribute("data-url"));
          return Math.max(0, total - (s ? (s.total || 0) : 0));
        }
        function cardNonpassing(c) { return parseInt(c.getAttribute("data-nonpassing") || "0", 10); }
        var nUnanswered = cardsArr.filter(function(c) { return cardUnanswered(c) > 0; }).length;
        var nNonpassing = cardsArr.filter(function(c) { return cardNonpassing(c) > 0; }).length;

        /* ── one bar: Sort (orders only) + Filters (compose with AND) ──────
           Sort = Name | 🕒 Recent, ordering only — it never hides a card.
           Filters combine: tag/state chips (OR within) AND a Modified-within
           window. Git dates load LAZILY on first Recent; the 📅 tags and the
           Modified chips then stay in BOTH sorts, so tags + time work together. */
        var alphaOrder = cardsArr.slice();            // initial DOM order = the name sort
        var active = {}, timeSecs = 0, datesLoaded = false;
        var showTags = tagNames.length >= 2;

        var bar = document.createElement("div");
        bar.className = "lc-card-filter";
        var chips = "<span class='lc-card-filter-label'>Sort:</span>"
          + "<button type='button' class='lc-card-filter-chip' data-sort='name'>Name</button>"
          + "<button type='button' class='lc-card-filter-chip' data-sort='recent'>🕒 Recent</button>";
        if (showTags || nNonpassing || nUnanswered) {
          chips += "<span class='lc-card-filter-label' style='margin-left:0.6em'>Filter:</span>";
          if (showTags) chips += tagNames.map(function(t) {
            return "<button type='button' class='lc-card-filter-chip' data-tag='" + escapeHtml(t) + "'>"
              + escapeHtml(t) + " <span class='lc-card-filter-n'>" + allTags[t] + "</span></button>";
          }).join("");
          if (nNonpassing) chips += "<button type='button' class='lc-card-filter-chip' data-state='nonpassing' title='Cards with features not yet passing'>✗ to fix <span class='lc-card-filter-n'>" + nNonpassing + "</span></button>";
          if (nUnanswered) chips += "<button type='button' class='lc-card-filter-chip' data-state='unanswered' title='Cards with quizzes you have not answered'>❓ unanswered <span class='lc-card-filter-n'>" + nUnanswered + "</span></button>";
        }
        chips += "<span class='lc-card-times' style='display:none'>"
          + "<span class='lc-card-filter-label' style='margin-left:0.6em'>Modified:</span>"
          + "<button type='button' class='lc-card-filter-chip' data-age='3600'>hour</button>"
          + "<button type='button' class='lc-card-filter-chip' data-age='86400'>day</button>"
          + "<button type='button' class='lc-card-filter-chip' data-age='604800'>week</button>"
          + "<button type='button' class='lc-card-filter-chip' data-age='2592000'>month</button>"
          + "</span>";
        chips += "<button type='button' class='lc-card-filter-chip lc-card-filter-clear' data-clear='1' hidden>✕ clear</button>";
        /* ➕ New page — author new material without leaving the shelf. Runner
           mode only (it edits repo files), and only with a connected key.
           Creates <path>/<name>.md and opens it in the runner to edit+Save. */
        if (runnerMode && _folderPat && _lastXray)
          chips += "<button type='button' class='lc-card-filter-chip' data-newpage='1' style='margin-left:auto;background:#e8f5e9;border-color:#a5d6a7;color:#1b5e20'>➕ New</button>";
        bar.innerHTML = chips;
        wrap.parentNode.insertBefore(bar, wrap);
        _bar = bar;
        var npBtn = bar.querySelector("[data-newpage]");
        if (npBtn) npBtn.addEventListener("click", function () { newPagePrompt(npBtn); });
        function newPagePrompt(npBtn) {
          var raw = window.prompt("New page or folder?\n• a name → a page (module_03)\n• end with / → a folder (week4/)");
          if (!raw) return;
          raw = raw.trim();
          var isFolder = /\/\s*$/.test(raw);
          /* ".md" is the default AND the only extension: typing it is fine
             (stripped before slugifying — "notes.md" must not become
             notes_md.md), omitting it is fine too */
          var slug = raw.replace(/\/+$/, "").trim().toLowerCase().replace(/\.md$/i, "").replace(/[^a-z0-9]+/g, "_").replace(/^_+|_+$/g, "");
          if (!slug) return;
          var rel = (path === "." || path === "") ? "" : path;
          var apiPath = (runBaseDir && (rel === "" || rel.charAt(0) !== "/")) ? (rel ? runBaseDir + "/" + rel : runBaseDir) : rel;
          /* git has no empty folders — a new folder is created as its index.md,
             which is also its landing page (same convention as the vault) */
          var filePath = (apiPath ? apiPath + "/" : "") + slug + (isFolder ? "/index.md" : ".md");
          var title = raw.replace(/\/+$/, "").trim();
          npBtn.disabled = true; npBtn.textContent = "➕ Creating…";
          /* every new node ships a bare .folder so you can see what's around it —
             no path (defaults to the current folder) and no open knob (runner
             mode is implied inside a render). It just shows what's here. */
          var body = "# " + title + "\n\nStart writing here.\n\n[" +
            (isFolder ? "in this folder" : "in this module") + "](#)\n{: .folder }\n";
          fetch("https://api.github.com/repos/" + scanRepo + "/contents/" + filePath,
            { method: "PUT", headers: { Authorization: "Bearer " + _folderPat, Accept: "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28", "Content-Type": "application/json" },
              body: JSON.stringify({ message: "New: " + filePath, content: btoa(unescape(encodeURIComponent(body))) }) })
            .then(function (r) {
              if (r.status === 201) location.href = (window.lcHref ? window.lcHref("/run.html") : "/run.html") + "#src=gh:" + scanRepo + "/" + filePath;
              else if (r.status === 422) { npBtn.disabled = false; npBtn.textContent = "➕ New"; alert("“" + slug + "” already exists here."); }
              else r.json().then(function (d) { npBtn.disabled = false; npBtn.textContent = "➕ New"; alert("Couldn't create: " + (d.message || ("HTTP " + r.status))); });
            })
            .catch(function () { npBtn.disabled = false; npBtn.textContent = "➕ New"; alert("Couldn't reach GitHub — try again."); });
        }
        var timesWrap = bar.querySelector(".lc-card-times");
        /* honest empty-state: if no card got a date (API unreachable), a time
           window must not silently hide everything — show all + say why */
        var dateNote = document.createElement("span");
        dateNote.className = "lc-card-filter-label";
        dateNote.style.display = "none";
        dateNote.textContent = "⚠️ dates unavailable — showing all";
        timesWrap.appendChild(dateNote);

        function cardItem(c) { return urlSet[c.getAttribute("data-url")]; }
        function chipKey(chip) {
          if (chip.getAttribute("data-state")) return "state:" + chip.getAttribute("data-state");
          return chip.getAttribute("data-tag") || "";
        }
        function cardMatches(c, key) {
          if (key.indexOf("state:") === 0) {
            var st = key.slice(6);
            if (st === "unanswered") return cardUnanswered(c) > 0;
            if (st === "nonpassing") return cardNonpassing(c) > 0;
            return false;
          }
          return (c.getAttribute("data-tags") || "").split(" ").indexOf(key) >= 0;
        }
        function withinAge(c) {
          var d = (cardItem(c) || {}).date;
          return d && (Date.now() - (new Date(d)).getTime()) <= timeSecs * 1000;
        }
        function applyFilters() {                     // tag/state (OR) AND time
          var keys = Object.keys(active);
          var haveDates = !timeSecs || cardsArr.some(function(c) { return (cardItem(c) || {}).date; });
          cardsArr.forEach(function(c) {
            var tagOk = !keys.length || keys.some(function(k) { return cardMatches(c, k); });
            var timeOk = !timeSecs || !haveDates || withinAge(c);
            c.style.display = (tagOk && timeOk) ? "" : "none";
          });
          dateNote.style.display = (timeSecs && !haveDates) ? "" : "none";
          bar.querySelectorAll("[data-tag],[data-state]").forEach(function(chip) {
            var key = chipKey(chip); if (key) chip.classList.toggle("lc-card-filter-on", !!active[key]);
          });
          timesWrap.querySelectorAll("[data-age]").forEach(function(ch) {
            ch.classList.toggle("lc-card-filter-on", parseInt(ch.getAttribute("data-age"), 10) === timeSecs);
          });
          var clr = bar.querySelector("[data-clear]");
          if (clr) clr.hidden = !(keys.length || timeSecs);
        }
        function toggleTag(key) { if (!key) return; if (active[key]) delete active[key]; else active[key] = 1; applyFilters(); }
        function reflowRibbon() { if (ribbonSvg && ribbonSvg.parentNode === wrap) wrap.appendChild(ribbonSvg); }
        function paintDate(c) {
          var it = cardItem(c); if (!it || !it.date) return;
          c.setAttribute("data-date", it.date);
          var tag = c.querySelector(".lc-card-date");
          var lbl = fmtDate(it.date);
          if (!lbl) { if (tag) tag.remove(); return; }
          if (!tag) { tag = document.createElement("div"); tag.className = "lc-card-date"; c.appendChild(tag); }
          tag.textContent = "📅 " + lbl;
        }
        function ensureDates() {
          if (datesLoaded) return Promise.resolve();
          datesLoaded = true;
          /* one /commits call per card is rate-limit-hungry (anonymous = 60/h)
             → cache each file's date for 30 min so repeat visits are free */
          var CK = "lc_fdate.", TTL = 30 * 60 * 1000;
          return Promise.all(cardsArr.map(function(c) {
            var it = cardItem(c);
            if (!it || it.date || !it.path) return Promise.resolve();
            try {
              var hit = JSON.parse(localStorage.getItem(CK + it.path) || "null");
              if (hit && hit.d && Date.now() - hit.t < TTL) { it.date = hit.d; return Promise.resolve(); }
            } catch (e) {}
            return apiFetch("https://api.github.com/repos/" + _lcSiteRepo + "/commits?path=" + encodeURIComponent(it.path) + "&per_page=1")
              .then(function(cs) {
                it.date = (cs && cs[0] && cs[0].commit) ? ((cs[0].commit.committer || cs[0].commit.author || {}).date || null) : null;
                if (it.date) { try { localStorage.setItem(CK + it.path, JSON.stringify({ t: Date.now(), d: it.date })); } catch (e) {} }
              })
              .catch(function() {});
          }));
        }
        function orderBy(mode) {
          var order = mode === "recent"
            ? cardsArr.slice().sort(function(a, b) {
                var da = (cardItem(a) || {}).date || "", db = (cardItem(b) || {}).date || "";
                if (da && db) return db < da ? -1 : (db > da ? 1 : 0);
                if (da) return -1; if (db) return 1;
                return (a.getAttribute("data-url") || "").localeCompare(b.getAttribute("data-url"));
              })
            : alphaOrder;
          order.forEach(function(c) { wrap.appendChild(c); });
          reflowRibbon();
        }
        function setSort(mode) {
          bar.querySelectorAll("[data-sort]").forEach(function(b) { b.classList.toggle("lc-card-filter-on", b.getAttribute("data-sort") === mode); });
          if (mode === "recent") {
            ensureDates().then(function() {
              cardsArr.forEach(paintDate);            // 📅 tags on the cards
              timesWrap.style.display = "";           // reveal the Modified filters
              orderBy("recent"); applyFilters();
            });
          } else {
            // back to the initial Name state: no date filters, no date tags
            timeSecs = 0;                             // drop any active Modified window
            timesWrap.style.display = "none";
            cardsArr.forEach(function(c) { var t = c.querySelector(".lc-card-date"); if (t) t.remove(); });
            orderBy("name"); applyFilters();
          }
        }
        bar.addEventListener("click", function(e) {
          var s = e.target.closest("[data-sort]"), a = e.target.closest("[data-age]"),
              f = e.target.closest("[data-tag],[data-state]"), clr = e.target.closest("[data-clear]");
          if (s) setSort(s.getAttribute("data-sort"));
          else if (a) { var k = parseInt(a.getAttribute("data-age"), 10); timeSecs = (timeSecs === k) ? 0 : k; applyFilters(); }
          else if (f) toggleTag(chipKey(f));
          else if (clr) { active = {}; timeSecs = 0; applyFilters(); }
        });
        /* per-card tag chips drive the same filter */
        wrap.addEventListener("click", function(e) {
          var chip = e.target.closest(".lc-card-tag[data-tag]");
          if (!chip) return;
          e.preventDefault(); e.stopPropagation();
          toggleTag(chip.getAttribute("data-tag"));
        });

        /* hover ribbons — overlay SVG draws bezier arcs between linked cards */
        var ribbonSvg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
        ribbonSvg.style.cssText = "position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;overflow:visible;";
        wrap.style.position = "relative";
        wrap.appendChild(ribbonSvg);

        /* arrowhead marker for ribbons */
        var NS = "http://www.w3.org/2000/svg";
        var defs = document.createElementNS(NS, "defs");
        var mk = document.createElementNS(NS, "marker");
        mk.setAttribute("id", "lc-rib-arr"); mk.setAttribute("markerWidth", "7"); mk.setAttribute("markerHeight", "7");
        mk.setAttribute("refX", "6"); mk.setAttribute("refY", "3"); mk.setAttribute("orient", "auto");
        var mp = document.createElementNS(NS, "path"); mp.setAttribute("d", "M0,0 L0,6 L7,3 z");
        mp.setAttribute("fill", "#0066cc"); mp.setAttribute("opacity", "0.55");
        mk.appendChild(mp); defs.appendChild(mk); ribbonSvg.appendChild(defs);

        function cardCenter(cardEl) {
          var wr = wrap.getBoundingClientRect(), cr = cardEl.getBoundingClientRect();
          return { x: cr.left - wr.left + cr.width / 2, y: cr.top - wr.top + cr.height / 2 };
        }
        function drawRibbons(srcCard, linkedUrls) {
          /* keep defs, clear only paths */
          Array.from(ribbonSvg.childNodes).forEach(function(n) { if (n !== defs) ribbonSvg.removeChild(n); });
          linkedUrls.forEach(function(url) {
            var tgt = wrap.querySelector('[data-url="' + url + '"]');
            if (!tgt) return;
            var s = cardCenter(srcCard), t = cardCenter(tgt);
            var mx = (s.x + t.x) / 2, my = (s.y + t.y) / 2 - Math.abs(t.x - s.x) * 0.25;
            var path = document.createElementNS(NS, "path");
            path.setAttribute("d", "M" + s.x + "," + s.y + " Q" + mx + "," + my + " " + t.x + "," + t.y);
            path.setAttribute("fill", "none");
            path.setAttribute("stroke", "#0066cc");
            path.setAttribute("stroke-width", "1.5");
            path.setAttribute("stroke-dasharray", "4 3");
            path.setAttribute("opacity", "0.45");
            path.setAttribute("marker-end", "url(#lc-rib-arr)");
            ribbonSvg.appendChild(path);
          });
        }

        wrap.querySelectorAll(".lc-card[data-url]").forEach(function(cardEl) {
          var url = cardEl.getAttribute("data-url");
          var item = urlSet[url];
          if (!item || !item.links || !item.links.length) return;
          cardEl.addEventListener("mouseenter", function() { drawRibbons(cardEl, item.links); });
          cardEl.addEventListener("mouseleave", function() { ribbonSvg.innerHTML = ""; });
        });

        setSort(sortMode === "recent" ? "recent" : "name");   // honor the author's default; viewer can switch
        applyFilters();
    }
    function _renderFail(e) {
        if (e && e._lcHandled) return;    // the gentle to-be-defined card is already up
        if (runnerMode && !_folderPat)
          wrap.innerHTML = "<div class='lc-card' style='color:#6b7280'>🔒 Connect your author key (Get started, top right) to browse this private material.</div>";
        else
          wrap.innerHTML = "<div class='lc-card' style='color:#c00'>⚠️ " + escapeHtml(e.message) + "</div>";
    }
    (window.lcResolveKnob ? window.lcResolveKnob(_rawAttr) : Promise.resolve(_rawAttr))
      .then(function (_resolved) {
        if (!_resolved) {                 // an unset node variable, no default — gentle, never an error
          wrap.innerHTML = "<div class='lc-card' style='color:#6b7280'>🌱 To be defined — set this node's variable (Settings → Secrets and variables → Variables), or give the knob a default: path=\"= get_var('NAME','fallback')\".</div>";
          return;
        }
        var _rawPath = _resolved;
        if (window.lcBase && _rawPath.indexOf(window.lcBase + "/") === 0) _rawPath = _rawPath.slice(window.lcBase.length);
        path = _rawPath.replace(/^\/+|\/+$/g, "");
        refresh();
      });
  }

  /* ── boot ────────────────────────────────────────────────────── */
  /* code_chrome.md (loaded first, via topbar) provides the scan registry. */

  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader("p.folder", upgradeFolder);
  }

})();
</script>
