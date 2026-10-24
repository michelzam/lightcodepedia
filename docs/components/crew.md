# 🧑‍🤝‍🧑 Crew

A **crew** is a few agents working one inbox together. The agents are the
**rows of a dataset**; one line runs them, with its **bounds** said out
loud: how many tries per message, how many AI asks in total, and where
what stays open goes. Add a row and the crew has one more member; the loop,
the checks and the budget stay inside the component.

**This page is the tutorial**: press **▶ Run** below; − and + on its
bounds change the tries and the budget, and the gauge shows the budget
spent. Without an AI key on
this device, Sid sorts alone and the rest stays `OPEN`; with one, Rey reads
and Chuck checks. The crew is the desk's **concierge**: it takes every
message, hands it to the right worker, and answers for the result.

## 👀 Try it now

```csv
family,dog,stage,message
Nguyen,Biscuit,asked,We would like to visit Biscuit on Saturday
Okafor,Biscuit,met,How do I pay the adoption fee?
Ferraro,Biscuit,asked,We already met Biscuit last week. Can we pay now?
```
{: .dataset #inbox }

```csv
name,kind,system,checked_by
Sid,rules,sort,
Rey,reader,"Read one family message: which stage should the family move to next? Answer one line — VERDICT: met if they want to visit or see the dog, home if they want to pay or adopt, asked if they want neither and only need an answer. If a checker disagreed, follow its reason.",Chuck
Chuck,checker,"You check a verdict against the message's row. A family moves one stage at a time: asked, then met, then home — and stays where it is only when it wants neither a visit nor to pay. Answer AGREE or DISAGREE, then why, in one line.",
```
{: .dataset #members }

```python
def sort(message):
    m = message.lower()
    if "already" in m:
        return None            # a claim to check: not for the rules
    if "visit" in m:
        return "met"           # a visit: they meet the dog
    if "pay" in m or "fee" in m:
        return "home"          # the fee: the dog goes home
    return None
```
{: .model }

[The front desk](#)
{: .crew members="members" inbox="inbox" stages="asked, met, home" tries="2" budget="6" costs="1, 30, 900" #desk }

```
### 🧑‍🤝‍🧑 The crew — who does the job
[the workers](#)
{: .datagrid source="members" columns="name, kind, system, checked_by" #crew_grid }

[one worker](#)
{: .form master="crew_grid" #crew_form }
```
{: .accordion }

[The messages — each family's stage, and the next one the desk gives it](#)
{: .datagrid source="desk.sorted" columns="family, dog, stage, message, next_stage, why, tries, asks, tokens" #desk_stages }

💰 **The desk's cost: {= desk.cost }** {= desk.vs_last } = 🐍 {= desk.runs } rule runs × 1 + 🤖 {= desk.asks } AI asks × 30 + 🧑 {= desk.open } left `OPEN` for a person × 900

```
### 🎏 The run, as an event flow
[the run](#)
{: .event_flow source="desk.flow" #desk_flow }

### 📜 Every step — who said what, and what it cost
[the log](#)
{: .datagrid source="desk.log" columns="n, who, kind, out, tokens" #desk_log height="220" }
```
{: .accordion }

A family moves from **stage** to stage, as in the
[follow-up list](/components/model): `asked`, then `met`, then `home`. Each
message's row says where its family is (`stage`); the desk gives it where it
goes (`next_stage`). Ferraro asks to pay, but the row says `asked`: no visit
yet, and a family moves one stage at a time, so the next stage is `met`.
The `why` column says who decided, or what stopped the desk; what it could
not settle stays `OPEN`, so an undecided message never reads as a decision.
The event flow tells the same run beat by beat: each ⚡ a message moving to
its next stage, with what it cost and how sure it is — ✅ a rule or a
check said so, ⚠️ unchecked or left open.

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
| `stages` | the stages a message can move its family to, comma-separated |
| `tries` | at most this many reads per message (default 2) — a read and its check, two asks — − and + on the crew change it |
| `budget` | at most this many AI asks in total (default 6) — − and +, and a gauge of what the run spent |
| `fallback` | the stage written for what stays open (default `OPEN`) — a person, never a guess |
| `costs` | the price of a 🐍 rule run, a 🤖 AI ask and a 🧑 message left `OPEN` for a person (default `1, 30, 900`): `desk.cost` adds them up |
| `pace` | seconds between steps, so the work is seen a row at a time (default 0.5; 0 runs flat out) |
| `provider` · `model` · `temperature` · `max_tokens` | an [agent](/components/agent)'s own knobs: the crew **is** an agent, and these are its members' defaults (a member's own column wins; `max_tokens` 2000, as any agent — a model that thinks spends it before answering; the crew's line says it, − lowers it, + never climbs past the page's own, and an answer cut at it is marked ✂️) |

## 🧑‍🤝‍🧑 The members — one row each

| `kind` | what it does | `system` | cost |
|---|---|---|---|
| `rules` | the page's own Python function answers a stage, or `None` | the function's name | free |
| `reader` | one AI ask on the message's words; its answer must name a stage | its instructions | one ask |
| `checker` | one AI ask on a reader's verdict, with the message's whole row: `AGREE` or `DISAGREE`, and why | its instructions | one ask |
| `rules`, named in a reader's `checked_by` | a **Python check** instead: its function gets the message, the verdict and the row, returns `None` to agree or the reason it disagrees — for a rule that is exact | the function's name | free, the same answer every time |

`checked_by` wires a reader to its checker. The reader reads the words; the
checker checks them against the facts — the message's row (here, the
family's `stage`). A `reads` column names a dataset whose rows travel with
a member's ask too.

## 🔁 The loop

The stages are where a message moves its family: `met` books a visit,
`home` sends the payment link, `asked` keeps it where it is — a question a
person answers. The `why` column says who decided — Sid's rule, Chuck
agreed — or what stopped the desk: the budget spent, no agreement in its
tries, no key; then the message stays `OPEN`.

For each message: the rules first, in order. If none answers, the reader
proposes and its checker checks. Only a checker that says `AGREE` settles
it: a `DISAGREE` — or an answer with neither word, empty or cut — goes back
to the reader with the checker's words, and it tries again. It stops at `tries` for the
message or `budget` for the crew, and what is still open takes `fallback`
(`OPEN` by default).

The crew writes three datasets and touches nothing else:
- `desk.sorted`: every message from the start, then its `next_stage`, its `why`, its `tries`, its `asks` (a try is a read and its check: two asks, so the column adds up to the gauge) and its `tokens` (the row at work is selected, ⏳);
- `desk.flow`: the run as an [event flow](/components/event_flow) — `{: .event_flow source="desk.flow" }` draws it, each ⚡ a message moving to its next stage, its cost, ✅ or ⚠️;
- `desk.log`: every step, `who` said what (`in`, `out`) and its `tokens`;
- `desk.vs_last`: after a run, `= the last run` or `≠ the last run: N` — the same knobs, other AI words, another cost;
- `desk.cost`: the run's price — `desk.runs` rule runs, `desk.asks` AI asks, `desk.open` messages left for a person, each at its `costs=`: Python is the cheapest and the easiest to check, and rigid; the AI bends to any wording, at thirty times the price; a person is the most flexible and creative, and thirty times the AI. A [cell](/components/cells) under the grid shows it;
- the crew's lines — its tokens, the session's and this run's, and the engine's 🔋 asks and tokens left per day and per minute, as under every agent — and `desk.asks` · `desk.tokens` in a proof: the totals.

The crew is an [agent](/components/agent) made of agents: it has an agent's
**desk** — the 🔑 in its head opens the ring of engines, the same keys every
agent panel uses, open by itself while none is held — and when an engine
does not answer, the crew says so and marks its 🔑: the keys unfold when you press it. The members ask with **your
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
    self.stages = dict(zip(self.desk.sorted.values("family"), self.desk.sorted.values("next_stage")))
    assert self.stages["Nguyen"] == "met", self.stages
    assert self.stages["Okafor"] == "home", self.stages
    :::
    And the crew is an agent made of agents
    :::python
    assert isinstance(self.desk, Agent), "a crew is an agent"
    assert all(isinstance(m, Agent) for m in self.desk.members), "its members are agents"
    assert [m.name for m in self.desk.members] == ["Sid", "Rey", "Chuck"], [m.name for m in self.desk.members]
    :::
    And the claim was never taken for a payment, and the bounds held
    :::python
    assert self.stages["Ferraro"] != "home", "Ferraro is at asked: one stage at a time, a visit first"
    assert self.desk.asks <= self.desk.budget, f"{self.desk.asks} AI asks, the budget is {self.desk.budget}"
    :::
```
{: .feature #crew_proof visible="true" status="pending" tags="ai" }
