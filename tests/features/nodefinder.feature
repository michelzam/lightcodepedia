Feature: The LightNode router (404 page)

  lightcodepedia.org/@student lands on the 404 page, which routes: live fork
  site → redirect; fork without Pages → explain the switch, never a GitHub
  404; unknown name → an invitation, not a dead end.

  Background:
    Given I have a clean browser page

  Scenario: A live LightNode redirects
    Given a stubbed fork "egbas" whose site is live
    When I visit the node "@egbas"
    Then I land on the "egbas" LightNode

  Scenario: A fork without a live site explains the Pages switch
    Given a stubbed fork "egbas" whose site is not live
    When I visit the node "@egbas"
    Then the router explains the site is not switched on

  Scenario: An unknown name invites to start a LightNode
    Given a stubbed missing fork "nosuchuser"
    When I visit the node "@nosuchuser"
    Then the router invites to start a LightNode
