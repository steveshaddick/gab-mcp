# Campaign MCP server

Read-only MCP server over your campaign files, searched with SQLite FTS5.

## Layout

```
campaign/
  summaries/    S1.md, S2.md, ...      one page per session
  codex/        npcs.md, locations.md, open-threads.md, glossary.md, characters/*.md
  transcripts/  S1.txt, S2.txt, ...    raw, searched only on request
  dm/           NEVER indexed or served (secrets, planned plot)
```

Session numbers come from the first number in the filename (`S12.md` -> 12).

## Glossary (fixes speech-to-text spellings)

`codex/glossary.md`, one group per line, spellings only:

```
- Holda: Olda, Holdah
- Vassil: Vasil, Vassel
```

Searching any spelling also matches the others. Single-word names only.

## Run

```
pip install -r requirements.txt
export CAMPAIGN_DIR=./campaign
export CAMPAIGN_TOKENS="steve=<long-random>,alice=<long-random>"
uvicorn server:app --host 127.0.0.1 --port 8000
```

Generate tokens with `python -c "import secrets; print(secrets.token_urlsafe(32))"`.
Local testing without auth: `CAMPAIGN_ALLOW_NO_AUTH=1`.

The index rebuilds automatically when any file is added, removed, or changed.
`python index.py` forces a rebuild.

## Deploy (Steve)

- Put Caddy or nginx in front for HTTPS; Claude connects from Anthropic's cloud, so it must be public.
- Each player's connector URL: `https://your.domain/t/<their-token>/mcp`
- Turn off request-path logging at the proxy (tokens are in the URL).
- Revoke a player by removing their token from `CAMPAIGN_TOKENS` and restarting.
- Keep the repo pull (or file sync) on a cron so new sessions appear without a restart.

## Test locally

`npx @modelcontextprotocol/inspector` and point it at `http://127.0.0.1:8000/mcp`
(with `CAMPAIGN_ALLOW_NO_AUTH=1`).

## Not included yet

OAuth (the proper upgrade over URL tokens), and any write tools. Ingest stays
in Cowork or chat, reviewed in Git.
