{%- comment -%}
Section widgets — accordion, tabs, radio, grid, cards.

One family: each renders the `### `-delimited sections of a code block
(via the core parseSections/markdownBody helpers) into a different
layout, activated by IAL:

  ```
  ### First
  body…
  ### Second
  body…
  ```
  {: .accordion }   or  .tabs / .radio / .grid cols="2" / .cards

p.tabs (a link + {: .tabs }) renders the ### sections of another page,
fetched from the repository.

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-tabs { border: 1px solid #ddd; border-radius: 6px; margin: 1em 0; overflow: hidden; }
.lc-tabs .lc-tab-bar { display: flex; background: #f5f5f5; border-bottom: 1px solid #ddd; flex-wrap: wrap; }
.lc-tabs .lc-tab-btn { background: none; border: none; padding: 0.6em 1.2em; cursor: pointer; font-size: 0.95em; color: #555; border-right: 1px solid #ddd; }
.lc-tabs .lc-tab-btn:hover { background: #eaeaea; }
.lc-tabs .lc-tab-btn.active { background: white; color: #0066cc; font-weight: 600; box-shadow: inset 0 -3px 0 #0066cc; }
.lc-tabs .lc-tab-panel { display: none; padding: 1em 1.4em; }
.lc-tabs .lc-tab-panel.active { display: block; }

.lc-accordion { margin: 1em 0; }
.lc-accordion details { border: 1px solid #ddd; border-radius: 6px; margin: 0.4em 0; overflow: hidden; }
.lc-accordion details summary { padding: 0.7em 1em; background: #f5f5f5; cursor: pointer; font-weight: 600; list-style: none; user-select: none; }
.lc-accordion details summary::-webkit-details-marker { display: none; }
.lc-acc-live { float: right; font-weight: 400; font-size: 0.82em; color: #64748b; margin-left: 1em; }
.lc-accordion details[open] > summary { border-bottom: 1px solid #ddd; background: #e8f0fe; color: #0066cc; }
.lc-accordion details .lc-ac-body { padding: 0.8em 1.2em; }

.lc-radio-group { margin: 1em 0; }
.lc-radio-options { margin-bottom: 1em; padding: 0.6em 1em; background: #f5f5f5; border-radius: 6px; display: flex; flex-wrap: wrap; gap: 0.2em 0; }
.lc-radio-options label { margin-right: 1.4em; cursor: pointer; font-weight: 500; }
.lc-radio-options input { margin-right: 0.4em; }
.lc-radio-body { padding: 1em 1.4em; background: white; border: 1px solid #eee; border-left: 3px solid #0066cc; border-radius: 0 6px 6px 0; }
.lc-radio-content { display: none; }
.lc-radio-content.active { display: block; }

.lc-grid { display: grid; gap: 18px; margin: 1em 0; }
.lc-grid .lc-grid-cell { min-width: 0; }
.lc-grid .lc-grid-cell > h3 { margin-top: 0; margin-bottom: 0.6em; font-size: 1em; color: #666; text-transform: uppercase; letter-spacing: 0.05em; }

.lc-cards { display: grid; gap: 18px; margin: 1em 0; }
.lc-cards .lc-card { border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.2em 1.4em; background: white; transition: transform 0.15s, box-shadow 0.15s; }
.lc-cards .lc-card:hover { transform: translateY(-3px); box-shadow: 0 6px 20px rgba(0,0,0,0.08); border-color: #0066cc; }
.lc-cards .lc-card h3 { margin-top: 0; margin-bottom: 0.5em; font-size: 1.1em; color: #222; }
.lc-cards .lc-card p { margin: 0 0 0.6em; color: #555; line-height: 1.45; }
.lc-cards .lc-card p:last-child { margin-bottom: 0; }
.lc-cards .lc-card a { color: #0066cc; text-decoration: none; font-weight: 500; }
.lc-cards .lc-card a:hover { text-decoration: underline; }

@media (max-width: 700px) { .lc-cards { grid-template-columns: repeat(2, 1fr) !important; } }
@media (max-width: 480px) { .lc-cards { grid-template-columns: 1fr !important; } }
</style>

<script>
(function () {
  if (window._lcSectionsReady) return;
  window._lcSectionsReady = true;

  var _lcSiteRepo = {{ site.github.repository_nwo | default: "" | jsonify }};

  /* shared helpers from code_chrome.md (parsed earlier — topbar include) */
  var escapeHtml    = window.lcEscapeHtml;
  var loadMarked    = window.lcLoadMarked;
  var parseSections = window.lcParseSections;
  var markdownBody  = window.lcMarkdownBody;

  function upgradeAccordion(el) {
    var sections = parseSections(el);
    if (!sections.length) return;
    var wrap = document.createElement("div");
    wrap.className = "lc-accordion";
    sections.forEach(function(s) {
      /* a "!" label prefix renders the body eagerly (while still shut) so
         live components inside — vitals, checks — exist from page load */
      var eager = s.label.charAt(0) === "!";
      var label = eager ? s.label.slice(1).trim() : s.label;
      var d = document.createElement("details");
      var sum = document.createElement("summary");
      sum.textContent = label;
      var live = document.createElement("span");
      live.className = "lc-acc-live";
      sum.appendChild(live);
      var body = document.createElement("div");
      body.className = "lc-ac-body";
      d.appendChild(sum);
      d.appendChild(body);
      function render() {
        if (body.dataset.lcReady) return;
        body.dataset.lcReady = "1";
        loadMarked(function() {
          body.innerHTML = markdownBody(s.body);
          window.lcScanElement(body); /* IAL + full upgrade pipeline */
          /* mirror live counters into the summary: any element in the body
             with data-acc-summary shows its value in the title, visible
             even when the section is shut */
          var sync = function() {
            var parts = [];
            body.querySelectorAll("[data-acc-summary]").forEach(function(n) {
              var v = n.getAttribute("data-acc-summary");
              if (v) parts.push(v);
            });
            live.textContent = parts.length ? parts.join("  ·  ") : "";
          };
          try {
            new MutationObserver(sync).observe(body, {
              subtree: true, childList: true,
              attributes: true, attributeFilter: ["data-acc-summary"]
            });
          } catch (e) {}
          sync();
        });
      }
      d.addEventListener("toggle", function() { if (d.open) render(); });
      if (eager) render();
      wrap.appendChild(d);
    });
    el.parentNode.replaceChild(wrap, el);
  }

  function upgradeTabsInline(el) {
    var sections = parseSections(el);
    if (!sections.length) return;
    var gid = el.id || ("lc-ti-" + Math.random().toString(36).slice(2, 7));
    loadMarked(function() {
      var bar = sections.map(function(s, i){
        return "<button class=\"lc-tab-btn" + (i===0?" active":"") + "\" data-tab=\"" + gid + "-" + i + "\">" + s.label + "</button>";
      }).join("");
      var panels = sections.map(function(s, i){
        return "<div id=\"" + gid + "-" + i + "\" class=\"lc-tab-panel" + (i===0?" active":"") + "\">" + markdownBody(s.body) + "</div>";
      }).join("");
      var wrap = document.createElement("div");
      wrap.className = "lc-tabs";
      wrap.innerHTML = "<div class=\"lc-tab-bar\">" + bar + "</div>" + panels;
      wrap.querySelectorAll(".lc-tab-btn").forEach(function(b){
        b.addEventListener("click", function(){
          wrap.querySelectorAll(".lc-tab-btn").forEach(function(x){x.classList.remove("active");});
          wrap.querySelectorAll(".lc-tab-panel").forEach(function(x){x.classList.remove("active");});
          b.classList.add("active");
          document.getElementById(b.dataset.tab).classList.add("active");
        });
      });
      el.parentNode.replaceChild(wrap, el);
    });
  }

  function upgradeTabsFile(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    var a = el.querySelector("a");
    if (!a) return;
    var filePath = a.getAttribute("href").replace(/^\/+|\/+$/g, "");
    var gid = el.getAttribute("id") || ("lc-tf-" + Math.random().toString(36).slice(2, 7));
    var placeholder = document.createElement("div");
    placeholder.innerHTML = "<div style='padding:1em;color:#888'>⏳ Loading tabs…</div>";
    el.parentNode.replaceChild(placeholder, el);
    if (!_lcSiteRepo) {
      placeholder.innerHTML = "<div class='lc-tabs' style='padding:1em;color:#c00'>⚠️ site.github.repository_nwo not set.</div>";
      return;
    }
    var rawUrl = "https://raw.githubusercontent.com/" + _lcSiteRepo + "/main/docs/" + filePath + ".md";
    fetch(rawUrl)
      .then(function(r) { if (!r.ok) throw new Error("File not found: " + filePath + ".md"); return r.text(); })
      .then(function(text) {
        var lines = text.split("\n");
        var i = 0;
        if (lines[0] && lines[0].trim() === "---") {
          i = 1;
          while (i < lines.length && lines[i].trim() !== "---") i++;
          i++;
        }
        var body = lines.slice(i).join("\n");
        var sections = body.split(/\n(?=### )/).map(function(s) {
          var sl = s.split("\n");
          return { label: sl[0].replace(/^###\s*/, "").trim(), body: sl.slice(1).join("\n").trim() };
        }).filter(function(s) { return s.label; });
        if (!sections.length) {
          placeholder.innerHTML = "<div class='lc-tabs' style='padding:1em;color:#c00'>⚠️ No ### sections found in " + escapeHtml(filePath) + ".md</div>";
          return;
        }
        loadMarked(function() {
          var bar = sections.map(function(s, i) {
            return "<button class=\"lc-tab-btn" + (i===0?" active":"") + "\" data-tab=\"" + gid + "-" + i + "\">" + escapeHtml(s.label) + "</button>";
          }).join("");
          var panels = sections.map(function(s, i) {
            return "<div id=\"" + gid + "-" + i + "\" class=\"lc-tab-panel" + (i===0?" active":"") + "\">" + marked.parse(s.body) + "</div>";
          }).join("");
          var wrap = document.createElement("div");
          wrap.className = "lc-tabs";
          wrap.innerHTML = "<div class=\"lc-tab-bar\">" + bar + "</div>" + panels;
          wrap.querySelectorAll(".lc-tab-btn").forEach(function(b) {
            b.addEventListener("click", function() {
              wrap.querySelectorAll(".lc-tab-btn").forEach(function(x) { x.classList.remove("active"); });
              wrap.querySelectorAll(".lc-tab-panel").forEach(function(x) { x.classList.remove("active"); });
              b.classList.add("active");
              document.getElementById(b.dataset.tab).classList.add("active");
            });
          });
          placeholder.parentNode.replaceChild(wrap, placeholder);
        });
      })
      .catch(function(e) {
        placeholder.innerHTML = "<div class='lc-tabs' style='padding:1em;color:#c00'>⚠️ " + escapeHtml(e.message) + "</div>";
      });
  }

  function upgradeRadio(el) {
    var sections = parseSections(el);
    if (!sections.length) return;
    var gid = el.id || ("lc-rg-" + Math.random().toString(36).slice(2, 7));
    loadMarked(function() {
      var radios = sections.map(function(s, i){
        return "<label><input type=\"radio\" name=\"" + gid + "\" data-target=\"" + gid + "-" + i + "\"" + (i===0?" checked":"") + "> " + s.label + "</label>";
      }).join("");
      var panels = sections.map(function(s, i){
        return "<div id=\"" + gid + "-" + i + "\" class=\"lc-radio-content" + (i===0?" active":"") + "\">" + markdownBody(s.body) + "</div>";
      }).join("");
      var wrap = document.createElement("div");
      wrap.className = "lc-radio-group";
      wrap.innerHTML = "<div class=\"lc-radio-options\">" + radios + "</div><div class=\"lc-radio-body\">" + panels + "</div>";
      wrap.querySelectorAll("input[type=radio]").forEach(function(r){
        r.addEventListener("change", function(){
          wrap.querySelectorAll(".lc-radio-content").forEach(function(x){x.classList.remove("active");});
          document.getElementById(r.dataset.target).classList.add("active");
        });
      });
      el.parentNode.replaceChild(wrap, el);
    });
  }

  function upgradeGrid(el) {
    var sections = parseSections(el);
    if (!sections.length) return;
    var cols = el.getAttribute("cols") || "auto";
    var gap = el.getAttribute("gap") || "18";
    var hideHeadings = el.getAttribute("headings") === "hide";
    var tpl = cols === "auto" ? "repeat(auto-fit,minmax(280px,1fr))" : "repeat(" + cols + ",1fr)";
    loadMarked(function() {
      var cells = sections.map(function(s){
        var h = hideHeadings ? "" : "<h3>" + s.label + "</h3>";
        return "<div class=\"lc-grid-cell\">" + h + markdownBody(s.body) + "</div>";
      }).join("");
      var wrap = document.createElement("div");
      wrap.className = "lc-grid";
      wrap.style.gridTemplateColumns = tpl;
      wrap.style.gap = gap + "px";
      wrap.innerHTML = cells;
      el.parentNode.replaceChild(wrap, el);
    });
  }


  function upgradeCards(el) {
    var sections = parseSections(el);
    if (!sections.length) return;
    var cols = el.getAttribute("cols") || "auto";
    var gap = el.getAttribute("gap") || "18";
    var colStyle = cols === "auto"
      ? "repeat(auto-fit, minmax(240px, 1fr))"
      : "repeat(" + cols + ", 1fr)";
    var wrap = document.createElement("div");
    wrap.className = "lc-cards";
    wrap.style.gridTemplateColumns = colStyle;
    wrap.style.gap = gap + "px";
    el.parentNode.replaceChild(wrap, el);
    loadMarked(function() {
      wrap.innerHTML = sections.map(function(s) {
        return "<div class=\"lc-card\"><h3>" + s.label + "</h3>" + markdownBody(s.body) + "</div>";
      }).join("");
    });
  }

  /* ── boot ────────────────────────────────────────────── */
  /* code_chrome.md (loaded first, via topbar) provides the scan registry. */

  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader(".highlighter-rouge.accordion, pre.accordion", upgradeAccordion);
    window.lcRegisterUpgrader(".highlighter-rouge.tabs, pre.tabs", upgradeTabsInline);
    window.lcRegisterUpgrader("p.tabs", upgradeTabsFile);
    window.lcRegisterUpgrader(".highlighter-rouge.radio, pre.radio", upgradeRadio);
    window.lcRegisterUpgrader(".highlighter-rouge.grid, pre.grid", upgradeGrid);
    window.lcRegisterUpgrader(".highlighter-rouge.cards, pre.cards", upgradeCards);
  }

})();
</script>
