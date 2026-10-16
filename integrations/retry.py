"""Retry with exponential backoff and a dead-letter record. Offline-testable (inject sleep)."""
from __future__ import annotations

import time
from typing import Any, Callable, Dict, List, Optional

DEAD_LETTER: List[Dict[str, Any]] = []   # in production: an n8n error workflow row or a queue, see observability.md


def with_retry(fn: Callable[[], Any], *, attempts: int = 3, base_delay: float = 1.0,
               retry_on: tuple = (ConnectionError, TimeoutError), sleep: Callable[[float], None] = time.sleep,
               context: Optional[Dict[str, Any]] = None) -> Any:
    last: Optional[BaseException] = None
    for i in range(attempts):
        try:
            return fn()
        except retry_on as exc:   # only transient errors retry; contract errors fail fast
            last = exc
            if i < attempts - 1:
                sleep(base_delay * (2 ** i))
    DEAD_LETTER.append({"error": repr(last), "attempts": attempts, **(context or {})})
    raise last  # type: ignore[misc]
