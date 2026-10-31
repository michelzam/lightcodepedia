# 🎯 Impact map

The tree that makes features earn their place: goal → who → how (the
behaviour change) → what (the feature). Features come last — each one
must trace back to the goal.

```yaml
goal: More dogs go home, and no adoption fails after payment
who: The shelter coordinator
impacts:
  - how: She stops payments that come before a visit
    feature: visit_first
  - how: She sees each week where families stop
    what: The count table
    feature: weekly_proof
```
{: .impact_map #shelter_map pitch="map_pitch" }

The first leaf typed no `what`: it names a feature, and the leaf's name is
the card's title, calculated — the glyph after it is the card's state. 📝
wanted, 🔧 implemented, 🟢 proven, 🔴 failing, ⚪ not on this page. Every
leaf is a 🦄, the feature's icon, and reads as words: a leaf whose card is
elsewhere shows its id with spaces and a capital (`no_payment_before_visit`
→ *No payment before visit*), and a click on it says, under the leaf, that
the feature is written on another page.

```gherkin
Feature: Families meet the dog before they pay
  As the shelter's coordinator
  I want no family to pay before they have met the dog
  So that no adoption fails after payment

  Scenario: Paying before any visit
    Given a family that has chosen Biscuit
    And nobody has booked a visit yet
    When the family offers to pay
    Then the shelter does not take the payment
```
{: .feature #visit_first visible="true" status="wanted" tags="app" }

## Knobs

| knob | meaning |
|---|---|
| `#id` | the map's id (default `impact_map`) |
| `valuated="true"` · `estimated="true"` | show each leaf's `value` (with `value_why`) and `effort` (with `effort_why`) — quiet otherwise |
| `pitch="id"` | pulls `goal`/`who` from that pitch when your YAML leaves them empty; chip + x-ray wire |
| `feature:` (row field) | the id of a `.feature` card — the leaf links to it, takes its title when `what` is empty, and wears its state (📝 wanted · 🔧 implemented · 🟢 proven · 🔴 failing · ⚪ elsewhere) |

## A target on each leaf

A leaf may say what it bets on — a **measurable hypothesis** that moves a
metric: *in 30 minutes*, *for $20*, *twice a week*. Write it under
`target:`; the leaf shows it with a 🎯.

```yaml
goal: More dogs go home
impacts:
  - how: Families book a visit before they pay
    what: The gate
    target: no payment refunded after a visit, within a month
```
{: .impact_map #target_map }

## Worth and cost on the leaves

A leaf may carry what a stakeholder says it is **worth** (`value`, 0 to
1, with `value_why`) and what a builder says it **costs** (`effort`, in
Fibonacci points, with `effort_why`). The fields stay quiet until the map
is asked to show them: `valuated="true"` shows the worth, `estimated="true"`
the cost.

```yaml
goal: No family pays before meeting the dog
impacts:
  - how: She stops payments that come before a visit
    what: The gate
    value: 0.9
    value_why: every failed adoption costs a refund and a dog
    effort: 3
    effort_why: one rule on the payment form
  - how: She sees each week where families stop
    what: The count table
    value: 0.6
    value_why: helps her call the right families
    effort: 2
    effort_why: a query and a grid
```
{: .impact_map #valued_map valuated="true" estimated="true" }

## Facts the map stands on

A map may list the **facts** it stands on — what an expert, a survey or
the market said — under `facts:`. They show under the tree, and the
agents and proofs of the page read them with the rest of the map.

```yaml
goal: More dogs go home
facts:
  - Most failed adoptions start with a payment before any visit
  - Coordinators spend Tuesday mornings on the phone with families
impacts:
  - how: She stops payments that come before a visit
    what: The gate
```
{: .impact_map #facts_map }

## The map reads the pitch

With `goal` and `who` omitted, the map fills them from the pitch it
references — benefit becomes the goal, who stays who.

```yaml
impacts:
  - how: She stops payments that come before a visit
    what: The gate
```
{: .impact_map #pulled_map pitch="map_pitch" }

```yaml
who: shelter coordinators
need: must stop payments that come before a visit
product: Shelter Desk
category: adoption tracker
benefit: no family pays before meeting the dog
alternative: the paper binder
difference: enforces the order of the three steps
```
{: .pitch #map_pitch }

## The map collects the page's app features

A feature tagged `app` that no map row references is listed under the map
with its live status — a feature that exists but has not yet earned its
place on the map is exactly what an author should notice. The lesson's
own checks (any other tag) are never listed: the course checks the
learner, the app's features check the app.

```gherkin
Feature: The week's count stays honest
  Scenario: Counting the reservations
    Given the week's reservations
    :::python
    self.rows: list = [1, 2, 3]
    :::
    Then the count matches
    :::python
    assert len(self.rows) == 3
    :::
```
{: .feature #weekly_proof status="pending" visible="true" tags="app" }

## Proof

```gherkin
Feature: The map traces features to the goal
  Scenario: Four levels render
    Given the shelter's map
    :::python
    self.map: ImpactMap = self.page.shelter_map
    :::
    Then the goal, the person and both behaviours show
    :::python
    assert "no adoption fails" in self.map.text
    assert "coordinator" in self.map.text
    assert "where families stop" in self.map.text
    :::

  Scenario: An empty goal fills itself from the pitch
    Given the pulled map
    :::python
    self.map: ImpactMap = self.page.pulled_map
    :::
    Then it carries the pitch's benefit as its goal
    :::python
    assert "no family pays" in self.map.text
    :::

  Scenario: A leaf reads its feature
    Given the shelter's map
    :::python
    self.features: list = self.page.shelter_map.features
    :::
    Then the first leaf is the wanted feature, by its own title
    :::python
    assert self.features[0].exists, "the leaf names a card that is not here"
    assert self.features[0].wanted, "the first feature should still be wanted"
    assert "app" in self.features[0].tags
    assert "meet the dog" in self.features[0].title
    :::
```
{: .feature #impact_map_proof tags="lifecycle" visible="true" status="passing" }
