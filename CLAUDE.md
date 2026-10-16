# gtm-revops-toolkit

Public GitHub repo (peytonbackus-spec/gtm-revops-toolkit). See README.md for purpose and layout, and docs/REPO_MAP.md for the file map.

## Rules
- Public repo: never commit secrets, API keys, client or prospect data, or anything under a `_private/` folder.
- Never commit or push unless I ask for it in that message.
- Run the tests (`make test` or `pytest`) before proposing a change as done.
- Python venvs (`.venv/`) and `outputs/` are local and ignored; don't add them.
- Project MCP servers live in `mcp/*/` and are wired in `.mcp.json`; if the repo path changes, update `.mcp.json` and recheck `claude mcp list`.
