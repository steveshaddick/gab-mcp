---
name: getaround-archivist
description: Jake's skill for ingesting new Getaroun' Boyz D&D session transcripts into the gab-mcp repo and getting the changes back to Steve. Use when Jake has a new .docx transcript to add, needs to write a summary from one, update the codex after a session, apply table corrections from the DM, or open a pull request to Steve's repo with the changes. Requires a local clone of the repo (normally C:\\GetAroundBoys).
---

# Getaround Archivist

Jake's ingest + maintenance skill for the Getaroun' Boyz campaign repo (`https://github.com/steveshaddick/gab-mcp`). This writes to the repo and pushes to a branch for a PR. For question-answering, group recaps, and prep sheets, use `getaround-chronicler` instead.

## Repo layout (what you edit)

```
campaign/transcripts/   Session_###_YYYYMMDD.docx   raw Teams export, archive
                        Session_###_YYYYMMDD.txt    normalized; what the MCP server indexes
campaign/summaries/     Session_###_YYYYMMDD.md     one page per session
campaign/codex/         00_campaign_overview.md, npcs.md, loot_and_inventory.md,
                        open_threads.md, locations.md, glossary.md,
                        characters/*.md, ingest_log.md
skill/getaround-archivist/
  tools/normalize_transcript.py   speaker alias map (single source of truth)
  templates/session_summary.md
campaign/dm/            DM-only. NEVER read, quote, or index it.
```

## The table (for speaker attribution)
| Player | Character |
|---|---|
| Dungeon Ombudsman | DM |
| Phil Smith | Tordrug Slaatewalker (High Elf Wizard/Illusionist) |
| Jacob Featherstone (Jake) | Fic Torastro (High Elf Rogue) |
| sameaslasttime | Hairy Styles (Bugbear Sorcerer) |
| Steve Shaddick | PQNine Ten (Gnome Monk) |
| Jeff Burke | Baron Halfhammer (Half-Orc Ranger) |

**Speaker labels change every session.** The DM and sameaslasttime use joke display names. The alias map is in `tools/normalize_transcript.py` and is the single source of truth; this skill deliberately keeps no second copy, so updates travel through Git and nobody has to re-install the skill. Any unknown label that talks the most is the DM. If a new alias shows up, identify it from context, add it to `ALIAS` / `HAIRY` in `tools/normalize_transcript.py`, and note it in the ingest log.

PQNine is pronounced "Kwapnee" but should always be **spelled** PQNine. Anytime you see "Kwapnee" in a transcript it means PQNine.

## Ingesting a new session

Run from the repo root (normally `C:\\GetAroundBoys`).

1. **Normalize the transcript.**
   ```
   python3 skill/getaround-archivist/tools/normalize_transcript.py \
     campaign/transcripts/Session_###_YYYYMMDD.docx \
     -o campaign/transcripts
   ```
   This writes the matching `.txt` next to the `.docx`. **Both get committed** — the MCP server only indexes `.txt`. Transcripts are plain text even with a `.docx` extension.
2. **Read the DM's opening recap first** — it's usually the best summary of the previous session. Then read the DM's narration (long DM turns) and substantive player turns. Skip out-of-game chatter.
3. **Write the summary** at `campaign/summaries/Session_###_YYYYMMDD.md` from `templates/session_summary.md`. Keep the naming: the MCP server reads the session number from the first number in the filename.
4. **Update every codex file the session touched.** Edit entries in place, don't append duplicates. Move items between holders, open and close threads, keep `[S#]` references. Mark anything uncertain with ⚠️ rather than guessing.
5. **Update the session index and "story so far"** in `campaign/codex/00_campaign_overview.md`.
6. **Add any new speech-to-text spellings** of names to `campaign/codex/glossary.md` (one group per line, single-word names, e.g. `Halda: Holda, Holden`).
7. **Prepend an entry** to `campaign/codex/ingest_log.md`: Added / Changed / Closed / Needs confirmation. Show this to Jake for review before committing.

## Applying corrections

Use when Jake relays facts from the table ("corrections from the table...", "the DM says...", "actually it was..."):

1. For each correction, find **every** place the fact appears. Grep `campaign/codex/` and `campaign/summaries/`: one fact often lives in the loot table, a character file, open threads, and the NPC entry.
2. Edit each occurrence in place. Remove the ⚠️ marker if the correction settles it; keep the `[S#]` reference.
3. If a correction closes a thread, move it to **Resolved** in `open_threads.md`. If it overturns something, fix the summary too.
4. Prepend an entry to `campaign/codex/ingest_log.md`:
   ```
   ## YYYY-MM-DD — Table corrections
   - Confirmed: <fact> (S#). Source: DM | table | <player>.
   - Corrected: <old> → <new> (S#). Source: ...
   - Files touched: ...
   ```
   Also strike or remove the matching item from any earlier "Needs confirmation" list.
5. Show Jake the log entry and don't commit until he says so.

**Rulings from the DM win.** Anything marked "Source: DM" beats transcript inference. If a later transcript seems to contradict a DM ruling, keep the ruling and flag the conflict. Don't silently overwrite it.

## Git workflow — branch, push, PR

After Jake approves the ingest (or corrections) locally:

1. **Branch** off `main`. Name it after what's being added:
   - Ingest: `ingest-s###` (e.g. `ingest-s033`).
   - Corrections: `corrections-YYYY-MM-DD`.
   ```
   git checkout main && git pull origin main
   git checkout -b ingest-s###
   ```
2. **Stage** only the files touched. For an ingest that's normally:
   ```
   git add campaign/transcripts/Session_###_YYYYMMDD.docx \
           campaign/transcripts/Session_###_YYYYMMDD.txt \
           campaign/summaries/Session_###_YYYYMMDD.md \
           campaign/codex/
   ```
   Plus `skill/getaround-archivist/tools/normalize_transcript.py` if any new aliases were added.
3. **Commit** with a short, descriptive message:
   ```
   git commit -m "Ingest Session ### (YYYY-MM-DD): <short title>"
   ```
4. **Push** the branch:
   ```
   git push -u origin ingest-s###
   ```
5. **Open the PR** to Steve's `main` with `gh`:
   ```
   gh pr create --base main --head ingest-s### \
     --title "Ingest Session ### — <title>" \
     --body "..."
   ```
   PR body: 2–4 bullet summary of what the ingest added (new NPCs, closed threads, open ⚠️ items), and the ingest-log excerpt verbatim. Return the PR URL to Jake.

Show Jake each step's commands before running the destructive ones (commit, push, PR). Never force-push, never push to `main` directly, never commit anything in `campaign/dm/`.

## Things this skill does NOT do
- Answering lore questions, writing recap emails, or producing prep sheets — those are `getaround-chronicler`.
- Reading or indexing `campaign/dm/`.
- Rewriting history (`git rebase -i`, `git push --force`, etc.).
