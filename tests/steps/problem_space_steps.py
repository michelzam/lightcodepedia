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


@then('the pitch "{cid}" shows {n:d} lines')
def step_pitch_lines(context, cid, n):
    lines = _card(context, "pitch", cid).locator(".lc-pitch-line")
    expect(lines).to_have_count(n, timeout=15_000)


@then('the pitch line "{field}" of "{cid}" reads "{text}"')
def step_pitch_line_reads(context, cid, field, text):
    line = _card(context, "pitch", cid).locator(f'.lc-pitch-line[data-field="{field}"]')
    expect(line).to_contain_text(text, timeout=15_000)


@then('the drift warning on "{cid}" names words from the card')
def step_warn_names_words(context, cid):
    warn = _card(context, "pitch", cid).locator(".lc-pitch-warn")
    expect(warn).to_contain_text("words on the card:", timeout=PS_TIMEOUT)


def _editor_bar(context, cid):
    """the save bar of the form that edits document cid"""
    card = _card(context, "persona", cid)
    src = card.get_attribute("data-bind")
    return context.page.locator(f".lc-form[data-lc-id='{src}'] .lc-ps-savebar")


@when('I start over from the lesson\'s starter for "{cid}"')
def step_start_over(context, cid):
    context.page.once("dialog", lambda d: d.accept())
    btn = _editor_bar(context, cid).locator(".lc-ps-reset")
    expect(btn).to_be_visible(timeout=PS_TIMEOUT)
    btn.click()
    context.page.wait_for_timeout(500)


@then('the editor of "{cid}" carries a versions handle')
def step_versions_handle(context, cid):
    expect(_editor_bar(context, cid).locator(".lc-ver-btn")).to_be_attached(timeout=PS_TIMEOUT)


@then('the page reads "{text}"')
def step_page_reads(context, text):
    expect(context.page.locator("body")).to_contain_text(text, timeout=30_000)


@when('I follow the impact map "{cid}" leaf to "{ref}"')
def step_follow_leaf(context, cid, ref):
    leaf = _card(context, "imap", cid).locator(f'.lc-imap-what a[href="#{ref}"]')
    expect(leaf).to_be_visible(timeout=PS_TIMEOUT)
    leaf.click()
    context.page.wait_for_timeout(900)


@then('the page\'s address still names "{path}"')
def step_address_names(context, path):
    assert path in context.page.evaluate("() => location.hash"), context.page.url


@then('the proof "{fid}" is in view')
def step_proof_in_view(context, fid):
    ok = context.page.evaluate("""(fid) => {
      const el = document.querySelector('[data-lc-id="' + fid + '"]') || document.getElementById(fid);
      if (!el) return "missing";
      const r = el.getBoundingClientRect();
      return (r.top < innerHeight && r.bottom > 0) ? "ok" : "off " + Math.round(r.top);
    }""", fid)
    assert ok == "ok", ok


@then('the agent "{aid}" is named "{name}" and reads "{expr}"')
def step_agent_named_bound(context, aid, name, expr):
    panel = context.page.locator(f".lc-agent[data-lc-id='{aid}'], .lc-agent#{aid}, [data-lc-id='{aid}'] .lc-agent").first
    expect(panel.locator(".lc-agent-title")).to_have_text(name, timeout=PS_TIMEOUT)
    expect(panel.locator(".lc-agent-bound")).to_contain_text(expr)


@then('the impact map "{cid}" leaf "{ref}" reads "{text}"')
def step_leaf_reads(context, cid, ref, text):
    leaf = _card(context, "imap", cid).locator(f'.lc-imap-what a[data-feature="{ref}"]')
    expect(leaf).to_have_text(text, timeout=PS_TIMEOUT)


@then('the feature "{fid}" is wanted, with no run button')
def step_feature_wanted(context, fid):
    card = context.page.locator(f'.lc-feature[data-lc-id="{fid}"]')
    expect(card).to_have_attribute("data-status", "wanted", timeout=PS_TIMEOUT)
    expect(card.locator(".lc-feature-badge")).to_have_text("wanted")
    assert card.locator(".lc-feature-run").count() == 0, "a wanted feature offers nothing to run"


@then('the impact map "{cid}" does not collect "{ref}"')
def step_imap_not_collects(context, cid, ref):
    context.page.wait_for_timeout(1500)
    found = _card(context, "imap", cid).locator(f'.lc-imap-found a[href="#{ref}"]')
    assert found.count() == 0, "the map listed a lesson check as an app feature"


@given("the editor's grid library arrives late")
def step_ag_grid_late(context):
    """The live site's order of arrival, made deterministic: AG Grid (the
    editor form's library) lands 2.5 s after everything else, so a document
    card is wired before its source form has published. A sandbox serving AG
    from disk (AG_GRID_DIR) keeps doing so, only late; CI lets the CDN answer
    after the pause. The pause pumps Playwright's loop, so nothing else waits."""
    import os
    ag_dir = os.environ.get("AG_GRID_DIR") or ""
    path = os.path.join(ag_dir, "dist", "ag-grid-community.min.js") if ag_dir else ""
    body = open(path, "rb").read() if path and os.path.isfile(path) else None

    def late(route):
        context.page.wait_for_timeout(2500)
        if body is not None:
            route.fulfill(status=200, body=body,
                          content_type="application/javascript; charset=utf-8")
        else:
            route.continue_()

    context.page.route(
        "https://cdn.jsdelivr.net/npm/ag-grid-community@*/dist/ag-grid-community.min.js",
        late)


@then('the impact map "{cid}" shows "{a}" and "{b}"')
def step_imap_shows(context, cid, a, b):
    card = _card(context, "imap", cid)
    for want in (a, b):
        expect(card).to_contain_text(want, timeout=PS_TIMEOUT)


@then('the impact map "{cid}" says "{text}" under the leaf')
def step_imap_info(context, cid, text):
    info = _card(context, "imap", cid).locator(".lc-imap-what .lc-imap-info")
    expect(info).to_contain_text(text, timeout=PS_TIMEOUT)
