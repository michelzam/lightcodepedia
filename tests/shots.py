#!/usr/bin/env python3
"""Screenshot real course components — pictures of what a learner actually touched.

NOT via PDF. A PDF re-lays the page out for print, throws away every live
state, and adds a rasterisation step you then have to undo. Playwright shoots
the live DOM after the components have painted, and it can shoot ONE element
(a single grid, a single chart) instead of a whole page.

These stills are the concrete end of the concrete→abstract move: an animation
that pans across a grid the learner used, then lifts it into a diagram, is
telling the truth about their own screen. A drawing of a grid is not.

Rig setup:
    bash tests/local_rig.sh
    mkdir -p /tmp/site_build/docs && cp -r courses /tmp/site_build/docs/

That second line is not optional and not obvious: the runner resolves a
same-origin #src through window.lcHref, which prefixes Jekyll's baseurl
(/docs locally). So a page asked for as /courses/… is fetched from
/docs/courses/… — serve it where the runner looks, or every shot times out
on "Loading…".

Then:
    PW_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome \
    MARKED_JS=$PWD/.libs/marked.min.js JS_YAML=$PWD/.libs/js-yaml.min.js \
    AG_GRID_DIR=$PWD/.libs/ag CHART_JS=$PWD/.libs/chart.umd.min.js \
    python3 tests/shots.py hq/shots
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))

from playwright.sync_api import sync_playwright

# reuse the behave harness's CDN stubs rather than a second copy of them —
# they are already the tested answer to "jsdelivr is blocked in this sandbox"
from environment import (_stub_ag_grid, _stub_js_yaml,  # noqa: E402
                         _stub_marked, _stub_micropython)

BASE = os.environ.get("BASE_URL", "http://127.0.0.1:8899")
EXE = os.environ.get("PW_CHROMIUM_EXECUTABLE")
COURSE = "/courses/micro_build_ai"

# chart.js has no stub in environment.py (no scenario needed one yet), so it
# lives here. Same shape as the others: no-op when the env var is unset.
CHART_JS = os.environ.get("CHART_JS") or None
_CHART_BODY = None
if CHART_JS and os.path.isfile(CHART_JS):
    with open(CHART_JS, "rb") as _f:
        _CHART_BODY = _f.read()


def _stub_chart_js(page):
    if _CHART_BODY is None:
        return
    page.route(
        "https://cdn.jsdelivr.net/npm/chart.js@*/dist/chart.umd.min.js",
        lambda route: route.fulfill(
            status=200, content_type="application/javascript; charset=utf-8",
            body=_CHART_BODY),
    )


# (name, page, CSS selector, what it is) — one entry per picture.
#
# These are the CATALOG pages, not the lesson pages, and that is a deliberate
# retreat: a lesson page renders through the runner in SLIDES mode, where every
# section but the current one carries `hidden`. A hidden chart never paints, so
# Chart.js is never even fetched, so there is nothing to photograph. On top of
# that, The Broken Wire's grid and chart live inside a bench-backed
# {: .embed save="wiring.md" }, which needs a connected bench to resolve at all.
# Both are solvable (walk the slides, or seed a bench) — but the components on
# the catalog pages are the SAME components with the same data, so the pipeline
# can be proven now and the lesson-page shots done properly after.
SHOTS = [
    ("grid_dogs",   "/components/datagrid", '[data-lc-id="dg1"]',   "datagrid"),
    ("grid_edit",   "/components/datagrid", '[data-lc-id="editable_dogs"]', "datagrid"),
    ("chart_bar",   "/components/chart",    ".lc-chart >> nth=0",   "chart"),
    ("chart_line",  "/components/chart",    ".lc-chart >> nth=1",   "chart"),
    ("form_dog",    "/components/form",     '[data-lc-id="frm1"]',  "form"),
    ("dataset_grid", "/components/dataset", '[data-lc-id="monthly_grid"]', "dataset"),
]

# the lens view: one dataset feeding two charts and two grids — the clearest
# picture of wiring in the catalog, and the concrete thing an abstract diagram
# of pipes is an abstraction OF
XRAY_PAGE = "/components/dataset"


def open_page(page, url):
    """Load a page and unfold it far enough to photograph.

    Two things hide components from a camera and both are RIGHT for a reader:
    a {: .prerequisite } list marks later sections .lc-prereq-hidden until the
    pages above are earned, and slide fragments start folded. Dropping those
    classes shoots the page as its AUTHOR sees it — nothing about the
    components changes, only whether they are on screen.
    """
    page.goto(BASE + url, wait_until="domcontentloaded")
    page.wait_for_timeout(1500)
    page.evaluate("""() => document.querySelectorAll(
                       '.lc-prereq-hidden, .lc-slide-fragment')
                       .forEach(e => { e.classList.remove('lc-prereq-hidden');
                                       e.classList.remove('lc-slide-fragment'); })""")
    page.wait_for_timeout(600)


def shoot(page, out_dir, name, url, sel, kind):
    open_page(page, url)
    try:
        page.wait_for_selector(sel, state="visible", timeout=40_000)
    except Exception:
        return {"name": name, "ok": False, "why": f"{sel} never appeared"}
    el = page.locator(sel).first
    el.scroll_into_view_if_needed()
    # a grid lays out over a couple of frames and a chart animates in; there is
    # no event for "painted", so this one wait is honest rather than lazy
    page.wait_for_timeout(3000)
    box = el.bounding_box()
    if not box or box["height"] < 40:
        return {"name": name, "ok": False, "why": f"{sel} has no box"}
    path = os.path.join(out_dir, name + ".png")
    el.screenshot(path=path)
    return {"name": name, "ok": True, "file": path, "page": url, "sel": sel,
            "kind": kind, "w": round(box["width"]), "h": round(box["height"])}


def xray_shot(page, out_dir, url):
    """The lens view: the pipes between dataset, datagrid and chart.

    This is the picture that makes the abstraction visible on a REAL page —
    the wires a learner can only see with the lens on."""
    open_page(page, url)
    page.wait_for_timeout(2500)
    # the same switch the ⚙️ pill throws — no hunting for the pill in the DOM
    turned = page.evaluate(
        "() => { if (window.lcMode && window.lcMode.set) { window.lcMode.set('xray'); return 'lcMode'; }"
        "        document.body.classList.add('lc-xray'); return 'class only'; }")
    page.wait_for_timeout(3500)
    root = page.locator("main.markdown-body, .markdown-body, main").first
    path = os.path.join(out_dir, "xray_pipes.png")
    root.screenshot(path=path)
    return {"name": "xray_pipes", "ok": True, "file": path, "page": url,
            "kind": "xray", "how": turned}


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "hq/shots"
    os.makedirs(out_dir, exist_ok=True)
    results = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=EXE,
                                     args=["--js-flags=--expose-gc"])
        # 2x so a Ken Burns pan can zoom in without the pixels showing
        ctx = browser.new_context(viewport={"width": 1280, "height": 1000},
                                  device_scale_factor=2)
        page = ctx.new_page()
        for stub in (_stub_marked, _stub_micropython, _stub_ag_grid,
                     _stub_js_yaml, _stub_chart_js):
            stub(page)
        for name, url, sel, kind in SHOTS:
            r = shoot(page, out_dir, name, url, sel, kind)
            results.append(r)
            print(("  ok  " if r["ok"] else "  --  ")
                  + f"{r['name']:<12} "
                  + (f"{r['w']}x{r['h']}" if r["ok"] else r["why"]))
        r = xray_shot(page, out_dir, XRAY_PAGE)
        results.append(r)
        print(("  ok  " if r["ok"] else "  --  ") + f"{r['name']:<12} "
              + (r.get("how", "") if r["ok"] else r["why"]))
        browser.close()
    with open(os.path.join(out_dir, "shots.json"), "w") as fh:
        json.dump(results, fh, indent=2)
    got = sum(1 for r in results if r["ok"])
    print(f"\n{got}/{len(results)} shots written to {out_dir}")
    return 0 if got == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
