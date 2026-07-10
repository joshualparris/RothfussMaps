# University Evidence Summary v2

This version integrates the workbook findings from [evidencNOTW-import.csv](./evidencNOTW-import.csv) into the merged canon ledger at [university-evidence-ledger-v2.csv](./university-evidence-ledger-v2.csv).

## What Changed

- `v1` had 54 curated rows from direct PDF extraction.
- `v2` now has 70 rows.
- The workbook added specific room- and route-level detail that sharpened several buildings without changing the overall campus spine.

## Most Useful New Locks

- `Hollows`
  Hollows now has stronger internal identity.
  It includes a dark admissions theatre with a stage and raised crescent masters' table.
  It also has at least one back entrance and at least one master office, because Elodin is assigned an office there.

- `The Archives`
  The antechamber desk now has a stronger explicit rule: entry depends on being "in the book."
  The Stacks are now more clearly vertical and deeper than the earlier summary: six stories are described, with underground extension, stairwells, and enclosed stone rooms with heavy wooden doors.
  The four-plate door now has a stronger physical brief: seamless grey stone, no hinge or handle, copper plates, unusual keyholes, and `VALARITAS`.

- `The Mains`
  We now have a cleaner room-level anchor for floor plans.
  At least one classroom in Mains is a small teaching theatre with tiered semicircular seating and a raised demonstration stage.

- `The Mess`
  The Mess is now locked as a genuinely large dining hall rather than just a named service building.
  The dining room can seat roughly two hundred students at once.

- `The Medica`
  The Medica is now better grounded as a public-facing institution, not only a student training space.
  It treats broader patients and allows debts to be worked off after recovery.

- `Administrative space`
  The bursar is now better anchored as a separate stone-building destination reached by courtyard, hallway, and stairs.
  This gives the campus stronger support for a distributed administrative layout.

- `Haven`
  Haven is now much stronger for future floor-plan work.
  Capacity is explicitly large: roughly 320 to 350 present, with room for another 150.
  We also now have two distinct room archetypes:
  Alder Whin's padded daylit room.
  Elodin's former high-containment chamber with copper door, reinforced windows, missing inner handle, and anti-escape logic.

## Strong Campus Picture After Integration

- The University is west of Imre across Stonebridge and the Omethi canyon.
- The campus is a many-building academic town cluster rather than a walled monoblock.
- The Archives remain the dominant monolith and the best-locked building in canon.
- Mains remain accreted and labyrinthine.
- Mews remain radial and wing-structured.
- Haven remains a separately secured northern-edge institution beyond the core cluster.

## What Is Still Open

- Exact compass placement of Mains, Mews, Fishery, Masters' Hall, Crucible, and Hollows relative to one another is still incomplete.
- Masters' Hall is still only partially anchored.
  It has a strong room brief, but not a fully locked building relationship.
- The full surface access pattern of the Underthing is still incomplete.
- The exact relationship between Artificery and Fishery is still best treated as one complex with overlapping naming.

## Recommended Working Files

- Use [university-evidence-ledger-v2.csv](./university-evidence-ledger-v2.csv) for all future prompt generation.
- Keep [university-evidence-ledger-v1.csv](./university-evidence-ledger-v1.csv) as the earlier extraction baseline.
- Keep [evidencNOTW-import.csv](./evidencNOTW-import.csv) as the workbook trace source.

## Best Next Step

Freeze `campus_v1` from `v2`, then build:

1. `archives_building_brief_v1`
2. `mains_building_brief_v1`
3. `hollows_building_brief_v1`
4. `haven_building_brief_v1`

Those four now have enough evidence to support much stronger and more internally consistent floor-plan prompting.
