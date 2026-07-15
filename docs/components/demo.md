# 🎬 Demo

Record a **demonstration** — the learner shows *how to use* or *how to build*
something, and `.demo` logs what they actually did (actions, answers, edits,
timings) into one exportable file with a checksum. It's the **black box** to the
[🎥 recorder](/components/recorder)'s camera: one you *watch*, one you *grade*.

**This page is the tutorial** — and a live test. Try it right here.

## 👀 Try it now

Type your name → **Start** → then **answer the quiz** and **change the form**
below → **Finish**. Then hit **▶ Replay** to watch **Prof. LC walk your exact
path** — spotlighting each widget you touched and narrating what you did — and
**Export** to get the JSON. The summary shows your actions, quiz score, and karma.

Demonstrate: use the widgets below
{: .demo #try_demo title="Demo the widgets" }

**Q:** Which one records the *log* (not the video)?

- [x] `.demo` — the black box
- [ ] `.recorder` — the camera
- [ ] `.quiz`
{: .quiz #demo_quiz }

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

## ▶ Replay — the path, re-performed

After **Finish**, **▶ Replay** hands the trace to the [avatar](/components/avatar)
engine: **Prof. LC** walks from widget to widget in the order you touched them,
spotlights each one, and narrates the action (*"Clicked 'Add breed' → Set age → 3
→ answered the quiz"*). Click Prof. LC to stop.

It turns a raw log into something an **educator can watch** — you see the
*reasoning path*, not just a score: where the learner went, in what order, where
they paused. Because the replay is rebuilt from the **same events the sha-256
signs**, it's a faithful re-enactment, not a separate recording.

- Each action is logged with the **widget it touched** (its `#id` / `data-lc-id`)
  plus the value — so the path is **reproducible**; labels ride on top for reading.
- Replay runs **on this same page** (the widgets have to be present to be
  spotlighted). An educator opens the lesson, and — soon — drops in a learner's
  exported file to replay it. Any code can call `window.lcDemoReplay(trace)`.

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
/components/avatar
/components/recorder
/components/quiz
/components/form
```
{: .related }
