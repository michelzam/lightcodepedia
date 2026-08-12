# 🎯 Impact map

The tree that makes features earn their place: goal → who → how (the
behaviour change) → what (the feature). Features come last — each one
must trace back to the goal.

```yaml
goal: More dogs go home, and no adoption fails after payment
who: The shelter coordinator
impacts:
  - how: She stops payments that come before a visit
    what: The gate — card 3 waits for the visit date
  - how: She sees each week where families stop
    what: The count table
    feature: weekly_proof
```
{: .impact_map #shelter_map pitch="map_pitch" }

## Knobs

| knob | meaning |
|---|---|
| `#id` | the map's id (default `impact_map`) |
| `pitch="id"` | pulls `goal`/`who` from that pitch when your YAML leaves them empty; chip + x-ray wire |
| `feature:` (row field) | the id of a `.feature` proof — the leaf links to it |

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

## The map collects the page's proofs

A proof on the page that no map row references is listed under the map
with its live status — a feature that runs but has not yet earned its
place on the map is exactly what an author should notice.

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
{: .feature #weekly_proof status="pending" visible="true" tags="spec" }

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
```
{: .feature #impact_map_proof tags="lifecycle" visible="true" status="passing" }
