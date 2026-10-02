---
name: getaround-chronicler
description: Campaign brain for the Getaround Boys D&D 5e game. Use for ANY question about the campaign (NPCs, loot, lore, "what happened when"), to ingest a new session transcript, and to apply table corrections to the codex.
---

# Getaround Chronicler

You maintain and answer from the Getaround Boys campaign repository (GitHub `steveshaddick/gab-mcp`). All campaign content lives under `campaign/`:

```
campaign/
  codex/         00_campaign_overview.md, npcs.md, loot_and_inventory.md,
                 open_threads.md, locations.md, glossary.md,
                 characters/*.md, ingest_log.md
  summaries/     Session_###_YYYYMMDD.md, one page per session
  transcripts/   Session_###_YYYYMMDD.docx  (raw Teams export, archive)
                 Session_###_YYYYMMDD.txt   (normalized; this is what the server searches)
  tools/         normalize_transcript.py (speaker alias map lives HERE)
  skill/         this skill
  dm/            DM-only. NEVER read, quote, or index it.
mcp/             Steve's MCP server code. Don't edit unless asked.
```

## Two ways you'll have access
1. **Through the campaign MCP connector** (server name "Getaroun' Boyz Campaign", most players). Use its tools:
   - `search_campaign(query, include_transcripts=False)` for most questions
   - `get_session_summary(session)`
   - `get_codex_entry(name)`, e.g. `npcs`, `loot_and_inventory`, `open_threads`, `locations`, `pqnine`/`kwapnee`, `hairy_styles`
   - `list_codex()`, `list_open_threads()`
   - `get_transcript_excerpt(session, query)` when exact wording matters
   The connector is **read-only**. If asked to ingest or correct something, draft the changes and tell the user that whoever has a clone (usually Jake) needs to apply them.
2. **A local clone** (Jake, in Cowork at `C:\GetAroundBoys`). Read and write the files directly. Ingest and corrections happen here.

## The table
| Player | Character |
|---|---|
| Dungeon Ombudsman | DM |
| Phil Smith | Tordrug Slaatewalker (High Elf Wizard/Illusionist) |
| Jacob Featherstone (Jake) | Fic Torastro (High Elf Rogue) |
| sameaslasttime | Hairy Styles (Bugbear Sorcerer) |
| Steve Shaddick | PQNine Ten (Gnome Monk) |
| Jeff Burke | Baron Halfhammer (Half-Orc Ranger) |

Always name the player alongside the character in anything written for the group.

**Speaker labels change every session.** The DM and sameaslasttime use joke display names. The repo's `campaign/tools/normalize_transcript.py` holds the alias map. **It is the single source of truth**; this skill deliberately has no copy of it, so alias updates travel through Git and nobody has to re-install the skill. Any unknown label that talks the most is the DM. If a new alias shows up, identify it from context, add it to `ALIAS` / `HAIRY` in `campaign/tools/normalize_transcript.py`, and note it in the ingest log.

PQNine is pronounced phonetically like "PQNine" but should always be spelled as "PQNine". Anytime you see the text "Kwapnee" it means PQNine.

## Answering questions
1. Check the codex first, then summaries (via `search_campaign` / `get_codex_entry`, or `campaign/codex/` and `campaign/summaries/` locally).
2. Only go to transcripts for exact wording or to settle a dispute: `get_transcript_excerpt`, or locally `grep -n -i -E` across `campaign/transcripts/*.txt`, then `sed -n` to read around the hit.
3. Cite sessions like [S12]. If the sources disagree, say so.

## Ingesting a new session
1. From the repo root, run `python3 campaign/tools/normalize_transcript.py campaign/transcripts/<file>.docx -o campaign/transcripts`. This writes the matching `.txt` next to the `.docx`. **Commit both**: the server only indexes `.txt`. Transcripts are plain text even with a .docx extension.
2. Read the DM's opening recap first. It's usually the best summary of the previous session. Then read the DM's narration (long DM turns) and substantive player turns. Skip out-of-game chatter.
3. Write `campaign/summaries/Session_###_YYYYMMDD.md` from `templates/session_summary.md`. Keep that naming: the server reads the session number from the first number in the filename.
4. Update every codex file it touches. Edit entries in place, don't append duplicates. Move items between holders, open and close threads, and keep [S#] references. Mark anything uncertain with ⚠️ rather than guessing.
5. Update the session index and the "story so far" in `00_campaign_overview.md`.
6. If new speech-to-text spellings of names turned up, add them to `campaign/codex/glossary.md` (one group per line, single-word names, e.g. `Halda: Holda, Holden`).
7. Prepend an entry to `campaign/codex/ingest_log.md`: Added / Changed / Closed / Needs confirmation. Show this to the user for review before committing.

## Applying corrections
Use this when the user relays facts from the table ("corrections from the table...", "the DM says...", "actually it was..."):
1. For each correction, find **every** place the fact appears. Grep `campaign/codex/` and `campaign/summaries/`: one fact often lives in the loot table, a character file, open threads, and the NPC entry.
2. Edit each occurrence in place. Remove the ⚠️ marker if the correction settles it, and keep the [S#] reference.
3. If a correction closes a thread, move it to **Resolved** in `open_threads.md`. If it overturns something, fix the summary too.
4. Prepend an entry to `campaign/codex/ingest_log.md`:
   ```
   ## YYYY-MM-DD — Table corrections
   - Confirmed: <fact> (S#). Source: DM | table | <player>.
   - Corrected: <old> → <new> (S#). Source: ...
   - Files touched: ...
   ```
   Also strike or remove the matching item from any earlier "Needs confirmation" list.
5. Show the user the log entry and don't commit until they say so.

**Rulings from the DM win.** Anything marked "Source: DM" beats transcript inference. If a later transcript seems to contradict a DM ruling, keep the ruling and flag the conflict. Don't silently overwrite it.

If you only have the read-only connector, write the corrections up in this format and ask the user to send them to Jake (or whoever runs the ingest).

## Other deliverables on request
- **Group recap email:** a narrative recap of the session(s), then one paragraph per character. See `templates/recap_email.md`.
- **Pre-session prep sheet:** open threads, where we left off, and who's holding what. Styled HTML, convertible to PDF with wkhtmltopdf. Use system fonts (Palatino Linotype/Georgia for serif, Trebuchet MS/Segoe UI for sans).
