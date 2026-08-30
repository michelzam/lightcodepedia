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


def test_the_folder_is_the_modules_checks():
    """canvas.md wears the gate's name; a second spec keeps its own."""
    assert cm.specs_of(["canvas.md"], "01") == [("canvas.md", "⚙️ Quiz 01")]
    assert cm.specs_of(["assignment.md", "canvas.md"], "01") == [
        ("canvas.md", "⚙️ Quiz 01"), ("assignment.md", None)]


def test_the_module_check_is_always_filed_first():
    got = [n for n, _ in cm.specs_of(["a_first.md", "canvas.md", "z_last.md"], "02")]
    assert got == ["canvas.md", "a_first.md", "z_last.md"], got


def test_only_specs_count():
    """A stray file in __quiz is not a check."""
    got = cm.specs_of(["canvas.md", "notes.txt", "screenshot.png"], "01")
    assert got == [("canvas.md", "⚙️ Quiz 01")], got


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
