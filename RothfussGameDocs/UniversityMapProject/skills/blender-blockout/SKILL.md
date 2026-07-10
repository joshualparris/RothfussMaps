# Blender Blockout

Use this workflow only after validation passes and the floor JSON review gate allows blockout generation.

## Command

```powershell
python .\RothfussGameDocs\UniversityMapProject\run_pipeline.py --building archives --floor ground --stage blender
```

If Blender is not on PATH:

```powershell
python .\RothfussGameDocs\UniversityMapProject\run_pipeline.py --building archives --floor ground --stage blender --blender-exe "C:\Path\To\blender.exe"
```

## Rules

- Import one JSON file only.
- Use JSON `x/z` as Blender `x/y`; Blender `z` is vertical.
- Generate blockout geometry, not final art.
- Keep object metadata for certainty, notes, and source JSON.

## Review Gate

Requires `floor_json_frozen`.

Updates `blender_blockout_generated` after successful command-line generation.

