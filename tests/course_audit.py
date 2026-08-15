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
                              — ended up on the learners' folder page as a
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


# The three borders a course page may draw, and no others. Adding a fourth
# turns a vocabulary into decoration — decide it here, once, on purpose.
SEAM_LABELS = {"The app starts here", "A course tool", "Back to the lesson"}


def embedded_ids(path, text):
    """Ids an embedded file brings with it.

    `{: .runner src="_app_dogs.md" }` injects another file into this page, so
    `#all_dogs` can live there and still be a real anchor here — the avatar's
    `at:` finds it once the embed has rendered. Without this the app-extraction
    of 2026-08-14 red-lit three anchors that resolve perfectly at runtime.
    One level deep and same-course only: a src the audit cannot read (a gh:
    URL, a missing file) simply contributes nothing, which keeps the anchor
    check honest instead of silently permissive.
    """
    out = set()
    here = os.path.dirname(path)
    for m in re.finditer(r'\{:[^}\n]*\.runner[^}\n]*\bsrc="([^"]+)"', text):
        src = m.group(1)
        if re.match(r"^[a-z]+:|^/", src):
            continue
        try:
            sub = open(os.path.join(here, src)).read()
        except OSError:
            continue
        out |= set(re.findall(r"[#]([A-Za-z_][\w-]*)", sub))
    return out


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
    # ONE NAME, TWO SPELLINGS. A tag is an identifier the engine knows
    # (`event_flow`) but the chip renders it as words, and a lesson writes
    # words too — so `tags="event flow"` beside `[^event_flow]:` is the same
    # tag said twice, not a broken page (Michel, 2026-08-11). Match on the
    # snake_case form; report whatever the author actually typed.
    def key(x):
        return x.replace(" ", "_")

    ktags = {key(t): t for t in tags}
    kdefs = {key(d): d for d in defs}
    krefs = {key(r) for r in refs}

    for k in sorted(set(kdefs) - set(ktags)):
        problems.append(f'FN-NOT-A-TAG  [^{kdefs[k]}] is not a tag on this page. '
                        f"Footnotes are for tags only — make it prose, or an "
                        f"inline link if it is a source.")
    for k in sorted(set(kdefs) - krefs):
        problems.append(f"ORPHAN-DEF    [^{kdefs[k]}] defined, never referenced")
    for k in sorted(krefs - set(kdefs)):
        problems.append(f"DANGLING-REF  [^{k}] referenced, never defined")
    for k in sorted(set(ktags) - set(kdefs)):
        problems.append(f'TAG-NO-DEF    tag "{ktags[k]}" has no footnote')
    for k, pos in sorted(refs.items()):
        if all(in_fence(p, spans) for p in pos):
            problems.append(f"REF-IN-FENCE  [^{k}] only referenced inside a fence")

    body = text
    for a, b in reversed(spans):
        body = body[:a] + " " * (b - a) + body[b:]
    # A TAG IS AN IDENTIFIER; PROSE IS FOR PEOPLE. Same rule as above, on
    # the sentence side: `event flow` and `event_flow` are one word.
    spoken = {key(m.group(1)) for m in re.finditer(r"`([^`\n]+)`", body)}
    for t in sorted(tags):
        if key(t) not in spoken:
            problems.append(f'TAG-NO-PROSE  tag "{t}" is never used in backticked prose')

    problems.extend(verb_problems(body))

    for i, m in enumerate(re.finditer(r"^```dot\n(.*?)^```", text, re.S | re.M)):
        p = subprocess.run(["dot", "-Tsvg"], input=m.group(1),
                           capture_output=True, text=True)
        if p.returncode != 0:
            problems.append(f"DOT-FAIL      block {i + 1}: {p.stderr.strip()[:110]}")

    problems.extend(hint_problems(text))

    m = re.search(r"^```yaml\n(bot:.*?)^```", text, re.S | re.M)
    if m:
        block = m.group(1)
        if yaml:
            try:
                yaml.safe_load(block)
            except Exception as e:
                problems.append(f"AVATAR-YAML   {str(e)[:110]}")
        ids = set(re.findall(r"[#]([A-Za-z_][\w-]*)", text)) | embedded_ids(path, text)
        for a in sorted(set(re.findall(r"^\s*(?:-\s*)?at:\s*(\S+)", block, re.M))):
            missing = (a[1:] not in text) if a.startswith(".") else (a not in ids)
            if missing:
                problems.append(f'AVATAR-ANCHOR at: {a} resolves to nothing')

    # ── the borders keep one vocabulary ─────────────────────────────────
    # A seam is worth having only because it is the SAME border on page 40 as
    # on page 2 (Michel, 2026-08-13). Free text drifts — "you're in the app
    # now" by module 5 — and the mark stops meaning anything. The colour is
    # decoration; the label is the border, so the label is what is checked.
    for m in re.finditer(r"\{:[^}]*\.seam\b[^}]*\}", text):
        decl = m.group(0)
        lab = re.search(r'label="([^"]*)"', decl)
        if not lab:
            problems.append("SEAM-NO-LABEL a seam without a label is a "
                            "decoration: colour alone says nothing in print, "
                            "to a screen reader, or to a colour-blind reader")
        elif lab.group(1).strip() not in SEAM_LABELS:
            problems.append(f'SEAM-LABEL    "{lab.group(1)}" — say one of: '
                            + " · ".join(sorted(SEAM_LABELS)))
    return problems


# ── step code is documentation (Michel, 2026-08-11) ──────────────────────
# "python code, even in features, should use hints (for doc reason! at
# least)." A step block is the first Python most learners read closely, and
# it is read WITHOUT running it — so `kinds = self.flow.kinds()` says nothing
# about what comes back, while `kinds: list[str] = ...` answers the only
# question a beginner has. MicroPython parses annotations and ignores them,
# so this costs nothing at runtime.
#
# Only the FIRST binding of a name is checked — a reassignment is annotated
# once, like real Python. `self.x` counts too (Michel, 2026-08-11: *"be sure
# all variables and attributes have type hints (ex. self.btn: Button = …)"*),
# because the attribute a later step reads is exactly where a reader wants to
# know what they are holding. A class body that declares its type inside the
# call (`Attr(float, …)`) is already saying it.
_ASSIGN = re.compile(r"^\s*((?:self\.)?[a-z_][a-z_0-9]*)\s*=\s*(\S.*)$")
_DECLARED = re.compile(r"^\s*((?:self\.)?[a-z_][a-z_0-9]*)\s*:\s*[^=]+=")


def hint_problems(text):
    out, seen, inblk = [], set(), False
    for line in text.split("\n"):
        st = line.strip()
        if st == ":::python":
            inblk, seen = True, set()
            continue
        if st == ":::":
            inblk = False
            continue
        if not inblk:
            continue
        d = _DECLARED.match(line)
        if d:
            seen.add(d.group(1))
            continue
        m = _ASSIGN.match(line)
        if not m:
            continue
        name = m.group(1)
        if re.match(r"^(Attr|State)\(", m.group(2)):
            continue          # the model DSL states its type inside the call
        if name in seen:
            continue
        seen.add(name)
        out.append(f"STEP-NO-HINT  {name} = … needs a type hint "
                   f"({name}: list[str] = …) — step code is read, not run.")
    return out


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
                "AUTHOR's own bench output — it publishes to learners and shows "
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
