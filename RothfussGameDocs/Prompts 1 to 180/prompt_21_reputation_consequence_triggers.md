KKC TEXT ADVENTURE - PROMPT 21 OF 180
==========================================
Reputation Consequence Triggers
==========================================


This prompt builds directly on Prompts 1 through 20.
Do not restructure, rename, or refactor anything from those prompts.
Only add to what exists.


This prompt follows the original Phase 1 plan role for Prompt 21:
write reputation consequence triggers so academic and social standing start affecting reactions and access in modest, deterministic ways.


Shared project context remains unchanged from:
- `project_state.md`
- `hard_bans.md`
- `architecture_rule.md`
- `architecture_reminders.md`


GOAL OF THIS PROMPT
Introduce consequence triggers on top of the centralised reputation system without adding a huge new world-simulation layer.


Focus on small, testable consequences. Examples: low academic standing affects how certain Masters or academic-facing systems respond; very poor trust with Ambrose-related social channels can make specific interactions more hostile. Keep this modest and deterministic.


SCOPE OF THIS PROMPT
This prompt covers:
  1. Add engine/reputationConsequences.ts
  2. Define trigger helpers for academic standing and selected NPC trust bands
  3. Wire modest consequence checks into existing relevant flows
  4. Add tests for trigger thresholds and non-trigger cases


This prompt does NOT cover:
  - Delayed reputation spread
  - Dynamic NPC schedules
  - Large-scale hostility systems
  - New commands


FILES
Add exactly these files:
  - src/engine/reputationConsequences.ts
  - tests/reputationConsequences.test.ts


Modify these existing files:
  - src/engine/actions.ts
  - src/engine/npcEngine.ts
  - src/narration/renderStatus.ts


Do not add any other files.


IMPLEMENTATION DETAILS
Implement explicit trigger helpers keyed off the shared reputation engine and return one small structured consequence result that existing systems can query instead of duplicating thresholds. Define at least one academic standing trigger band and one Ambrose-related social hostility trigger band. Keep the effects local, readable, and deterministic: access friction, colder responses, or modest hostility gates are in scope; faction frameworks and broad simulation are not. If a consequence message is needed, keep it brief and in-world.


TESTS
Add tests for low academic standing trigger, no-trigger when standing is decent, and an Ambrose-trust-based social hostility check that remains local rather than global.


SUCCESS CRITERIA
This prompt is complete when:
  - reputation consequences are centralised and deterministic
  - existing systems can query consequence state without duplicating threshold logic
  - no delayed spread system is introduced yet
  - all new tests pass


==========================================
END OF PROMPT 21
==========================================
