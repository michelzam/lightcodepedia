---
---
# 🌐 LightNode Network

Every circle is a LightNode — a fork of Lightcodepedia hosted by a community member. Drag to rearrange. Click any node to open its card. The network grows every time someone completes the [onboarding](/start).

The live network map.
{: .lightnodes }

## 🚀 Deployment activity

[deploys-data](#)
{: .deploys count="10" }

[Latest runs](#)
{: .datagrid bind="deploys" rows="10" }

## 🧪 UX test results

Every deploy is checked by a [BDD UX suite](https://github.com/michelzam/lightcodepedia/tree/main/tests/features) written in Gherkin (behave + Playwright). Each row below is one `Scenario` from a `.feature` file, with its result from the latest run against the live site.

[ux-results](https://raw.githubusercontent.com/michelzam/lightcodepedia/main/docs/assets/ux-results.json)
{: .dataset id="uxtests" }

[Latest scenarios](#)
{: .datagrid bind="uxtests" rows="25" }

```
### 📋 Full Gherkin report
Every step of every scenario from the latest run, with timings. Also available [in its own tab](/assets/ux-report.html).

[Behave report](/assets/ux-report.html)
{: .embed-page height="700" }
```
{: .accordion }
