# Changelog — @karmicsoft/lc-gateway

## 0.3.1 — 2026-10-12

Asked by Toni with 0.3.0: "the new address and the event that points to it,
in the same branch and the same pull request".

- **Several files, one contribution.** `POST /contrib` with `files: [...]` —
  edits (`{ path, baseSha, record }`) and new records (`{ kind, title,
  record }`) together, at most 10. Every file passes the usual checks
  (folders, baseSha, protected fields, a waiting contribution, an existing
  slug) before anything is written; one refusal names the file
  (`file: <index>`) and nothing is written. New records are written first;
  one commit per file, one pull request listing them all. The answer gives
  each file's `{ path, slug, created }`, in the order sent.
- Each file of a bundle then finds its waiting contribution: `GET /fiche`
  on any of them reads the volunteer's version, and a single save joins the
  bundle (0.3.0's behaviour, per file).

## 0.3.0 — 2026-10-12

Asked by Toni (Blue Lion, for Mémoire des lieux) after the first tests on the
real site; his answers: own waiting contribution → join it; someone else's →
409 as before; "mine" by a fingerprint, not a name. Forms written for 0.2 keep
working: the API only gains a field.

- **Coming back to my waiting contribution.** `GET /fiche` returns the
  volunteer's own version from its branch, with `pending: { number, url,
  mine: true }`; `POST /contrib` with that `sha` adds a commit to the same
  branch and answers `200 { updated: true, pr }`. One pull request, up to
  date, for the reviewer. Protected fields are still judged against the
  published record.
- **Someone else's waiting contribution** still answers `409`, and `GET
  /fiche` says so (`pending.mine: false`) so the form can tell the volunteer.
- **Whose is it:** a mark in the pull request's description, a fingerprint
  of the address keyed by `SESSION_SECRET`. The address is never written.
  Pull requests opened before 0.3.0 carry no mark: nobody's, as before.
- **Fixed:** a waiting contribution is matched by its fiche's exact branch
  name — `louise-michel` no longer matches `louise-michel-bis`.

## 0.2.1 — 2026-10-11

Three fixes reported by Toni (Blue Lion, for Mémoire des lieux) after the
pilot replay. Backward compatible: a deployment that works keeps working.

- **The App key survives `docker run --env-file`.** One pair of surrounding
  quotes is dropped and a written `\n` becomes a line break; a key with real
  line breaks passes unchanged. New: `GITHUB_APP_PRIVATE_KEY_FILE`, the path
  of a mounted `.pem`. Setting both refuses to start; so does a key that does
  not read as a private key — the message names the variable, never the key.
- **`MAIL_TEXT` keeps its paragraphs** from an env file (quotes dropped, `\n`
  read). `MAIL_SUBJECT` and `VERIFY_TITLE` / `VERIFY_TEXT` / `VERIFY_BUTTON`
  lose surrounding quotes.
- **DEPLOY.md is right about restarts.** A restart keeps everyone signed in
  (sessions are signed cookies); only sign-in links not yet used are lost.
  One Scaleway instance, for the real reasons: a link is known only to the
  instance that mailed it, and rate limits are counted per instance.

## 0.2.0 — 2026-09-27

Antonio's review: `GET /fiche`, `baseSha` required, protected fields, a
button page for the mailed link, hourly and daily limits, memory sweep,
constant-time signatures.

## 0.1.0 — 2026-09

First delivery: e-mail sign-in, one contribution = one branch and one pull
request, written through lc-patch.
