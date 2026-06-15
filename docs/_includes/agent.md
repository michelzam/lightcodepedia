{%- comment -%}
AI agent widget — single-shot chat panel that calls GitHub Models.

Author syntax (minimum):
  ```yaml
  system: You are a Python tutor.
  ```
  {: .agent }

Bound to a runner (writes code back to a .run editor):
  ```python
  print('fix me'
  ```
  {: .run id="play" }

  ```yaml
  system: You are a Python tutor. Reply with full updated code.
  ```
  {: .agent bound="play" }

YAML knobs (optional):
  system, model, temperature, max_tokens, intro, placeholder,
  title, icon  (panel header text + emoji — default "Agent" / 🤖;
                set title: Ari to brand the panel as the guide)
IAL knobs:
  id="..."    required when there are multiple agents on a page
  rows="3"    prompt input height
  bound="X"   ties this agent to the .run widget with id="X" —
              the editor's current code + last output are
              auto-appended to every prompt, and the first python
              code block in the response gets an "⬇ Apply to #X"
              button.

The learner's PAT is asked once per page. All agents share it.
The token is held in a JS closure (in-memory) + the browser's
password manager via the hidden-username form trick. Nothing is
written to localStorage or cookies.

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-agent { border: 1px solid #e0e0e0; border-radius: 8px; margin: 1em 0; background: white; overflow: hidden; font-size: 0.95em; }
.lc-agent-head { background: linear-gradient(135deg, #f5f5f5 0%, #fafafa 100%); padding: 0.55em 1em; border-bottom: 1px solid #e0e0e0; display: flex; align-items: center; gap: 0.5em; font-weight: 600; color: #444; font-size: 0.92em; }
.lc-agent-icon { font-size: 1.2em; }
.lc-agent-title { flex: 1; }
.lc-agent-bound { font-size: 0.78em; color: #888; font-weight: 400; }
.lc-agent-bound code { background: #eef; padding: 0.05em 0.4em; border-radius: 3px; font-size: 0.95em; }
.lc-agent-key { background: white; border: 1px solid #ddd; color: #777; padding: 0.2em 0.5em; cursor: pointer; border-radius: 4px; font-size: 0.95em; line-height: 1; }
.lc-agent-key:hover { background: #f0f0f0; color: #444; }
.lc-agent-auth, .lc-agent-body { padding: 0.9em 1em; }
.lc-agent-auth p { margin: 0 0 0.6em; color: #555; font-size: 0.92em; }
.lc-agent-auth input[type="text"] { position: absolute; left: -9999px; }
.lc-agent-pw-row { display: flex; gap: 0.5em; margin-bottom: 0.5em; flex-wrap: wrap; }
.lc-agent-token { flex: 1; min-width: 200px; padding: 0.5em 0.7em; border: 1px solid #ccc; border-radius: 4px; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.88em; box-sizing: border-box; }
.lc-agent-token:focus { outline: 2px solid #0066cc; border-color: #0066cc; }
.lc-agent-auth button[type="submit"] { background: #0066cc; color: white; border: none; padding: 0.5em 1.1em; border-radius: 4px; cursor: pointer; font-weight: 500; font-size: 0.9em; }
.lc-agent-auth button[type="submit"]:hover { background: #0052a3; }
.lc-agent-help { font-size: 0.83em; color: #666; text-decoration: none; }
.lc-agent-help:hover { color: #0066cc; text-decoration: underline; }
.lc-agent-intro { margin: 0 0 0.7em; color: #666; font-style: italic; font-size: 0.9em; }
.lc-agent-ask { display: flex; gap: 0.5em; margin-bottom: 0.6em; align-items: flex-start; }
.lc-agent-prompt { flex: 1; padding: 0.5em 0.7em; border: 1px solid #ccc; border-radius: 4px; font: inherit; font-size: 0.92em; resize: vertical; min-height: 2.5em; box-sizing: border-box; }
.lc-agent-prompt:focus { outline: 2px solid #0066cc; border-color: #0066cc; }
.lc-agent-send { background: #0066cc; color: white; border: none; padding: 0.5em 1em; border-radius: 4px; cursor: pointer; font-weight: 500; font-size: 0.9em; white-space: nowrap; }
.lc-agent-send:hover:not(:disabled) { background: #0052a3; }
.lc-agent-send:disabled { background: #aaa; cursor: progress; }
.lc-agent-status { margin-bottom: 0.4em; min-height: 0; }
.lc-agent-status:empty { display: none; }
.lc-agent-err { color: #c62828; font-size: 0.88em; background: #fff5f5; padding: 0.4em 0.7em; border-radius: 4px; border: 1px solid #ffcdd2; display: inline-block; }
.lc-agent-response { margin-bottom: 0.6em; }
.lc-agent-response:empty { display: none; }
.lc-agent-msg-user { background: #e3f2fd; color: #1565c0; padding: 0.55em 0.85em; border-radius: 8px 8px 8px 2px; margin-bottom: 0.6em; font-size: 0.9em; white-space: pre-wrap; word-break: break-word; }
.lc-agent-msg-bot { background: #f5f5f5; color: #222; padding: 0.7em 0.95em; border-radius: 8px 8px 2px 8px; font-size: 0.94em; line-height: 1.55; word-break: break-word; }
.lc-agent-msg-bot p:first-child { margin-top: 0; }
.lc-agent-msg-bot p:last-child { margin-bottom: 0; }
.lc-agent-msg-bot pre.lc-agent-code { background: #1e1e1e; color: #d4d4d4; padding: 0.7em 0.9em; border-radius: 4px; overflow-x: auto; font-size: 0.84em; margin: 0.5em 0; }
.lc-agent-msg-bot pre.lc-agent-code code { background: transparent; padding: 0; font-size: inherit; color: inherit; }
.lc-agent-msg-bot code { background: #eef; padding: 0.1em 0.35em; border-radius: 3px; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.88em; }
.lc-agent-apply-bar { display: flex; gap: 0.5em; align-items: center; margin: -0.2em 0 0.5em; font-size: 0.85em; color: #555; }
.lc-agent-apply { background: #2e7d32; color: white; border: none; padding: 0.35em 0.85em; border-radius: 4px; cursor: pointer; font-weight: 500; font-size: 0.85em; }
.lc-agent-apply:hover { background: #1b5e20; }
.lc-agent-revert { background: white; color: #2e7d32; border: 1px solid #2e7d32; padding: 0.3em 0.7em; border-radius: 4px; cursor: pointer; font-size: 0.82em; }
.lc-agent-revert:hover { background: #f1f8e9; }
.lc-agent-usage { font-size: 0.78em; color: #888; text-align: right; padding-top: 0.5em; border-top: 1px solid #eee; }
.lc-agent-warn { font-size: 0.78em; color: #888; padding: 0 1em 0.7em; }
</style>
<script>
(function(){
  var AGENT_SEQ = 0;

  // ===== shared token state — one token per page, all agents observe =====
  var SHARED = { token: null, listeners: [] };
  function setSharedToken(v) {
    SHARED.token = v;
    SHARED.listeners.forEach(function(cb){ try { cb(v); } catch (e) {} });
  }
  function onSharedTokenChange(cb) { SHARED.listeners.push(cb); }

  // ===== utils =====
  function loadJsYaml() {
    if (window.jsyaml) return Promise.resolve();
    return new Promise(function(resolve){
      var existing = document.querySelector('script[src*="js-yaml"]');
      if (existing) { existing.addEventListener('load', resolve); return; }
      var s = document.createElement('script');
      s.src = 'https://cdn.jsdelivr.net/npm/js-yaml@4/dist/js-yaml.min.js';
      s.onload = function(){ resolve(); };
      s.onerror = function(){ resolve(); };
      document.head.appendChild(s);
    });
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function(c){
      return ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c];
    });
  }

  function renderMarkdown(text) {
    // Step 1: extract code blocks to placeholders so their newlines survive
    var blocks = [];
    var staged = String(text).replace(/```(\w*)\n?([\s\S]*?)```/g, function(_, lang, code){
      var idx = blocks.length;
      blocks.push({ lang: (lang || '').toLowerCase(), code: code.replace(/\n+$/, '') });
      return '@@LCAGENTCB' + idx + '@@';
    });
    // Step 2: escape + inline + paragraph + linebreak on the rest
    var html = escapeHtml(staged);
    html = html.replace(/`([^`\n]+)`/g, '<code>$1</code>');
    html = html.replace(/\*\*([^*\n]+)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/(^|[^*])\*([^*\n]+)\*(?!\*)/g, '$1<em>$2</em>');
    html = html.replace(/\n\n+/g, '</p><p>');
    html = html.replace(/\n/g, '<br>');
    // Step 3: restore code blocks with properly-escaped content
    html = html.replace(/@@LCAGENTCB(\d+)@@/g, function(_, idx){
      var b = blocks[parseInt(idx, 10)];
      var lc = b.lang ? ' class="language-' + b.lang + '"' : '';
      return '<pre class="lc-agent-code"><code' + lc + '>' + escapeHtml(b.code) + '</code></pre>';
    });
    return '<p>' + html + '</p>';
  }

  // ===== bound runner helpers =====
  function findRunner(boundId) {
    if (!boundId) return null;
    return document.getElementById('lc-pyrun-' + boundId);
  }
  function getBoundCode(boundId) {
    var r = findRunner(boundId);
    if (!r) return null;
    var ta = r.querySelector('.lc-pyrun-code');
    return ta ? ta.value : null;
  }
  function getBoundOutput(boundId) {
    var r = findRunner(boundId);
    if (!r) return null;
    var out = r.querySelector('.lc-pyrun-out');
    if (!out) return null;
    if (out.classList.contains('lc-empty')) return null;
    var t = (out.textContent || '').trim();
    return t || null;
  }
  function setBoundCode(boundId, code) {
    var r = findRunner(boundId);
    if (!r) return false;
    var ta = r.querySelector('.lc-pyrun-code');
    if (!ta) return false;
    ta.value = code;
    try { ta.dispatchEvent(new Event('input', { bubbles: true })); } catch (e) {}
    return true;
  }

  function buildAugmentedPrompt(boundId, userQuestion) {
    if (!boundId) return userQuestion;
    var code = getBoundCode(boundId);
    if (code == null) return userQuestion;
    var output = getBoundOutput(boundId);
    var trimmedCode = code.length > 4000 ? code.substring(0, 4000) + '\n# ...[truncated]' : code;
    var parts = [
      'The student is editing this Python code in editor #' + boundId + ':',
      '',
      '```python',
      trimmedCode,
      '```'
    ];
    if (output) {
      parts.push('', 'The last run produced this output:', '', '```', output, '```');
    }
    parts.push('', 'The student asks:', '', userQuestion);
    return parts.join('\n');
  }

  // ===== config defaults =====
  var DEFAULTS = {
    system: 'You are a helpful assistant.',
    model: 'openai/gpt-4o-mini',
    intro: '',
    placeholder: 'Ask anything...',
    temperature: 0.7,
    max_tokens: 500,
    title: 'Agent',
    icon: '🤖'
  };

  // ===== panel structure =====
  function buildPanel(id, cfg, rows, boundId) {
    var div = document.createElement('div');
    div.className = 'lc-agent';
    div.id = 'lc-agent-' + id;
    var introHtml = cfg.intro ? '<p class="lc-agent-intro">' + escapeHtml(cfg.intro) + '</p>' : '';
    var boundLabel = boundId ? '<span class="lc-agent-bound">linked to <code>#' + escapeHtml(boundId) + '</code></span>' : '';
    div.innerHTML =
      '<div class="lc-agent-head">' +
        '<span class="lc-agent-icon" aria-hidden="true">' + escapeHtml(cfg.icon) + '</span>' +
        '<span class="lc-agent-title">' + escapeHtml(cfg.title) + '</span>' +
        boundLabel +
        '<button type="button" class="lc-agent-key" title="Change token" aria-label="Change token">🔑</button>' +
      '</div>' +
      '<form class="lc-agent-auth" autocomplete="on">' +
        '<p>Paste your GitHub PAT. Your browser may offer to save it (encrypted in the OS keychain). One token covers every agent on this page.</p>' +
        '<input type="text" name="username" value="github-models" autocomplete="username" tabindex="-1" readonly>' +
        '<div class="lc-agent-pw-row">' +
          '<input type="password" name="password" class="lc-agent-token" autocomplete="current-password" placeholder="ghp_..." required>' +
          '<button type="submit">Save &amp; start</button>' +
        '</div>' +
        '<a class="lc-agent-help" href="https://github.com/settings/tokens" target="_blank" rel="noopener">How do I get one?</a>' +
      '</form>' +
      '<div class="lc-agent-body" hidden>' +
        introHtml +
        '<form class="lc-agent-ask">' +
          '<textarea class="lc-agent-prompt" rows="' + rows + '" placeholder="' + escapeHtml(cfg.placeholder) + '"></textarea>' +
          '<button type="submit" class="lc-agent-send">▶ Ask</button>' +
        '</form>' +
        '<div class="lc-agent-status" role="status" aria-live="polite"></div>' +
        '<div class="lc-agent-response"></div>' +
        '<div class="lc-agent-usage">Used 0 tokens this session.</div>' +
      '</div>' +
      '<div class="lc-agent-warn">⚠ Calls models.github.ai directly with your PAT. Don\'t use a PAT with broad scopes here.</div>';
    return div;
  }

  // ===== API call =====
  function ask(token, cfg, userText) {
    var url = 'https://models.github.ai/inference/chat/completions';
    var body = {
      model: cfg.model,
      messages: [
        { role: 'system', content: String(cfg.system) },
        { role: 'user', content: userText }
      ]
    };
    if (cfg.temperature != null) body.temperature = Number(cfg.temperature);
    if (cfg.max_tokens != null) body.max_tokens = parseInt(cfg.max_tokens, 10);
    return fetch(url, {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body)
    }).then(function(r){
      return r.json().then(function(data){ return { status: r.status, data: data }; })
        .catch(function(){ return { status: r.status, data: {} }; });
    }).then(function(result){
      if (result.status === 401 || result.status === 403) {
        return { error: 'Token rejected (' + result.status + '). Try a fresh PAT.', unauthorized: true };
      }
      if (result.status === 429) {
        return { error: 'Rate limited (429). Wait a moment and retry.' };
      }
      if (result.status >= 400) {
        var msg = (result.data && result.data.error && result.data.error.message) || ('HTTP ' + result.status);
        return { error: msg };
      }
      var choice = result.data.choices && result.data.choices[0];
      if (!choice) return { error: 'Empty response from API.' };
      return {
        text: (choice.message && choice.message.content) || '',
        usage: result.data.usage || null
      };
    }).catch(function(err){
      return { error: 'Network error: ' + (err.message || String(err)) };
    });
  }

  // ===== wire one panel =====
  function wirePanel(panel, cfg, boundId) {
    var totalTokens = 0;
    var authForm = panel.querySelector('.lc-agent-auth');
    var body = panel.querySelector('.lc-agent-body');
    var askForm = panel.querySelector('.lc-agent-ask');
    var prompt = panel.querySelector('.lc-agent-prompt');
    var sendBtn = panel.querySelector('.lc-agent-send');
    var status = panel.querySelector('.lc-agent-status');
    var response = panel.querySelector('.lc-agent-response');
    var usage = panel.querySelector('.lc-agent-usage');
    var keyBtn = panel.querySelector('.lc-agent-key');
    var tokenInput = panel.querySelector('.lc-agent-token');

    function showChat() { authForm.hidden = true; body.hidden = false; }
    function showAuth() { authForm.hidden = false; body.hidden = true; }

    // Initial state from shared token
    if (SHARED.token) showChat(); else showAuth();

    // React to other panels changing the token
    onSharedTokenChange(function(v){
      if (v) showChat(); else { response.innerHTML = ''; status.innerHTML = ''; showAuth(); }
    });

    authForm.addEventListener('submit', function(e){
      e.preventDefault();
      var v = (tokenInput.value || '').trim();
      if (!v) return;
      setSharedToken(v);  // all other panels switch to chat
    });

    keyBtn.addEventListener('click', function(){
      setSharedToken(null);  // all panels switch to auth
    });

    askForm.addEventListener('submit', function(e){
      e.preventDefault();
      var question = (prompt.value || '').trim();
      if (!SHARED.token || !question) return;
      sendBtn.disabled = true;
      sendBtn.textContent = '… thinking';
      status.innerHTML = '';
      response.innerHTML = '';

      var fullPrompt = buildAugmentedPrompt(boundId, question);

      ask(SHARED.token, cfg, fullPrompt).then(function(result){
        sendBtn.disabled = false;
        sendBtn.textContent = '▶ Ask';
        if (result.error) {
          status.innerHTML = '<span class="lc-agent-err">⚠ ' + escapeHtml(result.error) + '</span>';
          if (result.unauthorized) setSharedToken(null);
          return;
        }
        response.innerHTML =
          '<div class="lc-agent-msg-user">' + escapeHtml(question) + '</div>' +
          '<div class="lc-agent-msg-bot">' + renderMarkdown(result.text) + '</div>';

        // If bound: add an Apply button to the first python code block in the response.
        if (boundId) {
          var bot = response.querySelector('.lc-agent-msg-bot');
          var codeBlocks = bot.querySelectorAll('pre.lc-agent-code');
          var first = null;
          for (var i = 0; i < codeBlocks.length; i++) {
            var c = codeBlocks[i].querySelector('code');
            var lang = (c && c.className.match(/language-(\w+)/)) || [];
            if (!lang[1] || lang[1] === 'python' || lang[1] === 'py') { first = codeBlocks[i]; break; }
          }
          if (first) {
            var applyBar = document.createElement('div');
            applyBar.className = 'lc-agent-apply-bar';
            first.parentNode.insertBefore(applyBar, first.nextSibling);

            function renderApply() {
              applyBar.style.opacity = '1';
              applyBar.innerHTML = '<button class="lc-agent-apply" type="button">⬇ Apply to #' + escapeHtml(boundId) + '</button>';
              applyBar.querySelector('.lc-agent-apply').addEventListener('click', doApply);
            }
            function doApply() {
              var newCode = first.querySelector('code').textContent;
              var prevCode = getBoundCode(boundId);
              if (!setBoundCode(boundId, newCode)) return;
              applyBar.style.opacity = '1';
              applyBar.innerHTML = '<span style="color:#2e7d32; font-weight:600">✓ Applied</span> ' +
                '<button class="lc-agent-revert" type="button">↺ Revert</button>';
              applyBar.querySelector('.lc-agent-revert').addEventListener('click', function(){
                setBoundCode(boundId, prevCode != null ? prevCode : '');
                renderApply();
              });
              setTimeout(function(){
                if (applyBar.parentNode && applyBar.querySelector('.lc-agent-revert')) {
                  applyBar.style.opacity = '0.55';
                }
              }, 10000);
            }
            renderApply();
          }
        }

        if (result.usage) {
          var t = result.usage.total_tokens || 0;
          totalTokens += t;
          usage.textContent = 'Session: ' + totalTokens + ' tokens · this ask: ' + t +
            ' (' + (result.usage.prompt_tokens || 0) + ' prompt + ' +
            (result.usage.completion_tokens || 0) + ' reply).';
        }
        prompt.value = '';
      });
    });
  }

  // ===== upgrade one .agent block =====
  function upgradeAgent(el) {
    if (el.dataset.lcAgentUpgraded) return;
    el.dataset.lcAgentUpgraded = '1';
    var codeNode = el.querySelector('code');
    var raw = codeNode ? codeNode.textContent.replace(/\n+$/, '') : '';
    var cfg = {};
    if (window.jsyaml) {
      try { cfg = window.jsyaml.load(raw) || {}; } catch (e) {}
    }
    if (typeof cfg !== 'object' || Array.isArray(cfg)) cfg = {};
    Object.keys(DEFAULTS).forEach(function(k){
      if (cfg[k] === undefined) cfg[k] = DEFAULTS[k];
    });
    var id = el.getAttribute('id') || ('agent-' + (++AGENT_SEQ));
    var rows = parseInt(el.getAttribute('rows'), 10) || 3;
    var boundId = el.getAttribute('bound') || null;
    var panel = buildPanel(id, cfg, rows, boundId);
    // Slides partition runs before agent upgrade (it has to wait for js-yaml).
    // Carry the fragment marking from the original code-block to the new panel
    // so it stays in the slide reveal sequence.
    if (el.classList.contains('lc-slide-fragment')) {
      panel.classList.add('lc-slide-fragment');
      var rev = el.getAttribute('data-revealed');
      if (rev != null) panel.setAttribute('data-revealed', rev);
    }
    el.parentNode.replaceChild(panel, el);
    wirePanel(panel, cfg, boundId);
  }

  function init() {
    var els = document.querySelectorAll('.highlighter-rouge.agent, pre.agent, div.agent[class*="language-"]');
    Array.prototype.forEach.call(els, upgradeAgent);
  }

  window.lcUpgradeAgent = function(el) { loadJsYaml().then(function() { upgradeAgent(el); }); };

  function start() { loadJsYaml().then(init); }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function(){ setTimeout(start, 0); });
  } else {
    setTimeout(start, 0);
  }
})();
</script>
