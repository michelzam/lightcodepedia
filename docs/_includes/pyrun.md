{%- comment -%}
PyRun — the in-browser Python family, activated from md + IAL.

  python code block + {: .run }     editor with ▶ Run, doctests, show.grid/form
  python code block + {: .repl }    interactive REPL
  {: .run silent="true" }           executes on load, renders nothing
  link + {: .button }               styled button; an adjacent {: .onclick }
                                    Python block becomes its click handler

MicroPython (lazy-loaded, ~300 KB) runs the editor; buttons run on the
shared page instance against the steps-runtime preamble. CPython's
f'{x = }' is rewritten before the code reaches it (desugarFstrings). Exposes
window.lcPyrun.attach for Liquid-rendered python_run.md blocks and
flushes their lcPyrunQueue.

Auto-included by docs/_layouts/default.html.
{%- endcomment -%}

<style>
.lc-pyrun { border: 1px solid #d0d0d0; border-radius: 8px; overflow: hidden; margin: 1em 0; background: white; }
.lc-pyrun-title { background: #f3f4f6; padding: 0.45em 0.9em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; color: #444; border-bottom: 1px solid #d0d0d0; display: flex; align-items: center; gap: 0.5em; }
.lc-pyrun-title .lc-pyrun-lang { margin-left: auto; font-size: 0.75em; text-transform: uppercase; color: var(--lc-ink-mute, #616161); letter-spacing: 0.05em; }
.lc-pyrun textarea { display: block; width: 100%; box-sizing: border-box; border: none; outline: none; padding: 0.9em 1em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; line-height: 1.5; resize: none; background: #fafafa; color: #111; }   /* the grip below is the one handle (Michel, 2026-10-27: the corner one was "not useful and not in sync") */
.lc-pyrun-editor { display: flex; background: #fafafa; align-items: stretch; }
.lc-pyrun-codewrap { position: relative; flex: 1; min-width: 0; }
.lc-pyrun-codewrap .lc-pyrun-code { flex: none; width: 100%; padding-left: 0.6em; }
.lc-pyrun-hl { position: absolute; top: 0; left: 0; right: 0; bottom: 0; margin: 0; padding: 0.9em 1em 0.9em 0.6em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; line-height: 1.5; pointer-events: none; overflow: hidden; background: transparent; color: #111; white-space: pre-wrap; word-wrap: break-word; box-sizing: border-box; }
.lc-pyrun-hl code { font: inherit; background: transparent; padding: 0; color: inherit; display: block; will-change: transform; }
.lc-pyrun-codewrap .lc-pyrun-code { position: relative; background: transparent !important; color: transparent !important; caret-color: #111; }
.lc-pyrun-codewrap .lc-pyrun-code::selection { background: rgba(0, 102, 204, 0.18); color: transparent; }
.lc-pyrun .token.keyword, .lc-pyrun .token.boolean, .lc-pyrun .token.null { color: #cf222e; font-weight: 700; }   /* keywords bold (Michel, 2026-10-27) */
.lc-pyrun .token.string, .lc-pyrun .token.triple-quoted-string { color: #0a3069; }
.lc-pyrun .token.number { color: #0550ae; }
.lc-pyrun .token.comment { color: #59636e; font-style: italic; }
.lc-pyrun .token.function, .lc-pyrun .token.class-name, .lc-pyrun .token.builtin, .lc-pyrun .token.decorator { color: #8250df; }
.lc-pyrun .token.operator, .lc-pyrun .token.punctuation { color: #24292f; }
/* CODE DOES NOT WRAP (Michel, 2026-10-06/07). An overlay editor can only
   disagree with its caret where a line wraps, so a long line scrolls
   sideways instead; the overlay follows scrollLeft. By CSS alone: the
   first cut (wrap="off" + overflow:auto as well) left the editor
   read-only on the iPhone (WebKit), and this is the smallest piece.
   The gutter still measures rows through a mirror that copies the
   editor's white-space: true either way, one number per line. */
.lc-pyrun-code, .lc-pyrun-hl { white-space: pre; word-wrap: normal; overflow-wrap: normal; }
.lc-pyrun-mirror { position: absolute; top: 0; left: 0; visibility: hidden; pointer-events: none; box-sizing: border-box; margin: 0; }
.lc-pyrun-mirror div { min-height: 1.5em; }
.lc-pyrun-gutter { position: relative; overflow: hidden; background: #f3f4f6; border-right: 1px solid #e8e8e8; user-select: none; min-width: 2.5em; }
.lc-pyrun-gutter-inner { padding: 0.9em 0.5em 0.9em 0.6em; color: var(--lc-ink-mute, #616161); font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; line-height: 1.5; text-align: right; white-space: pre; pointer-events: none; will-change: transform; }
.lc-pyrun-bar { display: flex; align-items: center; gap: 0.6em; padding: 0.5em 0.9em; background: #f3f4f6; border-top: 1px solid #e0e0e0; }
.lc-pyrun-bar button { background: #0066cc; color: white; border: none; border-radius: 4px; padding: 0.35em 0.9em; cursor: pointer; font-size: 0.85em; font-weight: 500; }
.lc-pyrun-bar button:hover:not(:disabled) { background: #0052a3; }
.lc-pyrun-bar button:disabled { background: #888; cursor: progress; }
.lc-pyrun-bar .lc-pyrun-clear { background: #e5e5e5; color: #333; }
.lc-pyrun-bar .lc-pyrun-clear:hover:not(:disabled) { background: #d0d0d0; }
.lc-pyrun-bar .lc-pyrun-test { background: #3d7330; }
.lc-pyrun-bar .lc-pyrun-test:hover:not(:disabled) { background: #33641f; }
.lc-pyrun-bar .lc-pyrun-status { margin-left: auto; font-size: 0.78em; color: #666; }
/* 💬 SUBTITLES (Michel, 2026-10-27): an overlay over the editor where every
   part of the program says what it is — hover on a laptop, tap on a phone,
   the line under the bar repeats it. Reading mode: the editor waits below. */
.lc-pyrun-subs { position: absolute; top: 0; left: 0; right: 0; bottom: 0; margin: 0; padding: 0.9em 1em 0.9em 0.6em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; line-height: 1.5; background: #fafafa; color: #111; overflow: auto; white-space: pre; box-sizing: border-box; z-index: 2; }
.lc-pyrun-subs[hidden] { display: none; }
.lc-pyrun-subtitled .lc-pyrun-code { pointer-events: none; }
.lc-pyrun-subs .lc-sub { border-bottom: 1px dotted #8250df; cursor: help; border-radius: 2px; }
.lc-pyrun-subs .lc-sub-kw { color: #cf222e; font-weight: 700; }
.lc-pyrun-subs .lc-sub-string { color: #0a3069; }
.lc-pyrun-subs .lc-sub-number { color: #0550ae; }
.lc-pyrun-subs .lc-sub-comment { color: #59636e; font-style: italic; }
.lc-pyrun-subs .lc-sub-def, .lc-pyrun-subs .lc-sub-builtin { color: #8250df; }
.lc-pyrun-subs .lc-sub-line { display: block; min-height: 1.5em; }
.lc-pyrun-subs .lc-sub-line.lc-sub-hidden { display: none; }
.lc-pyrun-folds { position: absolute; top: 0; left: 0; right: 0; bottom: 0; pointer-events: none; }
.lc-pyrun-folds[hidden] { display: none; }
.lc-pyrun-gfold { position: absolute; left: 0.1em; width: 1em; height: 1.5em; padding: 0; border: none; background: transparent; color: #8250df; cursor: pointer; pointer-events: auto; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; line-height: 1.5; }
.lc-pyrun-subtitled .lc-pyrun-gutter-inner { padding-left: 1.3em; }
.lc-pyrun-subs .lc-sub:hover, .lc-pyrun-subs .lc-sub.lc-sub-on { background: #efe6ff; }
.lc-pyrun-subline { padding: 0.5em 0.9em; font-size: 0.85em; background: #faf5ff; border-top: 1px solid #e9d8ff; color: #3b2a63; }
.lc-pyrun-subline[hidden] { display: none; }
.lc-pyrun-subline code { background: #efe6ff; padding: 0 0.3em; border-radius: 3px; }
/* ↕ THE GRIP (Michel, 2026-10-27: "a vertical resizing handle, like mdpad"):
   a bar under the editor, dragged, sets its height for this visit; a double-click gives the program's own height back */
.lc-pyrun-grip { height: 0.75em; cursor: ns-resize; touch-action: none; display: flex; align-items: center; justify-content: center; background: #f3f4f6; border-top: 1px solid #e8e8e8; }
.lc-pyrun-grip::before { content: ""; width: 3.2em; height: 4px; border-radius: 3px; background: #c4c9d4; }
.lc-pyrun-grip:hover::before, .lc-pyrun[data-lc-resizing] .lc-pyrun-grip::before { background: #0066cc; }
.lc-pyrun-bar .lc-pyrun-icon { background: transparent; color: #333; padding: 0.25em 0.45em; font-size: 1em; border: 1px solid transparent; }
.lc-pyrun-bar .lc-pyrun-icon:hover:not(:disabled) { background: #e5e5e5; border-color: #d0d0d0; }
.lc-pyrun-bar .lc-pyrun-icon:disabled { background: transparent; opacity: 0.5; }
.lc-pyrun-bar .lc-pyrun-switch { background: transparent; color: #333; display: inline-flex; align-items: center; gap: 0.35em; padding: 0.25em 0.45em; font-size: 1em; border: 1px solid transparent; }
.lc-pyrun-bar .lc-pyrun-switch:hover:not(:disabled) { background: #e5e5e5; border-color: #d0d0d0; }
.lc-pyrun-track { display: inline-block; width: 26px; height: 14px; border-radius: 7px; background: #c9c9c9; position: relative; transition: background 0.15s; }
.lc-pyrun-knob { position: absolute; top: 2px; left: 2px; width: 10px; height: 10px; border-radius: 50%; background: #fff; transition: left 0.15s; }
.lc-pyrun-switch[aria-checked="true"] .lc-pyrun-track { background: #8250df; }
.lc-pyrun-switch[aria-checked="true"] .lc-pyrun-knob { left: 14px; }
/* 💡 COMPLETION (Michel, 2026-10-27: "code completion, a bit like in mdpad"):
   Ctrl+Space, or a word of two letters, lists what fits — keywords, the
   helpers, the program's own names, an object's attributes after a dot */
.lc-pyrun-comp { position: absolute; z-index: 6; min-width: 14em; max-width: 24em; max-height: 13em; overflow: auto; background: #fff; border: 1px solid #c8c8c8; border-radius: 6px; box-shadow: 0 6px 18px rgba(0,0,0,0.12); font-size: 0.85em; }
.lc-pyrun-comp .o { display: flex; gap: 0.5em; align-items: baseline; padding: 0.2em 0.6em; cursor: pointer; white-space: nowrap; }
.lc-pyrun-comp .o.on { background: #dbeafe; }
.lc-pyrun-comp .l { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-weight: 600; }
.lc-pyrun-comp .d { color: #777; overflow: hidden; text-overflow: ellipsis; }
/* ✨ THE SAME SYMBOL, LIT (Michel, 2026-10-27: "flash the other occurrences
   of a given symbol when selected"): a layer under the colours marks every
   other occurrence of the selected word */
.lc-pyrun-marks { position: absolute; top: 0; left: 0; right: 0; bottom: 0; margin: 0; padding: 0.9em 1em 0.9em 0.6em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; line-height: 1.5; pointer-events: none; overflow: hidden; background: transparent; color: transparent; white-space: pre; word-wrap: normal; box-sizing: border-box; }
.lc-pyrun-marks code { font: inherit; background: transparent; padding: 0; color: inherit; display: block; will-change: transform; }
.lc-pyrun-marks mark { background: #fff2a8; color: transparent; border-radius: 2px; box-shadow: 0 0 0 1px #f5d76e; }
.lc-pyrun-out { margin: 0; padding: 0.9em 1em; background: #1e1e1e; color: #d4d4d4; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; line-height: 1.5; white-space: pre-wrap; min-height: 2em; max-height: 300px; overflow-y: auto; }
.lc-pyrun-out.lc-empty { color: #888; font-style: italic; }
.lc-pyrun-out .lc-err { color: #ff6b6b; }
/* the question, and the line the reader answers on — a terminal's own look:
   the caret sits where the prompt ends, and Enter sends it */
.lc-pyrun-ask { display: inline; }
.lc-pyrun-ask-box { background: transparent; border: 0; border-bottom: 1px solid #4d4d4d;
  color: #9cdcfe; font: inherit; outline: none; min-width: 8em; padding: 0 0.15em; caret-color: #9cdcfe; }
.lc-pyrun-ask-box:focus { border-bottom-color: #9cdcfe; }
.lc-pyrun-view { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; padding: 0.9em 1em; background: #fafbfc; border-top: 1px solid #e0e0e0; }
.lc-pyrun-view:empty { display: none; }
.lc-pyrun-view .lc-rt-card { border: 1px solid #e0e0e0; border-radius: 8px; padding: 0.8em 1em; background: white; transition: transform 0.15s, box-shadow 0.15s; }
.lc-pyrun-view .lc-rt-card:hover { transform: translateY(-2px); box-shadow: 0 4px 14px rgba(0,0,0,0.06); border-color: #0066cc; }
.lc-pyrun-view .lc-rt-card h3 { margin: 0 0 0.4em; font-size: 1em; color: #222; }
.lc-pyrun-view .lc-rt-card .lc-rt-row { margin: 0.15em 0; font-size: 0.88em; color: #444; }
.lc-pyrun-view .lc-rt-card .lc-rt-row b { color: #0066cc; margin-right: 0.4em; }
.lc-pyrun-view .lc-rt-card .lc-rt-val { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.88em; color: #333; word-break: break-word; }
.lc-pyrun-bound { padding: 0.9em 1em; background: #fafbfc; border-bottom: 1px solid #d0d0d0; }
.lc-pyrun-bound:empty { display: none; }
.lc-pyrun-bound .lc-rt-card { border: 1px solid #e0e0e0; border-radius: 8px; padding: 0.8em 1em; background: white; transition: transform 0.15s, box-shadow 0.15s; }
.lc-pyrun-bound .lc-rt-card h3 { margin: 0 0 0.4em; font-size: 1em; color: #222; }
.lc-pyrun-bound .lc-rt-card .lc-rt-row { margin: 0.15em 0; font-size: 0.88em; color: #444; }
.lc-pyrun-bound .lc-rt-card .lc-rt-row b { color: #0066cc; margin-right: 0.4em; }
.lc-pyrun-bound .lc-rt-card .lc-rt-val { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.88em; color: #333; word-break: break-word; }
.lc-pyrun-fold > summary { padding: 0.45em 0.9em; cursor: pointer; background: #f3f4f6; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; color: #444; user-select: none; list-style: none; display: flex; align-items: center; gap: 0.5em; }
.lc-pyrun-fold > summary::-webkit-details-marker { display: none; }
.lc-pyrun-fold > summary::before { content: "▶"; font-size: 0.7em; transition: transform 0.15s; color: #888; }
.lc-pyrun-fold[open] > summary::before { transform: rotate(90deg); }
.lc-pyrun-fold > summary:hover { background: #e8e9eb; }
.lc-pyrun-fold[open] > summary { border-bottom: 1px solid #d0d0d0; }
.lc-pyrun-tests { background: #fafbfc; border-top: 1px solid #e0e0e0; }
.lc-pyrun-tests:empty { display: none; }
.lc-pyrun-tests .lc-pyrun-test-summary { padding: 0.5em 0.9em; font-weight: 600; background: #f3f4f6; border-bottom: 1px solid #d0d0d0; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; color: #333; }
.lc-pyrun-tests .lc-pyrun-test-row { padding: 0.4em 0.9em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; border-bottom: 1px solid #f0f0f0; white-space: pre-wrap; }
.lc-pyrun-tests .lc-pyrun-test-row:last-child { border-bottom: none; }
.lc-pyrun-tests .lc-pyrun-test-pass { color: #2a7a2a; }
.lc-pyrun-tests .lc-pyrun-test-fail { color: #b00; background: #fff5f5; }
.lc-pyrun-tests .lc-pyrun-test-empty { color: var(--lc-ink-mute, #616161); font-style: italic; }

.lc-pyrepl { border: 1px solid #d0d0d0; border-radius: 8px; overflow: hidden; margin: 1em 0; background: #1e1e1e; }
.lc-pyrepl-title { background: #f3f4f6; padding: 0.45em 0.9em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; color: #444; border-bottom: 1px solid #d0d0d0; display: flex; align-items: center; gap: 0.5em; }
.lc-pyrepl-title .lc-pyrepl-reset { margin-left: auto; background: #e5e5e5; color: #333; border: none; border-radius: 4px; padding: 0.15em 0.55em; cursor: pointer; font-size: 0.95em; line-height: 1; }
.lc-pyrepl-title .lc-pyrepl-reset:hover { background: #d0d0d0; }
.lc-pyrepl-title .lc-pyrepl-status { font-size: 0.78em; color: #888; font-style: italic; margin-left: 0.5em; }
.lc-pyrepl-transcript { margin: 0; padding: 0.9em 1em; color: #d4d4d4; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; line-height: 1.5; white-space: pre-wrap; min-height: 4em; max-height: 320px; overflow-y: auto; }
.lc-pyrepl-transcript:empty::before { content: "type a Python expression below and press Enter"; color: #888; font-style: italic; }
.lc-pyrepl-transcript .lc-pyrepl-prompt-line { color: #6aa84f; }
.lc-pyrepl-transcript .lc-pyrepl-err { color: #ff6b6b; }
.lc-pyrepl-input-row { display: flex; align-items: center; gap: 0.5em; padding: 0.5em 1em; background: #1e1e1e; border-top: 1px solid #333; }
.lc-pyrepl-marker { color: #6aa84f; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; font-weight: bold; user-select: none; }
.lc-pyrepl-input { flex: 1; min-width: 0; background: transparent; border: none; outline: none; color: #d4d4d4; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.85em; line-height: 1.5; padding: 0; }
.lc-pyrepl-input:disabled { color: #666; }

.button { display: inline-block; padding: 0.5em 1.2em; background: #0066cc; color: white !important; text-decoration: none !important; border-radius: 4px; font-weight: 600; transition: background 0.15s; margin: 0.2em 0.3em 0.2em 0; }
/* safety net: if {: .button } is written on its own line it becomes a block IAL
   on the wrapping <p>, leaving the inner link the site colour (low contrast);
   force the inner link readable so the button works either way */
.button a { color: #fff !important; }
.button:hover { background: #0052a3; }
.button[kind="secondary"], .button-secondary { background: #6c757d; } .button[kind="secondary"]:hover, .button-secondary:hover { background: #5a6268; }
.button[kind="success"], .button-success { background: #28a745; } .button[kind="success"]:hover, .button-success:hover { background: #1e7e34; }
.button[kind="danger"], .button-danger { background: #dc3545; } .button[kind="danger"]:hover, .button-danger:hover { background: #bd2130; }
.button[kind="outline"], .button-outline { background: transparent; color: #0066cc !important; border: 2px solid #0066cc; padding: calc(0.5em - 2px) calc(1.2em - 2px); }
.button[kind="outline"]:hover, .button-outline:hover { background: #0066cc; color: white !important; }
</style>

<script>
(function () {
  if (window._lcPyrunReady) return;
  window._lcPyrunReady = true;

  var _lcSiteRepo = {{ site.github.repository_nwo | default: "" | jsonify }};

  /* shared loaders from code_chrome.md (parsed earlier — topbar include) */
  var loadPrism  = window.lcLoadPrism;
  var loadJsYaml = window.lcLoadJsYaml;

  /* ONE MicroPython per page. The wasm build is a singleton: a second
     loadMicroPython silently kills the first (every later call throws
     "NULL object"). Features, editors, cells, buttons, diagrams and the
     x-ray all share THIS interpreter; stdout/stderr route through a
     swappable hook — runPython is synchronous, so a consumer sets the
     hook, runs, and clears it, atomically. */
  function lcMpy() {
    if (window._lcMpyP) return window._lcMpyP;
    window._lcMpyP = import("https://cdn.jsdelivr.net/npm/@micropython/micropython-webassembly-pyscript@latest/micropython.mjs")
      .then(function (mjs) {
        return mjs.loadMicroPython({
          /* THE BUILD HANDS US LINES, NOT BYTES: with a function hook,
             MicroPython calls stdout once per line WITHOUT its newline — so
             two prints arrived as "ab", and `expected="0\n1\n2"`, which this
             component's own docs teach, could never match (found while
             building input(), 2026-09-02). Put the newline back, unless a
             build ever hands one over. */
          /* a doctest example's own prints are its result, not the
             program's: pycheck.md's stand-in holds them in _lcMpyCap */
          stdout: function (t) {
            var line = /\n$/.test(t) ? t : t + "\n";
            if (typeof window._lcMpyCap === "string") window._lcMpyCap += line;
            else if (window._lcMpyOut) window._lcMpyOut(line);
          },
          stderr: function (t) {
            var line = /\n$/.test(t) ? t : t + "\n";
            if (typeof window._lcMpyCap === "string") window._lcMpyCap += line;
            else if (window._lcMpyOut) window._lcMpyOut(line);
            else if (window.console) console.warn("[lc mpy stderr]", t);
          }
        });
      });
    return window._lcMpyP;
  }
  window.lcMpy = lcMpy;

  /* FRAMES — a terminal animation, played back (Michel, 2026-10-19: the pet
     race "for _ in range(10): time.sleep(.5); os.system('clear');
     race.run()" should show the pets getting closer). runPython is
     synchronous: nothing paints while it runs, so a real sleep would only
     freeze the page. While a program runs, time.sleep(s) and
     os.system('clear') leave MARKS in its output instead; the console then
     plays the output back, frame by frame, with the same pauses. The marks
     are installed for the run only and taken away after it. */
  window.LC_FRAMES_ON = [
    "import time as _lc_t, os as _lc_o",
    "if not hasattr(_lc_t, '_lc_real_sleep'):",
    "    _lc_t._lc_real_sleep = _lc_t.sleep",
    "def _lc_fsleep(s=0):",
    "    print('\\x1b[lc:sleep %s]' % s)",
    "def _lc_fsystem(cmd=''):",
    "    if str(cmd).strip() in ('clear', 'cls'):",
    "        print('\\x1b[2J')",
    "    return 0",
    "_lc_t.sleep = _lc_fsleep",
    "_lc_o.system = _lc_fsystem"
  ].join("\n");
  window.LC_FRAMES_OFF = "_lc_t.sleep = _lc_t._lc_real_sleep";
  var FRAME_MARK = /\x1b\[lc:sleep ([\d.]+)\]\n?|\x1b\[2J\n?/g;
  window.lcFrames = {
    has: function (t) { return /\x1b\[(lc:sleep [\d.]+\]|2J)/.test(t || ""); },
    /* what a terminal shows once the program is over: the last screen */
    final: function (t, initial) {
      var parts = String(t || "").split(/\x1b\[2J\n?/);
      var last = parts.length > 1 ? parts[parts.length - 1] : (initial || "") + parts[0];
      return last.replace(/\x1b\[lc:sleep [\d.]+\]\n?/g, "");
    },
    /* play the frames into render(screen); a newer play on the same
       element cancels the older one. Pauses are capped (2 s each, 400
       frames) so a slip like sleep(60) never hangs a lesson. */
    play: function (el, t, render, initial, done) {
      var frames = [], screen = initial || "", m, at = 0;
      FRAME_MARK.lastIndex = 0;
      while ((m = FRAME_MARK.exec(t)) !== null) {
        screen += t.slice(at, m.index);
        at = FRAME_MARK.lastIndex;
        if (m[1] !== undefined) frames.push({ show: screen, wait: Math.min(parseFloat(m[1]) || 0, 2) });
        else screen = "";
      }
      screen += t.slice(at);
      frames.push({ show: screen, wait: 0 });
      if (frames.length > 400) frames = frames.slice(frames.length - 400);
      var token = {};
      el._lcPlay = token;
      el.setAttribute("data-lc-playing", "1");
      (function step(i) {
        if (el._lcPlay !== token) return;
        render(frames[i].show);
        if (i + 1 >= frames.length) {
          el.removeAttribute("data-lc-playing");
          if (done) done();
          return;
        }
        setTimeout(function () { step(i + 1); }, frames[i].wait * 1000);
      })(0);
    }
  };

  var BOOTSTRAP_TPL = [
    "from js import document",
    "class _Showable:",
    "    def __init__(self, view_id):",
    "        self._view = document.getElementById(view_id)",
    "    def _esc(self, s):",
    "        return str(s).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')",
    "    def _card(self, title, rows_html):",
    "        c = document.createElement('div')",
    "        c.className = 'lc-rt-card'",
    "        c.innerHTML = '<h3>' + self._esc(title) + '</h3>' + rows_html",
    "        self._view.appendChild(c)",
    "    def _rows_from_pairs(self, pairs):",
    "        out = ''",
    "        for k, v in pairs:",
    "            out += '<div class=\"lc-rt-row\"><b>' + self._esc(k) + '</b><span class=\"lc-rt-val\">' + self._esc(v) + '</span></div>'",
    "        return out",
    "    def __call__(self, obj, title=None):",
    "        if isinstance(obj, dict):",
    "            t = title or obj.get('name') or obj.get('title') or 'dict'",
    "            self._card(t, self._rows_from_pairs(obj.items()))",
    "        elif isinstance(obj, (list, tuple)):",
    "            for i, item in enumerate(obj):",
    "                self(item, title=title and (title + '[' + str(i) + ']'))",
    "        else:",
    "            try:",
    "                d = obj.__dict__",
    "                if d:",
    "                    t = title or getattr(obj, 'name', None) or type(obj).__name__",
    "                    self._card(t, self._rows_from_pairs(d.items()))",
    "                    return",
    "            except (AttributeError, TypeError):",
    "                pass",
    "            self._card(title or type(obj).__name__, '<div class=\"lc-rt-val\">' + self._esc(obj) + '</div>')",
    "    def clear(self):",
    "        self._view.innerHTML = ''",
    "    def grid(self, rows, title=None, height=300):",
    "        import json as _json",
    "        from js import lcRenderDatagridFromJson",
    "        normalized = []",
    "        for r in rows:",
    "            if isinstance(r, dict):",
    "                normalized.append(r)",
    "            else:",
    "                try:",
    "                    normalized.append(r.__dict__)",
    "                except (AttributeError, TypeError):",
    "                    normalized.append({'value': str(r)})",
    "        lcRenderDatagridFromJson(self._view, _json.dumps(normalized), title or '', int(height))",
    "    def form(self, obj, title=None):",
    "        import json as _json",
    "        from js import lcRenderFormFromJson",
    "        if isinstance(obj, dict):",
    "            d = obj",
    "        else:",
    "            try:",
    "                d = obj.__dict__",
    "            except (AttributeError, TypeError):",
    "                d = {'value': str(obj)}",
    "        lcRenderFormFromJson(self._view, _json.dumps(d), title or '')",
    "show = _Showable('lc-pyrun-__ID__-view')",
    "class _Player:",
    "    def __init__(self, run_id):",
    "        self._id = run_id",
    "        self.tempo = 160",
    "        self.wave = 'square'",
    "    def _one(self, note, beats):",
    "        from js import lcPlayNote",
    "        lcPlayNote(self._id, str(note), float(beats) * 60.0 / float(self.tempo), self.wave)",
    "    def __call__(self, what, duration=1):",
    "        if isinstance(what, str):",
    "            self._one(what, duration)",
    "        elif isinstance(what, dict):",
    "            self._one(what['note'], what.get('duration', duration))",
    "        elif isinstance(what, tuple) and len(what) == 2 and isinstance(what[0], str):",
    "            self._one(what[0], what[1])",
    "        elif isinstance(what, (list, tuple)):",
    "            for x in what:",
    "                self(x, duration)",
    "        else:",
    "            self._one(getattr(what, 'note'), getattr(what, 'duration', duration))",
    "    def stop(self):",
    "        from js import lcPlayStop",
    "        lcPlayStop(self._id)",
    "play = _Player('__ID__')",
    "class Object:",
    "    def __init__(self, **kw):",
    "        for k, v in kw.items():",
    "            setattr(self, k, v)",
    "    def __repr__(self):",
    "        attrs = ', '.join(k + '=' + repr(v) for k, v in self.__dict__.items())",
    "        return 'Object(' + attrs + ')'",
    /* input() WITHOUT A CONSOLE. MicroPython runs on the page's own thread,
       so a real input() would wait for a stdin the browser does not have and
       freeze the tab (measured, 2026-09-01). Instead the call is ANSWERED
       FROM A QUEUE and, when the queue runs dry, it stops the pass and says
       which question is unanswered; the driver asks the reader and runs the
       script again from the top with one more answer in hand. The queue is
       keyed by CALL ORDER, so a loop needs nothing special — five questions
       in a while are just calls 1..5 (Michel asked exactly this, 2026-09-02).
       Each answer remembers its prompt: if a re-run asks something else at
       that position, the program changed its mind and the driver drops the
       answers from there on. */
    "import js",
    "import json as _lc_json",
    "class _LcNeedInput(Exception):",
    "    pass",
    "_lc_answers = []",
    "_lc_ask_i = 0",
    "def _lc_load_answers():",
    "    global _lc_answers, _lc_ask_i",
    "    _lc_ask_i = 0",
    "    try:",
    "        _lc_answers = _lc_json.loads(str(js.window._lcInputAnswers or '[]'))",
    "    except Exception:",
    "        _lc_answers = []",
    "def input(prompt=''):",
    "    global _lc_ask_i",
    "    p = str(prompt)",
    "    i = _lc_ask_i",
    "    _lc_ask_i = i + 1",
    "    if i < len(_lc_answers) and _lc_answers[i][0] == p:",
    "        v = _lc_answers[i][1]",
    "        print(p + v)",   /* the transcript a terminal would show */
    "        return v",
    "    js.window._lcInputWant = _lc_json.dumps([i, p])",
    "    raise _LcNeedInput(p)",
    "_BOUND_ID = 'lc-pyrun-__ID__-bound'",
    "def _render_bound(name):",
    "    g = globals()",
    "    if name not in g:",
    "        return",
    "    obj = g[name]",
    "    container = document.getElementById(_BOUND_ID)",
    "    if container is None:",
    "        return",
    "    container.innerHTML = ''",
    "    c = document.createElement('div')",
    "    c.className = 'lc-rt-card'",
    "    d = getattr(obj, '__dict__', None) or {}",
    "    rows = ''",
    "    for k, v in d.items():",
    "        rows += '<div class=\"lc-rt-row\"><b>' + str(k) + '</b><span class=\"lc-rt-val\">' + str(v) + '</span></div>'",
    "    c.innerHTML = '<h3>' + name + '</h3>' + rows",
    "    container.appendChild(c)",
    "try:",
    "    import json as _json",
    "    from js import jsyaml as _jsyaml, JSON as _JSON",
    "    class _Yaml:",
    "        def load(self, s):",
    "            return _json.loads(_JSON.stringify(_jsyaml.load(s)))",
    "    yaml = _Yaml()",
    "    yaml.safe_load = yaml.load",
    "except Exception:",
    "    pass"
  ].join("\n");


  /* MICROPYTHON HAS NO f'{x = }' (Michel, 2026-10-07: his starters print
     f'{secret = }'). CPython 3.8 reads {expr = } as the text "expr = "
     followed by repr(expr) — or format(expr, spec) when a :spec follows.
     The runner rewrites it that way before the code reaches MicroPython,
     inside f-strings only, same line count, so a traceback still points
     where the learner looks. Comparisons ({a == b}), keyword arguments
     ({f(a=1)}) and doubled-brace escapes are left alone. */
  function desugarFstrings(src) {
    var out = "", i = 0, n = src.length;
    while (i < n) {
      var ch = src[i];
      if (ch === "#") { var e = src.indexOf("\n", i); if (e < 0) e = n; out += src.slice(i, e); i = e; continue; }
      var m = /^([rRbBuUfF]{0,2})('''|"""|'|")/.exec(src.slice(i, i + 5));
      if (m && (i === 0 || !/[A-Za-z0-9_.]/.test(src[i - 1]))) {
        var prefix = m[1], q = m[2], isF = /[fF]/.test(prefix);
        var j = i + prefix.length + q.length, body = "";
        while (j < n) {
          if (src[j] === "\\") { body += src.slice(j, j + 2); j += 2; continue; }
          if (src.startsWith(q, j)) break;
          if (q.length === 1 && src[j] === "\n") break;
          body += src[j]; j++;
        }
        var closed = src.startsWith(q, j);
        out += prefix + q + (isF ? desugarFBody(body) : body) + (closed ? q : "");
        i = j + (closed ? q.length : 0);
        continue;
      }
      out += ch; i++;
    }
    return out;
  }
  function desugarFBody(body) {
    return body.replace(/\{\{/g, "\u0001").replace(/\}\}/g, "\u0002")
      .replace(/\{([^{}]*)\}/g, function (all, inner) {
        var m = /^(\s*)(.*?[^=!<>])(\s*=\s*)(![rsa])?(:[^{}]*)?$/.exec(inner);
        if (!m) return all;
        var expr = m[2], conv = m[4] || (m[5] ? "" : "!r"), spec = m[5] || "";
        return m[1] + expr + m[3] + "{" + expr + conv + spec + "}";
      })
      .replace(/\u0001/g, "{" + "{").replace(/\u0002/g, "}" + "}");   /* no literal doubled braces: Liquid eats them */
  }

  /* text into an element WITHOUT replacing its node — Chromium closes the
     open typing (undo) group whenever a node is removed from the page */
  function setText(el, s) {
    var c = el.firstChild;
    if (c && c.nodeType === 3 && !c.nextSibling) { if (c.data !== s) c.data = s; }
    else el.textContent = s;
  }

  /* EVERY WRITE INTO THE EDITOR KEEPS UNDO (Michel, 2026-10-07: "undo does
     NOT work"). Assigning .value wipes the browser's undo stack; typing
     through insertText does not — so Tab, the tutor's piece, anything that
     edits the program goes through here: ⌘Z takes it back, like typing.
     Falls back to setRangeText where insertText is refused (old Firefox). */
  function editRange(ta, start, end, text) {
    var want = ta.value.slice(0, start) + text + ta.value.slice(end), ok = false;
    try {
      ta.focus();
      ta.setSelectionRange(start, end);
      ok = document.execCommand("insertText", false, text) && ta.value === want;
    } catch (e) { ok = false; }
    if (!ok) {
      ta.setRangeText(text, start, end, "end");
      try { ta.dispatchEvent(new Event("input", { bubbles: true })); } catch (e) {}
    }
    return ta.value === want;
  }

  function attach(rootId, opts) {
    opts = opts || {};
    var ID = opts.id || rootId.replace(/^lc-pyrun-/, "");
    var BOUND = opts.bound || "";
    var INIT = opts.init || "";
    var root = document.getElementById(rootId);
    if (!root || root.dataset.lcAttached) return;
    root.dataset.lcAttached = "1";
    var codeEl = root.querySelector(".lc-pyrun-code");
    var gutterInner = root.querySelector(".lc-pyrun-gutter-inner");
    var runBtn = root.querySelector(".lc-pyrun-run");
    var clearBtn = root.querySelector(".lc-pyrun-clear");
    var testBtn = root.querySelector(".lc-pyrun-test");
    var status = root.querySelector(".lc-pyrun-status");
    var out = root.querySelector(".lc-pyrun-out");
    var view = root.querySelector(".lc-pyrun-view");
    var testsEl = root.querySelector(".lc-pyrun-tests");
    if (!codeEl || !runBtn) return;
    var buf = "";
    var mp = null;
    var loading = null;
    var BOOTSTRAP = BOOTSTRAP_TPL.replace(/__ID__/g, ID);

    function repaintBound() {
      if (!BOUND || !mp) return;
      try { mp.runPython("_render_bound(" + JSON.stringify(BOUND) + ")"); } catch (e) { }
    }

    function setOut(text, isErr) {
      out.classList.remove("lc-empty");
      out.textContent = "";
      if (isErr) {
        var span = document.createElement("span");
        span.className = "lc-err";
        span.textContent = text;
        out.appendChild(span);
      } else {
        out.textContent = text;
      }
    }

    function clearTests() {
      if (testsEl) testsEl.innerHTML = "";
    }

    /* One number per line, however many rows the line wraps into: a mirror
       with the editor's font, padding and width lays each line out as a
       block, its height says how many rows it took, and the gutter pads the
       number with that many blank rows. */
    var mirror = null;
    function rowsPerLine(lines) {
      var wrapEl = codeEl.parentNode;
      if (!wrapEl || !wrapEl.classList || !wrapEl.classList.contains("lc-pyrun-codewrap")) return null;
      if (!mirror) { mirror = document.createElement("div"); mirror.className = "lc-pyrun-mirror"; mirror.setAttribute("aria-hidden", "true"); wrapEl.appendChild(mirror); }
      var cs = getComputedStyle(codeEl);
      ["fontFamily", "fontSize", "fontWeight", "lineHeight", "letterSpacing", "tabSize",
       "whiteSpace", "wordWrap", "overflowWrap",
       "paddingTop", "paddingRight", "paddingBottom", "paddingLeft"].forEach(function (k) { mirror.style[k] = cs[k]; });
      mirror.style.width = codeEl.clientWidth + "px";    /* minus a scrollbar, as the text is laid out */
      var lh = parseFloat(cs.lineHeight);
      if (!(lh > 0)) lh = parseFloat(cs.fontSize) * 1.5;
      var kids = mirror.children;
      while (kids.length > lines.length) mirror.removeChild(mirror.lastChild);
      while (kids.length < lines.length) { var d = document.createElement("div"); d.appendChild(document.createTextNode("")); mirror.appendChild(d); }
      lines.forEach(function (ln, i) { setText(kids[i], ln || " "); });
      var out = [];
      for (var i = 0; i < kids.length; i++) out.push(Math.max(1, Math.round(kids[i].offsetHeight / lh)));
      return out;
    }
    /* THE EDITOR FITS ITS PROGRAM (Michel, 2026-10-07, Safari: "the cursor
       stays trapped in the first 7 lines"): without rows= the box grows
       with the lines and never scrolls inside — the page scrolls, as it
       does for any text. rows= pins the height, scrolling as before. */
    var FIT = !opts.rows, MIN_ROWS = parseInt(codeEl.getAttribute("rows"), 10) || 6;
    function fitRows() {
      if (!FIT) return;
      var n = Math.max(MIN_ROWS, codeEl.value.split("\n").length + 1);
      if (codeEl.rows !== n) codeEl.rows = n;
    }
    function updateGutter() {
      if (!gutterInner) return;
      fitRows();
      var lines = codeEl.value.split("\n");
      var rows = codeEl.clientWidth ? rowsPerLine(lines) : null;
      var s = "";
      for (var i = 0; i < lines.length; i++) {
        s += (i ? "\n" : "") + (i + 1);
        var extra = rows ? rows[i] - 1 : 0;
        for (var k = 0; k < extra; k++) s += "\n";
      }
      setText(gutterInner, s);   /* no node swap: typing stays one undo step */
    }
    function syncGutter() {
      if (!gutterInner) return;
      gutterInner.style.transform = "translateY(" + (-codeEl.scrollTop) + "px)";
    }
    if (gutterInner) {
      updateGutter();
      codeEl.addEventListener("input", updateGutter);
      codeEl.addEventListener("scroll", syncGutter);
      /* a narrower editor wraps more: the rows are measured again */
      if (window.ResizeObserver) new ResizeObserver(function () { updateGutter(); }).observe(codeEl);
      else window.addEventListener("resize", updateGutter);
    }

    var hlPre = root.querySelector(".lc-pyrun-hl");
    var hlCode = hlPre ? hlPre.querySelector("code") : null;
    /* THE OVERLAY IS PATCHED, NOT REBUILT, WHILE TYPING (2026-10-07): a
       rebuilt overlay removes nodes, and Chromium then closes the typing
       group — ⌘Z took one character at a time. A keystroke changes one
       text node in place (colours catch up on a pause); only a change
       that crosses tokens rebuilds, as the recolour does. */
    var hlText = null, hlTimer = null;
    function hlPatch(next) {
      if (hlText == null || !hlCode.firstChild) return false;
      var prev = hlText, a = 0, pb = prev.length, nb = next.length;
      while (a < pb && a < nb && prev[a] === next[a]) a++;
      while (pb > a && nb > a && prev[pb - 1] === next[nb - 1]) { pb--; nb--; }
      var walker = document.createTreeWalker(hlCode, NodeFilter.SHOW_TEXT), node, pos = 0, last = null;
      while ((node = walker.nextNode())) {
        var len = node.data.length;
        if (a >= pos && pb <= pos + len && (a < pos + len || pb > a)) {
          node.data = node.data.slice(0, a - pos) + next.slice(a, nb) + node.data.slice(pb - pos);
          return true;
        }
        if (a < pos + len) return false;   /* the change crosses tokens */
        pos += len; last = node;
      }
      if (last && a === pos && pb === pos) {   /* typed at the very end */
        last.data += next.slice(a, nb);
        return true;
      }
      return false;
    }
    function recolour() {
      hlTimer = null;
      if (!hlCode || hlText == null) return;
      if (window.Prism && window.Prism.languages && window.Prism.languages.python) {
        hlCode.textContent = hlText;
        try { window.Prism.highlightElement(hlCode); } catch (e) {}
      }
    }
    function syncHighlight() {
      if (!hlCode) return;
      var text = codeEl.value, shown = text + (text.slice(-1) === "\n" ? " " : "");
      if (!hlPatch(shown)) setText(hlCode, shown);
      hlText = shown;
      clearTimeout(hlTimer);
      hlTimer = setTimeout(recolour, 250);
      syncHlScroll();
    }
    function syncHlScroll() {
      if (!hlCode) return;
      hlCode.style.transform = "translate(" + (-codeEl.scrollLeft) + "px, " + (-codeEl.scrollTop) + "px)";
    }
    if (hlCode) {
      syncHighlight();
      loadPrism().then(syncHighlight);
      codeEl.addEventListener("input", syncHighlight);
      codeEl.addEventListener("scroll", syncHlScroll);
    }

    /* ↕ THE GRIP: drag sets the editor's height for this visit; double-click resets */
    var grip = root.querySelector(".lc-pyrun-grip");
    if (grip) {
      grip.addEventListener("pointerdown", function (ev) {
        ev.preventDefault();
        var y0 = ev.clientY, h0 = codeEl.getBoundingClientRect().height;
        grip.setPointerCapture(ev.pointerId);
        root.setAttribute("data-lc-resizing", "1");
        function move(e) { FIT = false; codeEl.style.height = Math.max(60, Math.round(h0 + e.clientY - y0)) + "px"; }
        function up() {
          root.removeAttribute("data-lc-resizing");
          grip.removeEventListener("pointermove", move); grip.removeEventListener("pointerup", up); grip.removeEventListener("pointercancel", up);
          updateGutter();
        }
        grip.addEventListener("pointermove", move); grip.addEventListener("pointerup", up); grip.addEventListener("pointercancel", up);
      });
      grip.addEventListener("dblclick", function () { codeEl.style.height = ""; FIT = !opts.rows; fitRows(); updateGutter(); });
    }

    /* 💬 SUBTITLES: the program read, part by part */
    var subsEl = root.querySelector(".lc-pyrun-subs"), subsBtn = root.querySelector(".lc-pyrun-subs-btn"), subLine = root.querySelector(".lc-pyrun-subline");
    /* ▾ IN THE GUTTER (Michel, 2026-10-27: "the folding sign could be in the
       gutter"): with the captions on, the gutter numbers only the lines
       still shown and carries a ▾/▸ beside each line that opens a block */
    var gutterEl = root.querySelector(".lc-pyrun-gutter"), folds = null;
    function paintGutterFolds() {
      if (!gutterEl || !gutterInner) return;
      if (!folds) { folds = document.createElement("div"); folds.className = "lc-pyrun-folds"; gutterEl.appendChild(folds); }
      if (subsEl.hidden) { folds.innerHTML = ""; folds.hidden = true; updateGutter(); return; }
      folds.hidden = false;
      var shown = Array.prototype.filter.call(subsEl.querySelectorAll(".lc-sub-line"), function (l) { return !l.classList.contains("lc-sub-hidden"); });
      var nums = [], marks = [];
      var cs = getComputedStyle(codeEl), lh = parseFloat(cs.lineHeight) || parseFloat(cs.fontSize) * 1.5, top0 = parseFloat(cs.paddingTop) || 0;
      shown.forEach(function (l, row) {
        var n = parseInt(l.getAttribute("data-l"), 10) + 1;
        nums.push(n);
        if (l.getAttribute("data-opens") === "1") {
          var folded = l.getAttribute("data-folded") === "1";
          marks.push('<button type="button" class="lc-pyrun-gfold" data-l="' + (n - 1) + '" aria-expanded="' + (folded ? "false" : "true") + '" title="' + (folded ? "Unfold" : "Fold") + ' this block" style="top:' + (top0 + row * lh) + 'px">' + (folded ? "▸" : "▾") + "</button>");
        }
      });
      setText(gutterInner, nums.join("\n"));
      folds.innerHTML = marks.join("");
    }
    if (gutterEl) gutterEl.addEventListener("click", function (e) {
      var b = e.target && e.target.closest ? e.target.closest(".lc-pyrun-gfold") : null;
      if (!b || !window.lcSubtitles || subsEl.hidden) return;
      var line = subsEl.querySelector('.lc-sub-line[data-l="' + b.getAttribute("data-l") + '"]');
      window.lcSubtitles.fold(line);
      paintGutterFolds();
    });
    function paintSubs() {
      if (!subsEl || !window.lcSubtitles || subsEl.hidden) return;
      subsEl.innerHTML = window.lcSubtitles.html(codeEl.value);
      paintGutterFolds();
    }
    function setSubtitles(on) {
      if (!subsEl) return;
      root.classList.toggle("lc-pyrun-subtitled", on);
      subsEl.hidden = !on;
      if (subsBtn) subsBtn.setAttribute("aria-checked", on ? "true" : "false");
      if (on) { paintSubs(); if (subLine) { subLine.hidden = false; subLine.textContent = "Hover or tap a part of the program: it says what it is."; } }
      else { if (subLine) { subLine.hidden = true; subLine.textContent = ""; } paintGutterFolds(); }
    }
    if (subsBtn) subsBtn.addEventListener("click", function () { setSubtitles(subsEl.hidden); });
    if (subsEl) {
      subsEl.addEventListener("click", function (e) {
        var t = e.target && e.target.closest ? e.target.closest(".lc-sub") : null;
        subsEl.querySelectorAll(".lc-sub-on").forEach(function (x) { x.classList.remove("lc-sub-on"); });
        if (!t || !subLine) return;
        t.classList.add("lc-sub-on");
        subLine.innerHTML = "<code>" + t.textContent.replace(/&/g, "&amp;").replace(/</g, "&lt;") + "</code> — " + (t.getAttribute("data-sub") || "").replace(/&/g, "&amp;").replace(/</g, "&lt;");
      });
      codeEl.addEventListener("input", paintSubs);
      if (opts.subtitles === "on" || opts.subtitles === "true") setSubtitles(true);
    }

    /* ✨ THE SAME SYMBOL, LIT: select a word (a double-click does), and every
       other occurrence of it lights up under the colours */
    var marksCode = root.querySelector(".lc-pyrun-marks code"), marksTimer = null;
    function escHtml(x) { return String(x).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
    function paintMarks() {
      marksTimer = null;
      if (!marksCode) return;
      var v = codeEl.value, a = codeEl.selectionStart, b = codeEl.selectionEnd, word = v.slice(a, b);
      if (!word || !/^[A-Za-z_][A-Za-z_0-9]*$/.test(word) || document.activeElement !== codeEl) { marksCode.innerHTML = ""; root.removeAttribute("data-lc-lit"); return; }
      var re = new RegExp("\\b" + word.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "\\b", "g"), out = "", last = 0, m, n = 0;
      while ((m = re.exec(v))) {
        if (m.index === a) continue;                      /* the selected one is already lit by the selection */
        out += escHtml(v.slice(last, m.index)) + "<mark>" + escHtml(m[0]) + "</mark>";
        last = m.index + m[0].length; n++;
      }
      marksCode.innerHTML = out + escHtml(v.slice(last)) + (v.slice(-1) === "\n" ? " " : "");
      marksCode.style.transform = hlCode ? hlCode.style.transform : "";
      root.setAttribute("data-lc-lit", n ? word + ":" + n : "");
    }
    function marksSoon() { clearTimeout(marksTimer); marksTimer = setTimeout(paintMarks, 80); }
    if (marksCode) {
      ["select", "mouseup", "keyup", "blur"].forEach(function (ev) { codeEl.addEventListener(ev, marksSoon); });
      codeEl.addEventListener("scroll", function () { if (hlCode) marksCode.style.transform = hlCode.style.transform; });
      codeEl.addEventListener("input", function () { if (marksCode.innerHTML) marksSoon(); });
    }

    /* 💡 COMPLETION: Ctrl+Space, or two letters of a word, lists what fits
       — keywords, the helpers, the program's own names, and after a dot the
       attributes the program itself uses on that name. Nothing invented. */
    var KEYWORDS = ["def", "class", "return", "for", "in", "while", "if", "elif", "else", "import", "from", "as", "True", "False", "None", "and", "or", "not", "is", "lambda", "with", "pass", "break", "continue", "try", "except", "finally", "raise", "yield", "global", "assert"];
    var BUILTINS = ["print", "len", "range", "str", "int", "float", "list", "dict", "tuple", "bool", "input", "type", "isinstance", "sorted", "max", "min", "sum", "abs", "round", "enumerate", "zip", "reversed", "any", "all", "open", "help", "repr", "format"];
    var HELPERS = { play: "play(note, beats) — a note, or a list of notes", show: "show(obj) — draw it as a card", Object: "Object(**kw) — a simple attribute holder", yaml: "yaml.load(text)" };
    var DOTS = { play: ["tempo", "wave", "stop()"], show: ["clear()", "grid(rows)", "form(obj)"], yaml: ["load(text)"] };
    var comp = { el: null, items: [], i: 0, at: 0 };
    function compClose() { if (comp.el) { comp.el.remove(); comp.el = null; } comp.items = []; root.removeAttribute("data-lc-comp"); }
    function wordAt(v, pos) {
      var a = pos; while (a > 0 && /[A-Za-z_0-9]/.test(v.charAt(a - 1))) a--;
      return { at: a, prefix: v.slice(a, pos), dot: v.charAt(a - 1) === "." };
    }
    function ownerBefore(v, at) {
      var e = at - 1, b = e; while (b > 0 && /[A-Za-z_0-9]/.test(v.charAt(b - 1))) b--;
      return v.slice(b, e);
    }
    function candidates(v, w) {
      var seen = {}, out = [];
      function add(label, detail, icon) { if (seen[label]) return; seen[label] = 1; out.push({ label: label, detail: detail || "", icon: icon || "" }); }
      if (w.dot) {
        var owner = ownerBefore(v, w.at);
        (DOTS[owner] || []).forEach(function (x) { add(x, "", "·"); });
        var re = new RegExp("\\b" + owner + "\\.([A-Za-z_][A-Za-z_0-9]*)", "g"), m;
        while ((m = re.exec(v))) add(m[1], "used in the program", "·");
        var re2 = /self\.([A-Za-z_][A-Za-z_0-9]*)/g;
        while ((m = re2.exec(v))) add(m[1], "an attribute", "·");
      } else {
        Object.keys(HELPERS).forEach(function (h) { add(h, HELPERS[h], "🧰"); });
        var re3 = /\b(?:def|class)\s+([A-Za-z_][A-Za-z_0-9]*)/g, m3;
        while ((m3 = re3.exec(v))) add(m3[1], "defined here", "📌");
        var re4 = /^\s*([A-Za-z_][A-Za-z_0-9]*)\s*(?::[^=\n]+)?=(?!=)/gm;
        while ((m3 = re4.exec(v))) add(m3[1], "a variable", "📌");
        var re5 = /\bfor\s+([A-Za-z_][A-Za-z_0-9]*)/g;
        while ((m3 = re5.exec(v))) add(m3[1], "a loop variable", "📌");
        KEYWORDS.forEach(function (k) { add(k, "keyword", "🔑"); });
        BUILTINS.forEach(function (k) { add(k, "built-in", "⚙️"); });
        var re6 = /[A-Za-z_][A-Za-z_0-9]{2,}/g;
        while ((m3 = re6.exec(v))) add(m3[0], "in the program", "");
      }
      var pre = w.prefix.toLowerCase();
      return out.filter(function (it) { return it.label.toLowerCase().indexOf(pre) === 0 && it.label !== w.prefix; }).slice(0, 12);
    }
    function caretRect() {
      var wrapEl = codeEl.parentNode, cs = getComputedStyle(codeEl);
      var m = document.createElement("div");
      m.style.cssText = "position:absolute;visibility:hidden;white-space:pre;top:0;left:0;";
      ["fontFamily", "fontSize", "fontWeight", "lineHeight", "letterSpacing", "tabSize", "paddingTop", "paddingRight", "paddingBottom", "paddingLeft", "boxSizing"].forEach(function (k) { m.style[k] = cs[k]; });
      m.style.width = codeEl.clientWidth + "px";
      var before = codeEl.value.slice(0, codeEl.selectionStart);
      m.textContent = before;
      var sp = document.createElement("span"); sp.textContent = "\u200b"; m.appendChild(sp);
      wrapEl.appendChild(m);
      var r = sp.getBoundingClientRect(), h = wrapEl.getBoundingClientRect();
      wrapEl.removeChild(m);
      return { left: r.left - h.left - codeEl.scrollLeft, bottom: r.bottom - h.top - codeEl.scrollTop };
    }
    function compShow() {
      var wrapEl = codeEl.parentNode;
      if (!comp.el) { comp.el = document.createElement("div"); comp.el.className = "lc-pyrun-comp"; comp.el.setAttribute("role", "listbox"); wrapEl.appendChild(comp.el); }
      comp.el.innerHTML = comp.items.map(function (it, k) {
        return "<div class='o" + (k === comp.i ? " on" : "") + "' role='option' data-k='" + k + "'><span class='i'>" + escHtml(it.icon) + "</span><span class='l'>" + escHtml(it.label) + "</span><span class='d'>" + escHtml(it.detail) + "</span></div>";
      }).join("");
      var r = caretRect(), hw = wrapEl.getBoundingClientRect();
      comp.el.style.left = Math.max(0, Math.min(r.left, hw.width - 220)) + "px";
      comp.el.style.top = (r.bottom + 2) + "px";
      root.setAttribute("data-lc-comp", comp.items.map(function (x) { return x.label; }).join(","));
    }
    function complete(force) {
      var v = codeEl.value, w = wordAt(v, codeEl.selectionStart);
      if (!force && !w.dot && w.prefix.length < 2) { compClose(); return; }
      if (!force && w.dot && !w.prefix.length) { /* a dot just typed: offer at once */ }
      var items = candidates(v, w);
      if (!items.length) { compClose(); return; }
      comp.items = items; comp.i = 0; comp.at = w.at; compShow();
    }
    function compAccept() {
      var it = comp.items[comp.i]; if (!it) return;
      var v = codeEl.value, a = comp.at, b = codeEl.selectionStart, ins = it.label;
      var back = ins.slice(-2) === "()" ? 1 : 0;
      codeEl.focus();
      codeEl.setSelectionRange(a, b);
      if (!document.execCommand || !document.execCommand("insertText", false, ins)) {
        codeEl.value = v.slice(0, a) + ins + v.slice(b);
        codeEl.dispatchEvent(new Event("input", { bubbles: true }));
      }
      var c = a + ins.length - back; codeEl.setSelectionRange(c, c);
      compClose();
    }
    codeEl.addEventListener("keydown", function (e) {
      if ((e.ctrlKey || e.metaKey) && e.code === "Space") { e.preventDefault(); complete(true); return; }
      if (!comp.el) return;
      if (e.key === "Escape") { e.preventDefault(); compClose(); }
      else if (e.key === "ArrowDown") { e.preventDefault(); comp.i = (comp.i + 1) % comp.items.length; compShow(); }
      else if (e.key === "ArrowUp") { e.preventDefault(); comp.i = (comp.i + comp.items.length - 1) % comp.items.length; compShow(); }
      else if (e.key === "Enter" || e.key === "Tab") { e.preventDefault(); compAccept(); }
    }, true);
    codeEl.addEventListener("input", function (e) {
      var d = e && e.data;
      if (d && /^[A-Za-z_.]$/.test(d)) complete(false); else compClose();
    });
    codeEl.addEventListener("blur", function () { setTimeout(function () { if (document.activeElement !== codeEl) compClose(); }, 150); });
    root.addEventListener("mousedown", function (e) {
      var o = e.target && e.target.closest ? e.target.closest(".lc-pyrun-comp .o") : null;
      if (!o) return;
      e.preventDefault(); comp.i = parseInt(o.getAttribute("data-k"), 10) || 0; compAccept();
    });
    root._lcComplete = function () { complete(true); return comp.items.map(function (x) { return x.label; }); };

    /* TAB INDENTS, SHIFT+TAB DEDENTS (Michel, 2026-10-07: "when a text is
       selected, a tab deletes it"). No selection: four spaces at the caret
       (Shift+Tab: up to four off the line's start). A selection: every line
       it touches moves, as one undoable edit, and stays selected. */
    codeEl.addEventListener("keydown", function(e){
      if (e.key !== "Tab") return;
      e.preventDefault();
      var v = codeEl.value, a = codeEl.selectionStart, b = codeEl.selectionEnd;
      if (a === b && !e.shiftKey) { editRange(codeEl, a, a, "    "); updateGutter(); syncHighlight(); return; }
      var from = v.lastIndexOf("\n", a - 1) + 1;
      var to = v.indexOf("\n", b === a ? b : b - 1); if (to < 0) to = v.length;
      var lines = v.slice(from, to).split("\n"), moved = lines.map(function (l) {
        if (!e.shiftKey) return "    " + l;
        var m = /^ {1,4}/.exec(l); return m ? l.slice(m[0].length) : l;
      });
      var text = moved.join("\n");
      if (text === v.slice(from, to)) return;
      editRange(codeEl, from, to, text);
      /* the lines stay selected (or the caret stays on its line) */
      if (b > a) codeEl.setSelectionRange(from, from + text.length);
      else { var d = moved[0].length - lines[0].length; codeEl.setSelectionRange(Math.max(from, a + d), Math.max(from, a + d)); }
      updateGutter(); syncHighlight();
    });

    function loadMp() {
      if (mp) return Promise.resolve(mp);
      if (loading) return loading;
      runBtn.disabled = true;
      if (testBtn) testBtn.disabled = true;
      status.textContent = "loading runtime…";
      loading = Promise.all([lcMpy(), loadJsYaml()])
        .then(function(results){ return results[0]; })
        .then(function(instance){
          mp = instance;
          try { mp.runPython(BOOTSTRAP); } catch (e) { }
          if (INIT) {
            try { mp.runPython(INIT); } catch (e) { }
          }
          repaintBound();
          runBtn.disabled = false;
          if (testBtn) testBtn.disabled = false;
          status.textContent = "ready";
          return mp;
        })
        .catch(function(e){
          runBtn.disabled = false;
          if (testBtn) testBtn.disabled = false;
          status.textContent = "";
          loading = null;
          throw e;
        });
      return loading;
    }

    /* ── input(), by ask-and-replay ─────────────────────────────────────
       One pass runs to the first unanswered question and stops there; the
       reader answers in the console; the script runs AGAIN from the top with
       that answer in the queue. n questions cost n+1 passes, and the reader
       sees only the last one — the transcript, prompts and answers included,
       exactly as a terminal shows it.

       A loop needs nothing special: the queue is keyed by call order.
       What it cannot survive is a program that asks a DIFFERENT question at
       the same position on a re-run (a random or timed path) — the prompts
       are recorded with the answers, and a mismatch drops the tail. And a
       program that asks without end would replay for ever, so the ceiling
       below stops it with a sentence instead of a hang. */
    var MAX_ASKS = 25;
    var answers = [];              /* [[prompt, value], …] — this press only */

    function askInConsole(prompt) {
      return new Promise(function (resolve) {
        out.classList.remove("lc-empty");
        out.textContent = buf;                       /* what printed so far */
        var line = document.createElement("span");
        line.className = "lc-pyrun-ask";
        line.textContent = prompt;
        var box = document.createElement("input");
        box.type = "text";
        box.className = "lc-pyrun-ask-box";
        box.setAttribute("aria-label", prompt || "input");
        line.appendChild(box);
        out.appendChild(line);
        box.focus();
        box.addEventListener("keydown", function (e) {
          if (e.key === "Enter") { e.preventDefault(); resolve(box.value); }
          else if (e.key === "Escape") { e.preventDefault(); resolve(null); }
        });
      });
    }

    /* the whole press: passes, questions, and the verdict */
    function runAsking(m) {
      answers = [];
      var pass = 0;
      function once() {
        window._lcInputAnswers = JSON.stringify(answers);
        window._lcInputWant = "";
        var ok = runUserCode(m);
        var want = window._lcInputWant;
        if (!want) return Promise.resolve(ok);       /* finished, green or red */
        if (++pass > MAX_ASKS) {
          setOut(buf + "\n… this program asks more questions than a page can "
               + "hold (" + MAX_ASKS + "). A conversation that long belongs in a "
               + "terminal, or in a REPL block.", true);
          return Promise.resolve(false);
        }
        var asked;
        try { asked = JSON.parse(want); } catch (e) { return Promise.resolve(ok); }
        answers.length = asked[0];                   /* the tail is stale */
        return askInConsole(asked[1]).then(function (value) {
          if (value === null) {                      /* Escape — leave it be */
            setOut(buf + "\n(cancelled — nothing was asked twice)", false);
            return false;
          }
          answers.push([asked[1], value]);
          return once();
        });
      }
      return once();
    }

    function runUserCode(m) {
      buf = "";
      view.innerHTML = "";
      /* shared interpreter: point `show` (and print) at THIS editor for
         the duration of the run — runPython is synchronous */
      window._lcMpyOut = function (t) { buf += t; };
      try { m.runPython(BOOTSTRAP); } catch (e) { }
      try { m.runPython("_lc_load_answers()"); } catch (e) { }
      try { m.runPython(window.LC_FRAMES_ON); } catch (e) { }
      try {
        /* the deck's files run as written: doctest, __doc__, help(),
           mypy.api — read from the program's text (pycheck.md) */
        m.runPython(desugarFstrings(window.lcPyBefore ? window.lcPyBefore(m, codeEl.value, ID + ".py") : codeEl.value));
        if (window.lcFrames.has(buf)) {
          /* an animation: play it, and keep the last screen as THE output */
          var raw = buf;
          buf = window.lcFrames.final(raw);
          window.lcFrames.play(out, raw, function (scr) { setOut(scr, false); });
        } else {
          out._lcPlay = null;
          setOut(buf || "(no print output)", false);
        }
        return true;
      } catch (e) {
        /* an unanswered input() is not an error the reader should read: the
           driver is about to ask the question and run this again */
        if (window._lcInputWant) return false;
        out._lcPlay = null;
        buf = window.lcFrames.final(buf);
        setOut(buf + (buf ? "\n" : "") + (e.message || String(e)), true);
        return false;
      } finally {
        try { m.runPython(window.LC_FRAMES_OFF); } catch (e) { }
        window._lcMpyOut = null;
      }
    }

    var EXPECTED = (opts.expected || "").replace(/\r\n/g, "\n");
    if (EXPECTED) root.dataset.lcQuizId = "run-" + ID;

    function checkExpected(ok) {
      if (!EXPECTED) return;
      var actual = (buf || "").replace(/\r\n/g, "\n").replace(/\n+$/, "");
      var want = EXPECTED.replace(/\n+$/, "");
      var match = ok && actual === want;
      status.textContent = match ? "✓ output matches" : "✗ expected: " + want;
      status.style.color = match ? "#2e7d32" : "#c62828";
      if (window.lcQuizScore && window.lcQuizScore.update) {
        window.lcQuizScore.update("run-" + ID, match);
      }
    }

    runBtn.addEventListener("click", function(){
      loadMp().then(function(m){
        clearTests();
        status.textContent = "running…";
        status.style.color = "";
        return runAsking(m).then(function (ok) {
          status.textContent = ok ? "done" : "error";
          status.style.color = "";
          repaintBound();
          checkExpected(ok);
        });
      }).catch(function(e){
        setOut("Failed to load MicroPython: " + (e.message || String(e)), true);
      });
    });

    if (testBtn) {
      testBtn.addEventListener("click", function(){
        loadMp().then(function(m){
          status.textContent = "running…";
          /* 🧪 defines the program's functions by running it — silently: a
             play() at the top level queues nothing under the test button
             (Michel, 2026-10-27: doctests "used exclusively by the green
             test button"; a test checks what a function returns) */
          window._lcPlayMuted = ID;
          var ok;
          try { ok = runUserCode(m); } finally { window._lcPlayMuted = null; }
          if (!ok) {
            status.textContent = "error in code";
            return;
          }
          /* the doctests are doctest's own (pycheck.md): every docstring's
             >>> lines, in their own namespace, statements included */
          clearTests();
          var rows = [];
          try {
            window._lcMpyOut = function (t) { buf += t; };
            window._lcDtRows = "[]";
            try { m.runPython("import js as _lc_js\n_lc_js.window._lcDtRows = _lc_dt_rows()"); rows = JSON.parse(String(window._lcDtRows)); }
            finally { window._lcMpyOut = null; }
          } catch (e) {
            var bad = document.createElement("div");
            bad.className = "lc-pyrun-test-row lc-pyrun-test-fail";
            bad.textContent = "Test runner error: " + (e.message || String(e));
            testsEl.appendChild(bad);
            status.textContent = "test error";
            repaintBound();
            return;
          }
          if (!rows.length) {
            var empty = document.createElement("div");
            empty.className = "lc-pyrun-test-row lc-pyrun-test-empty";
            empty.textContent = "No doctests found. Add >>> lines inside a triple-quoted docstring.";
            testsEl.appendChild(empty);
            status.textContent = "no tests";
            root.setAttribute("data-lc-doctest", "0/0");
            repaintBound();
            return;
          }
          var summary = document.createElement("div");
          summary.className = "lc-pyrun-test-summary";
          testsEl.appendChild(summary);
          var passed = 0;
          rows.forEach(function (r) {
            var row = document.createElement("div");
            var expr = r.source.split("\n").join(" ⏎ ");
            row.className = "lc-pyrun-test-row " + (r.ok ? "lc-pyrun-test-pass" : "lc-pyrun-test-fail");
            if (r.ok) { passed++; row.textContent = "✅ line " + r.line + "  " + expr; }
            else if (r.err) row.textContent = "❌ line " + r.line + "  " + expr + "  →  raised " + r.err;
            else row.textContent = "❌ line " + r.line + "  " + expr + "  →  got " + (r.got || "(nothing)") + ", expected " + (r.want || "nothing");
            testsEl.appendChild(row);
          });
          summary.textContent = passed + " passed, " + (rows.length - passed) + " failed";
          /* THE TALLY IS ON THE BLOCK (Michel, 2026-10-27: "the doctests could
             verify stuff, and the proof can verify the doctests are green"):
             a page's proof reads self.page.<id>.doctests, never a selector */
          root.setAttribute("data-lc-doctest", passed + "/" + rows.length);
          status.textContent = "tests done";
          repaintBound();
        }).catch(function(e){
          setOut("Failed to load MicroPython: " + (e.message || String(e)), true);
        });
      });
    }

    /* 🩺 Dr. mypy (lite) — the hints read from the text, mypy's words
       (pycheck.md); nothing runs, so it answers before the runtime loads */
    var mypyBtn = root.querySelector(".lc-pyrun-mypy");
    if (mypyBtn && window.lcDrMypy) {
      mypyBtn.addEventListener("click", function () {
        clearTests();
        var r = window.lcDrMypy(codeEl.value, { file: ID + ".py", strict: opts.mypy !== "loose", pretty: true });
        setOut(r.status === 0 ? "✅ Dr. mypy (lite): no type errors" : "❌ Dr. mypy (lite):\n" + r.out.replace(/\n$/, ""), r.status !== 0);
        root.setAttribute("data-lc-mypy", r.status === 0 ? "clean" : String(r.problems.filter(function (p) { return p.severity === "error"; }).length));
        status.textContent = r.status === 0 ? "types clean" : "type errors";
      });
    }

    clearBtn.addEventListener("click", function(){
      out.textContent = "click ▶ Run to execute";
      out.classList.add("lc-empty");
      view.innerHTML = "";
      clearTests();
      status.textContent = mp ? "ready" : "";
    });

    if (BOUND) {
      loadMp().catch(function(){ });
    }
  }

  function buildRunner(opts) {
    var id = opts.id;
    var bound = opts.bound || "";
    var folded = opts.folded;
    var rows = opts.rows || 6;
    var div = document.createElement("div");
    div.className = "lc-pyrun";
    div.id = "lc-pyrun-" + id;
    div.setAttribute("data-lc-id", id);        /* self.page.<id> in a proof (Michel, 2026-10-27) */
    var html = "";
    if (bound) html += '<div class="lc-pyrun-bound" id="lc-pyrun-' + id + '-bound"></div>';
    if (folded) {
      html += '<details class="lc-pyrun-fold"><summary>🐍 Edit &amp; run Python</summary>';
    } else {
      html += '<div class="lc-pyrun-title">🐍 <span>Python runner</span><span class="lc-pyrun-lang">python</span></div>';
    }
    html += '<div class="lc-pyrun-editor"><div class="lc-pyrun-gutter"><div class="lc-pyrun-gutter-inner"></div></div><div class="lc-pyrun-codewrap"><pre class="lc-pyrun-marks" aria-hidden="true"><code></code></pre><pre class="lc-pyrun-hl" aria-hidden="true" tabindex="-1"><code class="language-python"></code></pre><textarea class="lc-pyrun-code" rows="' + rows + '" spellcheck="false" aria-label="Python editor"></textarea><pre class="lc-pyrun-subs" hidden aria-label="Subtitles: what each part of the program is"></pre></div></div>';
    /* THE BAR SPEAKS SOFTLY (Michel, 2026-10-27: "make the buttons more
       subtle (icons + tooltips for labels) except for ▶ Run; make the
       subtitles button more an on/off switch so the current state is
       visible"): ▶ Run keeps its word; the rest are icons with a tooltip
       and an aria-label; 💬 is a switch that shows its state. */
    html += '<div class="lc-pyrun-grip" role="separator" aria-orientation="horizontal" title="Drag to make the editor taller or shorter — double-click to reset"></div>';
    html += '<div class="lc-pyrun-bar"><button class="lc-pyrun-run">▶ Run</button>' +
      '<button class="lc-pyrun-test lc-pyrun-icon" title="Test — run the >>> examples in the docstrings" aria-label="Test">🧪</button>' +
      (opts.mypy && opts.mypy !== "false" ? '<button class="lc-pyrun-mypy lc-pyrun-icon" title="Dr. mypy (lite) — check the type hints" aria-label="Dr. mypy">🩺</button>' : '') +
      '<button class="lc-pyrun-clear" title="Clear the output">Clear</button>' +
      '<button class="lc-pyrun-subs-btn lc-pyrun-switch" role="switch" aria-checked="false" title="Subtitles — what each part of the program is" aria-label="Subtitles"><span class="lc-pyrun-track"><span class="lc-pyrun-knob"></span></span>💬</button>' +
      '<span class="lc-pyrun-status"></span></div>';
    html += '<div class="lc-pyrun-subline" hidden></div>';
    html += '<pre class="lc-pyrun-out lc-empty">click ▶ Run to execute</pre>';
    html += '<div class="lc-pyrun-view" id="lc-pyrun-' + id + '-view"></div>';
    html += '<div class="lc-pyrun-tests" id="lc-pyrun-' + id + '-tests"></div>';
    if (folded) html += '</details>';
    div.innerHTML = html;
    div.querySelector(".lc-pyrun-code").value = opts.code || "";
    return div;
  }

  var REPL_BOOTSTRAP = [
    "def _repl_eval(line):",
    "    try:",
    "        _code = compile(line, '<repl>', 'eval')",
    "        _val = eval(_code)",
    "        if _val is not None:",
    "            print(repr(_val))",
    "    except SyntaxError:",
    "        try:",
    "            exec(compile(line, '<repl>', 'exec'))",
    "        except BaseException as e:",
    "            print(repr(e))",
    "    except BaseException as e:",
    "        print(repr(e))"
  ].join("\n");

  function buildRepl(opts) {
    var id = opts.id;
    var div = document.createElement("div");
    div.className = "lc-pyrepl";
    div.id = "lc-pyrepl-" + id;
    div.innerHTML =
      '<div class="lc-pyrepl-title">🐍 <span>Python REPL</span><button class="lc-pyrepl-reset" title="reset runtime — clears state">↻</button><span class="lc-pyrepl-status"></span></div>' +
      '<pre class="lc-pyrepl-transcript"></pre>' +
      '<div class="lc-pyrepl-input-row"><span class="lc-pyrepl-marker">&gt;&gt;&gt;</span><input class="lc-pyrepl-input" type="text" spellcheck="false" autocapitalize="off" autocorrect="off" autocomplete="off" aria-label="Python console input" /></div>';
    return div;
  }

  function attachRepl(rootId, opts) {
    opts = opts || {};
    var root = document.getElementById(rootId);
    if (!root || root.dataset.lcAttached) return;
    root.dataset.lcAttached = "1";
    var transcript = root.querySelector(".lc-pyrepl-transcript");
    var input = root.querySelector(".lc-pyrepl-input");
    var status = root.querySelector(".lc-pyrepl-status");
    var resetBtn = root.querySelector(".lc-pyrepl-reset");
    var INIT = opts.init || "";
    var buf = "";
    var mp = null;
    var loading = null;
    var history = [];
    var historyIdx = -1;

    function append(text, cls) {
      if (cls) {
        var span = document.createElement("span");
        span.className = cls;
        span.textContent = text;
        transcript.appendChild(span);
      } else {
        transcript.appendChild(document.createTextNode(text));
      }
      transcript.scrollTop = transcript.scrollHeight;
    }

    function loadMp() {
      if (mp) return Promise.resolve(mp);
      if (loading) return loading;
      input.disabled = true;
      status.textContent = "loading runtime…";
      loading = lcMpy()
        .then(function(instance){
          mp = instance;
          try { mp.runPython(REPL_BOOTSTRAP); } catch (e) { }
          if (INIT) {
            try { mp.runPython(INIT); } catch (e) { }
          }
          input.disabled = false;
          input.focus();
          status.textContent = "";
          return mp;
        })
        .catch(function(e){
          input.disabled = false;
          status.textContent = "load failed";
          loading = null;
          throw e;
        });
      return loading;
    }

    function submit(line) {
      window._lcMpyOut = null;
      if (!line) {
        append(">>> \n", "lc-pyrepl-prompt-line");
        return;
      }
      history.push(line);
      historyIdx = history.length;
      loadMp().then(function(m){
        append(">>> " + line + "\n", "lc-pyrepl-prompt-line");
        buf = "";
        window._lcMpyOut = function (t) { buf += t; };
        try { m.runPython(REPL_BOOTSTRAP); } catch (e0) { }
        try {
          m.runPython("_repl_eval(" + JSON.stringify(desugarFstrings(line)) + ")");
          if (buf) {
            if (buf.charAt(buf.length - 1) !== "\n") buf += "\n";
            var isErr = /^(SyntaxError|NameError|TypeError|ValueError|ZeroDivisionError|IndexError|KeyError|AttributeError|ImportError|RuntimeError|Exception)/.test(buf);
            append(buf, isErr ? "lc-pyrepl-err" : null);
          }
        } catch (e) {
          var msg = e.message || String(e);
          append(msg + "\n", "lc-pyrepl-err");
          append("(runtime crashed — state lost, reloading on next command)\n", "lc-pyrepl-err");
          mp = null;
          window._lcMpyOut = null;
          loading = null;
        }
      }).catch(function(e){
        append("Failed to load MicroPython: " + (e.message || String(e)) + "\n", "lc-pyrepl-err");
      });
    }

    if (resetBtn) {
      resetBtn.addEventListener("click", function(){
        mp = null;
        loading = null;
        history = [];
        historyIdx = -1;
        transcript.innerHTML = "";
        append("(runtime reset — state cleared)\n", "lc-pyrepl-err");
        input.focus();
      });
    }

    input.addEventListener("keydown", function(e){
      if (e.key === "Enter") {
        e.preventDefault();
        var line = input.value;
        input.value = "";
        submit(line);
      } else if (e.key === "ArrowUp") {
        if (history.length === 0) return;
        e.preventDefault();
        historyIdx = Math.max(0, historyIdx - 1);
        input.value = history[historyIdx] || "";
      } else if (e.key === "ArrowDown") {
        if (history.length === 0) return;
        e.preventDefault();
        historyIdx = Math.min(history.length, historyIdx + 1);
        input.value = history[historyIdx] || "";
      }
    });

    // Focus input when the transcript area is clicked
    root.addEventListener("click", function(e){
      if (e.target !== input) input.focus();
    });
  }

  var REPL_ID = 0;
  function upgradeRepl(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    var codeNode = el.querySelector("code");
    var raw = codeNode ? codeNode.textContent.replace(/\n+$/, "") : "";
    var id = el.id || ("_repl" + (++REPL_ID));
    var opts = {
      id: id,
      init: el.getAttribute("init") || raw || ""
    };
    var widget = buildRepl(opts);
    el.parentNode.replaceChild(widget, el);
    attachRepl("lc-pyrepl-" + id, opts);
  }


  var RUN_ID = 0;
  function upgradeRun(el) {
    if (el.dataset.lcUpgraded) return;
    el.dataset.lcUpgraded = "1";
    var codeNode = el.querySelector("code");
    var raw = codeNode ? codeNode.textContent.replace(/\n+$/, "") : "";
    var silent = el.hasAttribute("silent") && el.getAttribute("silent") !== "false";
    if (silent) {
      el.parentNode.removeChild(el);
      runSilent(raw);
      return;
    }
    var code = raw;
    var initFromCode = "";
    var sepRe = /^#\s*-{3,}\s*$\n?/m;
    var sepMatch = raw.match(sepRe);
    if (sepMatch) {
      initFromCode = raw.substring(0, sepMatch.index).replace(/\n+$/, "");
      code = raw.substring(sepMatch.index + sepMatch[0].length);
    }
    var id = el.id || ("r" + (++RUN_ID));
    var opts = {
      id: id,
      code: code,
      bound: el.getAttribute("bound") || "",
      init: el.getAttribute("init") || initFromCode || "",
      rows: parseInt(el.getAttribute("rows"), 10) || 0,   /* 0: the editor fits its program */
      folded: el.hasAttribute("folded") && el.getAttribute("folded") !== "false",
      expected: el.getAttribute("expected") || "",
      mypy: el.getAttribute("mypy") || "",    /* "true": a 🩺 Dr. mypy (lite) button, strict as the deck runs it */
      subtitles: el.getAttribute("subtitles") || ""   /* "on": the 💬 subtitles start shown */
    };
    var runner = buildRunner(opts);
    el.parentNode.replaceChild(runner, el);
    attach("lc-pyrun-" + id, opts);
  }

  /* The shared page runtime: one persistent MicroPython instance that silent
     setup code seeds and reactive {= cells } read. It's separate from the
     button/preamble instance (window._lcMpReady) — this one holds page data
     and model defs, so a `.run silent` block is the page's model, and its
     names stay live for the cells. Exported so cells.md evaluates in it. */
  function pageRuntime() {
    if (window._lcPageRuntime) return window._lcPageRuntime;
    var view = document.createElement("div");
    view.id = "lc-pyrun-page-view"; view.style.display = "none";
    var bound = document.createElement("div");
    bound.id = "lc-pyrun-page-bound"; bound.style.display = "none";
    document.body.appendChild(view);
    document.body.appendChild(bound);
    window._lcPageRuntime = Promise.all([lcMpy(), loadJsYaml()])
      .then(function(results){ return results[0]; })
      .then(function(mp){
        try { mp.runPython(BOOTSTRAP_TPL.replace(/__ID__/g, "page")); }
        catch (e) { if (window.console) console.warn("[lc page-rt bootstrap]", e.message || e); }
        return mp;
      });
    return window._lcPageRuntime;
  }
  window.lcPageRuntime = pageRuntime;

  function runSilent(code) {
    pageRuntime()
      .then(function(mp){
        try { mp.runPython(desugarFstrings(code)); } catch (e) { if (window.console) console.warn("[lc silent code]", e.message || e); }
        /* the page model just changed — cells and diagrams recompute */
        try { document.dispatchEvent(new CustomEvent("lc-model-changed", { detail: { source: "run-silent" } })); } catch (e) {}
      })
      .catch(function(e){ if (window.console) console.warn("[lc silent load]", e.message || e); });
  }

  // Export the runner for Liquid-rendered python_run.md blocks, then flush
  // any attach calls they queued while this file was still parsing.
  window.lcPyrun = { attach: attach, edit: editRange };
  if (window.lcPyrunQueue) {
    window.lcPyrunQueue.forEach(function(fn){ try { fn(); } catch (e) {} });
    window.lcPyrunQueue = null;
  }


  function upgradeButton(el) {
    var a = el.querySelector("a");
    if (!a) return;

    // Optional Python click handler: a code block tagged {: .onclick }
    // immediately following the button paragraph.
    var handlerCode = "";
    var sib = el.nextElementSibling;
    while (sib && !sib.textContent.trim()) sib = sib.nextElementSibling;
    if (sib && sib.classList.contains("onclick") && sib.querySelector("code")) {
      handlerCode = sib.querySelector("code").textContent;
      sib.parentNode.removeChild(sib);
    }

    if (handlerCode) {
      // Interactive button: replace the link with a real <button> so the
      // Python step layer (self.page.<id>.click()) and real clicks both run it.
      var lcId = el.getAttribute("data-lc-id") || el.getAttribute("id") || "";
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "lc-button";
      btn.textContent = (a.textContent || el.textContent || "").trim();
      if (lcId) btn.setAttribute("data-lc-id", lcId);
      btn.setAttribute("data-lc-py", handlerCode);
      btn.addEventListener("click", function () { runButtonHandler(btn); });
      el.parentNode.replaceChild(btn, el);
      return;
    }

    // Plain styled-link button (existing behaviour).
    /* the component page documents `kind=` — the code only read the older
       style-variant, so every kind="outline" silently rendered default
       (module 05's 🏠 button, 2026-08-18). Both spellings work; kind wins. */
    var style = el.getAttribute("kind") || el.getAttribute("style-variant") || "";
    stayHere(a);
    a.classList.add("button");
    if (style) a.classList.add("button-" + style);
    el.classList.remove("button");
  }

  /* A handler fence may be JUST the body — ideally one line, `button` in
     scope. The def line is the ENGINE's (Michel, 2026-08-11: beginners see
     only the if); it is added here for execution, and the lens shows it
     dimmed and locked. A full `def on_click…` still works unchanged. */
  window.lcWrapHandler = function (code) {
    if (/^\s*def\s+on_click\s*\(/m.test(code)) return code;
    return "def on_click(button):\n" + String(code).split("\n")
      .map(function (l) { return "    " + l; }).join("\n");
  };

  // Run a button's Python on_click(handler) via the shared MicroPython instance.
  function runButtonHandler(btn) {
    var pyCode = btn.getAttribute("data-lc-py") || "";
    if (!pyCode) return;
    var lcId = btn.getAttribute("data-lc-id") || "";
    var preamble = (document.getElementById("lc-steps-preamble") || {}).textContent || "";
    /* A BARE BODY IS THE PAGE'S OWN LINES, not a function's. Wrapped in a
       def, every name a beginner assigns died with the click — Michel wrote
       `message = …` in a button and `{= message }` beside it stayed empty
       (2026-09-01). A bare fence now runs at module scope with `button`
       bound, so what the lines set, the page can read. An explicit
       `def on_click(…)` keeps Python's own rules: its locals stay local. */
    var bare = !/^\s*def\s+on_click\s*\(/m.test(pyCode);
    var head = preamble + "\n"
      + "button = _wrap(js.window.document.querySelector(\"[data-lc-id='" + lcId + "']\"))\n";
    var fullCode = head + (bare ? pyCode + "\n" : pyCode + "\non_click(button)\n");
    if (!window._lcMpReady) window._lcMpReady = lcMpy();
    window._lcMpReady.then(function (mp) {
      var runFn = mp.runPython || mp.exec || mp.pyexec || mp.run;
      /* a handler that fails shows ⚠️ beside its button, and why (Michel, 2026-10-12) */
      try { if (runFn) runFn.call(mp, fullCode); if (window.lcWarn) window.lcWarn(btn, ""); }
      catch (e) {
        console.error("[lc-button]", e);
        if (window.lcWarn) window.lcWarn(btn, "This button's lines failed: " +
          (window.lcPyError ? window.lcPyError(e, head.split("\n").length - 1) : (e.message || e)));
      }
      /* a click changed the page's data, exactly as a form edit does — so the
         page's cells recompute on the same bus, and never a second later */
      try { document.dispatchEvent(new CustomEvent("lc-model-changed",
                                   { detail: { source: "button" } })); } catch (e) {}
    });
  }

  /* A BUTTON THAT GOES NOWHERE STAYS HERE (Michel, 2026-10-11: "the empty
     button, once clicked, leads elsewhere"): [📞 Call](#) has no job yet —
     its "#" would rewrite the runner's address (#src=…) and lose the page. */
  function stayHere(a) {
    var h = (a.getAttribute("href") || "").trim();
    if (h === "#" || h === "") a.addEventListener("click", function (e) { e.preventDefault(); });
  }

  /* ── boot ────────────────────────────────────────────────────── */
  /* code_chrome.md (loaded first, via topbar) provides the scan registry. */

  /* the inline form — [x](y){: .button kind="…" } — tags the <a> itself,
     so the paragraph upgrader above never sees it; map the knob here too */
  function upgradeButtonLink(a) {
    stayHere(a);
    var k = a.getAttribute("kind") || a.getAttribute("style-variant") || "";
    if (k) a.classList.add("button-" + k);
  }

  if (window.lcRegisterUpgrader) {
    window.lcRegisterUpgrader(".highlighter-rouge.run, pre.run", upgradeRun);
    window.lcRegisterUpgrader(".highlighter-rouge.repl, pre.repl", upgradeRepl);
    window.lcRegisterUpgrader("p.button", upgradeButton);
    window.lcRegisterUpgrader("a.button[kind], a.button[style-variant]", upgradeButtonLink);
  }

})();
</script>
