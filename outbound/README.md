# outbound/

The outbound engine: which accounts to work first, whether the list closes the coverage gap, and the handoff to Amplemarket.

| File | What it does | Real or stub |
|---|---|---|
| [scoring.py](scoring.py) + [scoring_weights.yaml](scoring_weights.yaml) | Explainable account ranking with signal decay; suppresses customers and open opportunities | Real, offline. Weights are hypothesis: validate |
| [coverage.py](coverage.py) | Coverage for consumption revenue: ramp, realization and win rate turn pipeline into revenue a period can realize, as low / expected / high | Real, offline. Inputs are placeholders |
| [handoff.py](handoff.py) | Builds and validates Amplemarket rows; holds anything unapproved | Real builder, stub push |
| [amplemarket_handoff.md](amplemarket_handoff.md) | Spec and open questions | Spec |
| [fixtures/accounts.json](fixtures/accounts.json) | Synthetic accounts | Synthetic |

```bash
python -m outbound.run --dry-run
```

## Why consumption changes the coverage math

A usage contract signs before it earns. Counting signed value as pipeline overstates a period, because devices go live over months and not all of them reach expected usage. The model therefore reports three cases and a win-rate-weighted view, and says what it assumed. The honest check is [usage_realization](../knowledge/definitions/revenue-metrics.yaml): realized divided by expected, per cohort, once real data exists.

Signal names in the weights file must match `icp_hypotheses.trigger_signals` in [company.yaml](../company.yaml); `audit_company_alignment()` and a test enforce it.
