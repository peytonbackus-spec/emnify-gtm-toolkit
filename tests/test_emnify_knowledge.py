from datetime import date

import yaml

from emnify_gtm.company import ROOT
from knowledge import tools


def test_validate_clean_and_stale():
    assert tools.validate(date(2026, 10, 16)) == []
    assert any("stale" in p for p in tools.validate(date(2027, 12, 1)))


def test_lookup_routes_and_gaps():
    assert tools.lookup("launch outbound list")[0]["id"] == "contract-outbound-launch"
    assert tools.lookup("organize the holiday party") == []


def test_index_is_current():
    idx = yaml.safe_load((ROOT / "knowledge" / "INDEX.yaml").read_text())
    assert {d["id"] for d in idx["documents"]} == {d["id"] for d in tools.documents()}
