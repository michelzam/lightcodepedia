{%- comment -%}
Widgets — small standalone content widgets, activated from md + IAL:

  ul + {: .carousel delay="4000" }      rotating item display
  code block + {: .scrollable height="300" }   fixed-height scroll pane
  ul + {: .dropdown label="Menu" }      dropdown of links
  ul/p of links + {: .menu }            horizontal icon nav
  link + {: .video } / {: .embed-page } / {: .embed }   media embeds
  code block + {: .code title="…" }   titled code viewer

Named widgets.md because carousel.md / scrollable.md / embed.md are
existing Liquid build-time includes (a separate mechanism, still in use
by content pages) — runtime upgraders must not shadow them.

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-code { border: 1px solid #d0d0d0; border-radius: 8px; overflow: hidden; margin: 1em 0; background: #fafafa; }
.lc-code-title { background: #f3f4f6; padding: 0.45em 0.9em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; color: #444; border-bottom: 1px solid #d0d0d0; display: flex; align-items: center; gap: 0.5em; }
.lc-code-title .lc-code-lang { margin-left: auto; font-size: 0.75em; text-transform: uppercase; color: #888; letter-spacing: 0.05em; }
.lc-code > .highlighter-rouge, .lc-code > pre { margin: 0 !important; border-radius: 0 !important; background: transparent !important; }
.lc-code .highlight { background: transparent !important; }
.lc-code .highlight pre, .lc-code > pre { padding: 0.9em 1em !important; margin: 0 !important; overflow-x: auto; font-size: 0.85em; line-height: 1.5; background: transparent !important; }

.lc-carousel { position: relative; padding: 1.2em 2em; min-height: 4em; background: #fafafa; border-left: 4px solid #0066cc; border-radius: 0 6px 6px 0; margin: 1em 0; }
.lc-carousel-item { display: none; font-style: italic; color: #444; line-height: 1.5; }
.lc-carousel-item.active { display: block; animation: lc-fade 0.4s ease; }
@keyframes lc-fade { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: none; } }
.lc-carousel-dots { text-align: center; margin-top: 0.8em; }
.lc-carousel-dots span { display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #ccc; margin: 0 3px; cursor: pointer; transition: background 0.2s; }
.lc-carousel-dots span.active { background: #0066cc; }

.lc-dropdown { position: relative; display: inline-block; margin: 0.3em 0; }
.lc-dd-toggle { background: #0066cc; color: white; border: none; padding: 0.5em 1em; border-radius: 4px; cursor: pointer; font-size: 0.95em; }
.lc-dd-toggle:hover { background: #0052a3; }
.lc-dd-menu { display: none; position: absolute; top: 100%; left: 0; background: white; border: 1px solid #ddd; border-radius: 4px; min-width: 180px; box-shadow: 0 2px 10px rgba(0,0,0,0.12); z-index: 500; margin-top: 4px; }
.lc-dd-menu.open { display: block; }
.lc-dd-menu a { display: block; padding: 0.6em 1em; color: #333; text-decoration: none; }
.lc-dd-menu a:hover { background: #f5f5f5; color: #0066cc; }
.lc-scrollable { overflow-y: auto; padding: 1em 1.4em; border: 1px solid #ddd; border-radius: 6px; background: #fafafa; margin: 1em 0; }

.lc-menu { display: flex; flex-wrap: wrap; align-items: center; gap: 0.3em 1.5em; padding: 0.5em 0; margin: 0.5em 0 1.2em; border-bottom: 1px solid #eee; }
.lc-menu a { display: inline-flex; align-items: center; gap: 0.4em; text-decoration: none; color: #333; font-weight: 500; font-size: 0.96em; padding: 0.2em 0; }
.lc-menu a:hover { color: #0066cc; }
.lc-menu .lc-menu-ic { font-size: 1.1em; line-height: 1; }

.lc-embed { margin: 0.5em 0; }
</style>

<script>
(function () {
  if (window._lcWidgetsReady) return;
  window._lcWidgetsReady = true;

  var _lcSiteRepo = {{ site.github.repository_nwo | default: "" | jsonify }};
  /* shared helpers from code_chrome.md (parsed earlier — topbar include) */
  var escapeHtml = window.lcEscapeHtml;
  var loadMarked = window.lcLoadMarked;

  function upgradeCarousel(el) {
    var items = Array.from(el.querySelectorAll("li")).map(function(li){ return li.innerHTML; });
    if (!items.length) return;
    var delay = parseInt(el.getAttribute("delay") || "4000", 10);
    var gid = el.id || ("lc-car-" + Math.random().toString(36).slice(2, 7));
    var itemsHtml = items.map(function(h, i){
      return '<div class="lc-carousel-item' + (i === 0 ? " active" : "") + '">' + h + '</div>';
    }).join("");
    var dotsHtml = items.map(function(_, i){
      return '<span class="' + (i === 0 ? "active" : "") + '" data-idx="' + i + '"></span>';
    }).join("");
    var wrapper = document.createElement("div");
    wrapper.className = "lc-carousel";
    wrapper.id = gid;
    wrapper.innerHTML = itemsHtml + '<div class="lc-carousel-dots">' + dotsHtml + '</div>';
    el.parentNode.replaceChild(wrapper, el);
    var elItems = wrapper.querySelectorAll(".lc-carousel-item");
    var dots = wrapper.querySelectorAll(".lc-carousel-dots span");
    var idx = 0;
    function show(n) {
      elItems.forEach(function(x){ x.classList.remove("active"); });
      dots.forEach(function(x){ x.classList.remove("active"); });
      elItems[n].classList.add("active");
      dots[n].classList.add("active");
      idx = n;
    }
    dots.forEach(function(d){ d.addEventListener("click", function(){ show(parseInt(d.dataset.idx, 10)); }); });
    setInterval(function(){ show((idx + 1) % elItems.length); }, delay);
  }

  function upgradeScrollable(el) {
    var h = el.getAttribute("height") || "300";
    var code = el.querySelector("code");
    var content = code ? code.innerHTML : el.innerHTML;
    var wrap = document.createElement("div");
    wrap.className = "lc-scrollable";
    wrap.style.maxHeight = h + "px";
    wrap.innerHTML = "<pre style=\"margin:0;white-space:pre-wrap;\">" + content + "</pre>";
    el.parentNode.replaceChild(wrap, el);
  }

  function upgradeDropdown(el) {
    var label = el.getAttribute("label") || "Menu";
    var gid = el.id || ("lc-dd-" + Math.random().toString(36).slice(2, 7));
    var links = Array.from(el.querySelectorAll("li a")).map(function(a){
      return "<a href=\"" + a.href + "\">" + a.textContent + "</a>";
    }).join("");
    var wrap = document.createElement("div");
    wrap.className = "lc-dropdown";
    wrap.id = "lc-dd-" + gid;
    wrap.innerHTML = "<button class=\"lc-dd-toggle\">" + label + "</button><div class=\"lc-dd-menu\">" + links + "</div>";
    var btn = wrap.querySelector(".lc-dd-toggle");
    var menu = wrap.querySelector(".lc-dd-menu");
    btn.addEventListener("click", function(e){ e.stopPropagation(); menu.classList.toggle("open"); });
    document.addEventListener("click", function(){ menu.classList.remove("open"); }, { passive: true });
    el.parentNode.replaceChild(wrap, el);
  }

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

  function _iframeEl(src, h, cls) {
    var f = document.createElement("iframe");
    if (cls) f.className = cls;
    f.src = src; f.width = "100%"; f.height = h || "400";
    f.setAttribute("loading", "lazy"); f.setAttribute("allowfullscreen", "");
    f.style.border = "none";
    return f;
  }
  function upgradeEmbedPage(el) {
    var a = el.querySelector("a");
    if (!a) return;
    var h = el.getAttribute("height") || "400";
    var src = (window.lcHref || String)(a.getAttribute("href"));
    if (src && src.indexOf("?") === -1) src += "?embed=true"; else src += "&embed=true";
    /* fresh="true" — for bot-regenerated pages (the behave report): Pages
       caches HTML ~10 min, so an embedded report could contradict the
       cache-busted JSON grids beside it. A per-load stamp keeps them honest. */
    if (el.getAttribute("fresh") === "true") src += "&v=" + Date.now();
    var f = _iframeEl(src, h, "lc-embed-page");
    if (el.id) { f.id = el.id; f.setAttribute("data-lc-id", el.id); }   /* so self.page.<id>.load() works */
    el.parentNode.replaceChild(f, el);
  }
  function upgradeEmbedExternal(el) {
    var a = el.querySelector("a");
    if (!a) return;
    var href = a.getAttribute("href");
    // External URLs → iframe
    if (/^https?:\/\//i.test(href)) {
      el.parentNode.replaceChild(_iframeEl(href, el.getAttribute("height") || "600", "lc-embed-page"), el);
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
    var pat = localStorage.getItem("lc_ed_pat") || "";
    var unpublished = /(^|\/)_[^\/]*$/.test(rel);   // _-prefixed: repo tree only, never in the Pages build
    var req;
    if (pat && _lcSiteRepo) {
      /* builder: the API + PAT reaches every node, published or not */
      req = fetch("https://api.github.com/repos/" + _lcSiteRepo + "/contents/docs/" + rel,
                  { headers: { Authorization: "Bearer " + pat, Accept: "application/vnd.github.v3.raw" } });
    } else if (unpublished) {
      /* only raw serves an unpublished node. On a PRIVATE repo raw 404s for
         anonymous visitors — don't fetch a URL we know will 404 (console error,
         nothing to show); invite a PAT. Public repos still preview it via raw. */
      if (window.lcRepoPrivate) {
        container.innerHTML = "<div style='color:#6b7280;font-style:italic;padding:0.5em 0'>🔑 Private node — connect a GitHub PAT (topbar “Get started”) to preview it.</div>";
        return;
      }
      req = fetch("https://raw.githubusercontent.com/" + _lcSiteRepo + "/HEAD/docs/" + rel);
    } else {
      /* published node: the Pages site serves its .md same-origin — works on the
         private lab too (raw would 404 there), no rate limit, no CORS */
      req = fetch(window.lcHref ? window.lcHref("/" + rel) : "/" + rel);
    }
    req
      .then(function(r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.text(); })
      .then(function(text) {
        // strip optional YAML front matter
        if (text.indexOf("---") === 0) {
          var end = text.indexOf("\n---", 3);
          if (end >= 0) { var nl = text.indexOf("\n", end + 1); text = nl >= 0 ? text.slice(nl + 1) : ""; }
        }
        loadMarked(function() {
          container.innerHTML = (window.lcInlineIAL || function (h) { return h; })(marked.parse(text.trim()));
          if (window.lcRebase) window.lcRebase(container); // heal root-absolute paths under a project base
        });
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
    el.parentNode.replaceChild(_iframeEl(src, el.getAttribute("height") || "400", "lc-video"), el);
  }

  function upgradeCode(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    var title = el.getAttribute("title") || "";
    var m = el.className.match(/language-([\w+-]+)/);
    var lang = m ? m[1] : "text";
    var wrap = document.createElement("div");
    wrap.className = "lc-code";
    if (title) {
      var bar = document.createElement("div");
      bar.className = "lc-code-title";
      bar.appendChild(document.createTextNode("📄 "));
      var t = document.createElement("span");
      t.textContent = title;
      bar.appendChild(t);
      var lg = document.createElement("span");
      lg.className = "lc-code-lang";
      lg.textContent = lang;
      bar.appendChild(lg);
      wrap.appendChild(bar);
    }
    el.parentNode.insertBefore(wrap, el);
    wrap.appendChild(el);
  }

  /* ── boot ────────────────────────────────────────────────────── */
  /* code_chrome.md (loaded first, via topbar) provides the scan registry. */

  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader("ul.carousel", upgradeCarousel);
    window.lcRegisterUpgrader(".highlighter-rouge.scrollable, pre.scrollable", upgradeScrollable);
    window.lcRegisterUpgrader("ul.dropdown", upgradeDropdown);
    window.lcRegisterUpgrader("p.menu, ul.menu", upgradeMenu);
    window.lcRegisterUpgrader("p.embed-page", upgradeEmbedPage);
    window.lcRegisterUpgrader("p.embed", upgradeEmbedExternal);
    window.lcRegisterUpgrader("p.video", upgradeVideo);
    window.lcRegisterUpgrader(".highlighter-rouge.code, pre.code", upgradeCode);
  }

})();
</script>
