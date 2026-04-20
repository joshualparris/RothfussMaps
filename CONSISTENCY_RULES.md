# Consistency Rules for University Map Project

## Source Hierarchy (Highest Wins)
1. Lawful-text evidence and evidence-ledger rows
2. Campus-layout freeze
3. Building briefs / reconstruction briefs
4. Floorplan JSON
5. AI prompts

If lower-level files contradict higher-level files, lower-level files must be rewritten.

## Certainty Tags
- **canon**: Directly supported by evidence ledger / source text
- **implied**: Strongly supported but not directly stated
- **reconstructed**: Practical bridge introduced to make a plan usable
- **unknown**: Unresolved and must stay unresolved
- **tension**: Two pieces of project evidence conflict and neither can be silently discarded

## Hard Rules
- Do not invent exact dimensions unless canon supplies them.
- Do not invent entrances, windows, stairs, towers, wings, courtyards, or adjacencies to make plans feel complete.
- Do not convert reconstructed claims into canon wording.
- Do not suppress contradictions.
- Do not let child prompts override parent freezes.
- Do not let image prompts include facts absent from the frozen brief.

## File Structure
Every building file must be split into five sections only:
- Canon
- Strong implication
- Reconstructed bridge
- Unknowns
- Hard bans

## Terminology
- "Fishery" and "Artificery" are treated as the same complex.
- "House of the Wind / Pennant Square / Questioning Hall" is frozen as one working square.
- "Belows / Billows" is one zone with spelling uncertainty.
- "North" aligns with the master campus map.

## Validation Checks
The repo must pass these checks:
- No story-count mismatches across files for the same building.
- No hard-ban violations (e.g., windows in Archives).
- No unsupported claims in prompts (must be in manifest).
- No parent/child inconsistency.
- No reconstructed claims presented as canon.