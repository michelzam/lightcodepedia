---
title: Seam
---

# 〰️ Seam

A page speaks in registers — the course talking, the app the reader acts in,
the course's own tools — and a beginner cannot infer a frame nobody gave
them. The seam is that frame: markdown's own `---`, with a name on it.

```markdown
---
{: .seam .blue label="The app starts here" }
```

---
{: .seam .blue label="The app starts here" }

Everything under that line belongs to the app. The mark is a **statement**,
not a container: it opens a region, and the next seam or the next heading
ends it. Nothing to nest, nothing to close.

---
{: .seam .amber label="A course tool" }

A checker, a 💾, a ▶ Run — scaffolding a shipped app would never carry. The
seam says so before the reader wonders.

---
{: .seam .muted label="Back to the lesson" }

## 🎛️ Knobs

| Knob | Meaning |
|---|---|
| `label` | **required** — the border itself. Three approved wordings, and no others: *The app starts here* · *A course tool* · *Back to the lesson* |
| `.red` `.green` `.blue` `.amber` `.muted` | optional tint, reusing the colour words the engine already has. Decoration only |
{: .wide_first }

## 📐 Why the label, and not the colour

Red already means something loud in a course: a failing check, a bomb on a
broken wire. A border that leans on colour says two things at once — and
says nothing at all in print, to a screen reader, or to the one reader in
twelve who cannot separate red from green. So the label carries the meaning
and the tint is decoration. `course_audit.py` enforces both: a seam with no
label, or with a fourth wording, is a page that fails its check.

The value of a border is that it is the **same** border on page 40 as on
page 2. That is worth more than the freedom to phrase it prettily.

```gherkin
Feature: A border markdown already had
  As a beginner reading a page that mixes lesson, app and tools
  I want to see where each one starts
  So that I never wonder whether I am supposed to fix the checker

  Scenario: The rule becomes a labelled seam
    Given the seam above this feature
    :::python
    self.seam: Object = Object._all(".lc-seam")[0]
    :::
    When the page has rendered
    Then it carries its label as readable text
    :::python
    self.text: str = self.seam._text()
    assert "app starts here" in self.text.lower(), self.text
    :::
    And the rule itself is still a rule
    :::python
    n: int = len(Object._all(".lc-seam hr"))
    assert n >= 3, f"{n} seam rules found"
    :::
```
{: .feature #seam_proof tags="ui" status="passing" }

[in this folder](.)
{: .folder parent="true" }
