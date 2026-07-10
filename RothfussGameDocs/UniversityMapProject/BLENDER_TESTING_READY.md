# Archives Ground Floor - Blender Testing Ready

## Current Automation Path

The repo is now the source of truth. Blender is a generated blockout target.

- Authoritative JSON: `data/buildings/archives_ground_v02_canon_safe.json`
- Schema: `schemas/canon_floor_plan_v02.schema.json`
- Validator: `scripts/validation/validate_floor_plan.py`
- Generic Blender importer: `scripts/blender/import_floor_plan.py`
- Blender UI wrapper: `blender_trace_script.py`
- Headless helper: `scripts/blender/run_headless_import.ps1`

## Validate First

```powershell
python .\RothfussGameDocs\UniversityMapProject\scripts\validation\validate_floor_plan.py .\RothfussGameDocs\UniversityMapProject\data\buildings\archives_ground_v02_canon_safe.json
```

Or use the harness:

```powershell
python .\RothfussGameDocs\UniversityMapProject\run_pipeline.py --building archives --floor ground --stage validate
```

## Blender UI Test

1. Close and reopen Blender.
2. Open `RothfussGameDocs\UniversityMapProject\blender_trace_script.py`.
3. Run with `Alt+P`.
4. Check for one root collection named from Archives ground.
5. Confirm you see footprint, rooms, doors, stairs, and labels as separate child collections.

## Headless Blender Test

```powershell
.\RothfussGameDocs\UniversityMapProject\scripts\blender\run_headless_import.ps1
```

If Blender is not on `PATH`, pass `-BlenderExe "C:\Path\To\blender.exe"`.

The preferred automation command is:

```powershell
python .\RothfussGameDocs\UniversityMapProject\run_pipeline.py --building archives --floor ground --stage blender
```

## What Was Removed From The Image-Driven Draft

- Secure staffed counter room
- Scriv office
- Transcription room
- Copying room
- Scriv rest room
- Lamp larder / lamp maintenance room
- Catalogue room as a locked ground-floor room
- Unpacking / acquisitions support room
- Vertical transport shaft
- Internal lantern-roof room
- Detailed staff workflow and back-of-house subdivision

## What Remains Uncertain

- Exact dimensions
- Exact room proportions
- Exact wall thicknesses
- Exact door placements
- Exact stair run, direction, enclosure, and destination
- Exact relationship between Tomes, Scrivs Only, and deeper Stacks beyond threshold logic
