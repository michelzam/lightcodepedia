from behave import when, then
from playwright.sync_api import expect

# components upgrade after the platform scan; yaml parsing is async
PS_TIMEOUT = 15_000


@when('the form "{fid}" field "{key}" is set to "{value}"')
def step_form_set(context, fid, key, value):
    """The same path a human keystroke takes: lcFormSet → grid → bus."""
    context.page.wait_for_selector(
        f'.lc-form[data-lc-id="{fid}"] .ag-row', timeout=PS_TIMEOUT
    )
    ok = context.page.evaluate(
        "([f, k, v]) => window.lcFormSet(f, k, v)", [fid, key, value]
    )
    assert ok, f"lcFormSet({fid}, {key}) found no such field"


def _card(context, kind, cid):
    return context.page.locator(f".lc-{kind}#{cid}")


@then('the persona card "{cid}" shows the name "{name}"')
def step_persona_name(context, cid, name):
    expect(_card(context, "persona", cid).locator(".lc-persona-name")).to_have_text(
        name, timeout=PS_TIMEOUT
    )


@then('the persona card "{cid}" has {count:d} empathy sections')
def step_persona_empathy(context, cid, count):
    expect(_card(context, "persona", cid).locator(".lc-empathy-cell")).to_have_count(
        count, timeout=PS_TIMEOUT
    )


@then('the pitch "{cid}" reads "{snippet}"')
def step_pitch_reads(context, cid, snippet):
    expect(_card(context, "pitch", cid).locator(".lc-pitch-text")).to_contain_text(
        snippet, timeout=PS_TIMEOUT
    )


@then('the pitch "{cid}" links to the persona "{ref}"')
def step_pitch_chip(context, cid, ref):
    chip = _card(context, "pitch", cid).locator(f'.lc-pitch-chip[href="#{ref}"]')
    expect(chip).to_be_visible(timeout=PS_TIMEOUT)


@then('the pitch "{cid}" shows no drift warning')
def step_pitch_no_warn(context, cid):
    # the card must have rendered before "no warning" means anything
    expect(_card(context, "pitch", cid).locator(".lc-pitch-text")).to_be_visible(
        timeout=PS_TIMEOUT
    )
    expect(_card(context, "pitch", cid).locator(".lc-pitch-warn")).to_be_hidden()


@then('the pitch "{cid}" shows a drift warning')
def step_pitch_warn(context, cid):
    expect(_card(context, "pitch", cid).locator(".lc-pitch-warn")).to_be_visible(
        timeout=PS_TIMEOUT
    )


@then('the impact map "{cid}" shows the goal "{snippet}"')
def step_imap_goal(context, cid, snippet):
    expect(_card(context, "imap", cid).locator(".lc-imap-goal").first).to_contain_text(
        snippet, timeout=PS_TIMEOUT
    )


@then('the impact map "{cid}" has {count:d} behaviour changes')
def step_imap_hows(context, cid, count):
    hows = _card(context, "imap", cid).locator(".lc-imap-how")
    expect(hows).to_have_count(count, timeout=PS_TIMEOUT)


@then('the impact map "{cid}" links to the pitch "{ref}"')
def step_imap_chip(context, cid, ref):
    chip = _card(context, "imap", cid).locator(f'.lc-pitch-chip[href="#{ref}"]')
    expect(chip).to_be_visible(timeout=PS_TIMEOUT)


@then('the impact map "{cid}" leaf links to the proof "{ref}"')
def step_imap_leaf(context, cid, ref):
    leaf = _card(context, "imap", cid).locator(f'.lc-imap-what a[href="#{ref}"]')
    expect(leaf).to_be_visible(timeout=PS_TIMEOUT)


@then('the impact map "{cid}" collects the proof "{ref}"')
def step_imap_collects(context, cid, ref):
    found = _card(context, "imap", cid).locator(f'.lc-imap-found a[href="#{ref}"]')
    expect(found).to_be_visible(timeout=PS_TIMEOUT)


@then('the persona card "{cid}" offers to save')
def step_has_save(context, cid):
    expect(_card(context, "persona", cid).locator(".lc-ps-save")).to_be_visible(
        timeout=PS_TIMEOUT
    )


@then('the persona card "{cid}" shows no save button')
def step_no_save(context, cid):
    # the card must have rendered before "no button" means anything
    expect(_card(context, "persona", cid).locator(".lc-persona-name")).to_be_visible(
        timeout=PS_TIMEOUT
    )
    expect(_card(context, "persona", cid).locator(".lc-ps-save")).to_have_count(0)


@then('the persona card "{cid}" says nothing is saved yet')
def step_says_empty(context, cid):
    expect(_card(context, "persona", cid).locator(".lc-ps-empty")).to_be_visible(
        timeout=PS_TIMEOUT
    )


@then('the proof "{fid}" shows the tag "{label}"')
def step_tag_label(context, fid, label):
    chip = context.page.locator(f'.lc-feature[data-lc-id="{fid}"] .lc-feature-tag', has_text=label)
    expect(chip.first).to_be_visible(timeout=PS_TIMEOUT)


@then('the proof "{fid}" carries the tag name "{name}"')
def step_tag_value(context, fid, name):
    chip = context.page.locator(f'.lc-feature[data-lc-id="{fid}"] .lc-feature-tag[data-tag="{name}"]')
    expect(chip.first).to_be_attached(timeout=PS_TIMEOUT)


@then('the save button for "{cid}" sits inside the form "{fid}"')
def step_save_in_form(context, cid, fid):
    btn = context.page.locator(f'.lc-form[data-lc-id="{fid}"] .lc-ps-save')
    expect(btn).to_be_visible(timeout=PS_TIMEOUT)
    # and nowhere on the card itself
    expect(_card(context, "persona", cid).locator(".lc-ps-save")).to_have_count(0)


@then('the pitch "{cid}" shows "{field}" as calculated')
def step_calc(context, cid, field):
    expect(_card(context, "pitch", cid).locator(".lc-pitch-calc").first).to_be_visible(
        timeout=PS_TIMEOUT
    )
