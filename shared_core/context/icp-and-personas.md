# ICP, Segments & Buying Committee

![Shared](https://img.shields.io/badge/supports-BOTH%20roles-7B61FF)

Both roles need one segment model that every system shares: the GTM Engineer to operationalize ICP segmentation and target-account strategy, Strategy & Ops to cut views by region, product, source and owner. This is that model. The machine-readable copy is in the company config (`segments`, `personas`) and is the one the code reads. Keep this page and the config in step.

> **Status:** the values below are the shipped *example*. Replace them with the company's real segments. Treat them as working hypotheses until validated against closed-won data in the first 30 days (see the [scoring calibration](../../gtm_engineer/lead_scoring/calibrate_scoring.py) approach). Provenance tags: `[PUBLIC]`, `[POSTING]`, `[ASSUME]`.

## Segments

| Segment key | Definition | Fit points | Primary motion |
|---|---|---|---|
| `enterprise` | Largest accounts (5,000+ employees) | 30 | Enterprise ABM, multi-threaded |
| `upper_mid_market` | 1,500–5,000 employees | 28 | Enterprise ABM |
| `vertical_a` | High-velocity vertical A | 26 | Velocity (inbound + SDR) |
| `vertical_c` | High-velocity vertical C | 22 | Velocity |
| `vertical_b` | High-velocity vertical B | 20 | Velocity |
| `mid_market` | 50–1,500 employees | 18 | Partner-led |
| `small_business` | Under 50 employees | 18 | Partner-led |
| `adjacent` | Adjacent regulated industries | 12 | Partner-led |
| `other` | Non-ICP | 0 | Nurture or disqualify |

## Anti-ICP (disqualify or nurture)

- No use case for the product (define the specific missing capability or workflow).
- Too small to fund an implementation and outside a partner channel (set the employee floor in config).
- Researchers, students, job seekers and vendors (a common source of inbound noise).
- An open opportunity already exists on the account. Route it to the owner; don't create a new lead.

## Buying committee

| Persona key | Typical titles | Role in deal | What they care about |
|---|---|---|---|
| `exec_buyer_primary` | VP / Head of the primary function | Economic buyer | Cost and performance trade-off at scale |
| `exec_buyer_security` | CISO, Director IT Security | Economic buyer | Risk reduction, vendor security posture |
| `exec_buyer_digital` | SVP Digital, Head of Channels | Economic buyer | Customer experience gains without added risk |
| `exec_buyer_ops` | Head of Operations | Economic buyer | Efficiency without added customer friction |
| `champion_product` | VP Product, Platform | Champion | Time-to-value, integration effort |
| `influencer_risk` | CRO, Compliance | Influencer / veto | Defensible audit trail |
| `champion_practitioner` | Manager, Analyst | Champion / user | Day-to-day workload, explainable results |
| `blocker_procurement` | Vendor Risk, Architecture | Blocker / gate | Security review, data residency, integration effort |

**Why it matters for Strategy & Ops:** stage 3+ deals without an economic buyer engaged are flagged by both the [data-quality monitor](../data_quality/dq_monitor.py) (rule O06) and the [deal-risk model](../../gtm_strategy_ops/ai_deal_risk/deal_risk.py).

**Why it matters for the GTM Engineer:** persona points feed the fit axis of the [lead score](../../gtm_engineer/lead_scoring/score_leads.py). Persona is derived from title with the title-normaliser described in the [enrichment waterfall spec](../../gtm_engineer/platform_admin/enrichment-waterfall.md).
