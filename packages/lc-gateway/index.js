/*!
 * @karmicsoft/lc-gateway — e-mail sign-in and pull-request writer for
 * git-backed content. © KarmicSoft — LightCode. See LICENSE.
 *
 * A volunteer without a GitHub account signs in with a magic link, edits a
 * record in the host's own form, and saves. The gateway turns that save into
 * one branch and one pull request, written through lc-patch so the diff shows
 * the edit and nothing else. It never commits to the published branch. It
 * writes with ONE identity, a GitHub App; the volunteer appears by name in a
 * Co-authored-by trailer, with a service address — the personal address is
 * never written anywhere.
 *
 * The whole service is a pure function of an abstract request (see
 * createGateway().request), so the acceptance suite drives it without a
 * socket and with GitHub, Brevo and the clock replaced. server.js is the
 * thin HTTP adapter, config.js reads the environment.
 */
import { createHmac, createSign, randomBytes, createHash, timingSafeEqual } from 'node:crypto';
import { patch } from '@karmicsoft/lc-patch';
import { load, dump } from '@karmicsoft/lc-serialize';

export const GATEWAY_VERSION = '0.3.3';

const DEFAULTS = {
  baseBranch: 'main',
  branchPrefix: 'contrib',
  prTitle: '{type}: {title} — {name}',
  linkTtlMin: 15,
  sessionTtlDays: 7,
  rateLimitPerMin: 5,
  rateLimitPerHour: 10,             // sign-in requests per address per hour
  mailPerDay: 200,                  // sign-in mails per day, all addresses together (the mail quota)
  protectedFields: ['id', 'slug', 'workflow.published', 'workflow.validated', 'workflow.withdrawnReason', 'withdrawnReason', 'validated', 'periods', 'districts'],
  allowCreate: true,
  requiredCheck: 'fiche-check',
  mergeMethod: 'SQUASH',
  mailFromName: 'Contributions',
  mailSubject: 'Your sign-in link',
  mailText: 'Hello {name},\n\nHere is your sign-in link, valid {minutes} minutes and once only:\n\n{link}\n\nIf you did not ask for it, ignore this message.',
  verifyTitle: 'Sign in',
  verifyButton: 'Sign in',
  verifyText: 'Press the button to finish signing in. The link works once.',
  githubApi: 'https://api.github.com',
  brevoApi: 'https://api.brevo.com/v3/smtp/email',
  contentDirs: [],
  allowlist: [],
};

/**
 * config: see config.js / DEPLOY.md. deps: { fetch, now, random, log } —
 * all optional, all replaceable (that is how the suite runs offline).
 */
