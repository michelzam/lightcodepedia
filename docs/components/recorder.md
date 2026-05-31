# 🎬 Recorder

Record your screen with your face in the corner — one tag, no install, no server. The video downloads straight to your computer when you stop.

**Try it now:**

Record this page.
{: .recorder }

Click **▶ Start recording**, share your screen when the browser asks, then click **⏹ Stop & download**.

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
| Face overlay | Your webcam, circular, in the corner — like a video call |
| Audio | Your microphone (toggle on/off before recording) |
| Screen audio | Optional — toggle on before recording (works best in Chrome) |

All compositing happens in the browser. Nothing is sent anywhere. The file downloads when you click ⏹.

---

## Options

| Attribute | Default | What it does |
|---|---|---|
| `pip="bottom-right"` | `bottom-right` | Face position: `bottom-right`, `bottom-left`, `top-right`, `top-left` |
| `size="180"` | `180` | Diameter of the face circle in pixels |
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
