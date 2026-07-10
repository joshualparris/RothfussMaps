KKC TEXT ADVENTURE — PROMPT 42 OF 180
==========================================
NPC Trust Reaction Layer
==========================================


This prompt builds directly on Prompts 1 through 41.
Do not restructure, rename, or refactor anything from those prompts.
Only add to what exists.


This prompt follows the original Phase 1 plan role for Prompt 42:
Introduce simple NPC reaction variation based on academic and social reputation bands.


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


Make key NPC responses feel more responsive to state without adding a full relationship simulation.


Implement compact reaction bands for one or two core NPCs and wire them into existing NPC response rendering. Keep the behavior narrow, deterministic, and limited to the current cast.


═══════════════════════════════════════
SCOPE OF THIS PROMPT
═══════════════════════════════════════


This prompt covers:
  1. Add engine/npcReactionRules.ts
  2. Define reputation-based response modifiers for selected NPCs
  3. Wire the rule set into existing NPC rendering or response helpers
  4. Add tests for low, neutral, and trusted response variants


This prompt does NOT cover:
  - Complete NPC attitude simulation
  - New NPCs beyond the MVP cast
  - Dynamic emotion or affliction systems


═══════════════════════════════════════
NEW FILES IN THIS PROMPT
═══════════════════════════════════════


Add exactly these files:
  - src/engine/npcReactionRules.ts
  - tests/npcReactionRules.test.ts


Modify these existing files:
  - src/engine/npcEngine.ts
  - src/narration/renderLocation.ts


Do not add any other files.


═══════════════════════════════════════
IMPLEMENTATION DETAILS
═══════════════════════════════════════


Implement one small reaction rule module that maps reputation bands to response modifiers or flavour lines. Existing NPC infrastructure should consult this module rather than hardcoded replies. Keep the rule set compact and limited to the current MVP cast.


═══════════════════════════════════════
TESTS
═══════════════════════════════════════


Verify the same NPC yields a colder response under low reputation, a neutral response at mid-range, and a warmer response when trust is high.


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
  - NPC responses vary with reputation
  - Reaction logic is centralised
  - The behaviour remains narrow and deterministic
  - All new tests pass


==========================================
END OF PROMPT 42
==========================================
