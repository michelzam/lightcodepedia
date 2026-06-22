{%- comment -%}
Related — renders an explicit set of page links as the same rich cards the
folder component builds (title, snippet, feature-status dots, theme tags).

Author with a plain fenced block of site paths, one per line:

    ```
    /components/tabs
    /components/radio
    ```
    {: .related }

(A markdown link list tagged {: .related } also works — any internal <a href>
inside the tagged element is collected.) Reuses folder.md's shared card
pipeline (lcExtractPageMeta / lcScanFeatures / lcBuildCardHtml).

Auto-included by docs/_layouts/default.html (after folder.md).
{%- endcomment -%}

<script>
(function () {
  if (window._lcRelatedReady) return;
  window._lcRelatedReady = true;

  var _repo = {{ site.github.repository_nwo | default: "" | jsonify }};
  var escapeHtml = window.lcEscapeHtml;

  /* GitHub contents API returns file bodies base64-encoded; decode as UTF-8 so
     emoji titles (📑, 🛢️ …) survive. */
  function b64utf8(b64) {
    var bin = atob((b64 || "").replace(/\s/g, ""));
    var bytes = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    return new TextDecoder("utf-8").decode(bytes);
  }

  var _pat = localStorage.getItem('lc_ed_pat') || '';
  var _hdrs = _pat ? { Authorization: 'Bearer ' + _pat, 'X-GitHub-Api-Version': '2022-11-28' } : {};

  function fetchContents(repoPath) {
    return fetch("https://api.github.com/repos/" + _repo + "/contents/" + repoPath, { headers: _hdrs })
      .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); });
  }

  /* a site url like "/components/tabs" or "/components/" maps to repo md paths
     to try in order: the file first, then the folder's index.md. */
  function repoPaths(url) {
    var slug = url.replace(/^\/+|\/+$/g, "");
    if (!slug) return ["docs/index.md"];
    return ["docs/" + slug + ".md", "docs/" + slug + "/index.md"];
  }

  function fetchItem(link) {
    var tries = repoPaths(link.url);
    function attempt(i) {
      if (i >= tries.length) {
        return Promise.resolve({ title: link.label || link.url, snippet: "", url: link.url, features: [] });
      }
      return fetchContents(tries[i]).then(function (obj) {
        if (!obj || obj.type !== "file" || !obj.content) throw new Error("not a file");
        var text = b64utf8(obj.content);
        var meta = window.lcExtractPageMeta(text);
        return {
          title: meta.title || link.label || link.url,
          snippet: meta.snippet,
          url: link.url,
          features: window.lcScanFeatures(text),
          isSubdir: /\/index\.md$/.test(tries[i])
        };
      }).catch(function () { return attempt(i + 1); });
    }
    return attempt(0);
  }

  function collectLinks(el) {
    var links = [], seen = {};
    function add(h, label) {
      if (!/^\//.test(h)) return;
      h = h.replace(/[#?].*$/, "").replace(/\/+$/, "") || "/";
      if (seen[h]) return; seen[h] = 1;
      links.push({ url: h, label: (label || "").trim() });
    }
    var anchors = el.querySelectorAll("a[href]");
    if (anchors.length) {
      Array.prototype.forEach.call(anchors, function (a) { add(a.getAttribute("href") || "", a.textContent || ""); });
    } else {
      var code = el.querySelector("code") || el;
      (code.textContent || "").split(/\r?\n/).forEach(function (line) {
        var h = line.trim();
        if (!h || /^#/.test(h)) return;
        add(/^\//.test(h) ? h : "/" + h, "");
      });
    }
    return links;
  }

  function upgradeRelated(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";

    var links = collectLinks(el);
    var wrap = document.createElement("div");
    wrap.className = "lc-cards lc-related";
    wrap.style.gridTemplateColumns = "repeat(auto-fit, minmax(200px, 1fr))";
    el.parentNode.replaceChild(wrap, el);

    if (!_repo || !links.length) {
      wrap.innerHTML = "<div style='padding:1em;color:#888'>No related pages.</div>";
      return;
    }
    wrap.innerHTML = "<div style='padding:1em;color:#888'>⏳ Loading…</div>";

    Promise.all(links.map(fetchItem)).then(function (items) {
      wrap.innerHTML = items.map(function (it) {
        return window.lcBuildCardHtml(it, { clickableTags: false });
      }).join("");
    }).catch(function (e) {
      wrap.innerHTML = "<div class='lc-card' style='color:#c00'>⚠️ " + escapeHtml(e.message) + "</div>";
    });
  }

  /* ── boot ────────────────────────────────────────────────────── */
  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader(".highlighter-rouge.related, pre.related, ul.related, ol.related, p.related", upgradeRelated);
  }

})();
</script>
