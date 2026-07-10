# Draft Floor JSON

Use this workflow when creating or revising one floor source file.

## Target Schema

`schemas/canon_floor_plan_v02.schema.json`

Required top-level fields:

- `building`
- `floor`
- `story_role`
- `footprint`
- `rooms`
- `doors`
- `stairs`
- `labels`
- `validation_flags`

## Rules

- Start from the building brief, not from image aesthetics.
- Keep dimensions approximate unless evidence supports precision.
- Add `approximate: true` for reconstructed geometry.
- Use `geometry_certainty` where geometry is less certain than the existence of a place.
- Prefer a simpler canon-safe blockout over a detailed speculative plan.

## Review Gate

`floor_json_frozen`

