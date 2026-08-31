#!/usr/bin/env python3
"""The module picker, checked against the twin it once raised.

Michel, 2026-08-29 in Canvas 861887: the gate matched modules on OUR exact
spelling, found no "📦 Module 01", and created one right beside his own
"📦 Module 01 — Data Quest". Two modules for one module. His ruling the next
day: "do not create a new module01, use the one I created".

So the gate files into the module already standing for that NUMBER, whatever
the teacher called it — and when two claim the number it stops and says so,
because merging is the teacher's call, not ours.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
import canvas_module as cm


def mods(*names):
    return [{"id": 100 + i, "name": n} for i, n in enumerate(names)]


def test_the_teachers_own_name_is_used():
    """The regression: his module, our run, no twin."""
    mod, clash = cm.pick_module(mods("📦 Module 01 — Data Quest"), "01")
    assert clash is None, clash
    assert mod["name"] == "📦 Module 01 — Data Quest"


def test_a_number_with_no_module_is_created():
    mod, clash = cm.pick_module(mods("📦 Module 01 — Data Quest"), "02")
    assert (mod, clash) == (None, None), (mod, clash)


def test_two_claimants_stop_the_run():
    mod, clash = cm.pick_module(
        mods("📦 Module 01", "📦 Module 01 — Data Quest"), "01")
    assert mod is None
    assert "merge them in Canvas" in clash and "Data Quest" in clash


def test_neighbours_are_not_this_module():
    """01 must not answer for 10, nor a module with no number at all."""
    rows = mods("Start here", "📦 Module 10 — Joins", "Syllabus")
    assert cm.pick_module(rows, "01") == (None, None)
    assert cm.pick_module(rows, "10")[0]["name"] == "📦 Module 10 — Joins"


def test_the_teacher_may_spell_it_any_way():
    for name in ("module 01 data quest", "Module 1: Data Quest",
                 "📦 MODULE_01", "Week 3 — Module 01"):
        mod, clash = cm.pick_module(mods(name), "01")
        assert mod and not clash, name


def test_every_spec_is_named_by_its_own_first_line():
    """The gate stopped imposing names the day it renamed Michel's."""
    assert cm.specs_of(["canvas.md"], "01") == [("canvas.md", None)]
    assert cm.specs_of(["assignment.md", "canvas.md"], "01") == [
        ("canvas.md", None), ("assignment.md", None)]


def test_the_module_check_is_always_filed_first():
    got = [n for n, _ in cm.specs_of(["a_first.md", "canvas.md", "z_last.md"], "02")]
    assert got == ["canvas.md", "a_first.md", "z_last.md"], got


def test_only_specs_count():
    """A stray file in __quiz is not a check."""
    got = cm.specs_of(["canvas.md", "notes.txt", "screenshot.png"], "01")
    assert got == [("canvas.md", None)], got


def test_a_renamed_check_keeps_the_teachers_name():
    """410: he renamed ⚙️ Quiz 01 to ⚙️ Quiz 1d — Data Quest by hand."""
    got = cm.title_for("⚙️ Quiz 1d — Data Quest", "⚙️ Quiz 01",
                       ["⚙️ Quiz 1d — Data Quest", "📍 Assignment 1c — Data Quest"])
    assert got == "⚙️ Quiz 1d — Data Quest", got


def test_a_check_created_under_the_gates_name_is_never_renamed():
    """BUILD-AI: the spec says "05 · Basement — check", Canvas says
    "⚙️ Quiz 05" — the run must update it, not rename it."""
    assert cm.title_for("05 · Basement — check", "⚙️ Quiz 05",
                        ["⚙️ Quiz 05"]) == "⚙️ Quiz 05"


def test_something_new_wears_its_own_title():
    assert cm.title_for("📍 Assignment 2a", "⚙️ Quiz 02", []) == "📍 Assignment 2a"
    assert cm.title_for("", "⚙️ Quiz 02", []) == "⚙️ Quiz 02"


def test_the_frame_page_is_found_by_number_under_any_name():
    page, clash = cm.page_for("01", ["📜 Module 01 — Data Quest", "ℹ️ Introduction"])
    assert (page, clash) == ("📜 Module 01 — Data Quest", None), (page, clash)


def test_only_our_scroll_pages_count_as_frames():
    """A course's own "📖 Module 10 — Advanced MySQL" must never be
    overwritten by a lesson frame — the scroll is ours, the book is his."""
    page, clash = cm.page_for("10", ["📖 Module 10 — Advanced MySQL"])
    assert (page, clash) == ("📜 Module 10", None), (page, clash)


def test_two_frames_for_one_module_stop_the_run():
    page, clash = cm.page_for("01", ["📜 Module 01", "📜 Module 01 — Data Quest"])
    assert page is None and "merge them in Canvas" in clash


def test_the_folders_front_page_is_not_a_check():
    """index.md is the shelf's own page everywhere else — it pushed an empty
    quiz into 861887 once, and once is the whole point of this line."""
    got = cm.specs_of(["assignment.md", "canvas.md", "index.md"], "01")
    assert [n for n, _ in got] == ["canvas.md", "assignment.md"], got


if __name__ == "__main__":
    fails = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            try:
                fn(); print("ok   " + name)
            except AssertionError as e:
                fails += 1; print("FAIL " + name + ": " + str(e)[:200])
    print("\n%d failure(s)" % fails)
    sys.exit(1 if fails else 0)
