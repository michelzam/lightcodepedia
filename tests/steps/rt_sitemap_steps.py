import json

from behave import given, then

# The course map's edges carry meaning: containment (the folder tree, drawn
# from paths alone) versus prerequisite (a constraint across it). These steps
# stub a small course tree through the git-trees + contents API the runner
# render uses, then count the edge classes the map actually painted.


@given('the course tree contains "{paths}"')
def step_course_tree(context, paths):
    context.lc_tree = [p.strip() for p in paths.split(",") if p.strip()]
    context.lc_extra = getattr(context, "lc_extra", {})

    tree = {"tree": [{"path": p, "type": "blob"} for p in context.lc_tree]}
    context.page.route(
        "**/api.github.com/repos/**/git/trees/**",
        lambda r: r.fulfill(status=200, content_type="application/json",
                            body=json.dumps(tree)))

    def serve(route):
        url = route.request.url
        path = url.split("/contents/")[-1].split("?")[0]
        title = path.rsplit("/", 1)[-1].replace(".md", "").title()
        body = "# " + title + "\n\nA page.\n"
        if path == context.lc_tree[0]:
            # the root index carries the map itself, with the default path
            body += '\n[Browse](.)\n{: .sitemap height="360" }\n'
        body += context.lc_extra.get(path, "")
        route.fulfill(status=200, content_type="text/plain", body=body)

    context.page.route("**/api.github.com/repos/**/contents/**", serve)
    context.page.route("**/raw.githubusercontent.com/**", serve)


@given('"{path}" requires "{target}"')
def step_page_requires(context, path, target):
    context.lc_extra = getattr(context, "lc_extra", {})
    context.lc_extra[path] = "\n- [Before this](%s)\n{: .prerequisite }\n" % target


def _edge_count(page, kind):
    return page.evaluate(
        "(k) => document.querySelectorAll('.lc-sm-edge-' + k).length", kind)


@then('the map draws {n:d} "{kind}" edges')
def step_edge_count(context, n, kind):
    context.page.wait_for_function(
        "([k, n]) => document.querySelectorAll('.lc-sm-edge-' + k).length === n",
        arg=[kind, n], timeout=20_000)


@then("the prerequisite edge is dashed and lighter than the tree")
def step_prereq_style(context):
    style = context.page.evaluate(
        """() => {
            const p = document.querySelector('.lc-sm-edge-prereq');
            const t = document.querySelector('.lc-sm-edge-tree');
            const cs = getComputedStyle(p), ct = getComputedStyle(t);
            return { dash: cs.strokeDasharray, op: parseFloat(cs.opacity),
                     tdash: ct.strokeDasharray, top: parseFloat(ct.opacity) };
        }"""
    )
    assert style["dash"] and style["dash"] != "none", style
    assert not style["tdash"] or style["tdash"] == "none", style
    assert style["op"] < style["top"], style


@then("the map explains its arrows")
def step_legend(context):
    legend = context.page.locator(".lc-sm-legend")
    legend.wait_for(state="visible", timeout=10_000)
    text = legend.inner_text().lower()
    assert "contains" in text and "first" in text, text
