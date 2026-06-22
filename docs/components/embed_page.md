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

```gherkin
Feature: A link becomes an embedded page
  As a lowcoder
  I want a page shown inside the current one
  So that I can compose pages without copy-pasting their content

  Scenario: The link is replaced by an iframe of that page
    Given the embed-page above (it embeds /components/run)
    :::python
    self.frame = Object._all("iframe.lc-embed-page")[0]
    :::
    When it has rendered
    Then it is an iframe of the page in embed mode
    :::python
    self.src = self.frame._attr("src") or ""
    assert "/components/run" in self.src, self.src
    assert "embed=true" in self.src, self.src
    :::
```
{: .feature tags="ui" status="passing" }

> Ask yourself: "What does the embedded page look like vs the normal page?"
> Point out the missing topbar — `?embed=true` strips the chrome.
{: .speaker-note }

**Q:** You embed `/components/quiz`. What does `?embed=true` do?

- [ ] Makes quiz answers visible.
- [x] Hides the topbar so the embedded page looks clean inside the frame.
- [ ] Forces the page into slide mode.
- [ ] Nothing — the site ignores `?embed=true`.
{: .quiz }

## 🗺️ Embed a local module

`{: .embed }` on a local path fetches the HTML fragment and inlines it — no iframe.
This embeds `_dog.md` (a small reusable module defined once, used anywhere):

```markdown
[Lucky](/_dog)
{: .embed }
```

[Lucky](/_dog)
{: .embed }

The map below comes from the same `{: .map }` component used in Tutorial 101 — Paris parks for walking your dog:

````
```json
[
  { "lat": 48.8620, "lon": 2.2474, "label": "🌳 Bois de Boulogne" },
  { "lat": 48.8797, "lon": 2.3832, "label": "🌳 Buttes-Chaumont" },
  { "lat": 48.8795, "lon": 2.3090, "label": "🌳 Parc Monceau" },
  { "lat": 48.8462, "lon": 2.3372, "label": "🌳 Jardin du Luxembourg" },
  { "lat": 48.8360, "lon": 2.4414, "label": "🌳 Bois de Vincennes" },
  { "lat": 48.8937, "lon": 2.3938, "label": "🌳 Parc de la Villette" }
]
```
{: .map height="350" zoom="12" }
````

```json
[
  { "lat": 48.8620, "lon": 2.2474, "label": "🌳 Bois de Boulogne" },
  { "lat": 48.8797, "lon": 2.3832, "label": "🌳 Buttes-Chaumont" },
  { "lat": 48.8795, "lon": 2.3090, "label": "🌳 Parc Monceau" },
  { "lat": 48.8462, "lon": 2.3372, "label": "🌳 Jardin du Luxembourg" },
  { "lat": 48.8360, "lon": 2.4414, "label": "🌳 Bois de Vincennes" },
  { "lat": 48.8937, "lon": 2.3938, "label": "🌳 Parc de la Villette" }
]
```
{: .map height="350" zoom="12" }

> For external iframe-able URLs (Datawrapper, Flourish, OSM export), `{: .embed }` still works as an iframe when the href starts with `https://`.
{: .speaker-note }

**Q:** An external site returns `X-Frame-Options: DENY`. You try to `.embed` it. What happens?

- [ ] The iframe renders fine — that header only affects other browsers.
- [ ] LightCode rewrites the URL to bypass the restriction.
- [x] The iframe shows blank or an error — the browser respects the header and refuses to load it.
- [ ] The site is embedded but without CSS.
{: .quiz }

## 🎬 Embed a video

`{: .video }` for YouTube links or Google Drive file IDs:

```markdown
[Python in 100 seconds](https://www.youtube.com/watch?v=x7X9w_GIm1s)
{: .video height="360" }
```

[Python in 100 seconds](https://www.youtube.com/watch?v=x7X9w_GIm1s)
{: .video height="360" }

```markdown
[Lecture recording](gdrive:1AbCdEfGhIjKlMnOpQrStUvWxYz)
{: .video height="400" }
```

`gdrive:ID` → `https://drive.google.com/file/d/ID/preview` automatically.
YouTube watch URLs → `/embed/VIDEO_ID` automatically.

## 🔧 Knobs

| IAL | `height=` default | Notes |
|---|---|---|
| `{: .embed-page }` | `400` | Appends `?embed=true` to the href — internal page iframe |
| `{: .embed }` (local path) | — | Fetches and inlines HTML fragment — no iframe |
| `{: .embed }` (https://) | `600` | External iframe — any iframe-able URL |
| `{: .video }` | `400` | YouTube + `gdrive:ID` shorthand |

**Q:** You write the following two lines. What URL does the iframe use?

```markdown
[Lecture](gdrive:ABC123)
{: .video }
```

- [ ] `gdrive:ABC123` — passed through literally.
- [x] `https://drive.google.com/file/d/ABC123/preview` — the shorthand is expanded.
- [ ] `https://drive.google.com/open?id=ABC123` — the download link.
- [ ] Nothing renders — `gdrive:` is not a recognised URL scheme.
{: .quiz }

## ⚠️ Limits worth knowing

- **CORS / `X-Frame-Options`.** Many sites block iframe embedding via security headers. If the embed shows blank or an error, the target site is blocking it — not something we can change.
- **One link per paragraph.** The upgrade looks for a single `<a>` inside the `<p>`. Extra text in the same paragraph breaks the upgrade.
