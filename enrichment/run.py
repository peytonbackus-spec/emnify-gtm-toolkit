"""Run the enrichment demo end to end on synthetic accounts, offline.

    python -m enrichment.run --dry-run
"""
from __future__ import annotations

import argparse
import json

from enrichment.dedupe import find_clusters
from enrichment.mapping import build_payload
from enrichment.sfdc_client import SalesforceClient
from enrichment.waterfall import enrich, load_fixture_providers

ACCOUNTS = [
    {"id": "A1", "name": "VoltGrid GmbH", "domain": "voltgrid.example", "country": "DE", "created_date": "2025-01-10"},
    {"id": "A2", "name": "Voltgrid", "domain": "https://www.voltgrid.example/", "country": "DE", "created_date": "2025-06-01", "employee_count": 180},
    {"id": "A3", "name": "FleetLoop BV", "domain": "fleetloop.example", "country": "NL", "created_date": "2025-03-02"},
    {"id": "A4", "name": "PetPaw Inc", "domain": "petpaw.example", "country": "US", "created_date": "2025-04-04"},
    {"id": "A5", "name": "Corner Bakery SAS", "domain": "bakery.example", "country": "FR", "created_date": "2025-05-05"},
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", default=True, help="always on in this build; live mode is a stub")
    ap.parse_args()
    print("== dedupe plan ==")
    print(json.dumps(find_clusters(ACCOUNTS), indent=2))
    providers = load_fixture_providers()
    sfdc = SalesforceClient(dry_run=True)
    print("== enrich + map + dry-run upsert ==")
    for acct in ACCOUNTS:
        res = enrich(acct, providers)
        payload = build_payload(res.record)
        print(json.dumps({"id": acct["id"], "credits": res.credits_spent, "vertical": res.record.get("iot_vertical"),
                          "result": sfdc.upsert(payload)}, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
