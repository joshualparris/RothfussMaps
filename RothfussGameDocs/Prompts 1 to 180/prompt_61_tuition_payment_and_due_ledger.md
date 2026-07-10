KKC TEXT ADVENTURE — PROMPT 61 OF 180
==========================================
Tuition Payment and Due Ledger
==========================================


This prompt builds directly on Prompts 1 through 60.
Do not restructure, rename, or refactor anything from those prompts.
Only add to what exists.


This prompt follows the original Phase 1 plan role for Prompt 61:
Add a deterministic tuition payment action and due-date ledger so the player can settle obligations explicitly.


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


Allow the player to pay tuition through a clear in-game command and see outstanding balances.


Track tuition due dates and amounts as ledger entries in state, then expose a payment action that reduces debt predictably. Keep the flow narrow and safe for the current University slice.


═══════════════════════════════════════
SCOPE OF THIS PROMPT
═══════════════════════════════════════


This prompt covers:
  1. Add engine/tuitionPayment.ts
  2. Track tuition obligations as due_date ledger entries in world_state
  3. Expose a pay tuition command in the parser
  4. Add tests for payment success, insufficient funds, and due ledger updates


This prompt does NOT cover:
  - Loans, interest, or credit systems
  - Open-ended financial planning
  - Any banking or investment mechanics


═══════════════════════════════════════
NEW FILES IN THIS PROMPT
═══════════════════════════════════════


Add exactly these files:
  - src/engine/tuitionPayment.ts
  - tests/tuitionPayment.test.ts


Modify these existing files:
  - src/engine/actions.ts
  - src/engine/tuitionEngine.ts
  - src/engine/state.ts
  - src/narration/renderStatus.ts


Do not add any other files.


═══════════════════════════════════════
IMPLEMENTATION DETAILS
═══════════════════════════════════════


Implement a tuition payment action that checks available currency, applies payment to the nearest due tuition entry, and updates world_state. Keep the logic deterministic and avoid any financial forecasting.


═══════════════════════════════════════
TESTS
═══════════════════════════════════════


Verify the player can pay tuition when they have enough currency, that payment reduces the due amount and removes completed ledger entries, and that payment is rejected when funds are insufficient.


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
  - The player can explicitly pay tuition
  - Due amounts are tracked in state
  - Payment results are deterministic
  - All new tests pass


==========================================
END OF PROMPT 61
==========================================
