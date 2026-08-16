Feature: Reel mode — Instagram-style vertical snap between titles

  Reuses the per-H2 .lc-slide sections the slides engine already builds. With
  reel mode on, the page becomes a full-viewport vertical scroll-snap
  container, one title per snap. ?reel=1 auto-enters; Esc / the FAB exits.

  Background:
    Given I have a clean browser page

  Scenario: ?reel=1 enters reel mode with a snap container
    When I navigate to "/tutorial101?reel=1"
    And I wait for the page to be interactive
    Then the page is in reel mode
    And the content is a vertical scroll-snap container
    And the reel shows a sticky title bar

  Scenario: Reel mode can be exited
    When I navigate to "/tutorial101?reel=1"
    And I wait for the page to be interactive
    Then the page is in reel mode
    When I exit reel mode
    Then the page is not in reel mode

  Scenario: Browser Back exits reel mode
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I enter reel mode
    Then the page is in reel mode
    When I press the browser back button
    Then the page is not in reel mode

  Scenario: The reel bar has a visible Back control
    When I navigate to "/tutorial101"
    And I wait for the page to be interactive
    And I enter reel mode
    Then the page is in reel mode
    When I click the reel back button
    Then the page is not in reel mode

  Scenario: The reel title is the title, not everything hung inside it
    A page's tags are painted as pills INSIDE its h1, so reading that
    heading raw gave the bar "Adoption Dayappuidatafeature" (Michel,
    2026-08-14). A title is what the author wrote.

    When I navigate to "/components/block?reel=1"
    And I wait for the page to be interactive
    Then the page is in reel mode
    And the page's title carries tag pills
    And the reel bar shows the title without the pills
    And the section picker shows titles without the pills

  Scenario: Left and right page the sections — arrows, chevrons, and swipe agree
    Double navigation (Michel, 2026-08-16): horizontal is the COARSE axis.
    ←/→, the « » in the bar, and a horizontal swipe all mean "next/previous
    ## section" — one grammar, three inputs.

    When I navigate to "/components/block?reel=1"
    And I wait for the page to be interactive
    Then the page is in reel mode
    And the reel is at section 1
    When I press the right arrow
    Then the reel is at section 2
    When I press the left arrow
    Then the reel is at section 1
    When I click the next-section chevron
    Then the reel is at section 2
    When I swipe right-to-left on neutral ground
    Then the reel is at section 3
    When I swipe left-to-right on neutral ground
    Then the reel is at section 2

  Scenario: Down and up arrows page by BLOCK, landing whole ideas under the bar
    Vertical is the FINE axis: the next key lands the next whole top-level
    block — never mid-paragraph. Within a long section the counter must NOT
    move; the reader is still inside the same idea.

    When I navigate to "/components/block?reel=1"
    And I wait for the page to be interactive
    Then the page is in reel mode
    When I press the down arrow
    Then the reel scrolled to align a block under the bar
    And the reel is at section 1
    When I press the up arrow
    Then the reel is back at the top

  Scenario: A vertical flick pages one block; a slow drag reads freely
    Velocity is the intent CSS cannot read (Michel, 2026-08-16: "Flick").
    Fast at release = exactly one block lands under the bar. Slow at
    release = a reading drag — the reel does nothing, and no block is a
    CSS snap point anymore, so fine reading has zero speed bumps.

    When I navigate to "/components/block?reel=1"
    And I wait for the page to be interactive
    Then the page is in reel mode
    And blocks are not CSS snap points
    When I flick upward on neutral ground
    Then the reel scrolled to align a block under the bar
    And the reel is at section 1
    When I drag slowly on neutral ground
    Then the reel did not move

  Scenario: A swipe over an interactive surface belongs to the surface
    A horizontal drag over a grid scrolls the table, over a canvas it pans
    a map — those gestures are the widget's. The reel takes swipes only on
    neutral ground.

    When I navigate to "/components/block?reel=1"
    And I wait for the page to be interactive
    Then the page is in reel mode
    And the reel is at section 1
    When I swipe right-to-left over a guarded surface
    Then the reel is at section 1

  Scenario: The bar names the section in view, on one line
    When I navigate to "/components/block?reel=1"
    And I wait for the page to be interactive
    Then the page is in reel mode
    When I press the right arrow
    Then the reel bar title is the current section's heading
