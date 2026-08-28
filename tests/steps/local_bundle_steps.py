"""Lightcode Local: the bundle must never offer doors it cannot answer."""
import glob
import os

from behave import then

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@then("the bundler's landing page bakes the local crumb")
def step_bundle_crumb(context):
    src = open(os.path.join(ROOT, "tools", "bundle_local.py")).read()
    assert "crumb=Lightcode%20Local" in src, \
        "the bundle's index.html redirect lost its crumb — the site menu will 404"


@then('each local app declares the "{crumb}" crumb')
def step_apps_declare(context, crumb):
    apps = glob.glob(os.path.join(ROOT, "local", "apps", "*.md"))
    assert apps, "no local apps found"
    for p in apps:
        t = open(p).read()
        assert '.frame' in t and 'crumb="%s"' % crumb in t, \
            "%s does not declare the local frame — its topbar offers 404 doors" % os.path.basename(p)
