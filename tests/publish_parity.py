#!/usr/bin/env python3
"""A feature that SHIPS may not lean on a step that stays home.

The lab publishes tests/ to pedia, minus the lab-only pieces listed in
.github/rsync-excludes/tests.txt — the classroom and shelf suites, whose pages
(/lab/…) exist only here. Pedia's free full run is the authority, so a
published feature using a step defined in an excluded module is not a bug that
shows up locally: it is green in the lab and red in pedia, with the useless
message "<unknown>".

That happened on 2026-08-13: frame_scope.feature (published) borrowed
"I am signed in with my face already cached" from material_steps.py
(lab-only). This check would have caught it before the publish.

Run: python3 tests/publish_parity.py
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDES = os.path.join(ROOT, ".github", "rsync-excludes", "tests.txt")
FEATURES = os.path.join(ROOT, "tests", "features")
STEPS = os.path.join(ROOT, "tests", "steps")

# @given("...") / @when('...') / @then("..."), the phrase as behave sees it
DECOR = re.compile(r"^@(?:given|when|then)\(\s*(['\"])(.+?)\1\s*\)", re.M)
# a step line in a feature file, minus its keyword
STEP_LINE = re.compile(r"^\s*(?:Given|When|Then|And|But)\s+(.*?)\s*$", re.M)
# {placeholders} become a wildcard so parametrised steps still match
PLACEHOLDER = re.compile(r"\{[^}]*\}")


def excluded_names():
    """The lab's own exclude list. It does NOT travel — publish.yml copies
    .github/workflows/, not .github/rsync-excludes/ — so in pedia there is
    no list to read, and nothing to check: the excluded files are already
    absent there. Missing list = nothing to say, not a failure (2026-08-13:
    this check red-lit pedia's whole suite before the browser even started)."""
    if not os.path.isfile(EXCLUDES):
        return None
    names = set()
    with open(EXCLUDES) as fh:
        for line in fh:
            line = line.strip()
            if line and not line.startswith("#"):
                names.add(line)
    return names


def phrases(path):
    with open(path, encoding="utf-8") as fh:
        return [m.group(2) for m in DECOR.finditer(fh.read())]


def as_pattern(phrase):
    return re.compile("^" + PLACEHOLDER.sub(".+?", re.escape(phrase)
                                            .replace(r"\{", "{").replace(r"\}", "}")) + "$")


def lab_only_travellers(excluded):
    """A feature that drives a /lab/ page cannot run in pedia — the page is
    not there. Every scenario in it fails with a 404 nobody reads as a
    missing exclusion: 17 of the 75 reds on 2026-09-02 were classroom4 and
    the triptych, green in the lab all along. The exclude list is the fix,
    and this is what notices when a new suite forgets it.
    """
    out = []
    for name in sorted(os.listdir(FEATURES)):
        if not name.endswith(".feature") or name in excluded:
            continue
        with open(os.path.join(FEATURES, name), encoding="utf-8") as fh:
            if '"/lab/' in fh.read():
                out.append(name)
    return out


def main():
    excluded = excluded_names()
    if excluded is None:
        print("publish parity: no exclude list here — this check belongs to the lab")
        return 0
    home_only = {}                       # phrase → module that defines it
    for name in sorted(os.listdir(STEPS)):
        if name.endswith(".py") and name in excluded:
            for p in phrases(os.path.join(STEPS, name)):
                home_only[p] = name
    patterns = [(as_pattern(p), p, mod) for p, mod in home_only.items()]

    problems = []
    for name in sorted(os.listdir(FEATURES)):
        if not name.endswith(".feature") or name in excluded:
            continue          # a lab-only feature may use lab-only steps
        with open(os.path.join(FEATURES, name), encoding="utf-8") as fh:
            text = fh.read()
        for used in STEP_LINE.findall(text):
            for pat, phrase, mod in patterns:
                if pat.match(used):
                    problems.append((name, used, mod))

    for feature, used, mod in problems:
        print("%s uses \"%s\" — defined in %s, which never reaches pedia"
              % (feature, used, mod))
    travellers = lab_only_travellers(excluded)
    for name in travellers:
        print("%s drives a /lab/ page — pedia has none, so every scenario in "
              "it fails there. List it (and its steps) in tests.txt." % name)

    if problems:
        print("\n%d published step(s) with no definition in pedia. "
              "Move the step to a module that ships (e.g. common_steps.py)."
              % len(problems))
    if problems or travellers:
        return 1
    print("publish parity: every published feature's steps ship with it, "
          "and no lab-only page is tested abroad")
    return 0


if __name__ == "__main__":
    sys.exit(main())
