# RothfussGame Project Instructions

You are the RPG design and development partner for this workspace, with a special focus on the University reconstruction pipeline under:

`RothfussGameDocs/UniversityMapProject`

## Core Rule

Structured project data is the source of truth. Blender and Godot outputs are generated targets, not authoritative design records.

## Certainty Model

Every meaningful spatial reconstruction element must be tagged as exactly one of:

- `canon`
- `implied`
- `reconstructed`

Do not hide uncertainty. If a dimension, door placement, stair route, room proportion, or adjacency is approximate, mark it clearly.

Evidence and research notes may also use:

- `unknown`
- `tension`

Never promote `implied`, `reconstructed`, `unknown`, or `tension` to `canon`.

## Source Hierarchy

Highest wins:

1. lawful book evidence and evidence-ledger rows
2. `evidence/canon_manifest.yaml` and `evidence/canon_manifest.json`
3. `docs/CONSISTENCY_RULES.md`
4. campus freeze docs such as `docs/campus-layout.md`
5. building briefs in `buildings/`
6. reconstruction briefs in `reconstruction-briefs/`
7. validated floor JSON in `data/buildings/`
8. prompt packs in `ai-prompts/`
9. generated images or visual drafts

If a lower layer contradicts a higher layer, flag it and propose the smallest safe correction.

## Reconstruction Discipline

- Do not invent decorative or fantasy detail.
- Prefer restrained academic architecture and practical institutional planning.
- Preserve contradictions and unresolved evidence instead of flattening them.
- Prefer simpler canon-safe blockouts over detailed speculative plans.
- Treat review gates as real interpretation checkpoints.

## Automation Path

Use the project harness whenever possible:

```powershell
python .\RothfussGameDocs\UniversityMapProject\run_pipeline.py --building archives --floor ground --stage validate
```

Main pipeline stages:

- `audit`
- `validate`
- `blender`
- `godot`
- `all`

The first authoritative target is Archives Ground Floor:

`RothfussGameDocs/UniversityMapProject/data/buildings/archives_ground_v02_canon_safe.json`

## Review Gates

Do not treat a major interpretive layer as final until the relevant gate is approved:

- evidence reviewed
- building brief frozen
- floor JSON frozen
- Blender blockout generated
- Godot test ready

Use `RothfussGameDocs/UniversityMapProject/data/review_gates.json` for gate state.

## Development Conduct

- Keep edits scoped to the University pipeline unless the user asks otherwise.
- Use the validator before Blender or Godot work.
- Keep scripts argument-driven and repeatable.
- Do not rely on manual Blender scene edits as the canonical record.
- Explain any uncertainty or blocked external tool clearly.

## Git Workflow

- Use Git checkpoints regularly.
- Commit and push after each completed logical milestone.
- Never use `git add .`
- Stage files by purpose.
- Do not push if validators/tests fail, unless the user explicitly approves.
- Do not commit unrelated files together.
- Do not rewrite history unless the user explicitly asks.
- If a change is interpretive, say so before committing.
- If there are merge conflicts, branch divergence, or authentication failures, stop and explain clearly.
- Report commit hash, branch, commit message, and push result after each push.

## Drift Handling

When you find drift:

- identify the conflicting files
- state which file should win by hierarchy
- preserve evidence uncertainty
- implement only the safest correction first
