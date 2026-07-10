#!/usr/bin/env python3

import argparse
import csv
import sys
from pathlib import Path


VALID_MODES = {"campus", "building", "floor", "room"}


def load_rows(csv_path: Path):
    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader)


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
    book = row.get("book", "").strip() or "Unknown book"
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
    if mode == "campus":
        return (
            "You are acting as a canon cartographer for a Kingkiller Chronicle University project.\n\n"
            "Your job is to synthesize a campus layout from the evidence below without inventing unsupported facts.\n"
        )
    if mode == "building":
        return (
            f"You are building a single authoritative building brief for the University project.\n\n"
            f"Target building: {target}\n\n"
            "Your job is to create a building brief that is internally consistent and safe for later floor-plan generation.\n"
        )
    if mode == "floor":
        return (
            f"You are producing a structured floor plan specification, not concept art.\n\n"
            f"Target building: {target}\n\n"
            "Your job is to turn the evidence below into a conservative, architecturally coherent floor-plan brief.\n"
        )
    return (
        f"You are producing one room specification inside a frozen building and floor plan.\n\n"
        f"Target location: {target}\n\n"
        "Your job is to produce a room-level spec without breaking the existing building logic.\n"
    )


def build_rules(mode: str) -> str:
    common = [
        "- Use only the evidence below.",
        "- If evidence conflicts, preserve the conflict and choose one explicit interpretation only if necessary.",
        "- Mark unsupported details as UNKNOWN.",
        "- Separate canon-confirmed, canon-implied, and design-inferred statements.",
        "- Do not invent exact dimensions unless the evidence supports them.",
    ]

    mode_specific = {
        "campus": [
            "- Start with spatial constraints, not prose summary.",
            "- Keep one fixed north reference.",
        ],
        "building": [
            "- Include exterior shell, entrances, circulation, and required room functions.",
            "- Add hard bans where the evidence rules features out.",
        ],
        "floor": [
            "- Prioritize adjacency, circulation, and access logic over aesthetics.",
            "- Do not add decorative rooms to make the plan look richer.",
            "- End with a blueprint-oriented image prompt that does not redesign the structure.",
        ],
        "room": [
            "- This room must fit the existing floor plan exactly.",
            "- Do not move doors, stairs, windows, or neighboring rooms unless the evidence requires it.",
            "- End with a room-only image prompt that preserves the frozen layout.",
        ],
    }

    all_rules = common + mode_specific[mode]
    return "\n".join(all_rules)


def build_output_spec(mode: str) -> str:
    specs = {
        "campus": [
            "1. Locked campus constraints",
            "2. Contradictions or ambiguities",
            "3. Proposed campus layout logic",
            "4. Explicit design inferences",
            "5. Clean adjacency list",
            "6. Compact campus blueprint brief",
        ],
        "building": [
            "1. Building identity",
            "2. Confirmed facts",
            "3. Implied facts",
            "4. Explicit design inferences",
            "5. Exterior shell",
            "6. Entrances and circulation",
            "7. Required room functions",
            "8. Hard bans",
            "9. Open questions",
            "10. Final frozen brief",
        ],
        "floor": [
            "1. Floor count decision",
            "2. Per-floor room list",
            "3. Room adjacency rules",
            "4. Vertical movement rules",
            "5. Restricted areas",
            "6. Unknowns still unresolved",
            "7. JSON matching the provided floorplan schema",
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
    parser = argparse.ArgumentParser(description="Generate canon-safe map prompts from a University evidence ledger.")
    parser.add_argument("--csv", required=True, help="Path to the evidence ledger CSV.")
    parser.add_argument("--mode", required=True, choices=sorted(VALID_MODES), help="Prompt mode to generate.")
    parser.add_argument("--target", help="Target building or room. Required for non-campus modes.")
    args = parser.parse_args()

    if args.mode != "campus" and not args.target:
        parser.error("--target is required for building, floor, and room modes.")

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
