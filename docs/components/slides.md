# 📽️ Slides

Any page on this site can be presented as a slide deck — no source markup, no front matter, no `<div>`. The same markdown reads scrolly by default and presents as slides on demand.

**This page is the tutorial.** Click 📽️ at the bottom-left to enter slide mode, then press → (or click) to advance. The page walks you through how slides work, one slide at a time.

## Why a slide mode?

Two readers, one source.

- Students at home read the page scrolly, at their own pace.
- The same page projects cleanly as a deck for an in-class walkthrough.
- You write the markdown once. The viewer decides scroll vs. deck.
- No duplicate "presentation" file to keep in sync.

## How to start presenting

Three ways in.

- Tap **📽️ Present** at the bottom-left of any page.
- Append `?slides` to the URL — auto-starts in deck mode (shareable).
- Set a "Present" link from a syllabus that points to `your-page?slides`.

Press **Esc** to exit back to scrolly view. The URL drops `?slides` automatically.

## What becomes a slide?

The split is purely structural — no special marker required.

- Each `## h2` heading starts a new slide.
- Everything before the first `## h2` (your `# h1` plus any intro prose) is **slide 1**.
- Slides include every block until the next `## h2` — paragraphs, lists, code, widgets, tables.

So a normal lesson with five `## h2` sections becomes a six-slide deck (intro + five sections), automatically.

## Bullets become fragments

Bullets are the natural unit of "click to reveal more."

- This bullet appears first.
- This one comes on your next click.
- And this one after that.
- A bullet that ends a thought is the perfect fragment.

You don't write anything special — every `<li>` in a list auto-fragments when presented.

## Fragmenting prose

When you want a paragraph to fragment on its own, use the kramdown IAL `{: .fragment }`. It's pure markdown, still no HTML:

A normal paragraph above this one shows immediately.

> A reveal-on-click paragraph below.
{: .fragment }

That's the only new syntax you ever need to learn. And it's still optional — bullets cover 90 % of cases.

## Opting a list out

Sometimes a list is reference material — a glossary, a table of contents, a cheat sheet — and you want every item visible at once.

Tag the list with `{: .nofragments }`:

- All three items
- show together
- with no fragmenting
{: .nofragments }

## Live widgets stay live

The unfair advantage over PowerPoint: your `.run`, `.datagrid`, and `.form` widgets keep working inside slides. Click into them without advancing the deck.

```python
name = "world"
print(f"Hello, {name}!")
```
{: .run rows="3" }

Edit the code, hit ▶ Run, see output — all inside slide view. Then click outside the runner to advance.

## Navigation cheat sheet

On desktop:

- `→` / `Space` / click right half → next fragment or slide
- `←` / click left half → back
- `1`–`9` → jump to slide N
- `Q` → 📷 share QR (see below)
- `F` → toggle fullscreen
- `Esc` → exit slide mode

On phone:

- The bottom-center toolbar has **◀ / picker / ▶ / 📷**.
- The picker is iOS's native wheel — tap a slide name to jump.
- Tap the left half of the slide for prev, right half for next.

## Share with QR — classroom-friendly join

Tap **📷** (or press `Q`) and a big QR code fills the screen. Students point their phones at the code; their phones land on the **same slide you're showing**. The QR re-encodes itself on every slide change, so latecomers don't get teleported to slide 1 — they join wherever you actually are.

The URL the QR encodes is just the current page with `?slides=N` (N = current slide, 0-indexed). Anyone with that URL gets the deck starting at slide N — no backend, no real-time sync needed for a classroom projector setup. Each student then navigates at their own pace from there.

## Design tips — what works in both modes

A bullet list pulls double duty: a study note for the reader AND a fragment beat for the presenter. To get both, follow three rules.

- **One idea per bullet.** Short enough to read at a glance, complete enough to stand alone.
- **Five bullets max per slide.** If you need more, split into two `## h2` sections.
- **No deep nesting.** Nested lists fragment too, which gets confusing fast. Flatten when you can.
- **Code blocks live alone.** Put a runner on its own slide; don't bury it under five bullets.
- **Don't write "slide 3 of 5" in the prose.** The slide numbers come from structure; if you reorder sections, you don't want to renumber sentences.

## Common pitfalls

These bite first-time deck authors.

- Forgetting that `# h1` is your **title card**, not slide 2. Lead with the lesson title and a one-sentence hook.
- Stuffing a whole lecture into one `## h2`. If you're scrolling inside a slide in deck mode, that's a sign to split.
- Using `### h3` to break thoughts within a slide — `### h3` isn't a slide break (only `## h2` is). Use a paragraph or a bullet.
- Auto-fragmenting a 20-item list. Tag it `{: .nofragments }` or break it across slides.

## When the button hides

The 📽️ button hides itself on:

- Pages with no `## h2` heading (nothing to slide-break).
- The 404 page.
- Pages set with `no_slides: true` in front matter (per-page opt-out).
- Embed mode (`?embed=true`).

## Your turn — design a 3-slide tutorial

Open any lesson you've written. In your head, answer:

- What's the `# h1` title and one-sentence hook?
- What are the 2–3 `## h2` sections you'd want as slide breaks?
- Which bullets reveal one at a time vs. all-at-once?
- Is there a runner that deserves its own slide?

If your existing page already answers those four questions, you have a deck — no changes needed. Click 📽️ and present it. If not, the cleanup is the lesson plan you'd have written anyway.

## Limits worth knowing

- No shared cursor across viewers — clicking advances *your* view.
- Slide order follows source order. No per-audience reorder.
- No speaker notes yet. Ask if you want them.

{% include backtotop.md %}
