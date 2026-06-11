# 🎠 Carousel

Auto-rotating content panels — perfect for rotating quotes, tips, or testimonials. Items fade in one at a time; dots let you jump to any item.

**This page is the tutorial.** Click 📽️ at the bottom-left to enter slide mode.

## 👀 See it in action

- 💬 Working on this showed me how visual elements make learning clearer.
- 💬 The progression from visual exploration to executable models supports authentic learning.
- 💬 Lightcodepedia bridges professional software practices with approachable education.
- 💬 Very relevant and timely.
{: .carousel }

Watch the dot advance every 4 seconds. Click a dot to jump. That's the whole widget.

> Ask: "When would you use a carousel vs a bullet list?"
> Good answers: testimonials where you want one voice at a time, rotating tips that
> would overwhelm if shown all at once, a "quote of the day" style slot.
{: .speaker-note }

**Q:** A visitor is reading item 2. The carousel auto-advances. Where do they end up?

- [ ] Back to item 1 — it loops to the beginning.
- [x] Item 3 — it advances forward, wrapping around after the last item.
- [ ] It stops — auto-advance only runs once.
- [ ] Item 2 again — the visitor's reading pauses the timer.
{: .quiz }

## 🛠️ How to make one

Write a bullet list, then add `{: .carousel }` on the very next line:

```markdown
- First rotating item.
- Second rotating item.
- Third rotating item.
{: .carousel }
```

Each `- bullet` becomes one carousel slide. Items support inline markdown — **bold**, *italic*, `code`, [links](#) — all work inside the list items.

**Q:** You want 5 rotating tips. How many lines of markup do you need beyond the bullets?

- [ ] Five — one `{: .carousel }` per item.
- [ ] Two — an opening tag and a closing tag.
- [x] One — `{: .carousel }` on the line right after the last bullet.
- [ ] Zero — lists auto-carousel when they have more than 3 items.
{: .quiz }

## 🔧 Knobs

| Attribute | Default | What it does |
|---|---|---|
| `delay="N"` | `4000` | Milliseconds between auto-advances |
| `id="…"` | auto | Required when more than one carousel lives on the same page |

A slower carousel — one slide every 8 seconds:

- 🐢 Slow rotation gives readers time to actually finish a sentence.
- 🦥 Eight seconds feels long when you're watching it. It's fine for readers.
- ⏰ Use `delay="8000"` for longer quotes. Use `delay="2000"` for quick tips.
{: .carousel delay="8000" id="slow_demo" }

Two carousels need distinct ids:

```markdown
- Item A1.
- Item A2.
{: .carousel id="quotes" }

- Item B1.
- Item B2.
{: .carousel id="tips" delay="6000" }
```

**Q:** You have two carousels on the same page but the second one's dots control the first one too. What's missing?

- [ ] `class="isolated"` on the second carousel.
- [x] A distinct `id=` on each `{: .carousel }` — required when more than one lives on a page.
- [ ] Separate `<section>` wrappers around each carousel.
- [ ] Nothing is missing. Shared dots are a known feature.
{: .quiz }

## 🏁 Final exam — boss level

**Q:** Which of these are TRUE about the carousel? (Pick all that apply.)

- [x] Each `- bullet` becomes one rotating slide.
- [x] Inline markdown (bold, links, code) works inside items.
- [ ] `delay=` is in seconds — `delay="4"` means 4 seconds.
- [x] Without an `id=`, two carousels on the same page will conflict.
- [ ] Items must be plain text — no markdown inside bullets.
{: .quiz multi="true" }

**Q:** You want the quote "**Learning is not a spectator sport.**" (bold) to rotate with two others. How do you write it?

- [ ] `- Learning is not a spectator sport.` — markdown doesn't render inside carousels.
- [x] `- **Learning is not a spectator sport.**` — inline markdown works in list items.
- [ ] `- <b>Learning is not a spectator sport.</b>` — HTML tags required for bold.
- [ ] Bold isn't possible. Write it in all-caps for emphasis.
{: .quiz }
