# Enrichment

Folder: `enrichment/`. Takes domains to Salesforce-ready account records.

1. **Dedupe** by normalized domain, then conservative name-plus-country matching. Output is a merge plan for a human, never a merge.
2. **Waterfall** per field: ordered providers, structured `when` conditions, a minimum confidence, a credit budget, and a full trace of every step taken or skipped.
3. **Fit gate**: a vertical is classified from the description. No vertical, no paid contact credits.
4. **Mapping contract**: each field has a write policy (`fill_if_empty`, `overwrite_if_better`, `never`). Values are validated and coerced before they reach a payload.
5. **Upsert**: dry-run by default; the live client is a stub.

The Clay flow is specified column by column in `clay_table_spec.md`. No Clay workspace was opened. Provider order, thresholds and costs are hypothesis: validate. Measure fill rate, credits per correct field and wrong-vertical rate before trusting any of them.
