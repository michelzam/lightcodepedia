import os
from playwright.sync_api import sync_playwright

BASE_URL = os.environ.get("BASE_URL", "https://lightcodepedia.org").rstrip("/")

_pw = None
_browser = None


def before_all(context):
    global _pw, _browser
    _pw = sync_playwright().start()
    _browser = _pw.chromium.launch(headless=True)
    context.base_url = BASE_URL


def after_all(context):
    _browser.close()
    _pw.stop()


def before_scenario(context, scenario):
    mobile = "mobile" in scenario.tags
    if mobile:
        context.page = _browser.new_page(
            viewport={"width": 390, "height": 844},
            user_agent=(
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
            ),
            has_touch=True,
            is_mobile=True,
        )
    else:
        context.page = _browser.new_page(viewport={"width": 1280, "height": 800})
    context.page.set_default_timeout(15_000)


def after_scenario(context, scenario):
    context.page.close()
