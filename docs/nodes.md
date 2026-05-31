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

  var OWNER = 'michelzam';
  var REPO  = 'lightcodepedia';
  var statusEl = document.getElementById('lc-nodes-status');

  function apiFetch(url) {
    return fetch(url, { headers: hdrs }).then(function (r) {
      if (!r.ok) throw new Error('GitHub API returned ' + r.status);
      return r.json();
    });
  }

  function setStatus(msg) { if (statusEl) statusEl.textContent = msg; }
  function clearStatus()  { if (statusEl) statusEl.textContent = ''; }

  // ── fetch root owner + forks ──────────────────────────────────────────────
  Promise.all([
    apiFetch('https://api.github.com/users/' + OWNER),
    apiFetch('https://api.github.com/repos/' + OWNER + '/' + REPO + '/forks?per_page=100&sort=newest')
  ])
  .then(function (results) {
    var owner  = results[0];
    var forks  = results[1];
    var nodes  = [];
    var links  = [];
    var rootId = OWNER + '/' + REPO;

    nodes.push({
      id: rootId,
      login: OWNER,
      avatar: owner.avatar_url,
      level: 0,
      forkCount: forks.length,
      pinned: true
    });

    forks.forEach(function (f) {
      nodes.push({
        id: f.full_name,
        login: f.owner.login,
        avatar: f.owner.avatar_url,
        level: 1,
        forkCount: f.forks_count || 0,
        pinned: false
      });
      links.push({ source: rootId, target: f.full_name });
    });

    clearStatus();
    render(nodes, links);
  })
  .catch(function (e) {
    setStatus('⚠️ Could not load network: ' + e.message + (pat ? '' : ' — log in for higher rate limits.'));
  });

  // ── D3 render ─────────────────────────────────────────────────────────────
  function render(nodes, links) {
    var wrap = document.getElementById('lc-nodes-wrap');
    var W    = wrap.offsetWidth  || 900;
    var H    = 580;
    var svg  = d3.select('#lc-nodes-svg')
                 .attr('viewBox', '0 0 ' + W + ' ' + H);

    // clip paths for circular avatars
    var defs = svg.append('defs');
    nodes.forEach(function (d) {
      var r = d.level === 0 ? 36 : 24;
      defs.append('clipPath')
        .attr('id', 'lc-clip-' + d.login)
        .append('circle')
        .attr('r', r);
    });

    // ── simulation ────────────────────────────────────────────────────────
    var sim = d3.forceSimulation(nodes)
      .force('link',
        d3.forceLink(links)
          .id(function (d) { return d.id; })
          .distance(160)
          .strength(0.55)
      )
      .force('charge', d3.forceManyBody().strength(-500))
      .force('center',  d3.forceCenter(W / 2, H / 2))
      .force('collide',
        d3.forceCollide().radius(function (d) { return d.level === 0 ? 52 : 38; })
      )
      .alphaDecay(0.012);   // slow decay → long springy settling

    // pin root to centre
    var root = nodes.find(function (d) { return d.level === 0; });
    if (root) { root.fx = W / 2; root.fy = H / 2; }

    // ── links ─────────────────────────────────────────────────────────────
    var link = svg.append('g')
      .selectAll('line')
      .data(links)
      .join('line')
      .attr('class', 'lc-link')
      .attr('stroke', '#a0b4d8')
      .attr('stroke-width', 1.5)
      .attr('stroke-dasharray', '5 3')
      .attr('opacity', 0.65);

    // ── node groups ───────────────────────────────────────────────────────
    var node = svg.append('g')
      .selectAll('g')
      .data(nodes)
      .join('g')
      .attr('class', 'lc-node')
      .attr('cursor', 'pointer')
      .on('click', function (event, d) {
        var url = d.level === 0
          ? 'https://lightcodepedia.org'
          : 'https://' + d.login + '.github.io/lightcodepedia';
        window.open(url, '_blank');
      })
      .call(dragBehavior(sim));

    // glow ring (outermost)
    node.append('circle')
      .attr('r', function (d) { return d.level === 0 ? 42 : 29; })
      .attr('fill', function (d) { return d.level === 0 ? '#f5a623' : '#0066cc'; })
      .attr('opacity', 0.12);

    // white background circle
    node.append('circle')
      .attr('r', function (d) { return d.level === 0 ? 38 : 26; })
      .attr('fill', '#fff')
      .attr('stroke', function (d) { return d.level === 0 ? '#f5a623' : '#4a90d9'; })
      .attr('stroke-width', 2.5);

    // avatar image (clipped to circle)
    node.append('image')
      .attr('href', function (d) { return d.avatar; })
      .attr('x',   function (d) { return d.level === 0 ? -36 : -24; })
      .attr('y',   function (d) { return d.level === 0 ? -36 : -24; })
      .attr('width',  function (d) { return d.level === 0 ? 72 : 48; })
      .attr('height', function (d) { return d.level === 0 ? 72 : 48; })
      .attr('clip-path', function (d) { return 'url(#lc-clip-' + d.login + ')'; })
      .attr('preserveAspectRatio', 'xMidYMid slice');

    // username label
    node.append('text')
      .attr('class', 'lc-node-label')
      .attr('y',            function (d) { return d.level === 0 ? 54 : 38; })
      .attr('text-anchor',  'middle')
      .attr('font-size',    function (d) { return d.level === 0 ? '13px' : '11px'; })
      .attr('fill',         '#333')
      .attr('font-weight',  function (d) { return d.level === 0 ? '700' : '400'; })
      .text(function (d) { return '@' + d.login; });

    // fork count badge (shown for nodes that have sub-forks)
    node.filter(function (d) { return d.forkCount > 0; })
      .append('text')
      .attr('class', 'lc-node-label')
      .attr('y',           function (d) { return d.level === 0 ? 67 : 50; })
      .attr('text-anchor', 'middle')
      .attr('font-size',   '10px')
      .attr('fill',        '#888')
      .text(function (d) { return d.forkCount + ' fork' + (d.forkCount !== 1 ? 's' : ''); });

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
          '<span style="color:#888">🌐 ' + siteUrl + '</span>'
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
        d.x = Math.max(50, Math.min(W - 50, d.x));
        d.y = Math.max(50, Math.min(H - 50, d.y));
        return 'translate(' + d.x + ',' + d.y + ')';
      });
    });
  }

  // ── drag with elastic release ──────────────────────────────────────────────
  function dragBehavior(sim) {
    return d3.drag()
      .on('start', function (event, d) {
        if (!event.active) sim.alphaTarget(0.35).restart();
        d.fx = d.x;
        d.fy = d.y;
      })
      .on('drag', function (event, d) {
        d.fx = event.x;
        d.fy = event.y;
      })
      .on('end', function (event, d) {
        if (!event.active) sim.alphaTarget(0);
        if (!d.pinned) {
          // release fx/fy so simulation springs the node back to equilibrium
          d.fx = null;
          d.fy = null;
        }
      });
  }

})();
</script>

{% include backtotop.md %}
