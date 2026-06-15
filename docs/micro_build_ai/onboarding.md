# 🔑 Rescue Lucky — and get the key that lets you

Open Lucky's record in the Navigator and you'll see it still reads
**"stray · unclaimed."** It's wrong. He *was* rescued — by you, last chapter. But
when you reach for **Save**, it's locked. 🔒

You can *look* at Lucky's world, but you can't *change* it yet. To actually
rescue him — to fix that record and make it stick — you need to be able to
**save changes**. And to save changes, you need your own free account and a
**key**. That's the whole reason this chapter exists: not paperwork — *the thing
that unlocks Save so you can finish the rescue.*

> The need is emotional first, technical second. Students don't set up a key
> because a syllabus says so; they set it up because Lucky's record is wrong and
> they can't stand it. The credential rides in on the story.
{: .speaker-note }

## 1️⃣ Get a GitHub account (30 seconds)

Your account is your **identity**[^identity] — the name the save is signed with.
Free, no payment, no setup:

[Create a free GitHub account →](https://github.com/signup){: .lc-btn }

## 2️⃣ Get a key — only as much as the moment needs

You don't grab one all-powerful key. You take **the smallest key for what you're
doing right now**, and you upgrade only when the story asks for more. That habit
has a name — *least privilege*[^least-privilege] — and it's the first real
security instinct a builder learns.

```
### 🐾 Now — a key to *plan* the rescue
**Goal:** ask Ari for help thinking it through. Read-only — it can't change a thing.
**Key:** a classic token[^pat] with **zero scopes**[^scope] — the safest thing
you can hand a browser.

1. Go to [github.com/settings/tokens](https://github.com/settings/tokens)
2. Click **Generate new token (classic)**.
3. Name it. **Leave every checkbox unchecked.**
4. **Generate** → copy the token (`ghp_…`).

Paste it into any 🤖 Ari panel and you can talk through Lucky's rescue. A
blank-scope key reads GitHub Models and **nothing else** — it could never
overwrite his record by accident.

### 💾 To actually *save* Lucky
**Goal:** fix the record in your own copy and make it stick.
**Key:** a classic token with the **`repo`** scope — the one that can write.

You'll do this *the moment you save* — not a second before:

1. Generate a new classic token.
2. Check the **`repo`** scope (read **and** write to your fork[^fork]).
3. Use it in the ✏️ editor — now **Save** unlocks, and Lucky's record changes.

A key that can *write* is a bigger responsibility, so it arrives only when a
bigger need does. That's least privilege, lived.
```
{: .radio }

> The two tabs are the lesson: a read-only key to *think*, a write key to *act* —
> and the write key shows up exactly when the story needs it, never earlier.
{: .speaker-note }

## 🧠 Where does your key go?

Nowhere near us. When you ask Ari or hit Save, your browser talks **straight to
GitHub** with your key attached. It travels from *your* browser to *GitHub* —
never to a Lightcodepedia server, because there isn't one. No shared key, no
log, no storage we control. Your browser may offer to remember it in your OS
keychain; that's the browser, not us.

**Q:** Lucky's record won't save — the button is locked. Which key fixes that?

- [ ] A classic token with **zero scopes**.
- [x] A classic token with **`repo`** scope — the one allowed to write.
- [ ] No key — Save is broken site-wide. (It isn't.)
- [ ] Any key at all; scopes are decoration. (They're not.)
{: .quiz }

**Q:** You only want to *ask Ari* about the rescue right now. Safest key?

- [x] Zero-scope classic token — read-only, least privilege.
- [ ] A `repo` token, "to be safe." (That's *less* safe.)
- [ ] A fine-grained token with every permission on.
- [ ] A shared site key. (There is none.)
{: .quiz }

## 🤖 Talk the rescue through with Ari

Paste your fresh key and ask Ari how to fix Lucky's record — or anything else.
The moment it answers, your key works and the rescue is underway.

```yaml
title: Ari
icon: 🐾
system: |
  You are Ari, an Aristotelian pair-lightcoder and guide for the BUILD-AI
  course on Lightcodepedia. Right now the learner is setting up their GitHub
  account and key so they can "rescue Lucky" — fix his record and save it.
  Explain accounts, tokens, scopes and least privilege in plain, warm, brief,
  Socratic language, always tied back to the story (read-only to plan, a write
  key to save). Prefer one small next step. Keep answers under ~120 words.
intro: "Paste your key above, then ask me how to unlock Save and fix Lucky's record."
placeholder: "Why can't I save Lucky's record yet?"
```
{: .agent id="ari_onboard" }

## 📖 Chapter decoded — the real words

You just did real security and identity work. The story called it a rescue;
here's what professionals call each piece:

| In the story | What professionals call it |
|---|---|
| "The name your save is signed with" | **Authentication / identity**[^identity] |
| "The key that unlocks Save" | A **Personal Access Token (PAT)** |
| "How much the key is allowed to touch" | Its **scope**[^scope] |
| "Take only as much key as the moment needs" | **Least privilege**[^least-privilege] |
| "Your own copy of the app to change" | A **fork**[^fork] |
| "Read-only to plan, a write key to act" | **Read vs. read-write access** |

## ⭐ Your karma

Passing the checks above added **karma**, saved right here in your browser. It
follows you across the whole story and counts toward your **BUILD-AI
credential** — no sign-up, nothing stored on a server.

## ➡️ Next — go save him

Key in hand and Ari live, you're ready to finish what you started.

```
### 🔮 Back to Lucky
[From the future →](/micro_build_ai/m1-from-the-future)

### 📚 The catalog
[Browse all chapters](/micro_build_ai/catalog)

### 🗺️ The spine
[Back to the journey](/micro_build_ai/)
```
{: .cards cols="3" }

[^identity]: **Authentication / identity** — proving *who* is making a change, so a save can be attributed (and trusted). Your GitHub account is that identity.
[^pat]: **Personal Access Token (PAT)** — a key GitHub issues for API access instead of your password. Classic PATs work out of the box; fine-grained ones spell out each permission.
[^scope]: **Scope** — exactly what a token is allowed to do. Zero scopes can read public models only; the `repo` scope can read and write your repositories.
[^least-privilege]: **Least privilege** — granting only the minimum access a task needs, so a leaked or misused key can do the least possible harm.
[^fork]: **Fork** — your own copy of a repository. You change *your* fork freely without touching the original, and a write-capable key pushes saves to it.