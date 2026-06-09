#!/usr/bin/env python3
"""Transform a behave JSON report into a slim per-scenario results file.

Reads behave's verbose `-f json` output and writes a flat array of scenario
rows that the LC `.dataset` / `.datagrid` components can render directly:

    [{"status": "✅", "scenario": "...", "feature": "...",
      "tags": "@mobile", "seconds": 1.23, "run": "2026-06-09T19:35Z"}, ...]

Usage:
    python tests/report_to_results.py <behave.json> <out.json> [--status STATE]

--status overrides every row's status (used to seed a "pending" file from a
behave --dry-run before the suite has run for real).
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
    if "--status" in sys.argv:
        force = sys.argv[sys.argv.index("--status") + 1]
    src, out = args[0], args[1]

    with open(src) as fh:
        report = json.load(fh)

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    rows = []
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
            })

    with open(out, "w") as fh:
        json.dump(rows, fh, ensure_ascii=False, indent=2)

    passed = sum(1 for r in rows if r["status"] == "✅")
    print(f"Wrote {len(rows)} scenarios to {out} ({passed} passed)")


if __name__ == "__main__":
    main()
