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
import { load } from '@karmicsoft/lc-serialize';
import assert from 'node:assert';
import { readFileSync, readdirSync, existsSync } from 'node:fs';
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
    const r = await call('GET', '/auth/verify?t=' + link.searchParams.get('t'));
    eq(r.status, 302);
    return r.headers['set-cookie'].split(';')[0];
  }
  return { gw, gh, mailbox, clock, call, signIn };
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
  const { call, mailbox } = rig();
  await call('POST', '/auth/request', { email: 'ada@example.org' });
  const t = new URL(mailbox[0].textContent.match(/https:\S+/)[0]).searchParams.get('t');
  const first = await call('GET', '/auth/verify?t=' + t);
  eq(first.status, 302);
  ok(/^lc_session=/.test(first.headers['set-cookie']));
  const me = await call('GET', '/me', null, first.headers['set-cookie'].split(';')[0]);
  eq(me.status, 200); deep(me.body, { name: 'Ada Test', role: 'contributor' });
  const again = await call('GET', '/auth/verify?t=' + t);
  eq(again.status, 401);
});
await scenario('A sign-in link expires', async () => {
  const { call, mailbox, clock } = rig();
  await call('POST', '/auth/request', { email: 'ada@example.org' });
  const t = new URL(mailbox[0].textContent.match(/https:\S+/)[0]).searchParams.get('t');
  clock.t += 16 * 60000;
  eq((await call('GET', '/auth/verify?t=' + t)).status, 401);
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
await scenario('Removing an address revokes access', async () => {
  const { gw, call, signIn } = rig();
  const cookie = await signIn('ada@example.org');
  eq((await call('GET', '/me', null, cookie)).status, 200);
  gw.setAllowlist(ALLOW.filter((a) => a.email !== 'ada@example.org'));
  const r = await call('POST', '/contrib', { path: 'fiches/persons/louise-michel.yaml', record: {} }, cookie);
  eq(r.status, 401);
});

feature('A contribution becomes one branch and one pull request');
const LM = 'fiches/persons/louise-michel.yaml';
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
  const r = await call('POST', '/contrib', { path: LM, record: edit(LM, (o) => { o.gender = 'femme'; }) }, cookie);
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
  const r = await call('POST', '/contrib', { path: LM, record: edit(LM, (o) => { o.gender = 'femme'; }) }, cookie);
  eq(r.status, 201);
  eq(r.body.pr.autoMerge, false);
  eq(gh.graphql.length, 0, 'auto-merge was requested for a contributor');
});
await scenario("A trusted author's pull request merges itself after a green check", async () => {
  const { call, gh, signIn } = rig();
  const cookie = await signIn('zoe@example.org');
  const r = await call('POST', '/contrib', { path: LM, record: edit(LM, (o) => { o.gender = 'femme'; }) }, cookie);
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
  await call('POST', '/contrib', { path: LM, record: edit(LM, (o) => { o.gender = 'femme'; }) }, cookie);
  eq(gh.prs[0].state, 'open');
  ok(!JSON.stringify(gh.graphql).includes('mergePullRequest'), 'the gateway tried to merge');
});
await scenario('Two contributors on the same fiche do not overwrite each other', async () => {
  const { call, gh, signIn, clock } = rig();
  const ada = await signIn('ada@example.org');
  const first = await call('POST', '/contrib', { path: LM, record: edit(LM, (o) => { o.gender = 'femme'; }) }, ada);
  eq(first.status, 201);
  clock.t += 60000;
  const zoe = await signIn('zoe@example.org');
  const r = await call('POST', '/contrib', { path: LM, record: edit(LM, (o) => { o.gender = 'autre'; }) }, zoe);
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
  await call('POST', '/contrib', { path: LM, record: edit(LM, (o) => { o.gender = 'femme'; }) }, cookie);
  eq(gh.tokens, 1);
});
})();

console.log(`\n${scen} scenarios, ${fail} failed.`);
process.exit(fail ? 1 : 0);
