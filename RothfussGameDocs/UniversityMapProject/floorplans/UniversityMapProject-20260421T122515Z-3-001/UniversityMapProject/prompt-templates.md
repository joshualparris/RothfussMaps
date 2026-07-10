# Prompt Templates

These are meant for text models first. Use image models only after the structured pass is complete.

## 1. Quote Extraction Prompt

```text
I am reconstructing the University from canon evidence for a game project.

I will give you one short excerpt or paraphrased passage at a time from a lawful copy of the books.
Your job is to convert it into structured spatial evidence only.

Rules:
- Do not invent architecture.
- Do not smooth over ambiguity.
- If the passage does not support a spatial claim, say "no usable spatial evidence".
- Separate direct evidence from implication.
- Keep output compact.

Return this JSON:
{
  "usable": true,
  "primary_location": "",
  "secondary_location": "",
  "constraint_type": "adjacency | direction | route | exterior_trait | interior_trait | access | environment | sequence",
  "constraint_statement": "",
  "certainty_tier": "Tier 1 | Tier 2 | Tier 3",
  "paraphrase": "",
  "negative_constraint": "",
  "notes": ""
}
```

## 2. Campus Synthesis Prompt

```text
You are acting as a canon cartographer for the Kingkiller Chronicle University project.

I will provide a ledger of spatial evidence gathered from TNOTW and TWMF.
Your job is to synthesize a campus layout without inventing unsupported facts.

Rules:
- Use only the evidence I provide.
- If evidence conflicts, preserve the conflict and propose the cleanest explicit interpretation.
- Mark all unsupported details as UNKNOWN.
- Separate canon-confirmed, canon-implied, and design-inferred statements.
- Do not write prose summary first. Start with constraints.

Output exactly in this order:
1. Locked campus constraints
2. Contradictions or ambiguities
3. Proposed campus layout logic
4. Explicit design inferences
5. A clean adjacency list
6. A compact campus blueprint brief for later image generation
```

## 3. Building Brief Prompt

```text
You are building a single authoritative building brief for the University project.

Target building: [BUILDING NAME]

I will provide only the evidence rows relevant to this building.
Your job is to create a building brief that is internally consistent and safe for later floor-plan generation.

Rules:
- Do not invent exact dimensions unless I explicitly give them.
- Keep the building faithful to the mood and logic of the books.
- Distinguish between confirmed, implied, and inferred.
- Include banned features where evidence rules something out.
- If evidence is thin, produce a conservative brief instead of a flashy one.

Output exactly in this order:
1. Building identity
2. Confirmed facts
3. Implied facts
4. Explicit design inferences
5. Exterior shell
6. Entrances and circulation
7. Required room functions
8. Hard bans
9. Open questions
10. Final frozen brief
```

## 4. Floor Plan Prompt

```text
You are producing a structured floor plan specification, not concept art.

Target building: [BUILDING NAME]

I will provide the frozen building brief and evidence notes.

Rules:
- Prioritize adjacency, circulation, and access logic over aesthetics.
- Do not add decorative rooms just to make the plan look richer.
- If the number of floors is unknown, give the minimum plausible count and mark it as inferred.
- Keep north fixed at the top.
- Preserve all banned assumptions.

Output exactly in this order:
1. Floor count decision
2. Per-floor room list
3. Room adjacency rules
4. Vertical movement rules
5. Restricted areas
6. Unknowns still unresolved
7. JSON matching my floorplan schema
8. A final image-generation prompt for a clean top-down blueprint using only the frozen structure
```

## 5. Room Prompt

```text
You are producing one room specification inside a frozen building and floor plan.

Target room: [ROOM NAME]
Building: [BUILDING NAME]
Floor: [FLOOR ID]

I will provide:
- the building brief
- the floor plan spec
- all known room constraints

Rules:
- This room must fit the existing floor plan exactly.
- Do not move doors, stairs, or neighboring rooms.
- Keep function first.
- Respect tone, class use, social status, and likely material culture.
- If a detail is unsupported, make the most conservative choice and label it as inferred.

Output exactly in this order:
1. Locked room constraints
2. Functional purpose
3. Entry and exit logic
4. Lighting and atmosphere
5. Furniture and fixtures
6. Lore-useful interactive details
7. Final image-generation prompt for this room only
```

## 6. Image Model Safety Add-On

Append this block to any image prompt:

```text
Important constraints:
- Do not redesign the structure.
- Do not add extra wings, stairs, balconies, towers, or windows unless specified.
- Keep the result diagrammatic and architecturally clear.
- Favor top-down plan clarity over cinematic style.
- If a detail is unknown, keep it minimal and understated.
```
