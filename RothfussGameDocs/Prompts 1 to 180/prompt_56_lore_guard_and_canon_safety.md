KKC TEXT ADVENTURE — PROMPT 56 OF 180
==========================================
Lore Guard and Canon Safety
==========================================


This prompt builds directly on Prompts 1 through 55.
Do not restructure, rename, or refactor anything from those prompts.
Only add to what exists.


This prompt follows the original Phase 1 plan role for Prompt 56:
Strengthen canon safety by adding a narrow guard for forbidden non-canon output in narration.


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


Reduce hallucination risk by formalising a small canon-safety check in the narration path.


Implement one explicit guard that enforces existing canon constraints for named locations, NPC roles, or forbidden phrases. Keep the guard narrow and deterministic.


═══════════════════════════════════════
SCOPE OF THIS PROMPT
═══════════════════════════════════════


This prompt covers:
  1. Add engine/canonGuard.ts
  2. Apply the guard in narration rendering or NPC response selection
  3. Add tests for forbidden and allowed text


This prompt does NOT cover:
  - New lore or content expansion
  - General hallucination detection
  - External model validation


═══════════════════════════════════════
NEW FILES IN THIS PROMPT
═══════════════════════════════════════


Add exactly these files:
  - src/engine/canonGuard.ts
  - tests/canonGuard.test.ts


Modify these existing files:
  - src/narration/localNarrator.ts
  - src/narration/renderLocation.ts


Do not add any other files.


═══════════════════════════════════════
IMPLEMENTATION DETAILS
═══════════════════════════════════════


Implement a small guard that validates output fragments against a fixed canon registry or disallowed list. Use it to reject known bad outputs rather than to attempt general hallucination filtering.


═══════════════════════════════════════
TESTS
═══════════════════════════════════════


Verify forbidden non-canon phrases are rejected and valid canonical phrases are allowed.


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
  - A canon safety guard exists
  - It is narrow and explicit
  - It prevents known bad outputs without blocking valid text
  - All new tests pass


==========================================
END OF PROMPT 56
==========================================
