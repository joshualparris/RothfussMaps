KKC TEXT ADVENTURE — PROMPT 74 OF 180
==========================================
Peer Request Scene
==========================================


This prompt builds directly on Prompts 1 through 73.
Do not restructure, rename, or refactor anything from those prompts.
Only add to what exists.


This prompt follows the original Phase 1 plan role for Prompt 74:
Add a narrow student request scene from Simmon or Wilem that reflects prior progress and offers a small, fixed choice.


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


Introduce one small social beat that makes the University cast feel reactive without branching into a quest system.


Trigger a short request scene dependent on a recent event or world_state note. Keep the interaction fixed and the outcome deterministic.


═══════════════════════════════════════
SCOPE OF THIS PROMPT
═══════════════════════════════════════


This prompt covers:
  1. Add engine/peerRequest.ts
  2. Trigger the scene once after a relevant completed event
  3. Record the response outcome in world_state
  4. Add tests for each scene variant


This prompt does NOT cover:
  - Full companion relationship arcs
  - Open-ended choice trees
  - Dynamic NPC quest systems


═══════════════════════════════════════
NEW FILES IN THIS PROMPT
═══════════════════════════════════════


Add exactly these files:
  - src/engine/peerRequest.ts
  - tests/peerRequest.test.ts


Modify these existing files:
  - src/engine/eventEngine.ts
  - src/engine/state.ts
  - src/narration/localNarrator.ts


Do not add any other files.


═══════════════════════════════════════
IMPLEMENTATION DETAILS
═══════════════════════════════════════


Implement one fixed request scene with deterministic text variants based on a prior event result. Keep the scene short and limited to one NPC.


═══════════════════════════════════════
TESTS
═══════════════════════════════════════


Verify the scene triggers after the right event and that the text variant matches the prior world_state.


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
  - A peer request scene exists
  - It is based on prior progress
  - The result is deterministic
  - All new tests pass


==========================================
END OF PROMPT 74
==========================================
