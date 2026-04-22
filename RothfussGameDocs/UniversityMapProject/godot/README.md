# Godot Walkthrough Scaffold

This is a generated Godot 4 walkthrough scaffold for the University blockout pipeline.

Source JSON:

`RothfussGameDocs/UniversityMapProject/data/buildings/archives_ground_v02_canon_safe.json`

Current walkthrough scene:

`res://scenes/archives_ground_walkthrough.tscn`

The scene is now generated as native Godot CSG from the source JSON, so it is visible in the editor and includes simple floor/wall collision. The old imported GLB can still exist at:

`res://assets/archives_ground_v02_canon_safe.glb`

This scene includes reconstructed upper Archives levels and playable stair links between them. Stairs are implemented as shallow collision ramps with visual treads so walking up and down is reliable in Godot.

Controls:

- WASD: move
- Mouse: look
- Left click: recapture mouse after pressing Esc
- Space: jump
- Esc: release mouse

Open the project, press Play, click into the game window if needed, then use WASD.
