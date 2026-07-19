# 🔬 Runner

The **runner** renders raw markdown into live components in the browser — no
Jekyll build. It reuses the exact pipeline the editor preview uses
(`marked → inline IAL → block IAL → lcScanElement`), so a page runs the same
whether Jekyll built it or the runner rendered it. This is the engine behind
instant benches: a private repo's markdown, fetched and run on the spot.

- **The `/run` page** takes its source from the URL hash: `/run#src=<url>`.
- **Embedded** anywhere with a `src` attribute — the live demo below is one.

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
    self.runner = Object._all(".lc-runner")
    self.blocks = Object._all(".lc-runner .lc-block")
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
