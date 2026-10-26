#!/usr/bin/env python3
"""The week picker and the frame, checked before the gate touches Canvas.

Michel, 2026-10-26: Module 9's activity, "similar to the one from module 7".
The Python class names its modules "Week 7: Objects", not "Module 07" — the
module gate's reader would have found no week and nothing to file into. The
frame gate reads either spelling, and the frame is the share dialog's own.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
import canvas_frame as cf

assert cf.week_number("Week 7: Objects") == 7
assert cf.week_number("Week 9") == 9
assert cf.week_number("📦 Module 09 — Tests") == 9
assert cf.week_number("Week 17: Final") == 17, "week 17 is not week 1"
assert cf.week_number("Week 1") != 17
assert cf.week_number("Backstage") is None
body = cf.frame_body("https://share.lightcodepedia.org/share/abc/page", 900)
assert 'src="https://share.lightcodepedia.org/share/abc/page?focus=1&amp;up=0"' in body, body
assert 'allow="display-capture; microphone; camera"' in body
print("canvas_frame selftest: ok")
