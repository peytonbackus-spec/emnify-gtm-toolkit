# Running the Toolkit

```bash
pip install -r requirements.txt
python -m enrichment.run --dry-run
python -m outbound.run --dry-run
python -m agents.run_evals
python -m knowledge.tools validate
python -m knowledge.tools lookup "launch outbound list"
python scripts/render_company_docs.py --check
python -m pytest
make data demo    # inherited template engines on synthetic data
```

Python 3.9 or newer. No API keys are needed; credentials are never required for anything in the repo. Environment variable names for future live use are in `.env.example`.
