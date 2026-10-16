#!/usr/bin/env python3
"""Render generated blocks in the docs from company.yaml.

    python scripts/render_company_docs.py            # rewrite blocks in place
    python scripts/render_company_docs.py --check    # exit 1 if any block is stale (CI)

A block looks like:
    <!-- BEGIN company:stack -->
    ...generated, do not edit...
    <!-- END company:stack -->
Only text between the markers changes. Offline, no credentials.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from emnify_gtm.company import load_company  # noqa: E402

DOCS = ["README.md", "ICP.md", "ROADMAP.md", "DECISIONS.md", "knowledge/README.md", "integrations/README.md", "ROLE_MAP.md"]
BLOCK = re.compile(r"(<!-- BEGIN company:(\w+) -->\n)(.*?)(<!-- END company:\2 -->)", re.S)


def r_stack(c: dict) -> str:
    rows = ["| Need | Tool | Source | State |", "|---|---|---|---|"]
    for key, v in c["stack"].items():
        rows.append(f"| {key.replace('_', ' ')} | {v['tool']} | {v['source']} | {v['state']} |")
    return "\n".join(rows) + "\n"


def r_verticals(c: dict) -> str:
    rows = ["| Vertical | Usage shape | Source | Tier |", "|---|---|---|---|"]
    for v in c["icp_hypotheses"]["verticals"]:
        rows.append(f"| {v['label']} | {v['usage_shape']} | {v['source']} | {v['tier']} |")
    return "\n".join(rows) + "\n"


def r_proof(c: dict) -> str:
    return "\n".join(f"- {p['claim']} ({p['company']}, {p['confidence']})" for p in c["proof_points"]) + "\n"


def r_role(c: dict) -> str:
    r = c["role"]
    return (f"{c['company']['name']} {r['title']} ({r['level']}, {r['function']}), reports to the {r['reports_to']}, "
            f"works with the {', '.join(r['works_with'])}. Job {r['job_id']}, posted {r['posted']}.\n")


def r_regions(c: dict) -> str:
    src = c["regions_source"]
    return (", ".join(c["regions"]) + f" (public: {src['origin']}; {src['note']}. "
            "Which region to start in is hypothesis: validate)\n")


def r_personas(c: dict) -> str:
    return "\n".join(f"- {p['label']}" for p in c["icp_hypotheses"]["buyer_personas"]) + "\n"


def r_qualification(c: dict) -> str:
    return "\n".join(f"- `{f}`" for f in c["icp_hypotheses"]["qualification_fields"]) + "\n"


RENDERERS = {"stack": r_stack, "verticals": r_verticals, "proof": r_proof, "role": r_role, "regions": r_regions,
             "personas": r_personas, "qualification": r_qualification}


def render(text: str, c: dict) -> str:
    def sub(m: re.Match) -> str:
        name = m.group(2)
        if name not in RENDERERS:
            raise SystemExit(f"Unknown block company:{name}")
        return f"{m.group(1)}{RENDERERS[name](c)}{m.group(4)}"
    return BLOCK.sub(sub, text)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    c = load_company()
    stale = []
    for rel in DOCS:
        p = ROOT / rel
        if not p.exists():
            continue
        old = p.read_text(encoding="utf-8")
        new = render(old, c)
        if new != old:
            stale.append(rel)
            if not args.check:
                p.write_text(new, encoding="utf-8")
    if args.check and stale:
        print("Stale generated blocks:", ", ".join(stale))
        return 1
    print("ok" if not stale else "rendered: " + ", ".join(stale))
    return 0


if __name__ == "__main__":
    sys.exit(main())
