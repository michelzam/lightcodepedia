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
      var _kForksCached = parseInt(localStorage.getItem('lc_karma_forks') || '0', 10);
      _kCached += _kForksCached * 50;
      if (kPts) kPts.textContent = _kCached || '…';
      if (kRow && _kCached > 0) kRow.style.display = 'flex';

      // verify karma from GitHub API: repo info (fork + downstream forks) then bio file
      var _ghHdrs = { Authorization: 'Bearer ' + pat, 'X-GitHub-Api-Version': '2022-11-28' };
      var _repoSlug = (repo || (u.login + '/lightcodepedia')).split('/')[1] || 'lightcodepedia';
      var _karma = 0; var _detail = [];
      fetch('https://api.github.com/repos/' + u.login + '/' + _repoSlug, { headers: _ghHdrs })
        .then(function(r) {
          if (!r.ok) { localStorage.removeItem('lc_karma_launch'); return Promise.reject('no-repo'); }
          return r.json();
        })
        .then(function(repoData) {
          _karma += 15; _detail.push('+15 site');
          localStorage.setItem('lc_karma_launch', '1');
          var downstream = repoData.forks_count || 0;
          if (downstream > 0) {
            _karma += downstream * 50;
            _detail.push('+' + downstream + '×50 forks');
            localStorage.setItem('lc_karma_forks', String(downstream));
          } else {
            localStorage.removeItem('lc_karma_forks');
          }
          return fetch('https://api.github.com/repos/' + u.login + '/' + _repoSlug + '/contents/docs/_profile.md', { headers: _ghHdrs });
        })
        .then(function(r) {
          if (r && r.ok) { _karma += 10; _detail.push('+10 bio'); localStorage.setItem('lc_karma_bio', '1'); }
          else             { localStorage.removeItem('lc_karma_bio'); }
          if (kPts) kPts.textContent = _karma;
          var detEl = document.getElementById('lc-ud-karma-detail');
          if (detEl) detEl.textContent = _detail.join('  ·  ');
          if (kRow) kRow.style.display = 'flex';
        })
        .catch(function(e) {
          if (e === 'no-repo') { if (kRow) kRow.style.display = 'none'; return; }
          /* network error — keep cached display */
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
        .then(function(r){ return r.ok ? r.json() : Promise.reject(r.status); })
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
