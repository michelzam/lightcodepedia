{%- comment -%}
Mdpad — a live Markdown scratchpad: read the rendered result on the LEFT,
type the source on the RIGHT, updating on every keystroke. Seed it with a fenced
markdown block; the IAL upgrades it in place (P8), and rendering reuses
the shared marked loader from core (P9). No JS in the content (P5).

Usage:
  ````markdown
  ## Hello!
  **Bold** and *italic*, a [link](/), and a list:
  - one
  - two
  ````
  {: .mdpad rows="14" }

IAL knobs:
  rows="14"   editor height in text rows (default 12)
  save="true" show a 💾 Save button that commits straight to the source file
  save="cv.md"
              the two-repo contract: the fence is the AUTHOR's seed, the
              learner's saved copy lives in their OWN bench — relative =
              beside the lesson (the page's folder, FULL course path, so two
              courses in one bench never collide), "/my/cv.md" = bench root
              for files that outlive one lesson
              (the repo they connected at join). On load the bench copy —
              when it exists — replaces the seed; 💾 commits back to it;
              ↺ restores the seed (their file survives until they 💾 over
              it). The author can republish the page forever: seed and
              saved copy are different files in different repos, so
              nothing ever collides.
  piano="true"   consecutive blocks banded in two shades of the source pane, the
              caret's block in a third — the "piano"
  numbers="true" a line number per source line in a gutter (wrapped lines keep one);
              a decoration's line also wears its component's icon there (🛢️ ▦ ☷)
  replay="1.5"  seconds per frame when 🎞 Replay plays the saved versions (default 1.5);
              the button sits at the head of 🕘 Versions, and any row of that
              list, clicked, shows that version the same way — read-only
  comment="true"
              💾 Save… asks for one line — what you just did — before it writes;
              the line is the version's name in 🕘 Versions (a diary, not
              "✍️ pad" ×12). Empty line = nothing written. Default off: one click.
  decorations="true"
              the preview renders the page the way the site does: block
              decorations ({: .red} under a paragraph, {: .pitch} under a
              yaml fence…) apply, and component fences come alive — a
              learner's résumé can carry a pitch, cards, a chart. Same
              pipeline as the runner. Debounced, not per keystroke: a
              component rebuilds, a word does not.
  id="..."    optional — names the pad for X-ray
  (always)       the source is painted: a fence and its body muted, a {: … }
                 decoration on a lighter band — class, #id and knobs in their
                 own colours — headings, links, emphasis; keystrokes patch the
                 mirror in place so ⌘Z stays whole (Michel, 2026-10-08)
  (decorations)  the preview's model is what the text declares: a dataset
                 the pad no longer writes leaves the registry with the render,
                 and a wire (source= master= bound= target=) to an id the page
                 does not have is drawn broken — dashed frame, one chip,
                 data-lc-broken on the pad (Michel, 2026-10-08)
  ✎ Hide / Edit  one small button on every pad folds the editor away so the
                 preview takes the whole width, and brings it back
                 (Michel, 2026-10-09, on the phone); pad.fold()/unfold()
  layout="rows"  preview ABOVE the source instead of beside it — for a
              landscape document (a story in colour) that would be squeezed
              in half a pane. DEFAULT: side by side (left/right).

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-mdpad { display: flex; gap: 0.75em; margin: 1em 0; min-height: 220px; position: relative; }
/* ✎ FOLD — the editor tucks away and the preview takes the whole width
   (Michel, 2026-10-09, on the phone); the same button brings it back */
