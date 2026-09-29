# Campaign MCP server

Read-only MCP server (Python, SQLite FTS5) that lets players' Claude search our DnD campaign: session summaries, a codex of living reference files, and raw transcripts.

## Layout

- `mcp`: The MCP server code, written in Python3
- `mcp/server.py`: FastMCP tools + per-player token auth (`CAMPAIGN_TOKENS`)
- `mcp/index.py`: builds/queries the FTS5 index; rebuilds automatically when files change
- `campaign/summaries/`: `S<number>.md`, one page per session
- `campaign/codex/`: living reference files (npcs, locations, factions, loot, timeline, lore, open-threads, glossary, `characters/<name>.md`)
- `campaign/transcripts/`: `S<number>.txt`, raw, searched only on request
- `campaign/dm/`: DM-only. NEVER indexed or served. Do not add it to `SOURCES` in `index.py`.
- `campaign/templates/`, `campaign/INGEST.md`: not indexed; templates and the ingest procedure

## Commands

- Install: `pip install -r requirements.txt`
- Rebuild index: `CAMPAIGN_DIR=./campaign python index.py`
- Run locally without auth: `CAMPAIGN_ALLOW_NO_AUTH=1 uvicorn server:app --port 8000`
- Run with auth: `CAMPAIGN_TOKENS="name=secret,..." uvicorn server:app --port 8000`
- Inspect tools: `npx @modelcontextprotocol/inspector` -> `http://127.0.0.1:8000/mcp`

## Status

- `index.py` was tested (build, alias search, DM-folder isolation).
- `server.py` has NOT been run against the real `mcp` package yet. First task: install, launch, and fix any SDK/API differences (imports, `TransportSecuritySettings`, `streamable_http_app`).

## Conventions

- Session number = first number in the filename (`S12.md` -> 12). Keep names consistent.
- Tools are read-only. Any write path must be a separate, role-gated tool.
- Token comparison uses `hmac.compare_digest`; don't log request paths (tokens appear in `/t/<token>/mcp`).
- Keep the tool surface small; return short, cited passages rather than whole files where possible.
- Glossary format is one spelling group per line: `Holda: Olda, Holdah` (single-word names only).

## Planned work

- Player identity from token (attach name in `TokenAuth`, read it in tools) for a `my_character` tool
- Roles: DM token unlocks DM-only tools; players see only what their character knows
- Usage logging (who searched what), OAuth to replace URL tokens
- Packaging the ingest procedure (`campaign/INGEST.md`) as a Skill
