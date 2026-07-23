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
/* ── tag filter bar (clickable chips above the grid) ── */
.lc-card-filter { display: flex; align-items: center; flex-wrap: wrap; gap: 0.4em; margin: 0 0 0.9em; }
.lc-card-filter-label { font-size: 0.75em; font-weight: 600; color: #6b7280; margin-right: 0.1em; }
/* every chip (sort, tag, work-state, time) shares ONE look: neutral pill, filled
   blue when active. Meaning is carried by the group label + icons, not by colour. */
.lc-card-filter-chip { font-size: 0.72em; font-weight: 600; padding: 0.2em 0.7em; border-radius: 99px; border: 1px solid #d1d5db; background: #f3f4f6; color: #374151; cursor: pointer; line-height: 1.6; }
.lc-card-filter-chip:hover { background: #e5e7eb; }
.lc-card-filter-on { background: #0284c7; color: #fff; border-color: #0284c7; }
.lc-card-filter-on:hover { background: #0369a1; }
.lc-card-filter-n { opacity: 0.65; font-weight: 500; }
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
    var card = '<div class="lc-card" data-url="' + item.url + '"' + tagsAttr + ' data-nonpassing="' + nonpassing + '" data-quizzes="' + (item.quizzes || 0) + '"' + (item.date ? ' data-date="' + escapeHtml(item.date) + '"' : '') + style + '><h3><a href="' + item.url + '">' + escapeHtml(item.title) + '</a></h3>';
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
         OPTIONS (see deploys.md — WebKit reports just "Load failed"). The
         repo is public, so on ANY failure retry bare: no headers → simple
         request → no preflight. Auth only raises the rate limit. */
      var bare = function() { return fetch(url).then(function(r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); }); };
      if (!_folderPat) return bare();
      return fetch(url, { headers: _folderHdrs })
        .then(function(r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
        .catch(bare);
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
        return { title: "📁 " + (meta.title || pretty), snippet: meta.snippet, url: "/" + slug, isSubdir: true, date: meta.date };
      }).catch(function () { return fallback; });
    }
    function buildFromManifest(all) {
      if (!Array.isArray(all)) throw new Error("bad manifest");
      var prefix = path + "/", slugBase = path.replace(/^docs\//, "");
      var pagePaths = [], subSet = {};
      all.forEach(function (rp) {
        if (rp.indexOf(prefix) !== 0) return;
        var rest = rp.slice(prefix.length);
        if (rest.indexOf("/") >= 0) { subSet[rest.split("/")[0]] = 1; return; }   // nested → a subdir
        if (!/\.md$/i.test(rest) || rest === "index.md") return;
        if (!showPrivate && rest.charAt(0) === "_") return;
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
          if (!showPrivate && f.name.startsWith("_")) return false;
          return true;
        }).sort(function(a, b) { return a.name.localeCompare(b.name); });
        var subdirs = files.filter(function(f) { return f.type === "dir"; })
          .sort(function(a, b) { return a.name.localeCompare(b.name); });

        // fetch index.md for each subdir; always emit a card (fallback to dir name on any error)
        var subdirFetches = subdirs.map(function(d) {
          var slug   = d.path.replace(/^docs\//, "");
          var pretty = d.name.replace(/[-_]/g, " ").replace(/\b\w/g, function(c){ return c.toUpperCase(); });
          var subUrl = runnerMode ? runUrl(d.path + "/index.md") : "/" + slug;
          var fallback = { title: "📁 " + pretty, snippet: "", url: subUrl, isSubdir: true };
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
                  return { title: "📁 " + (meta.title || pretty), snippet: meta.snippet, url: subUrl, isSubdir: true, date: meta.date };
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
    (window.lcResolveKnob ? window.lcResolveKnob(_rawAttr) : Promise.resolve(_rawAttr))
      .then(function (_resolved) {
        if (!_resolved) {                 // an unset node variable, no default — gentle, never an error
          wrap.innerHTML = "<div class='lc-card' style='color:#6b7280'>🌱 To be defined — set this node's variable (Settings → Secrets and variables → Variables), or give the knob a default: path=\"= get_var('NAME','fallback')\".</div>";
          throw { _lcHandled: true };
        }
        var _rawPath = _resolved;
        if (window.lcBase && _rawPath.indexOf(window.lcBase + "/") === 0) _rawPath = _rawPath.slice(window.lcBase.length);
        path = _rawPath.replace(/^\/+|\/+$/g, "");
        return runnerMode
          ? apiListing()
          : fetchText("/assets/pages_index.json")
              .then(function (t) { return buildFromManifest(JSON.parse(t)); })
              .catch(function () { return apiListing(); });   // no/invalid manifest → legacy API path
      })
      .then(function(items) {
        if (!items || !items.length) {
          wrap.innerHTML = "<div style='padding:1em;color:#888'>No pages found in " + escapeHtml(path) + "</div>";
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
        if (runnerMode && _folderPat)
          chips += "<button type='button' class='lc-card-filter-chip' data-newpage='1' style='margin-left:auto;background:#e8f5e9;border-color:#a5d6a7;color:#1b5e20'>➕ New</button>";
        bar.innerHTML = chips;
        wrap.parentNode.insertBefore(bar, wrap);
        var npBtn = bar.querySelector("[data-newpage]");
        if (npBtn) npBtn.addEventListener("click", function () {
          var raw = window.prompt("New page or folder?\n• a name → a page (module_03)\n• end with / → a folder (week4/)");
          if (!raw) return;
          raw = raw.trim();
          var isFolder = /\/\s*$/.test(raw);
          var slug = raw.replace(/\/+$/, "").trim().toLowerCase().replace(/[^a-z0-9]+/g, "_").replace(/^_+|_+$/g, "");
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
        });
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
      })
      .catch(function(e) {
        if (e && e._lcHandled) return;    // the gentle to-be-defined card is already up
        if (runnerMode && !_folderPat)
          wrap.innerHTML = "<div class='lc-card' style='color:#6b7280'>🔒 Connect your author key (Get started, top right) to browse this private material.</div>";
        else
          wrap.innerHTML = "<div class='lc-card' style='color:#c00'>⚠️ " + escapeHtml(e.message) + "</div>";
      });
  }

  /* ── boot ────────────────────────────────────────────────────── */
  /* code_chrome.md (loaded first, via topbar) provides the scan registry. */

  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader("p.folder", upgradeFolder);
  }

})();
</script>
