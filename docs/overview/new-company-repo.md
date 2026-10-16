# Creating a repo for a new company

1. `make new COMPANY="Acme Corp" FY_START=1` (or `python scripts/new_company.py ...`). Use `--git` to `git init`; nothing is committed or pushed for you.
2. In the new repo, edit `config/company.yaml`: segments, personas, stack, partners, stages, quota. Tag each value `[PUBLIC]`, `[POSTING]` or `[ASSUME]`.
3. If you renamed segment or persona keys, update the lookup tables at the top of `scripts/generate_sample_data.py`, then `make data`.
4. `make demo test`. Read the scoring calibration output before trusting weights.
5. Rewrite specs where the company's process differs.

Alternative: mark this repo as a GitHub template ("Use this template"), then run the scaffold in the copy.

The scaffold excludes `private-vault/`, `.backup/`, outputs and caches, and removes itself and the example config from the new repo.
