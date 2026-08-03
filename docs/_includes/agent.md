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
  {: .run #play }

  ```yaml
  system: You are a Python tutor. Reply with full updated code.
  ```
  {: .agent bound="play" }

YAML knobs (optional):
  system, model, temperature, max_tokens, intro, placeholder
  provider: gemini | openrouter | custom   (default gemini)
  base_url: https://…   override the endpoint (OpenAI-compatible dialect) —
            THE portability valve: a dead provider costs one yaml line.
            (GitHub Models died 2026-07-30 with a 410; never again.)
IAL knobs:
  id="..."    required when there are multiple agents on a page
  rows="3"    prompt input height
  bot="doc"   load persona + settings from docs/bots/doc.md — the file's
              markdown IS the system prompt; its yaml fence sets model/name/
              intro/placeholder and knowledge: [self, /page, …] (those pages'
              raw markdown is stuffed into the system prompt, trimmed to
              knowledge_budget chars, default 16000). Works on a paragraph
              too: "Ask Doc. {: .agent bot=doc }" — the text becomes the
              intro. Page fence knobs override the bot's.
  bound="X"   ties this agent to the .run widget with id="X" —
              the editor's current code + last output are
              auto-appended to every prompt, and the first python
              code block in the response gets an "⬇ Apply to #X"
              button.
  bound="{=expr}"  the second grammar (told apart by syntax — the legacy
              editor binding is untouched): evaluate a CELL expression at
              Ask time and hand the value to the model. {=cv1.source}
              reads a pad, {=inputs.field} a form — anything cells see.

The learner's key is asked ONCE — per device, not per page. It is
persisted per provider (like the course key) and offered to the
browser's password manager via the hidden-username form trick, so
the other devices get it by autofill. 🔑 forgets it everywhere.

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-agent { border: 1px solid #e0e0e0; border-radius: 8px; margin: 1em 0; background: white; overflow: hidden; font-size: 0.95em; }
.lc-agent-head { background: linear-gradient(135deg, #f5f5f5 0%, #fafafa 100%); padding: 0.55em 1em; border-bottom: 1px solid #e0e0e0; display: flex; align-items: center; gap: 0.5em; font-weight: 600; color: #444; font-size: 0.92em; }
.lc-agent-icon { font-size: 1.2em; }
.lc-agent-title { flex: 1; }
.lc-agent-bound { font-size: 0.78em; color: var(--lc-ink-mute, #616161); font-weight: 400; }
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
.lc-agent-warn { font-size: 0.78em; color: var(--lc-ink-mute, #616161); padding: 0 1em 0.7em; }
</style>
<script>
(function(){
  var AGENT_SEQ = 0;

  // ===== shared token state — one token per page, all agents observe =====
  // If the ✏️ editor is connected on this device, borrow its PAT silently —
  // same token, same GitHub, no re-pasting ceremony ("one token for
  // everything", as the docs teach). A 401 clears it and the normal
  // paste-once flow takes over. Nothing new is stored.
  /* one key per PROVIDER (persisted on the device + the browser's password
     manager, keyed by provider so keychain entries never collide). The old
     silent borrow of the editor's GitHub PAT died with GitHub Models —
     a repo key is not a model key. */
  var SHARED = { tokens: {}, listeners: [] };
  /* Persisted per provider, like the course key (lc_ed_pat) — the energy
     key is saved once, at the join door or any desk, and every page after
     opens connected (Michel 2026-08-03: 'saved automatically as the other
     keys'). In-memory-only was the GitHub-PAT-era posture; an AI key is
     scoped to spending its own free quota, and re-pasting it on every page
     was the actual risk — learners give up. */
  function getSharedToken(pid) {
    if (SHARED.tokens[pid]) return SHARED.tokens[pid];
    try { return localStorage.getItem("lc_ai_key_" + pid) || null; } catch (e) { return null; }
  }
  function setSharedToken(pid, v) {
    SHARED.tokens[pid] = v;
    try {
      if (v) localStorage.setItem("lc_ai_key_" + pid, v);
      else localStorage.removeItem("lc_ai_key_" + pid);
    } catch (e) {}
    SHARED.listeners.forEach(function(cb){ try { cb(pid, v); } catch (e) {} });
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
  /* One dialect, any engine: every provider below speaks OpenAI-compatible
     chat/completions with a Bearer key. GitHub Models spoke it too — and
     retired on 2026-07-30 with a 410 on the preflight. The lesson is
     permanent: the provider is CONFIGURATION, never architecture. A dead
     provider costs a yaml line (provider: / base_url:), not a course. */
  var PROVIDERS = {
    gemini: {
      base: 'https://generativelanguage.googleapis.com/v1beta/openai',
      /* the -latest alias rides Google's version churn (2.5 retires
         2026-10; 3.6 is today's GA) — a pinned version would 404 twice a
         year, an alias never does */
      model: 'gemini-flash-latest',
      key_name: 'Google AI Studio key',
      key_url: 'https://aistudio.google.com/apikey',
      key_hint: 'AIza...'
    },
    openrouter: {
      base: 'https://openrouter.ai/api/v1',
      model: 'meta-llama/llama-3.3-70b-instruct:free',
      key_name: 'OpenRouter key',
      key_url: 'https://openrouter.ai/keys',
      key_hint: 'sk-or-...'
    },
    custom: { base: '', model: '', key_name: 'API key', key_url: '', key_hint: 'sk-...' }
  };
  var DEFAULT_PROVIDER = 'gemini';

  var DEFAULTS = {
    system: 'You are a helpful assistant.',
    provider: DEFAULT_PROVIDER,
    base_url: '',
    model: '',
    intro: '',
    placeholder: 'Ask anything...',
    temperature: 0.7,
    /* today's models THINK before they answer, and the thinking spends
       this same allowance — 500 left a 19-token fragment on the screen.
       Budget for reasoning + reply, or learners read truncated answers. */
    max_tokens: 2000
  };

  /* resolve provider preset + per-fence overrides into {base, model, …} */
  function resolveEngine(cfg) {
    var pv = PROVIDERS[cfg.provider] || PROVIDERS[DEFAULT_PROVIDER];
    var base = (cfg.base_url || pv.base || '').replace(/\/+$/, '');
    return {
      base: base,
      host: (base.match(/^https?:\/\/([^\/]+)/) || [])[1] || 'the model service',
      model: cfg.model || pv.model,
      key_name: pv.key_name, key_url: pv.key_url, key_hint: pv.key_hint,
      id: cfg.provider || DEFAULT_PROVIDER
    };
  }

  // ===== bots: superprompt + knowledge as repo markdown (SSOT) =====
  // A bot is a file: docs/bots/<name>.md — the markdown body IS the system
  // prompt; one yaml fence inside it carries settings (model, temperature,
  // name, intro, placeholder, knowledge: [...pages or self], knowledge_budget).
  // Knowledge is honest context-stuffing: the listed pages' own markdown,
  // fetched raw and folded into the system prompt, trimmed to the budget.
  var _lcSiteRepo = {{ site.github.repository_nwo | default: "" | jsonify }};
  var _botCache = {};
  function rawUrl(mdPath) {
    return 'https://raw.githubusercontent.com/' + _lcSiteRepo + '/main/' + mdPath;
  }
  function pageMdPath(urlPath) {   /* /components/quiz → docs/components/quiz.md */
    var p = String(urlPath || '').replace(/\.html?$/, '').replace(/\/+$/, '');
    if (!p || p === '/') return 'docs/index.md';
    if (p.charAt(0) !== '/') p = '/' + p;
    return 'docs' + p + '.md';
  }
  function fetchText(url) {
    return fetch(url).then(function(r){ if (!r.ok) throw new Error('HTTP ' + r.status + ' for ' + url); return r.text(); })
      .catch(function(err){
        /* A PRIVATE repo (the lab, a bench) 404s on raw.githubusercontent with
           no auth — so a bot file / knowledge page can't be read there. Retry
           through the Contents API with the connected key (raw media type),
           the same fallback the runner uses. Public repos never reach here. */
        var m = /^https:\/\/raw\.githubusercontent\.com\/([^\/]+)\/([^\/]+)\/[^\/]+\/(.+)$/.exec(url);
        var pat = ''; try { pat = localStorage.getItem('lc_ed_pat') || localStorage.getItem('lc_org_pat') || ''; } catch (e) {}
        if (!m || !pat) throw err;
        return fetch('https://api.github.com/repos/' + m[1] + '/' + m[2] + '/contents/' + m[3],
          { headers: { Authorization: 'Bearer ' + pat, Accept: 'application/vnd.github.v3.raw', 'X-GitHub-Api-Version': '2022-11-28' }, cache: 'no-store' })
          .then(function(r){ if (!r.ok) throw new Error('HTTP ' + r.status + ' (contents) for ' + m[3]); return r.text(); });
      });
  }
  function parseBot(md) {
    var m = /```yaml\r?\n([\s\S]*?)```/.exec(md);
    var cfg = {};
    if (m && window.jsyaml) { try { cfg = window.jsyaml.load(m[1]) || {}; } catch (e) {} }
    var system = md.replace(m ? m[0] : '', '').replace(/\{:[^}]*\}/g, '').trim();
    return { system: system, cfg: (typeof cfg === 'object' && !Array.isArray(cfg)) ? cfg : {} };
  }
  /* A page-level runner render advertises the file it shows (the same
     data-lc-src contract embeds, xray and .folder follow). There, "self"
     must mean THAT file — a tutor on /run answering about docs/run.md was
     reading the vehicle, not the course (module_00, 2026-07-30). */
  function rtSrc() {
    var r = document.querySelector('#lc-run[data-lc-src-path]');
    if (!r || !r.dataset.lcSrcRepo || !r.dataset.lcSrcPath) return null;
    var dir = r.dataset.lcSrcPath.split('/').slice(0, -1).join('/');
    if (/^docs(\/|$)/.test(dir)) return null;   // a docs render keys as the site page
    return { repo: r.dataset.lcSrcRepo, path: r.dataset.lcSrcPath };
  }
  function loadBot(name) {
    var key = String(name || '').replace(/[^\w-]/g, '');
    var rt = rtSrc();
    /* one knowledge set per rendered course — /run swaps courses on
       hashchange without a reload, and a cached bot must not answer the
       next module with the previous module's material */
    if (rt) key += '|' + rt.repo + '/' + rt.path;
    if (_botCache[key]) return _botCache[key];
    _botCache[key] = fetchText(rawUrl('docs/bots/' + String(name || '').replace(/[^\w-]/g, '') + '.md')).then(function(md){
      var bot = parseBot(md);
      var cfg = { system: bot.system || DEFAULTS.system };
      Object.keys(bot.cfg).forEach(function(k){ if (k !== 'knowledge' && k !== 'knowledge_budget') cfg[k] = bot.cfg[k]; });
      var know = bot.cfg.knowledge;
      var budget = parseInt(bot.cfg.knowledge_budget, 10) || 16000;
      if (!Array.isArray(know) || !know.length) return cfg;
      return Promise.all(know.map(function(k){
        if (String(k) === 'self' && rt) {
          /* self = the RENDERED course file — and the fragments it embeds:
             a module composes from {: .embed } siblings, and a tutor focused
             on "the content" must read what the learner is reading */
          var base = 'https://raw.githubusercontent.com/' + rt.repo + '/HEAD/';
          return fetchText(base + rt.path).then(function(t){
            var dir = rt.path.split('/').slice(0, -1).join('/');
            /* lcEmbedRefs (widgets.md) is the SSOT for embed references —
               same resolution the widget itself uses to render them */
            var targets = window.lcEmbedRefs ? window.lcEmbedRefs(t, dir) : [];
            return Promise.all(targets.map(function(fp){
              return fetchText(base + fp)
                .then(function(x){ return '\n\n--- Embedded: ' + fp + ' ---\n' + x; })
                .catch(function(){ return ''; });
            })).then(function(embeds){
              return { path: rt.repo + '/' + rt.path, text: t + embeds.join('') };
            });
          }).catch(function(){ return null; });
        }
        var path = (String(k) === 'self') ? pageMdPath(window.lcPagePath ? window.lcPagePath() : location.pathname) : pageMdPath(k);
        return fetchText(rawUrl(path)).then(function(t){ return { path: path, text: t }; })
          .catch(function(){
            /* index pages: /section/ lives at section/index.md */
            var alt = path.replace(/\.md$/, '/index.md');
            return fetchText(rawUrl(alt)).then(function(t){ return { path: alt, text: t }; })
              .catch(function(){ return null; });
          });
      })).then(function(parts){
        var used = 0, chunks = [], trimmed = false;
        parts.filter(Boolean).forEach(function(p){
          if (used >= budget) { trimmed = true; return; }
          var t = p.text.length > (budget - used) ? p.text.slice(0, budget - used) : p.text;
          if (t.length < p.text.length) trimmed = true;
          used += t.length;
          chunks.push('--- Course material: ' + p.path + ' ---\n' + t);
        });
        if (chunks.length) {
          cfg.system += '\n\nUse the following course material when answering.' +
            (trimmed ? ' (Material was trimmed to fit.)' : '') + '\n\n' + chunks.join('\n\n');
          cfg._knowledge = { pages: chunks.length, chars: used, trimmed: trimmed };
        }
        return cfg;
      });
    });
    return _botCache[key];
  }

  // ===== lcBotAsk — the brain as a service for other components ==========
  // The docked guide (avatar.md) asks questions through here: same bot files,
  // same knowledge stuffing, same in-memory PAT, no second auth system.
  window.lcBotAsk = {
    /* who the brain speaks to — so every UI that asks for a key (the docked
       guide, the join wizard) names the SAME provider, with the same key
       hint and the same keychain identity. One place decides; nobody
       hard-codes a vendor into a prompt again. */
    engine: function () {
      var cfg = {};
      Object.keys(DEFAULTS).forEach(function (k) { cfg[k] = DEFAULTS[k]; });
      return resolveEngine(cfg);
    },
    ready: function () { return !!getSharedToken(DEFAULT_PROVIDER); },
    connect: function (key) { if (key) setSharedToken(DEFAULT_PROVIDER, String(key).trim()); },
    disconnect: function () { setSharedToken(DEFAULT_PROVIDER, null); },
    onChange: onSharedTokenChange,
    ask: function (botName, question, opts) {
      if (!getSharedToken(DEFAULT_PROVIDER)) return Promise.resolve({ error: 'No key' });
      return loadBot(botName).then(function (botCfg) {
        var cfg = {};
        Object.keys(DEFAULTS).forEach(function (k) { cfg[k] = DEFAULTS[k]; });
        Object.keys(botCfg).forEach(function (k) { cfg[k] = botCfg[k]; });
        if (opts && opts.direct) {
          /* the AUTHOR is curating content, not being tutored: no guiding
             questions — direct, complete, keep-worthy answers */
          cfg.system += '\n\nThis question comes from the course AUTHOR curating ' +
            'material, not a student: answer directly and completely, no guiding ' +
            'questions, no withheld solutions. Keep the step format.';
        }
        return ask(getSharedToken(DEFAULT_PROVIDER), cfg, question);
      }, function () {
        return { error: 'bot "' + botName + '" could not be loaded' };
      }).then(function (result) {
        if (result && result.unauthorized) setSharedToken(DEFAULT_PROVIDER, null);
        return result;
      });
    }
  };

  // ===== panel structure =====
  function buildPanel(id, cfg, rows, boundId, boundExpr) {
    var eng = resolveEngine(cfg);
    var div = document.createElement('div');
    div.className = 'lc-agent';
    div.id = 'lc-agent-' + id;
    var introHtml = cfg.intro ? '<p class="lc-agent-intro">' + escapeHtml(cfg.intro) + '</p>' : '';
    var boundLabel = boundId ? '<span class="lc-agent-bound">linked to <code>#' + escapeHtml(boundId) + '</code></span>'
      : boundExpr ? '<span class="lc-agent-bound">reads <code>{=' + escapeHtml(boundExpr) + '}</code></span>' : '';
    div.innerHTML =
      '<div class="lc-agent-head">' +
        '<span class="lc-agent-icon" aria-hidden="true">🤖</span>' +
        '<span class="lc-agent-title">' + escapeHtml(cfg.name || 'Agent') + '</span>' +
        boundLabel +
        '<button type="button" class="lc-agent-key" title="Change token" aria-label="Change token">🔑</button>' +
      '</div>' +
      '<form class="lc-agent-auth" autocomplete="on">' +
        '<p>Paste your ' + escapeHtml(eng.key_name) + ' once — it is saved on this device, and every ' + escapeHtml(eng.id) + ' helper in the course opens connected. Let your browser save it as a password too: that copy follows you to your other devices.</p>' +
        '<input type="text" name="username" value="lc-' + escapeHtml(eng.id) + '" autocomplete="username" tabindex="-1" readonly aria-label="Key account name, used by your password manager">' +
        '<div class="lc-agent-pw-row">' +
          '<input type="password" name="password" class="lc-agent-token" autocomplete="current-password" placeholder="' + escapeHtml(eng.key_hint) + '" required aria-label="' + escapeHtml(eng.key_name) + '">' +
          '<button type="submit">Save &amp; start</button>' +
        '</div>' +
        (eng.key_url ? '<a class="lc-agent-help" href="' + eng.key_url + '" target="_blank" rel="noopener">How do I get one?</a>' : '') +
      '</form>' +
      '<div class="lc-agent-body" hidden>' +
        introHtml +
        '<form class="lc-agent-ask">' +
          '<textarea class="lc-agent-prompt" rows="' + rows + '" placeholder="' + escapeHtml(cfg.placeholder) + '" aria-label="Ask ' + escapeHtml(cfg.name || 'Agent') + '"></textarea>' +
          '<button type="submit" class="lc-agent-send">▶ Ask</button>' +
        '</form>' +
        '<div class="lc-agent-status" role="status" aria-live="polite"></div>' +
        '<div class="lc-agent-response"></div>' +
        '<div class="lc-agent-log" hidden></div>' +
        '<div class="lc-agent-usage">Used 0 tokens this session.</div>' +
      '</div>' +
      '<div class="lc-agent-warn">⚠ Calls ' + escapeHtml(eng.host) + ' directly with your key. Use a key made for this, nothing broader.</div>';
    return div;
  }

  // ===== API call =====
  function ask(token, cfg, userText) {
    var eng = resolveEngine(cfg);
    if (!eng.base) return Promise.resolve({ error: 'No engine configured — set provider: or base_url: on this agent.' });
    var url = eng.base + '/chat/completions';
    var body = {
      model: eng.model,
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
        return { error: 'Key rejected (' + result.status + ') by ' + eng.host + '. 🔑 paste a fresh ' + eng.key_name + '.', unauthorized: true };
      }
      if (result.status === 429) {
        /* TWO different walls answer 429 and the difference matters to a
           learner: per-minute (wait 60s, keep working) vs the DAY's free
           allowance (gone until it resets — no amount of retrying helps).
           The provider says which in its own message; relay it. */
        var e429 = Array.isArray(result.data) ? result.data[0] : result.data;
        var m429 = (e429 && e429.error && e429.error.message) || '';
        var daily = /per\s*day|daily|PerDay|quota exceeded/i.test(m429);
        return { error: daily
          ? '🔋 Out of free energy for today — the day\'s allowance is spent and refills on its own (around midnight US Pacific). Nothing is broken; come back tomorrow, or use a key with a paid plan.'
          : '⏳ Too many questions too fast (per-minute limit). Wait about a minute and ask again — this one refills by itself.' };
      }
      if (result.status >= 400) {
        /* Google wraps errors in an ARRAY ([{error:{…}}]); OpenAI-style
           bodies don't — read both, or the learner sees a bare status
           code instead of the provider's own sentence */
        var eobj = Array.isArray(result.data) ? result.data[0] : result.data;
        var msg = (eobj && eobj.error && eobj.error.message) || ('HTTP ' + result.status);
        return { error: msg + ' (HTTP ' + result.status + ' from ' + eng.host + ')' };
      }
      var choice = result.data.choices && result.data.choices[0];
      if (!choice) return { error: 'Empty response from API.' };
      var text = (choice.message && choice.message.content) || '';
      /* ran out of allowance mid-thought: say so rather than pass a
         fragment off as the answer */
      if (choice.finish_reason === 'length') {
        text = (text ? text + '\n\n' : '') +
          '⚠️ *(cut off — the answer outgrew this agent\'s max_tokens. Ask for something shorter, or raise the knob.)*';
      }
      return { text: text, usage: result.data.usage || null };
    }).catch(function(err){
      /* fetch rejected → no HTTP answer reached the page. Usually the ROAD
         (ad-blocker, VPN, firewall) — but some providers answer errors
         without CORS headers, so a rejected key can also land here dressed
         as a network failure. Name both faces. */
      return { error: "Couldn't reach " + eng.host + " — no answer got through. " +
        "Often an ad-blocker, VPN or firewall on the road; if your network is fine, " +
        "the key itself may be stale or wrong (🔑 paste a fresh " + eng.key_name + "). " +
        "(" + (err.message || String(err)) + ")" };
    });
  }

  // ===== wire one panel =====
  function wirePanel(panel, cfg, boundId, boundExpr) {
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

    var engineId = resolveEngine(cfg).id;
    function myToken() { return getSharedToken(engineId); }
    function showChat() { authForm.hidden = true; body.hidden = false; }
    function showAuth() { authForm.hidden = false; body.hidden = true; }

    // Initial state from this provider's shared key
    if (myToken()) showChat(); else showAuth();

    // React to other panels changing THIS provider's key
    onSharedTokenChange(function(pid, v){
      if (pid !== engineId) return;
      if (v) showChat(); else { response.innerHTML = ''; status.innerHTML = ''; showAuth(); }
    });

    authForm.addEventListener('submit', function(e){
      e.preventDefault();
      var v = (tokenInput.value || '').trim();
      if (!v) return;
      setSharedToken(engineId, v);  // sibling panels of the same provider switch too
    });

    keyBtn.addEventListener('click', function(){
      setSharedToken(engineId, null);
    });

    askForm.addEventListener('submit', function(e){
      e.preventDefault();
      var question = (prompt.value || '').trim();
      if (!myToken() || !question) return;
      sendBtn.disabled = true;
      sendBtn.textContent = '… thinking';
      status.innerHTML = '';
      response.innerHTML = '';

      /* expression binding evaluates NOW — the model reads the document
         as it stands at Ask time, not as it was on page load */
      var promptP = (boundExpr && window.lcCellEval)
        ? window.lcCellEval(boundExpr).then(function (v) {
            return 'The document under review:\n\n```\n' + String(v) + '\n```\n\nThe request:\n\n' + question;
          }).catch(function () { return question; })
        : Promise.resolve(buildAugmentedPrompt(boundId, question));

      promptP.then(function (fullPrompt) {
        return ask(myToken(), cfg, fullPrompt);
      }).then(function(result){
        sendBtn.disabled = false;
        sendBtn.textContent = '▶ Ask';
        if (result.error) {
          status.innerHTML = '<span class="lc-agent-err">⚠ ' + escapeHtml(result.error) + '</span>';
          if (result.unauthorized) setSharedToken(engineId, null);
          return;
        }
        response.innerHTML =
          '<div class="lc-agent-msg-user">' + escapeHtml(question) + '</div>' +
          '<div class="lc-agent-msg-bot">' + renderMarkdown(result.text) + '</div>';

        // The panel shows one exchange at a time, but the SITTING has a
        // memory: every raw answer joins a hidden ledger, so a page's
        // .feature can audit the whole conversation (e.g. compare the
        // VERDICT lines two résumé versions earned).
        var logEl = panel.querySelector('.lc-agent-log');
        if (logEl) {
          var entry = document.createElement('div');
          entry.className = 'lc-agent-log-entry';
          entry.textContent = result.text;
          logEl.appendChild(entry);
        }

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
    var pageCfg = {};
    if (window.jsyaml && raw) {
      try { pageCfg = window.jsyaml.load(raw) || {}; } catch (e) {}
    }
    if (typeof pageCfg !== 'object' || Array.isArray(pageCfg)) pageCfg = {};
    var givenId = el.getAttribute('id') || null;
    var id = givenId || ('agent-' + (++AGENT_SEQ));
    var rows = parseInt(el.getAttribute('rows'), 10) || 3;
    /* bound= has two grammars, told apart by syntax so the legacy meaning
       is never touched: a plain id ties to a .run editor (code + output
       ride every prompt, Apply writes back); "{=expr}" evaluates a cell
       expression at Ask time and hands the VALUE to the model — any
       component property the page's cells can see. */
    var boundRaw = el.getAttribute('bound') || null;
    var boundId = boundRaw, boundExpr = null;
    if (boundRaw && /^\{=/.test(boundRaw.trim())) {
      boundExpr = boundRaw.trim().replace(/^\{=\s*/, '').replace(/\}\s*$/, '');
      boundId = null;
    }
    var botName = el.getAttribute('bot') || pageCfg.bot || null;
    /* a paragraph form — Ask Doc. {: .agent bot="doc" } — uses its text as intro */
    if (!codeNode && el.tagName === 'P' && !pageCfg.intro) {
      var pTxt = (el.textContent || '').trim();
      if (pTxt) pageCfg.intro = pTxt;
      pageCfg = Object.assign({}, pageCfg);
    }
    var botP = botName ? loadBot(botName) : Promise.resolve(null);
    botP.catch(function(){ return null; }).then(function(){ /* keep errors soft */ });
    return botP.then(function(botCfg){ return botCfg; }, function(){ return null; }).then(function(botCfg){
    var cfg = {};
    Object.keys(DEFAULTS).forEach(function(k){ cfg[k] = DEFAULTS[k]; });
    if (botCfg) Object.keys(botCfg).forEach(function(k){ cfg[k] = botCfg[k]; });
    Object.keys(pageCfg).forEach(function(k){ if (k !== 'bot') cfg[k] = pageCfg[k]; });
    if (botName && !botCfg) cfg.intro = '⚠ bot "' + botName + '" could not be loaded — answering with defaults. ' + (cfg.intro || '');
    var panel = buildPanel(id, cfg, rows, boundId, boundExpr);
    // Slides partition runs before agent upgrade (it has to wait for js-yaml).
    // Carry the fragment marking from the original code-block to the new panel
    // so it stays in the slide reveal sequence.
    if (el.classList.contains('lc-slide-fragment')) {
      panel.classList.add('lc-slide-fragment');
      var rev = el.getAttribute('data-revealed');
      if (rev != null) panel.setAttribute('data-revealed', rev);
    }
    /* the panel is the component: name it for the step runtime and expose
       its configuration, so a page's .feature can audit the agent — which
       briefing it runs under, which model. Only an author-given id joins
       the page model (auto ids aren't python names). */
    if (givenId) panel.setAttribute('data-lc-id', givenId);
    panel.setAttribute('data-system', cfg.system || '');
    var _eng = resolveEngine(cfg);
    panel.setAttribute('data-model', _eng.model || '');
    panel.setAttribute('data-provider', _eng.id || '');
    el.parentNode.replaceChild(panel, el);
    wirePanel(panel, cfg, boundId, boundExpr);
    if (cfg._knowledge) {
      var u = panel.querySelector('.lc-agent-usage');
      if (u) u.textContent = '📚 ' + (cfg.name || botName) + ' knows ' + cfg._knowledge.pages +
        ' page(s), ' + Math.round(cfg._knowledge.chars / 1000) + 'k chars' +
        (cfg._knowledge.trimmed ? ' (trimmed)' : '') + '.';
    }
    });
  }

  function init() {
    var els = document.querySelectorAll('.highlighter-rouge.agent, pre.agent, div.agent[class*="language-"], p.agent');
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
