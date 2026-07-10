# Crydee Method

This project now follows a practical book-to-walkthrough flow for Castle Crydee.

## Current Live Path

1. Use `magician_file.pdf` as the lawful source.
2. Extract spatial evidence into the Crydee ledgers and summaries.
3. Keep the evidence and canon manifest as the authority.
4. Maintain the draft walkable blockout in:
   - `data/buildings/castle_crydee_ground_v02_canon_safe.json`
5. Validate that JSON before regeneration.
6. Regenerate the Godot walkthrough from the JSON.
7. Open the Godot project and test first-person movement.

## Source Of Truth

For the current prototype, the main geometry source is:

- `data/buildings/castle_crydee_ground_v02_canon_safe.json`

Godot scenes are generated outputs, not the authoritative design record.

## Main Commands

Run the full current pipeline:

```powershell
python .\CrydeeProject\run_pipeline.py --stage all --force
```

Validate the current Crydee floor JSON only:

```powershell
python .\CrydeeProject\scripts\validate_floor_plan.py .\CrydeeProject\data\buildings\castle_crydee_ground_v02_canon_safe.json
```

Regenerate the Godot walkthrough only:

```powershell
python .\CrydeeProject\run_pipeline.py --stage godot --force
```

Open the Godot project:

```powershell
.\CrydeeProject\Godot_v4.6.2-stable_win64.exe\Godot_v4.6.2-stable_win64.exe --path .\CrydeeProject\godot
```

## Current Walkthrough

- Godot project: `godot/project.godot`
- Main scene: `godot/scenes/castle_crydee_ground_walkthrough.tscn`
- Player controller: `godot/scripts/player_controller.gd`

Controls:

- `WASD` move
- mouse look
- `Space` jump
- `Esc` release mouse

## What Is True Right Now

- The Crydee walkthrough is generated as native Godot CSG from the JSON.
- The current blockout is conservative and approximate, but it now covers more of the castle than the first prototype.
- The current playable target includes a cellar descent, a gatehouse watch level, and the magician's tower room.
- The prototype is working, but it is not a final canon architecture lock.

## Next Improvement Targets

- expand evidence coverage from the novel
- tighten the site layout and brief
- decide whether east and west battlements become full wall-walk routes
- review whether the keep front and balcony should split into a more explicit upper keep facade layer
- later, add Blender parity only if it helps the project
