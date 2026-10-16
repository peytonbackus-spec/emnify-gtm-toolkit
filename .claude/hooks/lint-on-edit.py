#!/usr/bin/env python3
"""PostToolUse(Write|Edit): run ruff (the linter in Makefile `lint` / pyproject [tool.ruff]) on the edited .py file."""
import json
import os
import shutil
import subprocess
import sys


def main():
    try:
        data = json.load(sys.stdin)
        path = (data.get("tool_input") or {}).get("file_path") or ""
    except Exception:
        return 0
    root = os.path.realpath(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())
    path = os.path.realpath(os.path.expanduser(path))
    if not path.endswith(".py") or not path.startswith(root + os.sep) or not os.path.isfile(path):
        return 0
    parts = path[len(root) + 1:].split(os.sep)
    if ".venv" in parts:
        return 0
    ruff = shutil.which("ruff")
    cmd = [ruff] if ruff else [sys.executable, "-m", "ruff"]
    try:
        r = subprocess.run(cmd + ["check", path], cwd=root, capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        return 0
    if r.returncode != 0 and "No module named ruff" in (r.stderr or ""):
        return 0
    if r.returncode != 0:
        print(f"ruff failed on {os.path.relpath(path, root)}:\n{r.stdout}{r.stderr}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
