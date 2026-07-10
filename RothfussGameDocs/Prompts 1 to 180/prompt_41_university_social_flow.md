KKC TEXT ADVENTURE — PROMPT 41 OF 180
==========================================
University Social Flow
==========================================


This prompt builds directly on Prompts 1 through 40.
Do not restructure, rename, or refactor anything from those prompts.
Only add to what exists.


This prompt follows the original Phase 1 plan role for Prompt 41:
Add a modest social interaction layer to the University day loop that uses existing reputation and NPC presence data.


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


Make the daily University experience feel more social by triggering a small in-world interaction or reaction during the morning/evening pass.


Use existing reputation bands and NPC presence to create a deterministic social hook. Keep the scope narrow: one or two extra social lines per day, no branching dialogue trees or new AI-driven chat systems.


═══════════════════════════════════════
SCOPE OF THIS PROMPT
═══════════════════════════════════════


This prompt covers:
  1. Add engine/socialFlow.ts
  2. Define a small set of social triggers based on location, time of day, and current NPC trust bands
  3. Invoke the social flow during the current morning/evening loop
  4. Add tests for conditions that should and should not trigger the social hook


This prompt does NOT cover:
  - Full NPC dialogue trees
  - Open-ended Gemini or chat-based social systems
  - Large new NPC relationship frameworks


═══════════════════════════════════════
NEW FILES IN THIS PROMPT
═══════════════════════════════════════


Add exactly these files:
  - src/engine/socialFlow.ts
  - tests/socialFlow.test.ts


Modify these existing files:
  - src/engine/time.ts
  - src/engine/state.ts
  - src/narration/localNarrator.ts


Do not add any other files.


═══════════════════════════════════════
IMPLEMENTATION DETAILS
═══════════════════════════════════════


Implement a deterministic socialFlow helper that inspects the current location, current reputation bands, and present NPCs, then returns a short narrative reaction or starter line. Call it once during the existing day loop so the player feels a small social response from the world. Keep the logic compact and limited to the current MVP cast.


═══════════════════════════════════════
TESTS
═══════════════════════════════════════


Add tests that assert a social line occurs when a satisfying NPC/trust condition is met, and that no extra social line occurs when the conditions are not met.


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
  - A social flow hook exists in the University day loop
  - The social hook is deterministic and reputation-aware
  - No broad new social engine is introduced
  - All new tests pass


==========================================
END OF PROMPT 41
==========================================
