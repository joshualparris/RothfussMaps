# AGENTS.md

## Project
Kingkiller Chronicle University Reconstruction

This repo reconstructs the University from *The Name of the Wind* and *The Wise Man's Fear* into a canon-constrained, structured spatial model that can later be rendered in Blender and explored in Godot.

The authoritative goal is **not** pretty images.
The authoritative goal is **source-of-truth structured reconstruction**.

This project must remain:
- canon-constrained
- uncertainty-aware
- architecture-first
- repeatable
- conservative

## Prime Directive
Do **not** invent details beyond what canon, strong implication, or explicitly flagged reconstruction supports.

Whenever uncertainty exists:
- preserve it
- label it
- log it
- do not silently flatten it into a neat answer

## Certainty Model
Use these tags consistently:

- `canon` = directly supported by text evidence or frozen high-priority evidence artifacts
- `implied` = strongly supported by multiple cues or by unavoidable reading of canon facts
- `reconstructed` = practical bridge required to make a usable spatial plan
- `unknown` = unresolved and must stay unresolved
- `tension` = project evidence conflicts and neither side should be silently discarded

Never present `implied`, `reconstructed`, `unknown`, or `tension` as `canon`.

## Source Hierarchy
Highest wins.

1. Lawful book evidence and evidence-ledger rows
2. `canon_manifest.yaml` / `canon_manifest.json`
3. `CONSISTENCY_RULES.md`
4. campus freeze documents such as `campus-layout.md`
5. building briefs in `buildings/`
6. reconstruction briefs in `reconstruction-briefs/`
7. floor JSON in `floorplans/` or `_3D Map/`
8. AI prompts in `ai-prompts/`
9. generated images

If a lower layer contradicts a higher layer:
- do not smooth over it
- flag it
- rewrite the lower layer
- document the change briefly

## Current Repo-Specific Ground Truth
These files already matter and should be consulted early:

- `The_Name_of_Wind.pdf`
- `The_Wise_Man's_Fear.pdf` if present in repo later
- `university-evidence-ledger-v3.csv`
- `university-evidence-summary-v3.md`
- `canon_manifest.yaml`
- `canon_manifest.json`
- `CONSISTENCY_RULES.md`
- `campus-layout.md`
- `buildings/*.md`
- `reconstruction-briefs/*.md`
- `floorplans/*.json`
- `_3D Map/*`
- `validate_repo.py`

Also check older files for drift:
- `university-evidence-ledger-v1.csv`
- `university-evidence-ledger-v2.csv`
- `evidence-ledger.csv`
- older briefs and prompt packs

## Frozen Project Philosophy
The pipeline should be:

1. extract evidence
2. log constraints
3. freeze building brief
4. draft floor JSON
5. validate
6. import to Blender blockout
7. export to Godot

Do not jump directly from PDFs to final geometry without preserving intermediate evidence and certainty tags.

## Architecture and Aesthetic Rules
Prefer:
- restrained academic architecture
- practical institutional planning
- structural clarity
- believable circulation
- harsh preservation logic where relevant

Avoid:
- fantasy spectacle
- decorative invention
- cinematic flourishes
- “cool” details not supported by evidence
- modern design assumptions unless explicitly marked as reconstructed

## Working Method
When asked to work on a building or floor:

1. find all evidence first
2. produce a short evidence table
3. separate `canon` / `implied` / `reconstructed` / `unknown`
4. identify conflicts
5. draft or revise the building brief
6. draft or revise structured JSON
7. validate geometry and metadata
8. only then touch Blender or Godot assets

## Required Behaviour for Scholarly Tasks
When reading book evidence:
- prefer short paraphrase plus citation or locator
- do not overquote copyrighted text
- separate observation from interpretation
- preserve sequence logic, threshold logic, and access logic carefully

When there is no precise dimensional data:
- use approximate dimensions only when needed for blockout
- mark them as approximate
- explain why they were introduced

When an image or prompt disagrees with evidence:
- trust evidence
- not the image

## Required Behaviour for JSON / Schema Tasks
Structured floor files should prefer these top-level fields when possible:
- `building`
- `floor`
- `story_role`
- `footprint`
- `rooms`
- `doors`
- `stairs`
- `labels`
- `validation_flags`

Each space-like entity should include where relevant:
- `id`
- `label`
- `certainty`
- `polygon` or equivalent geometry
- `notes`
- `source_refs`
- `access`

If older schemas are encountered:
- do not destroy them casually
- write migration notes
- prefer adapters or migration scripts

## Required Behaviour for Blender Tasks
Blender outputs are for **blockout verification**, not final art.

Rules:
- use one authoritative JSON target file at a time
- avoid importing every file in a folder unless explicitly requested
- use Blender-friendly Z-up logic
- preserve object metadata such as certainty and notes
- name objects predictably
- keep collections clean and separated

## Required Behaviour for Godot Tasks
Godot outputs are for exploratory walking, not visual polish.

Rules:
- preserve building and room ids
- preserve labels/hotspots
- keep navigation simple
- use blockout meshes and collision first
- do not add decorative props unless the user explicitly requests them

## Review Gates
For high-impact tasks, stop for review after:
- campus freeze changes
- building brief freezes
- floor plan freezes
- schema migrations
- importer refactors that change geometry interpretation

## What To Do When You Find Drift
If you find repo drift:
- identify the conflicting files
- say which file should win by hierarchy
- propose a minimal correction
- implement only the safest correction first

## Current First-Building Priority
First authoritative technical target:
- Archives
- Ground Floor

Strong elements to preserve there:
- square outer shell
- no windows
- single main entrance
- antechamber
- Tomes
- Scrivs Only route
- Stacks threshold
- lower-stacks stair logic
- public / restricted threshold hierarchy

## Output Style
Be direct.
Be structured.
Do not waffle.
Do not overclaim certainty.
Prefer conservative notes over fake precision.
