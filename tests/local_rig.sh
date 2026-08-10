#!/usr/bin/env bash
# LOCAL HARNESS ONLY — provision the offline test rig in one command.
# The sandbox reverts anything not committed between sessions, so this
# script is idempotent and cheap to re-run: it (1) fetches the CDN libs
# the engine needs (marked, js-yaml, AG Grid, MicroPython) into .libs/,
# (2) builds the site, (3) serves it on :8899. CI never uses this file.
set -e
REPO="$(cd "$(dirname "$0")/.." && pwd)"
LIBS="$REPO/.libs"
mkdir -p "$LIBS"
grep -qx ".libs/" "$REPO/.git/info/exclude" 2>/dev/null || echo ".libs/" >> "$REPO/.git/info/exclude"
cd "$LIBS"
[ -f marked.min.js ] || { npm pack marked@9 >/dev/null 2>&1 && tar xzf marked-9*.tgz package/marked.min.js -O > marked.min.js && rm -f marked-9*.tgz; }
[ -f js-yaml.min.js ] || { npm pack js-yaml@4 >/dev/null 2>&1 && tar xzf js-yaml-4*.tgz package/dist/js-yaml.min.js -O > js-yaml.min.js && rm -f js-yaml-4*.tgz; }
[ -d mpy ] || { npm pack @micropython/micropython-webassembly-pyscript@latest >/dev/null 2>&1 && tar xzf micropython-*.tgz && mv package mpy && rm -f micropython-*.tgz; }
[ -f chart.umd.min.js ] || { npm pack chart.js@4 >/dev/null 2>&1 && tar xzf chart.js-4*.tgz package/dist/chart.umd.min.js -O > chart.umd.min.js && rm -f chart.js-4*.tgz; }
[ -f alasql.min.js ] || { npm pack alasql@4 >/dev/null 2>&1 && tar xzf alasql-4*.tgz package/dist/alasql.min.js -O > alasql.min.js && rm -f alasql-4*.tgz; }
[ -d maplibre ] || { npm pack maplibre-gl@4 >/dev/null 2>&1 && tar xzf maplibre-gl-4*.tgz && mkdir -p maplibre && mv package/dist/maplibre-gl.js package/dist/maplibre-gl.css maplibre/ && rm -rf package maplibre-gl-4*.tgz; }
[ -d three ] || { npm pack three@0.170.0 >/dev/null 2>&1 && tar xzf three-0.170.0.tgz && mkdir -p three/build three/examples && mv package/build/three.module.js three/build/ && mv package/examples/jsm three/examples/jsm && rm -rf package three-0.170.0.tgz; }
[ -d ag ] || { npm pack ag-grid-community@31 >/dev/null 2>&1 && tar xzf ag-grid-community-31*.tgz && mv package ag && rm -f ag-grid-community-31*.tgz; }
cat > serve.py <<'PYEOF'
import http.server, os, socketserver
ROOT = "/tmp/site_build"
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=ROOT, **k)
    def translate_path(self, path):
        p = super().translate_path(path.split("?")[0].split("#")[0])
        if os.path.isdir(p):
            idx = os.path.join(p, "index.html")
            if os.path.exists(idx): return idx
        if not os.path.exists(p) and not p.endswith(".html") and os.path.exists(p + ".html"):
            return p + ".html"
        return p
    def log_message(self, *a): pass
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("127.0.0.1", 8899), H) as s:
    s.serve_forever()
PYEOF
export PATH=/opt/rbenv/versions/3.3.6/bin:$PATH
cd "$REPO"
PAGES_REPO_NWO=michelzam/lightcodelab bundle exec jekyll build -s docs -d docs/_site 2>&1 | tail -1
rm -rf /tmp/site_build && cp -r docs/_site /tmp/site_build
pkill -f "\.libs/serve\.py" 2>/dev/null || true
sleep 1
setsid python3 "$LIBS/serve.py" < /dev/null > /dev/null 2>&1 &
for i in $(seq 1 10); do curl -s -o /dev/null http://127.0.0.1:8899/run.html && break; sleep 1; done
echo "rig up: $(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8899/run.html)"
echo "env: MAPLIBRE_DIR=$LIBS/maplibre THREE_DIR=$LIBS/three MARKED_JS=$LIBS/marked.min.js JS_YAML=$LIBS/js-yaml.min.js MPY_DIR=$LIBS/mpy AG_GRID_DIR=$LIBS/ag CHART_JS=$LIBS/chart.umd.min.js ALASQL_JS=$LIBS/alasql.min.js"
