# 🪗 Accordion

Collapsible sections — each one a `<details>` panel that opens and closes on click. Perfect for FAQs, long reference material, or anything you want learners to discover at their own pace.

**This page is the tutorial.** Click 📽️ at the bottom-left to enter slide mode.

## 👀 See it in action

```
### 🐍 What is Python?
Python is a high-level, general-purpose programming language known for its readable syntax. Used for web, data science, AI, scripting, and more.

### 🤔 Do I need to install anything?
No — this site runs Python directly in your browser using WebAssembly. Nothing to install, nothing to configure.

### 🏁 How do I get started?
Go to the [🐍 Run](/components/run) page, edit the code, and hit ▶ Run. That's the whole setup.
```
{: .accordion }

Click each section to open it. Click again to close.

> Ask learners: "What kind of content belongs in an accordion?"
> Good answers: FAQs, step-by-step instructions, reference tables you don't want to scroll past.
{: .speaker-note }

**Q:** Two accordion sections are open at the same time. Is that allowed?

- [x] Yes — each `<details>` is independent; any number can be open.
- [ ] No — opening one closes the others (like a real accordion instrument).
- [ ] Only if you add `multi="true"` to the IAL.
- [ ] Only the first section can be open. The rest are decorative.
{: .quiz }

## 🛠️ How to make one

Write a plain fenced block (no language tag), use `### Heading` to start each section, then add `{: .accordion }` on the very next line:

````markdown
```
### ❓ First question
Answer goes here. Full **markdown** works — bullets, links, `code`.

### ❓ Second question
Another answer.
```
{: .accordion }
````

**Q:** You write `## Heading` instead of `### Heading` inside the fenced block. What happens?

- [ ] A bigger heading appears inside the accordion panel.
- [x] That section is ignored — only `### ` (h3) acts as the section separator.
- [ ] The whole accordion fails silently.
- [ ] It becomes the accordion's outer title, not a panel.
{: .quiz }

## 🔧 No extra knobs

Accordion has no extra IAL attributes — the structure comes entirely from `### ` headings and body content. Full markdown is supported in every panel body: bullets, tables, `code`, bold, links, even [🐍 Run](/components/run) runners.

## ⚠️ Limits worth knowing

- **No exclusive mode** (one-open-at-a-time). Each panel is a native `<details>` element — open/close is handled by the browser with no JS.
- **Same format as Tabs and Radio.** Accordion, tabs, and radio all use the same `### ` fenced-block source. Swap the IAL class to switch widget type with no other changes.

## 🏁 Final exam

**Q:** Which of these are TRUE about the accordion? (Pick all that apply.)

- [x] `### ` headings inside the fenced block become panel labels.
- [x] Multiple panels can be open simultaneously.
- [ ] You need `multi="true"` to allow more than one open panel.
- [x] Full markdown works inside each panel body.
- [x] Swapping `{: .accordion }` to `{: .tabs }` gives the same content as tabs.
{: .quiz multi="true" }

{% include backtotop.md %}
