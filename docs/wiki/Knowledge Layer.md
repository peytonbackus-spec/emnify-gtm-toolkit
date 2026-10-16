# Knowledge Layer

Folder: `knowledge/`. Process knowledge written so people and agents read the same source. The pattern is adapted from governance I already run in a personal vault.

- One schema: `id`, `type`, `tags`, `status`, `last_modified`, `confidence_score`.
- Workflow contracts declare purpose, steps, human gate, kill switch and metrics before anything automated runs.
- A router maps a plain-language request to the right contract. No match is logged as a gap.
- Agents read and propose into `proposals/`; a person merges.
- A validator fails on missing fields, duplicate ids, stale documents and contracts with no human-in-the-loop block.

Today every document is `hypothesis: validate`, and lookups report that along with the answer.
