Feature: The résumé rubric — acceptance criteria grade what the learner types
  Module 01's volunteer story seeds an mdpad with a wall-of-text CV and grades
  it with a red-first .feature. The rubric reads the pad's PREVIEW — titles,
  sections, bolds, bullets, links, images, plus this_year() for the date —
  so the criteria fail honestly on the wall and pass only on a structured,
  dated, humble page. This proves the whole self-grading loop end to end.

  Scenario: Red on the wall of text, green on the crafted page
    Given I have a clean browser page
    And the GitHub contents API serves "courses/demo/module_01/volunteer.md" with the document:
      """
      # The Volunteer

      ```markdown
      hi im a volunteer i guess. i am a real expert in computers and stuff.
      ```
      {: .mdpad #cv rows="8" }

      ```gherkin
      Feature: A resume that gets the volunteer through the door
        Scenario: Structure, mission, future, contact, humility
          Given the resume in the pad
          :::python
          self.cv = self.page.cv
          :::
          When I check it
          Then all eleven criteria hold
          :::python
          assert len(self.cv.titles) == 1, self.cv.titles
          assert len(self.cv.sections) >= 3, self.cv.sections
          assert "volunteer" in " ".join(self.cv.bolds).lower(), self.cv.bolds
          assert len(self.cv.italics) >= 1, self.cv.italics
          assert len(self.cv.bullets) >= 4, self.cv.bullets
          assert len(self.cv.numbered) >= 2, self.cv.numbered
          heads = [l.strip().split(".", 1)[0] for l in self.cv.source.split("\n")]
          assert "2" not in heads, "lazy-number every rank as 1."
          words = self.cv.rendered.replace(",", " ").replace(".", " ").split()
          years = [int(w) for w in words if len(w) == 4 and w.isdigit()]
          assert years and max(years) > this_year(), years
          assert len(self.cv.links) >= 1, self.cv.links
          assert self.cv.images >= 1, self.cv.images
          assert "expert" not in self.cv.rendered.lower(), "humble words"
          :::
      ```
      {: .feature #rubric visible="true" status="pending" tags="volunteer" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_01/volunteer.md"
    And I wait for the page to be interactive
    And I run the page's embedded features
    Then the embedded feature ends red
    When I retype the pad with:
      """
      # Jordan Rivera

      **Volunteer** builder for the shelter, writing *from the future* — 2999.

      ## Mission

      I help the shelter cope with data, apps and AI.

      ## Future skills

      - I wire forms, grids and charts so numbers explain themselves
      - I ask a page questions in SQL and watch it answer
      - I write the acceptance criteria before I build the thing
      - I repair data problems where they live, in the values

      ## Preferred pets

      1. Dogs, obviously
      1. Cats, when they allow it

      ## Reach me

      [write to me](https://example.org/jordan)

      ![a portrait](https://example.org/jordan.png)
      """
    And I run the page's embedded features
    Then every embedded feature passes

  Scenario: An engine gap speaks like a person, never like a traceback
    A site can serve an older runtime than the course page expects (the
    engine deploys through a publish, the content renders fresh from git).
    That mismatch is never the learner's fault — the step must say so,
    instead of leaking 'Mdpad object has no attribute …' at them.

    Given I have a clean browser page
    And the GitHub contents API serves "courses/demo/module_01/skew.md" with the document:
      """
      # Skew page

      ```markdown
      seed
      ```
      {: .mdpad #pad rows="4" }

      ```gherkin
      Feature: Engine skew is not the learner's fault
        Scenario: A step asks for vocabulary this engine lacks
          Given the pad
          :::python
          self.page.pad.vocabulary_from_the_future
          :::
      ```
      {: .feature #skew visible="true" status="pending" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_01/skew.md"
    And I wait for the page to be interactive
    And I run the page's embedded features
    Then the embedded feature ends red
    And the step error blames the engine, not the learner
