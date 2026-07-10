KKC TEXT ADVENTURE - PROMPT 23 OF 180
==========================================
Archives Access System
==========================================


This prompt builds directly on Prompts 1 through 22.
Do not restructure, rename, or refactor anything from those prompts.
Only add to what exists.


This prompt follows the original Phase 1 plan role for Prompt 23:
formalise Archives access as requiring Re'lar rank and Lorren's approval, with proper in-world denial handling.


Shared project context remains unchanged from:
- `project_state.md`
- `hard_bans.md`
- `architecture_rule.md`
- `architecture_reminders.md`


GOAL OF THIS PROMPT
Turn the existing Archives restrictions into one clear system rather than scattered checks.


Use the canon-safe MVP rule already established: the Stacks require Re'lar and Lorren's approval. Keep denial grounded and institutional.


SCOPE OF THIS PROMPT
This prompt covers:
  1. Add engine/archivesAccess.ts
  2. Track Lorren approval in world_state as a single explicit access flag
  3. Centralise access checks and denial text
  4. Add tests for rank and approval combinations


This prompt does NOT cover:
  - Full Archives browsing
  - Lorren as a full active NPC system
  - Research mechanics
  - New map areas beyond current Archives spaces


FILES
Add exactly these files:
  - src/engine/archivesAccess.ts
  - tests/archivesAccess.test.ts


Modify these existing files:
  - src/types/index.ts
  - src/engine/movement.ts
  - src/narration/renderLocation.ts


Do not add any other files.


IMPLEMENTATION DETAILS
Create one Archives access helper that determines whether the player may enter the Stacks by checking two explicit conditions: Re'lar rank and a Lorren approval flag stored in world_state. Return a clean in-world failure line when blocked, and make movement and location rendering call the same helper instead of scattering checks. Reuse existing rank and canon registry truth, but do not expand this into research mechanics or broader Archives simulation.


TESTS
Add tests for blocked E'lir, blocked Re'lar without approval, and successful access when both Re'lar rank and Lorren approval are present.


SUCCESS CRITERIA
This prompt is complete when:
  - Archives access logic is centralised
  - the Stacks require Re'lar and approval
  - denial messages are grounded and consistent
  - movement/rendering respect the shared access logic


==========================================
END OF PROMPT 23
==========================================
