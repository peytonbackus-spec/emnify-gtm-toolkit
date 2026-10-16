# Outbound and Coverage

Folder: `outbound/`.

## Scoring
Explainable ranking: vertical fit, size, region, decayed signals, and expected devices on a log scale. Every score lists its reasons and flags what is unknown. Customers, open opportunities and do-not-contact accounts are suppressed. Weights are hypothesis: validate; verticals get equal points until win data ranks them.

## Coverage for usage revenue
A usage deal signs before it earns. Each opportunity is converted into the revenue it can realize inside the period:

- steady monthly revenue as a **low / expected / high** range
- a linear ramp from go-live to steady state
- a usage realization factor
- win rate (a placeholder, labelled)

The output prints its assumptions and the gap to the target multiple. The honest check later is **usage realization**: realized divided by expected, per cohort.

## Handoff
Rows for Amplemarket are validated against a data contract. No approver, or any contract error, means the row is held.
