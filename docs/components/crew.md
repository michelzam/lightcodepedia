# 🧑‍🤝‍🧑 Crew

A **crew** is a team on one inbox: 🐍 Python functions and 🤖 AI agents side
by side, each a **row of a table**. One line runs them, with its bounds said
out loud — tries per message, AI asks in total, tokens per ask — and hands a
🧑 person whatever stays open. Every step is traced, every ask is priced.

Press **▶ Run** below. No AI key on this device? Python works alone, and the
rest stays `OPEN`.

## 👀 Try it now

```csv
family,dog,current_stage,message
Nguyen,Biscuit,asked,We would like to visit Biscuit on Saturday
Okafor,Biscuit,met,How do I pay the adoption fee?
Ferraro,Biscuit,asked,We already met Biscuit last week. Can we pay now?
```
{: .dataset #inbox }

```csv
name,kind,system,checked_by
Sid,python,sort,
Rey,ai,"Name the action this family message asks for. One line: VERDICT: meet, adopt or call. meet = they want to visit or see the dog. adopt = they want to pay or adopt. call = they only ask a question, a person calls them back. Examples: Can we visit Rex on Monday? → VERDICT: meet. How do we pay for Rex? → VERDICT: adopt. Is Rex good with cats? → VERDICT: call. If a checker disagreed, answer the action it allows.",Chuck
Chuck,ai,"Check a proposed action against the family's current_stage. meet only when it is asked; adopt only when it is met; call at any stage. Answer AGREE or DISAGREE, in one line; when you disagree, name the action the row allows.",
```
{: .dataset #members }

```python
def sort(message):
    m = message.lower()
    if "already" in m:
        return None            # a claim to check: not for the rules
    if "visit" in m:
        return "meet"          # a visit: they meet the dog
    if "pay" in m or "fee" in m:
        return "adopt"         # the fee: the dog goes home
    return None
```
{: .model }

[The front desk](#)
{: .crew members="members" inbox="inbox" actions="meet, adopt, call" tries="2" budget="6" costs="1, 30, 900" #desk }

```
### 🧑‍🤝‍🧑 The crew — who does the job
[the workers](#)
{: .datagrid source="members" columns="name, kind, system, checked_by" #crew_grid }

[one worker](#)
{: .form master="crew_grid" #crew_form }
```
{: .accordion }

[The messages — each family's current stage, and the action the desk recommends](#)
{: .datagrid source="desk.sorted" columns="family, dog, current_stage, message, action, why, tries, asks, tokens" #desk_actions }

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

Each worker is an **agent** whose attributes are its row: data, not code. A
row more, a worker more. A crew **is** an agent too, so one day a worker can
be a crew.

```yaml
script:
  - at: desk
    say: "{= members.count } members, one row each. {= members.first.name } goes first: Python is free."
stories: {}
```
{: .avatar #crew_guide dock="true" size="115" }

Meet the crew
{: .avatar_trigger target="crew_guide" }

## 🚀 What a crew opens

- **The cheapest worker first.** Python sorts what it can, free and the same
  every time; the AI gets only the rest.
- **Two agents, one check.** A reader proposes, a checker holds the facts; a
  disagreement goes back with its reason.
- **Exact rules in code.** A checker can be a Python function: free, and never
  wrong about the rule it states.
- **Bounds you can touch.** Tries, budget, tokens per ask: − and + on the crew,
  a gauge filling as the run spends.
- **A person, never a guess.** What the crew cannot settle stays `OPEN`.
- **Nothing hidden.** The run as an [event flow](/components/event_flow), every
  step in a log, the cost in a [cell](/components/cells), `=` or `≠` the last run.
- **Your keys, any engine.** The crew is an [agent](/components/agent): the
  same ring of engines, a busy one retried, a retired model healed.

## 🚧 Not yet

The AI workers are probabilistic. That is a strength — they read any wording,
and two different answers show a doubt — but it is not alignment. Today the
bounds and the checker are the only guardrails: no structured answers, no
reliability measured over many runs, no tool an agent calls by itself, no
crew of crews. Each inbox still needs its own craft: instructions, examples,
a budget tuned by hand.

## 🎛️ Knobs

| Knob | Meaning |
|---|---|
| `members` | the dataset of workers, one row each: `name`, `kind` (`python` or `ai`), `system` (a function's name, or an agent's instructions), `checked_by` |
| `inbox` | the dataset to work through, one row a message (`text=` names its column, default `message`) |
| `actions` | what the crew can answer, comma-separated |
| `tries` · `budget` | reads per message (a read and its check: two asks) · AI asks in total — − and + on the crew |
| `fallback` | the answer for what stays open (default `OPEN`): a person |
| `costs` | the price of a 🐍 run, a 🤖 ask, a 🧑 open message (default `1, 30, 900`) |
| `pace` | seconds between steps (default 0.5) |
| `provider` · `model` · `temperature` · `max_tokens` | an [agent](/components/agent)'s knobs, the workers' defaults; `max_tokens` (2000) can be lowered on the crew, never raised |

## 🧑‍🤝‍🧑 The workers

`kind` says **what** works; the wiring says the **job**:

| job | 🐍 `python` | 🤖 `ai` |
|---|---|---|
| **sort** | its function answers an action, or `None` | — |
| **read** (has a `checked_by`) | — | one ask on the words: an action |
| **check** (named in a `checked_by`) | its function gets the message, the action and the row: `None`, or its reason | one ask with the row: `AGREE` or `DISAGREE`, and why |

The crew writes only its own datasets — `desk.sorted` (each message, its
action, why, tries, asks, tokens), `desk.flow`, `desk.log` — and its totals:
`desk.cost`, `desk.runs`, `desk.asks`, `desk.open`, `desk.tokens`,
`desk.vs_last`.

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
    self.actions = dict(zip(self.desk.sorted.values("family"), self.desk.sorted.values("action")))
    assert self.actions["Nguyen"] == "meet", self.actions
    assert self.actions["Okafor"] == "adopt", self.actions
    :::
    And the crew is an agent made of agents
    :::python
    assert isinstance(self.desk, Agent), "a crew is an agent"
    assert all(isinstance(m, Agent) for m in self.desk.members), "its members are agents"
    assert [m.name for m in self.desk.members] == ["Sid", "Rey", "Chuck"], [m.name for m in self.desk.members]
    :::
    And the claim was never taken for a payment, and the bounds held
    :::python
    assert self.actions["Ferraro"] != "adopt", "Ferraro is at asked: a visit first — meet, not adopt"
    assert self.desk.asks <= self.desk.budget, f"{self.desk.asks} AI asks, the budget is {self.desk.budget}"
    :::
```
{: .feature #crew_proof visible="true" status="pending" tags="ai" }
