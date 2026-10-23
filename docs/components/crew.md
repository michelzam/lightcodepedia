# 🧑‍🤝‍🧑 Crew

A **crew** is a few agents working one inbox together. The agents are the
**rows of a dataset**; one line runs them, with its **bounds** said out
loud: how many tries a message gets, how many AI asks in all, and where
what stays open goes. Add a row and the crew has one more member; the loop,
the checks and the budget stay inside the component.

**This page is the tutorial**: press **▶ Run** below. Without an AI key on
this device, Sid sorts alone and the rest goes to `CALL`; with one, Rey reads
and Chuck checks.

## 👀 Try it now

```csv
family,message
Nguyen,We would like to visit Biscuit on Saturday
Okafor,How do I pay the adoption fee?
Ferraro,We already met Biscuit last week. Can we pay now?
```
{: .dataset #inbox }

```csv
dog,visits
Biscuit,none booked
```
{: .dataset #dogs }

```csv
name,kind,brief,checked_by,reads
Sid,rules,sort,,
Rey,reader,"Read one family message. Answer one line — VERDICT: VISIT, PAY or CALL.",Chuck,
Chuck,checker,"You check a verdict against the dog cards: a family pays only after a booked visit. Answer AGREE or DISAGREE, then why, in one line.",,dogs
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
{: .crew members="members" inbox="inbox" lanes="VISIT, PAY, CALL" tries="2" budget="6" fallback="CALL" #desk }

[Where each message went](#)
{: .datagrid source="desk.sorted" columns="family, lane, tries" #desk_lanes }

[Every step](#)
{: .datagrid source="desk.log" columns="n, who, kind, out" #desk_log height="200" }

## 🎛️ Knobs

| Knob | Meaning |
|---|---|
| `members` | the dataset whose rows are the members (`name`, `kind`, `brief`, `checked_by`, `reads`) |
| `inbox` | the dataset to work through, one row a message |
| `text` | the inbox column that holds the message (default `message`) |
| `lanes` | the answers a message can get, comma-separated |
| `tries` | at most this many reads a message (default 2) |
| `budget` | at most this many AI asks in all (default 6) |
| `fallback` | the lane for what stays open — a person, never a guess |

## 🧑‍🤝‍🧑 The members — one row each

| `kind` | what it does | `brief` | cost |
|---|---|---|---|
| `rules` | the page's own Python function answers a lane, or `None` | the function's name | free |
| `reader` | one AI ask; its answer must name a lane | its instructions | one ask |
| `checker` | one AI ask on a reader's verdict: `AGREE` or `DISAGREE`, and why | its instructions | one ask |

`checked_by` wires a reader to its checker; `reads` names a dataset whose
rows travel with the ask (here, the dog cards Chuck trusts).

## 🔁 The loop

For each message: the rules first, in order. If none answers, the reader
proposes and its checker checks. A `DISAGREE` goes back to the reader with
the checker's words, and it tries again. It stops at `tries` for the
message or `budget` for the crew, and what is still open takes `fallback`.

The crew writes two datasets and touches nothing else:
- `desk.sorted`: each message, its `lane` and its `tries`;
- `desk.log`: every step, `who` said what (`in`, `out`).

The members ask with **your own key**, the one every agent panel uses.

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
    assert self.desk.sorted.count == 3, f"{self.desk.sorted.count} of 3 messages sorted — press ▶ Run on the desk first"
    :::
    Then the rules sorted the plain ones for free
    :::python
    self.lanes = dict(zip(self.desk.sorted.values("family"), self.desk.sorted.values("lane")))
    assert self.lanes["Nguyen"] == "VISIT", self.lanes
    assert self.lanes["Okafor"] == "PAY", self.lanes
    :::
    And the claim was never taken for a payment, and the bounds held
    :::python
    assert self.lanes["Ferraro"] != "PAY", "Ferraro has no booked visit: not a payment"
    assert self.desk.asks <= 6, f"{self.desk.asks} AI asks, the budget is 6"
    :::
```
{: .feature #crew_proof }
