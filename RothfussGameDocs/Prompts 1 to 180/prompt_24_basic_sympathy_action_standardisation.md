KKC TEXT ADVENTURE - PROMPT 24 OF 180
==========================================
Basic Sympathy Action Standardisation
==========================================


This prompt builds directly on Prompts 1 through 23.
Do not restructure, rename, or refactor anything from those prompts.
Only add to what exists.


This prompt follows the original Phase 1 plan role for Prompt 24:
turn the early sympathy system into one clear MVP action path with deterministic pass/fail and consistent consequences.


Shared project context remains unchanged from:
- `project_state.md`
- `hard_bans.md`
- `architecture_rule.md`
- `architecture_reminders.md`


GOAL OF THIS PROMPT
Consolidate sympathy action handling so later prompts can build on a stable core.


Use the systems already introduced: links, warmth/body heat, materials, and simple backlash/slip outcomes. This is not full naming or advanced sympathy depth yet.


SCOPE OF THIS PROMPT
This prompt covers:
  1. Add engine/sympathyAction.ts as the central sympathy action module
  2. Route existing sympathy use through shared helpers
  3. Standardise consequences and result text hooks
  4. Add tests for successful, failed, and unsafe actions


This prompt does NOT cover:
  - Advanced sympathy chaining
  - Naming
  - Alchemy
  - Crafting


FILES
Add exactly these files:
  - src/engine/sympathyAction.ts
  - tests/sympathyAction.test.ts


Modify these existing files:
  - src/engine/actions.ts
  - src/engine/sympathyEngine.ts
  - src/narration/narrationContext.ts


Do not add any other files.


IMPLEMENTATION DETAILS
Implement one central sympathy action path in src/engine/sympathyAction.ts and route existing sympathy use through it rather than leaving logic split across call sites. Define the minimum deterministic decision flow: validate inputs, check link/material/heat requirements, resolve success or failure, apply cost, then assign one consequence bucket such as safe success, blocked attempt, backlash, or slip. The engine owns the full result object and narration only renders it.


TESTS
Add tests for a valid action, a blocked action due to missing material or unsafe condition, and a failed action with an appropriate consequence bucket.


SUCCESS CRITERIA
This prompt is complete when:
  - sympathy action handling is centralised
  - the engine owns all success/failure truth
  - later prompts can build on this shared path
  - all new tests pass


==========================================
END OF PROMPT 24
==========================================
