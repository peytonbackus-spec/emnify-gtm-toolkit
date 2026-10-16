# Sample runs

Captured output of the offline demos on synthetic data: fictional companies, placeholder weights, abstract revenue units. Nothing here is emnify data or a result. Regenerate with `python scripts/capture_examples.py`.

## Enrichment: dedupe plan, waterfall, mapping, dry-run upsert

```text
$ python -m enrichment.run --dry-run
== dedupe plan ==
[
  {
    "survivor_id": "A2",
    "merge_ids": [
      "A1"
    ],
    "reasons": [
      "same domain"
    ],
    "action": "propose_merge_for_human_approval"
  }
]
== enrich + map + dry-run upsert ==
{"id": "A1", "credits": 5, "vertical": "ev_charging", "result": {"status": "dry_run", "would_upsert": "Account", "external_id": {"Website_Domain__c": "voltgrid.example"}, "fields": {"NumberOfEmployees": 180, "Industry": "Energy", "BillingCountryCode": "DE", "IoT_Vertical__c": "ev_charging"}}}
{"id": "A2", "credits": 4, "vertical": "ev_charging", "result": {"status": "dry_run", "would_upsert": "Account", "external_id": {"Website_Domain__c": "voltgrid.example"}, "fields": {"NumberOfEmployees": 180, "Industry": "Energy", "BillingCountryCode": "DE", "IoT_Vertical__c": "ev_charging"}}}
{"id": "A3", "credits": 8, "vertical": "fleet_management", "result": {"status": "dry_run", "would_upsert": "Account", "external_id": {"Website_Domain__c": "fleetloop.example"}, "fields": {"NumberOfEmployees": 75, "Industry": "Transportation", "BillingCountryCode": "NL", "IoT_Vertical__c": "fleet_management"}}}
{"id": "A4", "credits": 3, "vertical": "pet_tracking", "result": {"status": "dry_run", "would_upsert": "Account", "external_id": {"Website_Domain__c": "petpaw.example"}, "fields": {"NumberOfEmployees": 12, "Industry": "Consumer Goods", "BillingCountryCode": "US", "IoT_Vertical__c": "pet_tracking"}}}
{"id": "A5", "credits": 5, "vertical": null, "result": {"status": "dry_run", "would_upsert": "Account", "external_id": {"Website_Domain__c": "bakery.example"}, "fields": {"NumberOfEmployees": 30, "BillingCountryCode": "FR"}}}
```

## Outbound: ranking, held handoff, coverage low / expected / high

```text
$ python -m outbound.run --dry-run
signal/company.yaml drift: none
== ranking ==
         A 100.0  VoltGrid (synthetic)  flags=[]
         A  81.1  FleetLoop (synthetic)  flags=['expected_device_count unknown: potential not scored']
         B  52.0  PetPaw (synthetic)  flags=['expected_device_count unknown: potential not scored']
         D  18.0  Corner Bakery (synthetic)  flags=['no vertical match', 'expected_device_count unknown: potential not scored']
suppressed     0  RoboHaul (synthetic)  flags=[]
== handoff (no approval given, so everything is held) ==
{"ready": 0, "held": 3}
== coverage (synthetic units) ==
{
  "assumptions": {
    "win_rate_default": 0.15,
    "period_months": 12,
    "ramp_months": 6,
    "usage_realization": 0.8,
    "label": "hypothesis: validate"
  },
  "low": {
    "unweighted_realized": 4680.0,
    "weighted_realized": 864.0,
    "coverage_ratio": 0.47,
    "weighted_ratio": 0.09
  },
  "expected": {
    "unweighted_realized": 8880.0,
    "weighted_realized": 1764.0,
    "coverage_ratio": 0.89,
    "weighted_ratio": 0.18
  },
  "high": {
    "unweighted_realized": 13800.0,
    "weighted_realized": 2880.0,
    "coverage_ratio": 1.38,
    "weighted_ratio": 0.29
  },
  "target_multiple": 3.0,
  "meets_target_multiple": false,
  "gap_realized": 21120.0
}
accounts to work to close the gap, at an assumed 2000 units of pipeline per 100 accounts: 1056
```

## Coverage sensitivity to ramp length and realization

```text
$ python -m outbound.sensitivity
Expected realized revenue as a share of 'signed value from go-live' (12-month period, synthetic opportunities)
ramp months | realization 60% | realization 80% | realization 100%
          3 |             53% |             71% |             88%
          6 |             43% |             57% |             71%
          9 |             33% |             44% |             54%
         12 |             25% |             33% |             41%
Read: a slow ramp or low realization can cut what a period realizes by a third or more versus counting signed value.
```

## Agent eval suites

```text
$ python -m agents.run_evals
research_brief: 4/4 (100.0%)
qualification_signal: 3/3 (100.0%)
personalization: 2/2 (100.0%)
```

## Knowledge router lookup

```text
$ python -m knowledge.tools lookup "launch outbound list"
- id: contract-outbound-launch
  path: knowledge/process/outbound-launch.yaml
  status: 'hypothesis: validate'
  confidence_score: '0.5'
```
