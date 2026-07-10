# Audit Report for University Map Project Refactor

## Summary
The repo has been refactored to implement a single source of truth via `canon_manifest.json`, with prompts inheriting from it. Validation script added to prevent future inconsistencies. A master campus prompt has now been added so downstream plans have an explicit north and scale anchor. Major contradictions have been reduced, but unresolved canon questions are still preserved rather than silently flattened.

## Contradictions Found and Fixed
1. **Archives height contradiction**: Files had both five-story and six-story wording. Normalized to **five-story** in the corrected Archives prompt family to match the current evidence freeze.
2. **Archives lighting contradiction**: Removed "natural light through windows" from prompts, kept "controlled artificial illumination".
3. **Duplicated floor prompts**: Broke the Archives upper-floor prompt family away from a clone pattern so later generations have distinct floor obligations instead of near-duplicates.
4. **Bursar prompt generic**: Updated to anchor on courtyard → stone building → hallway → stair down sequence.
5. **Crucible prompt over-assertive**: Reduced to classroom/lab context with specific equipment.
6. **Fishery/Artificery prompt assertive**: Focused on workshop and office, removed unsupported roof exit.
7. **Missing campus-image anchor**: Added `ai-prompts/university-site-plan.md` as the master campus/site plan prompt so later files no longer point to an implied map that does not exist.

## Unsupported Claims Removed or Downgraded
- Removed "roof exit" from Fishery prompt (not evidenced).
- Downgraded Mews fourth-floor to reconstructed bridge.
- Removed overclaimed adjacencies in campus layout.

## Frozen Bridges Retained
- Mews three-storey exterior + fourth-floor attic as reconstructed.
- Hollows/Masters' Hall relationship as unresolved.

## Files Changed
- canon_manifest.json: Created with structured claims.
- validate_repo.py: Created validation script.
- CONSISTENCY_RULES.md: Created rules document.
- ai-prompts/university-site-plan.md: Created as the master campus/site plan prompt.
- outputs/nano-banana/: Added staged storage guidance for workbench and approved image outputs.
- Key Archives files: Updated to five-story shell language and fixed lighting.
- Archives floor prompts: Made floor-specific.
- Bursar, Crucible, Fishery prompts: Tightened to evidence.

## Unresolved Issues Preserved
- Exact compass placement of buildings.
- Masters' Hall position.
- Hollows lecture hall vs office distinction.
- Fishery/Artificery exact relationship (treated as same complex).

## Validation Status
Repo passes the current automated checks and is ready for **campus-first** AI generation, with the explicit caveat that unresolved canon tensions should stay unresolved in downstream prompts.
