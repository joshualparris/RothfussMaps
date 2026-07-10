# Crydee Reconstruction Pipeline

This project is a canon-constrained reconstruction pipeline for Castle Crydee and its immediate settlement context from Raymond E. Feist's `Magician`. The source of truth is structured evidence and structured project data, not Blender scenes, Godot scenes, or image-model outputs.

## Current Scope

The working scope for this first phase is:

- Castle Crydee proper
- the keep and great hall
- the courtyard and gate sequence
- the walls, towers, battlements, and stable-side access
- the town below the castle where evidence supports it

The wider Duchy of Crydee, forest roads, and regional military geography may be added later, but they are not the first reconstruction target.

## Source Of Truth

Highest authority wins:

1. lawful text evidence and evidence-ledger rows
2. `evidence/canon_manifest.json`
3. `docs/CONSISTENCY_RULES.md`
4. `docs/site-layout.md`
5. `buildings/`
6. `reconstruction-briefs/`
7. `data/structures/`
8. `ai-prompts/`
9. generated images or future 3D outputs

## Certainty Model

Every meaningful reconstruction element should be tagged as one of:

- `canon`
- `implied`
- `reconstructed`

Research notes may also use:

- `unknown`
- `tension`

Do not silently promote uncertain material into canon.

## Folder Layout

- `evidence/` - ledgers, manifests, and extraction templates
- `docs/` - workflow notes, source audit, consistency rules, and planning docs
- `buildings/` - frozen structure briefs
- `reconstruction-briefs/` - longer design-and-reconstruction briefs
- `data/structures/` - future authoritative structure JSON targets
- `schemas/` - structure JSON contracts
- `scripts/` - source auditing, prompt generation, and repo validation helpers
- `templates/` - repeatable decision and JSON templates
- `ai-prompts/` - visualization prompts derived from frozen structure, not the reverse
- `logs/` - machine-generated audit outputs
- `exports/` - future Blender and Godot outputs

## Current State

This project now has a working first-person Godot prototype path. We have:

- a source PDF audit path
- an expanded Crydee evidence ledger covering the gate, court, keep front, service wings, cellars, and tower clues
- a Castle Crydee brief and tightened site-layout draft
- a versioned canonical-safe Crydee ground-floor JSON target with restrained cellar and upper-access layers
- a Godot walkthrough scaffold generated from JSON
- a lightweight pipeline harness that can validate and regenerate the walkthrough

We do not yet have:

- a frozen site layout
- a final canon architecture lock
- a full wall-walk or multi-tower circulation model
- a production-quality art pass
- a Blender-backed export path that the Crydee harness actively uses

That restraint is deliberate. The current walkthrough is a conservative blockout prototype, not a final reconstruction.

## Pipeline Harness

Run a source audit:

```powershell
python .\CrydeeProject\run_pipeline.py --stage source-audit
```

Run a scaffold audit:

```powershell
python .\CrydeeProject\run_pipeline.py --stage audit
```

Show review gates:

```powershell
python .\CrydeeProject\run_pipeline.py --show-gates
```

Update a gate:

```powershell
python .\CrydeeProject\run_pipeline.py --approve-gate evidence_ledger_started --gate-status approved --note "Initial Crydee evidence pass reviewed."
```

Run the full current prototype pipeline:

```powershell
python .\CrydeeProject\run_pipeline.py --stage all --force
```

## Prompt Workflow

Generate a conservative site prompt from the evidence ledger:

```powershell
python .\CrydeeProject\scripts\generate_prompt.py --csv .\CrydeeProject\evidence\evidence-ledger.csv --mode site --target "Castle Crydee"
```

## Next Milestone

The next real milestone is not basic walkability anymore. It is fidelity: continue the evidence pass, decide how far the battlements should become playable, and then split baseline Crydee from siege-state Crydee if the later war chapters demand a second versioned target.
