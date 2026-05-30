{%- comment -%}
AI agent widget — turns a YAML config block into a single-shot chat panel
that calls the GitHub Models API directly from the browser.

Author syntax:
  ```yaml
  system: You are a Python tutor.
  ```
  {: .agent }

Knobs (all optional):
  system, model, temperature, max_tokens, intro, placeholder
plus on the IAL:
  id="..."   required if multiple agents on the same page
  rows="3"   prompt input height

The learner's PAT is asked once and held in a JS closure. The token
input uses the hidden-username + visible-password form pattern so
browser password managers (encrypted by the OS keychain) can offer
to save it. Nothing is written to localStorage or cookies.

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-agent { border: 1px solid #e0e0e0; border-radius: 8px; margin: 1em 0; background: white; overflow: hidden; font-size: 0.95em; }
.lc-agent-head { background: linear-gradient(135deg, #f5f5f5 0%, #fafafa 100%); padding: 0.55em 1em; border-bottom: 1px solid #e0e0e0; display: flex; align-items: center; gap: 0.5em; font-weight: 600; color: #444; font-size: 0.92em; }
.lc-agent-icon { font-size: 1.2em; }
.lc-agent-title { flex: 1; }
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
.lc-agent-usage { font-size: 0.78em; color: #888; text-align: right; padding-top: 0.5em; border-top: 1px solid #eee; }
.lc-agent-warn { font-size: 0.78em; color: #888; padding: 0 1em 0.7em; }
</style>
<script>
(function(){
  var AGENT_SEQ = 0;

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
    var html = escapeHtml(text);
    html = html.replace(/```(\w*)\n?([\s\S]*?)```/g, function(_, lang, code){
      return '<pre class="lc-agent-code"><code>' + code.replace(/\n+$/, '') + '</code></pre>';
    });
    html = html.replace(/`([^`\n]+)`/g, '<code>$1</code>');
    html = html.replace(/\*\*([^*\n]+)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/(^|[^*])\*([^*\n]+)\*(?!\*)/g, '$1<em>$2</em>');
    html = html.replace(/\n\n+/g, '</p><p>');
    html = html.replace(/\n/g, '<br>');
    return '<p>' + html + '</p>';
  }

  var DEFAULTS = {
    system: 'You are a helpful assistant.',
    model: 'openai/gpt-4o-mini',
    intro: '',
    placeholder: 'Ask anything...',
    temperature: 0.7,
    max_tokens: 500
  };

  function buildPanel(id, cfg, rows) {
    var div = document.createElement('div');
    div.className = 'lc-agent';
    div.id = 'lc-agent-' + id;
    var introHtml = cfg.intro ? '<p class="lc-agent-intro">' + escapeHtml(cfg.intro) + '</p>' : '';
    div.innerHTML =
      '<div class="lc-agent-head">' +
        '<span class="lc-agent-icon" aria-hidden="true">🤖</span>' +
        '<span class="lc-agent-title">Agent</span>' +
        '<button type="button" class="lc-agent-key" title="Change token" aria-label="Change token">🔑</button>' +
      '</div>' +
      '<form class="lc-agent-auth" autocomplete="on">' +
        '<p>Paste your GitHub PAT to start. Your browser may offer to save it (encrypted in the OS keychain).</p>' +
        '<input type="text" name="username" value="github-models-' + id + '" autocomplete="username" tabindex="-1" readonly>' +
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
      '<div class="lc-agent-warn">⚠ Calls api.github.com directly with your PAT. Don\'t use a PAT with broad scopes here.</div>';
    return div;
  }

  function ask(token, cfg, question) {
    var url = 'https://models.github.ai/inference/chat/completions';
    var body = {
      model: cfg.model,
      messages: [
        { role: 'system', content: String(cfg.system) },
        { role: 'user', content: question }
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

  function wirePanel(panel, cfg) {
    var token = null;
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

    function showChat() { authForm.hidden = true; body.hidden = false; setTimeout(function(){ prompt.focus(); }, 0); }
    function showAuth() { authForm.hidden = false; body.hidden = true; setTimeout(function(){ tokenInput.focus(); }, 0); }

    authForm.addEventListener('submit', function(e){
      e.preventDefault();
      var v = (tokenInput.value || '').trim();
      if (!v) return;
      token = v;
      showChat();
    });

    keyBtn.addEventListener('click', function(){
      token = null;
      tokenInput.value = '';
      response.innerHTML = '';
      status.innerHTML = '';
      showAuth();
    });

    askForm.addEventListener('submit', function(e){
      e.preventDefault();
      var question = (prompt.value || '').trim();
      if (!token || !question) return;
      sendBtn.disabled = true;
      sendBtn.textContent = '… thinking';
      status.innerHTML = '';
      response.innerHTML = '';

      ask(token, cfg, question).then(function(result){
        sendBtn.disabled = false;
        sendBtn.textContent = '▶ Ask';
        if (result.error) {
          status.innerHTML = '<span class="lc-agent-err">⚠ ' + escapeHtml(result.error) + '</span>';
          if (result.unauthorized) { token = null; showAuth(); }
          return;
        }
        response.innerHTML =
          '<div class="lc-agent-msg-user">' + escapeHtml(question) + '</div>' +
          '<div class="lc-agent-msg-bot">' + renderMarkdown(result.text) + '</div>';
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
    var panel = buildPanel(id, cfg, rows);
    el.parentNode.replaceChild(panel, el);
    wirePanel(panel, cfg);
  }

  function init() {
    var els = document.querySelectorAll('.highlighter-rouge.agent, pre.agent, div.agent[class*="language-"]');
    Array.prototype.forEach.call(els, upgradeAgent);
  }

  function start() {
    loadJsYaml().then(init);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function(){ setTimeout(start, 0); });
  } else {
    setTimeout(start, 0);
  }
})();
</script>
