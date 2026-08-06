#!/usr/bin/env python3
"""Author-side integrity pass over a course. Not a behave suite — no browser.

Every check here exists because something slipped through once:

  TAG-NO-DEF / TAG-NO-PROSE   a feature tag with no footnote, or one a reader
                              never meets in prose, teaches nothing
  FN-NOT-A-TAG                the other direction, and the stricter half of the
                              same rule: the footnote list is the page's TAGS
                              and nothing else. With no heading above it a
                              reader cannot tell a definition from an aside,
                              so the list stops being where you look a tag up
  ORPHAN-DEF / DANGLING-REF   footnotes that define nothing anyone reads, and
                              refs pointing at definitions that were deleted
                              (a `[^karma]` once silently repointed at [^quiz])
  REF-IN-FENCE                a ref used ONLY inside a fenced block: the
                              page-level footnote pass shields fences, so the
                              reference never resolves and shows as "?"
  DOT-FAIL                    a graphviz block that will not render
  AVATAR-YAML / AVATAR-ANCHOR an avatar script that will not parse, or an at:
                              pointing at an id that no longer exists — a
                              walk to a missing target just stands still,
                              which is why `at: next` survived its own
                              anchor's deletion
  LATE-VERB / NO-VERB         "Yoda mode": a clause whose verb arrives last,
                              or never arrives. Michel's standing rule, and the
                              one that keeps coming back because a fluent adult
                              reader does not feel it.
  LEGACY-MARGIN               a margin still on the pre-dunder name. `_x` only
                              hides a file from the folder's cards; `__x` is
                              what never travels.
  BENCH-FILE                  an .md that some page's save="…" names, so the
                              copy in the repo is the author's own work, not
                              lesson content. This is how `cv.md` — written by
                              save="cv.md" while the author tested the lesson
                              — ended up on the students' folder page as a
                              card called "Cv". Same leak class as the notes
                              margin: an author's bench IS this repo, so
                              anything a lesson saves lands beside it.

    python3 tests/course_audit.py [courses/micro_build_ai]
"""
import glob
import os
import re
import subprocess
import sys

try:
    import yaml
except ImportError:
    yaml = None


def fenced_spans(text):
    return [(m.start(), m.end()) for m in
            re.finditer(r"^(`{3,})[^\n]*\n.*?^\1\s*$", text, re.S | re.M)]


def in_fence(pos, spans):
    return any(a <= pos < b for a, b in spans)


