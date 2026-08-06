#!/usr/bin/env python3
"""Photograph the x-ray's flowing PIPES — no hand-recorded screen needed.

The pipes look un-photographable because they need a gesture. They don't. On
desktop the gesture is Alt to raise the lens and Alt+Shift to switch it to
pipelines (xray.md: pointermove is gated on altKey, shiftKey picks the mode),
and Playwright drives modifier state natively.

Two details cost a cycle each if you guess them:
  · the handler needs a MOVEMENT DELTA, so move the mouse twice
  · the elements are .lcx-svg / .lcx-scene / .lcx-edge / .lcx-flow / .lcx-ring
    — count the svg's children to know the pipes really drew, rather than
    eyeballing a screenshot that might only be showing the lens

For MOVING pipes, pass record_video_dir to new_context() and drive the same
gesture: Playwright records the page itself.

    PW_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome \
    MARKED_JS=$PWD/.libs/marked.min.js JS_YAML=$PWD/.libs/js-yaml.min.js \
    AG_GRID_DIR=$PWD/.libs/ag CHART_JS=$PWD/.libs/chart.umd.min.js \
    MPY_DIR=$PWD/.libs/mpy python3 tests/shots_pipes.py hq/shots
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from playwright.sync_api import sync_playwright

from environment import (_stub_ag_grid, _stub_js_yaml,  # noqa: E402
                         _stub_marked, _stub_micropython)

BASE = os.environ.get("BASE_URL", "http://127.0.0.1:8899")
EXE = os.environ.get("PW_CHROMIUM_EXECUTABLE")
CHART_JS = os.environ.get("CHART_JS")

# one dataset feeding two charts and two grids: the densest wiring in the
# catalog, so the pipes have something worth showing
PAGE = "/components/dataset"
ANCHOR = '[data-lc-id="monthly_grid"]'


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "hq/shots"
    os.makedirs(out_dir, exist_ok=True)
    chart = None
    if CHART_JS and os.path.isfile(CHART_JS):
        with open(CHART_JS, "rb") as fh:
            chart = fh.read()

    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=EXE)
        ctx = browser.new_context(viewport={"width": 1400, "height": 900},
                                  device_scale_factor=2)
        page = ctx.new_page()
        for stub in (_stub_marked, _stub_micropython, _stub_ag_grid, _stub_js_yaml):
            stub(page)
        if chart:
            page.route(
                "https://cdn.jsdelivr.net/npm/chart.js@*/dist/chart.umd.min.js",
                lambda r: r.fulfill(status=200, body=chart,
                                    content_type="application/javascript"))

        page.goto(BASE + PAGE, wait_until="domcontentloaded")
        page.wait_for_selector(ANCHOR, state="visible", timeout=40_000)
        page.wait_for_timeout(3000)
        page.evaluate("() => window.lcMode && window.lcMode.set('xray')")
        page.wait_for_timeout(1500)

        grid = page.locator(ANCHOR).first
        grid.scroll_into_view_if_needed()
        page.wait_for_timeout(600)
        box = grid.bounding_box()
        cx, cy = box["x"] + box["width"] / 2, box["y"] + 40

        page.keyboard.down("Alt")
        page.keyboard.down("Shift")
        page.mouse.move(cx, cy)
        page.wait_for_timeout(400)
        page.mouse.move(cx + 2, cy + 2)      # the delta is what triggers a rebuild
        page.wait_for_timeout(1800)          # let the pipes draw and start flowing

        drawn = page.evaluate(
            "() => { var s = document.querySelector('.lcx-svg');"
            "        return s ? s.children.length : 0; }")
        path = os.path.join(out_dir, "xray_pipes_live.png")
        page.screenshot(path=path)
        page.keyboard.up("Shift")
        page.keyboard.up("Alt")
        browser.close()

    print(f"{drawn} pipe elements drawn -> {path}")
    if not drawn:
        print("  the lens may be up without the pipes: check the gesture, and "
              "that a SECOND mouse move happened")
    return 0 if drawn else 1


if __name__ == "__main__":
    sys.exit(main())
