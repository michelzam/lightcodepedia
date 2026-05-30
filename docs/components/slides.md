# 📽️ Slides

Any page on this site can be presented as slides — no source markup, no front matter, no `<div>`. Just click the 📽️ button at the bottom-left of any page (including this one) and watch the same markdown repaint as a deck.

Press 📽️ now to try it on this page.

## How it works

The viewer reads your already-rendered markdown and partitions it on `## h2` boundaries. Everything between two `## h2` headings becomes one slide. The first slide is everything before the first `## h2` (typically the `# h1` title plus any intro prose).

- The markdown source stays unchanged.
- The same page reads fine top-to-bottom in scrolly mode.
- The same page presents as a deck in slide mode.

## Fragments

Bullets auto-reveal one click at a time. You're reading bullets right now — in slide mode they'd start dim and brighten as you click.

- This is the first bullet of this slide.
- This is the second; it appears on the next click.
- Bullets are the natural unit of "click to reveal more."

If you want a paragraph to fragment instead of a bullet, tag it with kramdown's `{: .fragment }` — that's the only new syntax, and it's still pure markdown:

> A sentence that should appear on its own click.
{: .fragment }

If you want a list to **not** auto-fragment, tag the list with `{: .nofragments }`. Useful for reference lists where all items should be visible at once.

## Live widgets work inside slides

The unfair advantage over a real PowerPoint: your interactive widgets stay live inside the deck. You can present code, edit it on stage, and run it without ever leaving slide view.

```python
name = "world"
print(f"Hello, {name}!")
```
{: .run rows="3" }

Hit ▶ Run from inside the slide.

## Navigation

- `→` / `Space` / click anywhere → next fragment (or next slide)
- `←` → previous
- `1`-`9` → jump to slide N
- `F` → toggle fullscreen
- `Esc` → exit slide mode (back to scrolly)

The URL gets `?slides` appended on entry, so a slide-mode link is shareable. Open any page with `?slides` in the URL and it auto-starts in deck mode.

## When the button is hidden

The 📽️ button hides itself on:

- Pages with no `## h2` heading (nothing to slide-break)
- The 404 page
- Pages set with `no_slides: true` in front matter
- Embed mode (`?embed=true`)

## Limits worth knowing

- One presenter machine at a time. There's no shared-cursor / lockstep across viewers — clicking advances *your* view of the page.
- Slide order follows source order. No reordering, no hiding slides per audience.
- Speaker notes aren't a thing yet. If you want them, ask.

{% include backtotop.md %}
