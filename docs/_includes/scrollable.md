{%- comment -%}
Scrollable — fixed-height scrolling pane for long code blocks,
activated by IAL: a code block + {: .scrollable height="300" }
Also: Dropdown — a <ul> of links + {: .dropdown label="Menu" }

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-dropdown { position: relative; display: inline-block; margin: 0.3em 0; }
.lc-dd-toggle { background: #0066cc; color: white; border: none; padding: 0.5em 1em; border-radius: 4px; cursor: pointer; font-size: 0.95em; }
.lc-dd-toggle:hover { background: #0052a3; }
.lc-dd-menu { display: none; position: absolute; top: 100%; left: 0; background: white; border: 1px solid #ddd; border-radius: 4px; min-width: 180px; box-shadow: 0 2px 10px rgba(0,0,0,0.12); z-index: 500; margin-top: 4px; }
.lc-dd-menu.open { display: block; }
.lc-dd-menu a { display: block; padding: 0.6em 1em; color: #333; text-decoration: none; }
.lc-dd-menu a:hover { background: #f5f5f5; color: #0066cc; }
.lc-scrollable { overflow-y: auto; padding: 1em 1.4em; border: 1px solid #ddd; border-radius: 6px; background: #fafafa; margin: 1em 0; }
</style>

<script>
(function () {
  if (window._lcScrollableReady) return;
  window._lcScrollableReady = true;

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

  /* ── boot ────────────────────────────────────────────────────── */
  /* code_chrome.md (loaded first, via topbar) provides the scan registry. */

  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader(".highlighter-rouge.scrollable, pre.scrollable", upgradeScrollable);
    window.lcRegisterUpgrader("ul.dropdown", upgradeDropdown);
  }

})();
</script>
