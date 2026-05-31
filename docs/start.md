# 🚀 Get started

Set up your own Lightcodepedia site in 4 steps. Steps 1 and 2 take about 2 minutes on GitHub. Steps 3 and 4 are fully automatic.

<div id="lc-wizard">

<div class="lcw-step" id="lcw-s1">
<div class="lcw-head"><span class="lcw-num">1</span><span class="lcw-title">Create a GitHub account</span><span class="lcw-check" id="lcw-c1"></span></div>
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
<div class="lcw-head"><span class="lcw-num">2</span><span class="lcw-title">Create your access key</span><span class="lcw-check" id="lcw-c2"></span></div>
<div class="lcw-body">
<p>An <strong>access key</strong> (called a PAT) lets this page talk to GitHub on your behalf — to fork your site and save your edits. It never leaves your browser.</p>
<ol>
<li>Click <strong>Open GitHub token page →</strong> below.</li>
<li>Click <strong>Generate new token (classic)</strong>.</li>
<li>Give it any name, e.g. <em>lightcodepedia</em>.</li>
<li>Check the <strong><code>repo</code></strong> box (top of the list).</li>
<li>Scroll down → <strong>Generate token</strong> → copy the key (starts with <code>ghp_</code>).</li>
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
<div class="lcw-head"><span class="lcw-num">3</span><span class="lcw-title">Fork &amp; launch your site</span><span class="lcw-check" id="lcw-c3"></span></div>
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
<div class="lcw-head"><span class="lcw-num">4</span><span class="lcw-title">You're ready! 🎉</span></div>
<div class="lcw-body">
<div id="lcw-done-card" class="lcw-user-card">
<img id="lcw-done-avatar" src="" alt="" style="width:56px;height:56px;border-radius:50%;margin-right:14px">
<div>
<div id="lcw-done-welcome" style="font-weight:600;font-size:1.1em"></div>
<div><a id="lcw-done-url" href="#" target="_blank" style="font-size:0.9em"></a></div>
</div>
</div>
<div style="margin-top:1.4em">

```
### 🌱 Start the tutorial
Learn every building block — through the story of a dog called Lucky.

[Start →](/tutorial101)

### ✏️ Edit your pages
Open the built-in editor and start customising your site right now.

[Edit →](/pages)

### 🧩 Browse components
See every interactive block with live examples and documentation.

[Browse →](/components/)
```
{: .cards cols="3" }

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
</style>

<script>
(function(){
  var _pat = '', _user = null;

  // restore if already connected
  var stored = localStorage.getItem('lc_ed_pat');
  if (stored) {
    _pat = stored;
    var cached = null;
    try { cached = JSON.parse(localStorage.getItem('lc_gh_user') || 'null'); } catch(e){}
    if (cached && localStorage.getItem('lc_gh_user_for') === stored) {
      _user = cached;
      document.getElementById('lcw-pat').value = '••••••••••••';
      populateUserCard();
      // skip to step 3 if already validated
      lcwDone(1); lcwDone(2); lcwActivate(3);
    }
  }

  function populateUserCard() {
    if (!_user) return;
    var c = document.getElementById('lcw-user-card');
    c.style.display = 'flex';
    document.getElementById('lcw-uc-avatar').src = _user.avatar_url;
    document.getElementById('lcw-uc-name').textContent = _user.name || _user.login;
    document.getElementById('lcw-uc-login').textContent = '@' + _user.login;
    // also populate done card
    document.getElementById('lcw-done-avatar').src = _user.avatar_url;
    document.getElementById('lcw-done-welcome').textContent = 'Welcome, ' + (_user.name || _user.login) + '! 🎉';
    var repo = _user.login + '/lightcodepedia';
    var url = 'https://' + _user.login + '.github.io/lightcodepedia';
    document.getElementById('lcw-done-url').textContent = url;
    document.getElementById('lcw-done-url').href = url;
  }

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
        var hasRepo = d.scopes.split(',').map(function(s){return s.trim();}).indexOf('repo') >= 0;
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
        res.textContent = '✅ Key is valid — logged in as @' + d.user.login + ' with repo access.';
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

  // activate step 1 on load
  lcwActivate(1);
})();
</script>

{% include backtotop.md %}
