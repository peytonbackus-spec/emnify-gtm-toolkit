"""Offline outbound demo: score, hand off (dry), and show coverage.   python -m outbound.run --dry-run"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from outbound.coverage import accounts_to_work, coverage
from outbound.handoff import build_handoff
from outbound.scoring import audit_company_alignment, rank

FIX = Path(__file__).resolve().parent / "fixtures" / "accounts.json"
# Synthetic opportunities in abstract revenue units, to show the arithmetic. Not emnify figures.
OPPS = [{"id": "O1", "go_live_month": 2, "steady_monthly_revenue": {"low": 600, "expected": 1000, "high": 1400}},
        {"id": "O2", "go_live_month": 5, "steady_monthly_revenue": {"low": 300, "expected": 800, "high": 1500}, "win_probability": 0.3}]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", default=True, help="always on; the Amplemarket push is a stub")
    ap.parse_args()
    accounts = json.loads(FIX.read_text())
    drift = audit_company_alignment()
    print("signal/company.yaml drift:", drift or "none")
    ranked = rank(accounts)
    print("== ranking ==")
    for r in ranked:
        print(f"{r['tier']:>10} {r['score']:>5}  {r['name']}  flags={r['flags']}")
    print("== handoff (no approval given, so everything is held) ==")
    print(json.dumps({k: len(v) for k, v in build_handoff(ranked, accounts, approved_by=None).items()}))
    print("== coverage (synthetic units) ==")
    cov = coverage(OPPS, target=10000)
    print(json.dumps(cov, indent=2))
    print("accounts to work to close the gap, at an assumed 2000 units of pipeline per 100 accounts:",
          accounts_to_work(cov["gap_realized"], 2000))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
