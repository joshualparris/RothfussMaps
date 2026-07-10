KKC TEXT ADVENTURE - PROMPT 25 OF 180
==========================================
Canon Event System
==========================================


This prompt builds directly on Prompts 1 through 24.
Do not restructure, rename, or refactor anything from those prompts.
Only add to what exists.


This prompt follows the original Phase 1 plan role for Prompt 25:
add a small event system where fixed or semi-fixed events can trigger from world conditions without railroading the player.


Shared project context remains unchanged from:
- `project_state.md`
- `hard_bans.md`
- `architecture_rule.md`
- `architecture_reminders.md`


GOAL OF THIS PROMPT
Create the structural layer needed for tuition hearing, first Eolian audition framing, and later University events.


Keep the event system modest: trigger conditions, fixed vs flexible framing, and world state changes. Do not explode into branching narrative infrastructure.


SCOPE OF THIS PROMPT
This prompt covers:
  1. Add engine/eventEngine.ts
  2. Define event shape and trigger condition checks
  3. Add world-state updates on event resolution
  4. Add tests for trigger evaluation


This prompt does NOT cover:
  - Large branching story graphs
  - Cinematic scripting
  - Multi-era story management
  - Frontend event UI


FILES
Add exactly these files:
  - src/engine/eventEngine.ts
  - tests/eventEngine.test.ts


Modify these existing files:
  - src/types/index.ts
  - src/engine/actions.ts
  - src/engine/state.ts


Do not add any other files.


IMPLEMENTATION DETAILS
Implement a compact event model with id, trigger_conditions, is_fixed, and world_state_changes. Check triggers after actions. Keep it deterministic and engine-owned.


TESTS
Add tests for unmet triggers, met triggers, single-fire events, and world-state updates.


SUCCESS CRITERIA
This prompt is complete when:
  - events can trigger from world conditions
  - world_state changes are applied deterministically
  - the system is ready for concrete Phase 1 events
  - all new tests pass


==========================================
END OF PROMPT 25
==========================================
