# 🤖 Agent

An AI chat panel that lives right on the page — no server, no shared API key, no back-end code. Each learner uses their own GitHub PAT[^pat] to call GitHub Models[^gh-models] directly from the browser.

**This page is the tutorial.** Click 📽️ at the bottom-left to enter slide mode, then press → to advance. Live agent panels throughout the page let you chat with the examples as you read.

## 🧠 What actually happens

No magic — just a direct HTTPS call you could paste into `curl`.

- You type a question.
- The widget sends it (plus a system prompt) straight to `models.github.ai`.
- The response comes back as JSON. The widget renders it.
- Your PAT travels from your browser to GitHub's servers — never to ours.

This site has no server-side code, no shared API key, and no request log. Zero.

> Ask yourself: "where does your API key go when you click Ask?" before the demo.
> Five hands always go up. Walk through the answer: browser → GitHub. That's it.
{: .speaker-note }

**Q:** Who holds your PAT while the agent runs?

- [ ] The lightcodepedia server stores it in a session cookie.
- [ ] It's baked into the page's JavaScript bundle at build time.
- [x] Only your browser — it goes directly to `models.github.ai`.
- [ ] The NSA has it. (And all those emojis you've been sending.)
{: .quiz }

## 🔑 Getting your keys

Two badges, two jobs — and they are different keys on purpose:

| Use case | What it calls | The key |
|---|---|---|
| 🤖 **Agent chat** | An AI provider (OpenAI-compatible dialect) | the provider's own key — default **Google AI Studio** (free tier, [aistudio.google.com/apikey](https://aistudio.google.com/apikey)) |
| ✏️ **Page editor** (✏️ FAB) | GitHub Contents API (your repo files) | a GitHub PAT — `repo` (classic) or Contents → Read + Write (fine-grained) |

> **History note (2026-07-30):** the agent used to ride GitHub Models with a
> plain PAT — GitHub retired that service overnight (HTTP 410). The desk
> survived because the provider is *configuration*: `provider:` picks a
> preset (gemini, openrouter), `base_url:` points anywhere that speaks the
> OpenAI-compatible dialect — including a future class gateway. A dead
> provider costs one yaml line, never a course.

```
### 🤖 Agent only — the energy key

1. Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
   (any Google account; the free tier is plenty for a course).
2. *Create API key* → copy it.
3. Paste it into any agent's key form — one key covers every agent of that
   provider on the page, and your browser offers to remember it.

The free quota IS the energy lesson: every question spends a little —
fewer, better questions.

### ✏️ Editor only (fork + edit pages)
You need write access to your own forked repo.

**Route A — Classic PAT with `repo` scope:**

1. Go to [github.com/settings/tokens](https://github.com/settings/tokens)
2. Click *Generate new token (classic)*
3. Give it a name. Check the **`repo`** scope (top-level — covers all sub-scopes).
4. Click Generate → copy.
5. Open **✏️ Edit** from the Modes pill (bottom-left) — or press **⌥E** — then paste the token and your repo name (`owner/repo`).

**Route B — Fine-grained PAT:**

1. Go to [github.com/settings/personal-access-tokens](https://github.com/settings/personal-access-tokens)
2. Create a new token scoped to **your fork only**.
3. Under *Permissions → Repository permissions*, enable **Contents → Read and write**.
4. Click Generate → copy.

> Use your **fork**, not the original repo. The PAT must have push access — the editor
> verifies this on connect and before every save. A read-only PAT will be rejected
> with a clear error message.

### 🤖 + ✏️ Both — two badges, and that's the point
Since GitHub retired its model service, no single key covers both jobs:
the **work badge** (GitHub PAT) stores what you build, the **energy badge**
(provider key) pays the AI's way. They fail differently, they rotate
independently, and neither can leak the other's power — least privilege
by construction.
```
{: .radio }

> Walk learners through the table first — "which row is yours?" —
> then send them to the matching tab. The two-badges framing prevents the
> #1 support question (pasting the GitHub key into the agent).
{: .speaker-note }

**Q:** You want to chat with the Agent AND edit pages in your fork. What do you need?

- [ ] One GitHub PAT with every scope — the master key approach.
- [x] Two keys: a GitHub PAT for the editor, a provider key (e.g. AI Studio)
  for the agent — each does one job.
- [ ] A fine-grained PAT with Models → Read-only. (That service is retired.)
- [ ] No key needed — the site uses a shared server-side key.
{: .quiz }

## 🛠️ Tiniest agent

Drop `{: .agent }` after a fenced YAML block. That's the whole syntax.

````markdown
```yaml
system: You are a Python tutor. Keep answers short.
```
{: .agent }
````

Live demo — paste your PAT and ask it something:

```yaml
system: You are a cheerful Python tutor. Keep answers short and practical.
intro: "Paste your PAT above, then ask me anything about Python."
```
{: .agent #demo_tutor }

```gherkin
Feature: An AI tutor runs right on the page
  As a learner
  I want to chat with an AI about the lesson where I am reading
  So that I learn interactively, using my own key, with no server

  Scenario: The block upgrades into an agent panel
    Given the agent above
    :::python
    self.agent: Object = Object._all(".lc-agent")[0]
    :::
    When the page has upgraded it
    Then it is a visible agent panel
    :::python
    assert self.agent.visible
    :::
```
{: .feature tags="ai,learn" status="passing" }

On first use the panel asks for a PAT. Paste it, click **Save & start**, and your browser offers to remember it in the OS keychain. Next visit the field auto-fills.

> Walk through the PAT entry live — expand the key field, paste,
> click Save & start. Show the browser's "save password?" prompt
> and explain that this is the OS keychain, not localStorage.
{: .speaker-note }

## 🎛️ Knobs to turn

All configuration goes in the YAML block.

| Key | Default | What it does |
|---|---|---|
| `system` | "You are a helpful assistant." | The system prompt — defines the persona |
| `model` | `openai/gpt-4o-mini` | Any model GitHub Models free tier supports |
| `temperature` | `0.7` | 0 = deterministic oracle, 1 = jazz improvisation |
| `max_tokens` | `500` | Caps response length (and API cost) |
| `intro` | (none) | A hint rendered above the input |
| `placeholder` | "Ask anything..." | Placeholder text in the prompt field |

A fully-dressed example:

````markdown
```yaml
system: |
  You are a concise English→French translator.
  Reply with the translation ONLY — no preamble, no explanation.
model: openai/gpt-4o-mini
intro: "Type any English sentence — get French back."
placeholder: "Hello, how are you?"
temperature: 0.3
```
{: .agent #fr }
````

Renders to:

```yaml
system: |
  You are a concise English→French translator.
  Reply with the translation ONLY — no preamble, no explanation.
model: openai/gpt-4o-mini
intro: "Type any English sentence — get French back."
placeholder: "Hello, how are you?"
temperature: 0.3
```
{: .agent #fr }

**Q:** You want the model's output to be as creative and unpredictable as possible. Which `temperature` do you set?

- [ ] `0` — maximum creativity.
- [ ] `0.3` — the bold choice.
- [x] `1.0` — full jazz.
- [ ] `42` — works great, trust the universe.
{: .quiz }

### 🔌 `bound="{=expr}"` — wire the agent to any component

`bound=` has a second grammar, told apart by syntax so the editor binding
above is never touched: give it a **cell expression** and the agent reads
that VALUE at Ask time — no copy-paste, always current.

```markdown
```markdown
(the learner's draft)
```
{: .mdpad #cv1 rows="8" }

```yaml
system: You are the coordinator. End with VERDICT: n/8.
```
{: .agent #desk bound="{=cv1.source}" }
```

The header says `reads {=cv1.source}`; every Ask hands the model the pad's
current text. Anything the page's [cells](/components/cells) can see works:
a form field (`{=inputs.pitch}`), a pad, a store node.

### 📏 Ask the agent questions — from a `.feature`

Give the agent an `#id` and a page's feature can audit it: `system` reads
the briefing it currently runs under, `model` names the engine, and
`replies` returns **every answer of the sitting** — the visible panel shows
one exchange at a time, but a hidden ledger keeps them all. That's how a
rubric can, say, compare the `VERDICT:` lines two versions of a document
earned, deterministically, out of stochastic text: force the format in the
briefing, then parse it in the proof.

## 🧑‍⚕️ Bots — one persona, many pages

A **bot** is a markdown file in `docs/bots/` — the file's text *is* the
superprompt (readable by anyone, like every LC page), and one small fence
inside it sets the model, the name, and its **knowledge**: a list of course
pages whose own markdown is folded into every answer. `self` means *the page
the learner is on*. One line summons it anywhere:

````markdown
Ask Doc — he knows this page.
{: .agent bot="doc" }
````

Try the live one (it runs on **your** PAT, like every agent):

Ask Doc — he knows this page.
{: .agent bot="doc" #doc_demo }

- The page can still override any knob (`model:`, `temperature:`…) in a fence
  next to `bot=` — the page wins, the bot provides the defaults.
- Improve `docs/bots/doc.md` once and every lesson using `bot="doc"` levels up.
- Knowledge is honest **context-stuffing**, not embeddings: listed pages ride
  along with every question (trimmed to a budget — `knowledge_budget:` chars,
  default 16000 — with a visible "(trimmed)" note). Keep a bot's list to a few
  focused pages.
- On a **runner render** (a course opened through `/run`), `self` means the
  **rendered course file** — plus the `{: .embed }` fragments it composes
  from — never the runner shell. Each rendered module gets its own knowledge,
  fetched from the render's own repo with your key.

## 🐍 Bound to a runner

Add `bound="run-id"` to tie an agent to a Python editor. Every question automatically carries the editor's **current code** and **last output**. The agent can write code straight back into the editor.

````markdown
```python
# fix me — this errors
print('hello'
```
{: .run #buggy rows="4" }

```yaml
system: |
  You are a Python tutor. When asked to fix code, reply with the
  COMPLETE fixed code in a single python fenced block. Keep prose short.
```
{: .agent bound="buggy" #tutor }
````

Renders to:

```python
# fix me — this errors
print('hello'
```
{: .run #buggy rows="4" }

```yaml
system: |
  You are a Python tutor. When asked to fix code, reply with the
  COMPLETE fixed code in a single python fenced block. Keep prose short.
```
{: .agent bound="buggy" #tutor }

**Try it:**

- Hit ▶ Run — it errors.
- Type "fix it" and click ▶ Ask.
- Click **⬇ Apply to #buggy** next to the code block in the response.
- Hit ▶ Run again. Fixed.
- **↺ Revert** appears for ~10 s if you change your mind.

> Killer live demo: after fixing the syntax error, ask "add a loop that prints 1 to 5".
> Apply. Then ask "make it count down instead". Apply again.
> The agent sees the latest editor contents every time — that's the persistent state.
{: .speaker-note }

**What the agent actually receives** (built automatically, you never type this):

````
The learner is editing this Python code in editor #buggy:
```python
<current editor contents>
```
The last run produced this output:
```
<last stdout / stderr>
```
The learner asks:
<your typed question>
````

Code > 4000 chars is truncated. Empty editor and no-run-yet silently drop those sections.

**Q:** You apply the agent's fix to the editor and immediately regret it. What do you do?

- [ ] Close the browser tab. Works every time.
- [x] Click **↺ Revert** — it appears for ~10 seconds after Apply.
- [ ] `git blame` the agent.
- [ ] File a strongly-worded bug report against your own PAT.
{: .quiz }

## 🔐 How your token stays safe

Three layers, nothing exotic.

- **In-memory by default.** The PAT lives in a JS closure. Page reload clears it — nothing persists on disk without your browser asking first.
- **Browser password manager.** The input is a real `type="password"` field inside a real `<form>` with a hidden `<input name="username">`. Browsers recognize this pattern and offer to save the credential to the OS keychain (Apple Keychain / Windows Credential Manager). Next visit: autofill. No JS reads or writes any storage we control.
- **One token for the whole page.** Multiple agent panels share a single PAT. Enter it once; all panels unlock together. The 🔑 button on any panel clears it everywhere at once.

**Never** localStorage. **Never** cookies. **Never** a repo file. **Never** a generated bundle.

> Pause here and ask: "between page loads, where do you think the PAT is stored?"
> The answer — OS keychain, managed entirely by the browser — surprises everyone.
> Follow up: "so who wrote the code that stores it?" The browser vendor, not us.
{: .speaker-note }

**Q:** Which of these are TRUE about how the PAT is stored? (Pick all that apply.)

- [x] In memory only — page reload clears it.
- [x] The browser password manager handles on-disk encryption in the OS keychain.
- [ ] The widget writes it to `localStorage` for convenience.
- [x] All agent panels on the page share the same token.
- [ ] It's base64-encoded and stored in a session cookie.
{: .quiz multi="true" }

## ⚠️ Limits of v1

Know these before you build a 300-slide AI curriculum on top of it.

- **Stateless single-shot.** Each ▶ Ask is one independent request. No memory across questions — unless `bound=` is set, in which case the editor content IS the persistent state.
- **No streaming.** The full response arrives at once. Long answers feel slow.
- **No tool use yet.** The agent can write code back into an editor but can't run it itself. v2 plan: after Apply, auto-run the result and feed stdout into the next turn.
- **Free-tier rate limits.** GitHub Models caps requests per minute and per day. The panel surfaces the API error if you hit the ceiling.
- **First python block only gets Apply.** Multiple code blocks in one response → only the first gets the ⬇ button. Copy/paste the rest.

## 🏁 Final exam — boss level

**Q:** Which of these are TRUE about the agent widget? (Pick all that apply.)

- [x] Each learner uses their own PAT — no key is shared server-side.
- [x] Bound mode attaches the editor's current code to every Ask automatically.
- [ ] Conversation history accumulates across asks in the same session.
- [x] The 🔑 button clears the token for all panels on the page at once.
- [ ] The PAT is encrypted server-side and returned to you as a JWT.
{: .quiz multi="true" }

**Q:** Class starts in 2 minutes and a learner says "I get a 401 error". What's the most likely fix?

- [ ] Refresh the page fourteen times. Persistence pays.
- [ ] Switch to Firefox. Edge is the problem.
- [x] Generate a new classic PAT — the old one is wrong, expired, or has the wrong scope.
- [ ] The GitHub Models API is down. Accept your fate and pivot to flashcards.
{: .quiz }

> 401 = authentication failure. A fresh classic PAT (zero scopes) fixes 95 % of these.
{: .speaker-note }

**Q:** You want the agent to always see what the learner is currently coding. Which IAL attribute do you add to `{: .agent }`?

- [ ] `linked="run-id"`
- [x] `bound="run-id"`
- [ ] `attach="run-id"`
- [ ] `soul="run-id"` — the mystical approach
{: .quiz }

> `bound=` is the magic word. Point it at the runner's `id` and every Ask carries the editor state.
{: .speaker-note }

[^gh-models]: **GitHub Models** is GitHub's hosted inference gateway at `models.github.ai`, offering OpenAI-compatible chat completions for several model families on a free tier.

[^pat]: **PAT** = Personal Access Token, the credential GitHub uses for API authentication. Classic PATs work out of the box; fine-grained PATs need the explicit `models:read` permission checkbox.
