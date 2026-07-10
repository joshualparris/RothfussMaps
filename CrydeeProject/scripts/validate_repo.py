import csv
import json
import sys
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "docs/README.md",
    "docs/CONSISTENCY_RULES.md",
    "docs/NEXT_PHASE_PLAN.md",
    "docs/TODO.md",
    "docs/SOURCE_AUDIT.md",
    "docs/SOURCE_ACCURACY_TASKLIST.md",
    "docs/SOURCE_ACCURACY_AUDIT_V03.md",
    "docs/site-layout.md",
    "docs/crydee-evidence-summary-v1.md",
    "evidence/evidence-ledger.csv",
    "evidence/evidence-ledger-template.csv",
    "evidence/canon_manifest.json",
    "buildings/castle-crydee-brief.md",
    "reconstruction-briefs/castle-crydee-reconstruction.md",
    "templates/decision-log-template.md",
    "templates/structure-schema-template.json",
    "schemas/canon_structure_plan_v01.schema.json",
    "data/pipeline_manifest.json",
    "data/review_gates.json",
    "data/buildings/castle_crydee_site_v03_canon_safe.json",
    "scripts/source_audit.py",
    "scripts/generate_prompt.py",
    "scripts/validation/validate_structure_plan.py",
    "run_pipeline.py",
    "ai-prompts/crydee-site-plan.md",
    "ai-prompts/room-plan-great-hall-crydee.md",
    "magician_file.pdf",
]


def main():
    missing = []
    for rel_path in REQUIRED_FILES:
        path = PROJECT_DIR / rel_path
        if not path.exists():
            missing.append(rel_path)

    ledger_path = PROJECT_DIR / "evidence" / "evidence-ledger.csv"
    row_count = 0
    if ledger_path.exists():
        with ledger_path.open(newline="", encoding="utf-8") as handle:
            row_count = sum(1 for _ in csv.DictReader(handle))

    manifest_path = PROJECT_DIR / "data" / "pipeline_manifest.json"
    manifest_targets = 0
    if manifest_path.exists():
        with manifest_path.open("r", encoding="utf-8") as handle:
            manifest_targets = len(json.load(handle).get("targets", []))

    gates_path = PROJECT_DIR / "data" / "review_gates.json"
    gate_targets = 0
    if gates_path.exists():
        with gates_path.open("r", encoding="utf-8") as handle:
            gate_targets = len(json.load(handle).get("targets", {}))

    print("Crydee scaffold audit")
    print(f"- required files missing: {len(missing)}")
    print(f"- evidence rows: {row_count}")
    print(f"- manifest targets: {manifest_targets}")
    print(f"- review gate targets: {gate_targets}")

    for rel_path in missing:
        print(f"  missing: {rel_path}")

    if row_count == 0:
        print("WARNING: evidence ledger exists but has no rows.")

    if missing:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