def check_page(path, text):
    problems = []
    spans = fenced_spans(text)

    tags = set()
    for m in re.finditer(r'\{:[^}]*\btags="([^"]*)"', text):
        tags.update(t.strip() for t in m.group(1).split(",") if t.strip())

    defs = set(re.findall(r"^\[\^([^\]]+)\]:", text, re.M))

    # a `[^x]:` is a DEFINITION only at the start of a line (kramdown's rule).
    # Mid-line, "`x-ray`[^x-ray]: tap the pill" is a reference that merely
    # happens to be followed by a colon.
    refs = {}
    for m in re.finditer(r"\[\^([^\]]+)\]", text):
        ls = text.rfind("\n", 0, m.start()) + 1
        if m.start() == ls and text[m.end():m.end() + 1] == ":":
            continue
        refs.setdefault(m.group(1), []).append(m.start())

    # THE RULE (Michel, 2026-08-05): the footnote list IS the page's tags and
    # nothing else. There is no heading above it — footnotes are a notation,
    # not a section — so a reader cannot tell a tag definition from an aside,
    # and the list stops being the place you look a tag up. Expert sources are
    # not deleted, they stop being footnotes: an inline link in the prose is
    # where a curious reader wants Fowler or Adzic anyway.
    for k in sorted(defs - tags):
        problems.append(f'FN-NOT-A-TAG  [^{k}] is not a tag on this page. '
                        f"Footnotes are for tags only — make it prose, or an "
                        f"inline link if it is a source.")
    for k in sorted(defs - set(refs)):
        problems.append(f"ORPHAN-DEF    [^{k}] defined, never referenced")
    for k in sorted(set(refs) - defs):
        problems.append(f"DANGLING-REF  [^{k}] referenced, never defined")
    for k in sorted(tags - defs):
        problems.append(f'TAG-NO-DEF    tag "{k}" has no footnote')
    for k, pos in sorted(refs.items()):
        if all(in_fence(p, spans) for p in pos):
            problems.append(f"REF-IN-FENCE  [^{k}] only referenced inside a fence")

    body = text
    for a, b in reversed(spans):
        body = body[:a] + " " * (b - a) + body[b:]
    for t in sorted(tags):
        if f"`{t}`" not in body:
            problems.append(f'TAG-NO-PROSE  tag "{t}" is never used in backticked prose')

    problems.extend(verb_problems(body))

    for i, m in enumerate(re.finditer(r"^```dot\n(.*?)^```", text, re.S | re.M)):
        p = subprocess.run(["dot", "-Tsvg"], input=m.group(1),
                           capture_output=True, text=True)
        if p.returncode != 0:
            problems.append(f"DOT-FAIL      block {i + 1}: {p.stderr.strip()[:110]}")

    m = re.search(r"^```yaml\n(bot:.*?)^```", text, re.S | re.M)
    if m:
        block = m.group(1)
        if yaml:
            try:
                yaml.safe_load(block)
            except Exception as e:
                problems.append(f"AVATAR-YAML   {str(e)[:110]}")
        ids = set(re.findall(r"[#]([A-Za-z_][\w-]*)", text))
        for a in sorted(set(re.findall(r"^\s*(?:-\s*)?at:\s*(\S+)", block, re.M))):
            missing = (a[1:] not in text) if a.startswith(".") else (a not in ids)
            if missing:
                problems.append(f'AVATAR-ANCHOR at: {a} resolves to nothing')
    return problems


# ── the verb rule (Michel, standing) ─────────────────────────────────────
# "Yoda mode": the verb arrives at the very END of a clause. "the facts an app
# holds" makes a reader carry two nouns with nothing to do until a verb turns
# up. Kids and non-native readers stall on it; fluent adults do not feel it at
# all, which is why it keeps coming back.
#
# ONE pattern, and it is deliberately narrow: a REDUCED RELATIVE CLAUSE — a
# noun, then another noun phrase, then the verb, then the clause ends. That is
# the shape Michel has flagged twice, and it is the shape a regex can actually
# recognise.
#
# What is NOT here, on purpose: "no verb at all" ("Families arriving all
# morning"). A first attempt flagged "Families arrive all morning", "A promise
# and its app stop matching" and "A builder decides" — all correct English.
# Telling those apart needs to know which words are verbs, which needs a POS
# tagger, not a pattern. A rule that cries wolf gets ignored, and an ignored
# rule is worse than none, so that half stays a human job.
_LATE_VERBS = (r"holds|keeps|needs|shows|makes|brings|gives|takes|wants|sees|"
               r"reads|writes|uses|means|carries|guards|answers|owns|hides|"
               r"serves|counts|feeds|names|covers|drives")

# <noun> <det> <noun> <verb-s> <clause end> — the second noun phrase is what
# makes it a reduced relative rather than an ordinary subject + verb, so
# "A builder decides." (no noun before the determiner) never matches.
_REDUCED = re.compile(
    r"\b[a-z]{3,}\s+(?:a|an|the|its|their|your|our|his|her)\s+[a-z]+\s+"
    r"(?:" + _LATE_VERBS + r")\b\s*[.,;:]")


def verb_problems(body):
    flat = re.sub(r"\s+", " ", body)
    return ["LATE-VERB     '" + m.group(0).strip() + "' — the verb lands last. "
            "Keep the pronoun (\"software THAT copes\") or split it into two "
            "plain sentences." for m in _REDUCED.finditer(flat)]


