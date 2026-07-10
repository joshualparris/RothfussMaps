KKC TEXT ADVENTURE - PROMPT 27 OF 180
==========================================
First Eolian Audition Event Framing
==========================================


This prompt builds directly on Prompts 1 through 26.
Do not restructure, rename, or refactor anything from those prompts.
Only add to what exists.


This prompt follows the original Phase 1 plan role for Prompt 27:
script the first Eolian audition as a proper event wrapper around the existing music logic.


Shared project context remains unchanged from:
- `project_state.md`
- `hard_bans.md`
- `architecture_rule.md`
- `architecture_reminders.md`


GOAL OF THIS PROMPT
Make the first serious attempt for pipes feel like an event, not just a mechanical function call.


Use the existing audition logic and event system together. The player’s prep and condition matter, but the structure remains controlled.


SCOPE OF THIS PROMPT
This prompt covers:
  1. Add an Eolian audition event definition
  2. Use existing music/audition truth
  3. Add event framing and world-state updates
  4. Add tests


This prompt does NOT cover:
  - New music mechanics
  - Denna scene scripting
  - Concert-style multi-stage event trees


FILES
Add exactly these files:
  - src/content/events/eolianFirstAudition.ts
  - tests/eolianFirstAuditionEvent.test.ts


Modify these existing files:
  - src/engine/eventEngine.ts
  - src/engine/musicEngine.ts


Do not add any other files.


IMPLEMENTATION DETAILS
Wrap the existing audition logic rather than replacing it. The event layer should frame the moment and update world state, but not own music truth.


TESTS
Add tests for trigger conditions, successful world-state update, and correct use of underlying audition truth.


SUCCESS CRITERIA
This prompt is complete when:
  - the first audition can be framed as an event
  - the event uses existing music truth rather than duplicating it
  - world state can record that it happened
  - all new tests pass


==========================================
END OF PROMPT 27
==========================================