export function createGateway(config, deps = {}) {
  const cfg = { ...DEFAULTS, ...config };
  for (const k of ['publicUrl', 'repo', 'sessionSecret', 'coauthorEmail']) if (!cfg[k]) throw new Error('lc-gateway: config.' + k + ' is required');
  if (!cfg.contentDirs.length) throw new Error('lc-gateway: config.contentDirs must name at least one folder');
  const fetchFn = deps.fetch || globalThis.fetch;
  const now = deps.now || (() => Date.now());
  const random = deps.random || ((n) => randomBytes(n));
  const log = deps.log || (() => {});

  const links = new Map();          // sha256(token) → { email, exp, used }
  const hits = new Map();           // email → [timestamps] (rate limit)
  let sent = [];                    // timestamps of every mail sent (the daily quota)
  let ghToken = null;               // { token, exp }

  // ── allowlist ────────────────────────────────────────────────────────
  const norm = (e) => String(e || '').trim().toLowerCase();
  const who = (email) => cfg.allowlist.find((a) => norm(a.email) === norm(email)) || null;

  // ── sessions: a signed, self-contained cookie ────────────────────────
  const b64u = (b) => Buffer.from(b).toString('base64url');
  const sign = (s) => createHmac('sha256', cfg.sessionSecret).update(s).digest('base64url');
  function issueSession(email) {
    const payload = b64u(JSON.stringify({ e: email, x: now() + cfg.sessionTtlDays * 86400000 }));
    return payload + '.' + sign(payload);
  }
  function readSession(cookie) {
    if (!cookie) return null;
    const m = /(?:^|;\s*)lc_session=([^;]+)/.exec(cookie);
    const raw = m ? m[1] : cookie;
    const [payload, sig] = String(raw).split('.');
    if (!payload || !sig || !sameSig(sign(payload), sig)) return null;
    let s; try { s = JSON.parse(Buffer.from(payload, 'base64url').toString('utf8')); } catch (e) { return null; }
    if (!s || !s.e || !s.x || s.x < now()) return null;
    const a = who(s.e);
    return a ? { email: norm(s.e), name: a.name, role: a.role || 'contributor' } : null;   // removal revokes
  }
  function sameSig(a, b) {           // constant time: the length leaks nothing, the bytes must not
    const x = Buffer.from(String(a)), y = Buffer.from(String(b));
    return x.length === y.length && timingSafeEqual(x, y);
  }
  const cookieFor = (sess) => 'lc_session=' + sess + '; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=' + (cfg.sessionTtlDays * 86400);

  // ── sign-in links ────────────────────────────────────────────────────
  const hash = (t) => createHash('sha256').update(t).digest('hex');
  const DAY = 86400000, HOUR = 3600000;
  function sweep() {                 // nothing outlives its window in memory
    const t = now();
    for (const [k, l] of links) if (l.used || l.exp < t) links.delete(k);
    for (const [k, arr] of hits) { const a = arr.filter((x) => t - x < HOUR); a.length ? hits.set(k, a) : hits.delete(k); }
    sent = sent.filter((x) => t - x < DAY);
  }
  function rateLimited(email) {      // per address: a minute and an hour
    const t = now();
    const arr = (hits.get(email) || []).filter((x) => t - x < HOUR);
    arr.push(t); hits.set(email, arr);
    return arr.length > cfg.rateLimitPerHour || arr.filter((x) => t - x < 60000).length > cfg.rateLimitPerMin;
  }
  const quotaSpent = () => sent.length >= cfg.mailPerDay;   // all addresses together, known or not
  async function sendLink(a) {
    const token = b64u(random(32));
    sent.push(now());
    links.set(hash(token), { email: norm(a.email), exp: now() + cfg.linkTtlMin * 60000, used: false });
    const link = cfg.publicUrl.replace(/\/$/, '') + '/auth/verify?t=' + token;
    const mail = {
      sender: { email: cfg.mailFrom, name: cfg.mailFromName },
      to: [{ email: a.email, name: a.name }],
      subject: cfg.mailSubject,
      textContent: String(cfg.mailText).replace('{name}', a.name).replace('{minutes}', String(cfg.linkTtlMin)).replace('{link}', link),
    };
    if (deps.sendMail) return deps.sendMail(mail);
    const r = await fetchFn(cfg.brevoApi, { method: 'POST',
      headers: { 'api-key': cfg.brevoApiKey || '', 'content-type': 'application/json', accept: 'application/json' },
      body: JSON.stringify(mail) });
    if (!r.ok) log('brevo refused: ' + r.status);
  }
  function useLink(token) {
    const l = links.get(hash(String(token || '')));
    if (!l || l.used || l.exp < now()) return null;
    l.used = true;
    return who(l.email);
  }
  // The mailed link opens a page; a mail scanner that follows it consumes
  // nothing. The button on that page posts the token, and that is the one use.
  function verifyPage(token) {
    const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
    const html = '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
      + '<meta name="robots" content="noindex"><title>' + esc(cfg.verifyTitle) + '</title>'
      + '<style>body{font:16px/1.5 system-ui,sans-serif;max-width:32rem;margin:4rem auto;padding:0 1rem}button{font:inherit;padding:.6rem 1.4rem}</style></head>'
      + '<body><h1>' + esc(cfg.verifyTitle) + '</h1><p>' + esc(cfg.verifyText) + '</p>'
      + '<form method="post" action="' + esc(cfg.publicUrl.replace(/\/$/, '')) + '/auth/verify">'
      + '<input type="hidden" name="t" value="' + esc(token) + '"><button type="submit">' + esc(cfg.verifyButton) + '</button></form></body></html>';
    return { status: 200, headers: { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store', 'referrer-policy': 'no-referrer' }, body: html };
  }

  // ── GitHub, as an App ────────────────────────────────────────────────
  function appJwt() {
    const t = Math.floor(now() / 1000);
    const enc = (o) => b64u(JSON.stringify(o));
    const head = enc({ alg: 'RS256', typ: 'JWT' }) + '.' + enc({ iat: t - 60, exp: t + 540, iss: String(cfg.appId) });
    const s = createSign('RSA-SHA256'); s.update(head); s.end();
    return head + '.' + s.sign(String(cfg.privateKey).replace(/\\n/g, '\n'), 'base64url');
  }
  async function gh(path, init = {}, auth = 'installation') {
    const token = auth === 'app' ? appJwt() : await installationToken();
    const r = await fetchFn(cfg.githubApi + path, { ...init,
      headers: { authorization: 'Bearer ' + token, accept: 'application/vnd.github+json',
                 'x-github-api-version': '2022-11-28', 'content-type': 'application/json', ...(init.headers || {}) },
      body: init.body && typeof init.body !== 'string' ? JSON.stringify(init.body) : init.body });
    let json = null; try { json = await r.json(); } catch (e) { json = null; }
    return { ok: r.ok, status: r.status, json };
  }
  async function installationToken() {
    if (ghToken && ghToken.exp - now() > 300000) return ghToken.token;
    if (cfg.token) return cfg.token;                              // a plain token, for the live test mode only
    let id = cfg.installationId;
    if (!id) {
      const r = await gh('/repos/' + cfg.repo + '/installation', {}, 'app');
      if (!r.ok) throw new Error('the GitHub App is not installed on ' + cfg.repo);
      id = r.json.id;
    }
    const r = await gh('/app/installations/' + id + '/access_tokens', { method: 'POST' }, 'app');
    if (!r.ok) throw new Error('could not mint an installation token (' + r.status + ')');
    ghToken = { token: r.json.token, exp: Date.parse(r.json.expires_at) || (now() + 3600000) };
    return ghToken.token;
  }

  // ── the write: one branch, one pull request ──────────────────────────
  const slugOf = (p) => String(p).replace(/^.*\//, '').replace(/\.ya?ml$/, '');
  function insideContent(p) {
    if (!p || /(^|\/)\.\.(\/|$)/.test(p) || p.startsWith('/') || !/\.ya?ml$/.test(p)) return false;
    return cfg.contentDirs.some((d) => p.startsWith(d.replace(/\/$/, '') + '/') && !p.slice(d.length + 1).includes('/'));
  }
  // ── protected fields: the gateway refuses what the form must not send ──
  const getPath = (o, path) => path.split('.').reduce((x, k) => (x && typeof x === 'object' ? x[k] : undefined), o);
  const sameValue = (a, b) => JSON.stringify(a === undefined ? null : a) === JSON.stringify(b === undefined ? null : b);
  function touchedProtected(original, record) {
    return cfg.protectedFields.filter((f) => !sameValue(getPath(original, f), getPath(record, f)));
  }
  const stamp = () => { const d = new Date(now()); const z = (n) => String(n).padStart(2, '0');
    return d.getUTCFullYear() + z(d.getUTCMonth() + 1) + z(d.getUTCDate()) + '-' + z(d.getUTCHours()) + z(d.getUTCMinutes()); };
  /* WHOSE CONTRIBUTION IS WAITING (0.3.0, Toni: "1 oui, 2a, 3a"). The App is
     the only writer, so a pull request says who it is for by a mark in its
     description: a fingerprint of the address, keyed by the gateway's own
     secret — nobody can read the address back. A pull request without it
     (opened before 0.3.0, or after the secret rotated) is nobody's: the
     fiche answers as before. */
  const ownerMark = (email) => '<!-- lc-gateway:owner=' +
    createHmac('sha256', cfg.sessionSecret).update('owner:' + norm(email)).digest('base64url').slice(0, 22) + ' -->';
  const isMine = (pr, sess) => !!(pr && sess && String(pr.body || '').includes(ownerMark(sess.email)));
  const pendingOf = (pr, sess) => pr ? { number: pr.number, url: pr.html_url, mine: isMine(pr, sess) } : null;
  /* a bundle (0.3.1) names every file it carries in its description, so a
     waiting contribution is found for each of them, not only the first */
  const pathsMark = (paths) => '<!-- lc-gateway:paths=' + paths.join('|') + ' -->';
  async function openPrFor(path) {
    const byBranch = await openPrOn(slugOf(path));
    if (byBranch) return byBranch;
    const r = await gh('/repos/' + cfg.repo + '/pulls?state=open&per_page=100');
    return (r.ok && Array.isArray(r.json) ? r.json : []).find((p) => {
      const m = /<!-- lc-gateway:paths=([^>]*) -->/.exec(String(p.body || ''));
      return m && m[1].split('|').indexOf(path) >= 0;
    }) || null;
  }
  async function openPrOn(slug) {
    const r = await gh('/repos/' + cfg.repo + '/pulls?state=open&per_page=100');
    /* the exact shape <prefix>/<slug>-<yyyymmdd-hhmm>: louise-michel never
       matches louise-michel-bis's pull request */
    const esc = (x) => String(x).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const want = new RegExp('^' + esc(cfg.branchPrefix) + '/' + esc(slug) + '-\\d{8}-\\d{4}$');
    return (r.ok && Array.isArray(r.json) ? r.json : []).find((p) => p.head && want.test(String(p.head.ref))) || null;
  }
  async function writeAsPr(sess, { path, text, sha, title, type, message, files }) {
    files = files || [{ path, text, sha, message }];
    const slug = slugOf(files[0].path);
    const branch = cfg.branchPrefix + '/' + slug + '-' + stamp();
    const base = await gh('/repos/' + cfg.repo + '/git/ref/heads/' + cfg.baseBranch);
    if (!base.ok) throw new Error('cannot read ' + cfg.baseBranch);
    const mk = await gh('/repos/' + cfg.repo + '/git/refs', { method: 'POST', body: { ref: 'refs/heads/' + branch, sha: base.json.object.sha } });
    if (!mk.ok) throw new Error('cannot create the branch (' + mk.status + ')');
    for (const f of files) {                          /* one commit per file, all on one branch */
      const commitMsg = (f.message || message || (type + ': ' + title)) + '\n\nCo-authored-by: ' + sess.name + ' <' + cfg.coauthorEmail + '>';
      const put = await gh('/repos/' + cfg.repo + '/contents/' + f.path, { method: 'PUT',
        body: { message: commitMsg, content: Buffer.from(f.text, 'utf8').toString('base64'), branch, ...(f.sha ? { sha: f.sha } : {}) } });
      if (!put.ok) throw new Error('cannot write ' + f.path + ' (' + put.status + ')');
    }
    const prTitle = cfg.prTitle.replace('{type}', type).replace('{title}', title).replace('{name}', sess.name);
    const pr = await gh('/repos/' + cfg.repo + '/pulls', { method: 'POST',
      body: { title: prTitle, head: branch, base: cfg.baseBranch,
              body: 'Contribution by ' + sess.name + ' through the gateway. ' +
                (files.length === 1 ? 'File: `' + files[0].path + '`.'
                  : 'Files:\n' + files.map((f) => '- `' + f.path + '`').join('\n')) +
                '\n\n' + ownerMark(sess.email) + (files.length > 1 ? '\n' + pathsMark(files.map((f) => f.path)) : '') } });
    if (!pr.ok) throw new Error('cannot open the pull request (' + pr.status + ')');
    let autoMerge = false;
    if (sess.role === 'trusted' && pr.json.node_id) {
      const q = 'mutation($id:ID!,$m:PullRequestMergeMethod!){enablePullRequestAutoMerge(input:{pullRequestId:$id,mergeMethod:$m}){clientMutationId}}';
      const g = await gh('/graphql', { method: 'POST', body: { query: q, variables: { id: pr.json.node_id, m: cfg.mergeMethod } } });
      autoMerge = g.ok && !(g.json && g.json.errors);
      if (!autoMerge) log('auto-merge not enabled on #' + pr.json.number + ': ' + JSON.stringify(g.json && g.json.errors));
    }
    return { number: pr.json.number, url: pr.json.html_url, branch, autoMerge };
  }

  // ── the abstract request ─────────────────────────────────────────────
  const json = (status, body, headers = {}) => ({ status, headers: { 'content-type': 'application/json; charset=utf-8', ...headers }, body });
  const same202 = () => json(202, { ok: true, message: 'If this address is allowed, a link is on its way.' });

  async function request(req) {
    const url = new URL(req.path || '/', 'http://x');
    const p = url.pathname, m = (req.method || 'GET').toUpperCase();
    const ctype = String((req.headers && (req.headers['content-type'] || req.headers['Content-Type'])) || '');
    const body = typeof req.body === 'string'
      ? (/x-www-form-urlencoded/i.test(ctype) ? Object.fromEntries(new URLSearchParams(req.body)) : safeJson(req.body))
      : (req.body || {});
    const sess = readSession(req.headers && (req.headers.cookie || req.headers.Cookie));
    try {
      if (m === 'GET' && p === '/health') return json(200, { ok: true, version: GATEWAY_VERSION });
      if (m === 'POST' && p === '/auth/request') {
        const email = norm(body.email);
        if (!email) return json(400, { error: 'email required' });
        sweep();
        if (quotaSpent()) return json(429, { error: 'too many requests today, try again tomorrow' });
        if (rateLimited(email)) return json(429, { error: 'too many requests, try again later' });
        const a = who(email);
        if (a) await sendLink(a);                          // an unknown address learns nothing
        return same202();
      }
      if (m === 'GET' && p === '/auth/verify') {                 // the page: reads nothing, consumes nothing
        const t = url.searchParams.get('t') || '';
        if (!t) return json(400, { error: 't required' });
        return verifyPage(t);
      }
      if (m === 'POST' && p === '/auth/verify') {                // the button: the one use
        const a = useLink(body.t || url.searchParams.get('t'));
        if (!a) return json(401, { error: 'link refused', message: 'this link is no longer valid — ask for a new one' });
        const s = issueSession(a.email);
        const h = { 'set-cookie': cookieFor(s) };
        if (cfg.appUrl) return { status: 302, headers: { ...h, location: cfg.appUrl }, body: '' };
        return json(200, { ok: true, name: a.name, role: a.role || 'contributor' }, h);
      }
      if (m === 'GET' && p === '/me') {
        if (!sess) return json(401, { error: 'not signed in' });
        return json(200, { name: sess.name, role: sess.role });
      }
      if (m === 'GET' && p === '/fiche') {                        // the record and its sha, for a private repository
        if (!sess) return json(401, { error: 'not signed in' });
        const path = String(url.searchParams.get('path') || '');
        if (!insideContent(path)) return json(403, { error: 'reads are limited to ' + cfg.contentDirs.join(', ') });
        /* a contribution of mine waiting on this fiche: the form reopens MY
           version, from its branch, and says which pull request it is */
        const open = await openPrFor(path);
        const mine = isMine(open, sess);
        const ref = mine ? open.head.ref : cfg.baseBranch;
        const cur = await gh('/repos/' + cfg.repo + '/contents/' + path + '?ref=' + encodeURIComponent(ref));
        if (!cur.ok) return json(404, { error: 'no such record on ' + ref });
        const text = Buffer.from(cur.json.content || '', 'base64').toString('utf8');
        const out = { path, sha: cur.json.sha, text, record: load(text) };
        if (open) out.pending = pendingOf(open, sess);
        return json(200, out, { 'cache-control': 'no-store' });
      }
      if (m === 'POST' && (p === '/contrib' || p === '/contrib/new')) {
        if (!sess) return json(401, { error: 'not signed in', keep: true });
        if (p === '/contrib/new') return await createNew(sess, body);
        if (Array.isArray(body.files)) return await contributeMany(sess, body);
        return await contribute(sess, body);
      }
      return json(404, { error: 'no such route' });
    } catch (e) {
      log('error: ' + (e && e.message));
      return json(502, { error: String(e && e.message || e), keep: true });
    }
  }

  async function contribute(sess, body) {
    const path = String(body.path || '');
    if (!insideContent(path)) return json(403, { error: 'writes are limited to ' + cfg.contentDirs.join(', ') });
    if (!body.record || typeof body.record !== 'object') return json(400, { error: 'record required', keep: true });
    if (!body.baseSha) return json(400, { error: 'baseSha required', message: 'send the sha of the record as it was opened (GET /fiche gives it)', keep: true });
    const slug = slugOf(path);
    /* MY WAITING CONTRIBUTION FIRST (0.3.2, Toni: "for a new fiche still
       pending, the read of main fails before addToMine"): a record I
       created lives only on my branch until it is merged */
    const open = await openPrFor(path);
    const cur = await gh('/repos/' + cfg.repo + '/contents/' + path + '?ref=' + encodeURIComponent(cfg.baseBranch));
    if (open && isMine(open, sess)) return await addToMine(sess, body, path, open, cur.ok ? cur : null);
    if (!cur.ok) {
      if (open) return json(409, { error: 'open pull request', keep: true,
        message: 'this record is new and still waiting: #' + open.number,
        pr: { number: open.number, url: open.html_url }, pending: pendingOf(open, sess) });
      return json(404, { error: 'no such record on ' + cfg.baseBranch, keep: true });
    }
    if (body.baseSha !== cur.json.sha)
      return json(409, { error: 'stale', message: 'the record changed since it was opened — reload it', keep: true });
    if (open) return json(409, { error: 'open pull request', keep: true,
      message: 'a contribution on this record is already waiting: #' + open.number,
      pr: { number: open.number, url: open.html_url }, pending: pendingOf(open, sess) });
    const original = Buffer.from(cur.json.content || '', 'base64').toString('utf8');
    const touched = touchedProtected(load(original), body.record);
    if (touched.length) return json(403, { error: 'protected fields', fields: touched, keep: true,
      message: 'these fields are not the form\'s to change: ' + touched.join(', ') });
    const text = patch(original, body.record);
    if (text === original) return json(400, { error: 'nothing changed', keep: true });
    const type = String(body.type || body.record.type || 'fiche');
    const title = String(body.title || body.record.title || slug);
    const pr = await writeAsPr(sess, { path, text, sha: cur.json.sha, title: title, type: cap(type), message: body.message });
    return json(201, { ok: true, pr });
  }

  /* a second save of MY waiting contribution: one more commit on its
     branch, the same pull request, kept up to date for the reviewer.
     baseSha is the branch's (GET /fiche gave it); protected fields are
     judged against the published record — or, for a record not published
     yet, against the branch's version, whose id and slug the gateway wrote */
  async function addToMine(sess, body, path, open, main) {
    const branch = open.head.ref;
    const mine = await gh('/repos/' + cfg.repo + '/contents/' + path + '?ref=' + encodeURIComponent(branch));
    if (!mine.ok) return json(404, { error: 'no such record on ' + branch, keep: true });
    if (body.baseSha !== mine.json.sha)
      return json(409, { error: 'stale', message: 'your waiting version changed since it was opened — reload it', keep: true });
    const published = Buffer.from((main || mine).json.content || '', 'base64').toString('utf8');
    const touched = touchedProtected(load(published), body.record);
    if (touched.length) return json(403, { error: 'protected fields', fields: touched, keep: true,
      message: 'these fields are not the form\'s to change: ' + touched.join(', ') });
    const before = Buffer.from(mine.json.content || '', 'base64').toString('utf8');
    const text = patch(before, body.record);
    if (text === before) return json(400, { error: 'nothing changed', keep: true });
    const title = String(body.title || body.record.title || slugOf(path));
    const commitMsg = (body.message || ('Update: ' + title)) + '\n\nCo-authored-by: ' + sess.name + ' <' + cfg.coauthorEmail + '>';
    const put = await gh('/repos/' + cfg.repo + '/contents/' + path, { method: 'PUT',
      body: { message: commitMsg, content: Buffer.from(text, 'utf8').toString('base64'), branch, sha: mine.json.sha } });
    if (!put.ok) throw new Error('cannot write the file (' + put.status + ')');
    return json(200, { ok: true, updated: true,
      pr: { number: open.number, url: open.html_url, branch, autoMerge: !!open.auto_merge } });
  }

  /* SEVERAL FILES, ONE CONTRIBUTION (0.3.1, Toni: "the new address and the
     event that points to it, in the same branch and the same pull request").
     files: [{ path, baseSha, record }   an edit, as /contrib
             { kind, title, record }]    a new record, as /contrib/new
     Every file is checked first; one refusal and nothing is written. A file
     already in a waiting contribution refuses the bundle (save it there). */
  const MAX_FILES = 10;
  async function contributeMany(sess, body) {
    const items = body.files;
    if (!items.length) return json(400, { error: 'files is empty', keep: true });
    if (items.length > MAX_FILES) return json(400, { error: 'at most ' + MAX_FILES + ' files in one contribution', keep: true });
    const files = [], seen = {}, out = [];
    for (let i = 0; i < items.length; i++) {
      const it = items[i] || {}, where = { file: i };
      if (!it.record || typeof it.record !== 'object') return json(400, { error: 'record required', ...where, keep: true });
      if (it.kind != null) {                                       // a new record
        if (!cfg.allowCreate) return json(403, { error: 'creating records is off', ...where, keep: true });
        const dir = cfg.contentDirs.find((d) => d.replace(/\/$/, '').split('/').pop() === String(it.kind));
        if (!dir) return json(403, { error: 'kind must be one of ' + cfg.contentDirs.map((d) => d.split('/').pop()).join(', '), ...where, keep: true });
        const title = String(it.title || it.record.title || '').trim();
        if (!title) return json(400, { error: 'title required', ...where, keep: true });
        const slug = slugify(title), path = dir.replace(/\/$/, '') + '/' + slug + '.yaml';
        if (seen[path]) return json(400, { error: 'the same file twice', path, ...where, keep: true });
        const exists = await gh('/repos/' + cfg.repo + '/contents/' + path + '?ref=' + encodeURIComponent(cfg.baseBranch));
        if (exists.ok) return json(409, { error: 'a record with this slug already exists', path, ...where, keep: true });
        const record = { id: slug, slug, ...it.record };
        record.id = slug; record.slug = slug; record.title = title;
        const touched = touchedProtected({ id: slug, slug }, record).filter((f) => f !== 'id' && f !== 'slug');
        if (touched.length) return json(403, { error: 'protected fields', fields: touched, ...where, keep: true });
        const text = dump(record); load(text);
        const type = String(record.type || String(it.kind).replace(/s$/, ''));
        seen[path] = 1;
        files.push({ path, text, sha: null, message: cap(type) + ': ' + title, title, type });
        out.push({ path, slug, created: true });
      } else {                                                      // an edit
        const path = String(it.path || '');
        if (!insideContent(path)) return json(403, { error: 'writes are limited to ' + cfg.contentDirs.join(', '), ...where });
        if (seen[path]) return json(400, { error: 'the same file twice', path, ...where, keep: true });
        if (!it.baseSha) return json(400, { error: 'baseSha required', ...where, keep: true });
        const cur = await gh('/repos/' + cfg.repo + '/contents/' + path + '?ref=' + encodeURIComponent(cfg.baseBranch));
        if (!cur.ok) {
          const waiting = await openPrFor(path);                  /* new, still waiting: save it there */
          if (waiting) return json(409, { error: 'open pull request', path, ...where, keep: true, pending: pendingOf(waiting, sess),
            message: 'this record is new and still waiting: #' + waiting.number });
          return json(404, { error: 'no such record on ' + cfg.baseBranch, path, ...where, keep: true });
        }
        if (it.baseSha !== cur.json.sha) return json(409, { error: 'stale', path, ...where, keep: true,
          message: 'the record changed since it was opened — reload it' });
        const open = await openPrFor(path);
        if (open) return json(409, { error: 'open pull request', path, ...where, keep: true, pending: pendingOf(open, sess),
          message: 'a contribution on ' + path + ' is already waiting: #' + open.number });
        const original = Buffer.from(cur.json.content || '', 'base64').toString('utf8');
        const touched = touchedProtected(load(original), it.record);
        if (touched.length) return json(403, { error: 'protected fields', fields: touched, path, ...where, keep: true });
        const text = patch(original, it.record);
        if (text === original) return json(400, { error: 'nothing changed', path, ...where, keep: true });
        const title = String(it.record.title || slugOf(path)), type = String(it.record.type || 'fiche');
        seen[path] = 1;
        files.push({ path, text, sha: cur.json.sha, message: cap(type) + ': ' + title, title, type });
        out.push({ path, slug: slugOf(path), created: false });
      }
    }
    /* new records first: what the others point to exists before them */
    const order = files.map((f, i) => i).sort((a, b) => (files[a].sha ? 1 : 0) - (files[b].sha ? 1 : 0));
    const sorted = order.map((i) => files[i]);
    /* the title wears the MAIN file: the last written, the one the new
       records serve (0.3.3, Toni: "Address: Événement : … (+2)" — the event
       is the fiche, the address its helper); body.type still wins */
    const main = sorted[sorted.length - 1];
    const title = String(body.title || (main.title + (sorted.length > 1 ? ' (+' + (sorted.length - 1) + ')' : '')));
    const pr = await writeAsPr(sess, { files: sorted, title, type: cap(String(body.type || main.type)), message: body.message });
    return json(201, { ok: true, pr, files: out });            /* in the order the form sent them */
  }

  async function createNew(sess, body) {
    if (!cfg.allowCreate) return json(403, { error: 'creating records is off' });
    const kind = String(body.kind || '');
    const dir = cfg.contentDirs.find((d) => d.replace(/\/$/, '').split('/').pop() === kind);
    if (!dir) return json(403, { error: 'kind must be one of ' + cfg.contentDirs.map((d) => d.split('/').pop()).join(', ') });
    const title = String(body.title || (body.record && body.record.title) || '').trim();
    if (!title) return json(400, { error: 'title required', keep: true });
    const slug = slugify(title);
    const path = dir.replace(/\/$/, '') + '/' + slug + '.yaml';
    const exists = await gh('/repos/' + cfg.repo + '/contents/' + path + '?ref=' + encodeURIComponent(cfg.baseBranch));
    if (exists.ok) return json(409, { error: 'a record with this slug already exists', path, keep: true });
    const record = { id: slug, slug, ...(body.record || {}) };
    record.id = slug; record.slug = slug; record.title = title;
    const touched = touchedProtected({ id: slug, slug }, record).filter((f) => f !== 'id' && f !== 'slug');
    if (touched.length) return json(403, { error: 'protected fields', fields: touched, keep: true,
      message: 'these fields are not the form\'s to set: ' + touched.join(', ') });
    const type = String(record.type || kind.replace(/s$/, ''));
    const text = dump(record);
    load(text);                                                   // must parse back
    const pr = await writeAsPr(sess, { path, text, sha: null, title, type: cap(type), message: body.message });
    return json(201, { ok: true, pr, path });
  }

  return { request, config: cfg, version: GATEWAY_VERSION,
           setAllowlist(list) { cfg.allowlist = list; },
           _links: links, _hits: hits };
}

function safeJson(s) { try { return JSON.parse(s || '{}'); } catch (e) { return {}; } }
const cap = (s) => s ? s[0].toUpperCase() + s.slice(1) : s;
export function slugify(s) {
  return String(s).normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase()
    .replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 80) || 'record';
}
