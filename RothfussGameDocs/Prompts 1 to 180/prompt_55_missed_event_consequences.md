KKC TEXT ADVENTURE — PROMPT 55 OF 180
==========================================
Missed Event Consequences
==========================================


This prompt builds directly on Prompts 1 through 54.
Do not restructure, rename, or refactor anything from those prompts.
Only add to what exists.


This prompt follows the original Phase 1 plan role for Prompt 55:
Add explicit, modest penalties for skipping major scheduled events.


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


Make failing to attend key University events meaningful without creating a harsh failure state.


When the player misses a due event such as a tuition hearing or audition, apply a small deterministic cost or reputation penalty. Do not invent a complex failure story.


═══════════════════════════════════════
SCOPE OF THIS PROMPT
═══════════════════════════════════════


This prompt covers:
  1. Add engine/missedEventChecks.ts
  2. Detect missed required events when the day advances
  3. Apply modest consequences for missed events
  4. Add tests for attendance and missed-event penalties


This prompt does NOT cover:
  - Elaborate failure story branches
  - Alternate event paths
  - Multiple variable outcomes beyond the penalty


═══════════════════════════════════════
NEW FILES IN THIS PROMPT
═══════════════════════════════════════


Add exactly these files:
  - src/engine/missedEventChecks.ts
  - tests/missedEventChecks.test.ts


Modify these existing files:
  - src/engine/time.ts
  - src/engine/eventEngine.ts


Do not add any other files.


═══════════════════════════════════════
IMPLEMENTATION DETAILS
═══════════════════════════════════════


Implement a missed-event checker that runs when day advances. If a required event was due and not completed, apply a small reputation or world_state penalty. Keep the penalty fixed and predictable.


═══════════════════════════════════════
TESTS
═══════════════════════════════════════


Verify the penalty triggers for a missed event, does not trigger when attended, and does not fire outside due days.


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
  - Missed events have a deterministic consequence
  - Penalties are modest and clear
  - No complex failure branch is added
  - All new tests pass


==========================================
END OF PROMPT 55
==========================================
