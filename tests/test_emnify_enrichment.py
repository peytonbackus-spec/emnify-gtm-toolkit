import pytest

from enrichment.dedupe import find_clusters, norm_domain, norm_name
from enrichment.mapping import build_payload, coerce
from enrichment.sfdc_client import SalesforceClient
from enrichment.waterfall import check_predicate, classify_vertical, enrich, load_fixture_providers, load_rules
from enrichment.zoominfo_client import ZoomInfoProvider


def test_norm_domain_and_name():
    assert norm_domain("https://www.Example.com/path?q=1") == "example.com"
    assert norm_name("VoltGrid GmbH") == "voltgrid"


def test_dedupe_same_domain_picks_most_complete():
    recs = [{"id": "1", "name": "A", "domain": "a.example", "country": "DE"},
            {"id": "2", "name": "A", "domain": "http://www.a.example", "country": "DE", "employee_count": 5}]
    plan = find_clusters(recs)
    assert plan[0]["survivor_id"] == "2" and plan[0]["merge_ids"] == ["1"]
    assert plan[0]["action"] == "propose_merge_for_human_approval"


def test_dedupe_does_not_merge_different_country_or_generic_domain():
    recs = [{"id": "1", "name": "Acme Robotics", "domain": "gmail.com", "country": "DE"},
            {"id": "2", "name": "Acme Robotics", "domain": "gmail.com", "country": "US"}]
    assert find_clusters(recs) == []


def test_predicates():
    assert check_predicate({"field": "n", "op": "gte", "value": 20}, {"n": 25})
    assert not check_predicate({"field": "n", "op": "gte", "value": 20}, {})
    assert check_predicate({"field": "n", "op": "absent"}, {})
    with pytest.raises(ValueError):
        check_predicate({"field": "n", "op": "nope"}, {"n": 1})


def test_classify_vertical_no_guess():
    kws = load_rules()["vertical_keywords"]
    assert classify_vertical("EV charging station operator", kws) == "ev_charging"
    assert classify_vertical("Artisan bakery", kws) is None


def test_waterfall_low_confidence_falls_through_and_budget_caps():
    providers = load_fixture_providers()
    res = enrich({"domain": "fleetloop.example"}, providers)
    assert res.record["employee_count"] == 75 and res.provenance["employee_count"] == "clay_native"
    capped = enrich({"domain": "fleetloop.example"}, providers, budget=0)
    assert capped.credits_spent == 0 and "employee_count" not in capped.record


def test_contact_credits_only_after_fit_gate():
    res = enrich({"domain": "bakery.example"}, load_fixture_providers())
    assert "iot_vertical" not in res.record and "decision_maker_email" not in res.record


def test_mapping_policies():
    enriched = {"domain": "x.example", "employee_count": "40", "industry": "Energy", "hq_country": "de",
                "iot_vertical": "ev_charging", "company_description": "text"}
    p = build_payload(enriched, crm_current={"Industry": "Utilities"})
    assert p["fields"]["NumberOfEmployees"] == 40 and p["fields"]["BillingCountryCode"] == "DE"
    assert "Industry" not in p["fields"]          # fill_if_empty respected
    assert "Description" not in p["fields"]       # write_policy never
    assert build_payload({"employee_count": 1})["upsert"] is False


def test_mapping_rejects_unknown_vertical():
    with pytest.raises(ValueError):
        coerce("submarines", "enum")


def test_stubs_need_credentials(monkeypatch):
    for v in ("SFDC_INSTANCE_URL", "SFDC_ACCESS_TOKEN", "ZOOMINFO_USERNAME", "ZOOMINFO_CLIENT_ID", "ZOOMINFO_PRIVATE_KEY"):
        monkeypatch.delenv(v, raising=False)
    with pytest.raises(RuntimeError):
        SalesforceClient(dry_run=False)
    with pytest.raises(RuntimeError):
        ZoomInfoProvider()
    out = SalesforceClient().upsert({"upsert": True, "object": "Account", "external_id": {"k": "v"}, "fields": {}})
    assert out["status"] == "dry_run"
