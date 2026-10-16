"""Account prioritization for outbound. Deterministic, explainable, offline.

Every score returns its reasons so a rep (or the hiring manager) can see why an account ranks where it does.
Suppressed accounts (customer, open opportunity, do-not-contact) never reach a list.
"""
from __future__ import annotations

import math
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from emnify_gtm.company import get, vertical_keys

WEIGHTS = Path(__file__).resolve().parent / "scoring_weights.yaml"


def load_weights(path: Path = WEIGHTS) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def suppression_reason(acct: Dict[str, Any]) -> Optional[str]:
    if acct.get("is_customer"):
        return "existing customer"
    if acct.get("has_open_opportunity"):
        return "open opportunity"
    if acct.get("do_not_contact"):
        return "do not contact"
    return None


def score_account(acct: Dict[str, Any], w: Optional[dict] = None) -> Dict[str, Any]:
    w = w or load_weights()
    reasons: List[str] = []
    why = suppression_reason(acct)
    if why:
        return {"id": acct.get("id"), "score": 0, "tier": "suppressed", "reasons": [f"suppressed: {why}"], "flags": []}
    score, flags = 0.0, []

    if acct.get("iot_vertical") in vertical_keys():
        score += w["fit"]["vertical_in_icp"]
        reasons.append(f"+{w['fit']['vertical_in_icp']} vertical {acct['iot_vertical']}")
    else:
        flags.append("no vertical match")

    emp = acct.get("employee_count")
    pts = w["fit"]["size_default_points"]
    for band in w["fit"]["size_bands"]:
        if emp is not None and emp >= band["min_employees"]:
            pts = band["points"]
            break
    score += pts
    reasons.append(f"+{pts} size ({emp if emp is not None else 'unknown'} employees)")

    region_pts = w["fit"]["region_points"].get(acct.get("region"), 0)
    if region_pts:
        score += region_pts
        reasons.append(f"+{region_pts} region {acct['region']}")

    for sig in acct.get("signals", []):
        spec = w["signals"].get(sig["kind"])
        if not spec:
            flags.append(f"unknown signal {sig['kind']}")
            continue
        pts = spec["points"] * 0.5 ** (sig["days_ago"] / spec["half_life_days"])
        score += pts
        reasons.append(f"+{pts:.1f} signal {sig['kind']} ({sig['days_ago']}d ago)")

    devices = acct.get("expected_device_count")
    if devices:
        p = w["potential"]
        pts = p["max_points"] * min(1.0, math.log10(devices) / math.log10(p["device_count_for_max"]))
        score += pts
        reasons.append(f"+{pts:.1f} potential ({devices} devices expected)")
    else:
        flags.append("expected_device_count unknown: potential not scored")

    score = round(min(score, 100.0), 1)   # capped so tiers stay comparable
    tier = next((t for t, floor in w["tiers"].items() if score >= floor), "D")
    return {"id": acct.get("id"), "score": score, "tier": tier, "reasons": reasons, "flags": flags}


def rank(accounts: List[Dict[str, Any]], w: Optional[dict] = None) -> List[Dict[str, Any]]:
    w = w or load_weights()
    scored = [dict(score_account(a, w), name=a.get("name")) for a in accounts]
    return sorted(scored, key=lambda s: (-s["score"], str(s["id"])))


def audit_company_alignment() -> List[str]:
    """Signals in the weights file must match company.yaml trigger_signals, so docs and code cannot drift."""
    w = load_weights()
    declared = set(get("icp_hypotheses.trigger_signals"))
    return sorted(declared ^ set(w["signals"]))
