#!/usr/bin/env python3
"""Capture the offline demos into docs/examples/emnify-sample-runs.md.   python scripts/capture_examples.py

Synthetic data only. Re-run after changing weights, rules or fixtures so the examples never go stale.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUNS = [
    (["enrichment.run", "--dry-run"], "Enrichment: dedupe plan, waterfall, mapping, dry-run upsert"),
    (["outbound.run", "--dry-run"], "Outbound: ranking, held handoff, coverage low / expected / high"),
    (["outbound.sensitivity"], "Coverage sensitivity to ramp length and realization"),
    (["agents.run_evals"], "Agent eval suites"),
    (["knowledge.tools", "lookup", "launch outbound list"], "Knowledge router lookup"),
]


def main() -> int:
    out = ["# Sample runs", "",
           "Captured output of the offline demos on synthetic data: fictional companies, placeholder weights, abstract "
           "revenue units. Nothing here is emnify data or a result. Regenerate with `python scripts/capture_examples.py`."]
    for args, title in RUNS:
        res = subprocess.run([sys.executable, "-m", *args], cwd=ROOT, capture_output=True, text=True, check=True)
        shown = " ".join(a if " " not in a else f'"{a}"' for a in args)
        out += ["", f"## {title}", "", "```text", f"$ python -m {shown}", res.stdout.rstrip(), "```"]
    path = ROOT / "docs" / "examples" / "emnify-sample-runs.md"
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"wrote {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
