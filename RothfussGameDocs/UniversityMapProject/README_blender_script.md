# Blender Floor Plan Import

The current Blender workflow imports one authoritative floor JSON at a time.

## Current Source

- JSON: `data/buildings/archives_ground_v02_canon_safe.json`
- Convenience entry: `blender_trace_script.py`
- Generic importer: `scripts/blender/import_floor_plan.py`

## UI Usage

1. Open Blender.
2. Go to the Scripting tab.
3. Open `RothfussGameDocs\UniversityMapProject\blender_trace_script.py`.
4. Run it with `Alt+P`.

## Headless Usage

```powershell
.\RothfussGameDocs\UniversityMapProject\scripts\blender\run_headless_import.ps1
```

If Blender is not on `PATH`, pass `-BlenderExe`.

Preferred harness command:

```powershell
python .\RothfussGameDocs\UniversityMapProject\run_pipeline.py --building archives --floor ground --stage blender
```

## What It Builds

- Footprint collection with slab and outer shell walls
- Rooms collection with Antechamber, Tomes, Scrivs Only, and Stacks Threshold surfaces
- Doors collection with marker geometry
- Stairs collection with lower-access marker geometry
- Labels collection with text labels
- Custom properties for certainty tags, notes, source JSON, and references
- Optional `.blend` and `.glb` outputs for the Godot walkthrough path

The command-line path clears the default Blender scene before import and exports only the generated blockout collection.

## Coordinate Rule

The JSON stores plan coordinates as `x` and `z`.

The Blender importer maps:

- JSON `x` -> Blender `x`
- JSON `z` -> Blender `y`
- Blender `z` -> vertical elevation

This keeps the scene Blender-friendly and Z-up.
