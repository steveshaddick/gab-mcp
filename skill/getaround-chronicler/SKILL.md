---
name: getaround-chronicler
description: Campaign brain for the Getaround Boys D&D 5e game. Use for ANY question about the campaign (NPCs, loot, lore, "what happened when"), to ingest a new session transcript, and to apply table corrections to the codex.
---

# Getaround Chronicler

You maintain and answer from the Getaround Boys campaign repository:

```
transcripts/   raw Teams transcripts (archive; search, don't load whole)
tools/         normalize_transcript.py (speaker alias map lives HERE)
summaries/     one page per session
codex/         00_campaign_overview.md, npcs.md, loot_and_inventory.md,
               open_threads.md, locations.md, characters/*.md, ingest_log.md
```

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

**Speaker labels change every session.** The DM and sameaslasttime use joke display names. The repo's `tools/normalize_transcript.py` holds the alias map. **It is the single source of truth**; this skill deliberately has no copy of it, so alias updates travel through Git and nobody has to re-install the skill. Any unknown label that talks the most is the DM. If a new alias shows up, identify it from context, add it to `ALIAS` / `HAIRY` in `tools/normalize_transcript.py`, and note it in the ingest log.

PQNine is pronounced phonetically like "PQNine" but should always be spelled as "PQNine".

If the repo isn't on the local disk (e.g. a player using only the MCP connector), answer questions through the connector's tools. Ingesting and corrections are normally done by whoever has a clone. If you can't write to the repo, draft the changes and say so.

## Answering questions
1. Check `codex/` first, then `summaries/`.
2. Only go to `transcripts/` for exact wording or to settle a dispute. Use `grep -n -i -E` across files, then `sed -n` to read around the hit.
3. Cite sessions like [S12]. If the sources disagree, say so.

## Ingesting a new session
1. Run `python3 tools/normalize_transcript.py transcripts/<file> -o <scratch folder outside the repo>` from the repo root (or omit -o to print). Transcripts are plain text even with a .docx extension.
2. Read the DM's opening recap first. It's usually the best summary of the previous session. Then read the DM's narration (long DM turns) and substantive player turns. Skip out-of-game chatter.
3. Write `summaries/Session_###_YYYYMMDD.md` from `templates/session_summary.md`.
4. Update every codex file it touches. Edit entries in place, don't append duplicates. Move items between holders, open and close threads, and keep [S#] references. Mark anything uncertain with ⚠️ rather than guessing.
5. Update the session index and the "story so far" in `00_campaign_overview.md`.
6. Prepend an entry to `codex/ingest_log.md`: Added / Changed / Closed / Needs confirmation. Show this to the user for review before committing.

## Applying corrections
Use this when the user relays facts from the table ("corrections from the table...", "the DM says...", "actually it was..."):
1. For each correction, find **every** place the fact appears. Grep `codex/` and `summaries/`: one fact often lives in the loot table, a character file, open threads, and the NPC entry.
2. Edit each occurrence in place. Remove the ⚠️ marker if the correction settles it, and keep the [S#] reference.
3. If a correction closes a thread, move it to **Resolved** in `open_threads.md`. If it overturns something, fix the summary too.
4. Prepend an entry to `codex/ingest_log.md`:
   ```
   ## YYYY-MM-DD — Table corrections
   - Confirmed: <fact> (S#). Source: DM | table | <player>.
   - Corrected: <old> → <new> (S#). Source: ...
   - Files touched: ...
   ```
   Also strike or remove the matching item from any earlier "Needs confirmation" list.
5. Show the user the log entry and don't commit until they say so.

**Rulings from the DM win.** Anything marked "Source: DM" beats transcript inference. If a later transcript seems to contradict a DM ruling, keep the ruling and flag the conflict. Don't silently overwrite it.

## Other deliverables on request
- **Group recap email:** a narrative recap of the session(s), then one paragraph per character. See `templates/recap_email.md`.
- **Pre-session prep sheet:** open threads, where we left off, and who's holding what. Styled HTML, convertible to PDF with wkhtmltopdf. Use system fonts (Palatino Linotype/Georgia for serif, Trebuchet MS/Segoe UI for sans).
