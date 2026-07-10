# University Map Reconstruction Pipeline

This project is a canon-constrained reconstruction pipeline for the University from the Kingkiller Chronicle. The source of truth is structured data, not Blender scenes.

## Source Of Truth

The first authoritative floor source is:

`data/buildings/archives_ground_v02_canon_safe.json`

It uses the `canon_floor_plan_v02` contract and keeps the Archives ground floor intentionally restrained: square shell, no windows, single main entrance, antechamber, Tomes, Scrivs Only route, Stacks threshold, lower-stacks access logic, and public/restricted hierarchy.

## Certainty Model

Every meaningful plan element should be tagged as one of:

- `canon`
- `implied`
- `reconstructed`

Approximate geometry must be flagged clearly. Do not use precise dimensions to imply certainty the source does not support.

## Folder Layout

- `data/buildings/` - floor JSON sources
- `data/pipeline_manifest.json` - building/floor automation targets
- `data/review_gates.json` - interpretation approval gates
- `schemas/` - JSON schema contracts
- `scripts/validation/` - strict data validation
- `scripts/blender/` - Blender import and test helpers
- `scripts/godot/` - Godot walkthrough scaffold helpers
- `skills/` - project-local reconstruction workflows
- `exports/` - generated Blender/Godot pipeline outputs
- `docs/` - audit notes, evidence summaries, and design constraints
- `buildings/` - building-specific briefs
- `Projectplan/` - imported ChatGPT planning pack, retained as source context

## Pipeline Harness

Run an audit:

```powershell
python .\RothfussGameDocs\UniversityMapProject\run_pipeline.py --building archives --floor ground --stage audit
```

Run validation:

```powershell
python .\RothfussGameDocs\UniversityMapProject\run_pipeline.py --building archives --floor ground --stage validate
```

Show review gates:

```powershell
python .\RothfussGameDocs\UniversityMapProject\run_pipeline.py --building archives --floor ground --show-gates
```

Run Blender generation after validation and review gates:

```powershell
python .\RothfussGameDocs\UniversityMapProject\run_pipeline.py --building archives --floor ground --stage blender
```

Run Godot scaffold after Blender generation:

```powershell
python .\RothfussGameDocs\UniversityMapProject\run_pipeline.py --building archives --floor ground --stage godot
```

## Validation Workflow

Run:

```powershell
python .\RothfussGameDocs\UniversityMapProject\scripts\validation\validate_floor_plan.py .\RothfussGameDocs\UniversityMapProject\data\buildings\archives_ground_v02_canon_safe.json
```

The validator checks required keys, certainty tags, duplicate ids, polygon validity, room containment, door references, stair references, draft/approximation flags, and obvious geometry contradictions.

## Blender Import Workflow

For Blender UI testing, open:

`blender_trace_script.py`

Then run it from Blender's Scripting tab. It imports only the current Archives ground source.

For command-line Blender testing:

```powershell
.\RothfussGameDocs\UniversityMapProject\scripts\blender\run_headless_import.ps1
```

If Blender is not on `PATH`, pass:

```powershell
.\RothfussGameDocs\UniversityMapProject\scripts\blender\run_headless_import.ps1 -BlenderExe "C:\Path\To\blender.exe"
```

## Future Godot Path

After the Archives ground plan validates and imports cleanly:

1. Export a `.blend` or `.glb` blockout.
2. Create a Godot test scene for scale, collision, and player navigation.
3. Preserve JSON as the source of truth.
4. Regenerate engine assets from validated data instead of hand-editing final geometry first.

The harness can create the starter walkthrough project:

```powershell
python .\RothfussGameDocs\UniversityMapProject\run_pipeline.py --building archives --floor ground --stage godot
```

## Next Phases

1. Lock Archives Ground validation.
2. Add Archives lower and upper floor sources.
3. Apply the schema to other University buildings.
4. Integrate campus master layout after building-scale contracts are stable.
5. Build the Godot exploration pipeline.

## Codex Planning Pack

The ChatGPT planning pack has been normalized into:

- `AGENTS.md`
- `docs/codex_university_workflows.md`
- `docs/codex_master_prompts.md`
- `docs/MASTER_CODEX_PROMPT.md`
- `skills/`

The original `Projectplan/` folder is kept as context, but the normalized files above are the working references.
