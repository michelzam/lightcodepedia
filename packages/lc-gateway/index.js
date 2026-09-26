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
import { createHmac, createSign, randomBytes, createHash } from 'node:crypto';
import { patch } from '@karmicsoft/lc-patch';
import { load, dump } from '@karmicsoft/lc-serialize';

export const GATEWAY_VERSION = '0.1.0';

const DEFAULTS = {
  baseBranch: 'main',
  branchPrefix: 'contrib',
  prTitle: '{type}: {title} — {name}',
  linkTtlMin: 15,
  sessionTtlDays: 7,
  rateLimitPerMin: 5,
  allowCreate: true,
  requiredCheck: 'fiche-check',
  mergeMethod: 'SQUASH',
  mailFromName: 'Contributions',
  mailSubject: 'Your sign-in link',
  mailText: 'Hello {name},\n\nHere is your sign-in link, valid {minutes} minutes and once only:\n\n{link}\n\nIf you did not ask for it, ignore this message.',
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
    if (!payload || !sig || sign(payload) !== sig) return null;
    let s; try { s = JSON.parse(Buffer.from(payload, 'base64url').toString('utf8')); } catch (e) { return null; }
    if (!s || !s.e || !s.x || s.x < now()) return null;
    const a = who(s.e);
    return a ? { email: norm(s.e), name: a.name, role: a.role || 'contributor' } : null;   // removal revokes
  }
  const cookieFor = (sess) => 'lc_session=' + sess + '; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=' + (cfg.sessionTtlDays * 86400);

  // ── sign-in links ────────────────────────────────────────────────────
  const hash = (t) => createHash('sha256').update(t).digest('hex');
  function rateLimited(email) {
    const t = now(), win = 60000;
    const arr = (hits.get(email) || []).filter((x) => t - x < win);
    arr.push(t); hits.set(email, arr);
    return arr.length > cfg.rateLimitPerMin;
  }
  async function sendLink(a) {
    const token = b64u(random(32));
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
  const stamp = () => { const d = new Date(now()); const z = (n) => String(n).padStart(2, '0');
    return d.getUTCFullYear() + z(d.getUTCMonth() + 1) + z(d.getUTCDate()) + '-' + z(d.getUTCHours()) + z(d.getUTCMinutes()); };
  async function openPrOn(slug) {
    const r = await gh('/repos/' + cfg.repo + '/pulls?state=open&per_page=100');
    const want = cfg.branchPrefix + '/' + slug + '-';
    return (r.ok && Array.isArray(r.json) ? r.json : []).find((p) => p.head && String(p.head.ref).startsWith(want)) || null;
  }
  async function writeAsPr(sess, { path, text, sha, title, type, message }) {
    const slug = slugOf(path);
    const branch = cfg.branchPrefix + '/' + slug + '-' + stamp();
    const base = await gh('/repos/' + cfg.repo + '/git/ref/heads/' + cfg.baseBranch);
    if (!base.ok) throw new Error('cannot read ' + cfg.baseBranch);
    const mk = await gh('/repos/' + cfg.repo + '/git/refs', { method: 'POST', body: { ref: 'refs/heads/' + branch, sha: base.json.object.sha } });
    if (!mk.ok) throw new Error('cannot create the branch (' + mk.status + ')');
    const commitMsg = (message || (type + ': ' + title)) + '\n\nCo-authored-by: ' + sess.name + ' <' + cfg.coauthorEmail + '>';
    const put = await gh('/repos/' + cfg.repo + '/contents/' + path, { method: 'PUT',
      body: { message: commitMsg, content: Buffer.from(text, 'utf8').toString('base64'), branch, ...(sha ? { sha } : {}) } });
    if (!put.ok) throw new Error('cannot write the file (' + put.status + ')');
    const prTitle = cfg.prTitle.replace('{type}', type).replace('{title}', title).replace('{name}', sess.name);
    const pr = await gh('/repos/' + cfg.repo + '/pulls', { method: 'POST',
      body: { title: prTitle, head: branch, base: cfg.baseBranch,
              body: 'Contribution by ' + sess.name + ' through the gateway. File: `' + path + '`.' } });
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
    const body = typeof req.body === 'string' ? safeJson(req.body) : (req.body || {});
    const sess = readSession(req.headers && (req.headers.cookie || req.headers.Cookie));
    try {
      if (m === 'GET' && p === '/health') return json(200, { ok: true, version: GATEWAY_VERSION });
      if (m === 'POST' && p === '/auth/request') {
        const email = norm(body.email);
        if (!email) return json(400, { error: 'email required' });
        if (rateLimited(email)) return json(429, { error: 'too many requests, try again in a minute' });
        const a = who(email);
        if (a) await sendLink(a);                          // an unknown address learns nothing
        return same202();
      }
      if (m === 'GET' && p === '/auth/verify') {
        const a = useLink(url.searchParams.get('t'));
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
      if (m === 'POST' && (p === '/contrib' || p === '/contrib/new')) {
        if (!sess) return json(401, { error: 'not signed in', keep: true });
        if (p === '/contrib/new') return await createNew(sess, body);
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
    const slug = slugOf(path);
    const cur = await gh('/repos/' + cfg.repo + '/contents/' + path + '?ref=' + encodeURIComponent(cfg.baseBranch));
    if (!cur.ok) return json(404, { error: 'no such record on ' + cfg.baseBranch, keep: true });
    if (body.baseSha && body.baseSha !== cur.json.sha)
      return json(409, { error: 'stale', message: 'the record changed since it was opened — reload it', keep: true });
    const open = await openPrOn(slug);
    if (open) return json(409, { error: 'open pull request', keep: true,
      message: 'a contribution on this record is already waiting: #' + open.number, pr: { number: open.number, url: open.html_url } });
    const original = Buffer.from(cur.json.content || '', 'base64').toString('utf8');
    const text = patch(original, body.record);
    if (text === original) return json(400, { error: 'nothing changed', keep: true });
    const type = String(body.type || body.record.type || 'fiche');
    const title = String(body.title || body.record.title || slug);
    const pr = await writeAsPr(sess, { path, text, sha: cur.json.sha, title: title, type: cap(type), message: body.message });
    return json(201, { ok: true, pr });
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
    const type = String(record.type || kind.replace(/s$/, ''));
    const text = dump(record);
    load(text);                                                   // must parse back
    const pr = await writeAsPr(sess, { path, text, sha: null, title, type: cap(type), message: body.message });
    return json(201, { ok: true, pr, path });
  }

  return { request, config: cfg, version: GATEWAY_VERSION,
           setAllowlist(list) { cfg.allowlist = list; },
           _links: links };
}

function safeJson(s) { try { return JSON.parse(s || '{}'); } catch (e) { return {}; } }
const cap = (s) => s ? s[0].toUpperCase() + s.slice(1) : s;
export function slugify(s) {
  return String(s).normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase()
    .replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 80) || 'record';
}
