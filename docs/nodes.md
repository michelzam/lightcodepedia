---
title: LightNode Network
---
# 🌐 LightNode Network

Every circle is a LightNode — a fork of Lightcodepedia hosted by a community member. Drag to rearrange. Click any node to visit their site. The network grows every time someone completes the [onboarding](/start).

<div id="lc-nodes-wrap" style="position:relative;margin:1.5em 0">
  <svg id="lc-nodes-svg" style="width:100%;height:580px;border-radius:14px;background:linear-gradient(135deg,#eef2ff 0%,#f0f9ff 100%);display:block"></svg>
  <div id="lc-nodes-tooltip" style="display:none;position:absolute;background:#fff;border:1px solid #ddd;border-radius:8px;padding:8px 12px;font-size:0.82em;pointer-events:none;box-shadow:0 4px 16px rgba(0,0,0,.1);max-width:180px;line-height:1.5"></div>
  <div id="lc-nodes-status" style="text-align:center;color:#888;padding:1em;font-size:0.9em">⏳ Loading the LightNode network…</div>
</div>

<style>
.lc-node { transition: opacity 0.15s; }
.lc-node:hover { opacity: 0.85; }
.lc-node-label { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; pointer-events: none; }
.lc-link { transition: opacity 0.2s; }
</style>

