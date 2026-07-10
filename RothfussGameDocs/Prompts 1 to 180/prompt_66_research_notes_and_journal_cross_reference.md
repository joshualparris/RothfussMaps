KKC TEXT ADVENTURE — PROMPT 66 OF 180
==========================================
Research Notes and Journal Cross-Reference
==========================================


This prompt builds directly on Prompts 1 through 65.
Do not restructure, rename, or refactor anything from those prompts.
Only add to what exists.


This prompt follows the original Phase 1 plan role for Prompt 66:
Add a simple research note entry that records a Library visit and cross-references it in the player journal.


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


Give Stacks access a concrete reward by recording research notes the player can review later.


When research access succeeds, add a short note to world_state and expose it through the journal or status. Keep the entry factual and narrow.


═══════════════════════════════════════
SCOPE OF THIS PROMPT
═══════════════════════════════════════


This prompt covers:
  1. Extend engine/stacksAccess.ts with note recording
  2. Record a research note in world_state
  3. Expose the note through the in-world journal
  4. Add tests for note creation and display


This prompt does NOT cover:
  - Full research or book reading systems
  - Large archives browsing
  - Complex note-taking interfaces


═══════════════════════════════════════
NEW FILES IN THIS PROMPT
═══════════════════════════════════════


Add exactly these files:
  - tests/researchNotes.test.ts


Modify these existing files:
  - src/engine/stacksAccess.ts
  - src/engine/journal.ts
  - src/engine/state.ts
  - src/narration/renderStatus.ts


Do not add any other files.


═══════════════════════════════════════
IMPLEMENTATION DETAILS
═══════════════════════════════════════


When Stacks access succeeds, append a canonical research note to the world_state journal. Ensure the note is concise and only records the fact of the visit and the topic.


═══════════════════════════════════════
TESTS
═══════════════════════════════════════


Verify a research note is stored on successful access and that it appears in the journal output.


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
  - Research notes are recorded
  - The journal displays them
  - The behaviour stays narrow
  - All new tests pass


==========================================
END OF PROMPT 66
==========================================
