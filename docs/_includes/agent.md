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
  provider: gemini | openrouter | groq | custom   (default from the ring)
            THE AUTHOR'S SUGGESTION, not the learner's engine: the ring
            (docs/bots/providers.yml — engines, endpoints, models, where a
            key comes from; never a key) lets a learner hold several keys
            and pick which answers first. Their ★ outranks provider:.
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
/* why the key went away — on the form that is asking for another one, because
   the chat body's status line is hidden the moment the key is dropped */
.lc-agent-authmsg { margin: 0 0 0.7em; padding: 0.5em 0.7em; border-left: 3px solid #e65100; background: #fff8e1; color: #5d4037; font-size: 0.88em; border-radius: 0 4px 4px 0; }
.lc-agent-auth input[type="text"] { position: absolute; left: -9999px; }
.lc-agent-pw-row { display: flex; gap: 0.5em; margin-bottom: 0.5em; flex-wrap: wrap; }
.lc-agent-token { flex: 1; min-width: 200px; padding: 0.5em 0.7em; border: 1px solid #ccc; border-radius: 4px; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.88em; box-sizing: border-box; }
.lc-agent-token:focus { outline: 2px solid #0066cc; border-color: #0066cc; }
.lc-agent-auth button[type="submit"] { background: #0066cc; color: white; border: none; padding: 0.5em 1.1em; border-radius: 4px; cursor: pointer; font-weight: 500; font-size: 0.9em; }
.lc-agent-auth button[type="submit"]:hover { background: #0052a3; }
.lc-agent-ring-row { display: flex; gap: 0.5em; align-items: center; flex-wrap: wrap; padding: 0.4em 0; border-top: 1px solid #f0f0f0; }
.lc-agent-ring-row:first-child { border-top: none; }
.lc-agent-ring-name { flex: 0 0 11em; font-weight: 600; color: #444; font-size: 0.9em; }
.lc-agent-ring-name small { font-weight: 400; color: #2e7d32; margin-left: 0.3em; }
.lc-agent-ring-row input[type="password"] { flex: 1 1 10em; min-width: 8em; }
.lc-agent-ring-held { color: #2e7d32; font-size: 0.88em; }
.lc-agent-ring-first { color: #b45309; font-size: 0.85em; font-weight: 600; }
.lc-agent-ring-row button[type="button"] { background: white; color: #555; border: 1px solid #ccc; padding: 0.3em 0.7em; border-radius: 4px; cursor: pointer; font-size: 0.82em; }
.lc-agent-ring-row button[type="button"]:hover { border-color: #0066cc; color: #0066cc; }
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
.lc-agent-note { font-size: 0.85em; color: #475569; }
.lc-agent-fallback-yes, .lc-agent-fallback-no { font: inherit; font-size: 0.85em;
  padding: 0.25em 0.8em; border-radius: 6px; border: 1px solid #cbd5e1;
  background: #fff; cursor: pointer; margin-top: 0.4em; }
.lc-agent-fallback-yes { border-color: #0066cc; color: #0052a3; font-weight: 600; }
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
  /* `why` travels with a CLEARED key: the panel that discovers a dead key
     writes its explanation into .lc-agent-status, which lives inside the chat
     body — and clearing the key hides that body and blanks it. The reason
     reached the DOM and was erased in the same tick, so a learner was sent
     back to the paste box with no idea why. Hand the reason to the listeners
     and they can put it on the form that is actually asking. */
  function setSharedToken(pid, v, why) {
    SHARED.tokens[pid] = v;
    try {
      if (v) localStorage.setItem("lc_ai_key_" + pid, v);
      else localStorage.removeItem("lc_ai_key_" + pid);
    } catch (e) {}
    SHARED.listeners.forEach(function(cb){ try { cb(pid, v, why); } catch (e) {} });
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
      'The learner is editing this Python code in editor #' + boundId + ':',
      '',
      '```python',
      trimmedCode,
      '```'
    ];
    if (output) {
      parts.push('', 'The last run produced this output:', '', '```', output, '```');
    }
    parts.push('', 'The learner asks:', '', userQuestion);
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
    groq: {
      base: 'https://api.groq.com/openai/v1',
      model: 'llama-3.3-70b-versatile',
      key_name: 'Groq key',
      key_url: 'https://console.groq.com/keys',
      key_hint: 'gsk_...'
    },
    custom: { base: '', model: '', key_name: 'API key', key_url: '', key_hint: 'sk-...' }
  };
  var DEFAULT_PROVIDER = 'gemini';

  /* THE RING IS A FILE. docs/bots/providers.yml declares the engines — name,
     endpoint, model, where a key comes from — and never a key. Adding an
     engine that speaks the OpenAI dialect is a yaml entry, not a release;
     the table above is only the fallback for a site whose file cannot be
     read. (Michel, 2026-09-16: "declare those somewhere, in a yaml file in
     the repo, so the ring stays generic".) */
  var _lcSiteBase = {{ site.baseurl | default: "" | jsonify }};
  function loadProviders() {
    if (window.lcProvidersReady) return window.lcProvidersReady;
    window.lcProvidersReady = loadJsYaml().then(function () {
      return fetch(_lcSiteBase + '/bots/providers.yml', { cache: 'no-store' })
        .then(function (r) { return r.ok ? r.text() : ''; });
    }).then(function (txt) {
      var doc = (txt && window.jsyaml) ? window.jsyaml.load(txt) : null;
      if (doc && doc.providers && typeof doc.providers === 'object') {
        var ring = {};
        Object.keys(doc.providers).forEach(function (id) {
          var p = doc.providers[id] || {};
          if (!p.base) return;
          ring[id] = { name: p.name || id, base: String(p.base).replace(/\/+$/, ''),
                       model: p.model || '', models: Array.isArray(p.models) ? p.models.map(String) : [],
                       key_name: p.key_name || ((p.name || id) + ' key'),
                       key_url: p.key_url || '', key_hint: p.key_hint || 'sk-...', free: !!p.free };
        });
        if (Object.keys(ring).length) {
          Object.keys(PROVIDERS).forEach(function (id) { if (id !== 'custom') delete PROVIDERS[id]; });
          Object.keys(ring).forEach(function (id) { PROVIDERS[id] = ring[id]; });
          if (doc['default'] && PROVIDERS[doc['default']]) DEFAULT_PROVIDER = doc['default'];
        }
      }
      try { document.dispatchEvent(new CustomEvent('lc-providers')); } catch (e) {}
      return PROVIDERS;
    }).catch(function () { return PROVIDERS; });
    return window.lcProvidersReady;
  }
  loadProviders();
  /* the engines a learner can hold a key for, in the ring's order */
  function ringIds() {
    return Object.keys(PROVIDERS).filter(function (id) { return id !== 'custom' && PROVIDERS[id].base; });
  }
  /* WHICH HELD KEY ANSWERS FIRST: the learner's ★ if that key is held, else
     the page's own suggestion if held, else the first held key on the ring.
     A learner with only a Groq key is served by Groq on every page. */
  function firstHeld(prefer) {
    var star = '';
    try { star = localStorage.getItem('lc_ai_first') || ''; } catch (e) {}
    if (star && PROVIDERS[star] && getSharedToken(star)) return star;
    if (prefer && PROVIDERS[prefer] && getSharedToken(prefer)) return prefer;
    var ids = ringIds();
    for (var i = 0; i < ids.length; i++) if (getSharedToken(ids[i])) return ids[i];
    return '';
  }
  function setFirst(id) {
    try { if (id) localStorage.setItem('lc_ai_first', id); else localStorage.removeItem('lc_ai_first'); } catch (e) {}
    SHARED.listeners.forEach(function (cb) { try { cb(id, getSharedToken(id), ''); } catch (e) {} });
  }

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

  function rememberedModel(pid) {
    try { return localStorage.getItem('lc_ai_model_' + pid) || ''; } catch (e) { return ''; }
  }
  function rememberModel(pid, model) {
    try { if (model) localStorage.setItem('lc_ai_model_' + pid, model); } catch (e) {}
  }
  /* THE PRESET IS GONE — ASK THE ENGINE. A 404 on chat/completions is the
     engine saying "no such model" (Michel, 2026-09-16: OpenRouter retired
     the free slug, Groq the 70b id, and the trail showed both). Every
     engine on the ring also serves /models; take the first of the ring's
     preferences it lists (exact id, then prefix — Gemini says
     "models/gemini-2.5-flash"), else the first free one, else the first.
     The choice is remembered on this device; the ring file's list is where
     the author steers it. Returns '' when nothing better is known. */
  function isFreeModel(m) {
    if (/:free$/.test(String(m.id || ''))) return true;
    var pr = m.pricing || {};
    return pr.prompt != null && Number(pr.prompt) === 0 && Number(pr.completion || 0) === 0;
  }
  function discoverModel(eng, key) {
    var pv = PROVIDERS[eng.id] || {};
    var prefs = (pv.models || []).filter(function (m) { return m && m !== eng.model; });
    return fetch(eng.base + '/models', { headers: { Authorization: 'Bearer ' + key } })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (j) {
        var list = ((j && j.data) || []).filter(function (m) { return m && m.id; });
        if (!list.length) return '';
        var ids = list.map(function (m) { return String(m.id).replace(/^models\//, ''); });
        for (var i = 0; i < prefs.length; i++) {
          var want = String(prefs[i]).replace(/^models\//, '');
          for (var k = 0; k < ids.length; k++) {
            if (ids[k] === want || ids[k].indexOf(want) === 0) { if (ids[k] !== eng.model) return ids[k]; }
          }
        }
        for (var f = 0; f < list.length; f++) if (isFreeModel(list[f]) && ids[f] !== eng.model) return ids[f];
        return ids[0] !== eng.model ? ids[0] : '';
      }).catch(function () { return ''; });
  }

  /* resolve provider preset + per-fence overrides into {base, model, …} */
  function resolveEngine(cfg) {
    var suggested = cfg.provider || DEFAULT_PROVIDER;
    var pid = suggested;
    /* the learner's ring outranks the page's suggestion — unless the page
       wires its own endpoint, which no ring key could serve */
    if (!cfg.base_url && suggested !== 'custom' && !cfg.exact) pid = firstHeld(suggested) || suggested;
    var pv = PROVIDERS[pid] || PROVIDERS[DEFAULT_PROVIDER];
    var base = (cfg.base_url || pv.base || '').replace(/\/+$/, '');
    return {
      base: base,
      host: (base.match(/^https?:\/\/([^\/]+)/) || [])[1] || 'the model service',
      /* a fence's model: names a model OF ITS provider — on another engine
         it would 404; the ring's own preset answers there, or the model the
         engine itself named the day the preset was gone (see discoverModel) */
      model: (cfg.model && pid === suggested) ? cfg.model : (rememberedModel(pid) || pv.model),
      name: pv.name || pid,
      key_name: pv.key_name, key_url: pv.key_url, key_hint: pv.key_hint,
      id: pid
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
    /* THE TUTOR MUST NOT HOLD THE ANSWER KEY (Michel, 2026-08-13: Doc handed a
     quiz answer straight over). A page's markdown marks the right option with
     [x] and often explains it in a note underneath — so "knowledge: self" was
     posting the answer sheet with every question. A prompt rule alone is a
     promise; removing the answer from what the tutor can see is a fact.
     The question and its options stay, so a guide can still ask what the
     learner thinks and hint — which is the point. */
  function redactAnswers(text) {
    var lines = String(text || "").split("\n");
    for (var i = 0; i < lines.length; i++) {
      if (!/^\{:\s*\.quiz/.test(lines[i].trim())) continue;
      for (var j = i - 1; j >= 0; j--) {
        var l = lines[j];
        if (/^\s*[-*+]\s*\[[ xX]\]/.test(l)) { lines[j] = l.replace(/\[[xX]\]/, "[ ]"); continue; }
        if (/^\s*>/.test(l)) { lines[j] = ""; continue; }        /* the note that explains it */
        if (/^\s*$/.test(l)) continue;
        break;                                                    /* the question itself: keep it */
      }
    }
    return lines.join("\n");
  }
  window.lcRedactAnswers = redactAnswers;   /* the rule, readable by a check */

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
        parts = parts.map(function (p) {
          return p ? { path: p.path, text: redactAnswers(p.text) } : p;
        });
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

  /* One wording for "the model stopped mid-thought", so a caller can strip
     it back off as reliably as it was added. */
  var TRUNCATED_NOTE =
    '⚠️ *(cut off — the answer outgrew this agent\'s max_tokens. ' +
    'Ask for something shorter, or raise the knob.)*';

  /* ===== Who is asking: the author, or a learner? ========================
     AUTHOR MODE IS OWNERSHIP, NOT A KEY (Michel, 2026-08-13, reading a course
     page in Canvas signed in as zamm-student: *"I'm surprised to see I'm
     author"*). Every onboarded learner holds an editor key — it is how their
     own bench saves — so "a key is present" made every learner an author and
     handed them the direct answers.

     The honest question is the one X-ray already asks: can this viewer PUSH
     to the repo the material comes from? (folder.md, Michel 2026-07-31:
     *pedagogical access is not ownership*.) A learner reading the org vault
     cannot; the author reading their own lab can. One request per repo per
     session, and the answer FAILS CLOSED — unknown means learner. */
  window.lcAuthorMode = (function () {
    var SITE = {{ site.github.repository_nwo | default: "" | jsonify }};
    var inflight = {};
    function key() { try { return localStorage.getItem('lc_ed_pat') || ''; } catch (e) { return ''; } }
    /* the material's own repo: a rendered page says where it came from, and a
       site page IS its own source */
    function repo() {
      var root = document.getElementById('lc-run');
      return (root && root.getAttribute('data-lc-src-repo')) || SITE || '';
    }
    function check() {
      var r = repo(), k = key();
      if (!r || !k) return Promise.resolve(false);
      var id = 'lc_author_' + r + '|' + k.slice(-6);
      try { var seen = sessionStorage.getItem(id);
            if (seen === '1' || seen === '0') return Promise.resolve(seen === '1'); } catch (e) {}
      if (!inflight[id]) inflight[id] = fetch('https://api.github.com/repos/' + r, {
          headers: { Authorization: 'Bearer ' + k, Accept: 'application/vnd.github+json' } })
        .then(function (res) { return res.ok ? res.json() : null; })
        .then(function (d) {
          var can = !!(d && d.permissions && d.permissions.push);
          try { sessionStorage.setItem(id, can ? '1' : '0'); } catch (e) {}
          return can;
        })
        .catch(function () { return false; });
      return inflight[id];
    }
    return { check: check, repo: repo };
  })();

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
    ready: function () { return !!firstHeld(DEFAULT_PROVIDER); },
    /* a key pasted at a door or the guide goes to the engine the ring names
       for this learner — the same identity the agents will look under */
    connect: function (key) { if (key) setSharedToken(window.lcBotAsk.engine().id, String(key).trim()); },
    disconnect: function () { setSharedToken(window.lcBotAsk.engine().id, null); },
    onChange: onSharedTokenChange,
    ask: function (botName, question, opts) {
      if (!firstHeld(DEFAULT_PROVIDER)) return Promise.resolve({ error: 'No key' });
      return loadBot(botName).then(function (botCfg) {
        var cfg = {};
        Object.keys(DEFAULTS).forEach(function (k) { cfg[k] = DEFAULTS[k]; });
        Object.keys(botCfg).forEach(function (k) { cfg[k] = botCfg[k]; });
        if (opts && opts.direct) {
          /* the AUTHOR is curating content, not being tutored: no guiding
             questions — direct, complete, keep-worthy answers */
          cfg.system += '\n\nThis question comes from the course AUTHOR curating ' +
            'material, not a learner: answer directly and completely, no guiding ' +
            'questions, no withheld solutions. Keep the step format.';
        }
        var eng = resolveEngine(cfg);
        return ask(getSharedToken(eng.id), cfg, question).then(function (result) {
          if (result && result.unauthorized) setSharedToken(eng.id, null, result.error);
          return result;
        });
      }, function () {
        return { error: 'bot "' + botName + '" could not be loaded' };
      }).then(function (result) {
        if (result && result.usage && window.lcTokens) window.lcTokens.add(result.usage);
        return result;
      });
    }
  };

  /* ── the day's spend, in one place ───────────────────────────────────
     Every reply already carries usage; until now each panel counted only
     its own session, and the docked guide counted nothing — so a learner
     could burn a free-tier day across six pages and never see a number
     (Michel, 2026-08-13). This adds them up per DAY (the quota's own
     rhythm), per browser, and tells anyone who wants to show it.
     It counts what THIS browser spent — Google does not publish what is
     left, and inventing a "remaining" would be worse than saying nothing. */
  window.lcTokens = (function () {
    var KEY = 'lc_tokens';
    function today() { return new Date().toISOString().slice(0, 10); }
    function read() {
      var d = { day: today(), tokens: 0, asks: 0 };
      try { var raw = JSON.parse(localStorage.getItem(KEY) || 'null'); if (raw && raw.day === d.day) d = raw; } catch (e) {}
      return d;
    }
    function write(d) { try { localStorage.setItem(KEY, JSON.stringify(d)); } catch (e) {} }
    return {
      add: function (usage) {
        var n = (usage && (usage.total_tokens || usage.totalTokens)) || 0;
        var d = read();
        d.tokens += n; d.asks += 1; d.day = today();
        write(d);
        try { document.dispatchEvent(new CustomEvent('lc-tokens', { detail: d })); } catch (e) {}
        return d;
      },
      today: read,
      /* the sentence anyone can show: a chip, a tooltip, a page */
      line: function () {
        var d = read();
        if (!d.asks) return 'No AI questions asked today.';
        return d.asks + ' AI question' + (d.asks > 1 ? 's' : '') + ' today · about ' +
               (d.tokens >= 1000 ? Math.round(d.tokens / 100) / 10 + 'k' : d.tokens) + ' tokens. ' +
               'Your free key is limited — fewer, better questions last longer.';
      }
    };
  })();

  var KNOB_RE = /^(system|intro|placeholder|name|model|model_fallback|provider|base_url|fallback|temperature|max_tokens|bot|knowledge|knowledge_budget)\s*:\s?(.*)$/;
  function lenientCfg(raw) {
    var out = {}, key = null, buf = [];
    function flush() { if (key) out[key] = buf.join('\n').replace(/^\s*\|\s*\n?/, '').trim(); }
    String(raw || '').split('\n').forEach(function (line) {
      var m = KNOB_RE.exec(line);
      if (m) { flush(); key = m[1]; buf = [m[2]]; }
      else if (key) buf.push(line);
    });
    flush();
    ['temperature', 'max_tokens', 'knowledge_budget'].forEach(function (k) {
      if (out[k] != null && out[k] !== '' && !isNaN(Number(out[k]))) out[k] = Number(out[k]);
    });
    return out;
  }

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
      '<div class="lc-agent-auth">' +
        '<div class="lc-agent-authmsg" role="status" aria-live="polite" hidden></div>' +
        '<p>Paste a key for any engine below. One is enough; two means a busy engine never stops you — the ★ one answers first, the others step in. Keys stay on this device, sent to their own engine only; let your browser keep them as passwords and they follow you.</p>' +
        '<div class="lc-agent-ring"></div>' +
      '</div>' +
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

  /* THE RING: one row per engine the file declares — held keys show a check
     and a forget, the rest a paste box and where to get one. Each row is its
     own form with the hidden-username trick, so a password manager files
     every key under its engine's name. ★ marks who answers first. */
  function paintRing(panel, cfg) {
    var box = panel.querySelector('.lc-agent-ring');
    if (!box) return;
    var ids = ringIds();
    if (cfg.provider === 'custom' && cfg.base_url) ids = ['custom'].concat(ids);
    var star = firstHeld(cfg.provider || DEFAULT_PROVIDER);
    box.innerHTML = ids.map(function (id) {
      var pv = PROVIDERS[id] || {};
      var held = !!getSharedToken(id);
      var name = escapeHtml(pv.name || id) + (pv.free ? '<small>free tier</small>' : '');
      return '<form class="lc-agent-ring-row" data-pid="' + escapeHtml(id) + '" data-held="' + (held ? '1' : '0') + '" autocomplete="on">' +
        '<span class="lc-agent-ring-name">' + (held && id === star ? '★ ' : '') + name + '</span>' +
        '<input type="text" name="username" value="lc-' + escapeHtml(id) + '" autocomplete="username" tabindex="-1" readonly aria-label="Key account name, used by your password manager">' +
        (held
          ? '<span class="lc-agent-ring-held">✓ key saved</span>' +
            (id === star ? '<span class="lc-agent-ring-first">answers first</span>'
                         : '<button type="button" data-first="' + escapeHtml(id) + '">★ answer first</button>') +
            '<button type="button" data-forget="' + escapeHtml(id) + '">forget</button>'
          : '<input type="password" name="password" class="lc-agent-token" autocomplete="current-password" placeholder="' + escapeHtml(pv.key_hint || 'sk-...') + '" required aria-label="' + escapeHtml(pv.key_name || id) + '">' +
            '<button type="submit">Save</button>' +
            (pv.key_url ? '<a class="lc-agent-help" href="' + escapeHtml(pv.key_url) + '" target="_blank" rel="noopener">get a key</a>' : '')) +
        '</form>';
    }).join('');
    box.querySelectorAll('form').forEach(function (f) {
      f.addEventListener('submit', function (e) {
        e.preventDefault();
        var v = (f.querySelector('input[type=password]').value || '').trim();
        if (v) setSharedToken(f.getAttribute('data-pid'), v);
      });
    });
    box.querySelectorAll('[data-forget]').forEach(function (b) {
      b.addEventListener('click', function () { setSharedToken(b.getAttribute('data-forget'), null); });
    });
    box.querySelectorAll('[data-first]').forEach(function (b) {
      b.addEventListener('click', function () { setFirst(b.getAttribute('data-first')); });
    });
    panel.setAttribute('data-engine', resolveEngine(cfg).host);
    var warn = panel.querySelector('.lc-agent-warn');
    if (warn) warn.textContent = '⚠ Calls ' + resolveEngine(cfg).host + ' directly with your key. Use a key made for this, nothing broader.';
  }

  // ===== API call =====
  /* ONE attempt at ONE engine. The ladder that decides which engine, and how
     many times, is ask() below. */
  function askOnce(token, cfg, userText, engOverride) {
    var eng = engOverride || resolveEngine(cfg);
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
      /* 401 and 403 are NOT the same answer, and treating them alike used to
         DELETE a perfectly good key.
           401 — this credential is not valid. Pasting a fresh one IS the fix,
                 so drop the stored key and ask for another.
           403 — the credential is valid but not allowed to make THIS call: a
                 key restricted to certain websites, an API not switched on for
                 the project, a region block, a proxy answering for the host.
                 Re-pasting the same key changes nothing, so keeping it is the
                 only useful move — and the provider's own sentence says far
                 more than "rejected" ever could.
         Michel, 2026-08-05: "it asks every time after a refresh". This was it —
         one 403 at any desk wiped the key the join door had just saved. */
      if (result.status === 401) {
        return { error: 'Key rejected (401) by ' + eng.host + '. 🔑 paste a fresh ' + eng.key_name + '.', unauthorized: true };
      }
      if (result.status === 403) {
        var e403 = Array.isArray(result.data) ? result.data[0] : result.data;
        var m403 = (e403 && e403.error && e403.error.message) || '';
        return { error: '🚧 ' + eng.host + ' will not take this call — your key is kept, ' +
          'because pasting it again would not help. Usually the key is limited to ' +
          'certain websites, or the service is not switched on for it yet.' +
          (m403 ? ' The provider says: “' + m403 + '”' : '') };
      }
      if (result.status === 429) {
        /* TWO different walls answer 429 and the difference matters to a
           learner: per-minute (wait 60s, keep working) vs the DAY's free
           allowance (gone until it resets — no amount of retrying helps).
           The provider says which in its own message; relay it. */
        var e429 = Array.isArray(result.data) ? result.data[0] : result.data;
        var m429 = (e429 && e429.error && e429.error.message) || '';
        var daily = /per\s*day|daily|PerDay|quota exceeded/i.test(m429);
        /* …and a THIRD face wears the second's costume (Michel, 2026-08-28:
           "I used NO energy today!"): the free tier counts REQUESTS per
           project, and during demand spikes the provider sheds load through
           this same quota door — sometimes at a limit of zero. When OUR
           meter says this browser spent nothing today, "come back tomorrow"
           is a misdiagnosis; say what is actually known instead. Suspect,
           never retriable: the ladder must not hammer a quota wall, but a
           human is welcome to tap try-again in a moment. */
        var spent = (window.lcTokens && window.lcTokens.today()) || {};
        if (daily && !spent.asks) {
          return { error: '🔋 The provider says the day\'s free allowance is spent — but this browser spent nothing today. Usually a demand spike on the free tier, or another device using the same key. Nothing is broken; worth trying again in a few minutes.',
                   status: 429, elsewhere: true, suspectSpike: true };
        }
        return { error: daily
          ? '🔋 Out of free energy for today — the day\'s allowance is spent and refills on its own (around midnight US Pacific). Nothing is broken; come back tomorrow, or use a key with a paid plan.'
          : '⏳ Too many questions too fast (per-minute limit). Wait about a minute and ask again — this one refills by itself.',
          status: 429,
          /* a wall on THIS key says nothing about another provider's quota —
             worth another engine, never worth an immediate retry here */
          elsewhere: true };
      }
      if (result.status >= 400) {
        /* Google wraps errors in an ARRAY ([{error:{…}}]); OpenAI-style
           bodies don't — read both, or the learner sees a bare status
           code instead of the provider's own sentence */
        var eobj = Array.isArray(result.data) ? result.data[0] : result.data;
        var msg = (eobj && eobj.error && eobj.error.message) || ('HTTP ' + result.status);
        return { error: msg + ' (HTTP ' + result.status + ' from ' + eng.host + ')',
                 status: result.status,
                 /* 500/502/503/504 = the service wobbled, not the request:
                    the same call a moment later usually works */
                 retriable: result.status >= 500 };
      }
      var choice = result.data.choices && result.data.choices[0];
      if (!choice) return { error: 'Empty response from API.' };
      var text = (choice.message && choice.message.content) || '';
      /* ran out of allowance mid-thought: say so rather than pass a
         fragment off as the answer.
         Three fields, because showing a half answer and FILING one are
         different decisions: `text` is what a reader should see (notice
         included), `clean` is the model's own words without it, and
         `truncated` lets a caller refuse to persist the fragment. Before
         this the notice was only prose inside text — so the guide's 📌 kept
         a half sentence, and the ⚠️ line with it, into the page (2026-08-07). */
      var truncated = choice.finish_reason === 'length';
      var clean = text;
      if (truncated) text = (text ? text + '\n\n' : '') + TRUNCATED_NOTE;
      return { text: text, clean: clean, truncated: truncated,
               usage: result.data.usage || null };
    }).catch(function(err){
      /* fetch rejected → no HTTP answer reached the page. Usually the ROAD
         (ad-blocker, VPN, firewall) — but some providers answer errors
         without CORS headers, so a rejected key can also land here dressed
         as a network failure. Name both faces. */
      return { error: "Couldn't reach " + eng.host + " — no answer got through. " +
        "Often an ad-blocker, VPN or firewall on the road; if your network is fine, " +
        "the key itself may be stale or wrong (🔑 paste a fresh " + eng.key_name + "). " +
        "(" + (err.message || String(err)) + ")",
        retriable: true };
    });
  }

  /* ── The ladder: retry, then another engine that already has a key ──────
     "This model is currently experiencing high demand… (HTTP 503)" landed in
     front of a class often enough to be the lesson (Michel, 2026-08-19). A
     spike lasts seconds, so the cheapest fix is to ask again — the same fix
     the publish button learned on 2026-08-06: a retry the learner has to
     invent is a retry the button should have made.

     Then, and only then, another provider. The chain is the keys the learner
     ALREADY HOLDS, never the providers that exist: falling back to a service
     they have never signed up for replaces a 503 with a demand for a second
     account mid-lesson. An author may name the order (fallback: openrouter);
     otherwise it is whatever is on the keyring.

     What never cascades: 401 (this key is wrong — spraying it at three
     services helps nobody) and 403 (the key is fine, this call is not
     allowed). Those are answers, not weather. */
  function heldFallbacks(cfg, primaryId) {
    var named = String(cfg.fallback || '').split(',')
      .map(function (x) { return x.trim(); }).filter(Boolean);
    var ids = named.length ? named : Object.keys(PROVIDERS);
    return ids.filter(function (id) {
      var pv = PROVIDERS[id];
      return id !== primaryId && pv && pv.base && getSharedToken(id);
    });
  }
  function pause(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }

  /* CONSENT BEFORE SPENDING (Michel, 2026-08-19: "who might be paying?").
     Retrying the same engine spends nothing new — same key, same plan, and
     the reader already chose it. Switching engines can spend someone's
     money, so it is asked, once per sitting per engine, and remembered for
     that sitting only. A desk with nowhere to ask (the docked guide) simply
     does not switch: silence is the safe answer when nobody can consent. */
  function fallbackAllowed(id) {
    try { return sessionStorage.getItem('lc_ai_fallback_ok_' + id) === '1'; }
    catch (e) { return false; }
  }
  function rememberFallback(id) {
    try { sessionStorage.setItem('lc_ai_fallback_ok_' + id, '1'); } catch (e) {}
  }

  function ask(token, cfg, userText, askConsent) {
    var primary = resolveEngine(cfg);
    var RETRY_MS = [1500, 4000];          /* a demand spike outlives neither */

    function tryEngine(eng, key, retries, healed) {
      return askOnce(key, cfg, userText, eng).then(function (res) {
        if (!res.error) return res;
        /* "no such model": heal once — the engine names what it serves */
        if (res.status === 404 && !healed) {
          return discoverModel(eng, key).then(function (found) {
            if (!found) return res;
            var was = eng.model;
            eng.model = found;
            rememberModel(eng.id, found);
            return tryEngine(eng, key, retries, true).then(function (r2) {
              if (!r2.error) r2.healed = eng.host + ': ' + was + ' is gone; using ' + found + ' (remembered on this device)';
              else r2.error = r2.error + ' — after ' + was + ' was gone and ' + found + ' was tried instead';
              return r2;
            });
          });
        }
        if (!res.retriable || !retries.length) return res;
        return pause(retries[0]).then(function () {
          return tryEngine(eng, key, retries.slice(1), healed);
        });
      });
    }

    return tryEngine(primary, token, RETRY_MS.slice()).then(function (res) {
      if (!res.error) return res;
      /* the key is the problem, or the request is: no other engine helps */
      if (res.unauthorized || res.status === 403 || res.status === 400) return res;
      if (!res.retriable && !res.elsewhere) return res;
      var chain = heldFallbacks(cfg, primary.id);
      if (!chain.length) return res;
      /* EVERY ENGINE'S OWN WORD. When the fallback failed too, the desk
         moved on in silence and the final red line quoted Gemini alone —
         Michel (2026-09-16) could not tell whether OpenRouter and Groq had
         been asked, let alone what they said. The trail rides the failure:
         one line per engine, its host and its sentence, or "not asked". */
      var trail = [primary.host + ': ' + res.error];

      function next(i) {
        if (i >= chain.length) {                  /* the first failure is the honest one */
          if (trail.length > 1) res.trail = trail;
          return Promise.resolve(res);
        }
        var id = chain[i];
        /* exact: the ladder picked this engine on purpose — the ring's ★
           must not fold it back into the engine that just failed */
        var eng = resolveEngine({ provider: id, model: cfg.model_fallback || '', exact: true });
        var consent = fallbackAllowed(id)
          ? Promise.resolve(true)
          : (askConsent ? Promise.resolve(askConsent(eng, res)) : Promise.resolve(false));
        return consent.then(function (ok) {
          if (!ok) { trail.push(eng.host + ': not asked — you said wait'); return next(i + 1); }
          rememberFallback(id);
          return run();
        });

        function run() {
        return tryEngine(eng, getSharedToken(id), []).then(function (r2) {
          if (r2.error) { trail.push(eng.host + ': ' + r2.error); return next(i + 1); }
          /* the reader is told WHO answered when it is not the first choice —
             the same honesty as the guide naming whose Doc is speaking. The
             note rides `via`, never the text: a notice folded into the answer
             gets kept into the page (the 📌 lesson of 2026-08-07). */
          r2.via = eng.host;
          return r2;
        });
        }
      }
      return next(0);
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
    var authMsg = panel.querySelector('.lc-agent-authmsg');

    /* the engine is whoever the ring names NOW — it moves when a key is
       pasted, forgotten or starred, on this desk or any other */
    function engineId() { return resolveEngine(cfg).id; }
    function myToken() { return getSharedToken(engineId()); }
    function sayOnForm(why) {
      if (!authMsg) return;
      authMsg.textContent = why || '';
      authMsg.hidden = !why;
    }
    function showChat() { authForm.hidden = true; body.hidden = false; sayOnForm(''); }
    function showAuth(why) { paintRing(panel, cfg); authForm.hidden = false; body.hidden = true; sayOnForm(why); }

    // Initial state from the ring: any held key opens the desk
    paintRing(panel, cfg);
    if (myToken()) showChat(); else showAuth();
    document.addEventListener('lc-providers', function () { paintRing(panel, cfg); });

    // React to any desk changing any key: the ring repaints, the door follows
    onSharedTokenChange(function(pid, v, why){
      paintRing(panel, cfg);
      /* the reason rides along, because this repaint is what used to erase it */
      if (myToken()) { if (authForm.hidden === false && !why) showChat(); }
      else { response.innerHTML = ''; status.innerHTML = ''; showAuth(why); }
      if (v && !why && pid === engineId()) showChat();
    });

    /* 🔑 opens the ring — add a second engine, star one, forget one */
    keyBtn.addEventListener('click', function(){
      if (authForm.hidden) { paintRing(panel, cfg); authForm.hidden = false; }
      else if (myToken()) authForm.hidden = true;
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
        return ask(myToken(), cfg, fullPrompt, function (eng, failure) {
          /* the offer, in the desk itself: one sentence about who is busy,
             one button naming who would answer and on whose key */
          return new Promise(function (resolve) {
            status.innerHTML =
              '<span class="lc-agent-note">⏳ ' + escapeHtml(failure.error || 'That engine is busy.') +
              '<br>Ask <b>' + escapeHtml(eng.host) + '</b> instead? It runs on your ' +
              escapeHtml(eng.key_name) + ' — your plan there, your spending.</span> ' +
              '<button type="button" class="lc-agent-fallback-yes">Use ' + escapeHtml(eng.host) + '</button> ' +
              '<button type="button" class="lc-agent-fallback-no">No, wait</button>';
            var yes = status.querySelector('.lc-agent-fallback-yes');
            var no  = status.querySelector('.lc-agent-fallback-no');
            yes.addEventListener('click', function () { status.innerHTML = ''; resolve(true); });
            no.addEventListener('click', function () { resolve(false); });
          });
        });
      }).then(function(result){
        sendBtn.disabled = false;
        sendBtn.textContent = '▶ Ask';
        if (result.error) {
          status.innerHTML = '<span class="lc-agent-err">⚠ ' + escapeHtml(result.error) + '</span>' +
            (result.trail && result.trail.length
              ? '<div class="lc-agent-note lc-agent-trail">The ring was tried, engine by engine:<br>' +
                result.trail.map(function (l) { return '· ' + escapeHtml(l); }).join('<br>') + '</div>'
              : '');
          /* carry the reason INTO the clear — the auth wall this triggers
             hides the status line we just wrote */
          if (result.unauthorized) setSharedToken(engineId(), null, result.error);
          return;
        }
        /* a fallback engine answered: say which, in the status line and not
           in the answer — the log below keeps the model's own words only */
        status.innerHTML = (result.via
          ? '<span class="lc-agent-note">↩︎ ' + escapeHtml(result.via) +
            ' answered — your first engine was busy.</span>'
          : '') + (result.healed
          ? '<div class="lc-agent-note lc-agent-healed">🩹 ' + escapeHtml(result.healed) + '</div>'
          : '');
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
          if (window.lcTokens) window.lcTokens.add(result.usage);
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
      try { pageCfg = window.jsyaml.load(raw) || {}; } catch (e) { pageCfg = null; }
    }
    /* A SHEET IS PROSE, NOT YAML. Module 01 asks the learner to paste a
       whole briefing after `system:` — and a briefing that ends with
       "VERDICT: n/8" is not valid YAML: the second colon kills the parse,
       the desk fell back to "You are a helpful assistant.", and the check
       read "too short" (found 2026-09-16, building the gear scenario).
       When YAML refuses, read the sheet the way a person does: a known
       knob at the start of a line opens a value, everything until the next
       knob belongs to it. */
    if (pageCfg === null || typeof pageCfg !== 'object' || Array.isArray(pageCfg)) pageCfg = lenientCfg(raw);
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
