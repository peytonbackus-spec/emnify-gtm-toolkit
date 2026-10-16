"""Salesforce upsert client: STUB. Needs credentials to go live; dry-run works offline.

Live mode is intentionally not implemented here. When wiring it, use the Salesforce REST composite upsert on the
external id, one record per call first, and keep every write behind the human-review gate in company.yaml.
"""
from __future__ import annotations

import os
from typing import Any, Dict

REQUIRED_ENV = ("SFDC_INSTANCE_URL", "SFDC_ACCESS_TOKEN")   # names only; values live in the environment


class SalesforceClient:
    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        if not dry_run:
            missing = [v for v in REQUIRED_ENV if not os.environ.get(v)]
            if missing:
                raise RuntimeError(f"stub: live Salesforce writes need {', '.join(missing)}")

    def upsert(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not payload.get("upsert"):
            return {"status": "skipped", "reason": payload.get("reason")}
        if self.dry_run:
            return {"status": "dry_run", "would_upsert": payload["object"], "external_id": payload["external_id"],
                    "fields": payload["fields"]}
        raise NotImplementedError("stub: live upsert not implemented; see module docstring")
