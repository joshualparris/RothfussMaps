KKC TEXT ADVENTURE — PROMPT 52 OF 180
==========================================
Tuition Reminder and Debt Tracking
==========================================


This prompt builds directly on Prompts 1 through 51.
Do not restructure, rename, or refactor anything from those prompts.
Only add to what exists.


This prompt follows the original Phase 1 plan role for Prompt 52:
Make tuition obligations explicit by tracking due dates and reminding the player when payment is required.


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


Give the player a clear tuition reminder mechanic instead of hidden or unexplained penalties.


Track tuition as a due date ledger item in world state and surface reminders or small overdue notes during the morning pass.


═══════════════════════════════════════
SCOPE OF THIS PROMPT
═══════════════════════════════════════


This prompt covers:
  1. Add engine/tuitionReminder.ts
  2. Record tuition due dates in world_state
  3. Add reminder text to status or morning pass
  4. Add tests for near-due and overdue conditions


This prompt does NOT cover:
  - A full loan or banking system
  - Open-ended financial planning
  - Large economy expansions


═══════════════════════════════════════
NEW FILES IN THIS PROMPT
═══════════════════════════════════════


Add exactly these files:
  - src/engine/tuitionReminder.ts
  - tests/tuitionReminder.test.ts


Modify these existing files:
  - src/engine/tuitionEngine.ts
  - src/engine/time.ts
  - src/narration/renderStatus.ts


Do not add any other files.


═══════════════════════════════════════
IMPLEMENTATION DETAILS
═══════════════════════════════════════


Implement a tuition tracker with due_date and amount. When the due date is near or passed, add a reminder line to the morning pass or status output. Apply only a small deterministic overdue marker.


═══════════════════════════════════════
TESTS
═══════════════════════════════════════


Verify a near-due reminder appears, overdue notification appears when the date passes, and no reminder is shown when on time.


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
  - Tuition due dates are tracked
  - The player receives reminders
  - Overdue status is deterministic
  - All new tests pass


==========================================
END OF PROMPT 52
==========================================
