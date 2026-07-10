"""Compatibility wrapper for the Archives ground-floor Blender import.

New automation should call scripts/blender/import_floor_plan.py with an explicit
JSON path. This wrapper exists so older notes and Blender text blocks that call
import_archives_ground() still work.
"""

import importlib.util
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent if "__file__" in globals() else Path(
    r"c:\Users\joshua.parris\OneDrive - Dubbo Christian School\Documents\03_Projects\RothfussGame\RothfussGameDocs\UniversityMapProject\scripts"
)
PROJECT_DIR = SCRIPT_DIR.parent
JSON_PATH = PROJECT_DIR / "data" / "buildings" / "archives_ground_v02_canon_safe.json"
GENERIC_IMPORTER = PROJECT_DIR / "scripts" / "blender" / "import_floor_plan.py"


def load_generic_importer():
    spec = importlib.util.spec_from_file_location("import_floor_plan", GENERIC_IMPORTER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def import_archives_ground():
    importer = load_generic_importer()
    return importer.import_floor_plan(JSON_PATH)


if __name__ == "__main__":
    import_archives_ground()
