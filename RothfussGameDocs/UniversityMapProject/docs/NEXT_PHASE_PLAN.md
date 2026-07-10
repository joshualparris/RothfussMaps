# Next Phase Plan

## Phase 1: Archives Ground Lock

- Run `run_pipeline.py --stage audit`.
- Run `run_pipeline.py --stage validate`.
- Review Archives evidence and update `evidence_reviewed`.
- Review `buildings/archives-brief.md` and update `building_brief_frozen`.
- Keep `floor_json_frozen` as `approved_for_blockout` unless geometry changes materially.

## Phase 2: Blender Blockout

- Install Blender or pass `--blender-exe`.
- Run `run_pipeline.py --stage blender`.
- Confirm generated `.blend` and `.glb`.
- Review scale, axis mapping, room zones, and labels.

## Phase 3: Godot Walkthrough

- Run `run_pipeline.py --stage godot`.
- Open `godot/project.godot`.
- Check imported GLB, player scale, camera height, collision, and navigation.

## Phase 4: Archives Expansion

- Draft lower Archives and upper floor JSON only after brief and evidence gates are reviewed.
- Keep deep Stacks, Puppet, Underthing links, and four-plate door as separate gated interpretation passes.

## Phase 5: Other Buildings

- Repeat the same pipeline for Mews, Hollows, Masters Hall, Medica, Mess, and other University structures.
- Do not merge campus layout automation until building-level contracts are stable.

