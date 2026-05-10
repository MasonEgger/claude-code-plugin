#!/usr/bin/env python3
# ABOUTME: Local HTTP server for /bpe:review.
# Serves a generated HTML review artifact, accepts feedback JSON via POST /save, then exits.

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import threading
import webbrowser
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

PID_FILE = Path("/tmp/bpe-review-server.pid")
SHUTDOWN_DELAY_SECONDS = 3
TAILSCALE_PROBE_TIMEOUT_SECONDS = 2


def pick_bind_address() -> str:
    """Return the local Tailscale IPv4 if the daemon is up, otherwise localhost.

    Reviewing on a phone or another laptop is the common case — when Tailscale
    is active, bind to the tailnet IP so other devices on the tailnet can reach
    the review page directly. Falls back silently to 127.0.0.1 if Tailscale is
    not installed, the daemon is down, or the device is logged out.
    """
    if shutil.which("tailscale") is None:
        return "127.0.0.1"
    try:
        result = subprocess.run(
            ["tailscale", "ip", "-4"],
            capture_output=True,
            text=True,
            timeout=TAILSCALE_PROBE_TIMEOUT_SECONDS,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return "127.0.0.1"
    if result.returncode != 0:
        return "127.0.0.1"
    for line in result.stdout.splitlines():
        ip = line.strip()
        if ip:
            return ip
    return "127.0.0.1"


def kill_existing_server() -> None:
    if not PID_FILE.exists():
        return
    try:
        old_pid = int(PID_FILE.read_text().strip())
        os.kill(old_pid, 15)
    except (ValueError, ProcessLookupError, PermissionError):
        pass
    PID_FILE.unlink(missing_ok=True)


def write_pid_file() -> None:
    PID_FILE.write_text(str(os.getpid()))


def make_handler(
    html_bytes: bytes,
    feedback_path: Path,
    source_artifact: str,
    shutdown_event: threading.Event,
) -> type[BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_: object) -> None:
            return  # quiet

        def do_GET(self) -> None:  # noqa: N802 (BaseHTTPRequestHandler API)
            if self.path in ("/", "/index.html"):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(html_bytes)
                return
            self.send_response(404)
            self.end_headers()

        def do_POST(self) -> None:  # noqa: N802
            if self.path != "/save":
                self.send_response(404)
                self.end_headers()
                return
            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length).decode("utf-8")
            try:
                payload = json.loads(body)
            except json.JSONDecodeError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid JSON")
                return
            payload["artifact_path"] = source_artifact
            payload["saved_at"] = datetime.now().isoformat()
            feedback_path.write_text(json.dumps(payload, indent=2))
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(
                b"<!doctype html><meta charset=utf-8>"
                b"<title>Saved</title>"
                b"<style>body{font-family:system-ui;max-width:40rem;margin:4rem auto;padding:0 1rem;line-height:1.5}</style>"
                b"<h1>Saved</h1>"
                b"<p>Feedback recorded. You can close this tab.</p>"
                b"<p>Back in Claude Code, run <code>/bpe:apply-review</code> to load and apply your feedback.</p>"
            )
            threading.Timer(SHUTDOWN_DELAY_SECONDS, shutdown_event.set).start()

    return Handler


HEAD_ASSETS = """
<script src="https://cdn.tailwindcss.com"></script>
<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
  mermaid.initialize({ startOnLoad: false, theme: 'default', securityLevel: 'loose' });
  window.__bpeMermaid = mermaid;
</script>
"""

RUNTIME_HELPERS = """
<script>
(function() {
  function enableCheckboxes() {
    document.querySelectorAll('input[type="checkbox"][disabled]').forEach(function(cb) {
      cb.removeAttribute('disabled');
      cb.classList.add('cursor-pointer');
    });
  }
  function convertMermaidBlocks() {
    var blocks = document.querySelectorAll('pre > code.language-mermaid, pre > code.lang-mermaid');
    blocks.forEach(function(code) {
      var pre = code.parentElement;
      var container = document.createElement('div');
      container.className = 'mermaid';
      container.textContent = code.textContent;
      pre.parentNode.replaceChild(container, pre);
    });
  }
  function renderMermaid() {
    if (!window.__bpeMermaid) {
      setTimeout(renderMermaid, 50);
      return;
    }
    var nodes = document.querySelectorAll('.mermaid:not([data-processed="true"])');
    if (nodes.length === 0) return;
    window.__bpeMermaid.run({ nodes: nodes }).catch(function(err) {
      console.error('Mermaid render failed:', err);
    });
  }
  function init() {
    enableCheckboxes();
    convertMermaidBlocks();
    renderMermaid();
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
</script>
"""


