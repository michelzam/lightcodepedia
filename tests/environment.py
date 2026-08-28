import json
import os
import urllib.request
from datetime import datetime, timezone

from playwright.sync_api import sync_playwright

BASE_URL = os.environ.get("BASE_URL", "https://lightcodepedia.org").rstrip("/")
ASSETS = os.path.join(os.path.dirname(__file__), "..", "docs", "assets")
KEEP_RUNS = 30  # bound the committed history
# LOCAL HARNESS ONLY: pin the chromium binary when the pip playwright build
# and the pre-provisioned browser build differ (e.g. driver wants 1148 but
# /opt/pw-browsers has 1194). No effect in CI where the versions match.
PW_EXECUTABLE = os.environ.get("PW_CHROMIUM_EXECUTABLE") or None
_LAUNCH = dict(headless=True, args=["--js-flags=--expose-gc"])
if PW_EXECUTABLE:
    _LAUNCH["executable_path"] = PW_EXECUTABLE

# LOCAL HARNESS ONLY: the runner (and editor preview) load marked.js from
# https://cdn.jsdelivr.net/npm/marked@9/marked.min.js. In CI that CDN is
# reachable; in this sandbox jsdelivr is blocked (ERR_TUNNEL_CONNECTION_FAILED)
# so the render pipeline never runs. When MARKED_JS points at a local copy of
# marked.min.js, fulfil that one CDN request from disk. No effect when the env
# var is unset (CI), and it only ever intercepts the marked script URL.
MARKED_JS = os.environ.get("MARKED_JS") or None
_MARKED_BODY = None
if MARKED_JS and os.path.isfile(MARKED_JS):
    with open(MARKED_JS, "rb") as _f:
        _MARKED_BODY = _f.read()


def _stub_marked(page):
    if _MARKED_BODY is None:
        return
    page.route(
        "https://cdn.jsdelivr.net/npm/marked@*/marked.min.js",
        lambda route: route.fulfill(
            status=200,
            content_type="application/javascript; charset=utf-8",
            body=_MARKED_BODY,
        ),
    )


# LOCAL HARNESS ONLY: datagrids and forms load AG Grid from
# https://cdn.jsdelivr.net/npm/ag-grid-community@31/… (one script, two
# stylesheets). Same sandbox story as marked. When AG_GRID_DIR points at an
# unpacked copy of the npm package, fulfil those three from disk.
AG_GRID_DIR = os.environ.get("AG_GRID_DIR") or None
if AG_GRID_DIR and not os.path.isfile(
        os.path.join(AG_GRID_DIR, "dist", "ag-grid-community.min.js")):
    AG_GRID_DIR = None


def _stub_ag_grid(page):
    if AG_GRID_DIR is None:
        return

    def serve(rel, ctype):
        with open(os.path.join(AG_GRID_DIR, rel), "rb") as f:
            body = f.read()
        return lambda route: route.fulfill(
            status=200, content_type=ctype, body=body)

    page.route(
        "https://cdn.jsdelivr.net/npm/ag-grid-community@*/dist/ag-grid-community.min.js",
        serve(os.path.join("dist", "ag-grid-community.min.js"),
              "application/javascript; charset=utf-8"),
    )
    page.route(
        "https://cdn.jsdelivr.net/npm/ag-grid-community@*/styles/ag-grid.css",
        serve(os.path.join("styles", "ag-grid.css"), "text/css; charset=utf-8"),
    )
    page.route(
        "https://cdn.jsdelivr.net/npm/ag-grid-community@*/styles/ag-theme-alpine.css",
        serve(os.path.join("styles", "ag-theme-alpine.css"),
              "text/css; charset=utf-8"),
    )


# LOCAL HARNESS ONLY: YAML-format data blocks parse through js-yaml, also
# from jsdelivr. When JS_YAML points at a local js-yaml.min.js, serve it.
JS_YAML = os.environ.get("JS_YAML") or None
_JS_YAML_BODY = None
if JS_YAML and os.path.isfile(JS_YAML):
    with open(JS_YAML, "rb") as _f:
        _JS_YAML_BODY = _f.read()


def _stub_js_yaml(page):
    if _JS_YAML_BODY is None:
        return
    page.route(
        "https://cdn.jsdelivr.net/npm/js-yaml@*/dist/js-yaml.min.js",
        lambda route: route.fulfill(
            status=200,
            content_type="application/javascript; charset=utf-8",
            body=_JS_YAML_BODY,
        ),
    )


