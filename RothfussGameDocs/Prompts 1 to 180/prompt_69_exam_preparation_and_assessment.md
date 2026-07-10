KKC TEXT ADVENTURE — PROMPT 69 OF 180
==========================================
Exam Preparation and Assessment
==========================================


This prompt builds directly on Prompts 1 through 68.
Do not restructure, rename, or refactor anything from those prompts.
Only add to what exists.


This prompt follows the original Phase 1 plan role for Prompt 69:
Add a narrow exam event that assesses study, attendance, and readiness to produce a deterministic outcome.


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


Introduce a small academic assessment event that rewards preparation and attendance in a predictable way.


Define a single exam event with a fixed pass/fail outcome based on prior study score, attendance, and readiness. Keep the event small and avoid any broader grading system.


═══════════════════════════════════════
SCOPE OF THIS PROMPT
═══════════════════════════════════════


This prompt covers:
  1. Add engine/examEvent.ts
  2. Define pass/fail conditions based on study and attendance
  3. Render a concise exam result and record it in world_state
  4. Add tests for exam outcomes


This prompt does NOT cover:
  - Detailed gradebook mechanics
  - Open-ended exam question generation
  - Multiple subject exams


═══════════════════════════════════════
NEW FILES IN THIS PROMPT
═══════════════════════════════════════


Add exactly these files:
  - src/engine/examEvent.ts
  - tests/examEvent.test.ts


Modify these existing files:
  - src/engine/eventEngine.ts
  - src/engine/studyAction.ts
  - src/engine/attendance.ts
  - src/narration/localNarrator.ts


Do not add any other files.


═══════════════════════════════════════
IMPLEMENTATION DETAILS
═══════════════════════════════════════


Implement an exam event with a deterministic evaluation function that considers study_score, attendance flags, and current readiness. Store the result for later reference.


═══════════════════════════════════════
TESTS
═══════════════════════════════════════


Verify a well-prepared player passes, a poorly prepared player fails, and the event result is stored correctly.


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
  - An exam event exists
  - It evaluates deterministically
  - The player can see the result
  - All new tests pass


==========================================
END OF PROMPT 69
==========================================
