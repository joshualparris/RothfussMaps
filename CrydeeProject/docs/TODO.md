# TODO

## Immediate

- [x] Fix the V03 Godot stair generation so vertical routes use longer, collision-safe ramps with landings
- [x] Review `scripts/godot/setup_walkthrough_project.py` vertical-link generation against the current player controller
- [x] Add landings and collision-safe stair geometry for cellar, gatehouse walk, magician tower, and Pug-to-Kulgan routes
- [ ] Re-test stair ascent and descent manually in Godot for feel, not just smoke-test validity

## V03 Source-Accuracy Pass

- [x] Create `data/buildings/castle_crydee_site_v03_canon_safe.json` without overwriting V02
- [x] Add site geography:
  town below, gate approach road, sea view, raised castle platform, east clearing, forest edge, west assault field
- [x] Add stronger verticality:
  battlement walk level, gentler stair links, a fuller tower stack, and clearer upper traversal
- [x] Enhance the gate sequence:
  great gate panels, inset door marker, gate towers, and clearer watch context
- [x] Enhance the courtyard and keep front:
  broad keep stairs, large doors, herald balcony, ceremony markers
- [x] Enhance the great hall, service corridor, kitchen, and cellar routes with functional props
- [x] Enhance the magician's tower and Pug-to-Kulgan relationship
- [x] Add certainty-aware route markers and a site legend
- [x] Keep `Launch_Crydee.bat` compatible with the regenerated scene path

## Current Priority

- [ ] Walk the regenerated V03 scene manually and tune stair feel, sprint speed, and fly/respawn ergonomics
- [ ] Expand the town-below and cliff relationship so the approach reads more like a lived frontier site than a context strip
- [ ] Tighten the great hall court arrangement and banner logic against any additional textual evidence
- [ ] Decide whether baseline Crydee and siege-state Crydee should split into separate targets
- [ ] Decide whether the battlement perimeter now wants explicit tower-watch sub-spaces rather than one continuous walk
- [ ] Continue the full Crydee evidence extraction sweep across the novel with more chapter anchors

## Detailed Backlog

- [ ] Work through `docs/SOURCE_ACCURACY_TASKLIST.md` section by section
- [ ] Compare V02 and V03 side by side and keep only the changes that clearly improve source-fit or playability
- [ ] Add a separate review checklist for "canon function vs reconstructed geometry" on every major tower and wall element

## Completed Foundation

- [x] Create scaffold structure for Crydee reconstruction
- [x] Add source audit workflow for `magician_file.pdf`
- [x] Seed an evidence ledger with initial Crydee spatial rows
- [x] Add canon manifest and consistency rules
- [x] Add Castle Crydee brief and reconstruction brief
- [x] Add schema, validator, prompt generator, and pipeline harness
- [x] Add a first working Godot walkthrough scaffold
- [x] Wire the pipeline to the live Crydee floor JSON and Godot project
- [x] Tighten `docs/site-layout.md`
- [x] Improve the current ground-floor blockout beyond the first conservative draft
- [x] Add a real upper-level or tower traversal plan for the gatehouse walk and magician's tower
- [x] Add a playable cellar layer tied to kitchen evidence
- [x] Add a V03 site-accuracy pass with approach context, battlements, and stronger hero routes
- [ ] Review and freeze `buildings/castle-crydee-brief.md`
- [ ] Add chapter references where practical
- [ ] Decide whether the east and west battlements should remain one perimeter route or split into named watch zones

## Later

- [ ] Add Blender import workflow if we want export parity with the University project
- [ ] Split baseline Crydee and siege-state Crydee into separate versioned targets if needed
