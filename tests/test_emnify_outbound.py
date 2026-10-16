import json

from outbound.coverage import accounts_to_work, coverage, ramp_factor, realized_in_period
from outbound.handoff import build_handoff
from outbound.run import FIX
from outbound.scoring import audit_company_alignment, rank, score_account

OPP = {"go_live_month": 2, "steady_monthly_revenue": {"low": 100, "expected": 200, "high": 300}}


def test_weights_match_company_signals():
    assert audit_company_alignment() == []


def test_suppression_and_ranking_order():
    accts = json.loads(FIX.read_text())
    ranked = rank(accts)
    assert ranked[0]["id"] == "S1" and ranked[0]["score"] <= 100
    s5 = next(r for r in ranked if r["id"] == "S5")
    assert s5["tier"] == "suppressed" and s5["score"] == 0


def test_signal_decays_and_unknown_devices_flagged():
    base = {"id": "x", "iot_vertical": "robotics", "employee_count": 100, "region": "US"}
    fresh = score_account({**base, "signals": [{"kind": "funding_round", "days_ago": 0}]})["score"]
    old = score_account({**base, "signals": [{"kind": "funding_round", "days_ago": 120}]})["score"]
    assert fresh > old
    assert any("expected_device_count" in f for f in score_account(base)["flags"])


def test_ramp_and_realization():
    assert ramp_factor(-1, 6) == 0 and ramp_factor(0, 6) == 1 / 6 and ramp_factor(10, 6) == 1.0
    # go-live month 2, 6-month ramp, 80% realization: months 2..11 ramp 1/6..1, steady 200
    expected = 200 * 0.8 * (1 / 6 + 2 / 6 + 3 / 6 + 4 / 6 + 5 / 6 + 1 + 1 + 1 + 1 + 1)
    assert abs(realized_in_period(OPP, 12) - round(expected, 2)) < 0.01


def test_coverage_cases_ordered_and_gap():
    cov = coverage([OPP], target=1000)
    assert cov["low"]["unweighted_realized"] < cov["expected"]["unweighted_realized"] < cov["high"]["unweighted_realized"]
    assert cov["assumptions"]["label"] == "hypothesis: validate"
    assert accounts_to_work(100, 0) is None and accounts_to_work(250, 100) == 250


def test_unapproved_rows_are_held():
    accts = json.loads(FIX.read_text())
    ranked = rank(accts)
    none_ok = build_handoff(ranked, accts, approved_by=None)
    assert none_ok["ready"] == [] and none_ok["held"]
    ok = build_handoff(ranked, accts, approved_by="reviewer-1")
    assert ok["ready"] and all(r["approved_by"] == "reviewer-1" for r in ok["ready"])


def test_sensitivity_monotonic():
    from outbound.run import OPPS
    from outbound.sensitivity import grid
    g = grid(OPPS)
    assert g[3][1.0] > g[6][1.0] > g[12][1.0]          # slower ramp realizes less
    assert g[6][0.6] < g[6][0.8] < g[6][1.0]           # lower realization realizes less


def test_scoring_regions_match_company_yaml():
    from emnify_gtm.company import get
    from outbound.scoring import load_weights
    assert sorted(load_weights()["fit"]["region_points"]) == sorted(get("regions"))
