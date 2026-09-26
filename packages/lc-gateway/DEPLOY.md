# lc-gateway — deploy guide

One image, two hosts: an **OVH VPS** with Docker, or **Scaleway Serverless
Containers** in `fr-par`. EU hosting only. The image holds no secret; the
host's secret store does. The host configures, never edits source.

## 1. Before the first run

### The GitHub App (once)

1. GitHub → Settings → Developer settings → GitHub Apps → **New GitHub App**.
   Name it (`contrib-<your-site>`), any homepage, webhook **off**.
2. Repository permissions: **Contents: read & write**, **Pull requests: read
   & write**, **Metadata: read**. Nothing else.
3. Create, note the **App ID**, generate a **private key** (a `.pem`).
4. **Install** the App on the content repository only.

The App is the single writer. Its commits appear as `<app-name>[bot]`.

### The repository

- Branch protection on `main`: require the status check **`fiche-check`**
  before merging, and require pull requests. Repository settings → General →
  **Allow auto-merge** on. Without both, the `trusted` role degrades to a
  pull request that waits like any other (the gateway logs it).
- The check itself is the host's: a GitHub Actions workflow on the records
  changed by the pull request, in seconds, required by branch protection.

### Brevo

A transactional API key (Brevo → SMTP & API → API keys) and a verified sender
address. The gateway sends plain-text mail through `POST /v3/smtp/email`.

## 2. Configuration (environment)

| Variable | Required | Meaning |
|---|---|---|
| `PUBLIC_URL` | yes | Where this gateway answers, for the links it mails |
| `APP_URL` | yes | Where a signed-in volunteer lands; also the CORS origin |
| `GITHUB_REPO` | yes | `owner/name` |
| `CONTENT_DIRS` | yes | Folders a contribution may write, comma-separated, e.g. `src/content/persons,src/content/events` |
| `GITHUB_APP_ID` | yes | The App ID |
| `GITHUB_APP_PRIVATE_KEY` | yes | The `.pem`, literal newlines or `\n` |
| `GITHUB_INSTALLATION_ID` | no | Resolved from the repo when absent |
| `BREVO_API_KEY` | yes | Transactional key |
| `MAIL_FROM` | yes | Verified sender address |
| `MAIL_FROM_NAME`, `MAIL_SUBJECT`, `MAIL_TEXT` | no | Sender name, subject, plain-text body (`{name}`, `{minutes}`, `{link}`) |
| `ALLOWLIST` | yes | JSON: `[{"email":"…","name":"…","role":"contributor"}, …]`; roles `contributor` or `trusted`. Store it as a secret, never in the repo |
| `SESSION_SECRET` | yes | 32+ random bytes; rotating it signs everyone out |
| `BASE_BRANCH` | no | `main` |
| `BRANCH_PREFIX` | no | `contrib` |
| `PR_TITLE` | no | `{type}: {title} — {name}` |
| `COAUTHOR_EMAIL` | yes | The service address every volunteer is credited with; never a personal one |
| `LINK_TTL_MIN` | no | 15 |
| `SESSION_TTL_DAYS` | no | 7 |
| `RATE_LIMIT_PER_MIN` | no | 5 sign-in requests per address per minute |
| `ALLOW_CREATE` | no | `true` — volunteers may create records in the content folders |
| `REQUIRED_CHECK` | no | `fiche-check` (documentation; GitHub enforces it) |
| `MERGE_METHOD` | no | `SQUASH`, `MERGE` or `REBASE` for auto-merge |
| `PORT` | no | 8080 |

Everything in this table is a value, not code.

## 3. OVH VPS (Docker)

```sh
# on the VPS, once
sudo apt-get install -y docker.io
# build from the bricks workspace (or pull the image you pushed to a registry)
cd packages && docker build -f lc-gateway/Dockerfile -t lc-gateway .
# secrets in a root-only file, never in the shell history
sudo install -m 600 /dev/null /etc/lc-gateway.env && sudo nano /etc/lc-gateway.env
docker run -d --name lc-gateway --restart unless-stopped \
  --env-file /etc/lc-gateway.env -p 127.0.0.1:8080:8080 lc-gateway
```

Put it behind the VPS's reverse proxy with TLS (Caddy: `contrib.example.org {
reverse_proxy 127.0.0.1:8080 }`). `PUBLIC_URL` is that HTTPS address.
Sessions and sign-in links live in memory: one container, and a restart
signs everyone out (they ask for a new link). Fine for a pilot.

## 4. Scaleway Serverless Containers (fr-par)

```sh
scw registry namespace create name=lc region=fr-par
docker tag lc-gateway rg.fr-par.scw.cloud/lc/lc-gateway:0.1.0
docker push rg.fr-par.scw.cloud/lc/lc-gateway:0.1.0
scw container namespace create name=contrib region=fr-par
scw container container create namespace-id=<ns> name=lc-gateway \
  registry-image=rg.fr-par.scw.cloud/lc/lc-gateway:0.1.0 port=8080 \
  min-scale=1 max-scale=1 memory-limit=256 \
  environment-variables.PUBLIC_URL=https://… environment-variables.APP_URL=https://… \
  secret-environment-variables.GITHUB_APP_PRIVATE_KEY="$(cat app.pem)" \
  secret-environment-variables.ALLOWLIST="$(cat allowlist.json)" …
scw container container deploy <id>
```

`min-scale=1` and `max-scale=1`: the pilot keeps sessions in memory, so one
instance, always warm. Secrets go through `secret-environment-variables`,
never plain ones. The console offers the same fields under Containers →
Settings → Environment variables / Secrets.

## 5. Check it runs

```sh
curl https://contrib.example.org/health          # {"ok":true,"version":"0.1.0"}
curl -X POST https://contrib.example.org/auth/request -H 'content-type: application/json' \
     -d '{"email":"you@example.org"}'             # 202, and a mail if you are allowlisted
```

## 6. Live test mode (optional, off by default)

The package suite runs offline. To run the write scenarios against a real,
**throwaway** repository seeded with a few records:

```sh
GITHUB_REPO=you/throwaway GITHUB_TOKEN=ghp_… CONTENT_DIRS=content/persons,content/events \
PUBLIC_URL=http://localhost SESSION_SECRET=x COAUTHOR_EMAIL=contrib@example.org ALLOWLIST='[{"email":"you@example.org","name":"You","role":"contributor"}]' \
node server.js
```

then drive `/auth/request` with `sendMail` replaced by reading the link from
the log, or call `/contrib` with a session you mint in Node. `GITHUB_TOKEN`
is accepted for this mode only; production always uses the App.

## 7. What is not in 0.1.0

- Persistent sessions across restarts or instances (a store would come with
  a second instance).
- A web UI: the form is the host's, built on lc-record.
- Any write outside `CONTENT_DIRS`, any commit to `BASE_BRANCH`, any merge by
  the gateway itself. These are refusals by design, not gaps.
