"""Build the Amplemarket handoff list from ranked accounts. Validates every row against the data contract.

Rows without approval stay in `held`. Nothing is pushed: the Amplemarket client is a stub that needs credentials.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from integrations.contract_check import check, load_contract


def build_handoff(ranked: List[Dict[str, Any]], accounts: List[Dict[str, Any]], approved_by: Optional[str],
                  min_tier: str = "B", sequence_key: str = "hypothesis-validate") -> Dict[str, List[Dict[str, Any]]]:
    order = ["A", "B", "C", "D"]
    by_id = {a["id"]: a for a in accounts}
    contract = load_contract("amplemarket_handoff")
    ready, held = [], []
    for i, r in enumerate(ranked, start=1):
        if r["tier"] == "suppressed" or r["tier"] not in order or order.index(r["tier"]) > order.index(min_tier):
            continue
        a = by_id[r["id"]]
        row = {"sfdc_account_id": str(a["id"]), "contact_email": a.get("contact_email", ""), "priority_rank": i,
               "signal": (a["signals"][0]["kind"] if a.get("signals") else r["reasons"][0]).replace("_", " "),
               "sequence_key": sequence_key, "approved_by": approved_by or ""}
        errors = check(row, contract)
        (held if errors else ready).append({**row, "errors": errors} if errors else row)
    return {"ready": ready, "held": held}
