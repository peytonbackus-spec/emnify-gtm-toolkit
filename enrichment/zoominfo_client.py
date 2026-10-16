"""ZoomInfo provider: STUB. Needs a ZoomInfo contract and API credentials; nothing here calls out.

Implements the Provider protocol from waterfall.py so it can replace the fixture provider without engine changes.
"""
from __future__ import annotations

import os
from typing import Any, Dict, Optional, Tuple

REQUIRED_ENV = ("ZOOMINFO_USERNAME", "ZOOMINFO_CLIENT_ID", "ZOOMINFO_PRIVATE_KEY")   # names only


class ZoomInfoProvider:
    name = "zoominfo"

    def __init__(self) -> None:
        missing = [v for v in REQUIRED_ENV if not os.environ.get(v)]
        if missing:
            raise RuntimeError(f"stub: ZoomInfo lookups need {', '.join(missing)}")

    def lookup(self, record: Dict[str, Any], field_name: str) -> Optional[Tuple[Any, float]]:
        raise NotImplementedError("stub: map ZoomInfo's response confidence to a 0-1 score here")
