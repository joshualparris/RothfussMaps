"""Compatibility wrapper for the canon floor-plan validator.

New automation should call:
scripts/validation/validate_floor_plan.py <json_path>
"""

import importlib.util
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
VALIDATOR_PATH = PROJECT_DIR / "scripts" / "validation" / "validate_floor_plan.py"
DEFAULT_JSON = PROJECT_DIR / "data" / "buildings" / "archives_ground_v02_canon_safe.json"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_floor_plan", VALIDATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    validator = load_validator()
    argv = sys.argv[1:] or [str(DEFAULT_JSON)]
    return validator.main(argv)


if __name__ == "__main__":
    sys.exit(main())