.lc-mdpad-fold { position: absolute; top: 0.35em; right: 0.35em; z-index: 3; font: inherit; font-size: 0.72em;
  padding: 0.2em 0.55em; border-radius: 6px; border: 1px solid #bbb; background: rgba(255, 255, 255, 0.92);
  color: #555; cursor: pointer; line-height: 1.3; }
.lc-mdpad-fold:hover { border-color: #888; color: #222; }
.lc-mdpad.lc-mdpad-folded > .lc-mdpad-src { display: none !important; }
/* ↕ the grip under the pad: drag to resize, for this visit only */
.lc-mdpad-grip { position: absolute; left: 0; right: 0; bottom: -0.75em; height: 0.75em; cursor: ns-resize;
  touch-action: none; z-index: 2; display: flex; align-items: center; justify-content: center; }
.lc-mdpad-grip::before { content: ""; width: 3.2em; height: 4px; border-radius: 3px; background: #c4c9d4; }
.lc-mdpad-grip:hover::before, .lc-mdpad[data-lc-resizing] .lc-mdpad-grip::before { background: #0066cc; }
/* a dragged height wins over rows=: both panes may shrink below their content and scroll */
.lc-mdpad[style*="height"] > .lc-mdpad-out, .lc-mdpad[style*="height"] > .lc-mdpad-src,
.lc-mdpad[style*="height"] .lc-mdpad-in { min-height: 0; }
.lc-mdpad[style*="height"] .lc-mdpad-in { height: auto; align-self: stretch; }
.lc-mdpad-in {
  flex: 1; min-width: 0; resize: vertical;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 0.85em; line-height: 1.5; padding: 0.8em;
  border: 1px solid #d0d0d0; border-radius: 6px;
  background: #1e1e2e; color: #cdd6f4;
}
.lc-mdpad-out {
  flex: 1; min-width: 0; padding: 0.8em; overflow: auto;
  border: 1px solid #d0d0d0; border-radius: 6px;
  background: #fafafa; font-size: 0.95em;
}
/* an APP SCREEN: a pad that is both saved to the bench and decorated is a
   page of the learner's own app, so its preview wears app chrome — a title
   bar mirroring the page's own # line — instead of a bare rendering */
.lc-mdpad-app { padding: 0; border-radius: 12px; border: 1px solid #c7cdd6;
  box-shadow: 0 6px 18px rgba(15, 23, 42, 0.10); background: #fff; display: flex; flex-direction: column; }
.lc-mdpad-apphead { display: flex; align-items: center; gap: 0.5em; padding: 0.5em 0.9em;
  background: #1e293b; color: #f8fafc; font-weight: 600; font-size: 0.9em;
  border-radius: 12px 12px 0 0; letter-spacing: 0.01em; }
.lc-mdpad-apphead .lc-mdpad-appdots { display: inline-flex; gap: 4px; margin-right: 0.2em; }
.lc-mdpad-apphead .lc-mdpad-appdots i { width: 8px; height: 8px; border-radius: 50%; background: #64748b; display: inline-block; }
.lc-mdpad-appbody { padding: 0.8em; overflow: auto; flex: 1; }
/* phones: preview first, then the source under it — same order as wide */
@media (max-width: 640px) { .lc-mdpad { flex-direction: column; } }
/* layout="rows": the same stacking on every screen, for a landscape document */
.lc-mdpad.lc-mdpad-rows { flex-direction: column; }
.lc-mdpad-bar { margin: -0.4em 0 1em; display: flex; justify-content: flex-end; gap: 0.5em; align-items: center; }
.lc-mdpad-mine { margin-right: auto; font-size: 0.78em; color: #2e7d32; }
.lc-mdpad-reset { font: inherit; font-size: 0.85em; padding: 0.35em 0.7em; border-radius: 6px;
  border: 1px solid #bbb; background: #fff; color: #555; cursor: pointer; }
.lc-mdpad-reset:hover { border-color: #888; color: #222; }
/* 🕘 versions — styling for the SHARED panel (lcVersions) in a pad's bar */
.lc-mdpad-bar .lc-ver-btn { font: inherit; font-size: 0.85em; padding: 0.35em 0.7em;
  border-radius: 6px; border: 1px solid #bbb; background: #fff; color: #555; cursor: pointer; }
.lc-mdpad-bar .lc-ver-btn:hover { border-color: #888; color: #222; }
/* an ON/OFF button looks on: pressed = inverted, so the open list reads as a
   state and not as a second click's surprise (Michel, 2026-10-06) */
.lc-mdpad-bar .lc-ver-btn[aria-pressed="true"] { background: #333; border-color: #333; color: #fff; }
.lc-mdpad-bar button:disabled { opacity: 0.45; cursor: default; }
/* 💾 Save… — the one-line box: what did you just do? */
.lc-mdpad-commentbar { display: flex; gap: 0.5em; align-items: center; margin: -0.4em 0 0.8em; font-size: 0.9em; }
.lc-mdpad-commentbar input { flex: 1; min-width: 120px; font: inherit; padding: 0.35em 0.6em; border: 1px solid #bbb; border-radius: 6px; }
.lc-mdpad-commentbar button { font: inherit; font-size: 0.9em; padding: 0.35em 0.7em; border-radius: 6px; border: 1px solid #bbb; background: #fff; color: #444; cursor: pointer; }
.lc-mdpad-commentbar button.lc-mdpad-keep { background: #0066cc; border-color: #0066cc; color: #fff; }
.lc-mdpad-commentbar button:disabled { opacity: 0.45; cursor: default; }
.lc-ver-panel { border: 1px solid #d0d0d0; border-radius: 8px; margin: -0.6em 0 1em;
  background: #fafafa; overflow: hidden; font-size: 0.88em; }
.lc-ver-panel ol { list-style: none; margin: 0; padding: 0; max-height: 220px; overflow: auto; }
.lc-ver-panel li { display: flex; align-items: center; gap: 0.6em; padding: 0.45em 0.9em;
  border-bottom: 1px solid #eee; }
.lc-ver-panel li:last-child { border-bottom: none; }
.lc-ver-panel li.now { background: #eef6ff; }
.lc-ver-panel li.starter { background: #fffbeb; }
.lc-ver-panel li.starter .lc-ver-when { color: #92400e; font-style: italic; }
.lc-ver-when { color: #444; white-space: nowrap; }
/* the name is the row's text, so it reads first and takes the room */
.lc-ver-msg { flex: 1; color: #222; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.lc-ver-panel li.pick { cursor: pointer; }
.lc-ver-panel li.pick:hover { background: #f1f5f9; }
.lc-ver-panel li.selected { background: #dbeafe !important; box-shadow: inset 3px 0 0 #0066cc; }
.lc-ver-head { display: flex; align-items: center; gap: 0.8em; padding: 0.45em 0.9em; border-bottom: 1px solid #e5e7eb; background: #f3f4f6; }
.lc-ver-head .lc-ver-play { font: inherit; font-size: 0.9em; padding: 0.3em 0.7em; border-radius: 6px; border: 1px solid #bbb; background: #fff; color: #444; cursor: pointer; }
.lc-ver-head .lc-ver-play:disabled { opacity: 0.6; cursor: default; }
.lc-ver-hint { color: var(--lc-ink-mute, #616161); font-size: 0.85em; }
.lc-ver-sha { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; color: #94a3b8; font-size: 0.85em; }
.lc-ver-panel button { font: inherit; font-size: 0.85em; padding: 0.2em 0.6em; border-radius: 5px;
  border: 1px solid #cbd5e1; background: #fff; color: #334155; cursor: pointer; }
.lc-ver-panel button:hover { border-color: #0066cc; color: #0066cc; }
.lc-ver-diff { margin: 0; padding: 0.7em 0.9em; background: #fff; border-top: 1px solid #eee;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.82em;
  line-height: 1.5; white-space: pre-wrap; overflow: auto; max-height: 260px; }
.lc-ver-diff .add { background: #dcfce7; color: #166534; display: block; }
.lc-ver-diff .del { background: #fee2e2; color: #991b1b; display: block; }
.lc-ver-diff .same { color: #64748b; display: block; }
.lc-mdpad-save { font: inherit; font-size: 0.85em; padding: 0.35em 1em; border-radius: 6px;
  border: 1px solid #0066cc; background: #0066cc; color: #fff; cursor: pointer; }
.lc-mdpad-save:hover:not(:disabled) { background: #0052a3; }
.lc-mdpad-save:disabled { opacity: 0.45; cursor: default; }
/* FOCUS — the caret's block, pulsed in the preview (Michel, 2026-10-05: "help
   students see where to focus when they make a change", as the page editor does) */
.lc-mdpad-out .lc-mdpad-focus { animation: lc-mdpad-pulse 1.4s ease-out; border-radius: 4px; }
/* a wire to nothing: the block wears a dashed frame that names the missing id */
.lc-mdpad-out .lc-mdpad-broken { outline: 2px dashed #c62828; outline-offset: 4px; border-radius: 4px; }
.lc-mdpad-out .lc-mdpad-broken::before { content: "🔌 " attr(data-lc-broken) " — no such id on this page"; display: block; color: #c62828; font-size: .8em; font-family: ui-sans-serif, system-ui, sans-serif; margin-bottom: .35em; }
.lc-mdpad-wires { color: #c62828; font-size: .85em; margin: 0 0 .6em; }
@keyframes lc-mdpad-pulse {
  0%   { background: #dbeafe; box-shadow: 0 0 0 4px #dbeafe; }
  100% { background: transparent; box-shadow: 0 0 0 4px transparent; }
}
@media (prefers-reduced-motion: reduce) {
  .lc-mdpad-out .lc-mdpad-focus { animation: none; box-shadow: 0 0 0 3px #bfdbfe; }
}
/* PIANO + NUMBERS — a backdrop behind the source mirrors it line for line:
   consecutive blocks banded in two shades of the dark pane, the caret's block
   in a third; a gutter with one number per source line (wrapped lines keep
   theirs). The textarea goes transparent over it. */
.lc-mdpad-src { flex: 1; min-width: 0; position: relative; display: flex; }
.lc-mdpad-src .lc-mdpad-in { flex: 1; min-width: 0; background: transparent; position: relative; z-index: 1; color: transparent; caret-color: #cdd6f4; }
.lc-mdpad-src .lc-mdpad-in::selection { background: rgba(137, 180, 250, 0.35); color: transparent; }
/* the painted source: a fence and its body muted, a decoration on its own
   lighter band — the class, the #id and each knob in their colours */
.lc-mdpad-piano .ln { color: #cdd6f4; }
/* the token colours (.md-h, .md-ial …) live with the painter, in widgets.md */
.lc-mdpad-src[data-numbers] .lc-mdpad-in { padding-left: 4.4em; }
.lc-mdpad-piano { position: absolute; inset: 0; overflow: hidden; pointer-events: none; z-index: 0;
  box-sizing: border-box; background: #1e1e2e; border: 1px solid transparent; border-radius: 6px;
  white-space: pre-wrap; overflow-wrap: break-word; word-break: normal; }
.lc-mdpad-piano .k1 { background: #26263a; }
.lc-mdpad-piano .now { background: #30304c; box-shadow: inset 3px 0 0 #89b4fa; }
/* with a gutter, the current block's bar moves into it, clear of the first letters */
.lc-mdpad-src[data-numbers] .lc-mdpad-piano .now { box-shadow: none; }
.lc-mdpad-piano[data-plain] .k1 { background: transparent; }
.lc-mdpad-piano[data-plain] .now { background: transparent; box-shadow: none; }
.lc-mdpad-piano .ln { position: relative; }
/* the gutter: a grayer column so numbers never read as text (Michel, 2026-10-05) —
   painted as the pane's background, so it stays put while the text scrolls; each
   row's cell then carries the piano into the gutter in its own grayer shades.
   2026-10-10 (Michel): the block's shade fills the WHOLE gutter for its height,
   to the pane's left edge; the current block's blue bar is drawn in the gutter,
   just left of the text, never over the first letters; the icons sit centred in
   a column of their own, an emoji and a glyph (▦ ☷) brought to one size. The
   pseudo-elements keep the line's font size, so every offset is in its units. */
.lc-mdpad-src[data-numbers] .lc-mdpad-piano { background:
  linear-gradient(90deg, #2a2a38 0, #2a2a38 4em, #1e1e2e 4em); }
.lc-mdpad-src[data-numbers] .lc-mdpad-piano .ln::before {
  content: attr(data-n); position: absolute; left: -4.4em; top: 0; bottom: 0; width: 4.4em; box-sizing: border-box;
  text-align: right; padding-right: 0.95em; color: #6c7086; line-height: inherit; font-variant-numeric: tabular-nums;
  background: linear-gradient(90deg, transparent 4em, #3c3c50 4em, #3c3c50 calc(4em + 1px), transparent calc(4em + 1px)); }
.lc-mdpad-src[data-numbers] .lc-mdpad-piano .k1 .ln::before { background-color: #30303f; }
.lc-mdpad-src[data-numbers] .lc-mdpad-piano .now .ln::before { background: #3a3a54
  linear-gradient(90deg, transparent 3.85em, #89b4fa 3.85em, #89b4fa calc(3.85em + 3px), transparent calc(3.85em + 3px)); }
.lc-mdpad-src[data-numbers] .lc-mdpad-piano .ln.here::before { color: #cdd6f4; }
.lc-mdpad-src[data-numbers] .lc-mdpad-piano .ln[data-ic]::after {
  content: attr(data-ic); position: absolute; left: -4.25em; top: 0; width: 1.5em; text-align: center;
  line-height: inherit; transform: scale(0.82); }
.lc-mdpad-src[data-numbers] .lc-mdpad-piano .ln[data-ick="g"]::after { transform: scale(1.3); color: #cdd6f4; }
/* 🎞 REPLAY — the source pane becomes a diff pane: + green, − red, the
   usual cues; a slider is the cursor; play runs forward, the moonwalk back */
.lc-mdpad-replay, .lc-mdpad-hist { font: inherit; font-size: 0.85em; padding: 0.35em 0.7em; border-radius: 6px;
  border: 1px solid #bbb; background: #fff; color: #555; cursor: pointer; }
.lc-mdpad-replay:hover { border-color: #888; color: #222; }
.lc-mdpad-replay:disabled { opacity: 0.6; cursor: default; }
.lc-mdpad-diff { flex: 1; min-width: 0; margin: 0; padding: 0.8em; overflow: auto; box-sizing: border-box;
  border: 1px solid #d0d0d0; border-radius: 6px; background: #1e1e2e; color: #9399b2;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; line-height: 1.5; white-space: pre-wrap; }
.lc-mdpad-diff .ln { display: block; position: relative; }
.lc-mdpad-diff .add { background: #1f3b2a; color: #a6e3a1; }
.lc-mdpad-diff .del { background: #3b1f26; color: #f38ba8; }
/* THE SIGNS LIVE IN THE GUTTER (Michel, 2026-10-05): + and − are drawn beside the
   line, never typed into it — select and copy a section, the signs stay behind.
   With numbers="true" the gutter also counts the frame's lines. */
.lc-mdpad-diff { padding-left: 2.6em; background:
  linear-gradient(90deg, #2a2a38 0, #2a2a38 2.1em, #3c3c50 2.1em, #3c3c50 calc(2.1em + 1px), #1e1e2e calc(2.1em + 1px)); }
.lc-mdpad-diff .ln::before { content: attr(data-s); position: absolute; left: -2.6em; top: 0; bottom: 0; width: 2.1em;
  box-sizing: border-box; text-align: right; padding-right: 0.45em; color: #6c7086; }
.lc-mdpad-diff[data-numbers] { padding-left: 4.4em; background:
  linear-gradient(90deg, #2a2a38 0, #2a2a38 3.9em, #3c3c50 3.9em, #3c3c50 calc(3.9em + 1px), #1e1e2e calc(3.9em + 1px)); }
.lc-mdpad-diff[data-numbers] .ln::before { content: attr(data-s) " " attr(data-n); left: -4.4em; width: 3.9em; }
.lc-mdpad-diff[data-numbers] .ln[data-ic]::after { content: attr(data-ic); position: absolute; left: -4.35em; top: 0; width: 1.5em;
  text-align: center; transform: scale(0.82); }
.lc-mdpad-diff[data-numbers] .ln[data-ick="g"]::after { transform: scale(1.3); color: #cdd6f4; }
/* the commit's line, floating on the editor under the change while the versions play */
.lc-mdpad-sub { position: absolute; transform: translate(-50%, 0); max-width: 46%; z-index: 3; pointer-events: none;
  background: rgba(17, 17, 27, 0.62); color: #fff; padding: 0.45em 0.9em; border-radius: 12px; font-size: 0.92em;
  line-height: 1.35; text-align: center; opacity: 0; transition: opacity .35s ease, top .35s ease; box-shadow: 0 4px 14px rgba(0,0,0,0.18); }
.lc-mdpad-sub.on { opacity: 0.88; }
@media (prefers-reduced-motion: reduce) { .lc-mdpad-sub { transition: none; } }
.lc-mdpad-diff .add::before { color: #a6e3a1; }
.lc-mdpad-diff .del::before { color: #f38ba8; }
/* the piano, in the pane and in its gutter */
.lc-mdpad-diff .k1 .ln::before { background: #30303f; }
.lc-mdpad-diff .now .ln::before { background: #3a3a54; }
.lc-mdpad-diff[data-piano] .k1 { background: #26263a; }
.lc-mdpad-diff[data-piano] .now { background: #30304c; box-shadow: inset 3px 0 0 #89b4fa; }
/* word level: inside an edited line, the words that actually differ */
.lc-mdpad-diff .add b { font-weight: inherit; background: #2f6b3f; color: #d9ffd9; border-radius: 3px; }
.lc-mdpad-diff .del b { font-weight: inherit; background: #7a2f3f; color: #ffd9e0; border-radius: 3px; }
/* line by line, during play: removed lines fold away, added lines unfold, one after the other */
.lc-mdpad-diff .fold, .lc-mdpad-diff .unfold { overflow: hidden; transition: max-height .35s ease, opacity .35s ease; transition-delay: var(--d, 0s); max-height: 14em; }
.lc-mdpad-diff .unfold { max-height: 0; opacity: 0; }
.lc-mdpad-diff .unfold.go { max-height: 14em; opacity: 1; }
.lc-mdpad-diff .fold.go { max-height: 0; opacity: 0; }
/* the preview cross-fades: a ghost of the old render fades over the new one */
.lc-mdpad-ghost { position: absolute; pointer-events: none; opacity: 1; transition: opacity .3s ease; z-index: 2; }
.lc-mdpad-ghost.go { opacity: 0; }
@media (prefers-reduced-motion: reduce) {
  .lc-mdpad-diff .fold, .lc-mdpad-diff .unfold, .lc-mdpad-ghost { transition: none; }
}
.lc-mdpad-replaybar { display: flex; gap: 0.6em; align-items: center; margin: -0.4em 0 0.6em; font-size: 0.85em; color: #555; }
.lc-mdpad-replaybar button { font: inherit; padding: 0.3em 0.7em; border-radius: 6px; border: 1px solid #bbb; background: #fff; color: #444; cursor: pointer; }
.lc-mdpad-replaybar button:hover { border-color: #888; color: #222; }
.lc-mdpad-replaybar input[type=range] { flex: 1; min-width: 80px; accent-color: #0066cc; }
.lc-mdpad-replaybar .lc-mdpad-frame { white-space: nowrap; font-variant-numeric: tabular-nums; }
</style>

<script>
(function () {
  if (window._lcMdpadReady) return;
  window._lcMdpadReady = true;

  /* ── BLOCKS: the source as the preview counts it. Split at blank lines;
     a fence runs to its closing fence whatever it holds; a run of IAL lines
     ({: … }) belongs to the block above, as the preview merges it into that
     element. One block = one top-level element in the preview, which is
     what the focus below relies on; a heading is found by its words. */
  function blocksOf(src) {
    var lines = src.split("\n"), blocks = [], cur = null, fence = null;
    for (var i = 0; i < lines.length; i++) {
      var ln = lines[i], t = ln.trim();
      if (fence) {
        cur.end = i;
        if (t.charAt(0) === fence.charAt(0) && /^(`{3,}|~{3,})$/.test(t) && t.length >= fence.length) fence = null;
        continue;
      }
      if (t === "") { cur = null; continue; }
      if (!cur && blocks.length && /^\{:.*\}$/.test(t)) { blocks[blocks.length - 1].end = i; continue; }
      if (!cur) { cur = { start: i, end: i, head: ln }; blocks.push(cur); } else cur.end = i;
      var m = t.match(/^(`{3,}|~{3,})/);
      if (m) fence = m[1];
    }
    return blocks;
  }
  function blockAt(blocks, line) {
    for (var i = 0; i < blocks.length; i++) if (line >= blocks[i].start && line <= blocks[i].end) return i;
    return -1;
  }
  function escHtml(s) { return s.replace(/[&<>]/g, function (c) { return c === "&" ? "&amp;" : c === "<" ? "&lt;" : "&gt;"; }); }
  /* THE COMPONENT'S ICON IN THE GUTTER (Michel, 2026-10-10): a decoration line
     carries its component's emoji beside its number — 🛢️ dataset, ▦ datagrid,
     ☷ form — the icons the x-ray and the editor already show, read from the
     one component model. A class that is no component (.red, #top) gets none. */
  function compIcons() { return window.lcComponentIcons(); }   /* widgets.md */
  var _icons = {};
  /* a text glyph (▦ ☷ ▤) draws smaller than a colour emoji (🛢️ 📈): marked, then scaled up */
  function icGlyph(ic) { return !(ic.codePointAt(0) > 0xFFFF || ic.indexOf("\uFE0F") >= 0); }
  function ialIcon(body) {
    var cls = (body.match(/(?:^|\s)\.([A-Za-z][\w-]*)/) || [])[1];
    return cls ? (_icons[cls.replace(/[-_]/g, "").toLowerCase()] || "") : "";
  }

  function upgradeMdpad(el) {
    if (el.dataset.lcMdpadDone) return;
    el.dataset.lcMdpadDone = "1";
    var seed = (el.querySelector("code") || el).textContent.replace(/\n+$/, "");
    var rows = parseInt(el.getAttribute("rows") || "12", 10);
    var deco = el.getAttribute("decorations") === "true";
    var id = el.id || "";

    var wrap = document.createElement("div");
    wrap.className = "lc-mdpad";
    if (deco) wrap.setAttribute("data-lc-decorations", "1");
    if ((el.getAttribute("layout") || "") === "rows") wrap.classList.add("lc-mdpad-rows");
    if (id) wrap.setAttribute("data-lc-id", id);
    /* a named pad is page data: it publishes {source} as a cell scope, so
       expressions can read what the learner typed — {=cv1.source} in prose,
       in a visible= gate, or handed to an agent through bound="{=…}".
       Debounced: cells recompute in MicroPython, not per keystroke. */
    var _pubT = null;
    function publish(fire) {
      if (!id) return;
      wrap.setAttribute("data-lc-value", JSON.stringify({ source: ta.value }));
      if (fire) {
        try { document.dispatchEvent(new CustomEvent("lc-model-changed")); } catch (e) {}
      }
    }

    var ta = document.createElement("textarea");
    ta.className = "lc-mdpad-in";
    var piano = el.getAttribute("piano") === "true", numbers = el.getAttribute("numbers") === "true";
    var src = null, keysEl = null;
    /* the mirror ALWAYS exists now: it carries the colours (2026-10-08);
       the piano's bands and the numbers stay the knobs they were */
    if (true) {
      src = document.createElement("div");
      src.className = "lc-mdpad-src";
      if (numbers) src.setAttribute("data-numbers", "1");
      keysEl = document.createElement("div");
      keysEl.className = "lc-mdpad-piano lc-md-paint";
      keysEl.setAttribute("aria-hidden", "true");
      if (!piano) keysEl.setAttribute("data-plain", "1");
      src.appendChild(keysEl);
      src.appendChild(ta);
    }
    ta.setAttribute("aria-label", "Markdown editor");
    ta.spellcheck = false;
    ta.rows = rows;
    ta.value = seed;

    var out = document.createElement("div");
    out.className = "lc-mdpad-out";
    var body = out, appTitle = null;   /* app chrome, decided once save= is known */

    /* save="true" — commit straight from the pad, no x-ray, no page editor.
       It reuses the SAME commit path the x-ray Keep uses (lcCommitInline), so
       there is one way a block gets written back, not two that drift. The
       button only exists when a save is actually possible: a key, a resolved
       source, and a source that is not read-only. */
    /* save="my/cv.md" — the OTHER save: the page is the author's (vault,
       no learner write), the work is the learner's. The fence seeds; the
       learner's copy persists at this path in their own bench and, when it
       exists, replaces the seed on load. Same page, two repos, one writer
       per file — the author can republish forever without touching it. */
    var saveKnob = el.getAttribute("save") || "";
    var benchPath = saveKnob && saveKnob !== "true" ? saveKnob : "";
    if (benchPath) wrap.setAttribute("data-lc-save", benchPath);   /* named in a proof's verdict */
    var saveWrap = null, saveBtn = null, resetBtn = null, mineTag = null, histBtn = null;
    var pace = parseFloat(el.getAttribute("replay")) || 1.5;   /* seconds per replay frame */
    /* comment="true": 💾 Save… — the ellipsis promises a question, one line
       about what was just done; it becomes the version's name. */
    var askComment = el.getAttribute("comment") === "true";
    /* AN APP SCREEN (Michel, 2026-10-02): saved to the bench AND decorated,
       the pad is a page of the learner's own app — so the preview wears app
       chrome, a title bar that mirrors the page's # line (the file's name
       until there is one). The outer .lc-mdpad-out stays what proofs and
       the suite read; only the rendering moves into the body under the bar. */
    if (deco && benchPath) {
      out.classList.add("lc-mdpad-app");
      var head = document.createElement("div");
      head.className = "lc-mdpad-apphead";
      head.innerHTML = "<span class='lc-mdpad-appdots'><i></i><i></i><i></i></span>";
      appTitle = document.createElement("span");
      appTitle.className = "lc-mdpad-apptitle";
      appTitle.textContent = benchPath;
      head.appendChild(appTitle);
      body = document.createElement("div");
      body.className = "lc-mdpad-appbody";
      out.appendChild(head);
      out.appendChild(body);
    }
    /* the stripe every saved block wears — see lcBenchFrame in widgets.md */
    var frame = null;
    if (saveKnob) {
      saveWrap = document.createElement("div");
      saveWrap.className = "lc-mdpad-bar";
      if (benchPath) {
        mineTag = document.createElement("span");
        mineTag.className = "lc-mdpad-mine";
        mineTag.hidden = true;
        mineTag.textContent = "✓ yours — saved in your space";
        histBtn = document.createElement("button");
        histBtn.type = "button";
        histBtn.className = "lc-mdpad-hist";
        histBtn.hidden = true;          /* nothing to show until a first save */
        histBtn.textContent = "🕘 Versions";
        histBtn.title = "Every version you saved — read it, compare it, bring it back";
        resetBtn = document.createElement("button");
        resetBtn.type = "button";
        resetBtn.className = "lc-mdpad-reset";
        resetBtn.textContent = "↺ Start over";
        resetBtn.title = "Bring back the lesson's starter — your saved copy stays until you 💾 again";
        /* 🎞 Replay lives INSIDE 🕘 Versions (its head), not in this bar —
           one place for the history (Michel, 2026-10-06) */
        saveWrap.appendChild(mineTag);
        saveWrap.appendChild(histBtn);
        saveWrap.appendChild(resetBtn);
      }
      saveBtn = document.createElement("button");
      saveBtn.type = "button";
      saveBtn.className = "lc-mdpad-save";
      saveBtn.textContent = askComment ? "💾 Save…" : "💾 Save";
      saveWrap.appendChild(saveBtn);
    }

    /* Preview LEFT, source RIGHT — and appended in that order, so the DOM
       order matches what the eye sees. Reversing this with CSS alone would
       leave a keyboard and a screen reader walking it the other way round. */
    wrap.appendChild(out);
    wrap.appendChild(src || ta);
    /* ✎ fold: the editor tucks away, the preview takes the whole width */
    var foldBtn = document.createElement("button");
    foldBtn.type = "button"; foldBtn.className = "lc-mdpad-fold";
    function setFold(on) {
      wrap.classList.toggle("lc-mdpad-folded", !!on);
      if (on) wrap.setAttribute("data-lc-folded", "1"); else wrap.removeAttribute("data-lc-folded");
      foldBtn.textContent = on ? "✎ Edit" : "✎ Hide";
      foldBtn.setAttribute("aria-pressed", on ? "true" : "false");
      foldBtn.title = on ? "Bring the editor back" : "Fold the editor — the preview takes the whole width";
    }
    foldBtn.addEventListener("click", function () { setFold(!wrap.classList.contains("lc-mdpad-folded")); });
    setFold(false);
    wrap.appendChild(foldBtn);
    wrap._lcFold = setFold;
    /* ↕ THE GRIP (Michel, 2026-10-10: "a non persistent way to be resized
       vertically, so during work or demos we can decide different layouts"):
       a bar under the pad, dragged, sets the pad's height — editor and
       preview together, side by side or stacked. Nothing is kept: the next
       visit opens at the lesson's rows=. Double-click gives that back now. */
    var grip = document.createElement("div");
    grip.className = "lc-mdpad-grip";
    grip.setAttribute("role", "separator");
    grip.setAttribute("aria-orientation", "horizontal");
    grip.title = "Drag to make the pad taller or shorter — double-click to reset";
    wrap.appendChild(grip);
    grip.addEventListener("pointerdown", function (ev) {
      ev.preventDefault();
      var y0 = ev.clientY, h0 = wrap.getBoundingClientRect().height;
      grip.setPointerCapture(ev.pointerId);
      wrap.setAttribute("data-lc-resizing", "1");
      function move(e) {
        wrap.style.height = Math.max(160, Math.round(h0 + e.clientY - y0)) + "px";
        if (keysEl) paintSoon();
      }
      function up() {
        wrap.removeAttribute("data-lc-resizing");
        grip.removeEventListener("pointermove", move);
        grip.removeEventListener("pointerup", up);
        grip.removeEventListener("pointercancel", up);
      }
      grip.addEventListener("pointermove", move);
      grip.addEventListener("pointerup", up);
      grip.addEventListener("pointercancel", up);
    });
    grip.addEventListener("dblclick", function () { wrap.style.height = ""; if (keysEl) paintSoon(); });
    el.parentNode.replaceChild(wrap, el);
    if (saveWrap) wrap.parentNode.insertBefore(saveWrap, wrap.nextSibling);
    /* the stripe goes round BOTH the pad and its keep bar, so the frame
       reads as one owned thing rather than a box with a bar loose under it */
    if (benchPath && window.lcBenchFrame) {
      frame = window.lcBenchFrame(wrap, { path: benchPath, id: id, mine: false });
      if (frame && saveWrap) frame.el.appendChild(saveWrap);
    }

    if (saveBtn && benchPath) {
      var bOrigin = seed, bSha = null;
      /* A BUTTON THAT WOULD DO NOTHING IS OFF (Michel, 2026-10-06): 💾 with
         nothing changed, ↺ while the editor already holds the starter. The
         title says why, so off is never mute. */
      var refreshBench = function () {
        var t = window.lcBench ? window.lcBench.target(wrap) : {};
        var why = !window.lcBench ? "Saving needs a newer engine"
                : !t.pat || !t.repo ? "Join the course (connect your key) to keep your work"
                : ta.value === bOrigin ? "Nothing changed since your last save" : "";
        saveBtn.disabled = !!why || !!commentBox;
        saveBtn.title = why || (askComment ? "Keep this in your own space — and say in one line what you just did"
                              : "Keep this in your own space (" +
          (window.lcBench ? window.lcBench.resolve(benchPath, wrap) : benchPath) + ")");
        if (resetBtn) {
          var onSeed = ta.value === seed;
          resetBtn.disabled = onSeed;
          resetBtn.title = onSeed ? "This is the lesson's starter already"
                         : "Bring back the lesson's starter — your saved copy stays until you 💾 again";
        }
      };
      var commentBox = null;
      refreshBench();
      if (window.lcBench) {
        window.lcBench.read(benchPath, wrap).then(function (f) {
          if (!f) return;
          bOrigin = f.text; bSha = f.sha;
          /* a decorated pad glues a saved copy's decorations back to their
             lines (old gaps, see lcGlueIAL); the healed text differs from
             the saved one, so 💾 offers to keep it */
          ta.value = deco && window.lcGlueIAL ? window.lcGlueIAL(f.text) : f.text;
          wrap.setAttribute("data-lc-mine", "1");
          if (mineTag) mineTag.hidden = false;
          if (frame) frame.setMine(true);
          revealVersions();                      /* a saved file HAS a history */
          render(); publish(true); refreshBench();   /* the text moved: ↺ and 💾 decide again */
        }).catch(function () {});
      }
      function doSave(message) {
        saveBtn.disabled = true; saveBtn.textContent = "💾 Saving…";
        /* FIRST save writes the author's starter first, so the learner's
           opening change has something to compare against — otherwise
           version one IS their text and 🕘 shows a single row that differs
           from nothing. Written on the first save, never on load: a reader
           who never edits leaves no commits at all. Never allowed to block
           the real save. */
        var first = !bSha;
        (first
          ? window.lcBench.write(benchPath, seed, window.lcStarterMsg, null, wrap)
              .then(function (sha) { bSha = sha || bSha; })
              .catch(function () {})
          : Promise.resolve()
        ).then(function () {
        return window.lcBench.write(benchPath, ta.value, message, bSha, wrap)
          .then(function (sha) {
            bOrigin = ta.value; bSha = sha || bSha;
            wrap.setAttribute("data-lc-mine", "1");
            wrap.removeAttribute("data-lc-dirty");
            try { document.dispatchEvent(new CustomEvent("lc-saved", { detail: { id: id } })); } catch (e2) {}
            if (mineTag) mineTag.hidden = false;
            if (frame) frame.setMine(true);
            revealVersions();
            closeVersions();                     /* the list just grew — re-open it fresh */
            window.lcxToast && window.lcxToast("Saved to your space ✓", true);
          })
          .catch(function (e) {
            window.lcxToast && window.lcxToast("Save failed: " + (e.message || e), false);
          })
          .finally(function () { saveBtn.textContent = askComment ? "💾 Save…" : "💾 Save"; refreshBench(); });
        });
      }
      /* the one-line box under the pad: Enter keeps, Esc or an empty line
         keeps nothing. The line is the commit message — the diary entry. */
      function askThenSave() {
        if (commentBox) return;
        var box = document.createElement("div");
        box.className = "lc-mdpad-commentbar";
        var inp = document.createElement("input");
        inp.type = "text"; inp.maxLength = 120;
        inp.placeholder = "What did you just do? — one line, e.g. the card follows the table";
        inp.setAttribute("aria-label", "What did you just do?");
        var keep = document.createElement("button");
        keep.type = "button"; keep.className = "lc-mdpad-keep"; keep.textContent = "💾 Keep"; keep.disabled = true;
        var cancel = document.createElement("button");
        cancel.type = "button"; cancel.className = "lc-mdpad-cancel"; cancel.textContent = "Cancel";
        box.appendChild(inp); box.appendChild(keep); box.appendChild(cancel);
        saveWrap.parentNode.insertBefore(box, saveWrap);
        commentBox = box; refreshBench();
        function close() {
          if (box.parentNode) box.parentNode.removeChild(box);
          commentBox = null; refreshBench();
        }
        inp.addEventListener("input", function () { keep.disabled = !inp.value.trim(); });
        inp.addEventListener("keydown", function (e) {
          if (e.key === "Enter" && inp.value.trim()) { e.preventDefault(); go(); }
          if (e.key === "Escape") { e.preventDefault(); close(); }
        });
        function go() { var line = inp.value.trim(); if (!line) return; close(); doSave("✍️ " + line); }
        keep.addEventListener("click", go);
        cancel.addEventListener("click", close);
        inp.focus();
      }
      saveBtn.addEventListener("click", function () {
        refreshBench();
        if (saveBtn.disabled) return;
        if (askComment) askThenSave(); else doSave("✍️ " + (id || benchPath));
      });
      resetBtn.addEventListener("click", function () {
        ta.value = seed;
        render(); publish(true); refreshBench();
        window.lcxToast && window.lcxToast("Starter restored — 💾 to make it yours", true);
      });

      /* 🕘 versions — the SHARED panel (lcVersions), the same one the grid
         uses. One implementation, two call sites; removing this call takes
         the feature out of the pad and nothing else. */
      var vers = window.lcVersions ? window.lcVersions.attach({
        path: benchPath, el: wrap, anchor: saveWrap,
        current: function () { return ta.value; },
        apply: function (t) { ta.value = t; render(); publish(true); refreshBench(); },
        /* the panel's head carries 🎞; a row click shows that version */
        play: function () { if (rp.on) rpStop(); else rpStart(); },
        onSelect: function (c) {
          (rp.on ? Promise.resolve() : rpStart()).then(function () {
            var i = -1;
            (rp.frames || []).forEach(function (f, k) { if (f.sha === c.sha) i = k; });
            if (i >= 0) { rpPause(); rpShow(i); }
          });
        },
        onClose: function () { if (rp.on) rpStop(); }
      }) : null;
      if (vers) histBtn.parentNode.replaceChild(vers.button, histBtn);
      function closeVersions() { if (vers) vers.close(); }
      function revealVersions() { if (vers) vers.reveal(); }
      /* the play button is the panel's — it exists only while the list is open */
      function setPlay(text, disabled) {
        var b = vers && vers.playButton ? vers.playButton() : null;
        if (!b) return;
        b.textContent = text; b.disabled = !!disabled;
      }

      /* ── 🎞 REPLAY (Michel, 2026-10-05): every saved version as a frame, the
         author's starter first (the first save writes it, above), read-only.
         The source pane becomes a diff pane with the usual cues (+ green,
         − red) against the frame before; the block that changed pulses in
         the preview; a slider is the cursor; ▶ plays forward, ◀ backward
         (the moonwalk), replay="1.5" seconds per frame. Nothing is written:
         the learner's text waits under the pane, untouched. */
      var rp = { frames: null, at: 0, timer: null, dir: 1, ui: null, diffEl: null, on: false, sub: null };
      function rpLoad() {
        if (rp.frames) return Promise.resolve(rp.frames);
        return window.lcBench.history(benchPath, wrap, 100).then(function (list) {
          list = list.slice().reverse();              /* oldest first: frame zero is the starter */
          return Promise.all(list.map(function (c) {
            return window.lcBench.readAt(benchPath, c.sha, wrap).then(function (t) {
              return { sha: c.sha, when: c.when, message: c.message, text: t == null ? "" : String(t),
                       starter: String(c.message || "").indexOf(window.lcStarterMsg || "📄 starter") === 0 };
            });
          }));
        }).then(function (frames) { rp.frames = frames; return frames; });
      }
      /* WORD LEVEL: an edited line is a − / + pair; the words that differ are
         the middle once the common head and tail are peeled off, backed off to
         word boundaries so a mark never starts mid-word. */
      function wordMarks(a, b) {
        var i = 0, n = Math.min(a.length, b.length);
        while (i < n && a.charAt(i) === b.charAt(i)) i++;
        while (i > 0 && /\S/.test(a.charAt(i - 1)) && /\S/.test(a.charAt(i) || " ")) i--;
        var j = 0;
        while (j < n - i && a.charAt(a.length - 1 - j) === b.charAt(b.length - 1 - j)) j++;
        while (j > 0 && /\S/.test(a.charAt(a.length - j)) && /\S/.test(a.charAt(a.length - j - 1) || " ")) j--;
        if (i + j < 2) return null;            /* nothing in common: a different line, not an edit */
        function mark(t) {
          var mid = t.slice(i, t.length - j);
          return escHtml(t.slice(0, i)) + (mid ? "<b>" + escHtml(mid) + "</b>" : "") + escHtml(t.slice(t.length - j));
        }
        return [mark(a), mark(b)];
      }
      var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      var rpAnimT = null;
      function rpShow(n, animate) {
        var f = rp.frames && rp.frames[n]; if (!f) return;
        rp.at = n;
        if (vers && vers.mark) vers.mark(f.sha);      /* the list follows the frame */
        animate = !!animate && !reduced;
        clearTimeout(rpAnimT);
        var prev = n > 0 ? rp.frames[n - 1].text : f.text;
        var rows = window.lcDiffLines ? window.lcDiffLines(prev, f.text)
                 : f.text.split("\n").map(function (l) { return ["same", l]; });
        /* pair each run of − with the run of + right after it, line by line */
        var html = rows.map(function (r) { return escHtml(r[1]); }), marked = [];
        for (var a = 0; a < rows.length; a++) {
          if (rows[a][0] !== "del") continue;
          var d0 = a; while (a < rows.length && rows[a][0] === "del") a++;
          var p0 = a; while (a < rows.length && rows[a][0] === "add") a++;
          for (var q = 0; q < Math.min(p0 - d0, a - p0); q++) {
            var m = wordMarks(rows[d0 + q][1], rows[p0 + q][1]);
            if (m) { html[d0 + q] = m[0]; html[p0 + q] = m[1]; marked[d0 + q] = marked[p0 + q] = true; }
          }
          a--;
        }
        /* TIME TRAVEL KEEPS THE COLOURS (Michel, 2026-10-10): every line not
           word-marked is painted as the editor paints it, and a decoration
           wears its component's icon in the gutter. The fence state follows
           the frame's own text — a removed line never opens or closes one. */
        var ics = [];
        for (var pf = 0, fenceP = null; pf < rows.length; pf++) {
          var rl = rows[pf][1];
          if (!marked[pf]) html[pf] = window.lcPaintMdLine(rl, fenceP);
          var dm = fenceP === null && numbers && rl.match(/^\s*\{:(.*)\}\s*$/);
          ics.push(dm ? ialIcon(dm[1]) : "");
          var fm = /^\s*(`{3,}|~{3,})/.exec(rl);
          if (fm && rows[pf][0] !== "del") fenceP = fenceP === null ? rl.trim().slice(fm[1].length).trim() : null;
        }
        /* the first changed line, as the NEW text counts lines; and each
           row's block in the frame's text, a removed line joining the block
           that follows it — the piano bands the pane and its gutter by block */
        var fb = blocksOf(f.text), changed = -1, firstRow = -1, keys = [], nums = [];
        for (var i = 0, ln = 0; i < rows.length; i++) {
          if (rows[i][0] !== "same" && firstRow < 0) { changed = ln; firstRow = i; }
          if (rows[i][0] === "del") { keys.push(null); nums.push(""); }
          else { keys.push(blockAt(fb, ln)); nums.push(String(ln + 1)); ln++; }
        }
        for (var i2 = rows.length - 1, nextKey = -1; i2 >= 0; i2--) {
          if (keys[i2] === null) keys[i2] = nextKey; else nextKey = keys[i2];
        }
        var changedRows = [], parts = [], open = null;
        var idx = changed < 0 ? -1 : blockAt(fb, changed);
        if (changed >= 0 && idx < 0) { for (var k = 0; k < fb.length; k++) if (fb[k].start > changed) { idx = k; break; } }
        if (changed >= 0 && idx < 0) idx = fb.length - 1;
        rows.forEach(function (r, i) {
          var cls = "ln " + r[0];
          if (animate && r[0] !== "same") { cls += r[0] === "add" ? " unfold" : " fold"; changedRows.push(i); }
          var band = keys[i] < 0 ? "gap" : ((keys[i] % 2 ? "k1" : "k0") + (keys[i] === idx ? " now" : ""));
          if (band !== open) { if (open !== null) parts.push("</div>"); parts.push("<div class='" + band + "'>"); open = band; }
          parts.push("<span class='" + cls + "' data-s='" + (r[0] === "add" ? "+" : r[0] === "del" ? "−" : " ") + "' data-n='" + nums[i] + "'" +
            (ics[i] ? " data-ic='" + ics[i] + "'" + (icGlyph(ics[i]) ? " data-ick='g'" : "") : "") + ">" + (html[i] || "\u00a0") + "</span>");
        });
        if (open !== null) parts.push("</div>");
        rp.diffEl.innerHTML = parts.join("");
        var rowEls = Array.prototype.slice.call(rp.diffEl.querySelectorAll(".ln"));
        /* the preview: a ghost of the old render fades over the new one */
        var total = 0;
        if (animate && out.parentNode) {
          var ghost = out.cloneNode(true);
          ghost.classList.add("lc-mdpad-ghost");
          ghost.style.left = out.offsetLeft + "px"; ghost.style.top = out.offsetTop + "px";
          ghost.style.width = out.offsetWidth + "px"; ghost.style.height = out.offsetHeight + "px";
          wrap.style.position = "relative";
          wrap.appendChild(ghost);
          requestAnimationFrame(function () { ghost.classList.add("go"); });
          setTimeout(function () { if (ghost.parentNode) ghost.parentNode.removeChild(ghost); }, 400);
        }
        render(f.text);
        if (animate && changedRows.length) {
          /* one line after the other, the whole run inside half the frame */
          var step = Math.max(15, Math.min(80, (pace * 1000 * 0.5) / changedRows.length));
          changedRows.forEach(function (ri, k) { rowEls[ri].style.setProperty("--d", (k * step / 1000) + "s"); });
          total = changedRows.length * step + 350;
          wrap.setAttribute("data-lc-animating", "1");
          requestAnimationFrame(function () {
            changedRows.forEach(function (ri) { var e = rowEls[ri]; if (e) e.classList.add("go"); });
          });
          rpAnimT = setTimeout(function () {
            wrap.removeAttribute("data-lc-animating");
            focusPreview(idx, fb);                  /* the pulse lands as the last line settles */
          }, total);
        } else {
          focusPreview(idx, fb);
        }
        var sp = firstRow >= 0 ? rowEls[firstRow] : null;
        rp.diffEl.scrollTop = sp ? Math.max(0, sp.offsetTop - rp.diffEl.offsetTop - 40) : 0;
        rp.ui.slider.value = String(n);
        rp.ui.label.textContent = (n + 1) + " / " + rp.frames.length + " · " +
          (f.starter ? "the lesson's starter" : (f.when ? new Date(f.when).toLocaleString() : "saved"));
        wrap.setAttribute("data-lc-frame", String(n));
        rp.changedEl = sp;
        if (wrap.hasAttribute("data-lc-playing")) { rpSay(f); setTimeout(rpPlace, total + 30); }
      }
      /* THE COMMIT SPEAKS (Michel, 2026-10-10): while ▶ Play or ◀ Moonwalk
         runs, the frame's own line — what the learner said they did — floats
         as a subtitle, 🤓 first, capitalised, half-seen, the way Doc's bubble
         walks a screen. It sits on the EDITOR, right under the lines that
         changed, and follows them frame to frame: the words beside the
         syntax they name, for students to recognise it. Paused, it fades. */
      function rpLine(f) {
        if (f.starter) return "The lesson's starter";
        var t = String(f.message || "").split("\n")[0].replace(/^[^\p{L}\p{N}]+/u, "").trim();
        return t ? t.charAt(0).toUpperCase() + t.slice(1) : "";
      }
      function rpSay(f) {
        var line = rpLine(f);
        if (!line) { rpHush(); return; }
        if (!rp.sub) {
          rp.sub = document.createElement("div");
          rp.sub.className = "lc-mdpad-sub";
          rp.sub.setAttribute("role", "status");
          wrap.style.position = "relative";
          wrap.appendChild(rp.sub);
        }
        rp.sub.textContent = "🤓 " + line;
        rpPlace();
        rp.sub.classList.add("on");
      }
      function rpPlace() {
        if (!rp.sub || !rp.diffEl) return;
        var W = wrap.getBoundingClientRect(), D = rp.diffEl.getBoundingClientRect();
        var y = D.top + 24;
        if (rp.changedEl && rp.changedEl.isConnected) {
          /* the last changed row of the run, so the words sit under the change */
          var last = rp.changedEl, nx = last.nextElementSibling;
          while (nx && /\b(add|del)\b/.test(nx.className)) { last = nx; nx = nx.nextElementSibling; }
          y = last.getBoundingClientRect().bottom + 6;
        }
        y = Math.max(D.top + 8, Math.min(y, D.bottom - 40));
        rp.sub.style.maxWidth = Math.round(D.width * 0.9) + "px";
        rp.sub.style.left = (D.left - W.left + D.width / 2) + "px";
        rp.sub.style.top = (y - W.top) + "px";
      }
      function rpHush() { if (rp.sub) rp.sub.classList.remove("on"); }
      function rpPause() {
        if (rp.timer) clearInterval(rp.timer);
        rp.timer = null;
        if (rp.ui) { rp.ui.play.textContent = "▶ Play"; rp.ui.back.textContent = "◀ Moonwalk"; }
        wrap.removeAttribute("data-lc-playing");
        setTimeout(function () { if (!rp.timer) rpHush(); }, 1200);   /* the last line is read, then fades */
      }
      function rpStep() {
        var n = rp.at + rp.dir;
        if (n < 0 || n >= rp.frames.length) { rpPause(); return; }
        rpShow(n, true);
        /* landed on an end: stop there, now, not one silent tick later */
        if (n === 0 || n === rp.frames.length - 1) rpPause();
      }
      function rpPlay(dir) {
        rpPause();
        rp.dir = dir;
        /* pressed at an end: start again from the other end */
        if (dir > 0 && rp.at >= rp.frames.length - 1) rpShow(0);
        if (dir < 0 && rp.at <= 0) rpShow(rp.frames.length - 1);
        rp.timer = setInterval(rpStep, pace * 1000);
        wrap.setAttribute("data-lc-playing", dir > 0 ? "forward" : "backward");
        rpSay(rp.frames[rp.at]);
        if (dir > 0) rp.ui.play.textContent = "⏸ Pause"; else rp.ui.back.textContent = "⏸ Pause";
      }
      function rpStart() {
        if (rp.on || !window.lcBench) return Promise.resolve();
        /* ONE replay, however many clicks: a row picked while the frames
           are still loading joins the start in flight instead of starting
           a second one — two slider bars and a strip-high second diff pane,
           measured on an already hidden editor (Michel, 2026-10-06). */
        if (rp.starting) return rp.starting;
        setPlay("⏳ reading your versions…", true);
        rp.starting = rpLoad().then(function (frames) {
          if (!frames.length) {
            setPlay("🎞 Replay", false);
            if (window.lcxToast) window.lcxToast("No versions yet — 💾 writes the first one.", true);
            return;
          }
          rp.on = true;
          setPlay("■ Stop", false);
          wrap.setAttribute("data-lc-replay", "1");
          wrap.setAttribute("data-lc-frames", String(frames.length));
          /* the list stays open: its rows are the frames, and 🕘 keeps working */
          [saveBtn, resetBtn].forEach(function (b) { if (b) b.disabled = true; });
          setFold(false);                 /* a replay needs the pane it measures */
          var pane = src || ta;
          rp.diffEl = document.createElement("pre");
          rp.diffEl.className = "lc-mdpad-diff lc-md-paint";
          rp.diffEl.setAttribute("aria-label", "This version, with what changed since the one before");
          /* THE PANE KEEPS THE EDITOR'S HEIGHT (Michel, 2026-10-05): a frame's
             length must not move the bar under the pad — the pane scrolls
             inside, to the first change, as the editor would. */
          if (numbers) rp.diffEl.setAttribute("data-numbers", "1");
          if (piano) rp.diffEl.setAttribute("data-piano", "1");
          /* ON A PHONE the pad stacks (column): a basis of 0 would squeeze
             the pane to a strip (Michel, 2026-10-06, "time travelling
             squeezes the editor"), so there it keeps its own height; side
             by side it shares the width as the editor did. */
          var column = getComputedStyle(wrap).flexDirection === "column";
          rp.diffEl.style.height = pane.offsetHeight + "px";
          rp.diffEl.style.flex = column ? "0 0 auto" : "1 1 0";
          /* THE PREVIEW KEEPS ITS SIZE TOO: a frame's length must not grow
             the pad and push the page around — the preview scrolls to the
             change instead (focusPreview). On a phone, at most a screen's
             worth, so the pad, the slider and the list stay in reach. */
          var oh = out.offsetHeight;
          if (column) oh = Math.min(oh, Math.round(window.innerHeight * 0.6));
          out.style.boxSizing = "border-box";       /* the measured height is the padded one */
          out.style.height = oh + "px";
          if (column) out.style.flex = "0 0 auto";
          wrap.insertBefore(rp.diffEl, pane);
          pane.style.display = "none";
          var box = document.createElement("div");
          box.className = "lc-mdpad-replaybar";
          function mk(text, cls) { var b = document.createElement("button"); b.type = "button"; b.className = cls; b.textContent = text; return b; }
          rp.ui = { box: box, back: mk("◀ Moonwalk", "lc-mdpad-back"), play: mk("▶ Play", "lc-mdpad-play"),
                    slider: document.createElement("input"), label: document.createElement("span") };
          rp.ui.slider.type = "range"; rp.ui.slider.min = "0"; rp.ui.slider.max = String(frames.length - 1);
          rp.ui.slider.step = "1"; rp.ui.slider.setAttribute("aria-label", "Version");
          rp.ui.label.className = "lc-mdpad-frame";
          box.appendChild(rp.ui.back); box.appendChild(rp.ui.play); box.appendChild(rp.ui.slider); box.appendChild(rp.ui.label);
          saveWrap.parentNode.insertBefore(box, saveWrap);
          rp.ui.slider.addEventListener("input", function () { rpPause(); rpShow(+rp.ui.slider.value); });
          rp.ui.play.addEventListener("click", function () { rp.timer && rp.dir > 0 ? rpPause() : rpPlay(1); });
          rp.ui.back.addEventListener("click", function () { rp.timer && rp.dir < 0 ? rpPause() : rpPlay(-1); });
          rpShow(0);
        }).then(function () { rp.starting = null; }, function (e) { rp.starting = null; throw e; });
        return rp.starting;
      }
      function rpStop() {
        if (!rp.on) return;
        rpPause();
        clearTimeout(rpAnimT);
        wrap.removeAttribute("data-lc-animating");
        wrap.querySelectorAll(".lc-mdpad-ghost").forEach(function (g) { g.parentNode.removeChild(g); });
        rp.on = false;
        setPlay("🎞 Replay", false);
        if (vers && vers.mark) vers.mark(null);
        ["data-lc-replay", "data-lc-frame", "data-lc-frames"].forEach(function (a) { wrap.removeAttribute(a); });
        if (rp.diffEl && rp.diffEl.parentNode) rp.diffEl.parentNode.removeChild(rp.diffEl);
        if (rp.sub && rp.sub.parentNode) rp.sub.parentNode.removeChild(rp.sub);
        rp.sub = null;
        if (rp.ui && rp.ui.box.parentNode) rp.ui.box.parentNode.removeChild(rp.ui.box);
        rp.diffEl = null; rp.ui = null;
        (src || ta).style.display = "";
        out.style.height = ""; out.style.flex = ""; out.style.boxSizing = "";   /* the preview breathes again */
        refreshBench();                 /* 💾 and ↺ decide their own state again */
        rp.frames = null;               /* a save in between adds a frame: read again next time */
        lastFocus = -2; render(); focusNow();
      }
      /* a proof drives it as a person would: pad.replay(), pad.frame = n, pad.stop() */
      wrap._lcReplay = { start: rpStart, stop: rpStop, play: rpPlay, pause: rpPause,
                         go: function (n) { if (rp.on) { rpPause(); rpShow(n); } } };
    }

    /* ── WIRES: the preview's model is what its text declares ──────────────
       A student (Michel, 2026-10-08): the dataset fence deleted, the grid
       still showed its rows; the id renamed, nothing visibly broke. The
       registry is page-wide and forgot nothing, so a wire kept finding the
       old object. Two rules now. (1) An id this pad declared and no longer
       does leaves the registry with the render — no save, no reload.
       (2) A wire (source= master= bound= target=) to an id the page does not
       have is DRAWN broken: a dashed frame naming the missing id on the
       block, one chip over the preview, data-lc-broken for a proof. */
    var WIRE_RE = /\b(source|master|bound|target)\s*=\s*"([^"]*)"/g, ID_RE = /#([A-Za-z_][\w-]*)/g;
    function wiresOf(text) {
      var lines = text.split("\n"), bl = blocksOf(text), ids = {}, wires = [], fence = null;
      for (var i = 0; i < lines.length; i++) {
        var t = lines[i].trim(), fm = t.match(/^(`{3,}|~{3,})/);
        if (fence) { if (fm && fm[1].charAt(0) === fence.charAt(0) && fm[1].length >= fence.length && /^(`{3,}|~{3,})$/.test(t)) fence = null; continue; }
        if (fm) { fence = fm[1]; continue; }
        var ial = t.match(/^\{:(.*)\}$/);
        if (!ial) continue;
        var m;
        ID_RE.lastIndex = 0;
        while ((m = ID_RE.exec(ial[1]))) ids[m[1]] = true;
        WIRE_RE.lastIndex = 0;
        while ((m = WIRE_RE.exec(ial[1]))) {
          /* only a plain id is a wire to this page: an expression, a file or
             a repo path names something else */
          if (/^[A-Za-z_][\w-]*$/.test(m[2])) wires.push({ block: blockAt(bl, i), kind: m[1], id: m[2] });
        }
      }
      return { ids: ids, wires: wires };
    }
    var prevIds = {}, wiresEl = null;
    /* one source block = one top-level element — except a beside= row, which
       stands for as many blocks as it holds (the scan folded them) */
    function blockEl(idx) {
      for (var i = 0; i < body.children.length; i++) {
        var c = body.children[i], n = (c.classList.contains("lc-blocks") && c.hasAttribute("data-lc-beside")) ? c.children.length : 1;
        if (idx < n) return n === 1 ? c : c.children[idx];
        idx -= n;
      }
      return null;
    }
    function forgetGone(cur) {
      Object.keys(prevIds).forEach(function (id) {
        if (cur.ids[id] || !window.lcDatasets || !(id in window.lcDatasets)) return;
        delete window.lcDatasets[id];
        if (window.lcDatasetListeners) delete window.lcDatasetListeners[id];
      });
      prevIds = cur.ids;
    }
    function markWires(cur) {
      var broken = [];
      cur.wires.forEach(function (w) {
        if (cur.ids[w.id]) return;
        if (window.lcDatasets && (w.id in window.lcDatasets)) return;   /* the page's own data */
        var outside = document.getElementById(w.id) || document.getElementById("lc-pyrun-" + w.id);
        if (outside && !wrap.contains(outside)) return;                  /* a part of the page around */
        var label = w.kind + " «" + w.id + "»", el = blockEl(w.block);
        if (el && el.nodeType === 1) {
          el.classList.add("lc-mdpad-broken");
          el.setAttribute("data-lc-broken", (el.getAttribute("data-lc-broken") ? el.getAttribute("data-lc-broken") + ", " : "") + label);
        }
        broken.push(label);
      });
      if (broken.length) {
        if (!wiresEl) { wiresEl = document.createElement("div"); wiresEl.className = "lc-mdpad-wires"; wiresEl.setAttribute("role", "status"); }
        wiresEl.textContent = "⚠ " + broken.length + " broken wire" + (broken.length > 1 ? "s" : "") + ": " + broken.join(", ") + " — no such id on this page";
        if (wiresEl.parentNode !== out) out.insertBefore(wiresEl, out.firstChild);
        wrap.setAttribute("data-lc-broken", String(broken.length));
      } else {
        if (wiresEl && wiresEl.parentNode) wiresEl.parentNode.removeChild(wiresEl);
        wrap.removeAttribute("data-lc-broken");
      }
    }
    function render(text) {
      var v = typeof text === "string" ? text : ta.value;   /* a replay frame, else the editor */
      if (!window.marked) {
        body.innerHTML = "<pre>" + v.replace(/[&<]/g, function (c) { return c === "&" ? "&amp;" : "&lt;"; }) + "</pre>";
        return;
      }
      var inline = window.lcInlineIAL || function (h) { return h; };
      if (!deco) { body.innerHTML = inline(window.marked.parse(v)); return; }
      /* decorations: the runner's pipeline on the preview — IAL on its own
         paragraph, block IAL applied, then the same scan that upgrades a
         page's fences into components, and the cells inside them */
      var norm = window.lcNormIAL ? window.lcNormIAL(v) : v.replace(/([^\n])\n(\{:)/g, "$1\n\n$2");
      var cur = wiresOf(v);
      forgetGone(cur);                      /* what the text no longer declares is gone */
      body.innerHTML = inline(window.marked.parse(norm));
      if (window.lcApplyIAL) window.lcApplyIAL(body);
      if (window.lcScanElement) window.lcScanElement(body);
      if (window.lcCellsRescan) window.lcCellsRescan();
      markWires(cur);                       /* a wire to nothing is drawn as such */
      if (appTitle) {
        var h1 = body.querySelector("h1");
        appTitle.textContent = (h1 && h1.textContent.trim()) || benchPath;
      }
    }
    /* ── FOCUS: the block under the caret, shown on both sides ── */
    var blocks = blocksOf(ta.value), lastFocus = -2;
    function caretLine() { return ta.value.slice(0, ta.selectionStart || 0).split("\n").length - 1; }
    function caretBlock() { return blockAt(blocks, caretLine()); }
    function focusPreview(idx, bl) {
      bl = bl || blocks;
      body.querySelectorAll(".lc-mdpad-focus").forEach(function (e) { e.classList.remove("lc-mdpad-focus"); });
      if (idx < 0 || !bl[idx]) return;
      var target = null, hm = bl[idx].head.match(/^\s*#{1,6}\s+(.*)$/);
      if (hm) {
        var want = hm[1].replace(/[*_`#]/g, "").trim().toLowerCase();
        var hs = body.querySelectorAll("h1,h2,h3,h4,h5,h6");
        for (var i = 0; i < hs.length && !target; i++)
          if (hs[i].textContent.trim().toLowerCase() === want) target = hs[i];
      }
      if (!target) target = blockEl(idx);
      if (!target) return;
      void target.offsetWidth;
      target.classList.add("lc-mdpad-focus");
      /* bring it into the preview's own view — never scroll the page */
      var scroller = body === out ? out : body;
      var box = scroller.getBoundingClientRect(), r = target.getBoundingClientRect();
      if (r.top < box.top) scroller.scrollTop -= (box.top - r.top) + 8;
      else if (r.bottom > box.bottom) scroller.scrollTop += (r.bottom - box.bottom) + 8;
    }
    /* ── COLOURS IN THE SOURCE (Michel, 2026-10-08: "to help learners match
       the components"). The mirror under the textarea already holds every
       line (the piano); now the line is painted — a fence and its body
       muted, a {: … } decoration on its own lighter band with the class,
       the #id and each knob in their colours, headings, links, emphasis —
       and the textarea's own text is transparent over it, caret kept.
       One painter, line by line; the fence state carries across lines. */
    var FENCE_RE = /^\s*(`{3,}|~{3,})/;
    /* the painter is shared with the read-only .code snippets (widgets.md):
       a snippet on the lesson and the pad beside it wear the same colours */
    function paintLine(raw, fence) { return window.lcPaintMdLine(raw, fence); }
    function paintPiano() {
      if (!keysEl) return;
      var cs = getComputedStyle(ta);
      ["fontFamily", "fontSize", "lineHeight", "letterSpacing", "tabSize", "paddingTop", "paddingLeft",
       "paddingBottom", "borderTopWidth", "borderLeftWidth", "borderRightWidth", "borderBottomWidth"]
        .forEach(function (k) { keysEl.style[k] = cs[k]; });
      /* the textarea's scrollbar narrows ITS text; mirror that or long lines wrap apart */
      var bar = ta.offsetWidth - ta.clientWidth - parseFloat(cs.borderLeftWidth) - parseFloat(cs.borderRightWidth);
      keysEl.style.paddingRight = (parseFloat(cs.paddingRight) + Math.max(0, bar)) + "px";
      /* fence: null outside, else its info string ("csv", "" …) — a CSV
         fence paints its columns in turns */
      var lines = ta.value.split("\n"), now = caretBlock(), here = caretLine(), html = "", li = 0, fence = null;
      function line(n) {
        var ial = fence === null && numbers && lines[n].match(/^\s*\{:(.*)\}\s*$/);
        var ic = ial ? ialIcon(ial[1]) : "";
        var h = "<div class='ln" + (n === here ? " here" : "") + "' data-n='" + (n + 1) + "'" +
          (ic ? " data-ic='" + ic + "'" + (icGlyph(ic) ? " data-ick='g'" : "") : "") + ">" + paintLine(lines[n], fence) + "</div>";
        var m = FENCE_RE.exec(lines[n]);
        if (m) fence = fence === null ? lines[n].trim().slice(m[1].length).trim() : null;
        return h;
      }
      blocks.forEach(function (b, i) {
        for (; li < b.start; li++) html += line(li);
        html += "<div class='" + (i % 2 ? "k1" : "k0") + (i === now ? " now" : "") + "'>";
        for (; li <= b.end; li++) html += line(li);
        html += "</div>";
      });
      for (; li < lines.length; li++) html += line(li);
      keysEl.innerHTML = html;
      keysEl.scrollTop = ta.scrollTop;
    }
    /* A KEYSTROKE PATCHES ONE TEXT NODE (2026-10-08): rebuilding the mirror
       removes nodes, and Chromium then closes the typing group — ⌘Z took
       one character at a time. The edit lands in the mirror's own text
       node; the colours catch up on a pause. A change across lines, or a
       line emptied, repaints at once — a fair place for undo to stop. */
    var lastVal = ta.value, _paintT = null;
    function paintSoon() { clearTimeout(_paintT); _paintT = setTimeout(paintPiano, 250); }
    function patchOneLine(prev, next) {
      var a = 0, pb = prev.length, nb = next.length;
      while (a < pb && a < nb && prev[a] === next[a]) a++;
      while (pb > a && nb > a && prev[pb - 1] === next[nb - 1]) { pb--; nb--; }
      if (prev.slice(a, pb).indexOf("\n") >= 0 || next.slice(a, nb).indexOf("\n") >= 0) return false;
      var li = next.slice(0, a).split("\n").length - 1;
      var ls = next.lastIndexOf("\n", a - 1) + 1, le = next.indexOf("\n", a); if (le < 0) le = next.length;
      var line = next.slice(ls, le), col = a - ls, removed = pb - a, inserted = next.slice(a, nb);
      if (!line) return false;
      var div = keysEl.querySelector(".ln[data-n='" + (li + 1) + "']");
      if (!div) return false;
      var walker = document.createTreeWalker(div, NodeFilter.SHOW_TEXT), node, nodes = [], pos = 0;
      while ((node = walker.nextNode())) nodes.push(node);
      if (nodes.length === 1 && nodes[0].data === " ") { nodes[0].data = line; return true; }
      for (var i = 0; i < nodes.length; i++) {
        var len = nodes[i].data.length;
        if (col >= pos && col + removed <= pos + len && (col < pos + len || i === nodes.length - 1)) {
          var d = nodes[i].data;
          nodes[i].data = d.slice(0, col - pos) + inserted + d.slice(col - pos + removed);
          return div.textContent === line;
        }
        if (col < pos + len) return false;
        pos += len;
      }
      return false;
    }
    function focusNow() {
      var idx = caretBlock();
      if (idx !== lastFocus) {
        lastFocus = idx;
        focusPreview(idx);
        if (idx >= 0) wrap.setAttribute("data-lc-focus", String(idx)); else wrap.removeAttribute("data-lc-focus");
      }
      paintSoon();
    }
    var _focT = null;
    function focusSoon() { clearTimeout(_focT); _focT = setTimeout(focusNow, 150); }
    ta.addEventListener("click", focusSoon);
    ta.addEventListener("keyup", focusSoon);
    ta.addEventListener("select", focusNow);
    ta.addEventListener("input", function () {
      var next = ta.value, patched = patchOneLine(lastVal, next);
      lastVal = next; blocks = blocksOf(next);
      if (patched) paintSoon(); else paintPiano();
    });
    if (keysEl) {
      ta.addEventListener("scroll", function () { keysEl.scrollTop = ta.scrollTop; });
      if (window.ResizeObserver) new ResizeObserver(paintPiano).observe(ta);
    }
    /* a proof moves the caret the way a person would: pad.caret = n */
    wrap._lcCaret = function (pos) { ta.focus(); ta.setSelectionRange(pos, pos); blocks = blocksOf(ta.value); focusNow(); paintPiano(); };
    /* a proof writes the pad as a person would (pad.source = "…"): one render, now */
    wrap._lcApply = function (t) {
      ta.value = t; lastVal = t; render(); publish(true); paintPiano();
      if (typeof refreshBench === "function") refreshBench();
      blocks = blocksOf(ta.value);
    };

    var _renT = null;
    ta.addEventListener("input", deco
      ? function () { clearTimeout(_renT); _renT = setTimeout(render, 350); }
      : render);
    ta.addEventListener("input", function () {
      /* edited since the last save: a proof reading this pad says so */
      if (benchPath) {
        if (ta.value !== bOrigin) wrap.setAttribute("data-lc-dirty", "1");
        else wrap.removeAttribute("data-lc-dirty");
        if (typeof refreshBench === "function") refreshBench();
      }
      clearTimeout(_pubT);
      _pubT = setTimeout(function () { publish(true); }, 400);
    });
    publish(false);  /* the seed is data too — no recompute storm on load */
    render();  /* show the seed immediately (escaped) … */
    if (window.lcLoadMarked) window.lcLoadMarked(render);  /* … then with marked */
    if (keysEl) paintPiano();
    if (keysEl && numbers) compIcons().then(function (m) { _icons = m; paintPiano(); });
  }

  /* code_chrome.md provides the scan registry; one registration covers the
     initial scan and every re-scan. */
  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader(".highlighter-rouge.mdpad, pre.mdpad", upgradeMdpad);
  }
})();
</script>
