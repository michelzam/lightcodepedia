# 🎬 Recorder

Record your screen with your face in the corner — no install, no server. Launch it from the **🎬 top-bar button** on any page, or drop a tag inline. When you stop, you review the clip and save it straight to your computer.

**Try it now:**

Record this page.
{: .recorder }

Click **🎬 Set up recording**, share your screen when the browser asks, then press **▶ Start** on the floating panel when you're ready. **⏸ Pause** any time, then **⏹ Stop** to review and save.

---

## Launch from anywhere

You don't need a tag on the page to record. The **🎬 button in the top bar** opens the recorder on any page, in any sign-in state:

- **Signed out** — the **Get started ▾** menu also has a **🎬 Record** entry.
- **Signed in** — your avatar menu has a **🎬 Record screen** row.

The in-page `{: .recorder }` tag below is just a second way to drop a launcher exactly where you want it in your content.

> On **desktop**, recording covers a single page — navigating away reloads the page and ends the recording. On **iPhone** the recording is owned by iOS and spans pages.

---

## How to add one

Write any paragraph and add `{: .recorder }` on the next line:

```markdown
Record this demo.
{: .recorder }
```

That's it. The paragraph text is replaced by the recorder widget.

---

## What it records

| Layer | What you see |
|---|---|
| Background | Your entire screen (or a window — you choose when the browser asks) |
| Face overlay | Your webcam, in a floating circle you can drag anywhere — like a video call. It stays visible while you record so you stay connected to your audience. |
| Background | Optional virtual background for your face — tap **🖼 BG** to cycle Off → Blur → Dark → Blue → Green → White, just like Zoom or Teams. |
| Audio | Your microphone (toggle on/off before recording) |
| Screen audio | The sound playing in the page/tab (a demo video, etc.). Toggle **🔊 Screen audio** on, and tick **"Share tab audio"** in Chrome's share dialog. If your mic is also on, the two are **mixed** into the recording. |

In **Chrome/Edge/Firefox** the screen is captured at your display's **native resolution** (crisp). In **Safari** it's capped at **1080p**, because Safari's recorder is unstable at higher resolutions and crashes mid-recording. Nothing is sent anywhere; everything stays in your browser.

## Start when you're ready, pause, then review

- **It starts armed, not rolling.** After you share your screen, the floating panel shows **▶ Start** with the timer at `Ready`. Your screen is already being captured (so macOS already offers Presenter Overlay) — but nothing is encoded yet. Set up your overlay/notes, then press **▶ Start** to actually begin. (**⏹ Cancel** throws it away before you start.)
- **⏸ Pause / ▶ Resume** — pause and resume any time; the timer freezes while paused.
- **⏹ Stop** opens a **review panel** that plays your recording back. From there: **⬇ Save**, **↻ Re-record**, or **🗑 Discard**.

Nothing is written to disk until you press **Save**.

> **On a Mac, your face comes from macOS itself.** While recording, open the green 🟢 screen-sharing icon in the menu bar and turn on **Presenter Overlay → Small**. macOS composites your camera into the recording in higher quality than any in-page overlay — so on Mac we deliberately *don't* open our own camera (running two camera feeds at once destabilises Safari and was crashing recordings). On Windows/Linux, our own draggable face circle (with optional virtual backgrounds) is used instead.

---

## Your face: which browser?

How your face is shown depends on the browser, because of how each one talks to macOS:

| Browser | Your face | Recording length |
|---|---|---|
| **Safari (Mac)** | macOS **Presenter Overlay** (the polished native bubble) — turn it on from the green 🟢 menu-bar icon | ⚠️ Safari can drop the capture after ~20–40s |
| **Chrome / Edge (Mac)** | **Our own** draggable face circle + virtual backgrounds | Stable / long |
| **Windows / Linux** | **Our own** draggable face circle + virtual backgrounds | Stable / long |

**Rule of thumb:** want the fancy native overlay → **Safari**, but keep clips short. Want a long, reliable recording with your face → **Chrome** (uses our own circle). Native Presenter Overlay is **not** available in Chrome — that's a macOS restriction, not a bug.

---

## Options

| Attribute | Default | What it does |
|---|---|---|
| `pip="bottom-right"` | `bottom-right` | Face position: `bottom-right`, `bottom-left`, `top-right`, `top-left` |
| `size="240"` | `240` | Diameter of the face circle in pixels |
| `zoom="1.35"` | `1.35` | How far to zoom into your face inside the circle (1 = no zoom) |
| `fps="25"` | `25` | Frames per second |

Example with options:

```markdown
Record with face top-left.
{: .recorder pip="top-left" size="140" }
```

---

## Two recorders on one page

```markdown
Screen only view.
{: .recorder pip="bottom-right" size="200" }

Presenter view.
{: .recorder pip="top-right" size="120" fps="30" }
```

---

## Output format

| Browser | Format |
|---|---|
| Chrome / Edge | `.webm` (VP9) |
| Firefox | `.webm` |
| Safari | `.mp4` |

The file is named `recording-YYYY-MM-DD-HH-MM-SS.webm` (or `.mp4` on Safari).

---

## ⚠️ Things to know

- **Requires a modern browser** — Chrome, Edge, Firefox or Safari 14.1+.
- **Screen share prompt** — the browser always asks which screen or window to share. You choose; we never see it.
- **Camera is optional** — untick 📷 Camera before recording if you don't want the face overlay.
- **Long recordings** — the whole video is held in memory until you stop. For recordings over ~30 minutes, use a dedicated tool like OBS.
- **No upload, no server** — the file is written directly to your downloads folder.
- **Desktop recording is single-page** — the recording stops if you navigate to another page, because the browser reloads everything. Record one page per video on desktop.
- **iPhone recording spans pages** — on iOS the recorder shows your floating face cam and you start *native* screen recording from Control Centre. Because iOS owns the capture, it keeps going as you move across pages. Long-press the ⏺ button to enable the microphone.
