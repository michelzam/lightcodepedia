{%- comment -%}
Nodes — the LightNode network map: a D3 force-directed graph of the
template repository's fork network. Activated by IAL: {: .lightnodes }.

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<script>
(function () {
  if (window._lcNodesReady) return;
  window._lcNodesReady = true;

  // ── LightNode network graph (D3 force-directed fork map) ───────────────────
  function loadD3(cb) {
    if (window.d3) { cb(); return; }
    var s = document.createElement("script");
    s.src = "https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js";
    s.onload = cb;
    s.onerror = function() {
      var st = document.getElementById("lc-nodes-status");
      if (st) st.textContent = "⚠️ Could not load the graph library.";
    };
    document.head.appendChild(s);
  }

  function upgradeNodes(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    var OWNER     = el.getAttribute("owner")  || "michelzam";
    var REPO      = el.getAttribute("repo")   || "lightcodepedia";
    var MAX_DEPTH = parseInt(el.getAttribute("depth")  || "3",   10);
    var H         = parseInt(el.getAttribute("height") || "580", 10);

    var wrap = document.createElement("div");
    wrap.id = "lc-nodes-wrap";
    wrap.style.cssText = "position:relative;margin:1.5em 0";
    wrap.innerHTML = [
      '<style>',
      '.lc-node{transition:opacity .15s}',
      '.lc-node:hover{opacity:.85}',
      '.lc-node-label{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;pointer-events:none}',
      '.lc-link{transition:opacity .2s}',
      '</style>',
      '<svg id="lc-nodes-svg" style="width:100%;height:' + H + 'px;border-radius:14px;background:linear-gradient(135deg,#eef2ff 0%,#f0f9ff 100%);display:block"></svg>',
      '<div id="lc-nodes-tooltip" style="display:none;position:absolute;background:rgba(0,0,0,.72);color:#fff;border-radius:6px;padding:5px 10px;font-size:0.78em;pointer-events:none;white-space:nowrap"></div>',
      '<div id="lc-nodes-popup" style="display:none;position:absolute;background:#fff;border:1px solid #ddd;border-radius:12px;padding:16px;box-shadow:0 8px 32px rgba(0,0,0,.15);min-width:220px;z-index:20">',
      '  <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px">',
      '    <img id="lc-np-avatar" src="" alt="" style="width:42px;height:42px;border-radius:50%;flex-shrink:0">',
      '    <div style="min-width:0">',
      '      <div id="lc-np-login" style="font-weight:700;font-size:0.95em"></div>',
      '      <div id="lc-np-stats" style="font-size:0.78em;color:#888;margin-top:2px"></div>',
      '    </div>',
      '    <button onclick="document.getElementById(\'lc-nodes-popup\').style.display=\'none\'" style="margin-left:auto;background:none;border:none;cursor:pointer;font-size:1.3em;color:#bbb;line-height:1;padding:0;flex-shrink:0">×</button>',
      '  </div>',
      '  <a id="lc-np-site" href="#" target="_blank" rel="noopener" style="display:flex;align-items:center;gap:8px;padding:9px 12px;border:1px solid #0066cc;border-radius:8px;text-decoration:none;color:#0066cc;font-size:0.85em;margin-bottom:8px;font-weight:500">',
      '    <span>🌐</span><span>Visit LightNode</span><span style="margin-left:auto;font-size:0.85em;opacity:.6">↗</span>',
      '  </a>',
      '  <a id="lc-np-profile" href="#" target="_blank" rel="noopener" style="display:flex;align-items:center;gap:8px;padding:9px 12px;border:1px solid #e0e0e0;border-radius:8px;text-decoration:none;color:#444;font-size:0.85em">',
      '    <span>👤</span><span>GitHub profile</span><span style="margin-left:auto;font-size:0.85em;opacity:.6">↗</span>',
      '  </a>',
      '</div>',
      '<div id="lc-nodes-status" style="text-align:center;color:#888;padding:1em;font-size:0.9em">⏳ Loading the LightNode network…</div>'
    ].join("");
    el.parentNode.replaceChild(wrap, el);

    loadD3(function() { runNodes(); });

    function runNodes() {
      var pat  = localStorage.getItem("lc_ed_pat") || "";
      var hdrs = { "X-GitHub-Api-Version": "2022-11-28", Accept: "application/vnd.github+json" };
      if (pat) hdrs["Authorization"] = "Bearer " + pat;

      var statusEl = document.getElementById("lc-nodes-status");
      var popup    = document.getElementById("lc-nodes-popup");

      var GRAPH_TTL = 3600000;
      var GRAPH_KEY = "lc_nodes_graph", GRAPH_TS_KEY = "lc_nodes_ts";

      var COLORS = ["#f5a623", "#0066cc", "#2a9d2a", "#9b59b6", "#e74c3c"];
      function nodeColor(d) { return COLORS[Math.min(d.level, COLORS.length - 1)]; }

      function apiFetch(url) {
        return fetch(url, { headers: hdrs }).then(function (r) {
          var rem = parseInt(r.headers.get("X-RateLimit-Remaining") || "-1", 10);
          if (rem >= 0) localStorage.setItem("lc_rate_remaining", String(rem));
          if (!r.ok) throw new Error("GitHub API " + r.status + (rem >= 0 ? " (" + rem + " calls left)" : ""));
          return r.json();
        });
      }
      function setStatus(msg) { if (statusEl) statusEl.textContent = msg; }
      function clearStatus()  { if (statusEl) statusEl.textContent = ""; }

      document.addEventListener("click", function (e) {
        if (popup && !popup.contains(e.target)) popup.style.display = "none";
      });

      function rootNode() {
        return {
          id: OWNER + "/" + REPO, login: OWNER,
          avatar: "https://github.com/" + OWNER + ".png",
          level: 0, forkCount: 0, stars: 0, pinned: true
        };
      }

      function buildGraph() {
        var nodes = {}, links = [], rootId = OWNER + "/" + REPO;
        nodes[rootId] = rootNode();
        return Promise.all([
          apiFetch("https://api.github.com/users/" + OWNER).catch(function () { return null; }),
          apiFetch("https://api.github.com/repos/" + OWNER + "/" + REPO).catch(function () { return null; })
        ])
        .then(function (results) {
          var ownerUser = results[0], rootRepo = results[1];
          if (ownerUser && ownerUser.avatar_url) nodes[rootId].avatar = ownerUser.avatar_url;
          if (rootRepo) {
            nodes[rootId].forkCount = rootRepo.forks_count || 0;
            nodes[rootId].stars     = rootRepo.stargazers_count || 0;
          }
          var wave = [{ id: rootId, depth: 0 }];
          function processWave(currentWave) {
            if (!currentWave.length) return;
            var nextWave = [];
            setStatus("⏳ Scanning depth " + (currentWave[0].depth + 1) + "… (" + Object.keys(nodes).length + " nodes)");
            var fetches = currentWave
              .filter(function (w) { return w.depth < MAX_DEPTH; })
              .map(function (w) {
                return apiFetch("https://api.github.com/repos/" + w.id + "/forks?per_page=100&sort=newest")
                  .then(function (forks) {
                    if (nodes[w.id]) nodes[w.id].forkCount = forks.length;
                    forks.forEach(function (f) {
                      if (!nodes[f.full_name]) {
                        nodes[f.full_name] = {
                          id: f.full_name, login: f.owner.login, avatar: f.owner.avatar_url,
                          level: w.depth + 1, forkCount: f.forks_count || 0,
                          stars: f.stargazers_count || 0, pinned: false
                        };
                        links.push({ source: w.id, target: f.full_name });
                        if (f.forks_count > 0 && w.depth + 1 < MAX_DEPTH) {
                          nextWave.push({ id: f.full_name, depth: w.depth + 1 });
                        }
                      }
                    });
                  }).catch(function () {});
              });
            return Promise.all(fetches).then(function () { return processWave(nextWave); });
          }
          return processWave(wave);
        })
        .then(function () { return { nodes: Object.values(nodes), links: links }; });
      }

      var _cachedGraph = null, _cachedTs = parseInt(localStorage.getItem(GRAPH_TS_KEY) || "0", 10);
      try { _cachedGraph = JSON.parse(localStorage.getItem(GRAPH_KEY) || "null"); } catch (e) {}
      var _cacheUsable = _cachedGraph && _cachedGraph.nodes && _cachedGraph.nodes.length > 0;

      if (_cacheUsable && (Date.now() - _cachedTs) < GRAPH_TTL) {
        var _ageMin = Math.round((Date.now() - _cachedTs) / 60000);
        render(_cachedGraph.nodes, _cachedGraph.links);
        if (statusEl) { statusEl.textContent = "📦 cached · " + _ageMin + "m ago — refresh after 1h for live data"; statusEl.style.display = "block"; }
      } else {
        buildGraph()
          .then(function (graph) {
            if (!graph.nodes || !graph.nodes.length) graph = { nodes: [rootNode()], links: [] };
            try { localStorage.setItem(GRAPH_KEY, JSON.stringify(graph)); } catch (e) {}
            localStorage.setItem(GRAPH_TS_KEY, String(Date.now()));
            render(graph.nodes, graph.links);
            if (graph.nodes.length <= 1 && statusEl) {
              statusEl.style.display = "block";
              statusEl.textContent = pat
                ? "No forks yet — be the first to fork and grow the network!"
                : "🔑 Log in (top-right) to load the full network — GitHub limits anonymous requests.";
            } else { clearStatus(); }
          })
          .catch(function (e) {
            if (_cacheUsable) {
              render(_cachedGraph.nodes, _cachedGraph.links);
              setStatus("⚠️ Using cached graph — " + e.message);
            } else {
              render([rootNode()], []);
              if (statusEl) { statusEl.style.display = "block"; statusEl.textContent = "⚠️ " + e.message + (pat ? "" : " — log in (top-right) for the full network."); }
            }
          });
      }

      function showPopup(event, d) {
        var box     = wrap.getBoundingClientRect();
        var siteUrl = d.level === 0
          ? "https://lightcodepedia.org"
          : "https://" + d.login + ".github.io/lightcodepedia";
        var px = event.clientX - box.left + 16;
        var py = event.clientY - box.top  - 16;
        if (px + 240 > box.width)  px = event.clientX - box.left - 256;
        if (py + 180 > box.height) py = event.clientY - box.top  - 170;
        popup.style.left = Math.max(4, px) + "px";
        popup.style.top  = Math.max(4, py) + "px";
        var stats = [];
        if (d.stars     > 0) stats.push("⭐ " + d.stars);
        if (d.forkCount > 0) stats.push("🍴 " + d.forkCount);
        if (d.level     > 0) stats.push("depth " + d.level);
        document.getElementById("lc-np-avatar").src        = d.avatar;
        document.getElementById("lc-np-login").textContent = "@" + d.login;
        document.getElementById("lc-np-stats").textContent = stats.join(" · ");
        document.getElementById("lc-np-site").href         = siteUrl;
        document.getElementById("lc-np-profile").href      = "https://github.com/" + d.login;
        popup.style.display = "block";
      }

      function render(nodes, links) {
        var W   = wrap.offsetWidth || 900;
        var svg = d3.select("#lc-nodes-svg").attr("viewBox", "0 0 " + W + " " + H);
        svg.on("click", function () { popup.style.display = "none"; });
        var defs = svg.append("defs");
        nodes.forEach(function (d) {
          defs.append("clipPath").attr("id", "lc-clip-" + d.login)
            .append("circle").attr("r", radius(d));
        });
        function radius(d) { return d.level === 0 ? 36 : Math.max(16, 28 - d.level * 4); }
        var sim = d3.forceSimulation(nodes)
          .force("link", d3.forceLink(links).id(function (d) { return d.id; })
            .distance(function (l) { return 120 + l.source.level * 30; }).strength(0.6))
          .force("charge", d3.forceManyBody().strength(function (d) { return d.level === 0 ? -700 : -300; }))
          .force("center",  d3.forceCenter(W / 2, H / 2))
          .force("collide", d3.forceCollide().radius(function (d) { return radius(d) + 10; }))
          .alphaDecay(0.012);
        var root = nodes.find(function (d) { return d.level === 0; });
        if (root) { root.fx = W / 2; root.fy = H / 2; }
        var link = svg.append("g").selectAll("line").data(links).join("line")
          .attr("class", "lc-link")
          .attr("stroke", function (d) { return nodeColor(d.source); })
          .attr("stroke-width", function (d) { return d.source.level === 0 ? 1.8 : 1.2; })
          .attr("stroke-dasharray", "5 3").attr("opacity", 0.5);
        var node = svg.append("g").selectAll("g").data(nodes).join("g")
          .attr("class", "lc-node").attr("cursor", "pointer")
          .on("click", function (event, d) { event.stopPropagation(); showPopup(event, d); })
          .call(dragBehavior(sim));
        node.append("circle").attr("r", function (d) { return radius(d) + 6; })
          .attr("fill", nodeColor).attr("opacity", 0.1);
        node.append("circle").attr("r", radius).attr("fill", "#fff")
          .attr("stroke", nodeColor).attr("stroke-width", 2.5);
        node.append("image")
          .attr("href",   function (d) { return d.avatar; })
          .attr("x",      function (d) { return -radius(d); })
          .attr("y",      function (d) { return -radius(d); })
          .attr("width",  function (d) { return radius(d) * 2; })
          .attr("height", function (d) { return radius(d) * 2; })
          .attr("clip-path", function (d) { return "url(#lc-clip-" + d.login + ")"; })
          .attr("preserveAspectRatio", "xMidYMid slice");
        node.append("text").attr("class", "lc-node-label")
          .attr("y", function (d) { return radius(d) + 14; }).attr("text-anchor", "middle")
          .attr("font-size", function (d) { return d.level === 0 ? "13px" : Math.max(9, 11 - d.level) + "px"; })
          .attr("fill", "#333").attr("font-weight", function (d) { return d.level === 0 ? "700" : "400"; })
          .text(function (d) { return "@" + d.login; });
        node.filter(function (d) { return d.stars > 0; })
          .append("text").attr("class", "lc-node-label")
          .attr("y", function (d) { return radius(d) + 25; }).attr("text-anchor", "middle")
          .attr("font-size", "9px").attr("fill", "#c47900")
          .text(function (d) { return "⭐ " + d.stars; });
        var tip = d3.select("#lc-nodes-tooltip");
        node
          .on("mouseenter", function (event, d) {
            var parts = ["@" + d.login];
            if (d.stars)     parts.push("⭐ " + d.stars);
            if (d.forkCount) parts.push("🍴 " + d.forkCount);
            tip.style("display", "block").text(parts.join("  "));
          })
          .on("mousemove", function (event) {
            var box = wrap.getBoundingClientRect();
            tip.style("left", (event.clientX - box.left + 14) + "px")
               .style("top",  (event.clientY - box.top  - 32) + "px");
          })
          .on("mouseleave", function () { tip.style("display", "none"); });
        sim.on("tick", function () {
          link.attr("x1", function (d) { return d.source.x; })
              .attr("y1", function (d) { return d.source.y; })
              .attr("x2", function (d) { return d.target.x; })
              .attr("y2", function (d) { return d.target.y; });
          node.attr("transform", function (d) {
            var r = radius(d) + 10;
            d.x = Math.max(r, Math.min(W - r, d.x));
            d.y = Math.max(r, Math.min(H - r, d.y));
            return "translate(" + d.x + "," + d.y + ")";
          });
        });
      }

      function dragBehavior(sim) {
        return d3.drag()
          .on("start", function (event, d) {
            if (!event.active) sim.alphaTarget(0.35).restart();
            d.fx = d.x; d.fy = d.y;
          })
          .on("drag",  function (event, d) { d.fx = event.x; d.fy = event.y; })
          .on("end",   function (event, d) {
            if (!event.active) sim.alphaTarget(0);
            if (!d.pinned) { d.fx = null; d.fy = null; }
          });
      }
    }
  }

  /* ── boot ────────────────────────────────────────────────────── */
  /* code_chrome.md (loaded first, via topbar) provides the scan registry. */

  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader("p.lightnodes", upgradeNodes);
  }

})();
</script>
