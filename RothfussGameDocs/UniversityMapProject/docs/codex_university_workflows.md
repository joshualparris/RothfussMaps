# Codex Workflows For UniversityMapProject

These workflows turn the repo into a repeatable research-and-geometry pipeline rather than a pile of one-off prompts.

## 1. Audit Repo

Use when starting work or after major changes.

Steps:

1. Print a concise tree of relevant research, schema, 3D, and prompt files.
2. Identify source-of-truth evidence files.
3. Identify schema variants in `floorplans/`, `data/buildings/`, and `_3D Map/`.
4. Identify old importers and validators.
5. List contradictions or drift.
6. Propose a minimal migration plan.

Expected output:

- relevant file tree
- contradiction list
- schema mismatch list
- recommended next edits

Harness command:

```powershell
python .\RothfussGameDocs\UniversityMapProject\run_pipeline.py --building archives --floor ground --stage audit
```

## 2. Extract Building Evidence

Use when working on one building.

Inputs:

- lawful book PDFs if present
- evidence ledger CSVs
- manifest
- building briefs
- reconstruction briefs
- older floor plans and prompts

Steps:

1. Search sources for all mentions of the building and named subspaces.
2. Compile a short evidence table.
3. Split findings into `canon`, `implied`, `reconstructed`, `unknown`, and `tension`.
4. Flag anything in prompts or JSON that exceeds the evidence.

Expected output:

- evidence table
- certainty-tagged findings
- contradictions and unknowns
- recommended brief changes

## 3. Freeze Building Brief

Use once evidence is assembled.

Required sections:

- canon
- strong implication
- reconstructed bridge
- unknowns
- hard bans

Steps:

1. Start from the existing building brief if present.
2. Compare against manifest and evidence table.
3. Remove unsupported claims.
4. Preserve unresolved issues.
5. Write a concise frozen brief.

Review gate:

`building_brief_frozen`

## 4. Draft Floor JSON

Use after the building brief is frozen.

Rules:

- safer and simpler beats richer and more speculative
- geometry is blockout geometry, not art
- approximate dimensions must be flagged
- spatial certainty tags are only `canon`, `implied`, and `reconstructed`

Required top-level fields:

- `building`
- `floor`
- `story_role`
- `footprint`
- `rooms`
- `doors`
- `stairs`
- `labels`
- `validation_flags`

Review gate:

`floor_json_frozen`

## 5. Validate Floor

Use on every new or revised floor JSON.

Command:

```powershell
python .\RothfussGameDocs\UniversityMapProject\run_pipeline.py --building archives --floor ground --stage validate
```

Checks:

- required keys
- unique ids
- certainty tags
- polygon validity
- containment
- door references
- stair references
- approximation flags
- obvious geometry contradictions

## 6. Blender Blockout Import

Use only after validation passes.

Command:

```powershell
python .\RothfussGameDocs\UniversityMapProject\run_pipeline.py --building archives --floor ground --stage blender
```

Rules:

- target one file, not a directory
- use Blender Z-up
- create separate collections for footprint, rooms, doors, stairs, and labels
- attach metadata to objects
- no decorative mesh generation

## 7. Godot Walkable Test

Use after Blender blockout exists.

Command:

```powershell
python .\RothfussGameDocs\UniversityMapProject\run_pipeline.py --building archives --floor ground --stage godot
```

Rules:

- use collision and simple navigation first
- preserve ids and labels
- do not add decorative props by default

## 8. Building Pipeline Run

Example sequence:

1. audit relevant files
2. extract building evidence
3. freeze building brief
4. draft floor JSON
5. validate floor
6. import blockout to Blender
7. export or stage for Godot
8. stop and report uncertainties

Success condition:

The result is an authoritative, evidence-led, editable blockout source, not finished architecture.

