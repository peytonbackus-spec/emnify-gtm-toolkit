import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_scaffold_generates_runnable_repo():
    with tempfile.TemporaryDirectory() as tmp:
        dest = Path(tmp) / "acme"
        subprocess.run([sys.executable, str(ROOT / "scripts" / "new_company.py"), "Acme Corp",
                        "--dest", str(dest), "--fy-start-month", "1"], check=True, capture_output=True)
        cfg = (dest / "config" / "company.yaml").read_text()
        assert "name: Acme Corp" in cfg and "year_start_month: 1" in cfg
        assert not (dest / "config" / "example.yaml").exists()
        assert not (dest / "private-vault").exists()
        assert "Example Co" not in "".join(p.read_text() for p in dest.rglob("*.md"))
        r = subprocess.run([sys.executable, "-m", "gtm_engineer.lead_scoring.score_leads"],
                           cwd=dest, capture_output=True, text=True)
        assert r.returncode == 0 and "Acme Corp" in r.stdout


def test_scaffolded_repo_does_not_carry_template_only_files():
    with tempfile.TemporaryDirectory() as tmp:
        dest = Path(tmp) / "acme"
        subprocess.run([sys.executable, str(ROOT / "scripts" / "new_company.py"), "Acme Corp", "--dest", str(dest)],
                       check=True, capture_output=True)
        for rel in ("scripts/new_company.py", "tests/test_scaffold.py", "docs/overview/new-company-repo.md"):
            assert not (dest / rel).exists(), rel


def test_scaffold_with_calendar_fiscal_year_keeps_quarter_keys_aligned():
    """The relabelled quota and bookings-plan keys must still line up with the dates after `make data`."""
    with tempfile.TemporaryDirectory() as tmp:
        dest = Path(tmp) / "acme"
        subprocess.run([sys.executable, str(ROOT / "scripts" / "new_company.py"), "Acme Corp",
                        "--dest", str(dest), "--fy-start-month", "1"], check=True, capture_output=True)
        import yaml
        cfg = yaml.safe_load((dest / "config" / "company.yaml").read_text())
        assert cfg["current_fiscal_quarter"] == "FY26-Q4"
        assert list(cfg["sales_planning"]["bookings_plan"]) == ["FY27-Q1", "FY27-Q2", "FY27-Q3", "FY27-Q4"]
        assert "FY26-Q3" in cfg["quota"] and "FY26-Q4" in cfg["quota"]
        runs = [[str(dest / "scripts" / "generate_sample_data.py")]] + [["-m", m] for m in (
            "gtm_strategy_ops.sales_leadership.vp_brief", "gtm_strategy_ops.sales_planning.capacity_plan",
            "gtm_strategy_ops.sales_planning.quota_plan", "gtm_engineer.marketing_ops.campaign_report",
            "gtm_engineer.marketing_ops.demand_plan")]
        for args in runs:
            r = subprocess.run([sys.executable, *args], cwd=dest, capture_output=True, text=True)
            assert r.returncode == 0, (args, r.stderr[-400:])
