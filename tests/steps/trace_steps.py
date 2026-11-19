"""The paste trace (2026-11-19): what a learner typed, pasted from the page or from elsewhere,
and what the page wrote — counts and part ids only, one row of the progress record per 💾."""
import base64
import re

from behave import given, step
from playwright.sync_api import expect

LONG = "A paragraph written somewhere else entirely, long enough to count as a real paste. " * 2


def _ta(context, pid):
    ta = context.page.locator("[data-lc-id='%s'] textarea.lc-mdpad-in" % pid).first
    expect(ta).to_be_attached(timeout=20_000)
    return ta


def _paste(context, pid, text):
    """a paste as the browser delivers it: the event with its clipboard, then the text in the box"""
    _ta(context, pid)
    context.page.evaluate("""([pid, t]) => {
      const ta = document.querySelector("[data-lc-id='" + pid + "'] textarea.lc-mdpad-in");
      ta.focus(); ta.setSelectionRange(ta.value.length, ta.value.length);
      const dt = new DataTransfer(); dt.setData('text/plain', t);
      ta.dispatchEvent(new ClipboardEvent('paste', { clipboardData: dt, bubbles: true, cancelable: true }));
      ta.value += t; ta.dispatchEvent(new InputEvent('input', { bubbles: true, inputType: 'insertFromPaste' }));
    }""", [pid, text])


@step('I paste {n:d} characters from elsewhere into the pad "{pid}"')
def step_paste_elsewhere(context, n, pid):
    _paste(context, pid, (LONG * 4)[:n])


@step('I paste the lines of the code card "{cid}" into the pad "{pid}"')
def step_paste_card(context, cid, pid):
    text = context.page.evaluate("(c) => JSON.parse(document.querySelector(\"[data-lc-id='\" + c + \"']\").getAttribute('data-lc-value')).text", cid)
    context.trace_card_len = len(text)
    _paste(context, pid, text)


@step('I type "{text}" in the pad "{pid}"')
def step_type_in_pad(context, text, pid):
    ta = _ta(context, pid)
    ta.click()
    context.page.keyboard.press("End")
    context.page.keyboard.type(text)


@step('I press ⬇ Add on the code card "{cid}" for the trace')
def step_trace_add(context, cid):
    context.page.locator(".lc-code[data-lc-id='%s'] .lc-code-add" % cid).click()
    context.page.wait_for_timeout(400)


@step('I press 💾 on the pad "{pid}"')
def step_save_pad(context, pid):
    btn = context.page.locator(".lc-mdpad-save").first   # the save bar sits beside the pad, not in it
    expect(btn).to_be_enabled(timeout=20_000)
    btn.click()
    context.page.wait_for_timeout(2500)


def _trace_rows(context):
    puts = getattr(context, "bench_puts", {})
    keys = [k for k in puts if k.endswith("__progress.txt")]
    if not keys:
        return []
    body = base64.b64decode(puts[keys[-1]]["content"]).decode("utf-8")
    return [l.split("\t") for l in body.splitlines() if "\tc\t" in l]


@step('the progress record holds {n:d} trace rows')
def step_trace_count(context, n):
    rows = _trace_rows(context)
    assert len(rows) == n, "trace rows: %r" % rows


@step('the last trace row says {fields}')
def step_trace_row(context, fields):
    """fields like: typed=5 page=… ext=180 ext_n=1 applied=0 paths=~>pad:180"""
    rows = _trace_rows(context)
    assert rows, "no trace row"
    r = sorted(rows, key=lambda p: p[0])[-1]
    assert r[1] == "c" and r[2] == "1", r
    got = {"typed": r[3], "page": r[4], "ext": r[5], "ext_n": r[6], "applied": r[7], "paths": r[8] if len(r) > 8 else ""}
    for k, v in re.findall(r"(\w+)=(\S+)", fields):
        if v == "card":
            v = str(context.trace_card_len)
        v = v.replace("{card}", str(getattr(context, "trace_card_len", "")))
        assert got[k] == v, "%s is %r, not %r — row %r" % (k, got[k], v, r)
    assert "@" in r[0], "a trace row is keyed by page and time: %r" % r[0]

