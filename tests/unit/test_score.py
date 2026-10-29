"""tools/score.py: one learner, two pages of a two-module course — one done (quiz won,
proof green), one opened but not done, the rest never opened. Run: python3 -m pytest tests/unit -q"""
import csv, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
V = "gh:uwm-build-ai/uwm-build-ai-vault/courses/demo_course/"


def test_score_counts_pages_done(tmp_path):
    course = tmp_path / "courses" / "demo_course"
    for m, pages in (("module_00", ["00_a", "01_b"]), ("module_01", ["00_c", "01_d"])):
        (course / m).mkdir(parents=True)
        for p in pages:
            (course / m / (p + ".md")).write_text("# page\n")
    bench = tmp_path / "notes" / "ada"
    bench.mkdir(parents=True)
    (bench / "__progress.txt").write_text(
        "# lc-progress v2\n"
        + "%smodule_00/00_a\t3/3\t1/1\t2026-10-20T10:00:00Z\tb\n" % V
        + "%smodule_00/01_b\t2/3\t1/1\t2026-10-21T10:00:00Z\tb\n" % V
        + "%smodule_01/00_c\t0/0\t1/1\t2026-10-19T10:00:00Z\tb\n" % V)
    (tmp_path / "notes" / "zamm-student").mkdir()
    out = tmp_path / "scores.csv"
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "score.py"), "--notes", str(tmp_path / "notes"),
                        "--root", str(tmp_path), "--course", "courses/demo_course", "--max-module", "1",
                        "--exclude", "zamm-student", "--out", str(out)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    rows = list(csv.DictReader(open(out)))
    assert [x["login"] for x in rows] == ["ada"]
    assert rows[0]["done"] == "2" and rows[0]["total"] == "4" and rows[0]["left_pct"] == "50"
    assert rows[0]["last_save"] == "2026-10-21T10:00:00Z"
