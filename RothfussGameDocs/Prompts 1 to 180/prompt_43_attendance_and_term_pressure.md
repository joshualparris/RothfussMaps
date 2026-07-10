KKC TEXT ADVENTURE — PROMPT 43 OF 180
==========================================
Attendance and Term Pressure
==========================================


This prompt builds directly on Prompts 1 through 42.
Do not restructure, rename, or refactor anything from those prompts.
Only add to what exists.


This prompt follows the original Phase 1 plan role for Prompt 43:
Add a lightweight attendance model so missing class or study windows produces a small, understandable consequence.


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


Connect daily attendance to tuition and academic standing in a simple deterministic way.


Define class and study windows using current day/time state. Apply a modest consequence when the player misses attendance during those windows. Do not add a full timetable or gradebook.


═══════════════════════════════════════
SCOPE OF THIS PROMPT
═══════════════════════════════════════


This prompt covers:
  1. Add engine/attendance.ts
  2. Define class windows and missed-attendance rules
  3. Update tuition or academic standing when attendance is missed
  4. Add tests for attending, missing, and out-of-window behaviour


This prompt does NOT cover:
  - Full timetable or lecture simulation
  - Class-specific lecture content
  - Detailed grade mechanics


═══════════════════════════════════════
NEW FILES IN THIS PROMPT
═══════════════════════════════════════


Add exactly these files:
  - src/engine/attendance.ts
  - tests/attendance.test.ts


Modify these existing files:
  - src/engine/time.ts
  - src/engine/tuitionEngine.ts
  - src/narration/renderStatus.ts


Do not add any other files.


═══════════════════════════════════════
IMPLEMENTATION DETAILS
═══════════════════════════════════════


Implement a deterministic attendance model with defined class windows. When the player does not attend the relevant class or study window, apply a small academic standing penalty or tuition pressure note. Keep the effect modest and predictable.


═══════════════════════════════════════
TESTS
═══════════════════════════════════════


Verify attendance is tracked during the window, penalties apply only when the player misses a session, and no penalty occurs outside class time.


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
  - Attendance windows exist
  - Missed attendance produces a visible consequence
  - The system remains simple and deterministic
  - All new tests pass


==========================================
END OF PROMPT 43
==========================================
