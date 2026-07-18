# 🚀 Get started

Set up your own Lightcodepedia site in 6 steps. Steps 1 and 2 take about 2 minutes on GitHub. The rest is automatic — and each step earns you **karma** 🌟

_Karma measures your contribution to the network: your site, your bio, the friends you bring in. It shows up on the [community map](/nodes) and grows as your impact does._

<div id="lc-wizard">

<div class="lcw-step" id="lcw-s1">
<div class="lcw-head"><span class="lcw-num">1</span><span class="lcw-title">Create a GitHub account</span><span class="lcw-karma-badge">prerequisite</span><span class="lcw-check" id="lcw-c1"></span></div>
<div class="lcw-body">
<p>GitHub is the free service that hosts your site. If you already have an account, skip straight to step 2.</p>
<ol>
<li>Click <strong>Open GitHub signup →</strong> below — it opens in a new tab.</li>
<li>Fill in your email, a password, and a username.</li>
<li>Verify your email when GitHub asks.</li>
<li>Come back here and click <strong>I have an account ✓</strong>.</li>
</ol>
<div class="lcw-actions">
<a class="lcw-btn lcw-btn-outline" href="https://github.com/signup" target="_blank">Open GitHub signup →</a>
<button class="lcw-btn" onclick="lcwNext(1)">I have an account ✓</button>
</div>
</div>
</div>

<div class="lcw-step lcw-locked" id="lcw-s2">
<div class="lcw-head"><span class="lcw-num">2</span><span class="lcw-title">Create your access key</span><span class="lcw-karma-badge">prerequisite</span><span class="lcw-check" id="lcw-c2"></span></div>
<div class="lcw-body">
<p>An <strong>access key</strong> (called a PAT) lets this page talk to GitHub on your behalf — to fork your site and save your edits. It never leaves your browser.</p>
<ol>
<li>Click <strong>Open GitHub token page →</strong> below.</li>
<li>Click <strong>Generate new token (classic)</strong>.</li>
<li>Give it any name, e.g. <em>lightcodepedia</em>.</li>
<li>Check the <strong><code>repo</code></strong> box (top of the list).</li>
<li>Scroll down → <strong>Generate token</strong> → copy the key (starts with <code>ghp_</code>).<br>
<em>Already using a fine-grained key (<code>github_pat_…</code>)? It works too — give it <strong>Contents: read and write</strong> on your site.</em></li>
<li>Come back here and paste it below.</li>
</ol>
<div class="lcw-actions">
<a class="lcw-btn lcw-btn-outline" href="https://github.com/settings/tokens/new?description=lightcodepedia&scopes=repo" target="_blank">Open GitHub token page →</a>
</div>
<div class="lcw-field">
<input id="lcw-pat" type="password" placeholder="ghp_…" autocomplete="current-password" spellcheck="false">
<button class="lcw-btn" id="lcw-check-btn" onclick="lcwCheckPat()">Check key ✓</button>
</div>
<div id="lcw-pat-result" class="lcw-result"></div>
</div>
</div>

<div class="lcw-step lcw-locked" id="lcw-s3">
<div class="lcw-head"><span class="lcw-num">3</span><span class="lcw-title">Fork &amp; launch your site</span><span class="lcw-karma-badge">🌟 +15 pts</span><span class="lcw-check" id="lcw-c3"></span></div>
<div class="lcw-body">
<p>One click forks the Lightcodepedia template into your GitHub account and turns on your free website.</p>
<div id="lcw-user-card" style="display:none" class="lcw-user-card">
<img id="lcw-uc-avatar" src="" alt="" style="width:48px;height:48px;border-radius:50%;margin-right:12px">
<div><div id="lcw-uc-name" style="font-weight:600"></div><div id="lcw-uc-login" style="color:#888;font-size:0.85em"></div></div>
</div>
<div id="lcw-fork-status" class="lcw-result"></div>
<div class="lcw-actions" id="lcw-fork-actions">
<button class="lcw-btn" id="lcw-fork-btn" onclick="lcwFork()">🍴 Fork &amp; launch</button>
</div>
<div id="lcw-launch-result" style="display:none">
<p>✅ <strong>Your site is being built.</strong> It will be live at:</p>
<p><a id="lcw-site-url" href="#" target="_blank" style="font-size:1.1em;font-weight:600"></a></p>
<p style="color:#888;font-size:0.9em">The first build takes about 60 seconds. Reload the link above until it appears.</p>
<button class="lcw-btn" onclick="lcwNext(3)">Continue ✓</button>
</div>
</div>
</div>

