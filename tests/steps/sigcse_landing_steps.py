"""The temporary landing at /sigcse: steps of its own (published with it)."""
from behave import then


@then('the landing holds none of "{words}"')
def step_landing_none(context, words):
    # the page's own content: what sits beside its title, not the site's menu or footer
    text = context.page.evaluate("() => { const h = document.querySelector('h1'); return h ? h.parentElement.innerText : ''; }")
    assert "Two Probabilistic Systems" in text, "the landing's content was not found"
    found = [w.strip() for w in words.split(",") if w.strip().lower() in text.lower()]
    assert not found, "the landing still says: " + ", ".join(found)
