"""Pipeline coverage for consumption-based revenue.

A usage deal does not book its value at signature. Revenue ramps as devices come online, so contract-value coverage
overstates what a period will realize. This model converts each opportunity into the revenue it can realize inside the
target period, weights it by win rate, and reports coverage in those terms.

All defaults come from company.yaml `coverage_defaults` and are hypothesis: validate. Nothing here is an emnify figure.

Opportunity fields (the only inputs):
  steady_monthly_revenue: {low, expected, high}   revenue per month once all devices are live (a range, never one number)
  go_live_month:  months from period start until the first devices go live (0 = already live)
  win_probability: optional, overrides coverage_defaults.win_rate
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from emnify_gtm.company import get


def ramp_factor(months_since_go_live: int, ramp_months: int) -> float:
    """Linear ramp from first device to steady state; 0 before go-live."""
    if months_since_go_live < 0:
        return 0.0
    return min(1.0, (months_since_go_live + 1) / max(1, ramp_months))


def realized_in_period(opp: Dict[str, Any], period_months: int, case: str = "expected",
                       ramp_months: Optional[int] = None, realization: Optional[float] = None) -> float:
    ramp = int(ramp_months if ramp_months is not None else get("coverage_defaults.ramp_months_to_steady_usage"))
    real = float(realization if realization is not None else get("coverage_defaults.steady_state_usage_realization"))
    steady = float(opp["steady_monthly_revenue"][case])
    return round(sum(steady * real * ramp_factor(m - int(opp["go_live_month"]), ramp) for m in range(period_months)), 2)


def coverage(opps: List[Dict[str, Any]], target: float, period_months: int = 12, win_rate: Optional[float] = None) -> Dict[str, Any]:
    default_win = float(win_rate if win_rate is not None else get("coverage_defaults.win_rate"))
    out: Dict[str, Any] = {"assumptions": {"win_rate_default": default_win, "period_months": period_months,
                                           "ramp_months": get("coverage_defaults.ramp_months_to_steady_usage"),
                                           "usage_realization": get("coverage_defaults.steady_state_usage_realization"),
                                           "label": "hypothesis: validate"}}
    for case in ("low", "expected", "high"):
        raw = sum(realized_in_period(o, period_months, case) for o in opps)
        weighted = sum(realized_in_period(o, period_months, case) * float(o.get("win_probability", default_win)) for o in opps)
        out[case] = {"unweighted_realized": round(raw, 2), "weighted_realized": round(weighted, 2),
                     "coverage_ratio": round(raw / target, 2) if target else None,
                     "weighted_ratio": round(weighted / target, 2) if target else None}
    need = float(get("coverage_defaults.coverage_target_multiple"))
    out["target_multiple"] = need
    out["meets_target_multiple"] = (out["expected"]["coverage_ratio"] or 0) >= need
    out["gap_realized"] = round(max(0.0, need * target - out["expected"]["unweighted_realized"]), 2)
    return out


def accounts_to_work(gap: float, pipeline_per_100_accounts: float) -> Optional[int]:
    """How many more accounts must be worked to close a coverage gap. Needs a measured conversion rate; no default."""
    if pipeline_per_100_accounts <= 0:
        return None
    return int(-(-gap * 100 // pipeline_per_100_accounts))
