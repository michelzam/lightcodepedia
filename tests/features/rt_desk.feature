Feature: The fire page's acts — two wired desks, three points, gated rewards
  Module 01's fire story, act by act: two agents read the two résumé pads
  through expression wires (bound="{=cv1.source}"), three in-situ checks
  each earn a point (and a celebration on their first green), and the
  reinforcement quiz after each act hides until its check passes. The AI
  is stubbed; the deterministic audit arithmetic is what's under test.

  Scenario: Red everywhere, then rung by rung to four greens
    Given I have a clean browser page
    And a builder key is connected
    And the model desk answers with verdicts "2/8" then "7/8"
    And the GitHub contents API serves "courses/demo/module_01/north.md" with the document:
      """
      # Fire page

      ```markdown
      my resume v1
      ```
      {: .mdpad #cv1 rows="4" }

      ```yaml
      system: Review this resume.
      ```
      {: .agent #desk_one bound="{=cv1.source}" rows="3" }

      ```markdown
      (write version two here)
      ```
      {: .mdpad #cv2 rows="4" }

      ```yaml
      system: Review this resume.
      ```
      {: .agent #desk_two bound="{=cv2.source}" rows="3" }

      ```gherkin
      Feature: You can run an agent
        Scenario: The desk has answered you
          Given the desk by the door
          :::python
          self.desk = self.page.desk_one
          :::
          When I look at what it said
          Then it has answered at least once
          :::python
          assert len(self.desk.replies) >= 1, "the desk hasn't spoken yet"
          :::
      ```
      {: .feature #run_check visible="true" status="pending" celebration="true" }

      ```gherkin
      Feature: The desk's sheet is yours now
        Scenario: You replaced the three-word sheet
          Given the desk by the door
          :::python
          self.desk = self.page.desk_one
          :::
          When I read its instruction sheet
          Then it is no longer three words, and it demands the line
          :::python
          assert self.desk.system.strip() != "Review this resume.", "old sheet"
          assert len(self.desk.system) >= 60, "too short"
          assert "VERDICT" in self.desk.system.upper(), "no format"
          :::
      ```
      {: .feature #brief_check visible="true" status="pending" celebration="true" }

      Reward one unlocked.
      {: visible="= brief_check.passing" }

      ```gherkin
      Feature: A second version exists
        Scenario: v2 is real
          Given both pads
          :::python
          self.a = self.page.cv1.source.strip()
          self.b = self.page.cv2.source.strip()
          :::
          When I compare them
          Then version two exists and differs
          :::python
          assert self.b and "write version two here" not in self.b, "empty"
          assert self.b != self.a, "same"
          :::
      ```
      {: .feature #ship_check visible="true" status="pending" celebration="true" }

      ```gherkin
      Feature: The tuned desks agree you improved
        Scenario: Desk two's verdict beats desk one's
          Given each desk's latest verdict
          :::python
          def _verdict(replies):
              v = None
              for r in replies:
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
                          v = int(num)
              return v
          self.v1 = _verdict(self.page.desk_one.replies)
          self.v2 = _verdict(self.page.desk_two.replies)
          :::
          When I compare them
          Then the second outscores the first
          :::python
          assert self.v1 is not None, "no verdict from desk one"
          assert self.v2 is not None, "no verdict from desk two"
          assert self.v2 > self.v1, (self.v1, self.v2)
          :::
      ```
      {: .feature #verdict_check visible="true" status="pending" celebration="true" }
      """
    When I navigate to "/run.html#src=gh:acme/demo/courses/demo/module_01/north.md"
    And I wait for the page to be interactive
    And I connect the "desk_one" agent with key "test-key"
    Then the text "Reward one unlocked" is hidden
    When I run the page's embedded features
    Then the embedded feature ends red
    When I ask the "desk_one" agent "review it"
    And I brief the "desk_one" desk with "You are the shelter's volunteer coordinator. Judge against our eight criteria, be direct and specific, and end with one line: VERDICT: n/8."
    And I brief the "desk_two" desk with "You are the shelter's volunteer coordinator. Judge against our eight criteria, be direct and specific, and end with one line: VERDICT: n/8."
    And I retype the pad "cv2" with:
      """
      # Jordan Rivera — version two

      Better in every bold and bullet.
      """
    And I ask the "desk_two" agent "review it"
    And I run the page's embedded features
    Then every embedded feature passes
    And the text "Reward one unlocked" becomes visible
    And a confetti burst appears

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
    And I connect the "desk" agent with key "test-key"
    And I ask the desk agent into the void "hello desk"
    Then the desk blames the road, not the badge

  Scenario: A key saved at the join door opens every desk connected
    The energy key persists like the course key — saved once (step five,
    or any desk), every page after opens straight at the ask box. The old
    per-page re-pasting was the actual risk: learners give up.

    Given I have a clean browser page
    And a marked shim is preinstalled
    And a saved energy key "AIza-stub" for provider "gemini"
    And the GitHub contents API serves "courses/demo/mod/desk2.md" with the document:
      """
      # Desk

      ```yaml
      system: Review.
      ```
      {: .agent #desk rows="3" }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/desk2.md"
    And I wait for the page to be interactive
    Then the desk is already connected

  Scenario: Forgetting the key on one desk forgets it on the device
    Given I have a clean browser page
    And a marked shim is preinstalled
    And a saved energy key "AIza-stub" for provider "gemini"
    And the GitHub contents API serves "courses/demo/mod/desk2.md" with the document:
      """
      # Desk

      ```yaml
      system: Review.
      ```
      {: .agent #desk rows="3" }
      """
    When I navigate to "/run.html#src=gh:acme/demo-vault/courses/demo/mod/desk2.md"
    And I wait for the page to be interactive
    And I press the desk's forget-key button
    Then the saved energy key for "gemini" is gone