# LOCAL HARNESS ONLY: the .feature step runner imports MicroPython from
# https://cdn.jsdelivr.net/npm/@micropython/micropython-webassembly-pyscript@…
# (an ES module that then fetches its sibling .wasm). Same sandbox story as
# marked: blocked here, reachable in CI. When MPY_DIR points at an unpacked
# copy of that npm package, fulfil both requests from disk. No effect unset.
MPY_DIR = os.environ.get("MPY_DIR") or None
if MPY_DIR and not os.path.isfile(os.path.join(MPY_DIR, "micropython.mjs")):
    MPY_DIR = None


def _stub_micropython(page):
    if MPY_DIR is None:
        return

    def serve(name, ctype):
        with open(os.path.join(MPY_DIR, name), "rb") as f:
            body = f.read()
        return lambda route: route.fulfill(
            status=200, content_type=ctype, body=body)

    page.route(
        "https://cdn.jsdelivr.net/npm/@micropython/micropython-webassembly-pyscript@*/micropython.mjs",
        serve("micropython.mjs", "application/javascript; charset=utf-8"),
    )
    page.route(
        "https://cdn.jsdelivr.net/npm/@micropython/micropython-webassembly-pyscript@*/micropython.wasm",
        serve("micropython.wasm", "application/wasm"),
    )


# LOCAL HARNESS ONLY: charts load Chart.js and {: .query } loads alasql, both
# from jsdelivr. Neither had a shim, so every chart-bearing and SQL-bearing
# scenario was red on this rig whatever the engine did — a blind spot sitting
# exactly where the wiring lesson lives. Found on 2026-08-06 while checking
# whether three components.feature failures were a regression: they fail the
# same way on every engine build. Same shape as the shims above.
CHART_JS = os.environ.get("CHART_JS") or None
_CHART_BODY = None
if CHART_JS and os.path.isfile(CHART_JS):
    with open(CHART_JS, "rb") as _f:
        _CHART_BODY = _f.read()

ALASQL_JS = os.environ.get("ALASQL_JS") or None
_ALASQL_BODY = None
if ALASQL_JS and os.path.isfile(ALASQL_JS):
    with open(ALASQL_JS, "rb") as _f:
        _ALASQL_BODY = _f.read()

# LOCAL HARNESS ONLY: prism was added to the rig's lib downloads but never
# wired here — pages that highlight code failed offline on the CDN fetch
# (found 2026-08-25). When PRISM_DIR points at the unpacked components,
# fulfil them from disk.
PRISM_DIR = os.environ.get("PRISM_DIR") or None
_PRISM = {}
if PRISM_DIR:
    for _n in ("prism-core.min.js", "prism-python.min.js"):
        _p = os.path.join(PRISM_DIR, _n)
        if os.path.isfile(_p):
            with open(_p, "rb") as _f:
                _PRISM[_n] = _f.read()


# LOCAL HARNESS ONLY: the build_loop diorama imports Three.js as ES modules
# from https://cdn.jsdelivr.net/npm/three@0.170.0/… (an importmap in the
# layout's <head>). Same sandbox story as marked. When THREE_DIR points at an
# unpacked copy of the npm package, fulfil build/ and examples/jsm/ from disk.
THREE_DIR = os.environ.get("THREE_DIR") or None
if THREE_DIR and not os.path.isfile(
        os.path.join(THREE_DIR, "build", "three.module.js")):
    THREE_DIR = None


def _stub_three(page):
    if THREE_DIR is None:
        return

    def handler(route):
        rel = route.request.url.split("three@", 1)[1].split("/", 1)[1]
        path = os.path.join(THREE_DIR, *rel.split("/"))
        try:
            with open(path, "rb") as f:
                body = f.read()
        except OSError:
            route.fulfill(status=404, body=b"")
            return
        route.fulfill(status=200,
                      content_type="application/javascript; charset=utf-8",
                      body=body)

    page.route("https://cdn.jsdelivr.net/npm/three@*/**", handler)


# LOCAL HARNESS ONLY: the map component loads MapLibre from
# https://cdn.jsdelivr.net/npm/maplibre-gl@4/dist/… (one script, one
# stylesheet). Same sandbox story as marked.
MAPLIBRE_DIR = os.environ.get("MAPLIBRE_DIR") or None
if MAPLIBRE_DIR and not os.path.isfile(
        os.path.join(MAPLIBRE_DIR, "maplibre-gl.js")):
    MAPLIBRE_DIR = None


def _stub_maplibre(page):
    if MAPLIBRE_DIR is None:
        return

    def serve(rel, ctype):
        with open(os.path.join(MAPLIBRE_DIR, rel), "rb") as f:
            body = f.read()
        return lambda route: route.fulfill(
            status=200, content_type=ctype, body=body)

    page.route(
        "https://cdn.jsdelivr.net/npm/maplibre-gl@*/dist/maplibre-gl.js",
        serve("maplibre-gl.js", "application/javascript; charset=utf-8"),
    )
    page.route(
        "https://cdn.jsdelivr.net/npm/maplibre-gl@*/dist/maplibre-gl.css",
        serve("maplibre-gl.css", "text/css; charset=utf-8"),
    )


