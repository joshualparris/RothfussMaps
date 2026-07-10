KKC TEXT ADVENTURE - PROMPT 26 OF 180
==========================================
Tuition Hearing Event
==========================================


This prompt builds directly on Prompts 1 through 25.
Do not restructure, rename, or refactor anything from those prompts.
Only add to what exists.


This prompt follows the original Phase 1 plan role for Prompt 26:
script the tuition hearing as a canon-grounded fixed event whose framing can vary but whose institutional reality remains intact.


Shared project context remains unchanged from:
- `project_state.md`
- `hard_bans.md`
- `architecture_rule.md`
- `architecture_reminders.md`


GOAL OF THIS PROMPT
Use the event system to make tuition feel like a real University pressure point.


Keep the hearing modest and text-centric. The player can affect approach and flavour, but the event remains institutionally bounded.


SCOPE OF THIS PROMPT
This prompt covers:
  1. Add authored tuition hearing event definition
  2. Tie it to tuition and term conditions
  3. Add outcome hooks for academic standing/social pressure
  4. Add tests for trigger and outcome application


This prompt does NOT cover:
  - Full Masters dialogue roster
  - Large branching tribunal scenes
  - Rank advancement decisions


FILES
Add exactly these files:
  - src/content/events/tuitionHearing.ts
  - tests/tuitionHearingEvent.test.ts


Modify these existing files:
  - src/engine/eventEngine.ts
  - src/engine/tuitionEngine.ts


Do not add any other files.


IMPLEMENTATION DETAILS
Use the event system from Prompt 25 and keep the tuition hearing fixed in structure: trigger it from concrete tuition and term conditions, resolve it through one authored event definition, and apply deterministic world or reputation outcomes. Any variation should be limited to brief framing differences from already-existing state such as academic standing or social pressure; do not branch the core event flow and do not over-script every Master yet.


TESTS
Add tests for correct trigger conditions and correct world/reputation changes after the event.


SUCCESS CRITERIA
This prompt is complete when:
  - the tuition hearing can trigger correctly
  - the event feels institutional and grounded
  - the system remains deterministic
  - all new tests pass


==========================================
END OF PROMPT 26
==========================================
