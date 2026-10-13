#!/usr/bin/env python3
"""Regenerate the docs/STYLES.md catalog table from catalog/styles.json.

The JSON catalog is the single source of style status; this keeps the human table from
being hand-synchronized in a third place. tests/test_style_contracts.py fails when the
table is stale. Run: python3 tools/gen_style_status.py [--check]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

STATUS_LABEL = {
    "existing-complete-episodes": "Ready — complete episodes (legacy toolkit)",
    "complete-example-technical-and-sampled-visual-review": "Ready — complete example, technical + sampled-frame review",
    "design-specification-sample-pending": "Design specification — sample pending",
    "blocked-on-renderer": "Blocked on renderer",
}


def table() -> str:
    styles = json.loads((ROOT / "catalog/styles.json").read_text())["styles"]
    order = ["3b1b", "swiss", "cassette-futurism", "de-stijl", "bauhaus", "nasa-punk",
             "rhine-lab", "pixel-studio"]
    styles.sort(key=lambda s: order.index(s["id"]) if s["id"] in order else 99)
    lines = ["| ID | Useful for | Read the specification | Status |",
             "| --- | --- | --- | --- |"]
    for s in styles:
        status = STATUS_LABEL.get(s["status"], s["status"])
        if s.get("blocked_reason"):
            status += f" ({s['blocked_reason']})"
        if s.get("example"):
            status += f"; example `{s['example']}`"
        lines.append(f"| `{s['id']}` | {s['useful_for']} | [{s['doc_name']}](../{s['path']}) "
                     f"| {status} |")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="fail instead of writing when stale")
    args = ap.parse_args()
    doc = ROOT / "docs/STYLES.md"
    text = doc.read_text()
    pattern = re.compile(r"(<!-- styles-table:generated -->)\n(?:.*?\n)??(<!-- /styles-table -->)",
                         re.S)
    if not pattern.search(text):
        print("docs/STYLES.md lacks the styles-table markers", file=sys.stderr)
        return 1
    new = pattern.sub(lambda m: m.group(1) + "\n" + table() + "\n" + m.group(2), text)
    if new == text:
        print("docs/STYLES.md is in sync with catalog/styles.json")
        return 0
    if args.check:
        print("docs/STYLES.md is stale; run python3 tools/gen_style_status.py", file=sys.stderr)
        return 1
    doc.write_text(new)
    print("docs/STYLES.md regenerated from catalog/styles.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
