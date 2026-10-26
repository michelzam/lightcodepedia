"""tools/struggle.py on a synthetic bench in the benches' own shape (a write, then 📊 progress with
the record): one page red then green (recovery 2 h, one save between), one page green first right after an 80-line save (a jump), one page never green,
and two verbatim asks back to back (one pull). Run: python3 -m pytest tests/unit -q"""
import csv, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
V = "gh:uwm-build-ai/uwm-build-ai-vault/courses/micro_build_ai/"


def rec(rows, at="2026-10-01T00:00:00Z"):
    return "# lc-progress v2\n" + "\n".join("%s\t0/0\t%s\t%s\tb" % (V + p, g, at) for p, g in rows)


def test_struggle_reads_a_bench(tmp_path):
    bench = tmp_path / "notes" / "l1"
    (bench / "module_03").mkdir(parents=True)
    history = [
        {"sha": "a", "at": "2026-10-01T10:00:00Z", "message": "✍️ persona", "files": [], "added": 10, "removed": 0},
        {"sha": "b", "at": "2026-10-01T10:01:00Z", "message": "📊 progress", "files": ["__progress.txt"], "added": 1, "removed": 0,
         "record": rec([("module_03/01_persona", "0/2")], "2026-10-01T10:01:00Z")},
        {"sha": "c", "at": "2026-10-01T12:00:00Z", "message": "Inline edit: .feature  #x", "files": [], "added": 5, "removed": 2},
        {"sha": "d", "at": "2026-10-01T12:01:00Z", "message": "📊 progress", "files": ["__progress.txt"], "added": 1, "removed": 1,
         "record": rec([("module_03/01_persona", "2/2")], "2026-10-01T12:01:00Z")},
        {"sha": "e", "at": "2026-10-02T09:00:00Z", "message": "✍️ all_dogs", "files": [], "added": 80, "removed": 0},
        {"sha": "f", "at": "2026-10-02T09:01:00Z", "message": "📊 progress", "files": ["__progress.txt"], "added": 1, "removed": 1,
         "record": rec([("module_03/01_persona", "2/2"), ("module_04/01_a", "3/3"), ("module_04/02_b", "1/3")], "2026-10-02T09:01:00Z")},
    ]
    (bench / "history.json").write_text(json.dumps(history))
    (bench / "__progress.txt").write_text(rec([("module_03/01_persona", "2/2")]))
    (bench / "module_03" / "__04_concepts.doc.md").write_text(
        "# log\n\n## t1 · agent The reviewer · m\n\n**Q** is it consistent?\n\n**A** DRIFT\n\n"
        "## t2 · agent The reviewer · m\n\n**Q** is it consistent?\n\n**A** DRIFT\n\n"
        "## t3 · agent The reviewer · m\n\n**Q** is it consistent now\n\n**A** DRIFT\n")
    out = tmp_path / "struggle_2026-10-26"
    subprocess.run([sys.executable, os.path.join(ROOT, "tools", "struggle.py"), "--notes", str(tmp_path / "notes"), "--out", str(out)], check=True)
    rows = {r["module"]: r for r in csv.DictReader(open(str(out) + ".csv"))}
    assert rows["03"]["red_first"] == "1" and rows["03"]["recovery_h"] == "2.0" and rows["03"]["recovery_saves"] == "1"
    assert rows["03"]["pulls"] == "1"
    assert rows["04"]["green_first"] == "1" and rows["04"]["jumps"] == "1" and rows["04"]["never_green"] == "1"
    page = (str(out) + ".md")
    text = open(page).read()
    assert "{: .dataset #by_module" in text and "red_first_pct: 100" in text and "L01" in text
