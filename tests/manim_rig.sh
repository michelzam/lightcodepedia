#!/usr/bin/env bash
# LOCAL HARNESS ONLY — install the manim toolchain in one command.
# Same contract as local_rig.sh: the sandbox is ephemeral, so this is
# idempotent and cheap to re-run. CI never uses this file.
#
# Three things bite, in this order, and none of the error messages say so:
#   1. manim's build needs pangocairo HEADERS, not just the runtime libs
#      ("RequiredDependencyException: pangocairo >= 1.30.0 is required").
#   2. Debian's setuptools has no `install_layout`, which breaks building the
#      `srt` wheel ("AttributeError: install_layout"). A pip setuptools fixes
#      it, but plain `pip install -U setuptools` cannot uninstall the Debian
#      copy (no RECORD file) — it needs --ignore-installed.
#   3. `apt install ffmpeg` pulls recommends that 404 on this mirror
#      (libcaca0, mesa-va-drivers…). --no-install-recommends skips them.
#
# There is NO LaTeX here, on purpose: it is a very large install and the course
# needs no equations. That means Text() (pango) works and MathTex() does not.
set -e

echo "── system libs ──"
apt-get update -qq 2>/dev/null || true
apt-get install -y -qq libpango1.0-dev libcairo2-dev
apt-get install -y -qq --no-install-recommends ffmpeg
pkg-config --modversion pangocairo >/dev/null || {
  echo "pangocairo headers still missing — manim cannot build"; exit 1; }

echo "── python ──"
python3 -c "import manim" 2>/dev/null || {
  pip install --quiet --ignore-installed setuptools wheel
  pip install --quiet manim
}

python3 - <<'PY'
import manim, shutil, sys
print("manim", manim.__version__)
print("ffmpeg", shutil.which("ffmpeg") or "MISSING")
PY

echo
echo "rig up. Stills first, then the scene:"
echo "  bash tests/local_rig.sh"
echo "  PW_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome \\"
echo "  MARKED_JS=\$PWD/.libs/marked.min.js JS_YAML=\$PWD/.libs/js-yaml.min.js \\"
echo "  AG_GRID_DIR=\$PWD/.libs/ag CHART_JS=\$PWD/.libs/chart.umd.min.js \\"
echo "  MPY_DIR=\$PWD/.libs/mpy python3 tests/shots.py hq/shots"
echo "  manim -qh hq/anim/wiring_recap.py WiringRecap"
