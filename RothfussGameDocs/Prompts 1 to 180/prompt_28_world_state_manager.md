KKC TEXT ADVENTURE - PROMPT 28 OF 180
==========================================
World State Manager
==========================================


This prompt builds directly on Prompts 1 through 27.
Do not restructure, rename, or refactor anything from those prompts.
Only add to what exists.


This prompt follows the original Phase 1 plan role for Prompt 28:
formalise world state tracking so flags, term context, and event markers live in one coherent place.


Shared project context remains unchanged from:
- `project_state.md`
- `hard_bans.md`
- `architecture_rule.md`
- `architecture_reminders.md`


GOAL OF THIS PROMPT
Make world_state a first-class shared structure rather than a loose collection of flags.


Focus on coherent access/update helpers, not on adding lots of new flags.


SCOPE OF THIS PROMPT
This prompt covers:
  1. Add engine/worldStateEngine.ts
  2. Centralise get/set/update helpers
  3. Standardise common Phase 1 flags
  4. Add tests for state mutation and retrieval


This prompt does NOT cover:
  - Save-slot systems
  - Branch visualisation
  - Narrative debugging UI


FILES
Add exactly these files:
  - src/engine/worldStateEngine.ts
  - tests/worldStateEngine.test.ts


Modify these existing files:
  - src/engine/state.ts
  - src/engine/eventEngine.ts


Do not add any other files.


IMPLEMENTATION DETAILS
Implement a small world state helper layer around the existing world_state structure so engine code uses one shared path for reading, setting, and updating flags. Cover concrete categories: relationship and access flags such as has_met_X and archives approval, progression markers such as event ids already fired, and term context such as term_number and days_until_tuition. The helper should define how keys are stored, how updates remain deterministic, and how event and persistence code call into it rather than mutating loose flags directly.


TESTS
Add tests for world-state get/set/update behaviour and compatibility with persisted player/world state.


SUCCESS CRITERIA
This prompt is complete when:
  - world_state has a shared management layer
  - flags become easier to reason about
  - event and progression systems can rely on one shared place
  - all new tests pass


==========================================
END OF PROMPT 28
==========================================
