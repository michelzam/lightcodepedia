# Changelog — @karmicsoft/lc-gateway

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
