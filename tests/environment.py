import json
import os
import urllib.request
from datetime import datetime, timezone

from playwright.sync_api import sync_playwright

BASE_URL = os.environ.get("BASE_URL", "https://lightcodepedia.org").rstrip("/")
ASSETS = os.path.join(os.path.dirname(__file__), "..", "docs", "assets")
KEEP_RUNS = 30  # bound the committed history

_pw = None
_browser = None


def before_all(context):
    global _pw, _browser
    _pw = sync_playwright().start()
    # --expose-gc lets the metrics capture force a collection first, so
    # heap_mb measures THIS page, not residue from earlier scenarios in the
    # shared renderer process
    _browser = _pw.chromium.launch(
        headless=True, args=["--js-flags=--expose-gc"]
    )
    context.base_url = BASE_URL
    # fleet metrics: one row per page per run, captured after each scenario
    context.lc_metrics = {}          # path -> metrics row (last visit wins)
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
        _capture_page(context)
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


def _capture_page(context):
    url = context.page.url or ""
    if not url.startswith(context.base_url):
        return
    path = url[len(context.base_url):].split("#")[0].split("?")[0] or "/"
    row = context.page.evaluate(_CAPTURE_JS, context.lc_tokens)
    row["page"] = path
    row["console_errors"] = context.lc_console_errors
    row["run"] = context.lc_run
    context.lc_metrics[path] = row


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
