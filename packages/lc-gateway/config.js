/*!
 * @karmicsoft/lc-gateway — configuration from the environment.
 * © KarmicSoft — LightCode. See LICENSE.
 *
 * The host configures, never edits source: every knob is an environment
 * variable, every secret stays in the host's secret store. See DEPLOY.md.
 */
export function configFromEnv(env = process.env) {
  const s = (k, d) => (env[k] != null && env[k] !== '' ? env[k] : d);
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
    privateKey: s('GITHUB_APP_PRIVATE_KEY', ''),
    installationId: s('GITHUB_INSTALLATION_ID', ''),
    token: s('GITHUB_TOKEN', ''),                       // live test mode only — never in production
    brevoApiKey: s('BREVO_API_KEY', ''),
    mailFrom: s('MAIL_FROM', ''),
    mailFromName: s('MAIL_FROM_NAME', 'Contributions'),
    mailSubject: s('MAIL_SUBJECT', 'Your sign-in link'),
    ...(s('MAIL_TEXT', '') ? { mailText: s('MAIL_TEXT', '') } : {}),
    allowlist,
    sessionSecret: s('SESSION_SECRET', ''),
    linkTtlMin: n('LINK_TTL_MIN', 15),
    sessionTtlDays: n('SESSION_TTL_DAYS', 7),
    rateLimitPerMin: n('RATE_LIMIT_PER_MIN', 5),
    branchPrefix: s('BRANCH_PREFIX', 'contrib'),
    prTitle: s('PR_TITLE', '{type}: {title} — {name}'),
    coauthorEmail: s('COAUTHOR_EMAIL', ''),
    allowCreate: b('ALLOW_CREATE', 'true'),
    requiredCheck: s('REQUIRED_CHECK', 'fiche-check'),
    mergeMethod: s('MERGE_METHOD', 'SQUASH'),
  };
}
