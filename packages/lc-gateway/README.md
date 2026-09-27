# @karmicsoft/lc-gateway

**E-mail sign-in and pull-request writer for git-backed content.** A LightCode
brick, shipped as a container image. One volunteer, one edit, one branch, one
pull request — without a GitHub account.

The host keeps its own form (built on `lc-record`). The gateway does what the
host's static site cannot: hold the secrets, sign people in by e-mail, and
write to GitHub under a single service identity with the volunteer credited
by name.

## What it does

| Route | Verb | Does |
|---|---|---|
| `/health` | GET | `{ ok, version }` |
| `/auth/request` | POST `{ email }` | mails a magic link through Brevo — same answer whether the address is known or not; rate-limited |
| `/auth/verify?t=` | GET | the mailed link opens a page with one button; it reads nothing and consumes nothing, so a mail scanner that follows it does no harm |
| `/auth/verify` | POST `t` (the button) | the one use of the link, 15 minutes; sets the session cookie (7 days) and redirects to the app |
| `/me` | GET | `{ name, role }` of the signed-in volunteer |
| `/fiche?path=` | GET | `{ path, sha, text, record }` of a record on `main`, for a form whose repository is private; content folders only |
| `/contrib` | POST `{ path, baseSha, record, title?, type?, message? }` | one branch `contrib/<slug>-<yyyymmdd-hhmm>` + one pull request to `main`, the file written through **lc-patch**. `baseSha` is required |
| `/contrib/new` | POST `{ kind, title, record }` | a new record under the folder named by `kind`; `id`/`slug` derived from the title, never editable |

Refusals the host must expect, each with `keep: true` so the form keeps the
edit in the browser:

- `400 baseSha required` — the form must send the sha the record was opened
  with (`GET /fiche` gives it);
- `401` not signed in, session expired, or address removed from the allowlist;
- `403` path outside the content folders;
- `403 protected fields` — the record changes a field the form may never
  touch (`id`, `slug`, `workflow.published`, `validated`, `withdrawnReason`,
  `periods`, `districts`, configurable); the answer names them. Refused for
  every role, so a trusted author's auto-merge cannot carry one either;
- `409 stale` — the record moved on `main` since it was opened: reload it;
- `409 open pull request` — someone's contribution on this fiche is already
  waiting; the answer names it.

Roles: `contributor` → the pull request waits for review. `trusted` → the
gateway enables GitHub **auto-merge**; GitHub merges it only once the
required check (`fiche-check`, enforced by branch protection on `main`) is
green. The gateway itself never merges and never commits to `main`.

Identity: commits are authored by the GitHub App. The message ends with
`Co-authored-by: <Name> <the service address you configure>` — the
volunteer's personal address is never written to git, GitHub, or a log.

## Run

```sh
cd packages && docker build -f lc-gateway/Dockerfile -t lc-gateway .
docker run --env-file gateway.env -p 8080:8080 lc-gateway
```

Every knob is an environment variable; see **DEPLOY.md** for the list, the
GitHub App, Brevo, the OVH and Scaleway recipes, and the live test mode.

## Prove

`npm test` runs the sign-in and write scenarios agreed with a partner — link
once and 15 minutes, a scanner that opens it consumes nothing, no
enumeration, limits per minute, per hour and a daily mail quota, nothing
outliving its window in memory, session expiry, revocation, the fiche read,
one branch and one pull request, name never address, folders only, roles,
open-pull-request, stale, missing-sha and protected-field refusals, creation
— against an in-memory GitHub,
a mailbox and a clock of its own: no network, no secret. The service is a pure
function of an abstract request (`createGateway().request`), which is why it
can be tested that way and why `server.js` is fifteen lines.

The host's side — the form on `lc-record` and the pull-request check the
branch protection requires — is the host's to build.

MIT © 2026 KarmicSoft — [lightcodepedia.org](https://lightcodepedia.org)
