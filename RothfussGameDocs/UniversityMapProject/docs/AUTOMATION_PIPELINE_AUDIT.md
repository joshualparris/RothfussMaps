# Automation Pipeline Audit

## Relevant File Tree

- `data/buildings/archives_ground_v02_canon_safe.json`
- `data/buildings/archives_ground.json`
- `data/buildings/archives_ground_extracted.json`
- `data/buildings/*_ground.json`
- `schemas/canon_floor_plan_v02.schema.json`
- `scripts/validation/validate_floor_plan.py`
- `scripts/blender/import_floor_plan.py`
- `scripts/blender/run_headless_import.ps1`
- `scripts/import_archives_canon_safe.py`
- `blender_trace_script.py`
- `run_pipeline.py`
- `data/pipeline_manifest.json`
- `data/review_gates.json`
- `BLENDER_TESTING_READY.md`
- `README_blender_script.md`
- `README.md`

## Schema Mismatch Analysis

The older building JSON files use a shape like:

- `building_id`
- `floor_id`
- `metadata`
- `geometries.footprint`
- `geometries.rooms`
- `geometries.walls`
- `geometries.portals`
- `geometries.vertical_circulation`

The new canon-safe source uses:

- `building`
- `floor`
- `story_role`
- `footprint`
- `rooms`
- `doors`
- `stairs`
- `labels`
- `validation_flags`

Those are different contracts. The old validator and importer should not be treated as authoritative for the v02 Archives source.

## Importer Mismatch Analysis

The older Blender path had three core problems:

- It imported every JSON file in `data/buildings`.
- It expected the older `building_id` / `floor_id` / `geometries` contract.
- It treated source `z` as Blender `z` directly, leaving elevation logic muddled for a normal Blender Z-up workflow.

The new importer targets one JSON file and maps source floorplan coordinates as:

- JSON `x` -> Blender `x`
- JSON `z` -> Blender `y`
- Blender `z` -> vertical elevation

## Implementation Plan

1. Keep `archives_ground_v02_canon_safe.json` as the first authoritative source.
2. Validate that JSON using `scripts/validation/validate_floor_plan.py`.
3. Import that same JSON using `scripts/blender/import_floor_plan.py`.
4. Use `blender_trace_script.py` only as a convenience wrapper for Blender's Text Editor.
5. When Blender is installed, run `scripts/blender/run_headless_import.ps1` to verify import without UI clicking.
6. Prefer `run_pipeline.py` for repeatable audit, validation, Blender, and Godot stages.
7. After Archives ground validates cleanly, extend the same schema to other Archives floors before returning to campus-scale automation.

## Harness Commands

```powershell
python .\RothfussGameDocs\UniversityMapProject\run_pipeline.py --building archives --floor ground --stage audit
python .\RothfussGameDocs\UniversityMapProject\run_pipeline.py --building archives --floor ground --stage validate
python .\RothfussGameDocs\UniversityMapProject\run_pipeline.py --building archives --floor ground --stage blender
python .\RothfussGameDocs\UniversityMapProject\run_pipeline.py --building archives --floor ground --stage godot
```

## Current Canon-Safety Position

The source keeps the strongest safe elements: square shell, no windows, single entrance, antechamber, Tomes, Scrivs Only route, Stacks threshold, lower-stacks access logic, and public/restricted hierarchy.

The source deliberately does not lock speculative support rooms, shelving districts, exact stair direction, exact room proportions, or final door placements.
