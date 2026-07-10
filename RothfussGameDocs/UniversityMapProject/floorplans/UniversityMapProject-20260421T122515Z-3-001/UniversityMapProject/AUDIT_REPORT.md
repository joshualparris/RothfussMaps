# Audit Report for University Map Project Refactor

## Summary
The repo has been refactored to implement a single source of truth via `canon_manifest.json`, with prompts inheriting from it. Validation script added to prevent future inconsistencies. All known contradictions resolved.

## Contradictions Found and Fixed
1. **Archives height contradiction**: Files had both five-story and six-story. Resolved to six-story across all files based on evidence.
2. **Archives lighting contradiction**: Removed "natural light through windows" from prompts, kept "controlled artificial illumination".
3. **Duplicated floor prompts**: Made each Archives floor prompt floor-specific with unique constraints (2nd: scriv-work, 3rd: Sorting Hall, 4th: Cataloger's Mew, 5th: Scriptorium, 6th: roof access).
4. **Bursar prompt generic**: Updated to anchor on courtyard → stone building → hallway → stair down sequence.
5. **Crucible prompt over-assertive**: Reduced to classroom/lab context with specific equipment.
6. **Fishery/Artificery prompt assertive**: Focused on workshop and office, removed unsupported roof exit.

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
- All Archives files: Updated height to six-story, fixed lighting.
- Archives floor prompts: Made floor-specific.
- Bursar, Crucible, Fishery prompts: Tightened to evidence.

## Unresolved Issues Preserved
- Exact compass placement of buildings.
- Masters' Hall position.
- Hollows lecture hall vs office distinction.
- Fishery/Artificery exact relationship (treated as same complex).

## Validation Status
Repo now passes all automated checks. Ready for AI generation with reduced drift risk.