KKC TEXT ADVENTURE - PROMPT 22 OF 180
==========================================
Word Travels: Pending Reputation Changes Queue
==========================================


This prompt builds directly on Prompts 1 through 21.
Do not restructure, rename, or refactor anything from those prompts.
Only add to what exists.


This prompt follows the original Phase 1 plan role for Prompt 22:
add a delayed reputation spread queue so some changes reach the wider world after 1-3 in-game days instead of instantly.


Shared project context remains unchanged from:
- `project_state.md`
- `hard_bans.md`
- `architecture_rule.md`
- `architecture_reminders.md`


GOAL OF THIS PROMPT
Make the world feel more socially believable by separating immediate internal changes from delayed wider awareness.


Keep the delayed queue narrow and mechanical. Immediate direct trust changes can remain immediate; broader public-facing reputation shifts can queue and apply later.


SCOPE OF THIS PROMPT
This prompt covers:
  1. Add engine/reputationQueue.ts
  2. Use a dedicated pending_reputation_changes queue structure with apply_on_day
  3. Apply queued changes when day advances
  4. Add tests for delay and one-time application


This prompt does NOT cover:
  - Large social simulation
  - Dynamic rumour spread
  - NPC memory systems
  - New commands


FILES
Add exactly these files:
  - src/engine/reputationQueue.ts
  - tests/reputationQueue.test.ts


Modify these existing files:
  - src/engine/time.ts
  - src/engine/socialEngine.ts
  - src/engine/musicEngine.ts


Do not add any other files.


IMPLEMENTATION DETAILS
Implement a small pending queue abstraction around a dedicated pending_reputation_changes structure with apply_on_day, change payload, and applied state or removal on completion. Queue only public-facing reputation changes here; direct trust changes remain immediate. When the day advances, apply every due entry in deterministic order, persist the updated reputation result, and clear the queue entry so it cannot fire twice. Do not leave the storage choice open and do not add background simulation.


TESTS
Add tests for queuing a change, not applying it early, applying it on the correct day, and not applying it twice.


SUCCESS CRITERIA
This prompt is complete when:
  - pending public reputation changes can be delayed
  - queued changes apply on the correct day
  - queued changes apply only once
  - existing immediate systems still work


==========================================
END OF PROMPT 22
==========================================
