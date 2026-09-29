# Setup notes for Steve

## 1. The repo
Commit this folder as-is to a **private** Git repo, and add the other four players as collaborators.
- `codex/` + `summaries/` ≈ 55 KB total. This is what Claude reads.
- `transcripts/` ≈ 3.4 MB of raw Teams exports. Archive only; `.docx` files that are really plain text.
- `skill/getaround-chronicler.zip` is the Claude Skill. Each player uploads it in Claude under **Customize → Skills → + → Upload a skill**. It's private per account, so everyone installs their own copy. The skill holds only the *procedure* (no campaign data, no alias map), so players re-install it only when the procedure changes. New sessions and new aliases arrive through the repo.

Jake's local clone lives at `C:\GetAroundBoys` (for Cowork).

## 2. Remote MCP server (optional, but it's what makes the brain shared)
Claude connects to it **from Anthropic's cloud**, so it must be reachable on the public internet over HTTPS. Put auth on it (a token or OAuth).
Suggested read-only tools, backed by a pull of the repo:
- `list_files()` → paths under `codex/` and `summaries/`
- `read_file(path)`
- `search(query)` → grep across codex, summaries and transcripts; returns file, line, and snippet
- `read_transcript_range(session, start_line, end_line)`

Later, optionally, add `write_file(path, content)` + `commit(message)` so any player's Claude can run the weekly ingest.

Each player adds it in Claude via **+ → Add custom connector → paste URL**. Free plans allow one custom connector.

## 3. Weekly flow
1. Add `transcripts/Session_###_YYYYMMDD.docx`.
2. In Claude: "ingest session ###" (with the skill installed). Claude writes the summary, updates the codex, and appends to `codex/ingest_log.md`.
3. Review the log entry, then commit and push.

## Corrections
Tell Claude "corrections from the table: …". It updates every affected file and logs each item with a Source (DM / table / player). Review, then commit with a message like `Table corrections after S33`.
