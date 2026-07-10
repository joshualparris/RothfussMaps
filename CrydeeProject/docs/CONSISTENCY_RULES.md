# Consistency Rules

## Source Hierarchy

1. lawful text evidence and evidence-ledger rows
2. `evidence/canon_manifest.json`
3. `docs/site-layout.md`
4. building briefs and reconstruction briefs
5. structure JSON
6. AI prompts

Lower layers may interpret higher layers, but they may not contradict them.

## Certainty Tags

- `canon`: directly supported by the novel evidence
- `implied`: strongly supported but not directly stated
- `reconstructed`: practical bridge added to make the structure usable
- `unknown`: unresolved and must stay unresolved
- `tension`: two supported claims conflict and cannot be silently flattened

## Inheritance Rules

- Prompts inherit hard facts from the manifest and frozen briefs, not from copied prose.
- Child prompts may narrow a parent prompt but may not override a parent hard ban.
- If a prompt uses a reconstructed bridge, that bridge must stay labeled reconstructed.
- If canon is unresolved, preserve uncertainty instead of solving it by invention.

## Crydee-Specific Rules

### Castle Versus Town

- Do not collapse the castle keep, castle grounds, and town below into one flat undifferentiated space.
- If the relationship between castle elevation, town, cliffs, and shoreline is uncertain in detail, mark it uncertain.

### Peacetime Versus Siege

- Do not let siege descriptions overwrite the default peacetime layout without versioning the scene.
- A battlement mentioned during war is not automatically a full structural blueprint.

### Great Hall

- Treat the great hall as a confirmed anchor room.
- Do not invent its exact size, window count, or decorative scheme without evidence.

### Courtyard, Gate, and Stable Side

- Preserve route logic such as wall-behind-stables and courtyard-gate references.
- Do not add extra major gates, bridges, or posterns unless evidence supports them.

### Defensive Identity

- Keep Crydee practical and frontier-facing rather than turning it into a polished fantasy mega-castle.
- Prefer a workmanlike border fortress with lived-in noble and service functions.

## Hard Bans

- No exact full-castle master plan should be treated as canon before the evidence supports it.
- No concentric-castle geometry should be introduced merely because it looks dramatic.
- No decorative room inflation just to make the castle feel richer.
- No false precision in wall thickness, tower count, or courtyard dimensions.

