---
type: crosswalk
category: revops
tags:
  - crosswalk
  - third-party-skills
  - governance
status: active
last_updated: 2026-10-13
---

# Swan GTM skills crosswalk

On 2026-10-13, 41 skills from [swan-gtm/gtm-skills](https://github.com/swan-gtm/gtm-skills) were installed and reviewed. The repo is MIT-licensed, © 2026 Swan, and was reviewed at commit `9491842`. All 41 installed folder hashes matched upstream.

Eighteen skills were folded into this toolkit. Every artifact below is written in our own words, with a source line. No swan text is pasted in. Deciding where each skill went is a governance call under decision log #18 (plugins and third-party skills follow the AI workflow standard).

**How the artifacts are typed:**
- **Contract:** an agent workflow with declared reads, writes, tools and stop rules (YAML plus a markdown companion).
- **Playbook:** a human procedure or framework.
- **Governance note:** rules that constrain data or agent behavior.

| Swan skill (source path, folder hash) | Module | Artifact | Toolkit file |
|---|---|---|---|
| lead-routing (`skills/rutger-katz/lead-routing`, `e08013addbd6`) | `gtm_engineer/lead_routing` | Contract | [lead-routing-contract](../contracts/lead-routing-contract.md) |
| governed-crm-cleanup (`skills/ryan-iyengar/governed-crm-cleanup`, `d5056c843f59`) | `shared_core/data_quality` | Contract | [crm-cleanup-contract](../contracts/crm-cleanup-contract.md) |
| hygiene-gated-outbound (`skills/ryan-iyengar/hygiene-gated-outbound`, `64a0446fac38`) | `gtm_engineer/marketing_ops` | Contract | [outbound-launch-readiness-contract](../contracts/outbound-launch-readiness-contract.md) |
| pipeline-visibility (`skills/rutger-katz/pipeline-visibility`, `293c3f83c215`) | `gtm_strategy_ops/pipeline_analytics` | Playbook | [Pipeline_Visibility_and_Hygiene](../playbooks/Pipeline_Visibility_and_Hygiene.md) |
| operating-cadence-designer (`skills/rutger-katz/operating-cadence-designer`, `544361d744b4`) | `gtm_strategy_ops/sales_leadership` | Playbook | [Revenue_Operating_Cadence](../playbooks/Revenue_Operating_Cadence.md) |
| revops-revenue-planning (`skills/rutger-katz/revops-revenue-planning`, `b87e938dce83`) | `gtm_strategy_ops/sales_planning` | Playbook | [Annual_Plan_Versioning_and_Reforecast](../playbooks/Annual_Plan_Versioning_and_Reforecast.md) |
| gtm-planning (`skills/rutger-katz/gtm-planning`, `10de29468b1d`) | `gtm_strategy_ops/sales_planning` | Playbook | [GTM_Motion_and_Org_Design](../playbooks/GTM_Motion_and_Org_Design.md) |
| build-and-fill-a-tam (`skills/ryan-iyengar/build-and-fill-a-tam`, `42f29f9684d4`) | `gtm_strategy_ops/sales_planning` | Playbook | [TAM_Build_and_Coverage](../playbooks/TAM_Build_and_Coverage.md) |
| tam-builder (`skills/tanyo-gochev/tam-builder`, `e8d225a67038`) | `gtm_strategy_ops/sales_planning` | Playbook (same file) | [TAM_Build_and_Coverage](../playbooks/TAM_Build_and_Coverage.md) |
| crm-health-scoring (`skills/ryan-iyengar/crm-health-scoring`, `4c0a977b4b74`) | `shared_core/data_quality` | Playbook | [CRM_Health_Scoring](../playbooks/CRM_Health_Scoring.md) |
| revops-data-governance (`skills/rutger-katz/revops-data-governance`, `74a8011f10db`) | `shared_core/data_quality` | Governance note | [field-and-agent-write-governance](../../shared_core/data_quality/field-and-agent-write-governance.md) |
| earned-autonomy (`skills/nadav-david/earned-autonomy`, `78af153fdf2c`) | `shared_core/ai_governance` | Governance note | [earned-autonomy](../../shared_core/ai_governance/earned-autonomy.md) |
| weekly-performance-advisor (`skills/erwann-lefevre/weekly-performance-advisor`, `41273a1d543f`) | `gtm_engineer/marketing_ops` | Playbook | [Outbound_Campaign_Review](../playbooks/Outbound_Campaign_Review.md) |
| campaign-benchmarking (`skills/tanyo-gochev/campaign-benchmarking`, `3ea33f9506c5`) | `gtm_engineer/marketing_ops` | Playbook (same file) | [Outbound_Campaign_Review](../playbooks/Outbound_Campaign_Review.md) |
| outbound-performance-diagnosis (`skills/tanyo-gochev/outbound-performance-diagnosis`, `fa8695a470bd`) | `gtm_engineer/marketing_ops` | Playbook (same file) | [Outbound_Campaign_Review](../playbooks/Outbound_Campaign_Review.md) |
| campaign-challenger (`skills/erwann-lefevre/campaign-challenger`, `348968bececd`) | `gtm_engineer/marketing_ops` | Playbook (same file) | [Outbound_Campaign_Review](../playbooks/Outbound_Campaign_Review.md) |
| revops-hubspot (`skills/rutger-katz/revops-hubspot`, `9b75dc31195e`) | `docs/specs/architecture` (HubSpot) | Playbook | [HubSpot_Lifecycle_and_Workflow_Recipes](../playbooks/HubSpot_Lifecycle_and_Workflow_Recipes.md) |
| revops-salesforce (`skills/rutger-katz/revops-salesforce`, `11438644bd08`) | `shared_core/data_model`, `docs/specs/salesforce` | Playbook | [Salesforce_Flow_and_Forecast_Config](../playbooks/Salesforce_Flow_and_Forecast_Config.md) |

## What was deliberately left out

- **Vendor and benchmark figures.** This covers Agentforce and Breeze pricing, quota-attainment stats, and Ebsta and Fullcast numbers. Under decision #17 they are not inputs here; they live in the GTM 2nd Brain benchmark register with confidence scores.
- **The `revops-revenue-planning` workbook script.** Its Capacity sheet formulas are malformed (unquoted VLOOKUP keys, wrong cell references), and five of its test checks can never fail. [`capacity_plan.py`](../../gtm_strategy_ops/sales_planning/capacity_plan.py) already covers the capacity math.
- **Silent data changes.** Two sources (pipeline-visibility and revops-salesforce) auto-push overdue close dates. Both playbooks replace that with a review task.

## Elsewhere

- **Global skills:** six swan skills were kept as global Claude skills, and eight were merged into them.
- **GTM 2nd Brain:** six went in as raw-source captures with wiki notes.
- **Dropped:** three. `list-architect` stays in `~/skills-quarantine`.

The full plan is in `~/Inbox/swan-skills-plan.md`.
