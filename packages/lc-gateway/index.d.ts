/**
 * @karmicsoft/lc-gateway — e-mail sign-in and pull-request writer for
 * git-backed content. © KarmicSoft — LightCode.
 */

export const GATEWAY_VERSION: string;

export type Role = 'contributor' | 'trusted';

export interface AllowlistEntry { email: string; name: string; role?: Role }

export interface GatewayConfig {
  /** Where this gateway answers, for the links it mails (https://…). */
  publicUrl: string;
  /** Where a signed-in volunteer is sent after the link, and the CORS origin. */
  appUrl?: string;
  /** owner/name of the content repository. */
  repo: string;
  /** The published branch; never written. Default "main". */
  baseBranch?: string;
  /** Folders a contribution may write, one file deep, e.g. ["src/content/persons", "src/content/events"]. */
  contentDirs: string[];
  /** GitHub App credentials; the installation id is resolved from the repo when absent. */
  appId?: string | number;
  privateKey?: string;
  installationId?: string | number;
  /** A plain token instead of the App — live test mode only. */
  token?: string;
  /** Brevo transactional API key and sender. */
  brevoApiKey?: string;
  mailFrom?: string;
  mailFromName?: string;
  mailSubject?: string;
  /** Plain-text mail body; {name}, {minutes} and {link} are replaced. */
  mailText?: string;
  /** Who may sign in. Private configuration: a secret, never a file in the repo. */
  allowlist: AllowlistEntry[];
  /** Signs the session cookie. */
  sessionSecret: string;
  linkTtlMin?: number;        // 15
  sessionTtlDays?: number;    // 7
  rateLimitPerMin?: number;   // 5
  branchPrefix?: string;      // "contrib"
  prTitle?: string;           // "{type}: {title} — {name}"
  /** The service address every volunteer is credited with — required, never a personal one. */
  coauthorEmail: string;
  allowCreate?: boolean;      // true
  requiredCheck?: string;     // "fiche-check" (documentation: GitHub enforces it through branch protection)
  mergeMethod?: 'SQUASH' | 'MERGE' | 'REBASE';
  githubApi?: string;
  brevoApi?: string;
}

export interface GatewayDeps {
  fetch?: typeof fetch;
  now?: () => number;
  random?: (bytes: number) => Uint8Array;
  sendMail?: (mail: { sender: any; to: any[]; subject: string; textContent: string }) => Promise<void>;
  log?: (line: string) => void;
}

export interface AbstractRequest {
  method: string;
  /** Path with query, e.g. "/auth/verify?t=…". */
  path: string;
  headers?: Record<string, string | undefined>;
  /** JSON text, or an already-parsed object. */
  body?: string | object | null;
}

export interface AbstractResponse {
  status: number;
  headers: Record<string, string>;
  body: any;
}

export interface Gateway {
  /** The whole service as a function: routes /health, /auth/request, /auth/verify, /me, /contrib, /contrib/new. */
  request(req: AbstractRequest): Promise<AbstractResponse>;
  config: Required<GatewayConfig>;
  version: string;
  /** Replace the allowlist at run time (removal revokes live sessions). */
  setAllowlist(list: AllowlistEntry[]): void;
}

export function createGateway(config: GatewayConfig, deps?: GatewayDeps): Gateway;

/** Title → id/slug the way the corpus spells them: ASCII, lower case, hyphens. */
export function slugify(title: string): string;
