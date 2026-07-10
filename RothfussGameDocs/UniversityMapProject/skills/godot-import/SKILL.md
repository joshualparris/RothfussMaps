# Godot Import

Use this workflow after Blender has generated a GLB blockout.

## Command

```powershell
python .\RothfussGameDocs\UniversityMapProject\run_pipeline.py --building archives --floor ground --stage godot
```

## Output

The stage creates or refreshes:

- `godot/project.godot`
- `godot/scenes/player.tscn`
- `godot/scenes/archives_ground_walkthrough.tscn`
- `godot/scripts/player_controller.gd`

## Rules

- JSON remains the source of truth.
- Godot scene is for walking scale, collision testing, and atmosphere checks.
- Collision must be reviewed after import; do not assume generated collision is final.

## Review Gate

Requires `blender_blockout_generated`.

Updates `godot_test_ready` when the scaffold and asset path are ready.

