{%- comment -%}
Feature (Gherkin BDD) widget.

Wrap a ```gherkin fenced block with {: .feature } to render it as a styled
BDD feature card. Optional knobs:

  status="passing"   — passing | failing | pending  (colours the card border)
  tags="smoke,auth"  — comma-separated tags shown as chips in the header

Example:

  ```gherkin
  Feature: Login
    Scenario: Successful login
      Given I am on the login page
      When I enter valid credentials
      Then I should see the dashboard
  ```
  {: .feature status="passing" tags="smoke,auth" }

Auto-included by docs/_layouts/default.html on every page.
{%- endcomment -%}

<style>
.lc-feature { border: 1px solid #e5e7eb; border-left: 4px solid #9ca3af; border-radius: 0 8px 8px 0; margin: 1.2em 0; background: #fff; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
.lc-feature-passing { border-left-color: #22c55e; }
.lc-feature-failing  { border-left-color: #ef4444; }
.lc-feature-pending  { border-left-color: #f59e0b; }

.lc-feature-header { display: flex; align-items: center; gap: 0.6em; flex-wrap: wrap; padding: 0.55em 1em 0.5em; background: #f9fafb; border-bottom: 1px solid #e5e7eb; font-size: 0.88em; }
.lc-feature-name { font-weight: 600; color: #111827; flex: 1; min-width: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

.lc-feature-badge { display: inline-flex; align-items: center; gap: 0.3em; padding: 0.15em 0.6em; border-radius: 99px; font-size: 0.8em; font-weight: 500; line-height: 1.6; }
.lc-feature-badge::before { content: "●"; font-size: 0.75em; }
.lc-feature-badge-passing { background: #dcfce7; color: #15803d; }
.lc-feature-badge-failing  { background: #fee2e2; color: #b91c1c; }
.lc-feature-badge-pending  { background: #fef3c7; color: #92400e; }

.lc-feature-tags { display: flex; gap: 0.35em; flex-wrap: wrap; }
.lc-feature-tag { background: #e0f2fe; color: #075985; padding: 0.1em 0.55em; border-radius: 99px; font-size: 0.78em; font-weight: 500; }

.lc-feature-body pre { margin: 0; border-radius: 0; border: none; box-shadow: none; }
.lc-feature-body pre code { font-size: 0.83em; line-height: 1.6; }
</style>

<script>
(function () {
  function upgradeFeature(pre) {
    if (pre.dataset.lcFeatureUpgraded) return;
    pre.dataset.lcFeatureUpgraded = "1";

    var status = pre.getAttribute("status") || "";
    var tagsRaw = pre.getAttribute("tags") || "";
    var code = pre.querySelector("code");
    var text = code ? code.textContent : pre.textContent;

    var firstLine = text.trim().split("\n")[0];
    var featureName = firstLine.replace(/^Feature:\s*/i, "").trim() || "Feature";

    var statusHtml = status
      ? "<span class='lc-feature-badge lc-feature-badge-" + status + "'>" + status + "</span>"
      : "";

    var tagsHtml = "";
    if (tagsRaw) {
      tagsHtml = "<span class='lc-feature-tags'>"
        + tagsRaw.split(",").map(function (t) {
            return "<span class='lc-feature-tag'>" + t.trim() + "</span>";
          }).join("")
        + "</span>";
    }

    var card = document.createElement("div");
    card.className = "lc-feature" + (status ? " lc-feature-" + status : "");
    card.innerHTML =
      "<div class='lc-feature-header'>"
        + "<span class='lc-feature-name'>" + featureName + "</span>"
        + statusHtml
        + tagsHtml
      + "</div>"
      + "<div class='lc-feature-body'></div>";

    var body = card.querySelector(".lc-feature-body");
    var clonedPre = pre.cloneNode(true);
    clonedPre.removeAttribute("status");
    clonedPre.removeAttribute("tags");
    clonedPre.classList.remove("feature");
    body.appendChild(clonedPre);

    pre.parentNode.replaceChild(card, pre);
  }

  function init() {
    document.querySelectorAll("pre.feature").forEach(upgradeFeature);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
</script>
