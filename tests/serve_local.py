#!/usr/bin/env python3
"""Static server for the local BDD harness.

GitHub Pages serves the lab under a project base (michelzam.github.io/lightcodelab)
and resolves extensionless URLs ("/components/block") to their ".html" file.
A plain `python -m http.server` does neither, so a local build at a domain root
hides every base-path bug (root-absolute "/assets/x" that only heals at runtime)
and 404s on the extensionless paths the scenarios navigate to.

This mirrors production locally:
  * --base /lightcodelab  mounts the whole site under that prefix, so
    window.lcBase computes to "/lightcodelab" and unhealed URLs 404 in the
    suite instead of on the deployed lab.
  * extensionless requests fall back to "<path>.html" (Jekyll's ugly permalinks).

Point the suite at it with  BASE_URL=http://localhost:<port><base>  (see Makefile
target `pedia-lab`). Pass --base "" to serve at a domain root (pedia parity).
"""
import argparse
import os
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler


class BaseHandler(SimpleHTTPRequestHandler):
    base = ""  # url prefix the site is mounted under, e.g. "/lightcodelab"

    def translate_path(self, path):
        # strip the mount prefix so "/lightcodelab/components/block" maps into
        # the served directory; a request outside the prefix stays a 404
        clean = path.split("?", 1)[0].split("#", 1)[0]
        if self.base and clean != self.base and not clean.startswith(self.base + "/"):
            return os.path.join(self.directory, "__outside_base__")
        if self.base:
            clean = clean[len(self.base):] or "/"
        rebuilt = clean + (path[len(path.split("?", 1)[0]):] if "?" in path else "")
        fs = super().translate_path(rebuilt)
        # extensionless → .html (Jekyll ugly permalinks), unless it's a directory
        root, ext = os.path.splitext(fs)
        if not ext and not os.path.isdir(fs) and os.path.isfile(fs + ".html"):
            return fs + ".html"
        return fs

    def send_error(self, code, message=None, explain=None):
        # GitHub Pages serves the site's 404.html (status 404) for every miss —
        # that page doubles as the LightNode router, so mirror it locally or
        # the router is untestable here
        page = os.path.join(self.directory, "404.html")
        if code == 404 and os.path.isfile(page):
            with open(page, "rb") as f:
                body = f.read()
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            try:
                self.wfile.write(body)
            except (BrokenPipeError, ConnectionResetError):
                pass
            return
        super().send_error(code, message, explain)

    def log_message(self, *args):
        pass  # quiet — the suite is the signal, not access logs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True, help="built site root (e.g. docs/_site)")
    ap.add_argument("--base", default="", help='mount prefix, e.g. "/lightcodelab"')
    ap.add_argument("--port", type=int, default=4000)
    a = ap.parse_args()
    handler = partial(
        type("H", (BaseHandler,), {"base": a.base.rstrip("/")}),
        directory=os.path.abspath(a.dir),
    )
    srv = HTTPServer(("127.0.0.1", a.port), handler)
    print("serving %s at http://127.0.0.1:%d%s/" % (a.dir, a.port, a.base.rstrip("/")))
    srv.serve_forever()


if __name__ == "__main__":
    main()
