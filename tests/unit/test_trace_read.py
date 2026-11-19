"""tools/trace_read.py — the paste trace, read deterministically (2026-11-19)."""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))
import trace_read as tr  # noqa: E402

RECORD = "\n".join([
    "# lc-progress v2",
    "gh:o/r/courses/c/module_09/02_list\t2/3\t1/1\t2026-11-19T20:00Z\to/bench\t1/1",
    "gh:o/r/courses/c/module_09/02_list#q:list_quiz\tq\t2026-11-19T19:58Z\t\t",
    "gh:o/r/courses/c/module_09/02_list@2026-11-19T20:10:04Z\tc\t1\t214\t640\t1820\t1\t1960\tbill>feature_pad:430;take_lines>feature_pad:210;~>feature_pad:1820;apply_rows=>feature_pad:1960",
    "gh:o/r/courses/c/module_09/02_list@2026-11-19T20:01:00Z\tc\t1\t35\t0\t0\t0\t0\t",
    "gh:o/r/courses/c/module_09/03_run@2026-11-19T21:00:00Z\tc\t2\t1\t2\t3\t4\t5\tfuture",
    "crc 00000000",
]) + "\n"


def test_only_trace_rows_are_read_and_in_time_order():
    rows = tr.rows_of(RECORD, "zik")
    assert [r["saved_at"] for r in rows] == ["2026-11-19T20:10:04Z", "2026-11-19T20:01:00Z"]
    r = rows[0]
    assert (r["typed"], r["from_page"], r["from_elsewhere"], r["pastes_elsewhere"], r["applied"]) == (214, 640, 1820, 1, 1960)
    assert r["page"] == "gh:o/r/courses/c/module_09/02_list"
    assert r["from_parts"] == "bill;take_lines"          # pastes from the page, never ~ or the page's own writes


def test_a_later_format_is_never_guessed():
    assert all(r["page"].endswith("02_list") for r in tr.rows_of(RECORD, "zik"))


def test_the_table_is_the_same_bytes_every_time():
    with tempfile.TemporaryDirectory() as d:
        for seat in ("zik", "amy"):
            os.makedirs(os.path.join(d, seat))
            open(os.path.join(d, seat, "__progress.txt"), "w").write(RECORD)
        a, b = tr.table([d]), tr.table([d])
        assert a == b
        lines = a.splitlines()
        assert lines[0] == ",".join(tr.COLUMNS)
        assert [l.split(",")[0] for l in lines[1:]] == ["amy", "amy", "zik", "zik"]
        assert lines[1].split(",")[2] == "2026-11-19T20:01:00Z"   # by time within a page
