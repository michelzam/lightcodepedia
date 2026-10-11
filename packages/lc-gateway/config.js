/*!
 * @karmicsoft/lc-gateway — configuration from the environment.
 * © KarmicSoft — LightCode. See LICENSE.
 *
 * The host configures, never edits source: every knob is an environment
 * variable, every secret stays in the host's secret store. See DEPLOY.md.
 */
import { readFileSync } from 'node:fs';
import { createPrivateKey } from 'node:crypto';

/* `docker run --env-file` takes a value literally: the quotes stay, and \n
   is two characters. A value read here is forgiven both — one pair of
   matching surrounding quotes is dropped, and (where a text may span
   lines) a written \n becomes a line break. A value that already carries
   real line breaks (-e, a secret store) passes unchanged. (0.2.1, from
   Toni's report.) */
export function unquote(v) {
  const t = String(v);
  return t.length >= 2 && (t[0] === '"' || t[0] === "'") && t[t.length - 1] === t[0] ? t.slice(1, -1) : t;
}
export const multiline = (v) => unquote(v).replace(/\\n/g, '\n');

/* the App's key: GITHUB_APP_PRIVATE_KEY (one line with \n, quoted or not,
   or real lines) or GITHUB_APP_PRIVATE_KEY_FILE (a mounted PEM — the
   cleanest for Docker). Never both. It must read as a private key, or the
   gateway refuses to start; the message names the variable, never the key. */
function appKey(env) {
  const has = (k) => env[k] != null && env[k] !== '';
  if (has('GITHUB_APP_PRIVATE_KEY') && has('GITHUB_APP_PRIVATE_KEY_FILE'))
    throw new Error('Set GITHUB_APP_PRIVATE_KEY or GITHUB_APP_PRIVATE_KEY_FILE, not both');
  let key = '', from = 'GITHUB_APP_PRIVATE_KEY';
  if (has('GITHUB_APP_PRIVATE_KEY_FILE')) {
    from = 'GITHUB_APP_PRIVATE_KEY_FILE';
    try { key = readFileSync(unquote(env.GITHUB_APP_PRIVATE_KEY_FILE), 'utf8'); }
    catch (e) { throw new Error(from + ': cannot read the file it names'); }
  } else if (has('GITHUB_APP_PRIVATE_KEY')) key = multiline(env.GITHUB_APP_PRIVATE_KEY);
  if (!key) return '';
  try { createPrivateKey(key); }
  catch (e) { throw new Error(from + ' does not read as a private key (PEM) — check the value, its quotes and its line breaks'); }
  return key;
}

export function configFromEnv(env = process.env) {
  const s = (k, d) => (env[k] != null && env[k] !== '' ? env[k] : d);
  const q = (k, d) => { const v = s(k, d); return v === d ? v : unquote(v); };      // quotes forgiven
  const ml = (k, d) => { const v = s(k, d); return v === d ? v : multiline(v); };   // quotes and \n forgiven
  const n = (k, d) => Number(s(k, d));
  const b = (k, d) => /^(1|true|yes|on)$/i.test(String(s(k, d)));
  let allowlist = [];
  try { allowlist = JSON.parse(s('ALLOWLIST', '[]')); } catch (e) { throw new Error('ALLOWLIST must be a JSON array of {email,name,role}'); }
  if (!Array.isArray(allowlist)) throw new Error('ALLOWLIST must be a JSON array');
  return {
    publicUrl: s('PUBLIC_URL', ''),
    appUrl: s('APP_URL', ''),
    port: n('PORT', 8080),
    repo: s('GITHUB_REPO', ''),
    baseBranch: s('BASE_BRANCH', 'main'),
    contentDirs: s('CONTENT_DIRS', '').split(',').map((x) => x.trim()).filter(Boolean),
    appId: s('GITHUB_APP_ID', ''),
    privateKey: appKey(env),
    installationId: s('GITHUB_INSTALLATION_ID', ''),
    token: s('GITHUB_TOKEN', ''),                       // live test mode only — never in production
    brevoApiKey: s('BREVO_API_KEY', ''),
    mailFrom: s('MAIL_FROM', ''),
    mailFromName: s('MAIL_FROM_NAME', 'Contributions'),
    mailSubject: q('MAIL_SUBJECT', 'Your sign-in link'),
    ...(s('MAIL_TEXT', '') ? { mailText: ml('MAIL_TEXT', '') } : {}),
    allowlist,
    sessionSecret: s('SESSION_SECRET', ''),
    linkTtlMin: n('LINK_TTL_MIN', 15),
    sessionTtlDays: n('SESSION_TTL_DAYS', 7),
    rateLimitPerMin: n('RATE_LIMIT_PER_MIN', 5),
    rateLimitPerHour: n('RATE_LIMIT_PER_HOUR', 10),
    mailPerDay: n('MAIL_PER_DAY', 200),
    ...(s('PROTECTED_FIELDS', '') ? { protectedFields: s('PROTECTED_FIELDS', '').split(',').map((x) => x.trim()).filter(Boolean) } : {}),
    ...(s('VERIFY_TITLE', '') ? { verifyTitle: q('VERIFY_TITLE', '') } : {}),
    ...(s('VERIFY_TEXT', '') ? { verifyText: q('VERIFY_TEXT', '') } : {}),
    ...(s('VERIFY_BUTTON', '') ? { verifyButton: q('VERIFY_BUTTON', '') } : {}),
    branchPrefix: s('BRANCH_PREFIX', 'contrib'),
    prTitle: s('PR_TITLE', '{type}: {title} — {name}'),
    coauthorEmail: s('COAUTHOR_EMAIL', ''),
    allowCreate: b('ALLOW_CREATE', 'true'),
    requiredCheck: s('REQUIRED_CHECK', 'fiche-check'),
    mergeMethod: s('MERGE_METHOD', 'SQUASH'),
  };
}
