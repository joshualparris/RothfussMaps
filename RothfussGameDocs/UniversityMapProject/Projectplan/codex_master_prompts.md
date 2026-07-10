# Codex Master Prompts for UniversityMapProject

## 1) Repo Audit Prompt
```text
You are auditing the UniversityMapProject repo for a canon-constrained Kingkiller Chronicle reconstruction pipeline.

Read AGENTS.md first and obey it strictly.

Tasks:
1. Print a concise file tree of only the relevant research, schema, 3D, and prompt files.
2. Identify current source-of-truth evidence files.
3. Identify schema variants currently in use.
4. Identify importer and validator scripts.
5. Identify contradictions, drift, or over-assertive files.
6. Propose a minimal migration path toward one authoritative floor JSON pipeline.

Rules:
- Be conservative.
- Do not overclaim.
- Do not rewrite large parts of the repo yet.
- Stop after the audit and implementation plan.
```

## 2) Building Evidence Prompt
```text
You are working inside UniversityMapProject.

Read AGENTS.md first and obey it strictly.

Target building: {BUILDING_NAME}

Tasks:
1. Search the lawful book PDFs, evidence ledgers, manifest, building brief, reconstruction brief, existing floorplan JSON, and relevant prompts.
2. Build a concise evidence table for this building.
3. Separate findings into canon, implied, reconstructed, unknown, and tension.
4. Flag any unsupported or over-assertive claims currently present in prompts or JSON.
5. Recommend the smallest safe set of brief revisions.

Output:
- evidence table
- certainty-tagged findings
- contradictions and unresolveds
- brief revision recommendations
```

## 3) Floor JSON Prompt
```text
You are working inside UniversityMapProject.

Read AGENTS.md first and obey it strictly.

Target building: {BUILDING_NAME}
Target floor: {FLOOR_NAME}

Goal:
Produce or revise one canon-safe floor JSON suitable for validation and Blender blockout.

Rules:
- Prefer simpler safer geometry over richer speculation.
- Preserve threshold logic, access hierarchy, and named canon spaces.
- Strip unsupported support rooms unless absolutely necessary.
- Mark approximate dimensions and uncertain placements explicitly.
- Use top-level fields:
  - building
  - floor
  - story_role
  - footprint
  - rooms
  - doors
  - stairs
  - labels
  - validation_flags

Before writing JSON:
1. Summarize the strongest supported floor elements.
2. List what remains uncertain.
3. List any reconstructed bridges you plan to introduce.

Then write the JSON.
Then provide a short postscript:
- what was removed from earlier drafts
- what remains uncertain
- what should happen next
```

## 4) Validator + Blender Prompt
```text
You are working inside UniversityMapProject.

Read AGENTS.md first and obey it strictly.

Task:
Implement or refactor the validator and Blender importer for the authoritative floor JSON pipeline.

Requirements:
- validator checks required keys, unique ids, certainty tags, polygon validity, containment, reference integrity, and obvious contradictions
- Blender importer targets one JSON file passed as argument
- Blender importer uses Z-up logic
- Blender importer creates clean collections for footprint, rooms, doors, stairs, labels
- metadata such as certainty, notes, and source refs are preserved on imported objects
- avoid unrelated repo edits

Output:
- list of files changed
- short explanation of design choices
- command examples to run validation and import
```

## 5) Full Building Pipeline Prompt
```text
You are running one building/floor pipeline inside UniversityMapProject.

Read AGENTS.md first and obey it strictly.

Target building: {BUILDING_NAME}
Target floor: {FLOOR_NAME}

Execute this sequence:
1. audit relevant files only
2. extract evidence
3. revise or confirm building brief
4. draft or revise floor JSON
5. validate floor JSON
6. import blockout in Blender pipeline files
7. prepare minimal Godot-ready handoff notes

Rules:
- stop at review gates if the evidence is thin or contradictory
- do not silently invent geometry
- do not treat image outputs as authoritative
- prefer TODOs and uncertainty notes over fake precision

End with:
- what changed
- what remains uncertain
- whether the floor is safe to freeze
- exact next command to run
```