# LOCAL HARNESS ONLY: mermaid is an ESM bundle that pulls dozens of chunk
# files — packing it like the other shims is not worth it. In this sandbox a
# functional stub (initialize/run as no-ops) keeps "loads without console
# errors" honest about OUR code; CI and pedia load the real CDN bundle.
MERMAID_STUB = os.environ.get("MERMAID_STUB") == "1"


def _stub_mermaid(page):
    if not MERMAID_STUB:
        return
    page.route(
        "https://cdn.jsdelivr.net/npm/mermaid@*/dist/mermaid.esm.min.mjs",
        lambda route: route.fulfill(
            status=200,
            content_type="application/javascript; charset=utf-8",
            body=b"export default {initialize(){}, async run(){}}",
        ),
    )


def _stub_script(page, pattern, body):
    if body is None:
        return
    page.route(pattern, lambda route: route.fulfill(
        status=200, content_type="application/javascript; charset=utf-8",
        body=body))


_pw = None
_browser = None


def before_all(context):
    global _pw, _browser
    _pw = sync_playwright().start()
    # --expose-gc lets the metrics capture force a collection first, so
    # heap_mb measures THIS page, not residue from earlier scenarios in the
    # shared renderer process
    _browser = _pw.chromium.launch(**_LAUNCH)
    context.base_url = BASE_URL
    # fleet metrics: one row per page per run, captured after each scenario
    context.lc_metrics = {}          # path -> metrics row (measured cold, at suite end)
    context.lc_pages = set()         # every site path the scenarios visited
    context.lc_errors = {}           # path -> max console errors in one scenario
    context.lc_status = [0, 0]       # [passed, total]
    context.lc_run = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    context.lc_tokens = []
    try:
        with urllib.request.urlopen(BASE_URL + "/assets/component-model.json", timeout=10) as r:
            context.lc_tokens = [w[0] for w in json.load(r).get("wrap", [])]
    except Exception:
        pass  # counting LC components is best-effort


def after_all(context):
    try:
        _measure_cold(context)
        _write_metrics(context)
    except Exception as e:
        print("metrics write skipped:", e)
    _browser.close()
    _pw.stop()


def before_scenario(context, scenario):
    mobile = "mobile" in scenario.tags
    if mobile:
        context.page = _browser.new_page(
            viewport={"width": 390, "height": 844},
            user_agent=(
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
            ),
            has_touch=True,
            is_mobile=True,
        )
    else:
        context.page = _browser.new_page(viewport={"width": 1280, "height": 800})
    _stub_marked(context.page)  # LOCAL HARNESS ONLY (no-op when MARKED_JS unset)
    _stub_micropython(context.page)  # LOCAL HARNESS ONLY (no-op when MPY_DIR unset)
    _stub_ag_grid(context.page)  # LOCAL HARNESS ONLY (no-op when AG_GRID_DIR unset)
    _stub_js_yaml(context.page)  # LOCAL HARNESS ONLY (no-op when JS_YAML unset)
    _stub_three(context.page)  # LOCAL HARNESS ONLY (no-op when THREE_DIR unset)
    _stub_mermaid(context.page)  # LOCAL HARNESS ONLY (no-op when MERMAID_STUB unset)
    _stub_maplibre(context.page)  # LOCAL HARNESS ONLY (no-op when MAPLIBRE_DIR unset)
    _stub_script(context.page,  # LOCAL HARNESS ONLY (no-op when CHART_JS unset)
                 "https://cdn.jsdelivr.net/npm/chart.js@*/dist/chart.umd.min.js",
                 _CHART_BODY)
    _stub_script(context.page,  # LOCAL HARNESS ONLY (no-op when ALASQL_JS unset)
                 "https://cdn.jsdelivr.net/npm/alasql@*/dist/alasql.min.js",
                 _ALASQL_BODY)
    for _n, _b in _PRISM.items():  # LOCAL HARNESS ONLY (empty when PRISM_DIR unset)
        _stub_script(context.page,
                     "https://cdn.jsdelivr.net/npm/prismjs@*/components/" + _n, _b)
    context.page.set_default_timeout(15_000)
    context.lc_console_errors = 0
    context.page.on(
        "console",
        lambda msg: setattr(
            context, "lc_console_errors",
            context.lc_console_errors + (1 if msg.type == "error" else 0),
        ),
    )


