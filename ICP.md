# ICP hypotheses

Everything here is **hypothesis: validate**. Verticals come from emnify's public website; ordering, personas and triggers are working guesses. There is no emnify win or loss data behind any of it. The first job of the role is to replace this page with evidence.

<!-- BEGIN company:role -->
emnify GTM Engineer (Senior (IC4), Sales Operations), reports to the Revenue Operations Lead, works with the CRO. Job 5004134101, posted 2026-10-13.
<!-- END company:role -->

## Verticals

<!-- BEGIN company:verticals -->
| Vertical | Usage shape | Source | Tier |
|---|---|---|---|
| Fleet management and telematics | many devices, steady low data per device | public | hypothesis: validate |
| EV charging | many sites, steady low-to-medium data | public | hypothesis: validate |
| Airlines and aviation equipment | fewer devices, global roaming | public | hypothesis: validate |
| Smart building and energy | many devices, small payloads | public | hypothesis: validate |
| Point of sale and payment terminals | many devices, bursty low data | public | hypothesis: validate |
| Pet and asset tracking | high volume consumer devices, tiny payloads | public | hypothesis: validate |
| Robotics | fewer devices, higher data | public | hypothesis: validate |
<!-- END company:verticals -->

No vertical is ranked above another. [Scoring](outbound/scoring_weights.yaml) gives them equal fit points until win data exists. The "usage shape" column is a reasoning aid: it says what drives revenue in each case (many devices with small payloads versus fewer devices with more data), which is what a consumption forecast depends on.

## Buyer personas

<!-- BEGIN company:personas -->
- IoT product owner / head of connected products
- Head of hardware or embedded engineering
- Head of fleet, field or device operations
- Procurement / vendor management
<!-- END company:personas -->

## Trigger signals to test

Each is a bet that the signal precedes a connectivity decision. The test is whether signal-triggered accounts create more pipeline per 100 accounts worked than list-based ones.

| Signal | Where it could come from |
|---|---|
| New connected product launch | News, product pages, Sales Navigator |
| Hiring embedded or IoT engineers | Careers pages (verify at the company's own source before using it) |
| Funding round | News, Sales Navigator |
| Expansion into new countries | News, product pages |
| Connectivity provider contract window | Only discoverable in conversation or from partners |

## Qualification fields for consumption deals

A usage-based opportunity needs more than a contract amount. These are the fields to capture ([contract](knowledge/process/consumption-qualification.yaml)):

<!-- BEGIN company:qualification -->
- `expected_device_count`
- `expected_monthly_data_per_device_mb`
- `countries_of_deployment`
- `deployment_timeline_months`
- `current_connectivity_provider`
<!-- END company:qualification -->

## Anti-ICP (hypothesis: validate)

- Consumer-only products with no connected hardware.
- Accounts whose product has no cellular need (Wi-Fi-only devices).
- Existing customers and accounts with an open opportunity (suppressed in scoring).

## How this page gets validated

1. Pull closed-won and closed-lost for the last four quarters and label each by vertical, devices, countries and time to go-live.
2. Compare win rate and realized usage by vertical. Rank only where the sample is large enough to say so.
3. Re-weight [scoring](outbound/scoring_weights.yaml), update [company.yaml](company.yaml), run `python scripts/render_company_docs.py`.
