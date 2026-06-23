{%- comment -%}
Folder — card grid of a docs/ subfolder's pages, with per-page
feature-status dots. Fetches the folder listing and page front matter
from the repository. Activated by IAL: {: .folder } on a link paragraph.

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-card-footer { display: flex; align-items: center; gap: 0.5em; margin-top: 0.65em; flex-wrap: wrap; }
.lc-card-features { display: flex; gap: 0.35em; align-items: center; flex-wrap: wrap; margin-left: auto; }
.lc-card-tags { display: flex; gap: 0.3em; flex-wrap: wrap; }
.lc-card-tag { font-size: 0.7em; font-weight: 600; padding: 0.1em 0.5em; border-radius: 99px; background: #e0f2fe; color: #075985; line-height: 1.6; }
.lc-card-tag[data-tag] { cursor: pointer; }
.lc-card-tag[data-tag]:hover { background: #bae6fd; }
/* ── tag filter bar (clickable chips above the grid) ── */
.lc-card-filter { display: flex; align-items: center; flex-wrap: wrap; gap: 0.4em; margin: 0 0 0.9em; }
.lc-card-filter-label { font-size: 0.75em; font-weight: 600; color: #6b7280; margin-right: 0.1em; }
.lc-card-filter-chip { font-size: 0.72em; font-weight: 600; padding: 0.2em 0.65em; border-radius: 99px; border: 1px solid #bae6fd; background: #f0f9ff; color: #075985; cursor: pointer; line-height: 1.5; }
.lc-card-filter-chip:hover { background: #e0f2fe; }
.lc-card-filter-on { background: #0284c7; color: #fff; border-color: #0284c7; }
.lc-card-filter-n { opacity: 0.6; font-weight: 500; }
.lc-card-filter-clear { border-color: #e5e7eb; background: #fff; color: #6b7280; }
/* state filters (remaining work) are amber to set them apart from theme tags */
.lc-card-filter-state { border-color: #fcd34d; background: #fffbeb; color: #92400e; }
.lc-card-filter-state:hover { background: #fef3c7; }
.lc-card-filter-state.lc-card-filter-on { background: #0284c7; color: #fff; border-color: #0284c7; }
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
    var i = 0;
    if (lines[0] && lines[0].trim() === "---") {
      i = 1;
      while (i < lines.length && lines[i].trim() !== "---") i++;
      i++;
    }
    var title = null, snippet = "";
    for (; i < lines.length; i++) {
      var line = lines[i].trim();
      if (!title && /^#{1,2}\s/.test(line)) { title = line.replace(/^#+\s+/, ""); continue; }
      if (title && line && !/^[#{`\->|]/.test(line) && !/^\{:/.test(line) && line !== "---" && !/^[\-*+] /.test(line)) {
        snippet = line.replace(/\[([^\]]*)\]\([^)]*\)/g, "$1").replace(/[*_`!]/g, "").trim().substring(0, 140);
        if (snippet.length >= 140) snippet += "…";
        break;
      }
    }
    return { title: title, snippet: snippet };
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
    var card = '<div class="lc-card" data-url="' + item.url + '"' + tagsAttr + ' data-nonpassing="' + nonpassing + '" data-quizzes="' + (item.quizzes || 0) + '"' + style + '><h3><a href="' + item.url + '">' + escapeHtml(item.title) + '</a></h3>';
    if (item.snippet) card += '<p style="font-size:0.85em;color:#555;margin:0.3em 0 0">' + escapeHtml(item.snippet) + '</p>';
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
    var path = a.getAttribute("href").replace(/^\/+|\/+$/g, "");
    var cols = el.getAttribute("cols") || "auto";
    var showPrivate = el.getAttribute("show-private") === "true";
    var colStyle = cols === "auto"
      ? "repeat(auto-fit, minmax(200px, 1fr))"
      : "repeat(" + cols + ", 1fr)";
    var wrap = document.createElement("div");
    wrap.className = "lc-cards";
    wrap.style.gridTemplateColumns = colStyle;
    wrap.innerHTML = "<div style='padding:1em;color:#888'>⏳ Loading…</div>";
    el.parentNode.replaceChild(wrap, el);
    if (!_lcSiteRepo) {
      wrap.innerHTML = "<div class='lc-card' style='color:#c00'>⚠️ site.github.repository_nwo not set.</div>";
      return;
    }
    var _folderPat = localStorage.getItem('lc_ed_pat') || '';
    var _folderHdrs = _folderPat ? { Authorization: 'Bearer ' + _folderPat, 'X-GitHub-Api-Version': '2022-11-28' } : {};
    function apiFetch(url) {
      return fetch(url, { headers: _folderHdrs }).then(function(r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); });
    }
    apiFetch("https://api.github.com/repos/" + _lcSiteRepo + "/contents/" + path)
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
          var fallback = { title: "📁 " + pretty, snippet: "", url: "/" + slug, isSubdir: true };
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
                  return { title: "📁 " + (meta.title || pretty), snippet: meta.snippet, url: "/" + slug, isSubdir: true };
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
              return { title: title, snippet: meta.snippet, url: "/" + f.path.replace(/^docs\//, "").replace(/\.md$/i, ""), features: features, quizzes: quizzes, rawHrefs: rawHrefs };
            })
            .catch(function() {
              var title = f.name.replace(/\.md$/i, "").replace(/[-_]/g, " ").replace(/\b\w/g, function(c){ return c.toUpperCase(); });
              return { title: title, snippet: "", url: "/" + f.path.replace(/^docs\//, "").replace(/\.md$/i, "") };
            });
        });

        return Promise.all(subdirFetches.concat(pageFetches)).then(function(results) {
          var subdirItems = results.slice(0, subdirs.length).filter(Boolean);
          var pageItems   = results.slice(subdirs.length);
          return pageItems.concat(subdirItems);
        });
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

        if (tagNames.length >= 2 || nUnanswered || nNonpassing) {
          var bar = document.createElement("div");
          bar.className = "lc-card-filter";
          var chips = "<span class='lc-card-filter-label'>Filter:</span>";
          if (tagNames.length >= 2) chips += tagNames.map(function(t) {
            return "<button type='button' class='lc-card-filter-chip' data-tag='" + escapeHtml(t) + "'>"
              + escapeHtml(t) + " <span class='lc-card-filter-n'>" + allTags[t] + "</span></button>";
          }).join("");
          if (nNonpassing) chips += "<button type='button' class='lc-card-filter-chip lc-card-filter-state' data-state='nonpassing' title='Cards with features not yet passing'>✗ to fix <span class='lc-card-filter-n'>" + nNonpassing + "</span></button>";
          if (nUnanswered) chips += "<button type='button' class='lc-card-filter-chip lc-card-filter-state' data-state='unanswered' title='Cards with quizzes you have not answered'>❓ unanswered <span class='lc-card-filter-n'>" + nUnanswered + "</span></button>";
          chips += "<button type='button' class='lc-card-filter-chip lc-card-filter-clear' data-tag='' hidden>✕ clear</button>";
          bar.innerHTML = chips;
          wrap.parentNode.insertBefore(bar, wrap);

          var active = {};
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
          function applyFilter() {
            var keys = Object.keys(active), any = keys.length > 0;
            cardsArr.forEach(function(c) {
              c.style.display = (!any || keys.some(function(k) { return cardMatches(c, k); })) ? "" : "none";
            });
            bar.querySelectorAll(".lc-card-filter-chip").forEach(function(chip) {
              var key = chipKey(chip);
              if (key) chip.classList.toggle("lc-card-filter-on", !!active[key]);
            });
            var clr = bar.querySelector(".lc-card-filter-clear");
            if (clr) clr.hidden = !any;
          }
          function toggleKey(key) {
            if (!key) active = {};
            else if (active[key]) delete active[key];
            else active[key] = 1;
            applyFilter();
          }
          bar.addEventListener("click", function(e) {
            var chip = e.target.closest(".lc-card-filter-chip");
            if (chip) toggleKey(chipKey(chip));
          });
          /* per-card tag chips drive the same filter */
          wrap.addEventListener("click", function(e) {
            var chip = e.target.closest(".lc-card-tag[data-tag]");
            if (!chip) return;
            e.preventDefault(); e.stopPropagation();
            toggleKey(chip.getAttribute("data-tag"));
          });
        }

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
      })
      .catch(function(e) {
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
