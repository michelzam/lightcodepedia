#!/usr/bin/env python3
"""The tell detector, checked against the ways a quiz leaks.

Michel found the leak in my own drafts on 2026-08-19 — "the right answer is
the longest and sometimes with some bold 🤭" — so each case below is a way
to score without the material, and the detector must name it.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
import canvas_quiz as cq


def q(answers, text="Which fix works on the reservations list?", **kw):
    return {"questions": [{"name": "t", "text": text,
                           "answers": answers, **kw}], "anchors": ["reservations"]}


def only(quiz, needle):
    hits = [b for b in cq.tells(quiz) if needle in b]
    assert hits, "missed: %s\nsaw: %r" % (needle, cq.tells(quiz))
    return hits


def test_longest_key():
    only(q([{"text": "Sort it"}, {"text": "Delete rows"},
            {"text": "Add WHERE met = '' so only the families still waiting remain here",
             "correct": True}]), "longest option")


def test_formatting_only_on_key():
    only(q([{"text": "Sort the reservations grid by met"},
            {"text": "Delete the five rows from data"},
            {"text": "**Add the WHERE clause to it**", "correct": True}]), "bold/code/emoji")


def test_absolutes_in_distractors():
    only(q([{"text": "Always call every family listed"},
            {"text": "Add WHERE met to the query", "correct": True},
            {"text": "Never call a family in list"}]), "always/never/all")


def test_all_of_the_above():
    only(q([{"text": "Sort the reservations by met"},
            {"text": "Add the WHERE clause", "correct": True},
            {"text": "All of the above"}]), "other options")


def test_stem_without_an_anchor():
    """A question answerable from general knowledge is the whole failure."""
    only({"anchors": ["reservations", "Diallo"],
          "questions": [{"name": "generic", "text": "What does SQL WHERE do?",
                         "answers": [{"text": "Filters rows", "correct": True},
                                     {"text": "Sorts rows"}, {"text": "Joins tables"}]}]},
         "names nothing from the module")


def test_key_always_in_the_same_slot():
    quiz = {"anchors": ["reservations"], "questions": []}
    for i in range(4):
        quiz["questions"].append({"name": str(i), "text": "reservations question",
                                  "answers": [{"text": "aaa aaa"}, {"text": "bbb bbb"},
                                              {"text": "ccc ccc", "correct": True}]})
    only(quiz, "key sits in position")


def test_a_clean_quiz_passes():
    quiz = cq.load(os.path.join(os.path.dirname(__file__), "..", "courses",
                                "micro_build_ai", "module_05", "__quiz", "canvas.md"))
    assert cq.tells(quiz) == [], cq.tells(quiz)


def test_an_option_that_explains_nothing():
    """The quiz is the module's last lesson — a silent option teaches nobody."""
    only(q([{"text": "Sort the reservations grid", "why": "The view, not the question."},
            {"text": "Add the WHERE clause to it", "correct": True},
            {"text": "Delete the five rows again", "why": "The data is true."}]),
         "explain nothing")


def test_a_key_the_course_already_marks():
    """Enrolled learners hold read on the vault: they can grep for "- [x]"."""
    import tempfile, os as _os
    d = tempfile.mkdtemp()
    _os.makedirs(_os.path.join(d, "m5"))
    open(_os.path.join(d, "m5", "page.md"), "w").write(
        "**Q:** Was it broken?\n\n"
        "- [ ] No, every part rendered\n"
        "- [x] Yes, and nothing could tell you. The parts all worked; the page\n"
        "  answered the wrong question\n")
    quiz = {"anchors": ["reservations"], "questions": [{
        "name": "leak", "text": "reservations: was the page broken?",
        "answers": [{"text": "No the parts rendered fine here", "why": "x"},
                    {"text": "Yes and nothing could tell you the parts all worked "
                             "the page answered the wrong question", "correct": True, "why": "x"},
                    {"text": "No the data was wrong instead", "why": "x"}]}]}
    hits = cq.leaks(quiz, d)
    assert hits and "grep" in hits[0], hits


def test_every_explanation_rides_its_own_option():
    """Per-option only, by decision: the question-level comment slots stay
    empty — a second, vaguer voice after the picked option's own why, and
    "go fix it" is empty advice after the last attempt (Michel, 2026-08-21)."""
    q = {"name": "Q1", "text": "why?",
         "answers": [{"text": "a", "correct": True, "why": "the one"},
                     {"text": "b", "why": "not this"}]}
    body = cq.to_canvas_question(q, 1)["question"]
    assert body["answers"][0]["comments"] == "the one"
    assert body["answers"][1]["comments"] == "not this"
    # comments_html is the field the RESULTS PAGE renders — plain comments
    # stored fine and displayed nowhere (2026-08-21)
    assert body["answers"][0]["comments_html"] == "<p>the one</p>"
    assert "correct_comments" not in body and "incorrect_comments" not in body


def test_markdown_reads_as_the_same_spec():
    """One grammar, two readers: the md road must carry everything the yaml
    carried — knobs, notes, whys — and points defaults to 1 (Michel,
    2026-08-21: "make points = 1 by default")."""
    md = (
        '# T\n{: .canvas_quiz attempts="2" anchors="met, Diallo" }\n\n'
        'About the list.\n\n'
        '### q1\n\nWhat does met hold for Diallo?\n\n'
        '- [ ] a\n\n  > no\n\n'
        '- [x] b\n\n  > yes\n  > really\n\n'
        '{: .quiz }\n')
    sp = cq.parse_md(md)
    assert sp["title"] == "T" and sp["attempts"] == 2
    assert sp["anchors"] == ["met", "Diallo"]
    assert sp["description"] == "About the list."
    q = sp["questions"][0]
    assert q["text"] == "What does met hold for Diallo?"
    assert q["answers"][1].get("correct") and q["answers"][1]["why"] == "yes really"
    body = cq.to_canvas_question(q, 1)["question"]
    assert body["points_possible"] == 1


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
