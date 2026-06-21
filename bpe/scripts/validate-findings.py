#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""Validate a bpe:validator findings JSON block against the canonical schema.

Usage:
    validate-findings.py            # read JSON from stdin
    validate-findings.py FILE       # read JSON from FILE
    validate-findings.py -          # read JSON from stdin (explicit)

Exit codes:
    0  Input is well-formed; canonical JSON is written to stdout.
    1  Input is malformed; a human-readable error is written to stderr.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

SEVERITIES = frozenset({"block", "warn", "info"})
VERDICTS = frozenset({"block", "warn", "clean"})
REQUIRED_TOP = frozenset({"validator", "verdict", "findings", "iter"})
OPTIONAL_TOP = frozenset({"notes"})
REQUIRED_FINDING = frozenset({"severity", "file", "message"})
OPTIONAL_FINDING = frozenset({"line", "rule", "suggested_fix", "reference"})


def fail(msg: str) -> None:
    sys.stderr.write(f"validate-findings: {msg}\n")
    sys.exit(1)


def check_top(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict):
        fail(f"top-level value must be a JSON object, got {type(data).__name__}")
    keys = set(data.keys())
    missing = REQUIRED_TOP - keys
    if missing:
        fail(f"missing required top-level keys: {sorted(missing)}")
    unknown = keys - REQUIRED_TOP - OPTIONAL_TOP
    if unknown:
        fail(f"unknown top-level keys: {sorted(unknown)}")
    if not isinstance(data["validator"], str) or not data["validator"]:
        fail("validator: must be a non-empty string")
    if data["verdict"] not in VERDICTS:
        fail(f"verdict: expected one of {sorted(VERDICTS)}, got {data['verdict']!r}")
    if not isinstance(data["iter"], int) or isinstance(data["iter"], bool) or data["iter"] < 1:
        fail(f"iter: must be a positive integer, got {data['iter']!r}")
    if not isinstance(data["findings"], list):
        fail(f"findings: must be a list, got {type(data['findings']).__name__}")
    if "notes" in data and not isinstance(data["notes"], str):
        fail(f"notes: must be a string, got {type(data['notes']).__name__}")
    return data


def check_finding(idx: int, f: Any) -> None:
    prefix = f"findings[{idx}]"
    if not isinstance(f, dict):
        fail(f"{prefix}: must be an object, got {type(f).__name__}")
    keys = set(f.keys())
    missing = REQUIRED_FINDING - keys
    if missing:
        fail(f"{prefix}: missing required keys: {sorted(missing)}")
    unknown = keys - REQUIRED_FINDING - OPTIONAL_FINDING
    if unknown:
        fail(f"{prefix}: unknown keys: {sorted(unknown)}")
    if f["severity"] not in SEVERITIES:
        fail(
            f"{prefix}.severity: expected one of {sorted(SEVERITIES)}, "
            f"got {f['severity']!r}"
        )
    if not isinstance(f["file"], str) or not f["file"]:
        fail(f"{prefix}.file: must be a non-empty string")
    if not isinstance(f["message"], str) or not f["message"]:
        fail(f"{prefix}.message: must be a non-empty string")
    if "line" in f and (
        not isinstance(f["line"], int) or isinstance(f["line"], bool) or f["line"] < 1
    ):
        fail(f"{prefix}.line: must be a positive integer, got {f['line']!r}")
    for opt in ("rule", "suggested_fix", "reference"):
        if opt in f and not isinstance(f[opt], str):
            fail(f"{prefix}.{opt}: must be a string, got {type(f[opt]).__name__}")


def check_consistency(data: dict[str, Any]) -> None:
    severities = [f["severity"] for f in data["findings"]]
    has_block = "block" in severities
    has_warn = "warn" in severities
    verdict = data["verdict"]
    if has_block and verdict != "block":
        fail(
            f"verdict mismatch: findings contain a 'block' severity but verdict is "
            f"{verdict!r}; expected 'block'"
        )
    if not has_block and has_warn and verdict != "warn":
        fail(
            f"verdict mismatch: findings contain 'warn' but no 'block', so verdict "
            f"must be 'warn'; got {verdict!r}"
        )
    if not has_block and not has_warn and verdict != "clean":
        fail(
            f"verdict mismatch: no 'block' or 'warn' findings, so verdict must be "
            f"'clean'; got {verdict!r}"
        )


def canonicalize(data: dict[str, Any]) -> dict[str, Any]:
    canon: dict[str, Any] = {
        "validator": data["validator"],
        "verdict": data["verdict"],
        "iter": data["iter"],
        "findings": [],
    }
    for f in data["findings"]:
        cf: dict[str, Any] = {"severity": f["severity"], "file": f["file"]}
        if "line" in f:
            cf["line"] = f["line"]
        if "rule" in f:
            cf["rule"] = f["rule"]
        cf["message"] = f["message"]
        if "suggested_fix" in f:
            cf["suggested_fix"] = f["suggested_fix"]
        if "reference" in f:
            cf["reference"] = f["reference"]
        canon["findings"].append(cf)
    if "notes" in data:
        canon["notes"] = data["notes"]
    return canon


def main() -> None:
    if len(sys.argv) > 2:
        fail("usage: validate-findings.py [PATH | -]   (default: stdin)")
    source = sys.argv[1] if len(sys.argv) == 2 else "-"
    try:
        raw = sys.stdin.read() if source == "-" else Path(source).read_text()
    except OSError as e:
        fail(f"cannot read {source!r}: {e}")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        fail(f"input is not valid JSON: {e}")
    data = check_top(data)
    for i, f in enumerate(data["findings"]):
        check_finding(i, f)
    check_consistency(data)
    canon = canonicalize(data)
    sys.stdout.write(json.dumps(canon, indent=2, sort_keys=False) + "\n")


if __name__ == "__main__":
    main()
