# Validate Floor

Use this workflow before any Blender or Godot work.

## Command

```powershell
python .\RothfussGameDocs\UniversityMapProject\run_pipeline.py --building archives --floor ground --stage validate
```

## Checks

The validator checks:

- required keys
- certainty tags
- duplicate ids
- polygon validity
- room containment
- door references
- stair references
- draft and approximation flags
- obvious geometry contradictions

## Rule

If validation fails, fix the JSON or schema assumption before importing to Blender.

