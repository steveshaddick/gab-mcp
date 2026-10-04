# Getaround Boys — Campaign Brain

Shared memory for our D&D 5e campaign.

## Folder structure
- `campaign/` - holds the knowledge folders
- `campaign/transcripts/` — raw session transcripts, **archive only**. Don't load these into Claude wholesale.
- `campaign/summaries/` — one page per session.
- `campaign/codex/` — living reference files. **Start with `codex/00_campaign_overview.md`.**
- `tools/normalize_transcript.py` — strips a Teams transcript down to `SPEAKER (Character): text`.
- `skill/` - holds the Claude Skill.
- `mcp/` - holds the mcp server
- `SETUP_FOR_STEVE.md` — hosting / MCP notes.

Local clone for Jake / Cowork: `C:\GetAroundBoys`

## Weekly flow
1. Drop the new transcript in `campaign/transcripts/` as `Session_###_YYYYMMDD.docx`.
2. Ask Claude (with the skill installed) to "ingest session ###".
3. Review the change log it appends to `campaign/codex/ingest_log.md`.
4. Commit and push.
