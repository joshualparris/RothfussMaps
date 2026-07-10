KKC TEXT ADVENTURE — PROMPT 38 OF 180
==========================================
Lore Guard Adversarial Tests
==========================================


This prompt builds directly on Prompts 1 through 37.
Do not restructure, rename, or refactor anything from those prompts.
Only add to what exists.


This prompt follows the original Phase 1 plan role for Prompt 38:
stress-test the lore guard with adversarial mystery-extraction attempts.


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


Verify that the structured mystery/lore guard holds under more aggressive prompts.


This is not about gameplay — it is about trust in the narration safety layer.


═══════════════════════════════════════
SCOPE OF THIS PROMPT
═══════════════════════════════════════


This prompt covers:
  1. Add adversarial lore guard tests
  2. Use multiple forbidden-mystery phrasings
  3. Verify fallback behaviour


This prompt does NOT cover:
  - New lore systems
  - New provider integrations


═══════════════════════════════════════
NEW FILES IN THIS PROMPT
═══════════════════════════════════════


Add exactly these files:
  - tests/lore_guard_adversarial.test.ts


Modify these existing files:
  - tests/loreGuard.test.ts


Do not add any other files.


═══════════════════════════════════════
IMPLEMENTATION DETAILS
═══════════════════════════════════════


Test several phrasings and indirect tries. Keep the system deterministic and conservative.


═══════════════════════════════════════
TESTS
═══════════════════════════════════════


This prompt is itself the test-writing prompt. Add multiple adversarial inputs and confirm they are blocked.


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
  - the lore guard catches stronger extraction attempts
  - fallback behaviour still works
  - tests pass reliably


==========================================
END OF PROMPT 38
==========================================
