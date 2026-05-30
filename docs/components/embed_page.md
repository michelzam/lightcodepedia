# 🖼️ Embed

Embed another page from this site, an external URL, or a video — using a markdown link and an IAL. Three flavors: `embed-page`, `embed`, and `video`.

**This page is the tutorial.** Click 📽️ at the bottom-left to enter slide mode.

## 👀 Embed another page

`{: .embed-page }` on a paragraph containing a single link embeds that page in an iframe, with `?embed=true` appended automatically (hides the topbar):

```markdown
[🐍 Run component](/components/run)
{: .embed-page height="400" }
```

[🐍 Run component](/components/run)
{: .embed-page height="400" }

> Ask: "What does the embedded page look like vs the normal page?"
> Point out the missing topbar — `?embed=true` strips the chrome.
{: .speaker-note }

**Q:** You embed `/components/quiz`. What does `?embed=true` do?

- [ ] Makes quiz answers visible.
- [x] Hides the topbar so the embedded page looks clean inside the frame.
- [ ] Forces the page into slide mode.
- [ ] Nothing — the site ignores `?embed=true`.
{: .quiz }

## 🌐 Embed an external URL

`{: .embed }` for any external iframe-able URL:

```markdown
[OpenStreetMap](https://www.openstreetmap.org/export/embed.html?bbox=-0.09,51.50,-0.08,51.51)
{: .embed height="350" }
```

## 🎬 Embed a video

`{: .video }` for YouTube links or Google Drive file IDs:

```markdown
[Python in 100 seconds](https://www.youtube.com/watch?v=x7X9w_GIm1s)
{: .video height="360" }
```

```markdown
[Lecture recording](gdrive:1AbCdEfGhIjKlMnOpQrStUvWxYz)
{: .video height="400" }
```

`gdrive:ID` → `https://drive.google.com/file/d/ID/preview` automatically.
YouTube watch URLs → `/embed/VIDEO_ID` automatically.

## 🔧 Knobs

| IAL | `height=` default | Notes |
|---|---|---|
| `{: .embed-page }` | `400` | Appends `?embed=true` to the href |
| `{: .embed }` | `600` | Raw iframe — any external src |
| `{: .video }` | `400` | YouTube + `gdrive:ID` shorthand |

**Q:** You write `[Lecture](gdrive:ABC123){: .video }` as its own paragraph. What URL does the iframe use?

- [ ] `gdrive:ABC123` — passed through literally.
- [x] `https://drive.google.com/file/d/ABC123/preview` — the shorthand is expanded.
- [ ] `https://drive.google.com/open?id=ABC123` — the download link.
- [ ] Nothing renders — `gdrive:` is not a recognised URL scheme.
{: .quiz }

## ⚠️ Limits worth knowing

- **CORS / `X-Frame-Options`.** Many sites block iframe embedding via security headers. If the embed shows blank or an error, the target site is blocking it — not something we can change.
- **One link per paragraph.** The upgrade looks for a single `<a>` inside the `<p>`. Extra text in the same paragraph breaks the upgrade.

{% include backtotop.md %}
