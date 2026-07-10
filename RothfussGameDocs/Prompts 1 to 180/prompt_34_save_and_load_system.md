KKC TEXT ADVENTURE — PROMPT 34 OF 180
==========================================
Save and Load System
==========================================


This prompt builds directly on Prompts 1 through 33.
Do not restructure, rename, or refactor anything from those prompts.
Only add to what exists.


This prompt follows the original Phase 1 plan role for Prompt 34:
implement save/load so player_state and world_state can persist beyond the SQLite session if needed.


Current project state:
Prompts 1–20 are designed around a University-era Kvothe MVP.


Current architecture principles:
- engine owns truth
- narration never mutates state
- local deterministic path must always work
- optional Gemini path must fall back safely
- canon registry and mystery registry constrain narration
- no deep mystery resolution
- no refactors unless strictly required


Current MVP systems already planned:
- movement and location traversal
- day/time progression
- SQLite-backed player/world state
- hunger and fatigue
- tuition
- economy and currency
- inventory
- sympathy
- rumours
- Eolian / pipes
- busking at Anker’s
- reputation axes and NPC trust
- optional Gemini narration and NPC conversation
- lore guard


Current MVP focus:
- one playable era
- Kvothe only
- University + Imre slice
- grounded survival, study, work, and social consequence


═══════════════════════════════════════
HARD BANS — UNCHANGED
═══════════════════════════════════════


No Anthropic. No OpenAI. No new AI provider.
Gemini remains the only optional LLM provider in this codebase.


No web server. No frontend unless a later prompt explicitly introduces it.
No random feature sprawl.
No major refactors.
Do not invent lore.
Do not resolve mysteries.
Do not add systems outside the prompt’s stated scope.
If a referenced file does not yet exist, skip it rather than inventing around it.


═══════════════════════════════════════
ARCHITECTURE RULE — STILL ABSOLUTE
═══════════════════════════════════════


engine/* owns:
- command parsing
- movement
- access checks
- time advancement
- state mutation
- persistence
- gameplay truth


content/* owns:
- authored registries and text pools only


narration/* owns:
- prose rendering only
- prompt construction only
- fallback rendering only
- canon and mystery safety only


Narration must never mutate PlayerState.
Narration must never write to the DB.
The engine remains the source of truth.
repl.ts saves state exactly once per turn.


═══════════════════════════════════════
GOAL OF THIS PROMPT
═══════════════════════════════════════


Add explicit save/load files on top of the existing persistence model.


Keep the format simple and transparent. This is about reliability, not multiple save-slot UX.


═══════════════════════════════════════
SCOPE OF THIS PROMPT
═══════════════════════════════════════


This prompt covers:
  1. Add saveLoadEngine.ts
  2. Serialise player_state and world_state to JSON
  3. Support save and load helpers
  4. Add tests for round-trip correctness


This prompt does NOT cover:
  - Multiple save slots
  - Cloud sync
  - Encryption
  - UI save menus


═══════════════════════════════════════
NEW FILES IN THIS PROMPT
═══════════════════════════════════════


Add exactly these files:
  - src/engine/saveLoadEngine.ts
  - tests/saveLoadEngine.test.ts


Modify these existing files:
  - src/repl.ts
  - src/engine/state.ts


Do not add any other files.


═══════════════════════════════════════
IMPLEMENTATION DETAILS
═══════════════════════════════════════


Use plain JSON files with clear structure. Keep save/load explicit and testable. Do not replace the SQLite backing store; layer on top carefully.


═══════════════════════════════════════
TESTS
═══════════════════════════════════════


Add tests for save file creation, load round-trip, and graceful handling of missing files.


═══════════════════════════════════════
ARCHITECTURE REMINDERS
═══════════════════════════════════════


These rules from Prompt 1 still apply:


- narration/* never reads from or writes to the DB
- narration/* never mutates PlayerState
- engine/* owns all state changes
- repl.ts saves state exactly once per turn
- No `any` types
- No external API calls outside the optional Gemini provider
- No unused imports or files
- Add tests alongside implementation


═══════════════════════════════════════
SUCCESS CRITERIA
═══════════════════════════════════════


This prompt is complete when:
  - state can be serialised and loaded cleanly
  - round-trip preserves core fields
  - existing persistence is not broken
  - all new tests pass


==========================================
END OF PROMPT 34
==========================================