def inject_head_assets(html_text: str) -> str:
    """Inject Tailwind CDN and Mermaid ESM module into <head> (or top of doc)."""
    if "</head>" in html_text:
        return html_text.replace("</head>", HEAD_ASSETS + "</head>", 1)
    if "<body" in html_text:
        return html_text.replace("<body", HEAD_ASSETS + "<body", 1)
    return HEAD_ASSETS + html_text


def inject_runtime_helpers(html_text: str) -> str:
    """Inject checkbox enabler + Mermaid block converter before </body>."""
    if "</body>" in html_text:
        return html_text.replace("</body>", RUNTIME_HELPERS + "</body>", 1)
    return html_text + RUNTIME_HELPERS


def inject_save_script(html_text: str, save_url: str) -> str:
    script = f"""
<script>
(function() {{
  function collectFeedback() {{
    var sections = [];
    document.querySelectorAll('[data-section-id]').forEach(function(el) {{
      var id = el.getAttribute('data-section-id');
      var heading = el.getAttribute('data-section-heading') || '';
      var commentEl = document.querySelector('[data-section-comment="' + id + '"]');
      var decisionEl = document.querySelector('[data-section-decision="' + id + '"]:checked');
      sections.push({{
        id: id,
        heading: heading,
        comment: commentEl ? commentEl.value : '',
        decision: decisionEl ? decisionEl.value : 'unset'
      }});
    }});
    var globalEl = document.getElementById('global-comment');
    return {{
      sections: sections,
      global_comment: globalEl ? globalEl.value : ''
    }};
  }}
  function bindSave() {{
    var btn = document.getElementById('bpe-save-btn');
    if (!btn) return;
    btn.addEventListener('click', function() {{
      btn.disabled = true;
      btn.textContent = 'Saving…';
      fetch('{save_url}', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify(collectFeedback())
      }}).then(function(r) {{ return r.text(); }}).then(function(t) {{
        document.open(); document.write(t); document.close();
      }}).catch(function(err) {{
        btn.disabled = false;
        btn.textContent = 'Save';
        alert('Save failed: ' + err);
      }});
    }});
  }}
  if (document.readyState === 'loading') {{
    document.addEventListener('DOMContentLoaded', bindSave);
  }} else {{
    bindSave();
  }}
}})();
</script>
"""
    if "</body>" in html_text:
        return html_text.replace("</body>", script + "</body>", 1)
    return html_text + script


def main() -> None:
    if len(sys.argv) < 4:
        print(
            "Usage: review-server.py <html-path> <feedback-output-path> <source-markdown-path>",
            file=sys.stderr,
        )
        sys.exit(2)

    html_path = Path(sys.argv[1])
    feedback_path = Path(sys.argv[2])
    source_artifact = sys.argv[3]

    if not html_path.exists():
        print(f"HTML file not found: {html_path}", file=sys.stderr)
        sys.exit(1)

    kill_existing_server()
    write_pid_file()

    html_text = html_path.read_text(encoding="utf-8")
    shutdown_event = threading.Event()

    bind_addr = pick_bind_address()
    server = HTTPServer((bind_addr, 0), BaseHTTPRequestHandler)
    port = server.server_address[1]
    save_url = f"http://{bind_addr}:{port}/save"
    html_text = inject_head_assets(html_text)
    html_text = inject_runtime_helpers(html_text)
    html_with_script = inject_save_script(html_text, save_url).encode("utf-8")
    server.RequestHandlerClass = make_handler(
        html_with_script, feedback_path, source_artifact, shutdown_event
    )

    url = f"http://{bind_addr}:{port}/"
    print(f"BPE review server: {url}", flush=True)
    if bind_addr != "127.0.0.1":
        print(
            f"  (bound to Tailscale IP {bind_addr} — reachable from other tailnet devices)",
            flush=True,
        )
    print(f"Reviewing: {source_artifact}", flush=True)
    print(f"Feedback will be written to: {feedback_path}", flush=True)
    print("Click Save in the browser when done. Re-run /bpe:review to restart.", flush=True)

    threading.Thread(target=lambda: webbrowser.open(url), daemon=True).start()
    threading.Thread(target=server.serve_forever, daemon=True).start()

    shutdown_event.wait()
    server.shutdown()
    PID_FILE.unlink(missing_ok=True)
    print(f"Saved feedback to {feedback_path}", flush=True)


if __name__ == "__main__":
    main()
