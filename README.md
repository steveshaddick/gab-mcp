# Getaround Boys — Campaign Brain

Shared memory for our D&D 5e campaign.

- `transcripts/` — raw session transcripts, **archive only**. Don't load these into Claude wholesale.
- `summaries/` — one page per session.
- `codex/` — living reference files. **Start with `codex/00_campaign_overview.md`.**
- `skill/getaround-chronicler/` — the Claude Skill. Zip that folder and upload it in Claude under Customize → Skills.
- `SETUP_FOR_STEVE.md` — hosting / MCP notes.
- `tools/normalize_transcript.py` — strips a Teams transcript down to `SPEAKER (Character): text`.

Local clone for Jake / Cowork: `C:\GetAroundBoys`

## Weekly flow
1. Drop the new transcript in `transcripts/` as `Session_###_YYYYMMDD.docx`.
2. Ask Claude (with the skill installed) to "ingest session ###".
3. Review the change log it appends to `codex/ingest_log.md`.
4. Commit and push.
