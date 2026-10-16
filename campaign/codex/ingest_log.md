# Ingest Log

One entry per ingest: what changed in the codex. Newest first.

## 2026-10-15 — Normalizer bugfix + S33–S35 full re-ingest

Jake noticed each of the three S33–S35 summaries only covered the first ~half of its session. **Root cause:** `skill/getaround-archivist/tools/normalize_transcript.py`'s HDR regex matched only `MM:SS` timestamps and silently rejected `H:MM:SS` ones. Teams switches from `MM:SS` to `H:MM:SS` at the 1-hour mark, so every speaker header past that point was treated as a text line of the previous speaker's turn. The entire back half of each session collapsed into a single trailing mega-line (40K, 55K and 69K characters for S33/S34/S35 respectively).

- **Normalizer fix:** `HDR` now matches `\d+:\d+(:\d+)?` — a one-char change, backward compatible with the old `MM:SS` format.
- Re-normalized all three `.txt` transcripts:
  - S33: 787 → **1,178** lines
  - S34: 634 → **1,142** lines
  - S35: 827 → **1,577** lines
- Full re-ingest of the back halves. **Rewrote all three summaries**:
  - `Session_033_20261001.md` — added the Northfield / North Shield House inn evening, Tordrug's "Mona Lisa" book-lore on Constantori's portrait, Fic buying intel at the inn (learned about Carl + Haravin at the Harvest Inn), PQNine commissioning a stickman portrait from Carl at the Talking Troll, Baron pitching the "Sister Halda stinks" slander campaign.
  - `Session_034_20261008.md` — unchanged on the Tribor Travelers brawl and the Harvest Inn front half; expanded the back half (previously added via a two-pass workaround) and corrected the stable location (Baron slept in the cart at Northfield's stable, not the Talking Troll's).
  - `Session_035_20261014.md` — replaced the "Baron asks about a vault" cliffhanger with the full HQ break-in: Elix's full charmed interrogation ("no vault," "Dusk's office," "no secret door into basement — only between the two basements"), **Tordrug killed Elix with Shocking Grasp when the charm wore off** (not released), the roadside burial with PQNine's pewter mug + Minor Illusion crucifix, the party-wide infiltration setup (Hairy-as-Elix, Tordrug-as-Grinky, Invisibility 3rd on PQNine/Baron, Pass Without Trace, Fic's Cloak of Elvenkind), and the entire HQ sweep: front office (G10) coin box, receiving/goods room (G12) coffin, shared bedroom, quartermaster office (took the guild ledger), Dusk's round tower bedroom + two staircases, and the Tower Peak with the sentient Constantori's Portrait that started **screaming** for help as the session cut.
