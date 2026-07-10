# Codex Workflows for UniversityMapProject

## Purpose
These workflows are meant to turn the current repo into a repeatable research-and-geometry pipeline rather than a pile of one-off prompts.

---

## Workflow 1 — Audit Repo
Use when starting work or after major changes.

### Goal
Understand current structure, identify drift, and map existing assets to the new authoritative pipeline.

### Steps
1. Print a concise tree of relevant files only.
2. Identify source-of-truth evidence files.
3. Identify schema variants in `floorplans/` and `_3D Map/`.
4. Identify old importers/validators.
5. List contradictions or drift.
6. Propose a minimal migration plan.

### Expected output
- relevant file tree
- contradiction list
- schema mismatch list
- recommended next edits

---

## Workflow 2 — Extract Building Evidence
Use when working on one building.

### Inputs
- lawful book PDFs
- evidence ledger CSVs
- manifest
- building briefs
- reconstruction briefs
- older floor plans and prompts

### Goal
Produce a building-specific evidence pack that distinguishes support levels.

### Steps
1. Search PDFs and ledger for all mentions of the building and named subspaces.
2. Compile a short evidence table.
3. Split findings into:
   - canon
   - implied
   - reconstructed
   - unknown
   - tension
4. Flag anything in prompts/JSON that exceeds the evidence.

### Expected output
- evidence table
- certainty-tagged findings
- contradictions / unknowns
- recommended brief changes

---

## Workflow 3 — Freeze Building Brief
Use once evidence is assembled.

### Goal
Produce or revise a building brief that is safe enough to drive floor planning.

### Required sections
- Canon
- Strong implication
- Reconstructed bridge
- Unknowns
- Hard bans

### Steps
1. Start from existing building brief if present.
2. Compare against manifest and evidence table.
3. Remove unsupported claims.
4. Preserve unresolved issues.
5. Write a concise frozen brief.

### Expected output
- updated building brief
- short change log
- unresolved questions

---

## Workflow 4 — Draft Floor JSON
Use after the building brief is frozen.

### Goal
Produce one floor JSON suitable for validation and Blender blockout.

### Rules
- safer and simpler beats richer and more speculative
- geometry is blockout geometry, not art
- approximate dimensions must be flagged

### Required top-level fields
- building
- floor
- story_role
- footprint
- rooms
- doors
- stairs
- labels
- validation_flags

### Steps
1. Start from brief and evidence, not from image aesthetics.
2. Preserve threshold logic and access hierarchy.
3. Use minimal set of rooms needed to express supported structure.
4. Tag all uncertain elements.
5. Add notes for unresolved geometry.

### Expected output
- floor JSON draft
- list of reconstructed bridges introduced
- list of unresolved uncertainties

---

## Workflow 5 — Validate Floor
Use on every new or revised floor JSON.

### Goal
Catch structure, metadata, and geometry mistakes early.

### Checks
- required keys present
- unique ids
- certainty tags valid
- polygons well formed
- rooms inside footprint
- door refs valid
- stair refs valid
- approximate flags present where dimensions are not sourced
- no banned claims for the building
- no parent/child contradiction with brief or manifest

### Expected output
- pass/fail
- machine-readable errors
- human-readable summary

---

## Workflow 6 — Blender Blockout Import
Use only after validation passes.

### Goal
Turn one authoritative floor JSON into a clean Blender blockout.

### Rules
- target one file, not whole directory
- Z-up orientation
- separate collections for footprint, rooms, doors, stairs, labels
- attach metadata to objects
- no decorative mesh generation

### Expected output
- imported blockout scene
- logs
- optional saved `.blend`

---

## Workflow 7 — Godot Walkable Test
Use after Blender blockout exists.

### Goal
Make the floor explorable with minimal friction.

### Rules
- use collision and simple navigation first
- preserve ids and labels
- do not add loreful decoration by default

### Expected output
- walkable scene
- hotspots or labels
- notes on scale and traversal issues

---

## Workflow 8 — Building Pipeline Run
Use for one complete building/floor pass.

### Example sequence
1. audit relevant files
2. extract building evidence
3. freeze building brief
4. draft floor JSON
5. validate floor
6. import blockout to Blender
7. export or stage for Godot
8. stop and report uncertainties

### Success condition
The result is not “finished architecture.”
The result is an **authoritative, evidence-led, editable blockout source**.
