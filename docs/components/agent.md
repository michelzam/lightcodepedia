# 🤖 Agent

A chat panel that calls the GitHub Models[^gh-models] LLM API directly from the browser, with each learner using their own PAT[^pat]. No backend, no server-side code, no shared key.

## Tiniest agent

Drop `{: .agent }` after a YAML config block:

````markdown
```yaml
system: You are a Python tutor. Keep examples short.
```
{: .agent }
````

Renders to:

```yaml
system: You are a Python tutor. Keep examples short.
```
{: .agent id="py-tutor" }

On first use, the panel asks for a PAT. Paste it, click **Save & start**, and your browser offers to remember it (encrypted in the OS keychain). Next visit the field auto-fills.

## With knobs

````markdown
```yaml
system: |
  You are a friendly French translator. Translate the user's English
  text into natural conversational French. Reply with the translation
  ONLY — no explanations, no preamble.
model: openai/gpt-4o-mini
intro: "Type any English sentence — get the French back."
placeholder: "Hello, how are you?"
temperature: 0.3
```
{: .agent id="fr-translator" }
````

Renders to:

```yaml
system: |
  You are a friendly French translator. Translate the user's English
  text into natural conversational French. Reply with the translation
  ONLY — no explanations, no preamble.
model: openai/gpt-4o-mini
intro: "Type any English sentence — get the French back."
placeholder: "Hello, how are you?"
temperature: 0.3
```
{: .agent id="fr-translator" }

## YAML knobs

| Key | Default | Notes |
|---|---|---|
| `system` | "You are a helpful assistant." | The system prompt |
| `model` | `openai/gpt-4o-mini` | Any model the free tier supports |
| `temperature` | `0.7` | 0 = deterministic, 1 = creative |
| `max_tokens` | `500` | Cap response length |
| `intro` | (none) | Friendly hint shown above the input |
| `placeholder` | "Ask anything..." | Prompt input placeholder |

## IAL attributes on `{: .agent ... }`

| Attribute | Notes |
|---|---|
| `id="..."` | Required when more than one agent shares a page |
| `rows="3"` | Prompt input height |

## How the token is kept

- **In memory by default.** Lives in a closure variable. Page reload asks again.
- **Browser password manager.** The input is a `type="password"` field inside a real `<form>` with a hidden `<input name="username">`. Browsers recognize this pattern and offer to save the credential to the OS keychain (Apple Keychain, Windows Credential Manager, etc.). On the next visit, autofill repopulates the field — no JS reads or writes any storage we control.

**Never** localStorage. **Never** cookies. **Never** a repo file. **Never** a generated JavaScript bundle.

The 🔑 button at the top right of the panel lets you swap tokens at any time.

## What gets sent to GitHub

Single OpenAI-compatible chat completion, no history:

```
POST https://models.github.ai/inference/chat/completions
Authorization: Bearer <your PAT>
Content-Type: application/json

{
  "model": "openai/gpt-4o-mini",
  "messages": [
    { "role": "system", "content": "<your system>" },
    { "role": "user",   "content": "<the typed question>" }
  ],
  "temperature": 0.7,
  "max_tokens": 500
}
```

The response is parsed for `choices[0].message.content` and `usage.{prompt,completion,total}_tokens`. The usage counter at the bottom of the panel sums per-session tokens — it does **not** know your global GitHub quota.

## Which PAT to use

Two paths, both work:

- **Classic PAT** — at [github.com/settings/tokens](https://github.com/settings/tokens), click *Generate new token (classic)*. You can leave every scope unchecked. Click Generate, paste into the panel.
- **Fine-grained PAT** — at [github.com/settings/personal-access-tokens](https://github.com/settings/personal-access-tokens), pick *Public Repositories (read-only)* as the resource owner, then under *Repository permissions* enable **Models → Read-only**.

The classic path has zero clicks beyond Generate. The fine-grained path is more explicit about which permission you're granting. Both reach the same endpoint.

## Security caveats — please read

- Any other JavaScript on the page (CDN scripts we load, browser extensions) can read the PAT from the password field while the panel is mounted. For a teaching site this is acceptable, but **don't paste a PAT with broad write scopes** here. A scope-less classic PAT or a `models:read`-only fine-grained PAT is plenty.
- The PAT is sent over HTTPS only, directly to `models.github.ai`. It is **never** logged, sent to any other host, or stored anywhere on disk by this widget.
- If you suspect a token may have leaked (you screenshotted the network panel, pasted it in chat, etc.), revoke it at [github.com/settings/tokens](https://github.com/settings/tokens) and create a new one.

## Limits of v1

- **Stateless single-shot.** Each ▶ Ask is one prompt + one response. No conversation memory — asking a follow-up means re-stating context.
- **No streaming.** The full response arrives at once. Long responses feel slow.
- **No tool use.** The model can't yet call functions or run Python through your runner. v2 plan: when the model returns a tool-call payload, route it to the [🐍 MicroPython runner](/components/run) and feed the result back.
- **Free-tier rate limits.** GitHub Models caps requests per minute / day. The panel shows the API's error if you hit a limit.

[^gh-models]: **GitHub Models** is GitHub's hosted inference gateway at `models.github.ai`, offering OpenAI-compatible chat completions for several model families on a free tier.

[^pat]: **PAT** = Personal Access Token, the credential GitHub uses for API authentication. Classic PATs work out of the box; fine-grained PATs need the explicit `models:read` permission checkbox.

{% include backtotop.md %}