<div class="lcw-step lcw-locked" id="lcw-s4">
<div class="lcw-head"><span class="lcw-num">4</span><span class="lcw-title">Introduce yourself</span><span class="lcw-karma-badge">🌟 +10 pts</span><span class="lcw-check" id="lcw-c4"></span></div>
<div class="lcw-body">
<p>Add a sentence or two about yourself and why you joined. It will appear on the <a href="/nodes">community map</a> next to your LightNode.</p>
<div class="lcw-bio-wrap">
<textarea id="lcw-bio" rows="3" maxlength="280" placeholder="e.g. I teach Python to high-school students in Lyon. I joined Lightcodepedia to give my learners interactive pages they can actually run and explore." spellcheck="true"></textarea>
<div class="lcw-bio-footer"><span id="lcw-bio-count">0 / 280</span><button class="lcw-btn" id="lcw-bio-btn" onclick="lcwSaveBio()">Save bio ✓</button></div>
</div>
<div id="lcw-bio-result" class="lcw-result"></div>
</div>
</div>

<div class="lcw-step lcw-locked" id="lcw-s5">
<div class="lcw-head"><span class="lcw-num">5</span><span class="lcw-title">Invite a friend</span><span class="lcw-karma-badge">🌟 +50 pts / friend</span><span class="lcw-check" id="lcw-c5"></span></div>
<div class="lcw-body">
<p>Every friend who joins through your link and launches their LightNode earns you <strong>50 karma points</strong>. The network grows — and so does everyone in it.</p>
<div class="lcw-invite-box">
<input id="lcw-invite-url" type="text" readonly>
<button class="lcw-btn" onclick="lcwCopyInvite()" id="lcw-copy-btn">📋 Copy</button>
</div>
<div class="lcw-share-row" id="lcw-share-row"></div>
<p style="font-size:0.85em;color:#888;margin-top:0.8em">Share this link with anyone. When they finish the onboarding, your karma goes up automatically.</p>
<div class="lcw-actions" style="margin-top:1em">
<button class="lcw-btn lcw-btn-outline" onclick="lcwNext(5)">Skip for now →</button>
<button class="lcw-btn" onclick="lcwNext(5)">Done, continue ✓</button>
</div>
</div>
</div>

<div class="lcw-step lcw-locked" id="lcw-s6">
<div class="lcw-head"><span class="lcw-num">6</span><span class="lcw-title">You're ready! 🎉</span></div>
<div class="lcw-body">
<div id="lcw-done-card" class="lcw-user-card">
<img id="lcw-done-avatar" src="" alt="" style="width:56px;height:56px;border-radius:50%;margin-right:14px">
<div>
<div id="lcw-done-welcome" style="font-weight:600;font-size:1.1em"></div>
<div><a id="lcw-done-url" href="#" target="_blank" style="font-size:0.9em"></a></div>
<div id="lcw-done-karma" style="font-size:0.85em;color:#c47900;margin-top:4px"></div>
</div>
</div>
<div class="lcw-next-cards">
  <a class="lcw-next-card" href="/tutorial101">
    <div class="lcw-next-icon">🌱</div>
    <strong>Start the tutorial</strong>
    <div class="lcw-next-desc">Learn every building block — through the story of a dog called Lucky.</div>
    <div class="lcw-next-cta">Start →</div>
  </a>
  <a class="lcw-next-card" href="/pages">
    <div class="lcw-next-icon">✏️</div>
    <strong>Edit your pages</strong>
    <div class="lcw-next-desc">Open the built-in editor and start customising your site right now.</div>
    <div class="lcw-next-cta">Edit →</div>
  </a>
  <a class="lcw-next-card" href="/components/">
    <div class="lcw-next-icon">🧩</div>
    <strong>Browse components</strong>
    <div class="lcw-next-desc">See every interactive block with live examples and documentation.</div>
    <div class="lcw-next-cta">Browse →</div>
  </a>
</div>
</div>
</div>

</div>

