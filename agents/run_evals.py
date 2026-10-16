"""Run every agent eval offline. Exit 1 on any failure.   python -m agents.run_evals"""
from __future__ import annotations

import sys
from pathlib import Path

from agents.workflows import personalization, qualification_signal, research_brief
from shared_core.ai_governance.eval_harness import run_evals

EVALS = Path(__file__).resolve().parent / "evals"
SUITES = {"research_brief": research_brief, "qualification_signal": qualification_signal, "personalization": personalization}


def main() -> int:
    failed = 0
    for name, fn in SUITES.items():
        res = run_evals(EVALS / f"{name}_cases.json", fn)
        print(f"{name}: {res['passed']}/{res['total']} ({res['pass_rate']}%)")
        for c in res["cases"]:
            if not c["passed"]:
                failed += 1
                print(f"  FAIL {c['case']}: {c['errors']}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
