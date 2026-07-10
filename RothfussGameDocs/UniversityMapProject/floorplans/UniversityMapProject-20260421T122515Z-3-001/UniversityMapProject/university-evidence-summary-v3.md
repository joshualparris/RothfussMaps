# University Evidence Summary v3

This version integrates the WMF workbook findings from [evidencWMF-import.csv](./evidencWMF-import.csv) and the extra pasted user findings from [wmf-user-supplement.csv](./wmf-user-supplement.csv) into the merged canon ledger at [university-evidence-ledger-v3.csv](./university-evidence-ledger-v3.csv).

## What Changed

- `v2` had 70 rows.
- `v3` now has 90 rows.
- The new material mostly strengthens campus logistics, deep Archives structure, Fishery orientation, Underthing zones, and the richer University-side town.

## Most Important New Locks

- `University scale`
  Admissions now has stronger logistical scale.
  The University hosts over a thousand students, and admissions consumes eleven days with courtyard queues and public milling.

- `House of the Wind / Pennant Square`
  The largest University courtyard is now more tightly identified as a cobblestone public square with layered naming history.
  This gives us a much stronger candidate for a central event square.

- `Archives depth`
  We now have a clearer sense of inhabited and named deep Archives space.
  `Sub-three` sits below ordinary routes.
  Puppet has chambers in the belly of the Archives.
  The Stacks also support a more explicit coordinate system by floor, corner, row, rack, and shelf.

- `Fishery orientation`
  The Fishery is now better anchored architecturally.
  The workshop has low windows on the eastern wall.
  There is a south-facing exit toward a courtyard.
  Kilvin's office is clearly an enclosed hot-work room off the main workshop.

- `Mains roofscape`
  Mains is now stronger from above, not just in plan.
  Its roof is a maze of chimneys and mismatched slate, clay, and tin.

- `Underthing zoning`
  The Underthing now has several more specific sub-zones:
  `the Woods`, `Cricklet`, `Vaults`, and `Belows / Billows`.
  This makes it much easier to build a future subterranean map without reducing everything to one generic tunnel network.

- `University-side wealth district`
  The Golden Pony now gives us a stronger anchor for the affluent University-side commercial zone.
  Ambrose's lodging details reinforce that this side of the river includes much richer rooms than Mews or Anker's.

## Strong Campus Picture After v3

- The University is west of Imre across Stonebridge and the Omethi canyon.
- The campus is large, active, and built into a broader service town rather than existing as a sealed enclave.
- The Archives remain the best-locked building in canon, but now also feel more habitable, stratified, and internally administered.
- Mains remain accreted and maze-like from both inside and above.
- The Fishery now has better compass-facing and window evidence.
- Haven remains a separately secured northern-edge institution.
- The Underthing is now much more clearly a multi-region hidden infrastructure system.

## What Is Still Open

- Exact compass placement of Mains, Hollows, Masters' Hall, Mews, Fishery, Crucible, and Ledgers and Lists remains incomplete.
- House of the Wind, Pennant Square, and Questioning Hall are strongly related but still need one frozen interpretation for map use.
- The exact relation between `Belows` and earlier `Billows` still needs a decision log entry.
- The precise siting of Ambrose's rooms remains looser than major campus anchors.

## Recommended Working Files

- Use [university-evidence-ledger-v3.csv](./university-evidence-ledger-v3.csv) for future prompt generation.
- Keep [university-evidence-ledger-v2.csv](./university-evidence-ledger-v2.csv) as the pre-WMF-merge baseline.
- Keep [evidencWMF-import.csv](./evidencWMF-import.csv) and [wmf-user-supplement.csv](./wmf-user-supplement.csv) as source traces.

## Best Next Step

Freeze `campus_v1` from `v3`, then build these next:

1. `archives_building_brief_v1`
2. `fishery_building_brief_v1`
3. `mains_building_brief_v1`
4. `house_of_the_wind_square_brief_v1`
5. `underthing_zone_map_v1`

Those are the areas where `v3` added the most usable structure.
