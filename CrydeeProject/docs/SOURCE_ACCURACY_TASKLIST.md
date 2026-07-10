# Castle Crydee Source Accuracy Tasklist

Status: active Codex backlog

Purpose: turn the current Crydee audit into explicit, actionable tasks for future Codex passes. This backlog is for improving both source accuracy and Godot walkability without hiding uncertainty.

## Working Goal

- [ ] Push Crydee toward maximum source accuracy, while keeping all unresolved geometry marked as `implied` or `reconstructed` instead of `canon`.
- [ ] Improve the playable Godot prototype from a flat blockout into a more believable Castle Crydee site with defensible routes, topography, and lived-in spaces.

## Immediate Playability Blockers

- [ ] Fix stairs that are currently impossible or unreliable to walk in Godot.
- [ ] Inspect the vertical-link generation in `scripts/godot/setup_walkthrough_project.py`.
- [ ] Check whether each stair ramp is too steep for `CharacterBody3D` floor settings.
- [ ] Check whether visible stair treads, ceilings, or nearby walls are clipping into the player path.
- [ ] Add safe landings at the base and top of each major stair route.
- [ ] Re-test `cellar_descent`, `west_gate_tower_to_walk`, and `magician_tower_stair_link` in-editor.
- [ ] Add an explicit stair walkability smoke-test checklist to the Godot verification workflow.

## Priority 1: Build The Site, Not Just The Castle

- [ ] Add a town-below approach zone to the authoritative Crydee layout.
- [ ] Add a road or approach path that leads toward the great gate.
- [ ] Add an outside-to-inside route:
  town below -> road/gate approach -> great gate -> courtyard -> broad keep stairs -> great hall.
- [ ] Move the default play start to a route that shows Crydee as a place, not only as a plan.
- [ ] Keep all new site geography clearly marked as reconstructed unless directly supported by the novel.

## Priority 2: Add Topography

- [ ] Raise the castle platform so Crydee no longer reads as a flat test slab.
- [ ] Add the town-below height relationship.
- [ ] Add sea-facing or bluff-facing context on the castle side that needs it.
- [ ] Add forest-side context to the east.
- [ ] Add the broad clearing beyond the east wall.
- [ ] Preserve orientation anchors for west wall, east wall, town, and sea-facing views.

## Priority 3: Rebuild The Gate Scene

- [ ] Make the great gate visually distinct from the smaller inset postern.
- [ ] Rebuild the gatehouse passage so it feels like a real defensive threshold.
- [ ] Make at least one gate tower clearly readable as the gate watch location.
- [ ] Add a believable guard response path from gate/tower into the courtyard.
- [ ] Add a view back toward town and the lower approach through or near the gate.
- [ ] Keep twin-gate-tower symmetry marked reconstructed unless stronger text support appears.

## Priority 4: Rebuild The Courtyard And Keep Front

- [ ] Turn the keep stair landing into actual broad, walkable stairs rather than only a marker.
- [ ] Make the large keep doors prominent.
- [ ] Add a readable balcony overlooking the courtyard.
- [ ] Increase the sense that the courtyard can host the Choosing and Banapis gatherings.
- [ ] Add feast-state props as an optional variant:
  tables, ale casks, movement room, and clear sightlines to keep stairs.
- [ ] Keep a clean ceremonial route from the great gate to the foot of the keep stairs.

## Priority 5: Rebuild The Kitchen-Service Spine

- [ ] Make the great hall to kitchen path into a hero route.
- [ ] Add the long service corridor as a real navigable corridor, not just a label.
- [ ] Add a dishware or goblet table along the corridor wall.
- [ ] Add a servants' alcove or curtained service break if it can be justified without overclaiming canon.
- [ ] Keep storage-room adjacency tied to the kitchen/private-route evidence.
- [ ] Make cellar access feel like it belongs to the kitchen-service network.

## Priority 6: Make The Magician's Tower Feel Right

- [ ] Confirm the magician's tower remains the northmost tower in the current reconstruction logic.
- [ ] Preserve the kitchen shortcut route to the tower.
- [ ] Make the tower vertical route feel narrow, quiet, and solitary.
- [ ] Add a modest apprentice-scale room below Kulgan's implied upper space.
- [ ] Add a tower window or view cue so it feels like a tower, not a flat labeled room.
- [ ] Avoid making the magician's tower feel grander than the book supports.

## Priority 7: Add Defensive Wall-Walks

