---
id: contract-outbound-launch-readiness
type: contract-index
tags: [contract, workflow-contract, outbound, data-quality]
last_modified: 2026-10-13
---

# Outbound Launch Readiness Agent -- Workflow Contract

Companion note for [`outbound-launch-readiness-contract.yaml`](outbound-launch-readiness-contract.yaml).

**Objective:** before a CRM-derived audience enters any sequence, decide GO, CONDITIONAL GO or STOP on the exact launch slice, then rebuild the audience from source filters. It's a gate, not a sender.

**Role map:**
1. `slice_agent`: fixes the exact audience and its baseline counts.
2. `gate_agent`: runs the identity, ownership, reachability, context and fit gates.
3. `remediation_agent`: bounded fixes, through the [CRM cleanup contract](crm-cleanup-contract.md).
4. `rebuild_agent`: regenerates the audience, re-runs the gates and samples 10+ records.

**Where it sits in the send path:**
1. Audience built from [`scored_leads.csv`](../../outputs/scored_leads.csv) or a CRM list.
2. **This gate.**
3. The [CASL compliance gate](casl-compliance-gate-contract.md).
4. The sequencer.

Readiness and consent are separate questions; passing one never implies the other.

**Worked example (from the source):**
- **The audience:** 2,400 contacts, with 74 ownerless, 39 unresolved account duplicates, and 22 on open opportunities.
- **Fixes:**
  - The 22 open-opportunity contacts were suppressed, and their signal went to the deal owners.
  - The duplicates were resolved before any contact edits.
  - 61 ownerless contacts were routed by territory, and the 13 ambiguous ones were excluded.
- **Result:** after rebuilding from source, a clean subset of 2,353 got a CONDITIONAL GO. 47 records are excluded with reasons, and an older export is never appended to bring them back.

**Measurement note:** compare response quality by readiness defect as well as by message variant. Bad data can pass for bad copy.

_Source: adapted in our own words from swan-gtm/gtm-skills `skills/ryan-iyengar/hygiene-gated-outbound` (MIT, © 2026 Swan). See the [crosswalk](../crosswalks/swan-gtm-skills.md)._

## See Also
[casl-compliance-gate-contract](casl-compliance-gate-contract.md) . [crm-cleanup-contract](crm-cleanup-contract.md) . [Outbound_Campaign_Review](../playbooks/Outbound_Campaign_Review.md)
