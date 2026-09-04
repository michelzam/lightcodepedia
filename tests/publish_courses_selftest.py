#!/usr/bin/env python3
"""A scoped publish never touches a sibling course.

The courses gate mirrors staged courses into a vault. When a run is scoped
to ONE course, every other course already in the vault must survive; only
a full run may prune a course the lab dropped. (2026-09-03: a run scoped to
`databases` erased `micro_build_ai` for the whole class.) No network — the
mirror script runs on temp folders.
"""
import os, subprocess, sys, tempfile

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "tools", "mirror_courses.sh")


def fill(root, course, body):
    os.makedirs(os.path.join(root, course), exist_ok=True)
    with open(os.path.join(root, course, "index.md"), "w") as fh:
        fh.write(body)


def run(stage, vault, scoped):
    subprocess.run(["bash", SCRIPT, stage, vault, "1" if scoped else "0"], check=True,
                   capture_output=True)


def test_a_scoped_run_leaves_the_sibling_alone():
    with tempfile.TemporaryDirectory() as t:
        stage, vault = os.path.join(t, "stage"), os.path.join(t, "vault", "courses")
        fill(vault, "micro_build_ai", "old build-ai")
        fill(vault, "databases", "old databases")
        fill(stage, "databases", "fresh databases!")
        run(stage, vault, scoped=True)
        assert open(os.path.join(vault, "micro_build_ai", "index.md")).read() == "old build-ai", \
            "the sibling course was erased by a scoped run"
        assert open(os.path.join(vault, "databases", "index.md")).read() == "fresh databases!"


def test_a_full_run_refreshes_and_prunes():
    with tempfile.TemporaryDirectory() as t:
        stage, vault = os.path.join(t, "stage"), os.path.join(t, "vault", "courses")
        fill(vault, "micro_build_ai", "old")
        fill(vault, "retired_course", "gone from the lab")
        fill(stage, "micro_build_ai", "fresh!")
        fill(stage, "databases", "fresh!")
        run(stage, vault, scoped=False)
        assert open(os.path.join(vault, "micro_build_ai", "index.md")).read() == "fresh!"
        assert os.path.exists(os.path.join(vault, "databases", "index.md"))
        assert not os.path.exists(os.path.join(vault, "retired_course")), \
            "a full run must prune a course the lab no longer assigns here"


def test_a_stale_file_inside_a_course_is_removed():
    with tempfile.TemporaryDirectory() as t:
        stage, vault = os.path.join(t, "stage"), os.path.join(t, "vault", "courses")
        fill(vault, "databases", "old")
        with open(os.path.join(vault, "databases", "stale.md"), "w") as fh:
            fh.write("x")
        fill(stage, "databases", "fresh!")
        run(stage, vault, scoped=True)
        assert not os.path.exists(os.path.join(vault, "databases", "stale.md"))


if __name__ == "__main__":
    fails = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            try:
                fn(); print("ok  ", name)
            except AssertionError as e:
                fails += 1; print("FAIL", name, "—", e)
    print("\n%d failure(s)" % fails)
    sys.exit(1 if fails else 0)
