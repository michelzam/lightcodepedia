#!/usr/bin/env python3
"""Author-side integrity pass over a course. Not a behave suite — no browser.

Every check here exists because something slipped through once:

  TAG-NO-DEF / TAG-NO-PROSE   a feature tag with no footnote, or one a reader
                              never meets in prose, teaches nothing
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
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
