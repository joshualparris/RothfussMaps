KKC TEXT ADVENTURE — PROMPT 65 OF 180
==========================================
Campus Availability Schedule
==========================================


This prompt builds directly on Prompts 1 through 64.
Do not restructure, rename, or refactor anything from those prompts.
Only add to what exists.


This prompt follows the original Phase 1 plan role for Prompt 65:
Add a narrow availability schedule for key NPCs and activities based on the in-game day/time.


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


Make frequent University actions feel more grounded by limiting them to plausible windows and NPC availability.


Define availability for one or two NPCs or actions and use the current schedule engine to block or allow them. Keep the feature simple and deterministic.


═══════════════════════════════════════
SCOPE OF THIS PROMPT
═══════════════════════════════════════


This prompt covers:
  1. Extend engine/schedule.ts with NPC availability rules
  2. Define availability windows for one or two core NPCs
  3. Prevent actions when the NPC is unavailable
  4. Add tests for availability behaviour


This prompt does NOT cover:
  - Large NPC scheduling systems
  - Full campus timetable management
  - Dynamic availability based on many unrelated conditions


═══════════════════════════════════════
NEW FILES IN THIS PROMPT
═══════════════════════════════════════


Add exactly these files:
  - tests/availabilitySchedule.test.ts


Modify these existing files:
  - src/engine/schedule.ts
  - src/engine/npcEngine.ts
  - src/narration/renderLocation.ts


Do not add any other files.


═══════════════════════════════════════
IMPLEMENTATION DETAILS
═══════════════════════════════════════


Implement a small availability helper in schedule.ts that returns whether an NPC or activity is available in the current time slice. Use it in action resolution to block unavailable cases.


═══════════════════════════════════════
TESTS
═══════════════════════════════════════


Verify a sample NPC is only available during the defined window and that actions fail cleanly when it is not.


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
  - NPC availability exists
  - The system is deterministic
  - The scope remains narrow
  - All new tests pass


==========================================
END OF PROMPT 65
==========================================
