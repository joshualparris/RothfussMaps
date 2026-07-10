KKC TEXT ADVENTURE - PROMPT 29 OF 180
==========================================
Ambrose Conflict Escalation
==========================================


This prompt builds directly on Prompts 1 through 28.
Do not restructure, rename, or refactor anything from those prompts.
Only add to what exists.


This prompt follows the original Phase 1 plan role for Prompt 29:
turn Ambrose pressure into a staged escalation system rather than isolated incidents.


Shared project context remains unchanged from:
- `project_state.md`
- `hard_bans.md`
- `architecture_rule.md`
- `architecture_reminders.md`


GOAL OF THIS PROMPT
Make Ambrose feel like a persistent social threat without overbuilding a villain system.


Use small, deterministic stages. This is still University-level tension, not later-book-scale plotting.


SCOPE OF THIS PROMPT
This prompt covers:
  1. Add ambroseEscalation.ts
  2. Track escalation stage
  3. Tie stage changes to social interactions and trust bands
  4. Add tests for escalation progression


This prompt does NOT cover:
  - Sabotage scenes
  - Theft plots
  - Plum bob
  - Major disciplinary hearings


FILES
Add exactly these files:
  - src/engine/ambroseEscalation.ts
  - tests/ambroseEscalation.test.ts


Modify these existing files:
  - src/engine/socialEngine.ts
  - src/engine/worldStateEngine.ts


Do not add any other files.


IMPLEMENTATION DETAILS
Implement a small escalation model stored in world_state, with explicit ordered stages such as quiet_hostility, public_cuttingness, and formal_trouble_pressure. Define what kinds of social interactions or trust-band thresholds move Ambrose from one stage to the next, and make progression advance one stage at a time with no jumps. Keep the consequences local and deterministic: sharper social responses, access friction, or modest institutional pressure are in scope, while sabotage plots and large villain systems are not.


TESTS
Add tests for stage progression, no-jump behaviour, and stable persistence.


SUCCESS CRITERIA
This prompt is complete when:
  - Ambrose conflict now escalates coherently
  - the escalation remains modest and Phase-1 appropriate
  - world state can remember the stage
  - all new tests pass


==========================================
END OF PROMPT 29
==========================================
