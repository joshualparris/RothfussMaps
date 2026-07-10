KKC TEXT ADVENTURE — PROMPT 60 OF 180
==========================================
World State Manager Expansion
==========================================


This prompt builds directly on Prompts 1 through 59.
Do not restructure, rename, or refactor anything from those prompts.
Only add to what exists.


This prompt follows the original Phase 1 plan role for Prompt 60:
Expand the world state manager to persist event completion, scheduled obligations, and reputation ripple state.


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


Give the game a more explicit persistent state model for the small academic/social loop.


Record the new state items introduced by previous prompts in the world state manager and centralise their persistence.


═══════════════════════════════════════
SCOPE OF THIS PROMPT
═══════════════════════════════════════


This prompt covers:
  1. Add engine/worldStateExtensions.ts
  2. Persist event completion flags and obligation due dates
  3. Wire the world state manager to use these fields
  4. Add tests for world state reads and writes


This prompt does NOT cover:
  - Full save/load redesign
  - Non-University era systems
  - New database architectures


═══════════════════════════════════════
NEW FILES IN THIS PROMPT
═══════════════════════════════════════


Add exactly these files:
  - src/engine/worldStateExtensions.ts
  - tests/worldStateExtensions.test.ts


Modify these existing files:
  - src/engine/state.ts
  - src/engine/time.ts
  - src/engine/eventEngine.ts


Do not add any other files.


═══════════════════════════════════════
IMPLEMENTATION DETAILS
═══════════════════════════════════════


Implement an explicit world state extension module for the new event, schedule, and reputation flags introduced earlier. Centralise reads and writes so state management remains deterministic.


═══════════════════════════════════════
TESTS
═══════════════════════════════════════


Verify persisted completed events, scheduled obligations, and reputation ripple flags can be read and written correctly.


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
  - World state manager persists the new fields
  - The new state model is centralised
  - All new tests pass


==========================================
END OF PROMPT 60
==========================================
