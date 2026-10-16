import json
import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
FIX = Path(__file__).parent / "fixtures"


def fixture(name):
    return json.loads((FIX / name).read_text())


@pytest.fixture(autouse=True)
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"
    shutil.copytree(ROOT / "data", d)
    monkeypatch.setenv("SPEED_TO_LEAD_DATA_DIR", str(d))
    for k in ("SPEED_TO_LEAD_ADAPTERS", "ALLOW_LIVE_WRITES", "SPEED_TO_LEAD_JSON_PATH",
              "HUBSPOT_TOKEN", "SLACK_BOT_TOKEN", "HUBSPOT_SEQUENCE_USER_ID", "HUBSPOT_SENDER_EMAIL"):
        monkeypatch.delenv(k, raising=False)
    return d