def after_scenario(context, scenario):
    context.lc_status[1] += 1
    if getattr(scenario.status, "name", str(scenario.status)) == "passed":
        context.lc_status[0] += 1
    try:
        url = context.page.url or ""
        if url.startswith(context.base_url):
            path = url[len(context.base_url):].split("#")[0].split("?")[0] or "/"
            context.lc_pages.add(path)
            prev = context.lc_errors.get(path, 0)
            context.lc_errors[path] = max(prev, context.lc_console_errors)
    except Exception:
        pass  # metrics must never fail the suite
    context.page.close()


_CAPTURE_JS = """(tokens) => new Promise((res) => {
  let lcp = null;
  try {
    new PerformanceObserver((l) => {
      const e = l.getEntries();
      if (e.length) lcp = Math.round(e[e.length - 1].startTime);
    }).observe({ type: "largest-contentful-paint", buffered: true });
  } catch (e) {}
  try { if (window.gc) window.gc(); } catch (e) {}
  setTimeout(() => {
    try { if (window.gc) { window.gc(); window.gc(); } } catch (e) {}
    let transfer = 0;
    try {
      performance.getEntriesByType("resource")
        .concat(performance.getEntriesByType("navigation"))
        .forEach((e) => { transfer += e.transferSize || 0; });
    } catch (e) {}
    const mem = performance.memory;
    res({
      heap_mb: mem ? Math.round(mem.usedJSHeapSize / 104857.6) / 10 : null,
      dom_nodes: document.getElementsByTagName("*").length,
      lc_components: (tokens || []).reduce(
        (n, t) => n + document.getElementsByClassName(t).length, 0),
      transfer_kb: Math.round(transfer / 1024),
      lcp_ms: lcp,
    });
  }, 250);
})"""


def _measure_cold(context):
    """Visit every recorded path once, cold, in a fresh browser process —
    per-page heap without residue from the scenario browser's history.
    performance.memory is process-wide, so isolation is the only honest way."""
    if not context.lc_pages:
        return
    browser = _pw.chromium.launch(**_LAUNCH)
    for path in sorted(context.lc_pages):
        try:
            page = browser.new_page(viewport={"width": 1280, "height": 800})
            # Playwright disables site isolation, so cross-origin iframes
            # (YouTube, online IDEs, PDFs) share the renderer and their JS
            # heap would count as the page's. Block their documents: the
            # metric is the weight of OUR page, not its guests.
            page.route(
                "**/*",
                lambda route, req: route.abort()
                if req.resource_type == "document"
                and not req.url.startswith(context.base_url)
                else route.continue_(),
            )
            page.goto(context.base_url + path, wait_until="load", timeout=30_000)
            page.wait_for_timeout(1500)  # upgrades settle
            row = page.evaluate(_CAPTURE_JS, context.lc_tokens)
            row["page"] = path
            row["console_errors"] = context.lc_errors.get(path, 0)
            row["run"] = context.lc_run
            context.lc_metrics[path] = row
            page.close()
        except Exception:
            try:
                page.close()
            except Exception:
                pass
    browser.close()


def _read_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return []


def _cap_runs(rows):
    runs = sorted({r.get("run", "") for r in rows}, reverse=True)[:KEEP_RUNS]
    return [r for r in rows if r.get("run", "") in runs]


def _write_metrics(context):
    if not context.lc_metrics:
        return
    run = context.lc_run
    cols = ["run", "page", "heap_mb", "dom_nodes", "lc_components",
            "transfer_kb", "lcp_ms", "console_errors"]
    new_rows = [
        {c: r.get(c) for c in cols}
        for r in sorted(context.lc_metrics.values(), key=lambda r: r["page"])
    ]

    mpath = os.path.join(ASSETS, "metrics.json")
    old = [r for r in _read_json(mpath)
           if r.get("run") not in (run, "(awaiting first CI run)")]
    rows = _cap_runs(new_rows + old)  # newest run first → grid top
    with open(mpath, "w") as f:
        json.dump(rows, f, indent=1)

    heaps = [r["heap_mb"] for r in new_rows if r.get("heap_mb") is not None]
    trend_row = {
        "run": run,
        "pages": len(new_rows),
        "heap_max_mb": max(heaps) if heaps else None,
        "heap_avg_mb": round(sum(heaps) / len(heaps), 1) if heaps else None,
        "dom_max": max(r["dom_nodes"] for r in new_rows),
        "errors": sum(r["console_errors"] for r in new_rows),
        "passed": context.lc_status[0],
        "scenarios": context.lc_status[1],
    }
    tpath = os.path.join(ASSETS, "metrics_trend.json")
    told = [r for r in _read_json(tpath)
            if r.get("run") not in (run, "(awaiting first CI run)")]
    trows = _cap_runs(told + [trend_row])
    trows.sort(key=lambda r: r.get("run", ""))  # chronological → trend chart
    with open(tpath, "w") as f:
        json.dump(trows, f, indent=1)
    print(f"fleet metrics: {len(new_rows)} pages captured for run {run}")
