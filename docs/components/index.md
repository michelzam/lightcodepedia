# 🧩 Component Gallery

Welcome, lowcoder! Every interactive component you can use in your `.md` pages.

**The rule of the game:** you only write markdown. Components activate via `{: .class }` — an IAL tag on the line after a fenced block or link. No HTML, no CSS, no JavaScript needed!


````
### 🗺️ Component Map
[Browse](/docs/components)
{: .sitemap path="docs/components" height="460" }
````
{: .accordion }

## Available components

[Browse →](docs/components)
{: .folder cols="3" }

## 🎨 Component palette

```gherkin
Feature: Component palette
    As a lazy lowcoder & learner
    I want to discover the available components
    So that I can learn and customize my app quickly with minimal prior knowledge
  Background: 
    Given the user / learner is on this package (folder) or modules or subfolders)
  Scenario: Outside-in / X-Rays
    Given I am on a component doc page 
    When I explore with x-rays feature
    Then I can preview the inner structure and connections between blocks
  Scenario: Outside-in
    Given a module
    When I visualize and edit the source (SSOT) 
    Then I can see only  blocks
      with simple markdown and kramdown (IAL) 
      and some blocks and fences in yaml, python and csv
    And IAL have simpl names, with pythonistic #id, 
      simple knobs with obvious default values 
    And there is no js, html, css
  Scenario: from the future
    Given a module 
    When in preview or run it
    Then I can see first the Why (usage) through a meaningful simple use case
     And an example that illustrate the need
     And the way to create and customize it
     And the reference of all knobs
     And be able to test my knowledge with funny quizzes
     And my persistent score is displayed (and stored in localStorage)
  Scenario: Bottom-up
    Given a module 
    When in preview or run it
    Then I can see easily join other related components and examples
```
{: .feature visible="false" tags="learning" }