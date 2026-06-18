# Lightcodepedia

**An open, Markdown-authored platform for interactive, testable learning activities that run entirely in the browser.**

Write plain Markdown, tag a block with a kramdown IAL — `{: .datagrid }`, `{: .chart }`, `{: .run }`, `{: .quiz }` — and the browser engine upgrades it into a live, interactive component at runtime. No build step, no server: it's a static **GitHub Pages + Jekyll** site.

🔗 **Live:** <https://lightcodepedia.org> · **Component gallery:** <https://lightcodepedia.org/components>

## How it works

A page is a `.md` file. Components are activated by an IAL line right after a block:

    ```csv
    breed,weight,cuteness
    Beagle,12,8
    Corgi,11,10
    ```
    {: .dataset #dogs }

    [Cuteness by breed](#)
    {: .chart bind="dogs" type="bar" x="breed" y="cuteness" }

On load the runtime scans the DOM, finds the tagged blocks, and renders a live chart bound to the dataset — purely client-side. Authors write **Markdown only**; the engine owns all rendering.

## What's in the box

- **Data & viz** — `dataset`, `datagrid` (AG Grid), `chart`, `query` (in-browser SQL via AlaSQL)
- **Code & compute** — `run` / `repl` (Python in the browser via MicroPython), `mdpad` (live Markdown)
- **Learning** — `quiz`, `feature` (executable Gherkin), per-page score memory, homework submission
- **Media & layout** — `avatar`, `map`, `mermaid`, `graphviz`, `carousel`, `tabs`, `accordion`, `cards`, …
- **Authoring & inspection** — in-page editor (blocks · raw · AI-assisted), **X-ray** live object inspector, **reel** (Instagram-style) reading mode

Full catalogue: [`/components`](https://lightcodepedia.org/components).

## Architecture

- **`docs/`** is the entire product: the Jekyll site **and** the runtime. Each component is a self-registering upgrader in `docs/_includes/*.md` (`window.lcRegisterUpgrader(selector, fn)`).
- **Single source of truth:** `docs/_includes/steps_runtime.md` declares the component model (`@component` classes); `tools/gen_component_diagram.py` generates `docs/assets/component-model.json` and the model docs. The X-ray inspector and the editor read that model.
- **Continuous-delivery loop:** every push to `main` rebuilds Pages, runs a **behave + Playwright** UX suite against the *live* site, and commits the results back to `docs/assets/ux-results.json`. Behaviour is specified as Gherkin `.feature` files in `tests/` — scenarios are the executable acceptance criteria.

## Develop & test

```bash
pip install -r tests/requirements.txt
playwright install chromium
BASE_URL=https://lightcodepedia.org behave tests/features/
```

## License

© KarmicSoft. Released under the **LightCode Platform License** (community / educational / partnership use) — see [`LICENSE.md`](LICENSE.md). Developed in part under the Erasmus+ programme.

---

> The Python / Streamlit code at the repository root is **legacy and unmaintained**; the live product is entirely in `docs/`.