# ── the author's margin as a work queue (Michel, 2026-08-06) ─────────────
# "I will use notes in lab for you to improve the content." So a __*.notes.md
# written in the lab is not just private — it is a TO-DO list addressed to
# whoever works on the course next. This pass reads them and prints the open
# items, so they appear in the Course audit log on every push and nobody has to
# run a script to see them.
#
# Notes never FAIL the audit. They are requests, not defects: failing on them
# would make the gate red for the whole time a request is open, and a gate
# that is permanently red stops meaning anything.
def read_notes(course_dir):
    open_items, done, files = [], 0, []
    for path in sorted(glob.glob(os.path.join(course_dir, "**", "__*.md"),
                                 recursive=True)):
        rel = os.path.relpath(path, course_dir)
        text = open(path).read()
        hits = re.findall(r"^\s*[-*]\s+\[( |x|X)\]\s+(.+)$", text, re.M)
        if not hits:
            # a note with prose but no checkboxes still deserves to be seen
            body = [l.strip() for l in text.split("\n")
                    if l.strip() and not l.lstrip().startswith("#")]
            if body:
                files.append((rel, None))
                open_items.append((rel, body[0][:100]))
            continue
        files.append((rel, len(hits)))
        for mark, item in hits:
            if mark == " ":
                open_items.append((rel, item.strip()[:100]))
            else:
                done += 1
    return open_items, done, files


def print_notes(course_dir):
    open_items, done, files = read_notes(course_dir)
    if not files:
        return
    print("\n── the author's margin ──")
    for rel, n in files:
        print(f"   {rel}" + (f"  ({n} item{'s' if n != 1 else ''})" if n else ""))
    if open_items:
        print(f"\n   {len(open_items)} OPEN for whoever works on this next:")
        for rel, item in open_items:
            print(f"     [ ] {item}   ({rel})")
    if done:
        print(f"\n   {done} already ticked.")
    if not open_items:
        print("\n   nothing open.")


def bench_targets(course_dir):
    """Every file a lesson SAVES, resolved to a repo path.

    course.yml is publish metadata and lists no pages, so there is no manifest
    to diff against. There is something better: a bench artifact is, by
    definition, whatever some page's save="…" names. Collect those and the
    detection is exact rather than a guess about file naming.
    """
    out = set()
    for path in glob.glob(os.path.join(course_dir, "*", "*.md")):
        folder = os.path.dirname(path)
        for m in re.finditer(r'\bsave="([^"]+)"', open(path).read()):
            rel = m.group(1)
            if rel.startswith("/"):
                out.add(os.path.normpath(os.path.join(course_dir, rel.lstrip("/"))))
            else:
                out.add(os.path.normpath(os.path.join(folder, rel)))
    return out


def main():
    course = sys.argv[1] if len(sys.argv) > 1 else "courses/micro_build_ai"
    bench = bench_targets(course)
    bad = 0

    for path in sorted(glob.glob(os.path.join(course, "*", "*.md"))):
        rel = os.path.relpath(path, course)
        base = os.path.basename(path)
        if base.startswith("_"):
            continue                      # an author's private file, by convention
        text = open(path).read()
        problems = check_page(path, text)

        if base.endswith(".notes.md"):
            problems.append(
                "LEGACY-MARGIN a margin must be DUNDER-prefixed now "
                "(__x.notes.md, not _x.notes.md): a single underscore only "
                "hides it from the folder's cards, it never stopped a publish. "
                "Rename it or delete it — the engine reads the old name as a "
                "fallback, so nothing is lost either way.")

        if os.path.normpath(path) in bench:
            problems.append(
                "BENCH-FILE    a lesson SAVES this path, so this copy is the "
                "AUTHOR's own bench output — it publishes to students and shows "
                "as a card in the folder. Delete it (git history keeps it), or "
                "rename it with a leading _.")

        if problems:
            bad += 1
            print(f"\n{rel}")
            for p in problems:
                print(f"  x {p}")
        else:
            print(f"{rel}  ok")

    print(f"\n{bad} page(s) with problems")
    print_notes(course)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