<script src="https://d3js.org/d3.v7.min.js"></script>
<script>
(function () {
  var pat  = localStorage.getItem('lc_ed_pat') || '';
  var hdrs = { 'X-GitHub-Api-Version': '2022-11-28', Accept: 'application/vnd.github+json' };
  if (pat) hdrs['Authorization'] = 'Bearer ' + pat;

  var OWNER     = 'michelzam';
  var REPO      = 'lightcodepedia';
  var MAX_DEPTH = 3;   // scan forks-of-forks up to this depth
  var statusEl  = document.getElementById('lc-nodes-status');

  function apiFetch(url) {
    return fetch(url, { headers: hdrs }).then(function (r) {
      if (!r.ok) throw new Error('GitHub API ' + r.status);
      return r.json();
    });
  }
  function setStatus(msg) { if (statusEl) statusEl.textContent = msg; }
  function clearStatus()  { if (statusEl) statusEl.textContent = ''; }

  // ── BFS fork traversal ────────────────────────────────────────────────────
  // Visits every reachable fork up to MAX_DEPTH, collecting nodes + links.
  // Rate-limit friendly: fetches in waves (all nodes at depth d before d+1).
  function buildGraph() {
    var nodes   = {};   // id → node object
    var links   = [];
    var rootId  = OWNER + '/' + REPO;

    return apiFetch('https://api.github.com/users/' + OWNER)
      .then(function (ownerUser) {
        nodes[rootId] = {
          id: rootId, login: OWNER, avatar: ownerUser.avatar_url,
          level: 0, forkCount: 0, pinned: true
        };

        // BFS wave: list of { repoFullName, depth }
        var wave = [{ id: rootId, depth: 0 }];

        function processWave(currentWave) {
          if (!currentWave.length) return;
          var nextWave = [];
          setStatus('⏳ Scanning depth ' + (currentWave[0].depth + 1) + '…  (' + Object.keys(nodes).length + ' nodes so far)');

          // fetch forks for all nodes in this wave in parallel
          var fetches = currentWave
            .filter(function (w) { return w.depth < MAX_DEPTH; })
            .map(function (w) {
              return apiFetch(
                'https://api.github.com/repos/' + w.id + '/forks?per_page=100&sort=newest'
              ).then(function (forks) {
                // update parent forkCount
                if (nodes[w.id]) nodes[w.id].forkCount = forks.length;
                forks.forEach(function (f) {
                  if (!nodes[f.full_name]) {
                    nodes[f.full_name] = {
                      id: f.full_name,
                      login: f.owner.login,
                      avatar: f.owner.avatar_url,
                      level: w.depth + 1,
                      forkCount: f.forks_count || 0,
                      pinned: false
                    };
                    links.push({ source: w.id, target: f.full_name });
                    if (f.forks_count > 0 && w.depth + 1 < MAX_DEPTH) {
                      nextWave.push({ id: f.full_name, depth: w.depth + 1 });
                    }
                  }
                });
              }).catch(function () { /* skip unreachable repos silently */ });
            });

          return Promise.all(fetches).then(function () {
            return processWave(nextWave);
          });
        }

        return processWave(wave);
      })
      .then(function () {
        return { nodes: Object.values(nodes), links: links };
      });
  }

  buildGraph()
    .then(function (graph) {
      clearStatus();
      render(graph.nodes, graph.links);
    })
    .catch(function (e) {
      setStatus('⚠️ Could not load network: ' + e.message +
                (pat ? '' : ' — log in for higher rate limits.'));
    });

  // ── colour scale by depth ─────────────────────────────────────────────────
  var COLORS  = ['#f5a623', '#0066cc', '#2a9d2a', '#9b59b6', '#e74c3c'];
  function nodeColor(d) { return COLORS[Math.min(d.level, COLORS.length - 1)]; }

  // ── D3 render ─────────────────────────────────────────────────────────────
  function render(nodes, links) {
    var wrap = document.getElementById('lc-nodes-wrap');
    var W    = wrap.offsetWidth || 900;
    var H    = 580;
    var svg  = d3.select('#lc-nodes-svg').attr('viewBox', '0 0 ' + W + ' ' + H);

    // clip paths for circular avatars
    var defs = svg.append('defs');
    nodes.forEach(function (d) {
      var r = d.level === 0 ? 36 : Math.max(16, 28 - d.level * 4);
      defs.append('clipPath')
        .attr('id', 'lc-clip-' + d.login)
        .append('circle').attr('r', r);
    });

    function radius(d) { return d.level === 0 ? 36 : Math.max(16, 28 - d.level * 4); }

    // ── simulation ────────────────────────────────────────────────────────
    var sim = d3.forceSimulation(nodes)
      .force('link',
        d3.forceLink(links)
          .id(function (d) { return d.id; })
          .distance(function (l) { return 120 + l.source.level * 30; })
          .strength(0.6)
      )
      .force('charge', d3.forceManyBody().strength(function (d) {
        return d.level === 0 ? -700 : -300;
      }))
      .force('center', d3.forceCenter(W / 2, H / 2))
      .force('collide',
        d3.forceCollide().radius(function (d) { return radius(d) + 10; })
      )
      .alphaDecay(0.012);

    // pin root
    var root = nodes.find(function (d) { return d.level === 0; });
    if (root) { root.fx = W / 2; root.fy = H / 2; }

    // ── links ─────────────────────────────────────────────────────────────
    var link = svg.append('g')
      .selectAll('line').data(links).join('line')
      .attr('class', 'lc-link')
      .attr('stroke', function (d) { return nodeColor(d.source); })
      .attr('stroke-width', function (d) {
        return d.source.level === 0 ? 1.8 : 1.2;
      })
      .attr('stroke-dasharray', '5 3')
      .attr('opacity', 0.5);

    // ── node groups ───────────────────────────────────────────────────────
    var node = svg.append('g')
      .selectAll('g').data(nodes).join('g')
      .attr('class', 'lc-node')
      .attr('cursor', 'pointer')
      .on('click', function (event, d) {
        var url = d.level === 0
          ? 'https://lightcodepedia.org'
          : 'https://' + d.login + '.github.io/lightcodepedia';
        window.open(url, '_blank');
      })
      .call(dragBehavior(sim));

    // glow halo
    node.append('circle')
      .attr('r', function (d) { return radius(d) + 6; })
      .attr('fill', nodeColor)
      .attr('opacity', 0.1);

    // white backing circle
    node.append('circle')
      .attr('r', radius)
      .attr('fill', '#fff')
      .attr('stroke', nodeColor)
      .attr('stroke-width', 2.5);

    // avatar image
    node.append('image')
      .attr('href', function (d) { return d.avatar; })
      .attr('x', function (d) { return -radius(d); })
      .attr('y', function (d) { return -radius(d); })
      .attr('width',  function (d) { return radius(d) * 2; })
      .attr('height', function (d) { return radius(d) * 2; })
      .attr('clip-path', function (d) { return 'url(#lc-clip-' + d.login + ')'; })
      .attr('preserveAspectRatio', 'xMidYMid slice');

    // username label
    node.append('text')
      .attr('class', 'lc-node-label')
      .attr('y', function (d) { return radius(d) + 14; })
      .attr('text-anchor', 'middle')
      .attr('font-size', function (d) { return d.level === 0 ? '13px' : Math.max(9, 11 - d.level) + 'px'; })
      .attr('fill', '#333')
      .attr('font-weight', function (d) { return d.level === 0 ? '700' : '400'; })
      .text(function (d) { return '@' + d.login; });

    // depth badge for sub-sub-forks
    node.filter(function (d) { return d.level > 1; })
      .append('text')
      .attr('class', 'lc-node-label')
      .attr('y', function (d) { return radius(d) + 25; })
      .attr('text-anchor', 'middle')
      .attr('font-size', '9px')
      .attr('fill', '#aaa')
      .text(function (d) { return 'depth ' + d.level; });

    // ── tooltip ───────────────────────────────────────────────────────────
    var tip = d3.select('#lc-nodes-tooltip');
    node
      .on('mouseenter', function (event, d) {
        var siteUrl = d.level === 0
          ? 'lightcodepedia.org'
          : d.login + '.github.io/lightcodepedia';
        tip.style('display', 'block').html(
          '<strong>@' + d.login + '</strong><br>' +
          (d.forkCount > 0 ? '🍴 ' + d.forkCount + ' fork' + (d.forkCount !== 1 ? 's' : '') + '<br>' : '') +
          '<span style="color:#888">depth ' + d.level + ' · 🌐 ' + siteUrl + '</span>'
        );
      })
      .on('mousemove', function (event) {
        var box = wrap.getBoundingClientRect();
        tip
          .style('left', (event.clientX - box.left + 14) + 'px')
          .style('top',  (event.clientY - box.top  - 10) + 'px');
      })
      .on('mouseleave', function () { tip.style('display', 'none'); });

    // ── tick ──────────────────────────────────────────────────────────────
    sim.on('tick', function () {
      link
        .attr('x1', function (d) { return d.source.x; })
        .attr('y1', function (d) { return d.source.y; })
        .attr('x2', function (d) { return d.target.x; })
        .attr('y2', function (d) { return d.target.y; });
      node.attr('transform', function (d) {
        var r = radius(d) + 10;
        d.x = Math.max(r, Math.min(W - r, d.x));
        d.y = Math.max(r, Math.min(H - r, d.y));
        return 'translate(' + d.x + ',' + d.y + ')';
      });
    });
  }

  // ── drag with elastic release ──────────────────────────────────────────────
  function dragBehavior(sim) {
    return d3.drag()
      .on('start', function (event, d) {
        if (!event.active) sim.alphaTarget(0.35).restart();
        d.fx = d.x; d.fy = d.y;
      })
      .on('drag', function (event, d) {
        d.fx = event.x; d.fy = event.y;
      })
      .on('end', function (event, d) {
        if (!event.active) sim.alphaTarget(0);
        if (!d.pinned) { d.fx = null; d.fy = null; }
      });
  }

})();
</script>

{% include backtotop.md %}
