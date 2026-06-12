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
{: .datagrid bind="page_vitals" rows="8" }

And a structural check: every binding declared on this page — `bind=`, `bound-to=`, avatar targets and `at:` walks — must resolve to something real. The same check gates CI on the example pages.

Model integrity.
{: .modelcheck }

### 📡 Fleet metrics — every page, every deploy
The live card above measures only the page you're on; pages here are independent documents. So the **CI suite does the rounds**: on every deploy it visits each page and records heap, DOM size, components, transfer, LCP and console errors — identical conditions, every run. Newest run on top.

[metrics]({{ '/assets/metrics.json' | relative_url }})
{: .dataset #fleet_metrics }

[Per page](#)
{: .datagrid bind="fleet_metrics" rows="15" }

[trend]({{ '/assets/metrics_trend.json' | relative_url }})
{: .dataset #fleet_trend }

[Heaviest page per run](#)
{: .chart bind="fleet_trend" type="line" x="run" y="heap_max_mb" title="Max page heap (MB) per run" }

### 🌐 Network map
Drag to rearrange. Click any node to open its card.

The live network map.
{: .lightnodes }

### 🚀 Deployment activity

[deploys-data](#)
{: .deploys count="10" }

[Latest runs](#)
{: .datagrid bind="deploys" rows="10" }

### 🧪 UX test results
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
