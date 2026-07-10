KKC TEXT ADVENTURE — PROMPT 64 OF 180
==========================================
Rumour Ripple Integration
==========================================


This prompt builds directly on Prompts 1 through 63.
Do not restructure, rename, or refactor anything from those prompts.
Only add to what exists.


This prompt follows the original Phase 1 plan role for Prompt 64:
Connect the reputation ripple system to the rumour pool so world-state changes can be reflected in gossip.


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


Make reputation changes influence the rumour system in a small, deterministic way.


When the reputation ripple resolves, publish a related rumour or public reaction note. Keep the integration focused and avoid full social networking.


═══════════════════════════════════════
SCOPE OF THIS PROMPT
═══════════════════════════════════════


This prompt covers:
  1. Add engine/rumourRipple.ts
  2. Publish a rumour when a delayed reputation change resolves
  3. Ensure the rumour remains canon-safe and deterministic
  4. Add tests for rumour publication timing


This prompt does NOT cover:
  - Wide rumour networks or reputation markets
  - Open-ended multiplayer-style gossip systems
  - Non-deterministic rumour generation


═══════════════════════════════════════
NEW FILES IN THIS PROMPT
═══════════════════════════════════════


Add exactly these files:
  - src/engine/rumourRipple.ts
  - tests/rumourRipple.test.ts


Modify these existing files:
  - src/engine/reputationRipple.ts
  - src/engine/rumourPool.ts
  - src/engine/time.ts


Do not add any other files.


═══════════════════════════════════════
IMPLEMENTATION DETAILS
═══════════════════════════════════════


Implement a helper that turns a resolved reputation queue item into one fixed rumour note. Keep the published rumour narrow, canned, and limited to the current MVP cast.


═══════════════════════════════════════
TESTS
═══════════════════════════════════════


Verify the rumour is published only when the reputation change resolves and that it reflects the correct reputation band.


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
  - Reputation ripple publishes a rumour
  - The integration is deterministic
  - The rumour stays within MVP scope
  - All new tests pass


==========================================
END OF PROMPT 64
==========================================
