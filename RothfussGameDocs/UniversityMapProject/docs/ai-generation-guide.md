# University Map AI Generation Guide

This guide is for generating consistent, canon-constrained visuals from the files in this folder without letting the image model invent layout.

## Source Order
1. `university-evidence-ledger-v3.csv`
2. `campus-layout.md`
3. `buildings/*.md`
4. `floorplans/*.json`
5. `ai-prompts/*.md`

If two files disagree, prefer the higher item in that list.

## Working Method
1. Freeze the campus from `ai-prompts/university-site-plan.md`.
2. Freeze one building shell or site plan.
3. Freeze one floor.
4. Generate the floor plan.
5. Only then generate rooms and atmospherics.

Do not ask the image model to solve unresolved canon questions for you.

## Prompt Rules
- Include only canon, strong implication, or one explicit logged design bridge.
- Preserve unknowns instead of smoothing them away.
- When canon contains tension, state the chosen bridge in the prompt.
- Keep the same north reference across the whole project.
- Prefer technical drawings for site plans and floor plans before any painterly rendering.

## Recurring Canon Traps
- Do not put the University east of Imre.
- Do not give the Archives windows or multiple public entrances.
- Do not make Mains symmetrical or easy to navigate.
- Do not flatten the Mews into a plain dorm block.
- Do not turn Haven into offices for the Masters.
- Do not erase the difference between `Tomes` access and deeper `Stacks` access.
- Do not collapse all of the Underthing into one generic sewer tunnel.

## Best Prompt Shape
Every strong prompt should include:
- building or area identity
- the locked canon facts
- the unresolved questions that must stay unresolved
- the one design decision used to bridge gaps
- hard bans
- output style requirements

## Build Sequence
- `master campus site plan`: whole-campus anchor for north, scale, and major building masses
- `site plan`: one building exterior and immediate surroundings
- `floor plan`: circulation, stairs, thresholds, adjacency
- `room plan`: one room with inherited building and floor rules
- `interior render`: only after the room plan is frozen

## Practical Advice
- Use the updated prompts in `ai-prompts/` as starting points, not as invitations to embellish.
- Treat `ai-prompts/university-site-plan.md` as the first-generation anchor for the whole image workflow.
- Use `generate_prompt.py` against `university-evidence-ledger-v3.csv` whenever you want a fresh prompt from the current ledger.
- Version outputs as `campus_v1`, `archives_ground_v1`, `mews_room_baths_v1`, and so on.
- Store Nano Banana outputs in `outputs/nano-banana/<stage>/{workbench,approved}/` with the image, prompt, and decision note together.
- If a generation contradicts canon, discard it and revise the prompt. Do not absorb the contradiction into the project.
