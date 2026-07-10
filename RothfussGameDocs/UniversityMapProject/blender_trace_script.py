"""Blender convenience entry script for the Archives ground-floor blockout.

This file is intentionally tiny. The real importer is:
scripts/blender/import_floor_plan.py

Run this file from Blender's Scripting tab when you want the current
Archives ground-floor source JSON without passing command-line arguments.
"""

import importlib.util
from pathlib import Path


PROJECT_DIR = Path(
    r"c:\Users\joshua.parris\OneDrive - Dubbo Christian School\Documents\03_Projects\RothfussGame\RothfussGameDocs\UniversityMapProject"
)
IMPORTER_PATH = PROJECT_DIR / "scripts" / "blender" / "import_floor_plan.py"
SOURCE_JSON = PROJECT_DIR / "data" / "buildings" / "archives_ground_v02_canon_safe.json"


def load_importer(path):
    spec = importlib.util.spec_from_file_location("import_floor_plan", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


if not IMPORTER_PATH.exists():
    raise FileNotFoundError(f"Missing importer script: {IMPORTER_PATH}")

if not SOURCE_JSON.exists():
    raise FileNotFoundError(f"Missing source JSON: {SOURCE_JSON}")

importer = load_importer(IMPORTER_PATH)
importer.import_floor_plan(SOURCE_JSON)
