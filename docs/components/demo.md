# 🎬 Demo

Record a **demonstration** — the learner shows *how to use* or *how to build*
something, and `.demo` logs what they actually did (actions, answers, edits,
timings) into one exportable file with a checksum. It's the **black box** to the
[🎥 recorder](/components/recorder)'s camera: one you *watch*, one you *grade*.

**This page is the tutorial** — and a live test. Try it right here.

## 👀 Try it now

Type your name → **Start** → then **answer the quiz** and **change the form**
below → **Finish** and **Export**. The summary will show your actions, quiz
score, and karma; Export hands you the JSON.

Demonstrate: use the widgets below
{: .demo #try_demo title="Demo the widgets" }

**Q:** Which one records the *log* (not the video)?

- [x] `.demo` — the black box
- [ ] `.recorder` — the camera
- [ ] `.quiz`
{: .quiz }

```yaml
name: Lucky
mood: happy
treats: 3
```
{: .form #demo_form editable="true" }

> After **Finish**, you'll see `actions · active time · pauses · quiz · karma`,
> an optional YouTube-link box, and **📤 Export** / **📋 Copy JSON**. The file
> carries a **sha-256** so casual edits show.
{: .speaker-note }

## 🛠️ How to make one

Drop one line on any page; it records interactions on **that page** while active:

````markdown
Demonstrate: build a form
{: .demo #build_a_form title="Build a form" }
````

Start prompts for a **name** (and optional student ID) — there are no accounts,
so that's how the export is attributable.

## 🔧 Knobs

| Attribute | What it does |
|---|---|
| `#id` | Names this demo (used in the export filename + storage key) |
| `title="…"` | Shown on the recorder bar and stamped into the export |

## 🎥 Optional video

If the [recorder](/components/recorder) is on the page, a **🎥 Record video**
button appears — it opens the screen+face recorder (→ YouTube, unlisted). Paste
the resulting link into the box before Export and it's folded into the file.
The **log** works everywhere (including an embedded iframe); the **video** needs
screen-capture permission, so it's optional per demo.

## ⚠️ Good to know

- **Privacy-clean:** it logs *learning actions* — not keystrokes, not your screen.
- **Not proctoring:** the log is client-side, so the sha-256 is a **checksum**
  (detects casual edits), not tamper-proof evidence. Fine for demonstrating work.
- **Export, not upload:** you download/copy the file and hand it in wherever you
  submit — no platform lock-in.

## 🔗 Related

```
/components/recorder
/components/quiz
/components/form
```
{: .related }
