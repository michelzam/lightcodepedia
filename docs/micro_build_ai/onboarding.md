# 🔑 Get your key — Iteration 1 starts here

Everything in BUILD-AI that feels like magic — asking **Ari** for help, and later
**shipping your own app** — runs on one small thing: a **key** (a *token*) tied to
your own free GitHub account. This is the first urgent need the project hands
you. It takes about a minute, and then the lights come on.

> Why first? Because the key is what makes Ari *live* and what lets you publish
> your own work. We don't front-load theory; we front-load the one dependency
> everything else pulls on.
{: .speaker-note }

## 1️⃣ Get a GitHub account (30 seconds)

If you don't have one yet, create a free account:

[Create a free GitHub account →](https://github.com/signup){: .lc-btn }

That's the whole step. No payment, no setup.

## 2️⃣ Get a key — staged, just enough

You don't need one big powerful key. You need **the smallest key for what you're
doing right now**, and you upgrade it only when a new need appears. That habit —
*least privilege* — is itself one of the first things a builder learns.

```
### 🤖 Now — a key to ask Ari
**Goal:** chat with Ari on this site. Nothing else.
**Key:** a classic token with **zero scopes** — safe to create in seconds.

1. Go to [github.com/settings/tokens](https://github.com/settings/tokens)
2. Click **Generate new token (classic)**.
3. Give it a name. **Leave every checkbox unchecked.**
4. Click **Generate** → copy the token (starts with `ghp_…`).

Paste it into any 🤖 Ari panel and you're talking. A blank-scope key can read
GitHub Models and **nothing else** — the safest thing you can hand a browser.

### 🚀 Later — a key to ship your fork
**Goal:** edit and publish your *own* copy of a page (Iteration 1's "make it
exist" payoff, and every iteration after).
**Key:** a classic token with the **`repo`** scope.

You'll do this *when you first need to ship* — not now. When that need arrives:

1. Generate a new classic token.
2. Check the **`repo`** scope (covers reading and writing your fork).
3. Use it in the ✏️ editor (and it also works for Ari).

We escalate **on demand**, deliberately — a broader key only when a broader need
shows up. That's the same just-in-time rule the whole course runs on.
```
{: .radio }

> Most common stumble: students grab the powerful `repo` key on day one "to be
> safe." It's the opposite of safe. Start blank-scope for Ari; escalate when the
> ship step actually arrives.
{: .speaker-note }

## 🧠 Where does your key go?

Nowhere near us. When you ask Ari, your browser sends the question **straight to
`models.github.ai`** with your key attached. The key travels from *your* browser
to *GitHub* — never to a Lightcodepedia server, because there isn't one. No
shared key, no request log, no storage we control. Your browser may offer to
remember the key in your OS keychain; that's the browser, not us.

**Q:** When you click *Ask* on an Ari panel, who receives your key?

- [ ] A Lightcodepedia server stores it in a cookie.
- [ ] It's baked into the page's JavaScript at build time.
- [x] Only your browser — it goes directly to `models.github.ai`.
- [ ] Whoever's nearest. Keys are gregarious.
{: .quiz }

**Q:** You just want to chat with Ari today. Which key is the right one?

- [x] A classic token with **zero scopes** — least privilege.
- [ ] A classic token with `repo` — "to be safe."
- [ ] A fine-grained token with every permission enabled.
- [ ] No key — the site has a shared one. (It doesn't.)
{: .quiz }

## 🤖 Try it — say hi to Ari

Paste your fresh key in the panel below, then ask Ari anything. The moment it
answers, your key works and Iteration 1 is truly underway.

```yaml
title: Ari
icon: 🐾
system: |
  You are Ari, an Aristotelian pair-lightcoder and guide for the BUILD-AI
  course on Lightcodepedia. You help complete beginners build real, useful
  apps with low-code blocks and AI — no prior coding needed.
  Style: warm, brief, practical, Socratic. Start from the goal and the user's
  situation (behavior before architecture). Prefer one small next step over a
  long explanation. Use plain language; define any term in a few words.
  The learner is teaching a dog named Lucky 🐕 to use AI to build the "Paws
  Support Navigator"; Wanda 🐠 is the friendly skeptic. If asked for code, keep
  it minimal and say what it does. Gently steer off-topic questions back to
  building. Keep answers under ~120 words unless asked for more.
intro: "Welcome! Paste your key above, then ask me how to begin Iteration 1."
placeholder: "How do I start building the Paws Support Navigator?"
```
{: .agent id="ari_onboard" }

> First-run tip: the panel asks for the key once. After **Save & start**, your
> browser offers to remember it in the OS keychain — that's encrypted storage
> the browser owns, not localStorage we control.
{: .speaker-note }

## ⭐ Your karma

Passing the two checks above added **karma**, saved right here in your browser.
It follows you across the whole journey and counts toward your **BUILD-AI
credential** — no sign-up, nothing stored on a server.

## ➡️ Next — make something exist

Key in hand and Ari live, you're ready for the first build. Head into the
catalog and start operating the finished app — *behavior before architecture.*

```
### 🔮 First node
[From the future — use the finished app →](/micro_build_ai/m1-from-the-future)

### 📚 The catalog
[Browse all nodes](/micro_build_ai/catalog)

### 🗺️ The spine
[Back to the journey](/micro_build_ai/)
```
{: .cards cols="3" }
