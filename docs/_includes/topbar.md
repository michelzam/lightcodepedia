<script>
if (location.search.indexOf('embed=true') >= 0) {
  document.documentElement.classList.add('lc-embed-mode');
}
</script>
<style>
#lc-topbar {
  position: fixed;
  top: 0; left: 0; right: 0;
  height: 48px;
  background: rgba(255,255,255,0.95);
  border-bottom: 1px solid #ddd;
  display: flex;
  align-items: center;
  padding: 0 1.2rem;
  gap: 1.4rem;
  z-index: 1000;
  font-size: 0.9rem;
  backdrop-filter: blur(4px);
}
#lc-topbar .lc-brand {
  font-weight: bold;
  text-decoration: none;
  color: #333;
  margin-right: auto;
}
/* ── user pill ── */
#lc-user-pill { position: relative; flex-shrink: 0; }
#lc-user-btn {
  background: none; border: 1px solid #ddd; border-radius: 50%;
  padding: 2px; cursor: pointer; display: flex; align-items: center; line-height: 1;
}
#lc-user-btn:hover { border-color: #0066cc; box-shadow: 0 0 0 2px #e8f0fe; }
#lc-user-btn img { width: 28px; height: 28px; border-radius: 50%; display: block; }
#lc-user-caret { display: none; }
#lc-user-drop {
  display: none; position: absolute; right: 0; top: calc(100% + 6px);
  background: #fff; border: 1px solid #ddd; border-radius: 10px;
  box-shadow: 0 6px 24px rgba(0,0,0,.12); min-width: 220px; z-index: 2000;
  overflow: hidden;
}
#lc-user-drop.open { display: block; }
.lc-ud-head {
  display: flex; align-items: center; gap: 10px;
  padding: 14px 16px; border-bottom: 1px solid #eee; background: #fafafa;
}
.lc-ud-head img { width: 40px; height: 40px; border-radius: 50%; }
.lc-ud-name { font-weight: 600; font-size: 0.9em; line-height: 1.3; }
.lc-ud-login { font-size: 0.8em; color: #888; }
.lc-ud-karma-row {
  color: #b36a00; background: #fffbf0; justify-content: space-between;
  border-bottom: 1px solid #f0e8d0;
}
.lc-ud-karma-row:hover { background: #fff3d0; }
.lc-ud-karma-pts { font-weight: 700; }
.lc-ud-row {
  display: flex; align-items: center; gap: 8px;
  padding: 9px 16px; font-size: 0.85em; color: #333; text-decoration: none;
  border-bottom: 1px solid #f0f0f0; cursor: pointer;
}
.lc-ud-row:hover { background: #f5f5f5; }
.lc-ud-row:last-child { border-bottom: none; }
.lc-ud-row.danger { color: #c00; }
.lc-ud-repo { font-family: monospace; font-size: 0.8em; color: #555; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
#lc-start-pill {
  flex-shrink: 0; font-size: 0.82em; color: #0066cc;
  text-decoration: none; border: 1px solid #0066cc; border-radius: 20px;
  padding: 3px 10px; display: none;
}
#lc-start-pill:hover { background: #e8f0fe; }
@media (max-width: 700px) {
  #lc-user-btn .lc-user-login-label { display: none; }
  #lc-user-caret { display: none; }
}
#lc-topbar .lc-links { display: flex; gap: 1.2rem; }
#lc-topbar .lc-links p { margin: 0; }
#lc-topbar .lc-links a {
  text-decoration: none;
  color: #333;
  margin-right: 1rem;
}
#lc-topbar .lc-links a:hover { color: #0066cc; }
#lc-topbar .lc-link-icon { margin-right: 0.35em; }
@media (max-width: 700px) {
  #lc-topbar { padding: 0 0.7rem; gap: 0.8rem; }
  #lc-topbar .lc-link-label { display: none; }
  #lc-topbar .lc-link-icon { margin-right: 0; font-size: 1.15em; }
  #lc-topbar .lc-links a { margin-right: 0.5rem; }
}
body {
  padding-top: 56px;
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
  font-size: 16px;
  line-height: 1.5;
  color: #111;
  -webkit-font-smoothing: antialiased;
}
.markdown-body { max-width: 980px; margin: 0 auto; padding: 1em 1.2rem 2em; }
.markdown-body a { color: #2a7ae2; }
.markdown-body a:visited { color: #1756a9; }
.markdown-body code, .markdown-body pre { font-family: ui-monospace, "SFMono-Regular", Menlo, Consolas, "Liberation Mono", monospace; }
.markdown-body code { background: #eef; padding: 0.1em 0.35em; border-radius: 3px; font-size: 0.9em; }
.markdown-body pre code { background: transparent; padding: 0; }
.markdown-body pre:not([class*="lc-"]) { background: #f8f8f8; padding: 0.8em 1em; border-radius: 6px; overflow-x: auto; }
.markdown-body blockquote { border-left: 4px solid #ddd; padding: 0 1em; color: #555; margin: 1em 0; }
.markdown-body table { border-collapse: collapse; }
.markdown-body table th, .markdown-body table td { border: 1px solid #e0e0e0; padding: 0.4em 0.7em; }
.markdown-body table th { background: #f3f4f6; }
.markdown-body > h1:first-of-type {
  font-size: 1.9em;
  margin: 0.2em 0 0.8em;
  color: #222;
  border-bottom: 2px solid #0066cc;
  padding-bottom: 0.25em;
}
.lc-embed-mode #lc-topbar { display: none !important; }
.lc-embed-mode body { padding-top: 0 !important; }
.lc-embed-mode .markdown-body > h1:first-of-type { display: none !important; }
</style>
<div id="lc-topbar">
  <a class="lc-brand" href="/">💡 Lightcodepedia</a>
  {% assign _menu = site.pages | where: "path", "menu.md" | first %}
  <div class="lc-links">
    {{ _menu.content | markdownify }}
  </div>
  <a id="lc-start-pill" href="/start">🔑 Get started</a>
  <div id="lc-user-pill" style="display:none">
    <button id="lc-user-btn" aria-label="User menu" title="">
      <img id="lc-user-avatar" src="" alt="">
    </button>
    <div id="lc-user-drop">
      <div class="lc-ud-head">
        <img id="lc-ud-avatar" src="" alt="">
        <div>
          <div class="lc-ud-name" id="lc-ud-name"></div>
          <div class="lc-ud-login" id="lc-ud-login"></div>
        </div>
      </div>
      <a class="lc-ud-row" id="lc-ud-repo-link" href="#" target="_blank">
        <span>📁</span><span class="lc-ud-repo" id="lc-ud-repo-label"></span>
      </a>
      <a class="lc-ud-row lc-ud-karma-row" id="lc-ud-karma-row" href="/nodes" style="display:none;flex-direction:column;align-items:flex-start;gap:2px">
        <div style="display:flex;justify-content:space-between;width:100%;align-items:center">
          <span>🌟 <span id="lc-ud-karma-pts">…</span> karma pts</span>
          <span style="font-size:0.75em;color:#bbb">network →</span>
        </div>
        <div id="lc-ud-karma-detail" style="font-size:0.75em;color:#c47900;opacity:0.75"></div>
      </a>
      <a class="lc-ud-row" href="/start"><span>🚀</span><span>Onboarding</span></a>
      <a class="lc-ud-row" id="lc-ud-pages-link" href="#" target="_blank"><span>🌐</span><span id="lc-ud-pages-label">Your site</span></a>
      <div id="lc-ud-rate" style="display:none;padding:6px 16px;font-size:0.75em;border-bottom:1px solid #f0f0f0"></div>
      <div class="lc-ud-row danger" id="lc-ud-disconnect"><span>🔓</span><span>Disconnect</span></div>
    </div>
  </div>
</div>
{% include code_chrome.md %}
<script>
(function(){
  var links = document.querySelectorAll('#lc-topbar .lc-links a');
  links.forEach(function(a){
    var t = a.textContent.trim();
    var i = t.indexOf(' ');
    if (i > 0) {
      a.innerHTML = '<span class="lc-link-icon">' + t.substring(0, i) + '</span><span class="lc-link-label">' + t.substring(i + 1) + '</span>';
    }
  });

  // ── User pill ──────────────────────────────────────────────────────────────
  (function() {
    var pat  = localStorage.getItem('lc_ed_pat');
    var repo = localStorage.getItem('lc_ed_repo');
    if (!pat) { document.getElementById('lc-start-pill').style.display = 'block'; return; }

    function showUser(u) {
      var pill = document.getElementById('lc-user-pill');
      pill.style.display = 'block';
      document.getElementById('lc-user-avatar').src = u.avatar_url;
      document.getElementById('lc-user-btn').title = '@' + u.login;
      document.getElementById('lc-ud-avatar').src = u.avatar_url;
      document.getElementById('lc-ud-name').textContent = u.name || u.login;
      document.getElementById('lc-ud-login').textContent = '@' + u.login;

      // karma: show cached value instantly, then verify from GitHub API
      var kRow = document.getElementById('lc-ud-karma-row');
      var kPts = document.getElementById('lc-ud-karma-pts');
      var _kCached = 0;
      if (localStorage.getItem('lc_karma_launch')) _kCached += 15;
      if (localStorage.getItem('lc_karma_bio'))    _kCached += 10;
      var _kForksCached  = parseInt(localStorage.getItem('lc_karma_forks')   || '0', 10);
      var _kStarsCached  = parseInt(localStorage.getItem('lc_karma_stars')   || '0', 10);
      var _kViewsCached  = parseInt(localStorage.getItem('lc_karma_traffic') || '0', 10);
      var _kPagesCached  = parseInt(localStorage.getItem('lc_karma_pages')   || '0', 10);
      var _kQuizCached   = parseInt(localStorage.getItem('lc_karma_quizzes') || '0', 10);
      _kCached += _kForksCached * 50 + _kStarsCached * 10 + _kViewsCached + _kPagesCached * 10 + _kQuizCached * 5;
      if (kPts) kPts.textContent = _kCached || '…';
      if (kRow && _kCached > 0) {
        kRow.style.display = 'flex';
        var _cachedParts = [];
        if (_kForksCached > 0) _cachedParts.push('🍴 ' + _kForksCached + ' forks');
        if (_kStarsCached > 0) _cachedParts.push('⭐ ' + _kStarsCached + ' stars');
        if (_kViewsCached > 0) _cachedParts.push('👥 ' + _kViewsCached + ' visitors');
        if (_kPagesCached > 0) _cachedParts.push('📄 ' + _kPagesCached + ' pages');
        if (_kQuizCached  > 0) _cachedParts.push('🧩 ' + _kQuizCached  + ' quizzes');
        if (localStorage.getItem('lc_karma_bio'))    _cachedParts.push('📝 bio');
        if (localStorage.getItem('lc_karma_launch')) _cachedParts.push('🚀 site');
        var _detCached = document.getElementById('lc-ud-karma-detail');
        if (_detCached) _detCached.textContent = _cachedParts.join('  ·  ');
      }

      // verify karma from GitHub API — skip if verified less than 1 hour ago
      var _ghHdrs = { Authorization: 'Bearer ' + pat, 'X-GitHub-Api-Version': '2022-11-28' };

      // Authoritative, non-consuming rate check — /rate_limit does NOT count
      // against your quota, so it's the reliable source of truth. Runs even when
      // the karma cache is fresh (before the early return below).
      fetch('https://api.github.com/rate_limit', { headers: _ghHdrs })
        .then(function(r){ return r.ok ? r.json() : null; })
        .then(function(d){
          var core = d && d.resources && d.resources.core;
          if (core) {
            localStorage.setItem('lc_rate_remaining', String(core.remaining));
            localStorage.setItem('lc_rate_limit',     String(core.limit));
            showRateLimit(core.remaining, core.limit);
          }
        })
        .catch(function(){});
      var _repoSlug = (repo || (u.login + '/lightcodepedia')).split('/')[1] || 'lightcodepedia';
      var _repoBase = 'https://api.github.com/repos/' + u.login + '/' + _repoSlug;
      var _karma = 0;
      var _rc = { forks: 0, stars: 0, visitors: 0, pages: 0, quizzes: 0, bio: false, site: false };

      var _karmaTs = parseInt(localStorage.getItem('lc_karma_ts') || '0', 10);
      var _karmaAge = Date.now() - _karmaTs;  // ms since last full API verification
      if (_karmaAge < 3600000) {
        // cached values are fresh — skip the 5 API calls, just re-render
        _rc.site     = !!localStorage.getItem('lc_karma_launch');
        _rc.bio      = !!localStorage.getItem('lc_karma_bio');
        _rc.forks    = _kForksCached; _rc.stars = _kStarsCached;
        _rc.visitors = _kViewsCached; _rc.pages = _kPagesCached; _rc.quizzes = _kQuizCached;
        _karma = _kCached;
        if (kPts) kPts.textContent = _karma;
        // age label so user can see how stale
        var _ageMin = Math.round(_karmaAge / 60000);
        var _detEl2 = document.getElementById('lc-ud-karma-detail');
        if (_detEl2 && _detEl2.textContent) _detEl2.textContent += '  ·  ⏱ ' + _ageMin + 'm ago';
        if (kRow) kRow.style.display = 'flex';
        // still show rate limit from last known value
        showRateLimit(parseInt(localStorage.getItem('lc_rate_remaining') || '-1', 10));
        return;  // ← skip all API calls
      }

      // helper: reads X-RateLimit-* from a Response and persists it
      function trackRate(r) {
        var rem = parseInt(r.headers.get('X-RateLimit-Remaining') || '-1', 10);
        var lim = parseInt(r.headers.get('X-RateLimit-Limit')     || '-1', 10);
        if (rem >= 0) {
          localStorage.setItem('lc_rate_remaining', String(rem));
          if (lim > 0) localStorage.setItem('lc_rate_limit', String(lim));
          showRateLimit(rem, lim);
        }
        return r;
      }
      function showRateLimit(rem, lim) {
        var el = document.getElementById('lc-ud-rate');
        if (!el || rem < 0) return;
        if (!lim || lim < 0) lim = parseInt(localStorage.getItem('lc_rate_limit') || '5000', 10) || 5000;
        var ratio = rem / lim;
        // battery emoji: full when plenty left, almost-empty when running low
        var batt = ratio < 0.2 ? '🪫' : '🔋';
        el.style.display = 'flex';
        el.textContent = batt + ' ' + rem + ' / ' + lim + ' API calls left this hour';
        el.style.color = ratio < 0.1 ? '#c00' : ratio < 0.25 ? '#c47900' : '#888';
      }

      fetch(_repoBase, { headers: _ghHdrs }).then(trackRate)
        .then(function(r) {
          if (!r.ok) { localStorage.removeItem('lc_karma_launch'); return Promise.reject('no-repo'); }
          return r.json();
        })
        .then(function(repoData) {
          _rc.site = true; _karma += 15;
          localStorage.setItem('lc_karma_launch', '1');
          _rc.forks = repoData.forks_count || 0;
          _rc.stars = repoData.stargazers_count || 0;
          if (_rc.forks > 0) { _karma += _rc.forks * 50; localStorage.setItem('lc_karma_forks', String(_rc.forks)); }
          else localStorage.removeItem('lc_karma_forks');
          if (_rc.stars > 0) { _karma += _rc.stars * 10; localStorage.setItem('lc_karma_stars', String(_rc.stars)); }
          else localStorage.removeItem('lc_karma_stars');
          return fetch(_repoBase + '/contents/docs/_profile.md', { headers: _ghHdrs });
        })
        .then(function(r) {
          if (r && r.ok) { _rc.bio = true; _karma += 10; localStorage.setItem('lc_karma_bio', '1'); }
          else localStorage.removeItem('lc_karma_bio');
          return Promise.all([
            fetch(_repoBase + '/traffic/views', { headers: _ghHdrs }).then(function(r){ return r.ok ? r.json() : null; }).catch(function(){ return null; }),
            fetch(_repoBase + '/contents/docs/pages', { headers: _ghHdrs }).then(function(r){ return r.ok ? r.json() : []; }).catch(function(){ return []; })
          ]);
        })
        .then(function(results) {
          var traffic = results[0];
          var pages   = results[1];
          _rc.visitors = (traffic && traffic.uniques) || 0;
          if (_rc.visitors > 0) { _karma += _rc.visitors; localStorage.setItem('lc_karma_traffic', String(_rc.visitors)); }
          else localStorage.removeItem('lc_karma_traffic');
          _rc.pages = Array.isArray(pages) ? pages.filter(function(f){ return f.type === 'file' && /\.md$/i.test(f.name) && !f.name.startsWith('_') && f.name !== 'index.md'; }).length : 0;
          if (_rc.pages > 0) { _karma += _rc.pages * 10; localStorage.setItem('lc_karma_pages', String(_rc.pages)); }
          else localStorage.removeItem('lc_karma_pages');
          _rc.quizzes = parseInt(localStorage.getItem('lc_karma_quizzes') || '0', 10);
          if (_rc.quizzes > 0) { _karma += _rc.quizzes * 5; }
          localStorage.setItem('lc_karma_ts', String(Date.now()));  // mark fresh
          if (kPts) kPts.textContent = _karma;
          var parts = [];
          if (_rc.forks    > 0) parts.push('🍴 ' + _rc.forks + ' forks');
          if (_rc.stars    > 0) parts.push('⭐ ' + _rc.stars + ' stars');
          if (_rc.visitors > 0) parts.push('👥 ' + _rc.visitors + ' visitors');
          if (_rc.pages    > 0) parts.push('📄 ' + _rc.pages + ' pages');
          if (_rc.quizzes  > 0) parts.push('🧩 ' + _rc.quizzes + ' quizzes');
          if (_rc.bio)          parts.push('📝 bio');
          if (_rc.site)         parts.push('🚀 site');
          var detEl = document.getElementById('lc-ud-karma-detail');
          if (detEl) detEl.textContent = parts.join('  ·  ') + '  ·  ⏱ just now';
          if (kRow) kRow.style.display = 'flex';
        })
        .catch(function(e) {
          if (e === 'no-repo') { if (kRow) kRow.style.display = 'none'; return; }
          if (kPts) kPts.textContent = _karma;
          var detEl = document.getElementById('lc-ud-karma-detail');
          if (detEl && detEl.textContent) detEl.textContent += '  ·  ⚠️ partial';
          if (kRow && _karma > 0) kRow.style.display = 'flex';
        });

      var repoLabel = repo || (u.login + '/lightcodepedia');
      document.getElementById('lc-ud-repo-label').textContent = repoLabel;
      document.getElementById('lc-ud-repo-link').href = 'https://github.com/' + repoLabel;
      var siteHost = u.login + '.github.io';
      var repoSlug = repoLabel.split('/')[1] || 'lightcodepedia';
      document.getElementById('lc-ud-pages-link').href = 'https://' + siteHost + '/' + repoSlug;
      document.getElementById('lc-ud-pages-label').textContent = siteHost + '/' + repoSlug;
    }

    var cached = null;
    try { cached = JSON.parse(localStorage.getItem('lc_gh_user') || 'null'); } catch(e){}
    var cachedFor = localStorage.getItem('lc_gh_user_for');
    if (cached && cachedFor === pat) { showUser(cached); }
    else {
      fetch('https://api.github.com/user', { headers: { Authorization: 'Bearer ' + pat } })
        .then(function(r){ var rem=parseInt(r.headers.get('X-RateLimit-Remaining')||'-1',10); if(rem>=0)localStorage.setItem('lc_rate_remaining',String(rem)); return r.ok ? r.json() : Promise.reject(r.status); })
        .then(function(u){
          localStorage.setItem('lc_gh_user', JSON.stringify(u));
          localStorage.setItem('lc_gh_user_for', pat);
          showUser(u);
        })
        .catch(function(){ document.getElementById('lc-start-pill').style.display = 'block'; });
    }

    // dropdown toggle
    var btn = document.getElementById('lc-user-btn');
    var drop = document.getElementById('lc-user-drop');
    btn.addEventListener('click', function(e){ e.stopPropagation(); drop.classList.toggle('open'); });
    document.addEventListener('click', function(){ drop.classList.remove('open'); });
    drop.addEventListener('click', function(e){ e.stopPropagation(); });

    // disconnect
    document.getElementById('lc-ud-disconnect').addEventListener('click', function(){
      ['lc_ed_pat','lc_ed_repo','lc_gh_user','lc_gh_user_for'].forEach(function(k){ localStorage.removeItem(k); });
      location.reload();
    });
  })();
})();
</script>
