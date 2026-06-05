{%- comment -%}
Sitemap — force-directed graph of page links within a directory.
Fetches pages from the GitHub API, extracts internal Markdown links,
and renders an interactive SVG graph. Nodes are tinted by feature status.

Usage:
  [Browse](/docs/components)
  {: .sitemap path="docs/components" height="460" }

Attributes:
  path="…"     GitHub repo path to scan (required, use the link href)
  height="…"   SVG canvas height in px (default: 420)
{%- endcomment -%}

<style>
.lc-sitemap { position: relative; border: 1px solid #e5e7eb; border-radius: 8px; overflow: hidden; background: #fafafa; }
.lc-sitemap svg { display: block; width: 100%; }
.lc-sm-edge { stroke: #d1d5db; stroke-width: 1.5; }
.lc-sm-node circle { fill: #fff; stroke: #9ca3af; stroke-width: 1.5; cursor: pointer; }
.lc-sm-node circle:hover { stroke: #0066cc; stroke-width: 2.5; }
.lc-sm-label { font: 11px/1.3 ui-sans-serif,system-ui,sans-serif; fill: #374151; text-anchor: middle; pointer-events: none; }
.lc-sm-tip { position: absolute; background: #1e1e2e; color: #cdd6f4; padding: .4em .7em; border-radius: 6px; font-size: .78em; line-height: 1.45; max-width: 200px; pointer-events: none; z-index: 10; opacity: 0; transition: opacity .15s; }
.lc-sm-tip.on { opacity: 1; }
.lc-sm-tip-dots { display: flex; gap: 4px; margin-top: 4px; }
.lc-sm-msg { display: flex; align-items: center; justify-content: center; height: 100%; color: #9ca3af; font-size: .85em; }
</style>

<script>
(function () {

  var _repo = {{ site.github.repository_nwo | default: "" | jsonify }};

  /* ── helpers shared with folder (if already defined, reuse) ── */
  function smExtractMeta(text) {
    var lines = text.split("\n"), i = 0;
    if (lines[0] && lines[0].trim() === "---") {
      i = 1; while (i < lines.length && lines[i].trim() !== "---") i++; i++;
    }
    var title = null, snippet = "";
    for (; i < lines.length; i++) {
      var l = lines[i].trim();
      if (!title && /^#{1,2}\s/.test(l)) { title = l.replace(/^#+\s+/, ""); continue; }
      if (title && l && !/^[#{`\->|]/.test(l) && !/^\{:/.test(l)) {
        snippet = l.replace(/\[([^\]]*)\]\([^)]*\)/g, "$1").replace(/[*_`]/g, "").trim().substring(0, 100);
        break;
      }
    }
    return { title: title, snippet: snippet };
  }

  function smExtractLinks(text) {
    var clean = text.replace(/(`{3,})[^\n]*\n[\s\S]*?\1/g, "").replace(/`[^`\n]+`/g, "");
    var out = [], re = /\]\(([^)#\s]+)/g, m;
    while ((m = re.exec(clean)) !== null) {
      var h = m[1]; if (/^https?:|^mailto:/.test(h)) continue; out.push(h);
    }
    return out;
  }

  function smResolve(href, baseSlug) {
    if (/^\//.test(href)) return href.replace(/^\//, "").replace(/^docs\//, "").replace(/\.md$/i, "");
    var parts = baseSlug.split("/"); parts.pop();
    href.split("/").forEach(function (p) { if (p === "..") parts.pop(); else if (p && p !== ".") parts.push(p); });
    return parts.join("/").replace(/\.md$/i, "");
  }

  function smFeatureCounts(text) {
    var clean = text.replace(/(`{3,})[^\n]*\n[\s\S]*?\1/g, "").replace(/`[^`\n]+`/g, "``");
    var c = {}, re = /\{:\s*\.feature\b([^}]*)\}/g, m;
    while ((m = re.exec(clean)) !== null) {
      var s = (m[1].match(/\bstatus="(\w+)"/) || [])[1] || "none";
      c[s] = (c[s] || 0) + 1;
    }
    return c;
  }

  /* ── force simulation ─────────────────────────────────── */
  function simulate(nodes, edges, W, H) {
    var REPEL = 4000, ATT = 0.045, REST = 130, DAMP = 0.80, CEN = 0.016;
    var alpha = 1.0;
    var cx = W / 2, cy = H / 2;
    function tick() {
      alpha *= 0.984;
      for (var i = 0; i < nodes.length; i++) {
        for (var j = i + 1; j < nodes.length; j++) {
          var dx = (nodes[j].x - nodes[i].x) || 0.01, dy = (nodes[j].y - nodes[i].y) || 0.01;
          var d = Math.sqrt(dx * dx + dy * dy), f = REPEL / (d * d);
          var fx = f * dx / d, fy = f * dy / d;
          nodes[i].vx -= fx; nodes[i].vy -= fy; nodes[j].vx += fx; nodes[j].vy += fy;
        }
      }
      edges.forEach(function (e) {
        var dx = e.t.x - e.s.x, dy = e.t.y - e.s.y;
        var d = Math.sqrt(dx * dx + dy * dy) || 1, f = ATT * (d - REST);
        var fx = f * dx / d, fy = f * dy / d;
        if (!e.s.pin) { e.s.vx += fx; e.s.vy += fy; }
        if (!e.t.pin) { e.t.vx -= fx; e.t.vy -= fy; }
      });
      nodes.forEach(function (n) {
        if (n.pin) return;
        n.vx += (cx - n.x) * CEN * alpha; n.vy += (cy - n.y) * CEN * alpha;
        n.vx *= DAMP; n.vy *= DAMP;
        n.x = Math.max(n.r + 4, Math.min(W - n.r - 4, n.x + n.vx));
        n.y = Math.max(n.r + 4, Math.min(H - n.r - 18, n.y + n.vy));
      });
      return alpha;
    }
    return { tick: tick, setAlpha: function (v) { alpha = v; }, getAlpha: function () { return alpha; } };
  }

  /* ── render graph ─────────────────────────────────────── */
  function renderGraph(container, pages, H) {
    container.innerHTML = "";
    var tip = document.createElement("div"); tip.className = "lc-sm-tip"; container.appendChild(tip);

    var NS = "http://www.w3.org/2000/svg";
    var svg = document.createElementNS(NS, "svg"); svg.setAttribute("height", H); container.appendChild(svg);
    var W = container.clientWidth || 640;
    svg.setAttribute("viewBox", "0 0 " + W + " " + H);

    var slugSet = {}; pages.forEach(function (p) { slugSet[p.id] = true; });
    pages.forEach(function (p) {
      p.links = [];
      p.rawLinks.forEach(function (h) {
        var s = smResolve(h, p.id);
        if (slugSet[s] && s !== p.id) p.links.push(s);
      });
    });

    var nodeMap = {};
    var nodes = pages.map(function (p) {
      var n = { id: p.id, title: p.title, url: p.url, snippet: p.snippet, fc: p.fc,
        x: W / 2 + (Math.random() - 0.5) * 180, y: H / 2 + (Math.random() - 0.5) * 180,
        vx: 0, vy: 0, pin: false, r: 12 };
      nodeMap[p.id] = n; return n;
    });

    var edgeSet = {}, edges = [];
    pages.forEach(function (p) {
      p.links.forEach(function (tid) {
        var key = [p.id, tid].sort().join("|");
        if (!edgeSet[key] && nodeMap[tid]) { edgeSet[key] = true; edges.push({ s: nodeMap[p.id], t: nodeMap[tid] }); }
      });
    });

    /* size by degree */
    nodes.forEach(function (n) {
      var deg = edges.filter(function (e) { return e.s === n || e.t === n; }).length;
      n.r = 10 + Math.min(deg * 3, 14);
    });

    var eLayer = document.createElementNS(NS, "g"), nLayer = document.createElementNS(NS, "g");
    svg.appendChild(eLayer); svg.appendChild(nLayer);

    var edgeEls = edges.map(function (e) {
      var l = document.createElementNS(NS, "line"); l.setAttribute("class", "lc-sm-edge"); eLayer.appendChild(l); return l;
    });

    var sim = simulate(nodes, edges, W, H);
    var raf = null;

    var nodeEls = nodes.map(function (n) {
      var g = document.createElementNS(NS, "g"); g.setAttribute("class", "lc-sm-node");
      var c = document.createElementNS(NS, "circle"); c.setAttribute("r", n.r);
      if (n.fc.passing && !n.fc.failing) c.setAttribute("fill", "#f0fdf4");
      else if (n.fc.failing)              c.setAttribute("fill", "#fef2f2");
      else if (n.fc.pending)              c.setAttribute("fill", "#fffbeb");
      var lbl = document.createElementNS(NS, "text"); lbl.setAttribute("class", "lc-sm-label");
      lbl.setAttribute("dy", n.r + 13);
      lbl.textContent = n.title.length > 17 ? n.title.substring(0, 15) + "…" : n.title;
      g.appendChild(c); g.appendChild(lbl); nLayer.appendChild(g);

      /* drag */
      var ox, oy;
      c.addEventListener("mousedown", function (ev) {
        n.pin = true; ox = ev.clientX - n.x; oy = ev.clientY - n.y; ev.preventDefault();
      });
      document.addEventListener("mousemove", function (ev) {
        if (!n.pin) return;
        n.x = ev.clientX - ox; n.y = ev.clientY - oy;
        sim.setAlpha(Math.max(sim.getAlpha(), 0.25));
        if (!raf) loop();
      });
      document.addEventListener("mouseup", function () { n.pin = false; });

      /* tooltip */
      c.addEventListener("mouseenter", function (ev) {
        var fc = n.fc, dots = "";
        if (fc.passing) dots += "<span style='color:#86efac'>● " + fc.passing + "</span> ";
        if (fc.failing)  dots += "<span style='color:#fca5a5'>✗ " + fc.failing  + "</span> ";
        if (fc.pending)  dots += "<span style='color:#fcd34d'>◑ " + fc.pending  + "</span>";
        tip.innerHTML = "<strong>" + n.title + "</strong>" + (n.snippet ? "<br><span style='opacity:.7'>" + n.snippet + "</span>" : "")
          + (dots ? "<div class='lc-sm-tip-dots'>" + dots + "</div>" : "");
        tip.classList.add("on"); posTip(ev);
      });
      c.addEventListener("mousemove", posTip);
      c.addEventListener("mouseleave", function () { tip.classList.remove("on"); });
      c.addEventListener("click", function () { window.location.href = n.url; });
      return g;
    });

    function posTip(ev) {
      var r = container.getBoundingClientRect(), x = ev.clientX - r.left + 14, y = ev.clientY - r.top + 14;
      if (x + 215 > W) x -= 225;
      tip.style.left = x + "px"; tip.style.top = y + "px";
    }

    function draw() {
      edgeEls.forEach(function (el, i) {
        var e = edges[i];
        el.setAttribute("x1", e.s.x); el.setAttribute("y1", e.s.y);
        el.setAttribute("x2", e.t.x); el.setAttribute("y2", e.t.y);
      });
      nodeEls.forEach(function (g, i) {
        g.setAttribute("transform", "translate(" + nodes[i].x + "," + nodes[i].y + ")");
      });
    }

    function loop() {
      var a = sim.tick(); draw();
      raf = a > 0.008 ? requestAnimationFrame(loop) : null;
    }
    loop();

    new ResizeObserver(function () {
      W = container.clientWidth; svg.setAttribute("viewBox", "0 0 " + W + " " + H);
      sim.setAlpha(Math.max(sim.getAlpha(), 0.4));
      if (!raf) loop();
    }).observe(container);
  }

  /* ── upgrade a .sitemap element ──────────────────────── */
  function upgradeSitemap(el) {
    if (el.dataset.lcSmDone) return; el.dataset.lcSmDone = "1";
    var a = el.querySelector("a");
    var path = a ? a.getAttribute("href").replace(/^\/+|\/+$/g, "") : "";
    var H = parseInt(el.getAttribute("height") || "420", 10);
    if (!_repo || !path) { el.innerHTML = "<div class='lc-sm-msg'>⚠ set path</div>"; return; }
    el.style.height = H + "px";
    el.innerHTML = "<div class='lc-sm-msg'>Loading graph…</div>";

    var pat = localStorage.getItem("lc_ed_pat") || "";
    var hdrs = pat ? { Authorization: "Bearer " + pat, "X-GitHub-Api-Version": "2022-11-28" } : {};
    function apiFetch(url) { return fetch(url, { headers: hdrs }).then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); }); }

    apiFetch("https://api.github.com/repos/" + _repo + "/contents/" + path)
      .then(function (files) {
        if (!Array.isArray(files)) throw new Error("Not a directory");
        var pages = files.filter(function (f) { return f.type === "file" && /\.md$/i.test(f.name); });
        return Promise.all(pages.map(function (f) {
          var slug = f.path.replace(/^docs\//, "").replace(/\.md$/i, "");
          return fetch(f.download_url).then(function (r) { return r.text(); }).then(function (text) {
            var meta = smExtractMeta(text);
            return {
              id: slug, url: "/" + slug,
              title: meta.title || f.name.replace(/\.md$/i, "").replace(/[-_]/g, " ").replace(/\b\w/g, function (c) { return c.toUpperCase(); }),
              snippet: meta.snippet,
              rawLinks: smExtractLinks(text),
              fc: smFeatureCounts(text)
            };
          });
        }));
      })
      .then(function (pages) { renderGraph(el, pages, H); })
      .catch(function (e) { el.innerHTML = "<div class='lc-sm-msg'>⚠ " + e.message + "</div>"; });
  }

  /* ── boot ────────────────────────────────────────────── */
  function init(root) { (root || document).querySelectorAll(".sitemap").forEach(upgradeSitemap); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", function () { init(); });
  else init();

  var _os = window.lcScanElement;
  window.lcScanElement = function (root) { if (_os) _os(root); root.querySelectorAll(".sitemap").forEach(upgradeSitemap); };

})();
</script>
