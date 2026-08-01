Feature: The desk audit — tune an agent, prove the tuning with three points
  Module 01's fire story: a badly-briefed desk agent, a learner who rewrites
  its briefing, a résumé v2, and a three-scenario audit. The AI's judgment
  is stochastic; the points are deterministic — the audit compares the seed
  briefing, the two pads, and the VERDICT lines the learner's own prompt
  forced the model to emit.

  Scenario: The audit goes from red to three green points
    Given I have a clean browser page
    And a builder key is connected
    And the model desk answers with verdicts "2/8" then "7/8"
    And the GitHub contents API serves "courses/demo/module_01/north.md" with the document:
      """
      # Fire page

      ```yaml
      system: Review this resume.
      ```
      {: .agent #desk rows="3" }

      ```markdown
      my resume v1
      ```
      {: .mdpad #cv1 rows="4" }

      ```markdown
      (write version two here)
      ```
      {: .mdpad #cv2 rows="4" }

      ```gherkin
      Feature: The desk works for you now
        Scenario: You rewrote the prompt
          Given the desk agent
          :::python
          self.desk = self.page.desk
          :::
          When I check its briefing
          Then it is your own and demands a verdict line
          :::python
          assert self.desk.system.strip() != "Review this resume.", "seed prompt"
          assert len(self.desk.system) >= 60, "too short"
          assert "VERDICT" in self.desk.system.upper(), "no verdict demand"
          :::

        Scenario: You shipped a second version
          Given both pads
          :::python
          self.a = self.page.cv1.source.strip()
          self.b = self.page.cv2.source.strip()
          :::
          When I compare them
          Then version two exists and differs
          :::python
          assert self.b and "write version two here" not in self.b, "empty v2"
          assert self.b != self.a, "same as v1"
          :::

        Scenario: The machine you tuned says v2 is better
          Given every verdict this sitting
          :::python
          self.verdicts = []
          for r in self.page.desk.replies:
              up = r.upper()
              i = up.find("VERDICT")
              if i >= 0:
                  num = ""
                  for ch in up[i:i + 30]:
                      if ch.isdigit():
                          num += ch
                      elif num:
                          break
                  if num:
                      self.verdicts.append(int(num))
          :::
          When I read the first and the last
          Then the last outscores the first
          :::python
          assert len(self.verdicts) >= 2, self.verdicts
          assert self.verdicts[-1] > self.verdicts[0], self.verdicts
          :::
      ```
      {: .feature #audit visible="true" status="pending" tags="north-burns" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_01/north.md"
    And I wait for the page to be interactive
    And I run the page's embedded features
    Then the embedded feature ends red
    When I brief the desk agent with "You are the shelter's volunteer coordinator. Judge against our eight criteria, be direct and specific, and end with one line: VERDICT: n/8."
    And I ask the desk agent "my resume v1"
    And I ask the desk agent "my resume v2 with everything fixed"
    And I retype the pad "cv2" with:
      """
      # Jordan Rivera — version two

      Better in every bold and bullet.
      """
    And I run the page's embedded features
    Then every embedded feature passes

  Scenario: A blocked road names itself — not the learner's token
    'Network error: Load failed' taught nothing; a learner reads it as a
    broken key. When the fetch is refused before any HTTP answer, the desk
    must blame the road (ad-blocker, VPN, firewall) and say a bad token
    would sound different.

    Given I have a clean browser page
    And a builder key is connected
    And the model desk is unreachable
    And the GitHub contents API serves "courses/demo/module_01/road.md" with the document:
      """
      # Road page

      ```yaml
      system: Review this resume.
      ```
      {: .agent #desk rows="3" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_01/road.md"
    And I wait for the page to be interactive
    And I ask the desk agent into the void "hello desk"
    Then the desk blames the road, not the badge
