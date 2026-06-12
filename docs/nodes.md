---
---
# 🌐 LightNode Network

Every circle is a LightNode — a fork of Lightcodepedia hosted by a community member. The network grows every time someone completes the [onboarding](/start). Open a section below; the headline numbers stay visible up here even when everything is shut.

```
!📊 Vitals & model check
Live page health, published as a dataset and displayed by the standard grid and chart — the metrics chain is itself an LC component chain (Shift-X-ray it). Sampling is **off by default**: flip the switch on the card. Heap is Chrome/Edge only.

Page vitals collector.
{: .vitals #page_vitals interval="2" }

[Heap over time](#)
{: .chart bind="page_vitals" type="line" x="t" y="heap_mb" title="JS heap (MB)" }

[Samples](#)
{: .datagrid bind="page_vitals" rows="8" hints="t: seconds since the switch was flipped | heap_mb: JS heap in use (Chrome/Edge only) — sawtooth = allocate then garbage-collect, a rising floor = leak | dom_nodes: elements in the DOM — grows here because each sample adds chart points | lc_components: upgraded LC components (model wrap tokens) | listeners: dataset subscriptions (this chart + this grid) | transfer_kb: bytes over the network since load | lcp_ms: Largest Contentful Paint — when the main content became visible | cls: Cumulative Layout Shift — how much the page jumped while loading (0 = rock steady)" }

And a structural check: every binding declared on this page — `bind=`, `bound-to=`, avatar targets and `at:` walks — must resolve to something real. The same check gates CI on the example pages.

Model integrity.
{: .modelcheck }

### !📡 Fleet metrics — every page, every deploy
The live card above measures only the page you're on; pages here are independent documents. So the **CI suite does the rounds**: on every deploy it visits each page and records heap, DOM size, components, transfer, LCP and console errors — identical conditions, every run. Newest run on top.

[fleet stat](#)
{: .stat bind="fleet_trend" format="📡 {pages} pages · max {heap_max_mb} MB" requires="pages" }

[metrics]({{ '/assets/metrics.json' | relative_url }})
{: .dataset #fleet_metrics }

[Per page](#)
{: .datagrid bind="fleet_metrics" rows="15" hints="run: which CI run measured it | page: every page the UX suite visited | heap_mb: JS heap after the page was exercised — compare pages, watch for climbers | dom_nodes: elements in the DOM at the end of the scenario | lc_components: upgraded LC components on the page | transfer_kb: bytes downloaded | lcp_ms: Largest Contentful Paint | console_errors: console errors during the scenario (0 is the only good number)" }

[trend]({{ '/assets/metrics_trend.json' | relative_url }})
{: .dataset #fleet_trend }

[Heaviest page per run](#)
{: .chart bind="fleet_trend" type="line" x="run" y="heap_max_mb" title="Max page heap (MB) per run" }

### !🌐 Network map
Drag to rearrange. Click any node to open its card.

The live network map.
{: .lightnodes }

Most recent forks first — click a row to visit.

[Recent forks](#)
{: .datagrid bind="lightnodes" rows="6" hints="node: who forked | repo: the fork | forked: when it was created | level: forks-of-forks distance from the root | stars: its stargazers" }

### !🚀 Deployment activity

[deploys-data](#)
{: .deploys count="10" }

[deploys stat](#)
{: .stat bind="deploys" pick="first" format="🚀 last: {status} {state} · {when}" }

[Latest runs](#)
{: .datagrid bind="deploys" rows="10" }

### !🧪 UX test results

[ux stat](#)
{: .stat bind="fleet_trend" format="{passed}/{scenarios} scenarios" requires="scenarios" ok-when="passed==scenarios" }

Every deploy is checked by a [BDD UX suite](https://github.com/michelzam/lightcodepedia/tree/main/tests/features) written in Gherkin (behave + Playwright). Each row below is one `Scenario` from a `.feature` file, with its result from the latest run against the live site.


[ux-results]({{ '/assets/ux-results.json' | relative_url }})
{: .dataset #uxtests }

[Latest scenarios](#)
{: .datagrid bind="uxtests" rows="25" }

### 📋 Full Gherkin report
Every step of every scenario from the latest run, with timings. Also available [in its own tab](/assets/ux-report.html).

[Behave report](/assets/ux-report.html)
{: .embed-page height="700" }
```
{: .accordion }
