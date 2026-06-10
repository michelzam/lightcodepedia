{%- comment -%}
Embed — media embedding family, activated by IAL on a link paragraph:
  {: .video }      YouTube / Google Drive / direct URL → iframe
  {: .embed-page } another page of this site, chrome-less → iframe
  {: .embed }      external URL → iframe; local module → fetched + rendered inline

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-embed { margin: 0.5em 0; }
</style>

<script>
(function () {
  if (window._lcEmbedReady) return;
  window._lcEmbedReady = true;

  var _lcSiteRepo = {{ site.github.repository_nwo | default: "" | jsonify }};
  var escapeHtml = window.lcEscapeHtml;
  var loadMarked = window.lcLoadMarked;

  function _iframeEl(src, h) {
    var f = document.createElement("iframe");
    f.src = src; f.width = "100%"; f.height = h || "400";
    f.setAttribute("loading", "lazy"); f.setAttribute("allowfullscreen", "");
    f.style.border = "none";
    return f;
  }
  function upgradeEmbedPage(el) {
    var a = el.querySelector("a");
    if (!a) return;
    var h = el.getAttribute("height") || "400";
    var src = a.getAttribute("href");
    if (src && src.indexOf("?") === -1) src += "?embed=true"; else src += "&embed=true";
    el.parentNode.replaceChild(_iframeEl(src, h), el);
  }
  function upgradeEmbedExternal(el) {
    var a = el.querySelector("a");
    if (!a) return;
    var href = a.getAttribute("href");
    // External URLs → iframe
    if (/^https?:\/\//i.test(href)) {
      el.parentNode.replaceChild(_iframeEl(href, el.getAttribute("height") || "600"), el);
      return;
    }
    // Local module → fetch the raw markdown source and render it inline.
    // [Lucky](/_dog) → docs/_dog.md fetched from raw.githubusercontent.
    var container = document.createElement("div");
    container.className = "lc-embed";
    container.innerHTML = "<div style='color:#aaa;font-style:italic;padding:0.5em 0'>⏳ Loading…</div>";
    el.parentNode.replaceChild(container, el);
    var rel = href.replace(/^\/+|\/+$/g, "");
    if (!/\.md$/i.test(rel)) rel += ".md";
    var srcUrl = _lcSiteRepo
      ? "https://raw.githubusercontent.com/" + _lcSiteRepo + "/HEAD/docs/" + rel
      : "/" + rel;
    fetch(srcUrl)
      .then(function(r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.text(); })
      .then(function(text) {
        // strip optional YAML front matter
        if (text.indexOf("---") === 0) {
          var end = text.indexOf("\n---", 3);
          if (end >= 0) { var nl = text.indexOf("\n", end + 1); text = nl >= 0 ? text.slice(nl + 1) : ""; }
        }
        loadMarked(function() { container.innerHTML = marked.parse(text.trim()); });
      })
      .catch(function(err) {
        container.innerHTML = "<div style='color:#c00'>⚠️ Could not load " + escapeHtml(href) + ": " + escapeHtml(err.message) + "</div>";
      });
  }
  function upgradeVideo(el) {
    var a = el.querySelector("a");
    if (!a) return;
    var href = a.getAttribute("href");
    var src = href;
    var gdrive = href.match(/^gdrive:(.+)/);
    if (gdrive) src = "https://drive.google.com/file/d/" + gdrive[1] + "/preview";
    var yt = href.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&?]+)/);
    if (yt) src = "https://www.youtube.com/embed/" + yt[1];
    el.parentNode.replaceChild(_iframeEl(src, el.getAttribute("height") || "400"), el);
  }

  /* ── boot ────────────────────────────────────────────────────── */
  /* code_chrome.md (loaded first, via topbar) provides the scan registry. */

  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader("p.embed-page", upgradeEmbedPage);
    window.lcRegisterUpgrader("p.embed", upgradeEmbedExternal);
    window.lcRegisterUpgrader("p.video", upgradeVideo);
  }

})();
</script>
