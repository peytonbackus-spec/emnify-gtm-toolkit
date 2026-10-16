# Walkthrough: one account, signal to Salesforce

A talk track for "walk us through a flow". It follows a single synthetic account through the repo, in about ten minutes. Every emnify detail is hypothesis: validate, and I would start by asking how close this is to what already exists.

## 0. Frame (30 seconds)
Revenue is usage-based, so the question is not "is this a lead" but "is this account likely to put many devices online, soon, in places we serve". Everything below is built to answer that, cheaply, with a person approving anything that changes a record or reaches a prospect.

## 1. Input and dedupe
A domain arrives from a list or a signal. It is normalized (lowercase, no scheme, no `www`) and checked against existing accounts. Two records with one domain become a **merge plan**, with the most complete record as survivor. Nobody merges automatically. See [`dedupe.py`](../enrichment/dedupe.py).

## 2. The Clay table
Columns run in a deliberate order: description first (cheap), then a **vertical classification** that acts as a fit gate, then the paid fields, then contacts only for accounts that passed. See the column table in [`clay_table_spec.md`](../enrichment/clay_table_spec.md). I have not run this in a real workspace; I would rebuild it in the live one in an afternoon.

## 3. The waterfall
Each field has ordered providers. A value below the confidence floor counts as a miss and the next provider runs. A credit cap stops runaway spend. Every step, including skips and the reason, lands in a trace. See [`waterfall_rules.yaml`](../enrichment/waterfall_rules.yaml) and the run in the [sample runs](examples/emnify-sample-runs.md).

## 4. Mapping and write policy
Enrichment output meets the mapping contract: required key present, values coerced and validated, and a per-field policy (`fill_if_empty`, `overwrite_if_better`, `never`). The output is a payload plus a reason for every field written or skipped. See [`field_mapping.yaml`](../enrichment/field_mapping.yaml).

## 5. Prioritize
The enriched account is scored on vertical, size, region, decayed signals and expected devices, with reasons shown and unknowns flagged. Customers and open opportunities are suppressed. See [`scoring.py`](../outbound/scoring.py).

## 6. Coverage
The list is judged by revenue it can **realize in the period**, as low, expected and high, not by signed value. The [sensitivity table](examples/emnify-sample-runs.md) shows why: ramp length and realization move the answer by a lot, and neither is measured yet.

## 7. Agents propose
A research brief cites evidence and lists unknowns. A call summary produces **proposed** device count and countries with quotes. A draft email exists only if there is a signal. Text inside a summary that tries to give instructions is ignored and flagged. See [`agents/`](../agents/README.md).

## 8. Human gate, then n8n
Sends, CRM writes and disqualification go to a person. Approved items pass the data contract in n8n, which defaults to dry-run. Failures retry only if transient, and land in a dead-letter list. See [`integrations/`](../integrations/README.md).

## 9. What I would do first
Weeks 1-4 in [`ROADMAP.md`](../ROADMAP.md): learn what exists, agree the metric and write permissions, measure enrichment precision, then ship one small dry-run-first run.

## Likely pushback, and my answer
| Question | Answer |
|---|---|
| "Why not just buy another data vendor?" | Measure precision per provider first; see [DECISIONS](../DECISIONS.md). |
| "Why so many gates?" | Autonomy is earned per task with evidence. The gate moves to spot-check where the audit supports it. |
| "Is any of this proven?" | The mechanics run on synthetic data. The impact on emnify is untested. The results I cite are from a previous role and do not carry over automatically. |
