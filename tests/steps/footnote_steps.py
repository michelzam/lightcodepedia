from behave import then

# Page-level footnote settlement: refs live in block fences, defs at the end
# of the file; lcFootnotesSettle merges every chunk's notes into one list and
# numbers them globally in reading order.


@then('footnote "{a}" settles as number 1 and "{b}" as number 2')
def step_footnotes_settle_pair(context, a, b):
    context.page.wait_for_function(
        """([a, b]) => {
            var ra = document.querySelector('sup[data-lcfn="' + a + '"] a');
            var rb = document.querySelector('sup[data-lcfn="' + b + '"] a');
            return ra && rb && ra.textContent === '1' && rb.textContent === '2';
        }""",
        arg=[a, b],
        timeout=10_000,
    )


@then('footnote "{a}" settles as number 1')
def step_footnote_settles_one(context, a):
    context.page.wait_for_function(
        """(a) => {
            var r = document.querySelector('sup[data-lcfn="' + a + '"] a');
            var d = document.querySelector('li[data-lcfn-def="' + a + '"]');
            return r && r.textContent === '1' && d && d.offsetParent !== null;
        }""",
        arg=a,
        timeout=10_000,
    )


@then("the page shows a single footnote list with {n:d} visible entries")
def step_single_footnote_list(context, n):
    context.page.wait_for_function(
        """(n) => {
            var lists = document.querySelectorAll('div.footnotes[data-lcfn-src]');
            if (lists.length !== 1) return false;
            var vis = Array.prototype.filter.call(
              lists[0].querySelectorAll('li'),
              function (li) { return li.offsetParent !== null; });
            return vis.length === n;
        }""",
        arg=n,
        timeout=10_000,
    )
