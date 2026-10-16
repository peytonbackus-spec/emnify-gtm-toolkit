#!/usr/bin/env python3
"""Create a new company-specific toolkit repo from this template.

    python scripts/new_company.py "Acme Corp"
    python scripts/new_company.py "Acme Corp" --dest ~/work/acme-gtm --fy-start-month 1 --git
    make new COMPANY="Acme Corp"

What it does:
  1. Copies the template (code, specs, tests, sample data) to a new directory.
     Private material (private-vault/, .backup/, outputs/, caches, .git) is never copied.
  2. Writes config/company.yaml from config/example.yaml with the company name, fiscal
     calendar and variables filled in. The example file is not copied into the new repo's
     config/ so there is exactly one config to edit.
  3. Resolves the [VARIABLE] tokens in docs and prompts from that config
     (e.g. [COMPANY_NAME], [FORECAST_TOOL]). Tokens with no value are left in place and listed.
  4. Writes VARIABLES.md (every variable and its provenance) and a short README with next steps.

It never modifies the template and never pushes anything.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = {".git", "private-vault", ".backup", "outputs", "__pycache__", ".pytest_cache", ".venv", "node_modules"}
EXCLUDE_FILES = {"CHANGELOG.md", "VARIABLES.md", "README.md"}      # regenerated for the new repo
TEXT_EXT = {".md", ".py", ".yaml", ".yml", ".sql", ".json", ".toml", ".txt"}
TOKEN = re.compile(r"\[([A-Z][A-Z0-9_]+)\](?!\()")


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    if not slug:
        raise SystemExit("Company name must contain letters or digits.")
    return slug


def _ignore(_dir: str, names: list[str]) -> set[str]:
    return {n for n in names if n in EXCLUDE_DIRS or n.endswith(".pyc")}


def copy_template(dest: Path) -> None:
    shutil.copytree(ROOT, dest, ignore=_ignore, dirs_exist_ok=True)
    for name in EXCLUDE_FILES:
        f = dest / name
        if f.exists():
            f.unlink()
    # never carry a prior company config, the scaffolder, or template-only tests/docs
    for rel in ("config/company.yaml", "scripts/new_company.py", "tests/test_scaffold.py",
                "docs/overview/new-company-repo.md"):
        f = dest / rel
        if f.exists():
            f.unlink()


def write_config(dest: Path, company: str, fy_start_month: int, variables: dict[str, str]) -> Path:
    text = (ROOT / "config" / "example.yaml").read_text(encoding="utf-8")
    text = text.replace("name: Example Co", f"name: {company}", 1)
    text = text.replace("  COMPANY_NAME: Example Co", f"  COMPANY_NAME: {company}", 1)
    text = text.replace("year_start_month: 10", f"year_start_month: {fy_start_month}", 1)
    # quarter labels in the example (quota, bookings plan, current quarter) are for an Oct-start fiscal year;
    # relabel every one of them for other calendars so the keys still line up with the dates
    if fy_start_month != 10:
        text = FY_LABEL.sub(lambda m: relabel_quarter(m.group(0), fy_start_month), text)
    for key, value in variables.items():
        text = re.sub(rf"^(  {key}: ).*$", rf"\g<1>{value}", text, count=1, flags=re.M)
    header = (f"# Company config for {company}. Generated {date.today().isoformat()} from the template's config/example.yaml.\n"
              "# Every value is an [ASSUME] until you replace it with a sourced fact.\n")
    path = dest / "config" / "company.yaml"
    path.write_text(header + text, encoding="utf-8")
    (dest / "config" / "example.yaml").unlink(missing_ok=True)
    return path


FY_LABEL = re.compile(r"FY(\d{2})-Q([1-4])")


def relabel_quarter(label: str, start_month: int) -> str:
    """Map an Oct-start quarter label (FY27-Q1 = Oct-Dec 2026) to the same calendar quarter under another start month."""
    m = FY_LABEL.fullmatch(label)
    fy, q = 2000 + int(m.group(1)), int(m.group(2))
    months = (fy - 1) * 12 + 9 + 3 * (q - 1)           # months since year 0; Oct = index 9
    return fiscal_label(date(months // 12, months % 12 + 1, 1), start_month)


def fiscal_label(d: date, start_month: int) -> str:
    fy = d.year + (1 if start_month > 1 and d.month >= start_month else 0)
    q = ((d.month - start_month) % 12) // 3 + 1
    return f"FY{str(fy)[2:]}-Q{q}"


def load_variables(config_path: Path) -> dict[str, str]:
    import yaml
    return {k: str(v) for k, v in (yaml.safe_load(config_path.read_text(encoding="utf-8")).get("variables") or {}).items()}


def resolve_tokens(dest: Path, variables: dict[str, str]) -> dict[str, int]:
    """Replace [KEY] with its value in text files. Returns {unresolved token: count}."""
    unresolved: dict[str, int] = {}

    def repl(m: re.Match) -> str:
        key = m.group(1)
        if key in variables:
            return variables[key]
        unresolved[key] = unresolved.get(key, 0) + 1
        return m.group(0)

    for f in dest.rglob("*"):
        if not f.is_file() or f.suffix not in TEXT_EXT or any(p in EXCLUDE_DIRS for p in f.parts):
            continue
        if f.name == "company.yaml":
            continue
        s = f.read_text(encoding="utf-8")
        n = TOKEN.sub(repl, s)
        if n != s:
            f.write_text(n, encoding="utf-8")
    # tokens used as provenance tags are intentional, not unresolved variables
    for tag in ("ASSUME", "PUBLIC", "POSTING", "VERIFY"):
        unresolved.pop(tag, None)
    return unresolved


def write_variables_md(dest: Path, company: str, variables: dict[str, str]) -> None:
    rows = "\n".join(f"| `[{k}]` | {v} | ASSUME | docs, prompts |" for k, v in variables.items())
    (dest / "VARIABLES.md").write_text(f"""# Variables: {company}

