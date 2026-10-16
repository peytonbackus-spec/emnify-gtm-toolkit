# emnify-gtm-toolkit

Public GitHub repo (peytonbackus-spec/emnify-gtm-toolkit). See README.md for purpose and layout.

## Rules
- Public repo: never commit secrets, API keys, prospect or employer data, or anything under a `_private/` folder.
- Never commit or push unless I ask for it in that message. Use `git --no-pager`.
- Every emnify assumption is labelled "hypothesis: validate". No invented metrics; the only results quoted are the four confirmed ones in company.yaml `proof_points`.
- Edit values in company.yaml, then run `python scripts/render_company_docs.py`; do not hand-edit generated blocks.
- Run `python -m pytest` and `ruff check` before proposing a change as done.
- Python venvs (`.venv/`) and `outputs/` are local and ignored; BUILD_STATUS.md is a local build log and is ignored.
