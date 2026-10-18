/*!
 * BDD non-regression suite for @karmicsoft/lc-gateway.
 * Zero-dependency: a tiny Feature/Scenario harness over node:assert.
 * Run: node test.mjs   (or `npm test`)
 *
 * The sign-in and write features are a partner's acceptance text. GitHub and
 * Brevo are replaced by a small in-memory GitHub and a mailbox; the clock is
 * ours. The real records come from the lab (partners/…, never published);
 * without them one synthetic record of the same shape carries every scenario.
 * LIVE=1 with a throwaway repository runs the write scenarios for real
 * (see DEPLOY.md § live test) — off by default, never in CI.
 */
import { createGateway, slugify } from './index.js';
import { configFromEnv } from './config.js';
import { load } from '@karmicsoft/lc-serialize';
import assert from 'node:assert';
import { readFileSync, readdirSync, existsSync, writeFileSync, mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { generateKeyPairSync, createHash } from 'node:crypto';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

let scen = 0, fail = 0;
function feature(name) { console.log('\nFeature: ' + name); }
async function scenario(name, fn) {
  scen++;
  try { await fn(); console.log('  ✓ ' + name); }
  catch (e) { fail++; console.log('  ✗ ' + name + '\n      ' + (e.message || e)); }
}
const eq = assert.strictEqual, ok = assert.ok, deep = assert.deepStrictEqual;

const HERE = dirname(fileURLToPath(import.meta.url));
const FIX = join(HERE, '..', 'partners', 'bluelion', 'fixtures', 'paris-2026-09-24', 'fiches');
const fixtures = {};
if (existsSync(FIX)) {
  for (const dir of ['persons', 'events'])
    for (const f of readdirSync(join(FIX, dir))) fixtures['fiches/' + dir + '/' + f] = readFileSync(join(FIX, dir, f), 'utf8');
} else {
  /* the partner's fixtures stay in the lab; elsewhere one synthetic fiche
     of the same shape carries every scenario */
  console.log('(partner fixtures absent — running on a synthetic fiche)');
  fixtures['fiches/persons/louise-michel.yaml'] = 'id: louise-michel\nslug: louise-michel\ntype: person\ntitle: Louise Michel\ngender: féminin\naddresses:\n  - id: rue-houdon\n    role: école\n    period: 1870\nbody: ""\n';
}

// ── a small GitHub, in memory ──────────────────────────────────────────
function fakeGitHub(files) {
  const sha = (t) => createHash('sha1').update(t).digest('hex');
  const g = { main: { ...files }, branches: {}, commits: [], prs: [], graphql: [], nextPr: 100, tokens: 0 };
  g.fetch = async (url, init = {}) => {
    const u = new URL(url), p = u.pathname, m = (init.method || 'GET').toUpperCase();
    const body = init.body ? JSON.parse(init.body) : {};
    const reply = (status, json) => ({ ok: status < 400, status, json: async () => json });
    let mm;
    if (p === '/graphql') { g.graphql.push(body); return reply(200, { data: { enablePullRequestAutoMerge: { clientMutationId: null } } }); }
    if (p === '/repos/acme/fiches/installation') return reply(200, { id: 42 });
    if (p === '/app/installations/42/access_tokens') { g.tokens++; return reply(201, { token: 'ghs_fake', expires_at: new Date(Date.now() + 3600000).toISOString() }); }
    if (p === '/repos/acme/fiches/git/ref/heads/main') return reply(200, { object: { sha: 'main-sha' } });
    if (p === '/repos/acme/fiches/git/refs' && m === 'POST') { g.branches[body.ref.replace('refs/heads/', '')] = { ...g.main }; return reply(201, {}); }
    if ((mm = /^\/repos\/acme\/fiches\/contents\/(.+)$/.exec(p))) {
      const path = decodeURIComponent(mm[1]);
      if (m === 'GET') {
        const ref = u.searchParams.get('ref') || 'main';
        const store = ref === 'main' ? g.main : g.branches[ref];
        if (!store || !(path in store)) return reply(404, { message: 'Not Found' });
        return reply(200, { sha: sha(store[path]), content: Buffer.from(store[path]).toString('base64') });
      }
      if (m === 'PUT') {
        const store = g.branches[body.branch];
        if (!store) return reply(404, { message: 'no branch' });
        store[path] = Buffer.from(body.content, 'base64').toString('utf8');
        g.commits.push({ branch: body.branch, path, message: body.message, author: body.author || null, committer: body.committer || null });
        return reply(201, { content: { sha: sha(store[path]) } });
      }
    }
    if (p === '/repos/acme/fiches/pulls' && m === 'GET') return reply(200, g.prs.filter((x) => x.state === 'open'));
    if (p === '/repos/acme/fiches/pulls' && m === 'POST') {
      const pr = { number: g.nextPr++, node_id: 'PR_' + g.nextPr, state: 'open', title: body.title, body: body.body,
                   head: { ref: body.head }, base: { ref: body.base }, html_url: 'https://github.com/acme/fiches/pull/' + (g.nextPr - 1),
                   user: { login: 'contrib-app[bot]' }, autoMerge: false };
      g.prs.push(pr); return reply(201, pr);
    }
    return reply(500, { message: 'unexpected ' + m + ' ' + p });
  };
  g.sha = (path) => sha(g.main[path]);
  return g;
}

// a real key: the App JWT is signed for real, only the GitHub behind it is ours
const PEM = generateKeyPairSync('rsa', { modulusLength: 2048 }).privateKey.export({ type: 'pkcs1', format: 'pem' });

const ALLOW = [
  { email: 'ada@example.org', name: 'Ada Test', role: 'contributor' },
  { email: 'zoe@example.org', name: 'Zoé Test', role: 'trusted' },
];
function rig(over = {}) {
  const gh = fakeGitHub(fixtures);
  const mailbox = [];
  const clock = { t: Date.UTC(2026, 8, 26, 10, 0, 0) };
  let seed = 0;
  const gw = createGateway({
    publicUrl: 'https://contrib.example.org', appUrl: 'https://parisrevolutionnaire.org/contribuer',
    repo: 'acme/fiches', contentDirs: ['fiches/persons', 'fiches/events'],
    appId: '1', privateKey: PEM, installationId: '42', sessionSecret: 's3cret',
    mailFrom: 'contrib@example.org', coauthorEmail: 'contrib@example.org', allowlist: ALLOW.map((a) => ({ ...a })), ...over,
  }, { fetch: gh.fetch, now: () => clock.t, random: () => Buffer.from('rnd-' + String(++seed).padStart(28, '0')),
       sendMail: async (m) => { mailbox.push(m); }, log: () => {} });
  const call = (method, path, body, cookie) => gw.request({ method, path, headers: cookie ? { cookie } : {}, body });
  async function signIn(email) {
    await call('POST', '/auth/request', { email });
    const link = new URL(mailbox[mailbox.length - 1].textContent.match(/https:\S+/)[0]);
    const r = await press(link.searchParams.get('t'));
    eq(r.status, 302);
    return r.headers['set-cookie'].split(';')[0];
  }
  // the volunteer presses the button on the mailed page: a form post
  const press = (t) => gw.request({ method: 'POST', path: '/auth/verify', headers: { 'content-type': 'application/x-www-form-urlencoded' }, body: 't=' + encodeURIComponent(t) });
  return { gw, gh, mailbox, clock, call, signIn, press };
}
const edit = (path, fn) => { const o = load(fixtures[path]); fn(o); return o; };

await (async () => {
feature('Contributors sign in with e-mail, without a GitHub account');
await scenario('An allowed address receives a sign-in link', async () => {
  const { call, mailbox } = rig();
  const r = await call('POST', '/auth/request', { email: 'ada@example.org' });
  eq(r.status, 202);
  eq(mailbox.length, 1);
  eq(mailbox[0].to[0].email, 'ada@example.org');
  ok(/https:\/\/contrib\.example\.org\/auth\/verify\?t=/.test(mailbox[0].textContent));
});
await scenario('An unknown address learns nothing', async () => {
  const { call, mailbox } = rig();
  const known = await call('POST', '/auth/request', { email: 'ada@example.org' });
  const unknown = await call('POST', '/auth/request', { email: 'stranger@example.org' });
  eq(mailbox.length, 1);
  eq(unknown.status, known.status);
  deep(unknown.body, known.body);
});
await scenario('A sign-in link works once', async () => {
  const { call, mailbox, press } = rig();
  await call('POST', '/auth/request', { email: 'ada@example.org' });
  const t = new URL(mailbox[0].textContent.match(/https:\S+/)[0]).searchParams.get('t');
  const first = await press(t);
  eq(first.status, 302);
  ok(/^lc_session=/.test(first.headers['set-cookie']));
  const me = await call('GET', '/me', null, first.headers['set-cookie'].split(';')[0]);
  eq(me.status, 200); deep(me.body, { name: 'Ada Test', role: 'contributor' });
  const again = await press(t);
  eq(again.status, 401);
});
await scenario('A mail scanner that opens the link consumes nothing', async () => {
  const { call, mailbox, press } = rig();
  await call('POST', '/auth/request', { email: 'ada@example.org' });
  const t = new URL(mailbox[0].textContent.match(/https:\S+/)[0]).searchParams.get('t');
  for (let i = 0; i < 3; i++) {                          // the scanner, then the volunteer's browser
    const page = await call('GET', '/auth/verify?t=' + t);
    eq(page.status, 200);
    ok(/text\/html/.test(page.headers['content-type']));
    ok(!page.headers['set-cookie'], 'a GET signed someone in');
    ok(page.body.includes('method="post"') && page.body.includes('action="https://contrib.example.org/auth/verify"'), 'no button');
    ok(page.body.includes('value="' + t + '"'), 'the page does not carry the token');
  }
  eq((await press(t)).status, 302, 'the button did not work after the scanner');
  eq((await press(t)).status, 401, 'the button worked twice');
});
await scenario('A sign-in link expires', async () => {
  const { call, mailbox, clock, press } = rig();
  await call('POST', '/auth/request', { email: 'ada@example.org' });
  const t = new URL(mailbox[0].textContent.match(/https:\S+/)[0]).searchParams.get('t');
  clock.t += 16 * 60000;
  eq((await press(t)).status, 401);
});
await scenario('A session expires', async () => {
  const { call, clock, signIn } = rig();
  const cookie = await signIn('ada@example.org');
  clock.t += 8 * 86400000;
  const r = await call('POST', '/contrib', { path: 'fiches/persons/louise-michel.yaml', record: {} }, cookie);
  eq(r.status, 401);
  eq(r.body.keep, true, 'the edit is kept in the browser');
});
await scenario('Requests are rate-limited', async () => {
  const { call } = rig();
  const codes = [];
  for (let i = 0; i < 10; i++) codes.push((await call('POST', '/auth/request', { email: 'ada@example.org' })).status);
  deep(codes.slice(0, 5), [202, 202, 202, 202, 202]);
  deep(codes.slice(5), [429, 429, 429, 429, 429]);
});
await scenario('An address gets at most ten links an hour', async () => {
  const { call, clock, mailbox } = rig();
  const codes = [];
  for (let i = 0; i < 12; i++) { codes.push((await call('POST', '/auth/request', { email: 'ada@example.org' })).status); clock.t += 4 * 60000; }
  deep(codes.filter((c) => c === 202).length, 10); eq(codes[10], 429); eq(codes[11], 429);
  eq(mailbox.length, 10);
  clock.t += 60 * 60000;
  eq((await call('POST', '/auth/request', { email: 'ada@example.org' })).status, 202);
});
await scenario('The mail quota is shared by everyone and refills daily', async () => {
  const { call, clock, mailbox } = rig({ mailPerDay: 3 });
  const codes = [];
  for (const e of ['ada@example.org', 'zoe@example.org', 'ada@example.org', 'zoe@example.org', 'stranger@example.org']) {
    codes.push((await call('POST', '/auth/request', { email: e })).status); clock.t += 60000;
  }
  deep(codes, [202, 202, 202, 429, 429], 'known and unknown answer alike once the quota is spent');
  eq(mailbox.length, 3);
  clock.t += 24 * 60 * 60000;
  eq((await call('POST', '/auth/request', { email: 'ada@example.org' })).status, 202);
});
await scenario('Nothing outlives its window in memory', async () => {
  const { gw, call, clock } = rig();
  await call('POST', '/auth/request', { email: 'ada@example.org' });
  await call('POST', '/auth/request', { email: 'zoe@example.org' });
  eq(gw._links.size, 2); eq(gw._hits.size, 2);
  clock.t += 61 * 60000;
  await call('POST', '/auth/request', { email: 'stranger@example.org' });
  eq(gw._links.size, 0, 'expired links kept'); deep([...gw._hits.keys()], ['stranger@example.org']);
});
await scenario('Removing an address revokes access', async () => {
  const { gw, call, signIn } = rig();
  const cookie = await signIn('ada@example.org');
  eq((await call('GET', '/me', null, cookie)).status, 200);
  gw.setAllowlist(ALLOW.filter((a) => a.email !== 'ada@example.org'));
  const r = await call('POST', '/contrib', { path: 'fiches/persons/louise-michel.yaml', record: {} }, cookie);
  eq(r.status, 401);
});

feature('The form reads a fiche through the gateway');
const LM = 'fiches/persons/louise-michel.yaml';
await scenario('A signed-in volunteer reads a fiche and its sha', async () => {
  const { call, gh, signIn } = rig();
  const cookie = await signIn('ada@example.org');
  const r = await call('GET', '/fiche?path=' + encodeURIComponent(LM), null, cookie);
  eq(r.status, 200, JSON.stringify(r.body));
  eq(r.body.sha, gh.sha(LM)); eq(r.body.text, fixtures[LM]); eq(r.body.record.title, 'Louise Michel');
  eq(r.headers['cache-control'], 'no-store');
});
await scenario('Reading needs a session and stays inside the content folders', async () => {
  const { call, signIn } = rig();
  eq((await call('GET', '/fiche?path=' + encodeURIComponent(LM))).status, 401);
  const cookie = await signIn('ada@example.org');
  for (const path of ['src/lib/published.ts', 'fiches/persons/../../package.json', '/etc/passwd', 'fiches/themes/x.yaml'])
    eq((await call('GET', '/fiche?path=' + encodeURIComponent(path), null, cookie)).status, 403, path);
  eq((await call('GET', '/fiche?path=fiches/persons/nobody.yaml', null, cookie)).status, 404);
});

feature('A contribution becomes one branch and one pull request');
await scenario('A contribution opens a pull request', async () => {
  const { call, gh, signIn } = rig();
  const cookie = await signIn('ada@example.org');
  const record = edit(LM, (o) => { o.addresses[0].period = 1871; });
  const r = await call('POST', '/contrib', { path: LM, baseSha: gh.sha(LM), record }, cookie);
  eq(r.status, 201, JSON.stringify(r.body));
  ok(/^contrib\/louise-michel-\d{8}-\d{4}$/.test(r.body.pr.branch), r.body.pr.branch);
  eq(gh.commits.length, 1);
  eq(gh.commits[0].branch, r.body.pr.branch);
  eq(gh.prs.length, 1); eq(gh.prs[0].base.ref, 'main'); eq(gh.prs[0].head.ref, r.body.pr.branch);
  eq(gh.prs[0].title, 'Person: Louise Michel — Ada Test');
  eq(gh.main[LM], fixtures[LM], 'main changed');
  const written = gh.branches[r.body.pr.branch][LM];
  deep(load(written), record);
  eq(written.split('\n').filter((l, i) => l !== fixtures[LM].split('\n')[i]).length, 1, 'more than the edited line moved');
});
await scenario('The commit carries the name, never the personal address', async () => {
  const { call, gh, signIn } = rig();
  const cookie = await signIn('ada@example.org');
  const r = await call('POST', '/contrib', { path: LM, baseSha: gh.sha(LM), record: edit(LM, (o) => { o.gender = 'femme'; }) }, cookie);
  eq(r.status, 201);
  const c = gh.commits[0];
  eq(c.author, null, 'the commit author is the App, never a person');
  ok(c.message.endsWith('\n\nCo-authored-by: Ada Test <contrib@example.org>'), c.message);
  const everything = JSON.stringify(gh.commits) + JSON.stringify(gh.prs) + JSON.stringify(gh.branches);
  ok(!everything.includes('ada@example.org'), 'the personal address leaked');
});
await scenario('Writes are limited to persons and events', async () => {
  const { call, gh, signIn } = rig();
  const cookie = await signIn('ada@example.org');
  for (const path of ['src/lib/published.ts', 'fiches/persons/../../package.json', 'fiches/themes/x.yaml', '/etc/passwd']) {
    const r = await call('POST', '/contrib', { path, record: { a: 1 } }, cookie);
    eq(r.status, 403, path);
  }
  eq(gh.commits.length, 0); eq(gh.prs.length, 0);
});
await scenario("A contributor's pull request waits for review", async () => {
  const { call, gh, signIn } = rig();
  const cookie = await signIn('ada@example.org');
  const r = await call('POST', '/contrib', { path: LM, baseSha: gh.sha(LM), record: edit(LM, (o) => { o.gender = 'femme'; }) }, cookie);
  eq(r.status, 201);
  eq(r.body.pr.autoMerge, false);
  eq(gh.graphql.length, 0, 'auto-merge was requested for a contributor');
});
await scenario("A trusted author's pull request merges itself after a green check", async () => {
  const { call, gh, signIn } = rig();
  const cookie = await signIn('zoe@example.org');
  const r = await call('POST', '/contrib', { path: LM, baseSha: gh.sha(LM), record: edit(LM, (o) => { o.gender = 'femme'; }) }, cookie);
  eq(r.status, 201);
  eq(r.body.pr.autoMerge, true);
  eq(gh.graphql.length, 1);
  ok(/enablePullRequestAutoMerge/.test(gh.graphql[0].query));
  eq(gh.graphql[0].variables.id, gh.prs[0].node_id);
  // the merge itself is GitHub's: auto-merge waits for the required check
  // (branch protection on main requires "fiche-check" — see DEPLOY.md)
});
await scenario("A failing check blocks a trusted author's merge", async () => {
  // GitHub's auto-merge never merges while a required check fails; the
  // gateway's part is to ask for auto-merge and nothing more — it never
  // merges by itself. Proven by the absence of any merge call.
  const { call, gh, signIn } = rig();
  const cookie = await signIn('zoe@example.org');
  await call('POST', '/contrib', { path: LM, baseSha: gh.sha(LM), record: edit(LM, (o) => { o.gender = 'femme'; }) }, cookie);
  eq(gh.prs[0].state, 'open');
  ok(!JSON.stringify(gh.graphql).includes('mergePullRequest'), 'the gateway tried to merge');
});
await scenario('Two contributors on the same fiche do not overwrite each other', async () => {
  const { call, gh, signIn, clock } = rig();
  const ada = await signIn('ada@example.org');
  const first = await call('POST', '/contrib', { path: LM, baseSha: gh.sha(LM), record: edit(LM, (o) => { o.gender = 'femme'; }) }, ada);
  eq(first.status, 201);
  clock.t += 60000;
  const zoe = await signIn('zoe@example.org');
  const r = await call('POST', '/contrib', { path: LM, baseSha: gh.sha(LM), record: edit(LM, (o) => { o.gender = 'autre'; }) }, zoe);
  eq(r.status, 409);
  eq(r.body.pr.number, first.body.pr.number);
  ok(String(r.body.message).includes('#' + first.body.pr.number));
  eq(r.body.keep, true, 'the edit is kept in the browser');
  eq(gh.prs.length, 1);
});
await scenario('An edit based on an outdated fiche is refused', async () => {
  const { call, gh, signIn } = rig();
  const cookie = await signIn('ada@example.org');
  const before = gh.sha(LM);
  gh.main[LM] = fixtures[LM].replace('gender: féminin', 'gender: femme');   // main moved
  const r = await call('POST', '/contrib', { path: LM, baseSha: before, record: edit(LM, (o) => { o.bornName = 'Louise'; }) }, cookie);
  eq(r.status, 409);
  eq(r.body.error, 'stale');
  eq(r.body.keep, true);
  eq(gh.prs.length, 0);
});
await scenario('An edit without baseSha is refused — nothing is overwritten silently', async () => {
  // reproduced by the partner on Louise Michel: a gender corrected on main came back
  const { call, gh, signIn } = rig();
  const cookie = await signIn('ada@example.org');
  const opened = edit(LM, (o) => { o.bornName = 'Louise'; });           // opened before main moved…
  gh.main[LM] = fixtures[LM].replace('gender: féminin', 'gender: femme'); // …the correction on main
  const r = await call('POST', '/contrib', { path: LM, record: opened }, cookie);
  eq(r.status, 400); eq(r.body.error, 'baseSha required'); eq(r.body.keep, true);
  eq(gh.prs.length, 0);
  ok(gh.main[LM].includes('gender: femme'), 'the correction on main was lost');
});
await scenario('Protected fields are refused, whatever the role', async () => {
  const { call, gh, signIn } = rig();
  for (const email of ['ada@example.org', 'zoe@example.org']) {
    const cookie = await signIn(email);
    const cases = [
      ['slug', (o) => { o.slug = 'elsewhere'; }],
      ['id', (o) => { o.id = 'elsewhere'; }],
      ['workflow.published', (o) => { o.workflow = { ...(o.workflow || {}), published: false }; }],
      ['workflow.validated', (o) => { o.workflow = { ...(o.workflow || {}), validated: false }; }],
      ['periods', (o) => { o.periods = ['none']; }],
      ['withdrawnReason', (o) => { o.withdrawnReason = 'gone'; }],
    ];
    for (const [field, fn] of cases) {
      const r = await call('POST', '/contrib', { path: LM, baseSha: gh.sha(LM), record: edit(LM, fn) }, cookie);
      eq(r.status, 403, email + ' ' + field + ': ' + JSON.stringify(r.body));
      deep(r.body.fields, [field]); eq(r.body.keep, true);
    }
  }
  eq(gh.prs.length, 0, 'a pull request opened'); eq(gh.graphql.length, 0, 'auto-merge was requested');
});
await scenario('A new record cannot arrive with protected fields set', async () => {
  const { call, gh, signIn } = rig();
  const cookie = await signIn('zoe@example.org');
  const r = await call('POST', '/contrib/new', { kind: 'persons', title: 'Jeanne Test',
    record: { type: 'person', title: 'Jeanne Test', periods: ['commune-de-1871'], workflow: { published: true } } }, cookie);
  eq(r.status, 403); deep(r.body.fields, ['workflow.published', 'periods']);
  eq(gh.prs.length, 0);
});
await scenario('A contributor creates a new person', async () => {
  const { call, gh, signIn } = rig();
  const cookie = await signIn('ada@example.org');
  const r = await call('POST', '/contrib/new', { kind: 'persons', title: 'Jeanne Test',
    record: { id: 'hacked', slug: 'hacked', type: 'person', title: 'Jeanne Test', professions: ['couturière'] } }, cookie);
  eq(r.status, 201, JSON.stringify(r.body));
  eq(r.body.path, 'fiches/persons/jeanne-test.yaml');
  eq(gh.commits.length, 1);
  const files = Object.keys(gh.branches[r.body.pr.branch]).filter((p) => !(p in gh.main));
  deep(files, ['fiches/persons/jeanne-test.yaml']);
  const o = load(gh.branches[r.body.pr.branch][files[0]]);
  eq(o.id, 'jeanne-test'); eq(o.slug, 'jeanne-test');
  eq(gh.prs[0].title, 'Person: Jeanne Test — Ada Test');
});

feature('Housekeeping');
await scenario('slugify derives ids the way a French corpus spells them', async () => {
  eq(slugify('4ème siège de la maison d’édition Gallimard'), '4eme-siege-de-la-maison-d-edition-gallimard');
  eq(slugify('Nicolas de Condorcet'), 'nicolas-de-condorcet');
});
await scenario('Creation can be switched off by configuration', async () => {
  const { call, signIn } = rig({ allowCreate: false });
  const cookie = await signIn('ada@example.org');
  eq((await call('POST', '/contrib/new', { kind: 'persons', title: 'X', record: {} }, cookie)).status, 403);
});
await scenario('The installation token is minted once and reused', async () => {
  const { call, gh, signIn } = rig();
  const cookie = await signIn('ada@example.org');
  await call('POST', '/contrib', { path: LM, baseSha: gh.sha(LM), record: edit(LM, (o) => { o.gender = 'femme'; }) }, cookie);
  eq(gh.tokens, 1);
});

feature('The gateway reads an env file the way docker run --env-file writes it (0.2.1, Toni)');
const ENV = { PUBLIC_URL: 'https://contrib.example.org', GITHUB_REPO: 'acme/fiches', CONTENT_DIRS: 'fiches/persons',
              SESSION_SECRET: 's3cret', COAUTHOR_EMAIL: 'contrib@example.org' };
const oneLine = (pem) => pem.trim().split('\n').join('\\n');      // the PEM on one line, \n written out
await scenario('A quoted key with written \\n loads as a valid PEM', async () => {
  const cfg = configFromEnv({ ...ENV, GITHUB_APP_PRIVATE_KEY: '"' + oneLine(PEM) + '"' });
  eq(cfg.privateKey, PEM.trim());
  ok(cfg.privateKey.startsWith('-----BEGIN RSA PRIVATE KEY-----\n'));
});
await scenario('An unquoted key with real line breaks loads unchanged', async () => {
  eq(configFromEnv({ ...ENV, GITHUB_APP_PRIVATE_KEY: PEM }).privateKey, PEM);
});
await scenario('GITHUB_APP_PRIVATE_KEY_FILE loads the key; setting both refuses to start', async () => {
  const f = join(mkdtempSync(join(tmpdir(), 'lcgw-')), 'app.pem');
  writeFileSync(f, PEM);
  eq(configFromEnv({ ...ENV, GITHUB_APP_PRIVATE_KEY_FILE: f }).privateKey, PEM);
  assert.throws(() => configFromEnv({ ...ENV, GITHUB_APP_PRIVATE_KEY_FILE: f, GITHUB_APP_PRIVATE_KEY: PEM }), /not both/);
});
await scenario('An invalid key refuses to start, naming the variable and never the key', async () => {
  const secret = '-----BEGIN RSA PRIVATE KEY-----\\nnot-a-key-SECRET-BYTES\\n-----END RSA PRIVATE KEY-----';
  let msg = '';
  try { configFromEnv({ ...ENV, GITHUB_APP_PRIVATE_KEY: secret }); } catch (e) { msg = e.message; }
  ok(/GITHUB_APP_PRIVATE_KEY/.test(msg), 'no refusal: ' + msg);
  ok(!/SECRET-BYTES|not-a-key/.test(msg), 'the message leaks the key: ' + msg);
});
await scenario('A quoted MAIL_TEXT with written \\n mails several lines', async () => {
  const env = configFromEnv({ ...ENV, GITHUB_APP_PRIVATE_KEY: PEM, MAIL_SUBJECT: '"Votre lien"',
    MAIL_TEXT: '"Bonjour {name},\\n\\n{link}\\n\\nÀ bientôt"' });
  eq(env.mailSubject, 'Votre lien');
  const { call, mailbox } = rig({ mailText: env.mailText, mailSubject: env.mailSubject });
  await call('POST', '/auth/request', { email: 'ada@example.org' });
  const body = mailbox[0].textContent;
  ok(body.startsWith('Bonjour Ada Test,\n\nhttps://'), JSON.stringify(body));
  ok(!body.includes('\\n') && !body.includes('"'), JSON.stringify(body));
});
await scenario('After a restart, a session still holds; a link mailed before it is refused', async () => {
  const before = rig();
  const cookie = await before.signIn('ada@example.org');
  await before.call('POST', '/auth/request', { email: 'zoe@example.org' });
  const pending = new URL(before.mailbox[before.mailbox.length - 1].textContent.match(/https:\S+/)[0]).searchParams.get('t');
  const after = rig();                                   // a new instance, the same SESSION_SECRET
  eq((await after.call('GET', '/me', null, cookie)).status, 200);
  eq((await after.press(pending)).status, 401);
});

feature('A volunteer comes back to a contribution still waiting (0.3.0, Toni: 1 oui, 2a, 3a)');
const lmPath = encodeURIComponent(LM);
await scenario('Reopening a fiche with my waiting contribution shows my version and its pull request', async () => {
  const { call, gh, signIn } = rig();
  const ada = await signIn('ada@example.org');
  const first = await call('POST', '/contrib', { path: LM, baseSha: gh.sha(LM), record: edit(LM, (o) => { o.gender = 'femme'; }) }, ada);
  eq(first.status, 201);
  const r = await call('GET', '/fiche?path=' + lmPath, null, ada);
  eq(r.status, 200);
  eq(r.body.record.gender, 'femme', 'the published version came back');
  deep(r.body.pending, { number: first.body.pr.number, url: first.body.pr.url, mine: true });
  ok(!JSON.stringify(gh.prs).includes('ada@example.org'), 'the owner mark is the address itself');
});
await scenario('A second save adds a commit to my pull request, not a second one', async () => {
  const { call, gh, signIn, clock } = rig();
  const ada = await signIn('ada@example.org');
  const first = await call('POST', '/contrib', { path: LM, baseSha: gh.sha(LM), record: edit(LM, (o) => { o.gender = 'femme'; }) }, ada);
  clock.t += 60000;
  const mine = await call('GET', '/fiche?path=' + lmPath, null, ada);
  const rec = mine.body.record; rec.addresses[0].period = 1871;
  const r = await call('POST', '/contrib', { path: LM, baseSha: mine.body.sha, record: rec }, ada);
  eq(r.status, 200, JSON.stringify(r.body));
  eq(r.body.updated, true); eq(r.body.pr.number, first.body.pr.number);
  eq(gh.prs.length, 1, 'a second pull request was opened');
  eq(gh.commits.length, 2); eq(gh.commits[1].branch, first.body.pr.branch);
  ok(gh.commits[1].message.endsWith('Co-authored-by: Ada Test <contrib@example.org>'), gh.commits[1].message);
  const now = load(gh.branches[first.body.pr.branch][LM]);
  eq(now.gender, 'femme'); eq(now.addresses[0].period, 1871);
  eq(gh.main[LM], fixtures[LM], 'main changed');
});
await scenario("Someone else's waiting contribution: the published version, and the same 409", async () => {
  const { call, gh, signIn, clock } = rig();
  const ada = await signIn('ada@example.org');
  const first = await call('POST', '/contrib', { path: LM, baseSha: gh.sha(LM), record: edit(LM, (o) => { o.gender = 'femme'; }) }, ada);
  clock.t += 60000;
  const zoe = await signIn('zoe@example.org');
  const r = await call('GET', '/fiche?path=' + lmPath, null, zoe);
  eq(r.body.sha, gh.sha(LM)); eq(r.body.text, fixtures[LM]);
  deep(r.body.pending, { number: first.body.pr.number, url: first.body.pr.url, mine: false });
  const w = await call('POST', '/contrib', { path: LM, baseSha: r.body.sha, record: edit(LM, (o) => { o.gender = 'autre'; }) }, zoe);
  eq(w.status, 409); eq(w.body.pending.mine, false); eq(gh.commits.length, 1);
});
await scenario('A pull request opened before 0.3.0 has no owner mark: it is nobody\'s, as before', async () => {
  const { call, gh, signIn } = rig();
  const ada = await signIn('ada@example.org');
  await call('POST', '/contrib', { path: LM, baseSha: gh.sha(LM), record: edit(LM, (o) => { o.gender = 'femme'; }) }, ada);
  gh.prs[0].body = 'Contribution by Ada Test through the gateway. File: `' + LM + '`.';   // a 0.2 pull request
  const r = await call('GET', '/fiche?path=' + lmPath, null, ada);
  eq(r.body.text, fixtures[LM]); eq(r.body.pending.mine, false);
  eq((await call('POST', '/contrib', { path: LM, baseSha: gh.sha(LM), record: edit(LM, (o) => { o.gender = 'autre'; }) }, ada)).status, 409);
});
await scenario('My second save is still refused protected fields, and a stale or empty save', async () => {
  const { call, gh, signIn } = rig();
  const ada = await signIn('ada@example.org');
  await call('POST', '/contrib', { path: LM, baseSha: gh.sha(LM), record: edit(LM, (o) => { o.gender = 'femme'; }) }, ada);
  const mine = await call('GET', '/fiche?path=' + lmPath, null, ada);
  const bad = JSON.parse(JSON.stringify(mine.body.record)); bad.slug = 'someone-else';
  eq((await call('POST', '/contrib', { path: LM, baseSha: mine.body.sha, record: bad }, ada)).status, 403);
  eq((await call('POST', '/contrib', { path: LM, baseSha: gh.sha(LM), record: mine.body.record }, ada)).body.error, 'stale');
  eq((await call('POST', '/contrib', { path: LM, baseSha: mine.body.sha, record: mine.body.record }, ada)).body.error, 'nothing changed');
  eq(gh.commits.length, 1);
});
await scenario('A waiting contribution on louise-michel-bis is not louise-michel\'s', async () => {
  const { call, gh, signIn } = rig();
  const ada = await signIn('ada@example.org');
  gh.prs.push({ number: 7, node_id: 'PR_7', state: 'open', title: 'x', body: '', head: { ref: 'contrib/louise-michel-bis-20260926-0900' },
                base: { ref: 'main' }, html_url: 'https://github.com/acme/fiches/pull/7' });
  const r = await call('GET', '/fiche?path=' + lmPath, null, ada);
  eq(r.body.pending, undefined, 'another fiche\'s pull request was taken for this one');
  eq((await call('POST', '/contrib', { path: LM, baseSha: gh.sha(LM), record: edit(LM, (o) => { o.gender = 'femme'; }) }, ada)).status, 201);
});
await scenario('A new record still waiting reads back for its author', async () => {
  const { call, signIn } = rig();
  const ada = await signIn('ada@example.org');
  const c = await call('POST', '/contrib/new', { kind: 'persons', title: 'Jeanne Test', record: { type: 'person', gender: 'féminin' } }, ada);
  eq(c.status, 201, JSON.stringify(c.body));
  const r = await call('GET', '/fiche?path=' + encodeURIComponent('fiches/persons/jeanne-test.yaml'), null, ada);
  eq(r.status, 200, JSON.stringify(r.body)); eq(r.body.record.title, 'Jeanne Test'); eq(r.body.pending.mine, true);
});
await scenario('A new record still waiting takes its author\'s next save — same pull request (0.3.2, Toni)', async () => {
  /* Toni, 2026-10-18: "POST /contrib with this baseSha answers 404 no such
     record on main: the fiche exists only in my branch" */
  const { call, gh, signIn } = rig();
  const ada = await signIn('ada@example.org');
  const c = await call('POST', '/contrib/new', { kind: 'persons', title: 'Jeanne Test', record: { type: 'person', gender: 'féminin' } }, ada);
  const path = 'fiches/persons/jeanne-test.yaml';
  const mine = await call('GET', '/fiche?path=' + encodeURIComponent(path), null, ada);
  const rec = mine.body.record; rec.gender = 'femme';
  const r = await call('POST', '/contrib', { path, baseSha: mine.body.sha, record: rec }, ada);
  eq(r.status, 200, JSON.stringify(r.body)); eq(r.body.updated, true); eq(r.body.pr.number, c.body.pr.number);
  eq(gh.prs.length, 1); eq(gh.commits.length, 2);
  eq(gh.main[path], undefined, 'main was written');
  /* judged against the branch's version: its id and slug stay the gateway's */
  const again = await call('GET', '/fiche?path=' + encodeURIComponent(path), null, ada);
  const bad = again.body.record; bad.slug = 'elsewhere';
  const p403 = await call('POST', '/contrib', { path, baseSha: again.body.sha, record: bad }, ada);
  eq(p403.status, 403, JSON.stringify(p403.body)); deep(p403.body.fields, ['slug']);
});
await scenario('Someone else\'s new record still waiting says so — not "no such record"', async () => {
  const { call, gh, signIn, clock } = rig();
  const zoe = await signIn('zoe@example.org');
  const c = await call('POST', '/contrib/new', { kind: 'persons', title: 'Jeanne Test', record: { type: 'person' } }, zoe);
  clock.t += 60000;
  const ada = await signIn('ada@example.org');
  const path = 'fiches/persons/jeanne-test.yaml';
  const r = await call('POST', '/contrib', { path, baseSha: 'whatever', record: { type: 'person', gender: 'x' } }, ada);
  eq(r.status, 409, JSON.stringify(r.body)); eq(r.body.error, 'open pull request'); eq(r.body.pending.mine, false);
  eq(r.body.pending.number, c.body.pr.number);
  const b = await call('POST', '/contrib', { files: [{ path, baseSha: 'whatever', record: { type: 'person' } }] }, ada);
  eq(b.status, 409, JSON.stringify(b.body)); eq(b.body.error, 'open pull request');
  eq(gh.prs.length, 1);
});

feature('Several files, one contribution (0.3.1, Toni: the new address and the event that points to it)');
const JT = 'fiches/persons/jeanne-test.yaml';
await scenario('A new record and an edit pointing to it travel in one branch and one pull request', async () => {
  const { call, gh, signIn } = rig();
  const ada = await signIn('ada@example.org');
  const r = await call('POST', '/contrib', { files: [
    { path: LM, baseSha: gh.sha(LM), record: edit(LM, (o) => { o.gender = 'femme'; }) },
    { kind: 'persons', title: 'Jeanne Test', record: { type: 'person', gender: 'féminin' } },
  ] }, ada);
  eq(r.status, 201, JSON.stringify(r.body));
  eq(gh.prs.length, 1); eq(gh.commits.length, 2);
  eq(gh.commits[0].path, JT, 'the new record is written first');
  eq(gh.commits[1].path, LM);
  ok(gh.commits.every((c) => c.branch === r.body.pr.branch));
  deep(r.body.files, [{ path: LM, slug: 'louise-michel', created: false }, { path: JT, slug: 'jeanne-test', created: true }]);
  ok(gh.prs[0].body.includes('`' + JT + '`') && gh.prs[0].body.includes('`' + LM + '`'), gh.prs[0].body);
  eq(gh.main[LM], fixtures[LM], 'main changed');
  ok(!JSON.stringify(gh.prs).includes('ada@example.org'), 'the personal address leaked');
});
await scenario('A bundle\'s title wears the type of its main file, the last written — not the first (0.3.3, Toni)', async () => {
  /* Toni, 2026-10-18: "the title takes the type of the first file written,
     the address, while the main fiche is the event: Address: Événement : … (+2)" */
  const { call, gh, signIn } = rig();
  const ada = await signIn('ada@example.org');
  const r = await call('POST', '/contrib', { title: 'Événement : la rue Houdon', files: [
    { path: LM, baseSha: gh.sha(LM), record: edit(LM, (o) => { o.gender = 'femme'; }) },
    { kind: 'persons', title: 'Jeanne Test', record: { type: 'address' } },
  ] }, ada);
  eq(r.status, 201, JSON.stringify(r.body));
  eq(gh.commits[0].path, JT, 'the new record is still written first');
  eq(gh.prs[0].title, 'Person: Événement : la rue Houdon — Ada Test');
  const { call: call2, gh: gh2, signIn: signIn2 } = rig();
  const zoe = await signIn2('zoe@example.org');
  const r2 = await call2('POST', '/contrib', { files: [
    { path: LM, baseSha: gh2.sha(LM), record: edit(LM, (o) => { o.gender = 'femme'; }) },
    { kind: 'persons', title: 'Jeanne Test', record: { type: 'address' } },
  ] }, zoe);
  eq(r2.status, 201, JSON.stringify(r2.body));
  eq(gh2.prs[0].title, 'Person: Louise Michel (+1) — Zoé Test');
});
await scenario('One refusal and nothing is written', async () => {
  const { call, gh, signIn } = rig();
  const ada = await signIn('ada@example.org');
  const r = await call('POST', '/contrib', { files: [
    { kind: 'persons', title: 'Jeanne Test', record: { type: 'person' } },
    { path: LM, baseSha: gh.sha(LM), record: edit(LM, (o) => { o.slug = 'elsewhere'; }) },
  ] }, ada);
  eq(r.status, 403); eq(r.body.file, 1); eq(r.body.keep, true);
  eq(gh.commits.length, 0); eq(gh.prs.length, 0); eq(Object.keys(gh.branches).length, 0, 'a branch was created');
});
await scenario('A file already in a waiting contribution refuses the bundle, saying which', async () => {
  const { call, gh, signIn, clock } = rig();
  const zoe = await signIn('zoe@example.org');
  const first = await call('POST', '/contrib', { path: LM, baseSha: gh.sha(LM), record: edit(LM, (o) => { o.gender = 'femme'; }) }, zoe);
  clock.t += 60000;
  const ada = await signIn('ada@example.org');
  const r = await call('POST', '/contrib', { files: [
    { kind: 'persons', title: 'Jeanne Test', record: { type: 'person' } },
    { path: LM, baseSha: gh.sha(LM), record: edit(LM, (o) => { o.gender = 'autre'; }) },
  ] }, ada);
  eq(r.status, 409); eq(r.body.file, 1); eq(r.body.pending.number, first.body.pr.number);
  eq(gh.prs.length, 1); eq(gh.commits.length, 1);
});
await scenario('Back on a file of my bundle, I read my version and my save joins the bundle', async () => {
  const { call, gh, signIn, clock } = rig();
  const ada = await signIn('ada@example.org');
  const b = await call('POST', '/contrib', { files: [
    { kind: 'persons', title: 'Jeanne Test', record: { type: 'person' } },
    { path: LM, baseSha: gh.sha(LM), record: edit(LM, (o) => { o.gender = 'femme'; }) },
  ] }, ada);
  clock.t += 60000;
  const mine = await call('GET', '/fiche?path=' + encodeURIComponent(LM), null, ada);
  eq(mine.body.pending.mine, true); eq(mine.body.pending.number, b.body.pr.number); eq(mine.body.record.gender, 'femme');
  const rec = mine.body.record; rec.addresses[0].period = 1871;
  const r = await call('POST', '/contrib', { path: LM, baseSha: mine.body.sha, record: rec }, ada);
  eq(r.status, 200, JSON.stringify(r.body)); eq(r.body.pr.number, b.body.pr.number);
  eq(gh.prs.length, 1); eq(gh.commits.length, 3);
});
await scenario('A bundle refuses the same file twice, and more than ten files', async () => {
  const { call, gh, signIn } = rig();
  const ada = await signIn('ada@example.org');
  const twice = await call('POST', '/contrib', { files: [
    { path: LM, baseSha: gh.sha(LM), record: edit(LM, (o) => { o.gender = 'femme'; }) },
    { path: LM, baseSha: gh.sha(LM), record: edit(LM, (o) => { o.gender = 'autre'; }) },
  ] }, ada);
  eq(twice.status, 400); eq(twice.body.error, 'the same file twice');
  const many = await call('POST', '/contrib', { files: Array.from({ length: 11 }, (_, i) => ({ kind: 'persons', title: 'P ' + i, record: {} })) }, ada);
  eq(many.status, 400);
  eq(gh.commits.length, 0);
});
})();

console.log(`\n${scen} scenarios, ${fail} failed.`);
process.exit(fail ? 1 : 0);
