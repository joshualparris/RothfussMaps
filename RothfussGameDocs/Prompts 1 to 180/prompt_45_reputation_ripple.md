KKC TEXT ADVENTURE — PROMPT 45 OF 180
==========================================
Reputation Ripple
==========================================


This prompt builds directly on Prompts 1 through 44.
Do not restructure, rename, or refactor anything from those prompts.
Only add to what exists.


This prompt follows the original Phase 1 plan role for Prompt 45:
Extend the delayed reputation queue into a narrow ripple that publishes select changes to broader world state.


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


Make reputation feel like it reaches the wider world rather than only immediate NPCs.


Use the existing queue system to make one reputation change resolve into a broader world-state effect after a delay. Keep the ripple limited and mechanical.


═══════════════════════════════════════
SCOPE OF THIS PROMPT
═══════════════════════════════════════


This prompt covers:
  1. Add engine/reputationRipple.ts
  2. Define one delayed publication channel for public reputation changes
  3. Apply ripple effects when queued changes resolve
  4. Add tests for scheduled application and public exposure


This prompt does NOT cover:
  - Full rumour networking
  - Large social opinion simulation
  - Multiple dynamic social channels


═══════════════════════════════════════
NEW FILES IN THIS PROMPT
═══════════════════════════════════════


Add exactly these files:
  - src/engine/reputationRipple.ts
  - tests/reputationRipple.test.ts


Modify these existing files:
  - src/engine/reputationQueue.ts
  - src/engine/time.ts


Do not add any other files.


═══════════════════════════════════════
IMPLEMENTATION DETAILS
═══════════════════════════════════════


Implement a narrow ripple helper that transfers a queued reputation change into a broader world_state note or modifier after its delay. Keep the behaviour deterministic and limited to one public channel.


═══════════════════════════════════════
TESTS
═══════════════════════════════════════


Verify a queued change does not apply early, does apply on the correct day, and produces the expected public world-state effect.


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
  - Delayed reputation changes create a broader ripple
  - The ripple uses the existing queue infrastructure
  - No broad social simulation is added
  - All new tests pass


==========================================
END OF PROMPT 45
==========================================
