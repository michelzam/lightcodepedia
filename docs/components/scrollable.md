# 📜 Scrollable

Wrap long content in a fixed-height scrollable box. Good for log output, long code listings, or reference tables you want present but not page-dominating.

**This page is the tutorial.** Click 📽️ at the bottom-left to enter slide mode.

## 👀 See it in action

```
Line 1: Starting up...
Line 2: Loading modules...
Line 3: Connecting to database...
Line 4: Running migrations...
Line 5: Seeding data...
Line 6: Starting server...
Line 7: Listening on port 8080...
Line 8: First request received.
Line 9: GET / 200 OK
Line 10: GET /api/users 200 OK
Line 11: POST /api/login 200 OK
Line 12: Server running healthy.
```
{: .scrollable height="120" }

Scroll inside the box. The rest of the page stays put.

```gherkin
Feature: A fenced block becomes a fixed-height scroll box
  As a lowcoder
  I want long content kept in a scrollable box
  So that it stays present without dominating the page

  Scenario: The content is wrapped in a scrollable box
    Given the scrollable block above
    :::python
    self.box = Object._all(".lc-scrollable")[0]
    :::
    When it has rendered
    Then it is a visible box that still holds the content
    :::python
    assert self.box.visible
    assert "Listening on port 8080" in self.box.text, self.box.text[:80]
    :::
```
{: .feature tags="ui" status="passing" }

## 🛠️ How to make one

Put content in a plain fenced block, then add `{: .scrollable height="N" }`:

````markdown
```
Long content here...
Many more lines...
```
{: .scrollable height="150" }
````

`height=` is in pixels — the box never grows taller, and scrolls when content overflows.

## 🔧 Knobs

| Attribute | Default | What it does |
|---|---|---|
| `height="N"` | `300` | Maximum height in pixels before scrolling kicks in |

**Q:** You set `height="100"` but your content is only 2 lines. Does a scrollbar appear?

- [ ] Yes — the box is always exactly 100 px with a scrollbar.
- [x] No — the box shrinks to fit; scrolling only appears when content overflows.
- [ ] It depends on the browser.
- [ ] A 100 px empty grey box appears regardless.
{: .quiz }

## ⚠️ Limits

- **Plain text only** in the current upgrade — content renders inside `<pre>`. For scrollable rich markdown, use a raw `<div style="max-height:Npx;overflow-y:auto;">` HTML block (kramdown passes it through).
- **No syntax highlighting** — use `{: .code }` for highlighted code blocks.

## 🏁 Final exam

**Q:** You have a 50-line server log to show without it dominating the page. Which is right?

- [ ] Accordion — hide it by default.
- [x] `{: .scrollable height="200" }` on a fenced block.
- [ ] `{: .code }` — it scrolls automatically.
- [ ] Paginate it. Never put more than 10 lines on a page.
{: .quiz }
