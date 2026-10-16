---
type: area
category: revops
tags:
  - area
  - enrichment
  - vendor-evaluation
  - data-quality
status: active
last_updated: 2026-10-07
---

# Vendor Benchmark Verification

## Executive Summary
Vendors publish benchmarks ("our agent beats the incumbents on list precision") that favour the vendor. This playbook turns any such claim into a test you can rerun on your own accounts in an afternoon, using [`gtm_engineer/enrichment/precision_audit.py`](../../gtm_engineer/enrichment/precision_audit.py).

## Six questions to ask before believing a benchmark
1. **Who ran it, and who paid?** Vendor, customer or independent party.
2. **What ICP was used?** A narrow ICP flatters a tool built for it. Is it yours?
3. **How was precision labeled?** Who judged a contact "correct", and were they blind to which tool produced it?
4. **How big was the sample?** See the interval table below.
5. **How were the other tools configured?** Defaults, or a tuned waterfall?
6. **Can you rerun it on your own list?**

## Why sample size matters
95% Wilson interval for a measured 80% precision:

| n | Interval |
|---|---|
| 25 | 61% to 91% |
| 50 | 67% to 89% |
| 100 | 71% to 87% |
| 250 | 75% to 84% |
| 500 | 76% to 83% |
| 1,000 | 77% to 82% |

This captures sampling error only. It cannot detect a biased sample, inconsistent labels or a cherry-picked ICP.

## Run the test
1. Pull ~100 accounts [ASSUME: enough to see a gap of roughly 15 points or more; smaller gaps need more] that you know well and that fit your ICP.
2. Run each tool on the same list. Use `blind_sheet()` to shuffle contacts and strip tool names; keep the key.
3. Have someone who knows your market label each contact correct / not correct.
4. Join labels back through the key into `account_id, tool, correct` rows and run:
   ```bash
   python -m gtm_engineer.enrichment.precision_audit labels.csv --a ToolA --b ToolB
   ```
5. Read the paired result. The exact test only looks at accounts where the two tools disagree, so it is more sensitive than comparing two separate intervals. Keep the labeled sheet and rerun when a vendor ships a new version.

`python -m gtm_engineer.enrichment.precision_audit --demo` runs on synthetic seeded data so you can see the report format without any real data.

## Decision rule
Pick on price, integration and support when precision is statistically indistinguishable. Pick on precision only when the gap holds on your ICP, with a blind labeler and a sample large enough that the intervals do not overlap.
