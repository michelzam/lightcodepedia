# 🧑‍🤝‍🧑 Crew

A **crew** is a few agents working one inbox together. The agents are the
**rows of a dataset**; one line runs them, with its **bounds** said out
loud: how many tries a message gets, how many AI asks in all, and where
what stays open goes. Add a row and the crew has one more member; the loop,
the checks and the budget stay inside the component.

**This page is the tutorial**: press **▶ Run** below. Without an AI key on
this device, Sid sorts alone and the rest stays `OPEN`; with one, Rey reads
and Chuck checks. The crew is the desk's **concierge**: it takes every
message, hands it to the right worker, and answers for the result.

## 👀 Try it now

```csv
family,message
Nguyen,We would like to visit Biscuit on Saturday
Okafor,How do I pay the adoption fee?
Ferraro,We already met Biscuit last week. Can we pay now?
```
{: .dataset #inbox }

```csv
family,dog,previous_lane
Nguyen,Biscuit,
Okafor,Biscuit,VISIT
Ferraro,Biscuit,
```
{: .dataset #families }

```csv
name,kind,system,checked_by,reads
Sid,rules,sort,,
Rey,reader,"Read one family message. Answer one line — VERDICT: VISIT, PAY or CALL.",Chuck,
Chuck,checker,"You check a verdict against the family's card: a family can PAY only when its previous_lane is VISIT. Answer AGREE or DISAGREE, then why, in one line.",,families
```
{: .dataset #members }

```python
def sort(message):
    m = message.lower()
    if "already" in m:
        return None            # a claim to check: not for the rules
    if "visit" in m:
        return "VISIT"
    if "pay" in m or "fee" in m:
        return "PAY"
    return None
```
{: .model }

[The front desk](#)
{: .crew members="members" inbox="inbox" lanes="VISIT, PAY, CALL" tries="2" budget="6" fallback="OPEN" #desk }

[The families' cards — where each family is now, what Chuck checks](#)
{: .datagrid source="families" columns="family, dog, previous_lane" #family_cards }

[The messages — and the next lane the desk gives each](#)
{: .datagrid source="desk.sorted" columns="family, message, next_lane, why, tries, tokens" #desk_lanes }

```
### 🎏 The run, as an event flow
[the run](#)
{: .event_flow source="desk.flow" #desk_flow }

### 🧑‍🤝‍🧑 The crew — who can do what
[the members](#)
{: .datagrid source="members" columns="name, kind, system, checked_by, reads" #crew_grid }

[one member](#)
{: .form master="crew_grid" #crew_form }

### 📜 Every step — who said what, and what it cost
[the log](#)
{: .datagrid source="desk.log" columns="n, who, kind, out, tokens" #desk_log height="220" }
```
{: .accordion }

A **lane** is a state: each family's card holds its `previous_lane` (where it
is now), and the desk gives each message its `next_lane` (where it goes).
Ferraro asks to pay, but the card shows no visit yet, and a family pays only
after one: the next lane is `VISIT`. The `why` column says who decided, or
what stopped the desk; what it could not settle stays `OPEN`, so an
undecided message never reads as a decision. The event flow tells the same
run beat by beat, each ⚡ a message moving to its next lane.

Each member is an **agent**, its attributes — `name`, `system`, and
`model`, `temperature`… when a column sets them — read from its row: the
agents are **data**. Pick one in the grid, the form shows it; a row more is
a member more. A crew **is** an agent too, and its `members` are a list of
agents: the composite pattern — one day a member can be a crew itself.

```yaml
script:
  - at: desk
    say: "{= members.count } members, one row each. {= members.first.name } goes first: rules are free."
stories: {}
```
{: .avatar #crew_guide dock="true" size="115" }

Meet the crew
{: .avatar_trigger target="crew_guide" }

A guide's line can read the page: `{= members.first.name }` in a `say:` is a
[cell](/components/cells), read as the line is spoken.

## 🎛️ Knobs

| Knob | Meaning |
|---|---|
| `members` | the dataset whose rows are the members: each an agent (`name`, `system`, and `provider`, `model`, `temperature`, `max_tokens` if set), wired by `kind`, `checked_by`, `reads` |
| `inbox` | the dataset to work through, one row a message |
| `text` | the inbox column that holds the message (default `message`) |
| `lanes` | the answers a message can get, comma-separated |
| `tries` | at most this many reads a message (default 2) |
| `budget` | at most this many AI asks in all (default 6) |
| `fallback` | the lane for what stays open (default `OPEN`) — a person, never a guess |
| `pace` | seconds between steps, so the work is seen a row at a time (default 0.5; 0 runs flat out) |
| `provider` · `model` · `temperature` · `max_tokens` | an [agent](/components/agent)'s own knobs: the crew **is** an agent, and these are its members' defaults (a member's own column wins) |

## 🧑‍🤝‍🧑 The members — one row each

| `kind` | what it does | `system` | cost |
|---|---|---|---|
| `rules` | the page's own Python function answers a lane, or `None` | the function's name | free |
| `reader` | one AI ask; its answer must name a lane | its instructions | one ask |
| `checker` | one AI ask on a reader's verdict: `AGREE` or `DISAGREE`, and why | its instructions | one ask |

`checked_by` wires a reader to its checker; `reads` names a dataset whose
rows travel with the ask (here, the families' cards Chuck checks).

## 🔁 The loop

The lanes are the desk's next steps: `VISIT` books a visit, `PAY` sends the
payment link, `CALL` hands the message to a person who must answer it. The
`why` column says who decided — Sid's rule, Chuck agreed — or what stopped
the desk: the budget spent, no agreement in its tries, no key; then the
message stays `OPEN`.

For each message: the rules first, in order. If none answers, the reader
proposes and its checker checks. A `DISAGREE` goes back to the reader with
the checker's words, and it tries again. It stops at `tries` for the
message or `budget` for the crew, and what is still open takes `fallback`
(`OPEN` by default).

The crew writes three datasets and touches nothing else:
- `desk.sorted`: every message from the start, then its `next_lane`, its `why`, its `tries` and its `tokens` (the row at work is selected, ⏳);
- `desk.flow`: the run as an [event flow](/components/event_flow) — `{: .event_flow source="desk.flow" }` draws it, each ⚡ a message moving to its next lane;
- `desk.log`: every step, `who` said what (`in`, `out`) and its `tokens`;
- the crew's line, and `desk.asks` · `desk.tokens` in a proof: the totals.

The crew is an [agent](/components/agent) made of agents: it has an agent's
**desk** — the 🔑 in its head opens the ring of engines, the same keys every
agent panel uses, open by itself while none is held — and when an engine
does not answer, the crew says so and opens it. The members ask with **your
own key**, as a panel does: a busy engine retried, a retired model healed.

## 🧪 Proof

```gherkin
Feature: The desk sorts the inbox within its bounds
  As the shelter's coordinator
  I want every message sorted, the AI asked only when the rules cannot tell
  So that no family waits and the bill stays small

  Scenario: Press ▶ Run on the desk, then ▶ here
    Given the desk ran over the inbox
    :::python
    self.desk = self.page.desk
    assert self.desk.done, "press ▶ Run on the desk first"
    :::
    Then the rules sorted the plain ones for free
    :::python
    self.lanes = dict(zip(self.desk.sorted.values("family"), self.desk.sorted.values("next_lane")))
    assert self.lanes["Nguyen"] == "VISIT", self.lanes
    assert self.lanes["Okafor"] == "PAY", self.lanes
    :::
    And the crew is an agent made of agents
    :::python
    assert isinstance(self.desk, Agent), "a crew is an agent"
    assert all(isinstance(m, Agent) for m in self.desk.members), "its members are agents"
    assert [m.name for m in self.desk.members] == ["Sid", "Rey", "Chuck"], [m.name for m in self.desk.members]
    :::
    And the claim was never taken for a payment, and the bounds held
    :::python
    assert self.lanes["Ferraro"] != "PAY", "Ferraro has no booked visit: not a payment"
    assert self.desk.asks <= 6, f"{self.desk.asks} AI asks, the budget is 6"
    :::
```
{: .feature #crew_proof visible="true" status="pending" tags="ai" }
