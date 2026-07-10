KKC TEXT ADVENTURE — PROMPT 62 OF 180
==========================================
Academic Study Action
==========================================


This prompt builds directly on Prompts 1 through 61.
Do not restructure, rename, or refactor anything from those prompts.
Only add to what exists.


This prompt follows the original Phase 1 plan role for Prompt 62:
Introduce a narrow study action that increases academic standing based on deterministic effort rather than random skill checks.


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


Make studying a meaningful, trackable action that improves the player's academic condition over time.


Add a study command that records effort and boosts academic standing in a predictable way. Keep it limited to the current University systems and avoid broad RPG-style studies or stats.


═══════════════════════════════════════
SCOPE OF THIS PROMPT
═══════════════════════════════════════


This prompt covers:
  1. Add engine/studyAction.ts
  2. Track study effort using a simple numeric state field
  3. Apply study effects to academic standing or attendance outcomes
  4. Add tests for study success and diminishing returns


This prompt does NOT cover:
  - Complex learning trees or skill progressions
  - Open-ended mini-games
  - Multiple subject systems


═══════════════════════════════════════
NEW FILES IN THIS PROMPT
═══════════════════════════════════════


Add exactly these files:
  - src/engine/studyAction.ts
  - tests/studyAction.test.ts


Modify these existing files:
  - src/engine/actions.ts
  - src/engine/state.ts
  - src/engine/attendance.ts
  - src/narration/renderStatus.ts


Do not add any other files.


═══════════════════════════════════════
IMPLEMENTATION DETAILS
═══════════════════════════════════════


Implement a study helper that increments a study_score and applies that score to academic standing or exam readiness. Keep the effect deterministic and additive.


═══════════════════════════════════════
TESTS
═══════════════════════════════════════


Verify the study action increases the study score, that repeated study has predictable effects, and that the score influences related academic outcomes.


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
  - A study action exists
  - It improves academic standing predictably
  - The behaviour remains narrow and deterministic
  - All new tests pass


==========================================
END OF PROMPT 62
==========================================
