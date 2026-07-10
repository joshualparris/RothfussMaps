KKC TEXT ADVENTURE - PROMPT 30 OF 180
==========================================
Calendar and Term Structure
==========================================


This prompt builds directly on Prompts 1 through 29.
Do not restructure, rename, or refactor anything from those prompts.
Only add to what exists.


This prompt follows the original Phase 1 plan role for Prompt 30:
add a simple calendar so days, weeks, and term framing become explicit and deadlines sit on a real timeline.


Shared project context remains unchanged from:
- `project_state.md`
- `hard_bans.md`
- `architecture_rule.md`
- `architecture_reminders.md`


GOAL OF THIS PROMPT
Make time feel like a University term rather than just a day counter.


Keep the calendar simple and mechanical. This is for deadline realism, not for seasonal simulation.


SCOPE OF THIS PROMPT
This prompt covers:
  1. Add engine/calendarEngine.ts
  2. Map day numbers into weeks/term context
  3. Expose helpers for deadline/date text
  4. Add tests


This prompt does NOT cover:
  - Season/weather simulation
  - Holiday scheduling
  - Multi-term generation


FILES
Add exactly these files:
  - src/engine/calendarEngine.ts
  - tests/calendarEngine.test.ts


Modify these existing files:
  - src/narration/renderStatus.ts
  - src/engine/tuitionEngine.ts


Do not add any other files.


IMPLEMENTATION DETAILS
Implement a light calendar abstraction around the existing day_number/term_number rather than replacing them. Keep it deterministic and useful for status/deadlines.


TESTS
Add tests for week/day mapping and stable deadline text generation.


SUCCESS CRITERIA
This prompt is complete when:
  - the game can express time as part of a term structure
  - deadline systems can refer to the calendar cleanly
  - existing day tracking remains compatible
  - all new tests pass


==========================================
END OF PROMPT 30
==========================================
