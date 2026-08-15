# 🔬 Runner

The **runner** renders raw markdown into live components in the browser — no
Jekyll build. It reuses the exact pipeline the editor preview uses
(`marked → inline IAL → block IAL → lcScanElement`), so a page runs the same
whether Jekyll built it or the runner rendered it. This is the engine behind
instant benches: a private repo's markdown, fetched and run on the spot.

- **The `/run` page** takes its source from the URL hash: `/run#src=<url>`.
- **Embedded** anywhere with a `src` attribute — the live demo below is one.

**Modes** work on a rendered page like on a built one: after each `/run`
render the deck re-partitions around the rendered sections (one slide per
`##`), so 📽️ **Present** and 📲 **Reel** in the bottom-left pill drive the
rendered course. Embedded runner demos never affect their host page's deck.

**An embedded runner wears a border.** It is another file, injected — and a
reader who cannot see where the page stops and the injected file starts is
back to the blurry mixture the [seam](/components/seam) went after. So an embedded
render sits in a bordered box, and the injected file's own `#` title is
hidden: that title names the file to whoever opens it alone, while inside a
lesson the lesson's heading already said it. The page-level runner *is* the
page, and gets neither.

This is what lets a course keep the app in its own file:

```
## 🐕 The dogs in our care

Double-click any box to change what it says.

[Dogs](#)
{: .runner src="_app_dogs.md" }
```
{: .code }

The lesson keeps its commentary, the app file holds nothing but the app, and
`_app_dogs.md` still runs on its own.

**Images**: a relative `![…](pic.png)` in a rendered page resolves against
the rendered file's folder and is fetched with your key — so pictures in a
private course render like anywhere else. Site-absolute and external image
URLs pass through untouched.

```
[demo](#)
{: .runner src="/run_samples/probe.txt" }
```
{: .code }

## Live

The markdown at `/run_samples/probe.txt` — a heading, bold text, and a `.block`
component — rendered by the runner, not by Jekyll:

[demo](#)
{: .runner src="/run_samples/probe.txt" }

```gherkin
Feature: The runner renders markdown into live components
  As the platform
  I want raw markdown to run client-side with full component parity
  So that private benches need no Jekyll build

  Scenario: The embedded runner mounts and upgrades a component
    Given the runner demo on this page
    :::python
    self.runner: list = Object._all(".lc-runner")
    self.blocks: list = Object._all(".lc-runner .lc-block")
    :::
    When the engine has loaded
    Then the runner mounted and rendered a block card from the source
    :::python
    assert self.runner, "runner did not mount"
    assert self.blocks, "the .block component did not upgrade via the runner"
    assert any("Lucky" in b.text for b in self.blocks), [b.text[:30] for b in self.blocks]
    :::
```
{: .feature #runner_feature tags="learn" status="passing" }
