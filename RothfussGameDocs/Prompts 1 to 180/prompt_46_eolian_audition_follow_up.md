KKC TEXT ADVENTURE — PROMPT 46 OF 180
==========================================
Eolian Audition Follow-Up
==========================================


This prompt builds directly on Prompts 1 through 45.
Do not restructure, rename, or refactor anything from those prompts.
Only add to what exists.


This prompt follows the original Phase 1 plan role for Prompt 46:
Add proper follow-up framing and consequences after the first Eolian audition event.


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


Make the first audition feel like a real event with results, feedback, and a next-day response.


Record the audition outcome and trigger a deterministic follow-up event or note on the following day. Keep the focus on one audition and its immediate sequel.


═══════════════════════════════════════
SCOPE OF THIS PROMPT
═══════════════════════════════════════


This prompt covers:
  1. Add engine/auditionResults.ts
  2. Store audition outcomes in world_state
  3. Trigger a follow-up event or social note after the audition
  4. Add tests for success and failure outcomes


This prompt does NOT cover:
  - A full Eolian storyline
  - Open-ended music performance mechanics
  - Multiple audition routes


═══════════════════════════════════════
NEW FILES IN THIS PROMPT
═══════════════════════════════════════


Add exactly these files:
  - src/engine/auditionResults.ts
  - tests/auditionResults.test.ts


Modify these existing files:
  - src/engine/eventEngine.ts
  - src/engine/musicEngine.ts
  - src/engine/state.ts


Do not add any other files.


═══════════════════════════════════════
IMPLEMENTATION DETAILS
═══════════════════════════════════════


Implement an audition result handler that evaluates the player's performance and stores the result in world_state. Use a follow-up hook to render a natural next-day reaction or small consequence.


═══════════════════════════════════════
TESTS
═══════════════════════════════════════


Verify a successful audition result is recorded, a failed result is recorded, and the follow-up occurs on the next day.


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
  - The first Eolian audition has a follow-up
  - Outcome is stored and reused
  - The world responds predictably to the result
  - All new tests pass


==========================================
END OF PROMPT 46
==========================================
