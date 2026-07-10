# Consistency Rules

## Source Hierarchy
1. lawful-text evidence and evidence-ledger rows
2. `campus-layout.md`
3. building briefs and reconstruction briefs
4. floorplan JSON
5. AI prompts

Lower layers may interpret higher layers, but they may not contradict them.

## Certainty Tags
- `canon`: directly supported by evidence
- `implied`: strongly supported by canon
- `reconstructed`: practical bridge used to make a plan usable
- `unknown`: unresolved and must remain unresolved
- `tension`: conflicting supported claims that cannot be silently smoothed away

## Inheritance Rules
- Prompts inherit shell facts from the entity manifest, not from copied prose blocks.
- Child prompts may narrow a parent prompt but may not override a parent hard ban.
- If a child prompt uses a reconstructed bridge, that bridge must stay labeled as reconstructed.
- If canon is unresolved, prompts must preserve uncertainty instead of resolving it by invention.

## Hard-Ban Logic
- Any manifest claim marked `hard_ban: true` must never be contradicted downstream.
- Common examples:
  - no windows in the Archives
  - no natural window light in the Archives
  - no neat rectangular Mains master plan
  - no silent conversion of the Mews floor-count tension into canon

## Building-Specific Rules

### Archives
- Height is five stories, per current ledger evidence.
- Use a roof prompt, not a sixth-floor prompt.
- Tomes may be well-lit, but not by windows.
- Upper floor prompts must be distinct by role, not cloned.

### Mains
- Keep the shell irregular, accreted, and inconvenient.
- Remove exact dimensions or entrance counts unless ledger-backed.

### Mews
- Preserve the tension between three-story exterior wording and fourth-floor east-wing bunks.
- The working bridge is a reconstructed partial upper east-wing level.

### Hollows
- Admissions theatre and Elodin's office are canon in Hollows.
- Elodin's lecture hall may be placed there only if clearly labeled as reconstructed or uncertain.

### Masters' Hall
- Treat as residential-governance space first, not a fully specified office block.
- Do not import Elodin's office into Masters' Hall.

### Fishery or Artificery
- Keep workshop prompts anchored to Kilvin's office, east-wall windows, and south exit.
- Treat ventilation or safety zoning as reconstructed unless directly evidenced.

### Bursar
- Anchor the office prompt to the route sequence: courtyard -> stone building -> hallway -> stairs down -> bursar.

## Validation
- Run `python validate_repo.py` from `UniversityMapProject`.
- Validation must fail on:
  - story-count mismatches
  - banned terms in prompt families
  - duplicated floor prompts beyond threshold
  - unsupported shell rationalization
  - missing evidence anchors in key prompts
