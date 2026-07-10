#!/usr/bin/env python3

import argparse
import csv
import sys
from pathlib import Path


VALID_MODES = {"site", "structure", "level", "room"}


def load_rows(csv_path: Path):
    with csv_path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def normalize(value: str) -> str:
    return (value or "").strip().lower()


def row_matches_target(row, target: str) -> bool:
    if not target:
        return True
    target_norm = normalize(target)
    fields = [
        row.get("location_scope", ""),
        row.get("primary_location", ""),
        row.get("secondary_location", ""),
        row.get("constraint_statement", ""),
        row.get("paraphrase", ""),
        row.get("notes", ""),
    ]
    return any(target_norm in normalize(field) for field in fields)


def format_evidence(row) -> str:
    book = row.get("book", "").strip() or "Unknown source"
    chapter = row.get("chapter", "").strip()
    page_ref = row.get("page_ref", "").strip()
    certainty = row.get("certainty_tier", "").strip() or "Unrated"
    constraint = row.get("constraint_statement", "").strip()
    paraphrase = row.get("paraphrase", "").strip()
    negative = row.get("negative_constraint", "").strip()

    source_bits = [book]
    if chapter:
        source_bits.append(f"chapter {chapter}")
    if page_ref:
        source_bits.append(f"page {page_ref}")

    line = f"- [{certainty}] {' | '.join(source_bits)}: {constraint or paraphrase or 'No constraint statement entered.'}"
    if paraphrase and paraphrase != constraint:
        line += f" Paraphrase: {paraphrase}"
    if negative:
        line += f" Negative constraint: {negative}"
    return line


def build_intro(mode: str, target: str) -> str:
    if mode == "site":
        return (
            "You are acting as a canon cartographer for a Castle Crydee reconstruction project.\n\n"
            "Your job is to synthesize a site layout from the evidence below without inventing unsupported facts.\n"
        )
    if mode == "structure":
        return (
            f"You are building a single authoritative structure brief for the Crydee project.\n\n"
            f"Target structure: {target}\n\n"
            "Your job is to create a restrained structure brief that is safe for later structure-json generation.\n"
        )
    if mode == "level":
        return (
            f"You are producing a structured level or grounds specification, not concept art.\n\n"
            f"Target structure: {target}\n\n"
            "Your job is to turn the evidence below into a conservative, reconstruction-safe layout brief.\n"
        )
    return (
        f"You are producing one room specification inside a frozen Castle Crydee structure.\n\n"
        f"Target room: {target}\n\n"
        "Your job is to define that room without breaking the larger structure logic.\n"
    )


def build_rules(mode: str) -> str:
    common = [
        "- Use only the evidence below.",
        "- Preserve uncertainty where the novel is vague.",
        "- If evidence conflicts, preserve the conflict and choose one explicit interpretation only if necessary.",
        "- Separate canon-confirmed, canon-implied, and design-inferred statements.",
        "- Do not invent exact dimensions unless the evidence supports them.",
    ]

    mode_specific = {
        "site": [
            "- Start with spatial constraints, not atmosphere.",
            "- Keep the castle, service edge, and town-below relationship distinct if the evidence supports that split.",
        ],
        "structure": [
            "- Include shell logic, circulation, service logic, and defensive logic.",
            "- Add hard bans where the evidence rules features out or where generic fantasy drift would distort the site.",
        ],
        "level": [
            "- Prioritize adjacency, access, and defensive/service logic over aesthetics.",
            "- Do not add ornamental spaces to make the layout look richer.",
            "- End with a blueprint-oriented image prompt that does not redesign the structure.",
        ],
        "room": [
            "- This room must fit the existing structure logic exactly.",
            "- Do not move doors, walls, stairs, or adjacent spaces unless the evidence requires it.",
            "- End with a room-only image prompt that preserves the frozen layout.",
        ],
    }

    return "\n".join(common + mode_specific[mode])


def build_output_spec(mode: str) -> str:
    specs = {
        "site": [
            "1. Locked site constraints",
            "2. Contradictions or ambiguities",
            "3. Proposed site-layout logic",
            "4. Explicit design inferences",
            "5. Clean adjacency and route list",
            "6. Compact site blueprint brief",
        ],
        "structure": [
            "1. Structure identity",
            "2. Confirmed facts",
            "3. Implied facts",
            "4. Explicit design inferences",
            "5. Exterior shell",
            "6. Entrances and circulation",
            "7. Defensive and service logic",
            "8. Hard bans",
            "9. Open questions",
            "10. Final frozen brief",
        ],
        "level": [
            "1. Level or grounds decision",
            "2. Per-zone list",
            "3. Adjacency rules",
            "4. Access and vertical movement rules",
            "5. Restricted areas",
            "6. Unknowns still unresolved",
            "7. JSON matching the provided structure schema",
            "8. Final image-generation prompt for a clean top-down blueprint",
        ],
        "room": [
            "1. Locked room constraints",
            "2. Functional purpose",
            "3. Entry and exit logic",
            "4. Lighting and atmosphere",
            "5. Furniture and fixtures",
            "6. Lore-useful interactive details",
            "7. Final image-generation prompt for this room only",
        ],
    }
    return "\n".join(specs[mode])


def main():
    parser = argparse.ArgumentParser(description="Generate canon-safe Crydee prompts from an evidence ledger.")
    parser.add_argument("--csv", required=True, help="Path to the evidence ledger CSV.")
    parser.add_argument("--mode", required=True, choices=sorted(VALID_MODES))
    parser.add_argument("--target", help="Target structure or room. Required for non-site modes.")
    args = parser.parse_args()

    if args.mode != "site" and not args.target:
        parser.error("--target is required for structure, level, and room modes.")

    csv_path = Path(args.csv)
    if not csv_path.exists():
        print(f"CSV not found: {csv_path}", file=sys.stderr)
        sys.exit(1)

    rows = load_rows(csv_path)
    matching_rows = [row for row in rows if row_matches_target(row, args.target or "")]
    if not matching_rows:
        print("No evidence rows matched the request.", file=sys.stderr)
        sys.exit(1)

    evidence_lines = "\n".join(format_evidence(row) for row in matching_rows)

    sections = [
        build_intro(args.mode, args.target or ""),
        "Rules:",
        build_rules(args.mode),
        "",
        "Evidence:",
        evidence_lines,
        "",
        "Return exactly in this order:",
        build_output_spec(args.mode),
    ]
    print("\n".join(sections))


if __name__ == "__main__":
    main()