- [ ] Build a real west wall walkable route.
- [ ] Build an east wall walkable route or a clearly staged prototype of one.
- [ ] Add battlements and merlons rather than plain flat wall boxes.
- [ ] Add a courtyard-to-wall stair route.
- [ ] Add at least one defensible watch/bell location on the wall system.
- [ ] Preserve the broad clearing outside the east wall in the site context.
- [ ] Decide whether siege-state wall features belong in the baseline layout or a separate target.

## Room-By-Room Tasks

### Great Gate Passage

- [ ] Add the large gate leaves visually.
- [ ] Add the smaller postern visibly within or beside the main gate treatment.

### Gate Towers

- [ ] Keep one gate tower as a strong canon-supported watch anchor.
- [ ] Treat any mirrored second gate tower as reconstructed until more evidence appears.

### Courtyard

- [ ] Rebalance scale for ceremony, guard traffic, and feast use.
- [ ] Improve sightline to keep stairs and balcony.

### Keep Stair Landing

- [ ] Replace the current marker-first solution with stairs that are both readable and climbable.

### Great Hall

- [ ] Add a dais or court-facing arrangement.
- [ ] Preserve audience space for nobles, merchants, and townsfolk.

### Inner Hall

- [ ] Keep it marked reconstructed.
- [ ] Use it only as needed to support real source-backed circulation.

### Council Chamber

- [ ] Add a council table and private-meeting atmosphere.

### Ducal Private Hall

- [ ] Keep it implied rather than overconfident.
- [ ] Tie it to the post-council private-quarters route.

### Princess Garden

- [ ] Add the three steps up.
- [ ] Add a stone bench.
- [ ] Add hedges or rosebushes that screen most of the courtyard while preserving limited sight to the high walls.

### Storage Room

- [ ] Keep it tied to the private-route-to-kitchen evidence.

### Service Corridor

- [ ] Make it long, useful, and visually distinct from the great hall.

### Kitchen

- [ ] Make it feel busy and workmanlike.
- [ ] Preserve links to courtyard, cellar access, and magician's tower shortcut.

### Pantry

- [ ] Keep it marked implied unless stronger text support is found.

### Cellar Access And Cellars

- [ ] Make descent believable and traversable.
- [ ] Distinguish stores, ale storage, and refuge use more clearly.

### Magician Tower Base And Upper Room

- [ ] Make the base-to-room climb feel real.
- [ ] Preserve kitchen-side access logic.

### Stables

- [ ] Model the wall-behind-stables route.
- [ ] Keep exact stable placement marked reconstructed.

### Barracks And Armory

- [ ] Differentiate sleeping/garrison space from weapons storage.
- [ ] Keep the armory near the military wing.

### West And East Walls

- [ ] Make the orientation matter in the playable site.
- [ ] Support future siege-state logic without silently turning it into canon.

## Site Geography Tasks

- [ ] Add sea or horizon cues where Crydee should feel coastal.
- [ ] Add a clear town-below relationship.
- [ ] Add bluff or cliff logic where needed.
- [ ] Add forest-side context.
- [ ] Add direction cues for Sailor's Grief and the Six Sisters only if they can be added without fake precision.

## Defensive Accuracy Tasks

- [ ] Replace symbolic wall boxes with readable battlement logic.
- [ ] Add wall-walk width and defensive movement routes.
- [ ] Add merlons or parapet rhythm to key walls.
- [ ] Add siege-compatible access paths without mixing siege-state damage into the baseline unless versioned.

## Godot Walkthrough Immersion Tasks

- [ ] Make the playable route begin with a stronger Crydee arrival sequence.
- [ ] Reduce the debug-map feeling created by oversized flat slabs and labels.
- [ ] Replace temporary marker-first solutions where they block immersion.
- [ ] Keep future art passes subordinate to layout truth.

## Source-Accuracy Guardrails

- [ ] Never promote unknown tower count to canon.
- [ ] Never present exact geometry as canon when the novel does not support it.
- [ ] Keep baseline Crydee and siege-state Crydee separate if the layouts materially diverge.
- [ ] Use reference images for mood only unless they are proven source-authorized.
- [ ] Prefer practical frontier-ducal architecture over oversized fantasy-palace drift.

## Completion Targets

- [ ] Raise floor-plan logic from the current blockout level toward 8/10 or better.
- [ ] Raise Godot walkthrough immersion toward 8/10 or better.
- [ ] Make the next major rebuild pass feel like Castle Crydee rather than a labelled prototype.

