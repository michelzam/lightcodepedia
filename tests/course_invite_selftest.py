#!/usr/bin/env python3
"""Who gets asked, and who is left alone.

The planning half is where a mistake costs something real: inviting a
student twice is noise, inviting nobody is a stuck class, and burning an
invitation that expires in seven days on someone who already has one is
worse than doing nothing. No network here — the Canvas and GitHub halves
are stubbed, so this runs anywhere.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
import course_invite as ci


def stub(roster_rows, members=(), pending=()):
    ci.roster = lambda course: list(roster_rows)
    ci.org_state = lambda org: (set(members),
                                {e.lower(): {"created_at": "2026-08-12T00:00:00Z"}
                                 for e in pending},
                                len(members))


def emails_of(people):
    return sorted(p["email"] for p in people)


def test_a_fresh_roster_is_all_invited():
    stub([{"name": "A", "email": "a@uwm.edu"}, {"name": "B", "email": "b@uwm.edu"}])
    todo, skip, _, _ = ci.plan("1", "org")
    assert emails_of(todo) == ["a@uwm.edu", "b@uwm.edu"], todo
    assert not skip


def test_a_pending_invitation_is_not_sent_twice():
    """It expires in seven days; spending it again resets nothing and
    confuses the student's inbox."""
    stub([{"name": "A", "email": "a@uwm.edu"}, {"name": "B", "email": "b@uwm.edu"}],
         pending=["A@uwm.edu"])            # case must not matter
    todo, skip, _, _ = ci.plan("1", "org")
    assert emails_of(todo) == ["b@uwm.edu"], todo
    assert "already invited" in skip[0][1], skip


def test_a_student_with_no_email_is_named_not_dropped():
    """Canvas can withhold the address; a silent disappearance would leave a
    student stuck with nobody knowing why."""
    stub([{"name": "Ghost", "email": ""}, {"name": "B", "email": "b@uwm.edu"}])
    todo, skip, _, _ = ci.plan("1", "org")
    assert emails_of(todo) == ["b@uwm.edu"]
    assert skip and skip[0][0]["name"] == "Ghost" and "no email" in skip[0][1]


def test_the_same_address_twice_is_asked_once():
    stub([{"name": "A", "email": "a@uwm.edu"}, {"name": "A again", "email": "A@UWM.edu"}])
    todo, skip, _, _ = ci.plan("1", "org")
    assert len(todo) == 1, todo
    assert "twice" in skip[0][1]


def test_a_pasted_list_works_when_canvas_hides_emails():
    stub([], pending=[])
    todo, _, _, _ = ci.plan("", "org", emails=["x@uwm.edu", "y@uwm.edu"])
    assert emails_of(todo) == ["x@uwm.edu", "y@uwm.edu"]


def test_a_dry_run_sends_nothing():
    """The default must be harmless: --confirm is the only door to the API."""
    calls = []
    ci._call = lambda *a, **k: calls.append(a) or ("", "", 201)
    os.environ["ORG_TOKEN"] = "stub"
    sent, fail, _ = ci.invite("org", [{"name": "A", "email": "a@uwm.edu"}], None, False)
    assert calls == [], "a dry run reached the network: %r" % calls
    assert (sent, fail) == (0, 0)


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
