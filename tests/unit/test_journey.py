"""tools/journey.py on a synthetic bench (Canvas writes each verse line as its own paragraph and marks a stanza break with a non-breaking-space line): one module, two pages — the first green at once, the
second red then green with two asks and a recording that failed once then saved — and the
learner's question-2 words placed on the page they name (layer 2). Run: python3 -m pytest tests/unit -q"""
import csv, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
V = "gh:uwm-build-ai/uwm-build-ai-vault/courses/micro_build_ai/"


def rec(rows, at):
    return "# lc-progress v2\n" + "\n".join("%s\t0/0\t%s\t%s\tb\t0/0" % (V + p, g, at) for p, g in rows)


def test_journey_lanes_takes_and_words(tmp_path):
    bench = tmp_path / "notes" / "21joberoi"
    (bench / "module_07").mkdir(parents=True)
    history = [
        {"sha": "a", "at": "2026-10-31T01:32:00Z", "message": "📊 progress", "record": rec([("module_07/01_ship_it", "1/1")], "2026-10-31T01:32:00Z")},
        {"sha": "b", "at": "2026-10-31T01:55:00Z", "message": "📊 progress", "record": rec([("module_07/01_ship_it", "1/1"), ("module_07/02_not_in_the_room", "0/1")], "2026-10-31T01:55:00Z")},
        {"sha": "c", "at": "2026-10-31T02:10:00Z", "message": "📊 progress", "record": rec([("module_07/01_ship_it", "1/1"), ("module_07/02_not_in_the_room", "1/1")], "2026-10-31T02:10:00Z")},
    ]
    (bench / "history.json").write_text(json.dumps(history))
    (bench / "module_07" / "__02_not_in_the_room.doc.md").write_text(
        "# log\n\n## 2026-10-31T01:57:00Z · agent Bill · m · level socratic\n\n**Q** why red\n\n**A** what does it check?\n\n"
        "## 2026-10-31T02:00:00Z · agent Bill · m · level direct\n\n**Q** fix\n\n**A** paste this\n\n"
        "## 2026-10-31T02:03:00Z · recorder started\n\n**Q** 🎬 recording\n\n**A** chrome · framed\n\n"
        "## 2026-10-31T02:04:00Z · recorder failed\n\n**Q** 🎬 recording\n\n**A** screen share cancelled\n\n"
        "## 2026-10-31T02:06:00Z · recorder started\n\n**Q** 🎬 recording\n\n**A** chrome\n\n"
        "## 2026-10-31T02:08:00Z · recorder saved\n\n**Q** 🎬 recording\n\n**A** 812 KB\n")
    seats = tmp_path / "__seats.yml"
    seats.write_text('seats:\n  "jsoberoi@uwm.edu":\n    name: "Oberoi, Jessica"\n    login: "21joberoi"\n    journey: "building"\n')
    essays = tmp_path / "essays_q2_2026-11-05.md"
    essays.write_text("# 📍 Assignments 07\n\n## 📍 Assignment 07 — Your learning path (quiz 1, published)\n\n### Jessica Singh Oberoi · 2026-11-02\n\n"
                      "🎵On the Ship It page, I shared my creation,\n\nAdoption Day was ready to go.\n\n\u00a0\n\nOn Add a Guide, I gave it a voice,\n\n\u00a0\n\n"
                      "On Stage became the tricky part,\n\nthe recording buttons hid from sight.\n\n\u00a0\n\nAt work, I would use Ship first.🎵\n")
    course = tmp_path / "course" / "module_07"
    course.mkdir(parents=True)
    (course / "__intro.md").write_text("# ℹ️ Module 07 — Show Time\n")
    (course / "01_ship_it.md").write_text("# 🚀 Ship It\n\n## 📱 Can I see it on my phone?\n\n```gherkin\nFeature: x\n```\n{: .feature #ship_proof tags=\"ship, qr\" }\n\n```gherkin\nFeature: y\n```\n{: .feature #qr_proof tags=\"qr\" }\n")
    (course / "02_not_in_the_room.md").write_text("# 🧭 Add a Guide\n\n## 🌅 She opens it.\n\n```markdown\nx\n```\n{: .mdpad #g }\n\n[f](#)\n{: .form master=\"g\" }\n\n- [x] a\n{: .prerequisite }\n\n```gherkin\nFeature: z\n```\n{: .feature #guide_proof tags=\"avatar\" visible=\"true\" }\n")
    (course / "03_send_it.md").write_text("# 🎤 On Stage\n\n## 🎤 Step in\n")
    notes_file = tmp_path / "journey_notes.csv"
    notes_file.write_text("login,module,page,who,when,note\n21joberoi,07,02_not_in_the_room,michelzam,2026-11-09T05:00:00Z,\"she said: almost quit, tried again\"\n21joberoi,07,,michelzam,2026-11-09T05:01:00Z,watched her ship live\n")
    out = tmp_path / "journey_latest"
    subprocess.run([sys.executable, os.path.join(ROOT, "tools", "journey.py"), "--notes", str(tmp_path / "notes"), "--out", str(out),
                    "--essays", str(essays), "--seats", str(seats), "--course-dir", str(tmp_path / "course"), "--notes-file", str(notes_file)], check=True)
    rows = {r["page"]: r for r in csv.DictReader(open(str(out) + ".csv"))}
    ship, guide = rows["01_ship_it"], rows["02_not_in_the_room"]
    assert ship["reds"] == "0" and ship["outcome"] == "green" and guide["reds"] == "1" and guide["effort_min"] == "15"
    assert guide["asks"] == "2" and guide["help_levels"] == "direct 1 socratic 1"
    assert guide["takes"] == "2" and guide["failed_takes"] == "1"
    assert guide["title"] == "🧭 Add a Guide" and guide["tools"] == "mdpad form" and ship["title"] == "🚀 Ship It"
    assert ship["tags"] == "ship qr" and guide["tags"] == "avatar", (ship["tags"], guide["tags"])   # the tags the course cards wear
    assert guide["trail"] == "✗✓" and ship["trail"] == "✓", (guide["trail"], ship["trail"])         # the runs, in order
    assert guide["module_title"] == "Module 07 — Show Time", guide["module_title"]
    # layer 2: each sentence on the page its words name; the rest on the module
    assert ship["value"].startswith("On the Ship It page, I shared my creation") and "Adoption Day" in ship["value"]
    assert guide["value"] == "On Add a Guide, I gave it a voice,"
    stage = rows.get("03_send_it")   # no save on that page: its words still ride the module's rows
    assert stage is None
    assert "At work, I would use Ship first" in ship["module_value"] and "On Stage" not in ship["module_value"]
    # layer 3: the desk's notes ride the rows, the module's on every row of the module
    assert guide["notes"] == "she said: almost quit, tried again" and ship["notes"] == ""
    assert ship["module_notes"] == "watched her ship live"
    events = list(csv.DictReader(open(str(out) + "_events.csv")))
    kinds = sorted({(e["kind"], e["outcome"]) for e in events})
    assert ("take", "failed") in kinds and ("take", "saved") in kinds and ("ask", "") in kinds and ("proof", "red") in kinds
