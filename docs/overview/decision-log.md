# Decision Log

Design choices, and the reasoning behind each, so they can be defended or changed on purpose.

| # | Decision | Why | Alternative considered |
|---|---|---|---|
| 1 | **Split the repo at lead conversion** (🟦 / 🟩 / 🟪) | It's where the two roles actually divide, and it matches CRM object ownership | One combined toolkit: hides which work supports which role |
| 2 | **Shared core built once** | The roles overlap heavily; duplicating would let definitions drift | Copy into each track |
| 3 | **Two-axis lead score (fit × intent)** | Blended scores hide opposite cases (quiet ideal buyer vs noisy non-buyer) | Single 0–100 score |
| 4 | **Routing as an ordered rule list with a reason stamped on every lead** | The order is the policy; "why did this go to X?" is answerable from the record | Assignment rules without audit trail |
| 5 | **Rules decide deal risk; AI only explains** | Explainable, testable, and nobody has to trust a black box with the forecast | Model-scored risk |
| 6 | **Every revenue-affecting AI action goes to human review** | Forecast categories and disqualifications are too costly to get wrong silently | Confidence-only auto-apply |
| 7 | **Deny-by-default PII guard** | Prospect and customer data is sensitive; instructions in a prompt are not a control | Prompt-level instructions only |
| 8 | **Technical validation and security review as their own stage gates** | They're the long poles in long-cycle enterprise deals (configurable) | Generic 5-stage model |
| 9 | **Renewals forecast separately** | A large renewal shouldn't mask a new-business miss | One blended forecast |
| 10 | **Product-line and partner views from the warehouse, not forecasting-tool roll-ups** | Roll-up tools follow the CRM role hierarchy only | Restructure the role hierarchy (breaks record access) |
| 11 | **No CRM formula fields as forecasting-tool inputs; flow-stamped fields instead** | Many tools can't consume formula fields | Duplicate logic in the tool |
| 12 | **Mock LLM by default, live mode opt-in** | Runs and tests anywhere with no key and no data leaving the machine | Live-only |
| 13 | **Synthetic, seeded data with planted patterns** | Reproducible demos with real findings (mis-weighted segment, regional forecast bias) | Random data with no signal |
| 14 | **Python + SQL return identical numbers (tested)** | One definition per metric across both roles | Separate reporting stacks |
| 15 | **All company specifics in one YAML config, resolved by `make new`** | A new company repo is a config change, not a code fork | Per-company code branches |
| 16 | **Private material split out into a separate private repo** | The template can be public and shared safely | One repo with a gitignore |
| 17 | **Vendor benchmark claims are re-tested on our own accounts, blind, with an interval** | A vendor's number depends on its ICP, labeling and sample size; a 100-account blind test is cheap and answers the question we actually have | Trusting published benchmarks |
| 18 | **Plugins, mods and sub-agent effort follow the AI workflow standard** | They change agent behavior or cost; effort never replaces the HITL gate | Case-by-case approval with no written scope or stop rule |
| 19 | **Leadership reporting has two depths from one set of numbers (snapshot, full)** | Leaders differ on how much they want; a snapshot that can be expanded keeps one definition and ends "whose number is right" | Separate dashboards per audience |
| 20 | **Capacity from ramped rep equivalents × steady-state productivity, then quota above it by a stated over-assignment** | Quota is a target, productivity is what reps sell; planning on quota hides under-capacity | Headcount × quota |
| 21 | **One request queue for CRM and marketing-automation changes, with change classes and SLAs** | A CRM field change can break a sync nobody told Marketing Ops about; one door shows the collision before release | Separate queues per team |
| 22 | **Autonomy is earned per task from a logged record, and never lifts decision #6** ([earned autonomy](../../shared_core/ai_governance/earned-autonomy.md)) | Low-impact tasks can get faster with evidence, while revenue-affecting actions stay reviewed; automatic demotion keeps the ladder honest | A single confidence threshold for every action, or review of everything forever |
| 23 | **Third-party skill content is ported as our own contracts, playbooks and governance notes, with attribution, never pasted in** ([swan crosswalk](../crosswalks/swan-gtm-skills.md)) | Keeps one voice and one definition per concept, keeps unverified vendor numbers out (#17), and keeps the template publishable (#16) | Installing third-party skills globally and treating them as the toolkit's source of truth |
| 24 | **AI actions fail closed, and every agent's stop rule names a notification owner and a time limit** ([AI Workflow Standard](../../shared_core/ai_governance/README.md)) | A failed check that lets an action through is the costly failure, and a slow notification is a failure of its own; both are cheaper to settle before an incident | Letting an action proceed when a check cannot run; deciding who tells whom after something goes wrong |