Resolved from `config/company.yaml` when the repo was created. Every value starts as `ASSUME`; change the
provenance as you verify each one.

**Provenance:** `PUBLIC` = company site, press release or earnings coverage · `POSTING` = a job posting or brief ·
`ASSUME` = a working assumption to validate · `VERIFY` = from general knowledge, check before using

| Variable | Value | Provenance | Used in |
|---|---|---|---|
{rows}

The machine-readable source of truth is `config/company.yaml` (segments, personas, scoring weights, stages,
SLAs, quota, fiscal calendar). Edit it, then update the lookup tables in `scripts/generate_sample_data.py`
if you changed segment or persona keys, and run `make data demo test`.
""", encoding="utf-8")


def write_readme(dest: Path, company: str) -> None:
    (dest / "README.md").write_text(f"""# {company} GTM & RevOps Toolkit

Created from the GTM & RevOps toolkit template on {date.today().isoformat()}. Synthetic data only until you wire in real exports.

```bash
pip install -r requirements.txt
make data demo test
```

Start with `docs/overview/README.md`. Company facts live in `config/company.yaml`; sources and assumptions in `VARIABLES.md`.

## First edits

1. Replace the example segments, personas, stack and partners in `config/company.yaml` with sourced facts. Tag each `[PUBLIC]`, `[POSTING]` or `[ASSUME]`.
2. If you renamed segment or persona keys, update the lookup tables at the top of `scripts/generate_sample_data.py` (it fails fast if they drift), then `make data`.
3. Re-run `make demo test`, and read the calibration output before trusting any score weights.
4. Rewrite the spec pages in `gtm_engineer/` and `gtm_strategy_ops/` where the company's process differs from the example.
5. Keep strategy, financials, prospect lists and client notes out of this repo.
""", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("company", help='Company name, e.g. "Acme Corp"')
    ap.add_argument("--dest", help="Destination directory (default: ../<slug>-gtm-toolkit next to the template)")
    ap.add_argument("--fy-start-month", type=int, default=10, choices=range(1, 13), metavar="1-12",
                    help="Month the company's fiscal year begins (default 10; 1 = calendar year)")
    ap.add_argument("--git", action="store_true", help="Run `git init` in the new directory (no commit, no remote)")
    args = ap.parse_args()

    dest = Path(args.dest).expanduser().resolve() if args.dest else ROOT.parent / f"{slugify(args.company)}-gtm-toolkit"
    if dest == ROOT or ROOT in dest.parents:
        raise SystemExit("Destination must be outside the template directory.")
    if dest.exists() and any(dest.iterdir()):
        raise SystemExit(f"{dest} already exists and is not empty. Pick another --dest.")

    copy_template(dest)
    cfg = write_config(dest, args.company, args.fy_start_month, {})
    variables = load_variables(cfg)
    unresolved = resolve_tokens(dest, variables)
    write_variables_md(dest, args.company, variables)
    write_readme(dest, args.company)
    if args.git:
        subprocess.run(["git", "init", "-q"], cwd=dest, check=False)

    print(f"Created {dest}")
    if unresolved:
        print("Unresolved [TOKENS] (add them under `variables:` in config/company.yaml):")
        for k, n in sorted(unresolved.items()):
            print(f"  [{k}] x{n}")
    print("Next: cd there, `pip install -r requirements.txt`, `make data demo test`, then edit config/company.yaml.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
