# Setup notes for Steve

## Repo layout (as built)
```
campaign/codex/        living reference files + glossary.md + ingest_log.md
campaign/summaries/    Session_###_YYYYMMDD.md
campaign/transcripts/  Session_###_YYYYMMDD.docx (raw) + .txt (normalized, indexed)
campaign/tools/        normalize_transcript.py (speaker alias map)
campaign/skill/        getaround-chronicler skill + .zip for players
mcp/                   server
```

## Before players connect
- **Make the GitHub repo private.** It's public right now, and the transcripts are full recordings of real people, with names, work chat and side conversation. The server can pull from a private repo with a deploy key or a fine-grained read-only token.
- Run the server with `CAMPAIGN_TOKENS` (one token per player). It must be reachable over public HTTPS, because Claude connects from Anthropic's cloud.

## Player setup
1. Install the skill: upload `campaign/skill/getaround-chronicler.zip` under Customize → Skills.
2. Add the connector: + → Add custom connector → paste `https://<host>/t/<their-token>/mcp`.

The skill holds only the procedure. New sessions, aliases and glossary entries arrive through the repo/server, so players re-install the skill only when the procedure changes.

## Weekly flow (Jake, in Cowork at C:\GetAroundBoys)
1. Add `campaign/transcripts/Session_###_YYYYMMDD.docx`.
2. Ask Claude to "ingest session ###". It writes the `.txt`, the summary and the codex updates, and prepends to `ingest_log.md`.
3. Review, then commit and push. The server's index rebuilds when files change. Make sure the server host pulls (cron, or a webhook on push).

## Corrections
Tell Claude "corrections from the table: …". It updates every affected file and logs each item with a Source (DM / table / player). Review, then commit.