- **NPCs added or updated:** Courtney (Northfield innkeeper), Carl (Tribor artist, illiterate), "Dawn" (⚠️ Dusk's bedmate, likely a pet name), Agile Hand balcony lookout and quartermaster-office guard, two sleeping HQ members. **Elix the Saint updated to ⚫ dead** (killed by Tordrug after charm wore off). **Guildmaster Dusk updated** — confirmed female, has lover named "Dawn" ⚠️, lives in a round bedroom with staircases to the Tower Peak above (which was NOT on Grinky's floor-plan).
- **Loot updated:** Hairy kept Elix's cheap brass wedding ring (⚠️ Elix had a wife) and the worn wooden Saint figurine; party took 2 HQ wall-hook keys and the leather-bound guild ledger (Hairy carries); 15 cp + 11 sp from the HQ coin box (2 sp each distributed); PQNine's Tipsy Tankard pewter mug was buried with Elix.
- **Threads:** closed "Elix the Saint — the charmed captive" (he's dead); replaced "Agile Hand HQ — the break-in" with an **in-progress** version (party inside, portrait screaming, Dusk awake, guards knocking); added "The screaming portrait," "Guildmaster Dusk is awake," and "Elix's wife" threads.
- **Overview:** "story so far" S33–S35 paragraph rewritten to cover the whole arc through the HQ Tower Peak. "Where we left off" replaced with the portrait-screaming cliffhanger.
- **New glossary entries** for Carl, Dawn, Dusk, Elix (expanded), Northfield, Hairy's "Perry" alias at Full Hammer.
- **Needs confirmation (new):** whether "Dawn" is a real name or a pet name; whether the HQ wall-hook keys open specific interior doors; the Agile Hand ledger's contents; whether the earth-encrusted coffin in the receiving/goods room matters; whether Elix's wife is a plot hook or incidental; S35 title — Jake OK'd "The Tipsy Tankard Chase" early but the HQ break-in is now the bigger beat (candidate rename: "The Screaming Portrait").

## 2026-10-14 — Sessions 33–35

- **Added:** `summaries/Session_033_20261001.md`, `summaries/Session_034_20261008.md`, `summaries/Session_035_20261014.md`.
- **NPCs added:** Haravin Dar Dragon (Harvest Inn / Westbridge, "Dealer in Fine Arts"); Idrissa Caramorte (Cognoscenti Esoterica agent, hired the party for 2,000 gp); Grink "Grinky" Brithwort (Agile Hand junior, charmed by Tordrug); Jimmy Two Pouch (gnome courier); Guildmaster Dusk (Agile Hand); Elix the Saint (Dusk lieutenant, captured S35); Jaymont the Sinner (Agile Hand spy, unseen); Wish ⚠️ (Agile Hand, unseen); Deski Kwan ⚠️ (artist of the portrait, spelling unverified); Dayani Gristhorne (late commissioner of the portrait); Full Hammer (Tribor smith); Narth Tezran & Alestra Algar (Lion's Share / Lion Shield Coster, Tribor); Erlam Stock Spool (Tribor Travelers manager, named not met); Tribor Travelers clerk (unnamed, dropped unconscious by Hairy); Westbridge beggar; Tipsy Tankard bartenders; river bottle woman; piano woman and piano man.
- **Locations added:** Westbridge (farming village on the Long Road); Harvest Inn; Shrine of Chauntea (Westbridge); Idrissa's barn (abandoned farm by the giant oak, south-east of Westbridge); Agile Hand HQ (not yet entered); Tipsy Tankard (hamlet tavern); Full Hammer's Forge (Tribor); The Lion's Share (Tribor); Tribor Travelers (Tribor caravan yard); The Pleasing Ladder, The Tribor Arms (Tribor, referenced); Yartar (referenced).
- **Loot added:** heavy brass 3-tooth master key to Agile Hand HQ (Fic, on leather cord); Grinky's two-sided route+floor-plan map (Tordrug); 2 daggers (Fic, Tordrug); unclaimed scimitar / brass wedding ring / wooden Saint figurine from Elix; Hairy's chain-link necklace with Sisters-of-the-Vale insignia pieces (worked in by Full Hammer); corked bottle + anonymous "I know what you did" note (Tordrug); PQNine's Tipsy Tankard pewter mug.
- **Gold changes:** Tordrug +101 gp (sold Lord's Alliance longsword 6 gp + splint 95 gp in Tribor), −3 gp (Harvest Inn room), −1 gp (Haravin breakfast tip); Hairy +10 gp + necklace (chainmail), +4 gp (shortsword), −1 gp (barge), −2 gp (Jordan tip), −5 gp (Tribor Travelers clerk, lost); PQNine −10 gp (Westbridge beggar), −1 gp (Tipsy Tankard mug), carried his Carl handbill portrait; Fic −~1 gp 10 sp (burritos + drinks + Haravin tip); each player +4 gp 1 sp (Elix loot split).
- **Threads opened:** Agile Hand HQ infiltration (next session's objective); Guildmaster Dusk (knows where the portrait is); Elix the Saint's fate (charmed captive); Tribor warrant / bailiff's posse after the caravan-yard brawl; the "I know what you did" note; Jimmy Two Pouch's loyalty ⚠️; Haravin's unsettling "burrito-watching" interest ⚠️; Lion Shield Coster franchising into Tribor.
- **Threads advanced:** Constantori's portrait — now a hired contract (2,000 gp from Cognoscenti Esoterica), known to be sentient, painted by Deski Kwan ⚠️, commissioned by the late Dayani Gristhorne, held at the Agile Hand HQ (tower or basement); Westbridge destination reached; Haravin? question mark on Halda's map resolved — he was the party's contact to Idrissa, not an owner of the portrait; Shadow Strider training still needs a bigger city than Tribor; Duke Hallebrand targeting deferred until Shadow Strider is trained.
- **Threads closed:** none this ingest.
- **Normalizer updated:** `skill/getaround-archivist/tools/normalize_transcript.py` now auto-detects real Word `.docx` (ZIP magic bytes) via `python-docx` and parses the Teams real-docx format (`Name   HH:MM` on its own line, text on following lines). VTT and the older plain-text-with-`.docx` extension still work unchanged. These three transcripts are the first ingest in the new real-docx format.
- **Needs confirmation:** spelling of Deski Kwan (artist); spelling of Dayani / Diani Gristhorne; whether Elix's shortname "Elex" or similar is preferred by DM; whether Wish, Jaymont and Dusk are the full roster of master-key holders or just the ones Grinky named; whether Erlam Stock Spool is the Tribor Travelers owner or just the manager; the identity of the sender of the "I know what you did" note; exact nature of the Lion Shield Coster's franchise push (⚠️ worldbuilding, not plot-blocking).

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
