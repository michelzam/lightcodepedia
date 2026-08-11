from behave import then
from playwright.sync_api import expect

EF_TIMEOUT = 15_000


def _flow(context, fid):
    return context.page.locator(f".lc-event-flow#{fid}")


@then('the event flow "{fid}" shows {count:d} steps')
def step_ef_count(context, fid, count):
    expect(_flow(context, fid).locator(".lc-ef-step")).to_have_count(
        count, timeout=EF_TIMEOUT
    )


@then('the event flow "{fid}" step {n:d} is a "{kind}" note')
def step_ef_kind(context, fid, n, kind):
    chip = _flow(context, fid).locator(".lc-ef-step").nth(n - 1)
    expect(chip).to_have_attribute("data-kind", kind, timeout=EF_TIMEOUT)


@then('the event flow "{fid}" shows its legend')
def step_ef_legend(context, fid):
    expect(_flow(context, fid).locator(".lc-ef-legend")).to_be_visible(
        timeout=EF_TIMEOUT
    )


@then('the event flow legend mentions "{word}"')
def step_ef_legend_word(context, word):
    expect(context.page.locator(".lc-ef-legend").first).to_contain_text(
        word, timeout=EF_TIMEOUT
    )


from behave import when


@when("a mermaid fence is injected the way the runner renders one")
def step_inject_mermaid(context):
    context.page.evaluate(
        """() => {
            const host = document.createElement('div');
            host.id = 'mermaid-bdd';
            /* exactly what marked emits for a ```mermaid fence */
            host.innerHTML = '<pre><code class="language-mermaid">flowchart LR\\n  a --> b</code></pre>';
            document.querySelector('.markdown-body').appendChild(host);
            window.lcScanElement(host);
        }"""
    )


@then("the injected fence becomes a diagram")
def step_mermaid_upgraded(context):
    host = context.page.locator("#mermaid-bdd")
    expect(host.locator(".mermaid")).to_have_count(1, timeout=EF_TIMEOUT)
    expect(host.locator("code.language-mermaid")).to_have_count(0)
