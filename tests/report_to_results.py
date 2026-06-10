#!/usr/bin/env python3
"""Transform a behave JSON report into a slim per-scenario results file.

Reads behave's verbose `-f json` output and writes a flat array of scenario
rows that the LC `.dataset` / `.datagrid` components can render directly:

    [{"status": "✅", "scenario": "...", "feature": "...", "tags": "@mobile",
      "seconds": 1.23, "run": "2026-06-09T19:35Z",
      "url": "/assets/ux-report.html#scenario_0"}, ...]

The `url` field drives row-click navigation in the LC datagrid to the full
Gherkin HTML step trace for that scenario (including error details on failure).
The anchor `scenario_N` matches the positional ID used by behave-html-formatter.

Usage:
    python tests/report_to_results.py <behave.json> <out.json> [--status STATE]
                                       [--html-base BASE_URL]

--status overrides every row's status (used to seed a "pending" file from a
behave --dry-run before the suite has run for real).
--html-base sets the base path/URL for the HTML report (default: /assets/ux-report.html).
"""
import json
import sys
from datetime import datetime, timezone

ICON = {"passed": "✅", "failed": "❌", "skipped": "⏭️",
        "untested": "⏳", "pending": "⏳", "error": "❌"}


def scenario_status(el):
    """Derive a scenario's status from its own field or its steps."""
    st = el.get("status")
    if st:
        return st
    steps = el.get("steps", [])
    states = [s.get("result", {}).get("status") for s in steps if s.get("result")]
    if not states:
        return "untested"
    if "failed" in states or "error" in states:
        return "failed"
    if all(s == "passed" for s in states):
        return "passed"
    return "skipped"


def scenario_seconds(el):
    total = 0.0
    for s in el.get("steps", []):
        total += (s.get("result") or {}).get("duration", 0.0) or 0.0
    return round(total, 2)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    force = None
    html_base = "/assets/ux-report.html"
    for flag in ("--status", "--html-base"):
        if flag in sys.argv:
            val = sys.argv[sys.argv.index(flag) + 1]
            if flag == "--status":
                force = val
            else:
                html_base = val
    src, out = args[0], args[1]

    with open(src) as fh:
        report = json.load(fh)

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    rows = []
    idx = 0
    for feat in report:
        fname = (feat.get("name") or "").strip()
        for el in feat.get("elements", []):
            if el.get("type") != "scenario":
                continue
            st = force or scenario_status(el)
            rows.append({
                "status": ICON.get(st, "⚪"),
                "scenario": (el.get("name") or "").strip(),
                "feature": fname,
                "tags": " ".join("@" + t for t in (el.get("tags") or [])),
                "seconds": scenario_seconds(el),
                "run": stamp,
                "url": f"{html_base}#scenario_{idx}",
            })
            idx += 1

    with open(out, "w") as fh:
        json.dump(rows, fh, ensure_ascii=False, indent=2)

    passed = sum(1 for r in rows if r["status"] == "✅")
    print(f"Wrote {len(rows)} scenarios to {out} ({passed} passed)")


if __name__ == "__main__":
    main()
