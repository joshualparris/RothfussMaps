# Crydee Project

This workflow is built to reconstruct Castle Crydee as accurately and consistently as possible from `Magician` before any image model or 3D tool is allowed to decide the layout.

## Best Workflow

1. Audit the lawful source PDF and confirm text extractability.
2. Build an evidence ledger from the novel, using short paraphrases and page references.
3. Separate each clue into:
   - `Tier 1`: directly confirmed
   - `Tier 2`: strongly implied
   - `Tier 3`: design inference needed to make the site usable
4. Freeze the site layout before touching detailed room or wall geometry.
5. Freeze the Castle Crydee brief before touching structure JSON.
6. Freeze the first structure JSON before touching Blender or Godot.

If you skip those freeze points, later prompts and blockouts will drift.

## Why Direct Image Generation Is Weak

Image models are good at atmosphere and presentation, but weak at:

- preserving exact wall and gate relationships
- keeping one castle layout consistent across multiple generations
- separating peacetime layout from siege-time action beats
- retaining uncertainty where the novel is vague

Use image generation only after the evidence and structure are locked.

## Folder Contents

- `evidence/evidence-ledger.csv`
  Working Crydee evidence ledger with seed rows already added.
- `evidence/canon_manifest.json`
  High-value Crydee claims and guardrails.
- `docs/site-layout.md`
  Working layout synthesis for the castle-and-town site.
- `docs/SOURCE_ACCURACY_TASKLIST.md`
  Actionable Codex backlog derived from the current source-accuracy audit.
- `docs/SOURCE_ACCURACY_AUDIT_V03.md`
  Audit of what the V03 source-accuracy pass improved and what still remains reconstructed.
- `buildings/castle-crydee-brief.md`
  First restrained brief for the castle reconstruction.
- `reconstruction-briefs/castle-crydee-reconstruction.md`
  Longer brief that can grow into the eventual blockout plan.
- `schemas/canon_structure_plan_v01.schema.json`
  Planned structure contract for future validated geometry.
- `scripts/source_audit.py`
  Generates the PDF source audit from the Crydee novel file.
- `scripts/generate_prompt.py`
  Generates evidence-based prompts for site, structure, level, and room passes.
- `scripts/validate_repo.py`
  Checks the scaffold and evidence files are present and coherent.

## Recommended Pipeline

### Phase 1: Source Audit

Confirm:

- the source PDF exists
- the PDF is machine-readable
- page count and metadata are stable
- search terms like `Crydee`, `Castle Crydee`, `great hall`, and `west wall` are extractable

### Phase 2: Evidence Extraction

Track every reference to:

- the keep
- the great hall
- the courtyard
- the gate and gate sequence
- the walls, towers, and battlements
- the stables and service edge
- the town below the castle
- sea, cliffs, and approach routes where clearly supported

### Phase 3: Site Synthesis

Use the ledger to answer:

- Which zones definitely exist?
- Which zones are adjacent?
- Which routes are sequence-based rather than direction-based?
- Which details belong to peacetime layout versus wartime action?
- Which unknowns must stay unresolved?

### Phase 4: Structure Brief

For Castle Crydee, create a brief with:

- locked canon
- strong implication
- explicit reconstruction bridges
- entrances and circulation
- defensive logic
- hard bans

### Phase 5: Structure JSON

Only after the site layout is frozen should we draft the first structure JSON target. That file will become the first authoritative geometry source for later 3D work.

## Quick Start

1. Run `python .\CrydeeProject\run_pipeline.py --stage source-audit`
2. Review `docs/SOURCE_AUDIT.md`
3. Review `docs/SOURCE_ACCURACY_TASKLIST.md`
4. Expand `evidence/evidence-ledger.csv`
5. Review `docs/site-layout.md`
6. Tighten `buildings/castle-crydee-brief.md`
7. Freeze the first structure target only when the evidence supports it
