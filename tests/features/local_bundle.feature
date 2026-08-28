Feature: 🌀 Lightcode Local — the bundle behaves inside its walls
  The Tier A bundle ships ONLY the runner, and the site topbar baked into
  run.html points at pages the bundle does not carry — Georges clicked
  Courses and met a 404 (2026-08-25). So every road into the bundle wears
  crumb mode, which folds the bar to one read-only line with no doors;
  the crumb behaviour itself is proven in frame_scope.feature.

  Scenario: The bundle's front door carries the crumb from the first paint
    Then the bundler's landing page bakes the local crumb

  Scenario: Every app page declares the local frame itself
    Direct opens of run.html skip the landing page — each app carries the
    declaration, so the sealed bar rides every road in.

    Then each local app declares the "Lightcode Local" crumb
