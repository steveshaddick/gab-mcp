# Ingest Log

One entry per ingest: what changed in the codex. Newest first.

## 2026-10-01 — Adapted to the gab-mcp repo layout
- Added a normalized `.txt` next to every transcript `.docx` (the server only indexes `.txt`). Transcripts are now searchable via `search_campaign(include_transcripts=True)` and `get_transcript_excerpt`.
- Added `codex/glossary.md`: spelling groups for speech-to-text mishearings (PQNine/Kwapnee/Quapny…, Krokilmar/Crocilmar…, Halda/Holda…).
- Skill v3: paths under `campaign/`, the MCP tool names, the read-only connector vs. local clone, the glossary step, and `.txt` output in ingest. Keeps Steve's "always spell it PQNine" rule.
- `CLAUDE.md` layout section updated to match the real file names; `.gitignore` now ignores `.obsidian/` and `campaign.db`.

## 2026-09-28 — Skill v2
- The skill no longer bundles its own copy of the normalizer. `tools/normalize_transcript.py` in this repo is the single source of truth for speaker aliases.
- Added a "Applying corrections" procedure to the skill (log format with a Source field; DM rulings win).
- Players need to re-install the skill only when the procedure changes, not when sessions or aliases are added.

## 2026-09-28 — Session 32 (first "weekly" ingest)
- **Added:** `summaries/Session_032_20260924.md`.
- **NPCs:** Sister Halda updated (second ambush, stripped again, Constantori orders); new entries for Constantori, Haravin?, and the Cognoscenti Esoterica.
- **Loot:** Halda's plate set, sword, notebook, key and sealed order; tracker gear; potions; lead-lined artifact bags; +110 gp.
- **Threads opened:** Constantori's portrait (Westbridge). Halda round 3.
- **Needs confirmation:** who carries the notebook and the key; the name "Haravin"; how the loot was split.

## 2026-09-28 — Sessions 21–31
- **Added:** summaries for S21–S24 and S26–S31, plus a placeholder for S25 (no transcript; rebuilt from the S26 recap).
- **NPCs added:** Old Brindlewick, Nix Riddlestone, Mayor Braid Broadfoot, Sergeant Cragknuckle, **Fizzlewidget Tinklebottom**, the Abbot, the escaped cannibals, the grieving father, and the Callarduran priest.
- **Closed:** the silver run; Little Lockford (gear in the lava, paid); **PQNine's missing memory** (it was Fizzlewidget).
- **Opened:** the escaped cannibals; Fizzlewidget's fate; PQNine's gear sketch; Hairy's mother's voice.
- **Needs confirmation:** Fizzlewidget's fate after he was subdued; what else was in the onyx box; the Broadfoot payment amount; the cannibals' names; whether the figure "killed weeks earlier" in S29 was Nix or someone else; what the S24 quilt and dragon-lantern sign mean; which job Nindle brought in S21 ("Little Lock" = Little Lockford?).

## 2026-09-28 — Sessions 11–20
- **Added:** summaries for S11, S12 and S14–S20, plus a placeholder for S13 (no transcript).
- **NPCs added:** Norris Inker, Barlow Lundegger / Bilaro Quist, Varen Axebreaker, Bethra, Prisoner 13, the Warden + Vlax, Vessa Orin, Duke Hallebrand, Borum Feldhand, the Merckmire Hatchling, and minor figures.
- **Changed:** Sister Halda → hostile (the Sisters of the Vale are hunting the party). Marcos → friendly. Vasil → strained. Verity revealed as Varen's emissary. The Ledger moved from PQNine to Marlo.
- **Closed:** the egg (hatchling killed), the Codex retrieval, the Ledger, the Prisoner 13 job.
- **Opened:** the South Ward fire (600 dead), the Sisters of the Vale, the Axebreaker vault payout, the deep-gnome machines, Cormier College, the Font of Knowledge appraisal, Duke Hallebrand (Hairy).
- **Needs table confirmation:** what happened in S13 (Halda fight details, how the fire started, Verity payout); where the Codex is now; which Bag of Holding burst; Varen item picks #2–3; what was sold to Norris; Prisoner 13's real name spelling; the Warden's name; whether Jeff was at S14 and S20.

## 2026-09-28 — Initial build, Sessions 1–10
- Created all codex files and summaries for S1–S10 from raw transcripts.
- **Needs table confirmation:** who holds Bag of Holding #2, the Black Rod, the signet ring, the +1 rapier and the eye pin. Fate of the Erinyes statuette. Whether the Zala star-map deal happened. Whether Elra's backpack was retrieved. Who "Curtis" is.
- **Spelling to confirm:** Krokilmar / Crocilmar / Procilmar.
