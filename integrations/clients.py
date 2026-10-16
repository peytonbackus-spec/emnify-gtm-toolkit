"""Client STUBS for systems that need credentials. None of these call out. Env var names only; values stay in the environment."""
from __future__ import annotations

import os
from typing import Any, Dict, List


class _Stub:
    system = ""
    env: tuple = ()

    def __init__(self) -> None:
        missing = [v for v in self.env if not os.environ.get(v)]
        if missing:
            raise RuntimeError(f"stub: {self.system} needs {', '.join(missing)}")

    def _todo(self, what: str) -> Any:
        raise NotImplementedError(f"stub: {self.system} {what} is not implemented in this build")


class AmplemarketClient(_Stub):
    system, env = "Amplemarket", ("AMPLEMARKET_API_KEY",)

    def import_list(self, rows: List[Dict[str, Any]]) -> Any:
        return self._todo("list import")


class AttentionClient(_Stub):
    system, env = "Attention", ("ATTENTION_API_KEY",)

    def call_summaries(self, since: str) -> Any:
        return self._todo("call summaries")


class WeflowClient(_Stub):
    system, env = "Weflow", ("WEFLOW_API_KEY",)

    def activities(self, since: str) -> Any:
        return self._todo("activities")


class ClayClient(_Stub):
    system, env = "Clay", ("CLAY_API_KEY",)

    def push_rows(self, table_id: str, rows: List[Dict[str, Any]]) -> Any:
        return self._todo("row push")