<style>
#lc-wizard { margin: 1.5em 0; }
.lcw-step {
  border: 1px solid #ddd; border-radius: 10px; margin-bottom: 1em; overflow: hidden;
  transition: border-color 0.2s;
}
.lcw-step.lcw-active { border-color: #0066cc; box-shadow: 0 0 0 3px #e8f0fe; }
.lcw-step.lcw-done { border-color: #2a9d2a; opacity: 0.7; }
.lcw-step.lcw-locked { opacity: 0.45; pointer-events: none; }
.lcw-head {
  display: flex; align-items: center; gap: 12px;
  padding: 14px 18px; background: #f8f8f8; border-bottom: 1px solid #eee;
  font-weight: 600;
}
.lcw-step.lcw-active .lcw-head { background: #e8f0fe; border-bottom-color: #c0d4f5; }
.lcw-step.lcw-done .lcw-head { background: #f0faf0; }
.lcw-num {
  width: 28px; height: 28px; border-radius: 50%; background: #ddd;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.85em; flex-shrink: 0; font-weight: 700;
}
.lcw-step.lcw-active .lcw-num { background: #0066cc; color: #fff; }
.lcw-step.lcw-done .lcw-num { background: #2a9d2a; color: #fff; }
.lcw-title { flex: 1; }
.lcw-check { font-size: 1.1em; }
.lcw-body { padding: 18px 20px; }
.lcw-body ol { padding-left: 1.4em; margin: 0.6em 0 1em; }
.lcw-body ol li { margin-bottom: 0.4em; }
.lcw-actions { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 1em; }
.lcw-btn {
  background: #0066cc; color: #fff; border: none; border-radius: 6px;
  padding: 0.5em 1.2em; cursor: pointer; font-size: 0.9em; text-decoration: none;
  display: inline-block;
}
.lcw-btn:hover { background: #0052a3; }
.lcw-btn-outline {
  background: #fff; color: #0066cc; border: 1px solid #0066cc;
}
.lcw-btn-outline:hover { background: #e8f0fe; }
.lcw-field { display: flex; gap: 8px; margin-top: 1em; flex-wrap: wrap; }
.lcw-field input {
  flex: 1; min-width: 200px; padding: 0.45em 0.8em; border: 1px solid #ccc;
  border-radius: 6px; font-family: monospace; font-size: 0.9em;
}
.lcw-result { margin-top: 0.8em; font-size: 0.9em; min-height: 1.4em; }
.lcw-result.ok { color: #1a7a1a; }
.lcw-result.err { color: #c00; }
.lcw-user-card {
  display: flex; align-items: center; background: #f8f8f8;
  border: 1px solid #e0e0e0; border-radius: 8px; padding: 12px 16px;
  margin: 0.8em 0;
}
.lcw-karma-badge {
  margin-left: auto; font-size: 0.75em; font-weight: 600;
  color: #c47900; background: #fff8e1; border: 1px solid #ffe082;
  border-radius: 10px; padding: 2px 9px; white-space: nowrap; flex-shrink: 0;
}
.lcw-karma-badge:not([data-pts]) { color: #888; background: #f3f4f6; border-color: #e0e0e0; }
.lcw-bio-wrap { margin-top: 0.8em; }
.lcw-bio-wrap textarea {
  width: 100%; box-sizing: border-box; padding: 0.6em 0.8em;
  border: 1px solid #ccc; border-radius: 6px; font-family: inherit;
  font-size: 0.9em; line-height: 1.5; resize: vertical; min-height: 80px;
}
.lcw-bio-wrap textarea:focus { outline: none; border-color: #0066cc; box-shadow: 0 0 0 2px #e8f0fe; }
.lcw-bio-footer { display: flex; justify-content: space-between; align-items: center; margin-top: 6px; }
.lcw-bio-footer span { font-size: 0.8em; color: #aaa; }
.lcw-invite-box { display: flex; gap: 8px; margin-top: 0.8em; flex-wrap: wrap; }
.lcw-invite-box input {
  flex: 1; min-width: 200px; padding: 0.45em 0.8em; border: 1px solid #ccc;
  border-radius: 6px; font-family: monospace; font-size: 0.85em; background: #f8f8f8; color: #333;
}
.lcw-share-row { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 10px; }
.lcw-share-btn {
  font-size: 0.82em; padding: 5px 12px; border-radius: 6px; cursor: pointer;
  text-decoration: none; border: 1px solid #ddd; background: #fff; color: #333;
  display: inline-flex; align-items: center; gap: 5px;
}
.lcw-share-btn:hover { background: #f5f5f5; }
.lcw-next-cards { display: flex; gap: 14px; flex-wrap: wrap; margin-top: 1.2em; }
.lcw-next-card {
  flex: 1; min-width: 150px; padding: 16px 18px; border: 1px solid #ddd; border-radius: 10px;
  text-decoration: none; color: inherit; display: flex; flex-direction: column; gap: 5px;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.lcw-next-card:hover { border-color: #0066cc; box-shadow: 0 2px 12px rgba(0,102,204,.1); }
.lcw-next-icon { font-size: 1.4em; }
.lcw-next-desc { font-size: 0.85em; color: #555; flex: 1; }
.lcw-next-cta { font-size: 0.85em; color: #0066cc; font-weight: 600; margin-top: 4px; }
</style>

<script>
(function(){
  var _pat = '', _user = null;

  // restore if already connected
  var stored = localStorage.getItem('lc_ed_pat');
  var _restored = false;

  function restoreProgress() {
    var _hasLaunch  = !!localStorage.getItem('lc_karma_launch');
    var _hasBio     = !!localStorage.getItem('lc_karma_bio');
    var _hasStarted = !!localStorage.getItem('lc_started');
    lcwDone(1); lcwDone(2);
    if (_hasStarted)     { lcwDone(3); lcwDone(4); lcwDone(5); populateUserCard(); lcwActivate(6); }
    else if (_hasBio)    { lcwDone(3); lcwDone(4); lcwActivate(5); }
    else if (_hasLaunch) { lcwDone(3); lcwActivate(4); }
    else                 { lcwActivate(3); }
  }

  // verify karma from GitHub API then call restoreProgress
  function syncKarmaAndRestore() {
    if (!_user || !_pat) { restoreProgress(); return; }
    var ghHdrs = { Authorization: 'Bearer ' + _pat, 'X-GitHub-Api-Version': '2022-11-28' };
    var repoSlug = (localStorage.getItem('lc_ed_repo') || (_user.login + '/lightcodepedia')).split('/')[1] || 'lightcodepedia';
    var _repoBase = 'https://api.github.com/repos/' + _user.login + '/' + repoSlug;
    fetch(_repoBase, { headers: ghHdrs })
      .then(function(r) {
        if (!r.ok) { localStorage.removeItem('lc_karma_launch'); restoreProgress(); return Promise.reject('no-repo'); }
        return r.json();
      })
      .then(function(repoData) {
        localStorage.setItem('lc_karma_launch', '1');
        var forks = repoData.forks_count || 0;
        var stars = repoData.stargazers_count || 0;
        if (forks > 0) localStorage.setItem('lc_karma_forks', String(forks)); else localStorage.removeItem('lc_karma_forks');
        if (stars > 0) localStorage.setItem('lc_karma_stars', String(stars)); else localStorage.removeItem('lc_karma_stars');
        // fetch bio file, traffic, and pages directory in parallel
        return Promise.all([
          fetch(_repoBase + '/contents/docs/_profile.md', { headers: ghHdrs }),
          fetch(_repoBase + '/traffic/views', { headers: ghHdrs })
            .then(function(r) { return r.ok ? r.json() : null; }).catch(function() { return null; }),
          fetch(_repoBase + '/contents/docs/pages', { headers: ghHdrs })
            .then(function(r) { return r.ok ? r.json() : []; }).catch(function() { return []; })
        ]);
      })
      .then(function(results) {
        var bioResp = results[0], traffic = results[1], pages = results[2];
        if (bioResp && bioResp.ok) localStorage.setItem('lc_karma_bio', '1'); else localStorage.removeItem('lc_karma_bio');
        var uniques = (traffic && traffic.uniques) || 0;
        if (uniques > 0) localStorage.setItem('lc_karma_traffic', String(uniques)); else localStorage.removeItem('lc_karma_traffic');
        var pageCount = Array.isArray(pages) ? pages.filter(function(f) {
          return f.type === 'file' && f.name.endsWith('.md') && !f.name.startsWith('_');
        }).length : 0;
        if (pageCount > 0) localStorage.setItem('lc_karma_pages', String(pageCount)); else localStorage.removeItem('lc_karma_pages');
        restoreProgress();
      })
      .catch(function(e) { if (e !== 'no-repo') restoreProgress(); });
  }

  if (stored) {
    _pat = stored;
    var cached = null;
    try { cached = JSON.parse(localStorage.getItem('lc_gh_user') || 'null'); } catch(e){}

    if (cached && localStorage.getItem('lc_gh_user_for') === stored) {
      // valid cache — show progress immediately from localStorage, then refine from GitHub
      _user = cached;
      _restored = true;
      document.getElementById('lcw-pat').value = '••••••••••••';
      populateUserCard();
      restoreProgress();       // immediate: no gray steps while API loads
      syncKarmaAndRestore();   // async: validates + refines
    } else {
      // PAT exists but cache is stale — skip step 1, re-validate async on step 2
      _restored = true;
      lcwDone(1);
      document.getElementById('lcw-pat').value = '••••••••••••';
      lcwActivate(2);
      fetch('https://api.github.com/user', {
        headers: { Authorization: 'Bearer ' + stored, 'X-GitHub-Api-Version': '2022-11-28' }
      })
      .then(function(r) {
        var scopes = r.headers.get('X-OAuth-Scopes') || '';
        return r.json().then(function(u) { return { user: u, ok: r.ok, scopes: scopes }; });
      })
      .then(function(d) {
        if (!d.ok) return; // bad PAT — let user re-enter on step 2
        /* classic keys announce their scopes; fine-grained ones announce
           nothing — authenticated is the best pre-check they offer */
        var hasRepo = d.scopes.split(',').map(function(s){ return s.trim(); }).indexOf('repo') >= 0
                   || stored.indexOf('github_pat_') === 0;
        if (!hasRepo) return;
        _user = d.user;
        localStorage.setItem('lc_gh_user', JSON.stringify(d.user));
        localStorage.setItem('lc_gh_user_for', stored);
        populateUserCard();
        syncKarmaAndRestore();
      })
      .catch(function() { /* network error — stay on step 2 so user can retry */ });
    }
  }

  // store referrer from ?from= param
  var urlFrom = new URLSearchParams(location.search).get('from');
  if (urlFrom) localStorage.setItem('lc_referrer', urlFrom);

  var KARMA = { launch: 15, bio: 10, invite: 50 };

  function karmaTotal() {
    var k = 0;
    if (localStorage.getItem('lc_karma_launch')) k += KARMA.launch;
    if (localStorage.getItem('lc_karma_bio'))    k += KARMA.bio;
    k += parseInt(localStorage.getItem('lc_karma_forks')   || '0', 10) * KARMA.invite;
    k += parseInt(localStorage.getItem('lc_karma_stars')   || '0', 10) * 10;
    k += parseInt(localStorage.getItem('lc_karma_traffic') || '0', 10);
    return k;
  }

  function populateUserCard() {
    if (!_user) return;
    var c = document.getElementById('lcw-user-card');
    c.style.display = 'flex';
    document.getElementById('lcw-uc-avatar').src = _user.avatar_url;
    document.getElementById('lcw-uc-name').textContent = _user.name || _user.login;
    document.getElementById('lcw-uc-login').textContent = '@' + _user.login;
    // done card
    document.getElementById('lcw-done-avatar').src = _user.avatar_url;
    document.getElementById('lcw-done-welcome').textContent = 'Welcome, ' + (_user.name || _user.login) + '! 🎉';
    var url = 'https://' + _user.login + '.github.io/lightcodepedia';
    document.getElementById('lcw-done-url').textContent = url;
    document.getElementById('lcw-done-url').href = url;
    // invite URL
    var inviteUrl = 'https://lightcodepedia.org/start?from=' + _user.login;
    var invEl = document.getElementById('lcw-invite-url');
    if (invEl) invEl.value = inviteUrl;
    // share buttons
    var shareRow = document.getElementById('lcw-share-row');
    if (shareRow && !shareRow.dataset.built) {
      shareRow.dataset.built = '1';
      var msg = encodeURIComponent('I just set up my own interactive learning site on Lightcodepedia — join me! ' + inviteUrl);
      var shares = [
        ['✉️ Email',    'mailto:?subject=Join+me+on+Lightcodepedia&body=' + msg],
        ['𝕏 X/Twitter', 'https://twitter.com/intent/tweet?text=' + msg],
        ['💼 LinkedIn',  'https://www.linkedin.com/sharing/share-offsite/?url=' + encodeURIComponent(inviteUrl)],
        ['💬 WhatsApp',  'https://wa.me/?text=' + msg],
      ];
      shares.forEach(function(s){
        var a = document.createElement('a');
        a.className = 'lcw-share-btn'; a.href = s[1]; a.target = '_blank'; a.textContent = s[0];
        shareRow.appendChild(a);
      });
    }
    // bio field
    var storedBio = localStorage.getItem('lc_bio');
    if (storedBio) { var bioEl = document.getElementById('lcw-bio'); if (bioEl) { bioEl.value = storedBio; updateBioCount(); } }
    // karma on done card
    updateKarmaDisplay();
  }

  function updateKarmaDisplay() {
    var el = document.getElementById('lcw-done-karma');
    if (!el) return;
    var k = karmaTotal();
    el.textContent = k > 0 ? '🌟 ' + k + ' karma pts earned so far' : '';
  }

  // bio char counter
  var bioEl = document.getElementById('lcw-bio');
  if (bioEl) {
    bioEl.addEventListener('input', updateBioCount);
  }
  function updateBioCount() {
    var el = document.getElementById('lcw-bio');
    var cnt = document.getElementById('lcw-bio-count');
    if (el && cnt) cnt.textContent = el.value.length + ' / 280';
  }

  window.lcwSaveBio = function() {
    var bio = (document.getElementById('lcw-bio').value || '').trim();
    var res = document.getElementById('lcw-bio-result');
    var btn = document.getElementById('lcw-bio-btn');
    if (!bio) { res.className = 'lcw-result err'; res.textContent = '⚠️ Please write a sentence or two about yourself first.'; return; }
    btn.disabled = true; btn.textContent = 'Saving…';
    var login = _user ? _user.login : '';
    var repoName = (localStorage.getItem('lc_ed_repo') || (login + '/lightcodepedia')).split('/')[1] || 'lightcodepedia';
    // encode bio as base64 (handles non-ASCII)
    var raw = '---\nbio: true\n---\n' + bio + '\n';
    var encoded = btoa(unescape(encodeURIComponent(raw)));
    var hdrs = { Authorization: 'Bearer ' + _pat, 'Content-Type': 'application/json', 'X-GitHub-Api-Version': '2022-11-28' };
    // get existing sha if file already exists
    fetch('https://api.github.com/repos/' + login + '/' + repoName + '/contents/docs/_profile.md', { headers: hdrs })
      .then(function(r) { return r.ok ? r.json() : null; })
      .then(function(existing) {
        var body = { message: 'profile: save bio', content: encoded };
        if (existing && existing.sha) body.sha = existing.sha;
        return fetch('https://api.github.com/repos/' + login + '/' + repoName + '/contents/docs/_profile.md', {
          method: 'PUT', headers: hdrs, body: JSON.stringify(body)
        });
      })
      .then(function(r) {
        btn.disabled = false; btn.textContent = 'Save bio ✓';
        if (!r || !r.ok) throw new Error('save failed');
        localStorage.setItem('lc_bio', bio);
        localStorage.setItem('lc_karma_bio', '1');
        res.className = 'lcw-result ok';
        res.textContent = '✅ Saved to your site repo! +' + KARMA.bio + ' karma pts earned 🌟';
        updateKarmaDisplay();
        setTimeout(function(){ lcwNext(4); }, 900);
      })
      .catch(function() {
        // fallback: store locally
        btn.disabled = false; btn.textContent = 'Save bio ✓';
        localStorage.setItem('lc_bio', bio);
        localStorage.setItem('lc_karma_bio', '1');
        res.className = 'lcw-result ok';
        res.textContent = '✅ Saved locally. +' + KARMA.bio + ' karma pts earned 🌟';
        updateKarmaDisplay();
        setTimeout(function(){ lcwNext(4); }, 900);
      });
  };

  window.lcwCopyInvite = function() {
    var val = document.getElementById('lcw-invite-url').value;
    navigator.clipboard.writeText(val).then(function(){
      var btn = document.getElementById('lcw-copy-btn');
      btn.textContent = '✅ Copied!';
      setTimeout(function(){ btn.textContent = '📋 Copy'; }, 2000);
    });
  };

  function lcwActivate(n) {
    var el = document.getElementById('lcw-s' + n);
    if (!el) return;
    el.classList.remove('lcw-locked');
    el.classList.add('lcw-active');
    el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  function lcwDone(n) {
    var el = document.getElementById('lcw-s' + n);
    if (!el) return;
    el.classList.remove('lcw-active', 'lcw-locked');
    el.classList.add('lcw-done');
    var c = document.getElementById('lcw-c' + n);
    if (c) c.textContent = '✅';
    // collapse body
    var body = el.querySelector('.lcw-body');
    if (body) body.style.display = 'none';
  }

  window.lcwNext = function(n) {
    if (n === 5) { localStorage.setItem('lc_started', '1'); populateUserCard(); }
    lcwDone(n);
    lcwActivate(n + 1);
  };

  window.lcwCheckPat = function() {
    var pat = document.getElementById('lcw-pat').value.trim();
    if (!pat || pat.startsWith('•')) { pat = _pat; }
    var res = document.getElementById('lcw-pat-result');
    var btn = document.getElementById('lcw-check-btn');
    if (!pat) { res.className = 'lcw-result err'; res.textContent = '⚠️ Please paste your access key first.'; return; }
    btn.disabled = true; btn.textContent = 'Checking…';
    res.className = 'lcw-result'; res.textContent = '';
    fetch('https://api.github.com/user', { headers: { Authorization: 'Bearer ' + pat, 'X-GitHub-Api-Version': '2022-11-28' } })
      .then(function(r) {
        var scopes = r.headers.get('X-OAuth-Scopes') || '';
        return r.json().then(function(u) { return { user: u, ok: r.ok, scopes: scopes }; });
      })
      .then(function(d) {
        btn.disabled = false; btn.textContent = 'Check key ✓';
        if (!d.ok) {
          res.className = 'lcw-result err';
          res.textContent = '❌ Key not recognised — please generate a new one and try again.';
          return;
        }
        /* classic keys announce scopes; fine-grained (github_pat_…) don't —
           accept them authenticated and let first use prove the rest */
        var fineGrained = pat.indexOf('github_pat_') === 0;
        var hasRepo = fineGrained ||
          d.scopes.split(',').map(function(s){return s.trim();}).indexOf('repo') >= 0;
        if (!hasRepo) {
          res.className = 'lcw-result err';
          res.textContent = '⚠️ Key is valid but missing the repo permission. Please regenerate with the repo box checked.';
          return;
        }
        _pat = pat; _user = d.user;
        localStorage.setItem('lc_ed_pat', pat);
        localStorage.setItem('lc_gh_user', JSON.stringify(d.user));
        localStorage.setItem('lc_gh_user_for', pat);
        res.className = 'lcw-result ok';
        res.textContent = '✅ Key is valid — logged in as @' + d.user.login +
          (fineGrained ? '. Fine-grained key: be sure it has Contents read & write on your site.' : ' with repo access.');
        populateUserCard();
        setTimeout(function(){ lcwNext(2); }, 800);
      })
      .catch(function() {
        btn.disabled = false; btn.textContent = 'Check key ✓';
        res.className = 'lcw-result err';
        res.textContent = '❌ Could not reach GitHub — check your internet connection.';
      });
  };

  window.lcwFork = function() {
    var btn = document.getElementById('lcw-fork-btn');
    var status = document.getElementById('lcw-fork-status');
    btn.disabled = true; btn.textContent = '⏳ Forking…';
    status.className = 'lcw-result'; status.textContent = '';

    function setStatus(msg, cls) { status.className = 'lcw-result ' + (cls||''); status.textContent = msg; }

    var login = _user.login;
    var siteUrl = 'https://' + login + '.github.io/lightcodepedia';

    // check if fork already exists
    fetch('https://api.github.com/repos/' + login + '/lightcodepedia', {
      headers: { Authorization: 'Bearer ' + _pat, 'X-GitHub-Api-Version': '2022-11-28' }
    })
    .then(function(r){ return r.ok; })
    .then(function(exists){
      if (exists) { setStatus('✅ Fork already exists.'); return doPages(); }
      setStatus('🍴 Forking repository…');
      return fetch('https://api.github.com/repos/michelzam/lightcodepedia/forks', {
        method: 'POST',
        headers: { Authorization: 'Bearer ' + _pat, 'Content-Type': 'application/json', 'X-GitHub-Api-Version': '2022-11-28' },
        body: JSON.stringify({ default_branch_only: true })
      })
      .then(function(r){ if (!r.ok) throw new Error('Fork failed: ' + r.status); return r.json(); })
      .then(function(){ return waitForFork(login, 0); });
    })
    .then(function(){ if (typeof doPages === 'function') return doPages(); })
    .catch(function(e){ setStatus('❌ ' + e.message, 'err'); btn.disabled = false; btn.textContent = '🍴 Fork & launch'; });

    function waitForFork(login, attempts) {
      if (attempts > 20) throw new Error('Fork is taking too long — try refreshing and clicking again.');
      setStatus('⏳ Waiting for fork to be ready… (' + (attempts+1) + '/20)');
      return new Promise(function(res){ setTimeout(res, 3000); })
        .then(function(){
          return fetch('https://api.github.com/repos/' + login + '/lightcodepedia', {
            headers: { Authorization: 'Bearer ' + _pat, 'X-GitHub-Api-Version': '2022-11-28' }
          });
        })
        .then(function(r){ return r.ok ? true : waitForFork(login, attempts+1); });
    }

    function doPages() {
      setStatus('⚙️ Enabling your website…');
      localStorage.setItem('lc_ed_repo', login + '/lightcodepedia');
      // Enable Actions
      return fetch('https://api.github.com/repos/' + login + '/lightcodepedia/actions/permissions', {
        method: 'PUT',
        headers: { Authorization: 'Bearer ' + _pat, 'Content-Type': 'application/json', 'X-GitHub-Api-Version': '2022-11-28' },
        body: JSON.stringify({ enabled: true, allowed_actions: 'all' })
      })
      .then(function(){
        // Enable Pages (try POST, fall back to PUT)
        return fetch('https://api.github.com/repos/' + login + '/lightcodepedia/pages', {
          method: 'POST',
          headers: { Authorization: 'Bearer ' + _pat, 'Content-Type': 'application/json', 'X-GitHub-Api-Version': '2022-11-28' },
          body: JSON.stringify({ build_type: 'workflow' })
        })
        .then(function(r){
          if (r.status === 409 || r.status === 422) {
            return fetch('https://api.github.com/repos/' + login + '/lightcodepedia/pages', {
              method: 'PUT',
              headers: { Authorization: 'Bearer ' + _pat, 'Content-Type': 'application/json', 'X-GitHub-Api-Version': '2022-11-28' },
              body: JSON.stringify({ build_type: 'workflow' })
            });
          }
        });
      })
      .then(function(){ return triggerBuild(login); })
      .then(function(){
        localStorage.setItem('lc_karma_launch', '1');
        setStatus('✅ All set!', 'ok');
        document.getElementById('lcw-fork-actions').style.display = 'none';
        document.getElementById('lcw-site-url').textContent = siteUrl;
        document.getElementById('lcw-site-url').href = siteUrl;
        document.getElementById('lcw-done-url').textContent = siteUrl;
        document.getElementById('lcw-done-url').href = siteUrl;
        document.getElementById('lcw-launch-result').style.display = 'block';
      });
    }

    function triggerBuild(login) {
      setStatus('🔨 Triggering first build…');
      var ts = new Date().toISOString();
      var content = btoa('# Build trigger\nLast triggered: ' + ts + '\n');
      return fetch('https://api.github.com/repos/' + login + '/lightcodepedia/contents/docs/_build_trigger.md', {
        headers: { Authorization: 'Bearer ' + _pat, 'X-GitHub-Api-Version': '2022-11-28' }
      })
      .then(function(r){ return r.ok ? r.json() : null; })
      .then(function(existing){
        var body = { message: 'chore: trigger Pages build', content: content };
        if (existing && existing.sha) body.sha = existing.sha;
        return fetch('https://api.github.com/repos/' + login + '/lightcodepedia/contents/docs/_build_trigger.md', {
          method: 'PUT',
          headers: { Authorization: 'Bearer ' + _pat, 'Content-Type': 'application/json', 'X-GitHub-Api-Version': '2022-11-28' },
          body: JSON.stringify(body)
        });
      });
    }
  };

  // activate step 1 only if nothing was restored
  if (!_restored) lcwActivate(1);
})();
</script>
