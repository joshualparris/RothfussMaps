# University Map Project

This workflow is built to help you reconstruct the University as accurately and consistently as possible from canon evidence before you ask any AI to visualize it. The core rule is simple: do not let an image model decide layout. First lock the evidence, then lock the map, then lock each building, then generate visuals.

## Best Workflow

1. Build an evidence ledger from lawful copies of `TNOTW` and `TWMF`.
2. Convert every spatial clue into a short structured constraint.
3. Separate each constraint into:
   - `Tier 1`: directly confirmed
   - `Tier 2`: strongly implied
   - `Tier 3`: design inference needed to make the space usable
4. Freeze a campus layout before touching building interiors.
5. Freeze each building brief before touching floor plans.
6. Freeze each floor plan before touching individual rooms.

If you skip those freeze points, later prompts will drift and contradict each other.

## Why Direct Image Generation Is Weak

Image models are good at atmosphere and presentation, but weak at:

- counting rooms consistently
- preserving door and stair relationships
- respecting exact adjacency rules
- maintaining one building across multiple generations

For exact floor plans, use a text model first to produce a structured building spec or JSON layout. Use image generation only after the structure is locked.

## Research Rules

- Store short excerpts only. Prefer paraphrase plus page reference over long quotes.
- Treat every spatial claim as evidence, not truth, until it is logged.
- Record contradictions instead of smoothing them away.
- Mark unknowns as unknowns.
- When the books do not support a precise answer, make one explicit design decision and log it.

## Folder Contents

- `university-evidence-ledger-v3.csv`
  Current source-of-truth ledger for prompt generation and canon decisions.
- `evidence-ledger.csv`
  Older merged ledger snapshot retained for traceability.
- `campus-layout.md`
  Synthesized campus layout with confirmed adjacencies and design inferences.
- `buildings/`
  Frozen building briefs for each major structure (Mains, Archives, Mews, etc.).
- `floorplans/`
  JSON specifications for building floor plans with structured constraints.
- `reconstruction-briefs/`
  Canon-constrained reconstruction briefs for all buildings using the 8-section format.
- `ai-prompts/`
  Ready-to-use site plan prompts for Gemini/Nano Banana image generation, one per building with canon constraints; plus floor plan prompts for each building floor with detailed spatial constraints; plus room plan prompts for key canon-described rooms with specific evidence and context.
- `outputs/nano-banana/`
  Workbench and approved image-output storage for the campus-first generation workflow.
- `ai-generation-guide.md`
  Complete guide for consistent AI image generation.
- `evidence-ledger-template.csv`
  Use this as the master dataset for every spatial clue.
- `decision-log-template.md`
  Use this whenever two clues conflict or canon leaves a gap.
- `floorplan-schema-template.json`
  Use this as the structured output target before image generation.
- `prompt-templates.md`
  Ready-to-fill prompts for extraction, synthesis, floor plans, and rooms.
- `generate_prompt.py`
  Generates a consistent prompt from your filled evidence ledger.

## Recommended Pipeline

### Phase 1: Campus Evidence

Track every reference to:

- the Mains
- the Archives
- the Medica
- the Fishery
- the Artificery
- the Mews
- courtyards
- roads and paths
- Stonebridge and the river approach
- any approach sequence such as "from X to Y"

Your job here is not to draw. Your job is to collect constraints.

### Phase 2: Campus Synthesis

Use the ledger to answer:

- Which locations are definitely adjacent?
- Which directions are actually supported?
- Which routes are sequential but not directional?
- Which buildings have exterior traits that affect map shape?
- Which spaces are inside other spaces?

Lock a campus version only after you have answered those.

### Phase 3: Building Briefs

For each building, create a brief with:

- what is canon-confirmed
- what is canon-implied
- what is inferred for playability
- entrances and exits
- vertical movement
- major rooms or functions
- features that must not appear

### Phase 4: Floor Plans

Before using image generation, produce a structured floor plan spec. Keep it architectural and constraint-driven:

- floor count
- main circulation
- room adjacency

### Phase 5: AI Generation

Use the provided prompts in `/ai-prompts/` with Gemini/Nano Banana:

1. Generate floor plans first (technical drawings)
2. Generate building exteriors
3. Generate individual room interiors
4. Maintain consistency across all generations

## Quick Start

1. Review `university-evidence-ledger-v3.csv` and `campus-layout.md`
2. Generate the master campus anchor from `ai-prompts/university-site-plan.md`
3. Store workbench outputs under `outputs/nano-banana/01-campus/workbench/`
4. Freeze the approved campus image before generating building shells
5. Then move to building prompts in `ai-prompts/` and floor specs in `floorplans/`

## Key Findings Integrated

- **Evidence ledger**: `university-evidence-ledger-v3.csv` now has 90 structured rows and is the canon source of truth.
- **Campus freeze**: `campus-layout.md` now functions as the current `campus_v1` freeze, including explicit bridges for the House of the Wind naming issue, the Mews floor-count contradiction, and the `Belows` / `Billows` Underthing spelling tension.
- **Core building briefs**: Archives, Mains, Mews, and Haven have been refreshed against `v3` so the strongest anchor buildings no longer compete with older assumptions.
- **Prompt pack**: the key site-plan and ground-floor prompts for Archives, Mains, Mews, and Haven have been tightened to preserve contradictions and avoid speculative overfill.
- **Haven correction**: Haven has been restored to its canon role as the northern asylum-compound rather than a masters-office building.

### Phase 5: Room Pass

Generate rooms one by one only after the floor plan is frozen. Each room prompt should inherit:

- building identity
- floor identity
- adjacent spaces
- lighting rules
- entry and exit count
- furniture and function
- known lore interactions

## Prompt Generation

To generate prompts from the current canon ledger, run:

```bash
python3 RothfussGameDocs/UniversityMapProject/generate_prompt.py \
  --csv RothfussGameDocs/UniversityMapProject/university-evidence-ledger-v3.csv \
  --mode campus
```

For a building:

```bash
python3 RothfussGameDocs/UniversityMapProject/generate_prompt.py \
  --csv RothfussGameDocs/UniversityMapProject/university-evidence-ledger-v3.csv \
  --mode building \
  --target "the Archives"
```

For a floor plan:

```bash
python3 RothfussGameDocs/UniversityMapProject/generate_prompt.py \
  --csv RothfussGameDocs/UniversityMapProject/university-evidence-ledger-v3.csv \
  --mode floor \
  --target "the Archives"
```

For a room:

```bash
python3 RothfussGameDocs/UniversityMapProject/generate_prompt.py \
  --csv RothfussGameDocs/UniversityMapProject/university-evidence-ledger-v3.csv \
  --mode room \
  --target "the Archives"
```

## Practical Advice

- Use one text model for extraction and synthesis.
- Use one image model only for visualization after structure is locked.
- Keep a single north reference for the whole project.
- Version everything: `campus_v1`, `archives_v1`, `archives_floor_1_v1`.
- Never overwrite a frozen version without logging why.

## Strongest Working Principle

Do not ask, "What does the University probably look like?"

Ask, "What does canon require, what does canon imply, what remains unknown, and what single explicit design choice best bridges each gap without breaking tone or internal logic?"

## Recommended Image Order

1. `ai-prompts/university-site-plan.md`
2. `ai-prompts/archives-site-plan.md`
3. `ai-prompts/floor-plan-archives-ground.md`
4. upper Archives floor prompts only after they remain distinct and validated
5. other building site plans such as Hollows, Mains, Mews, Medica, Fishery, and Haven
6. room plans and interiors last
