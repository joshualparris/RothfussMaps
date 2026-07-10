from pathlib import Path
import bpy

EXPORT_DIR = Path("/ABSOLUTE/PATH/TO/models")
BUILDING_NAME = "Archives"

# Intended use:
# 1. Import all floor JSONs for one building into the same Blender scene.
# 2. Verify stair alignment and vertical stacking.
# 3. Export a single GLB per building.

def export_glb(building_name):
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    filepath = EXPORT_DIR / f"{building_name.lower()}.glb"
    bpy.ops.export_scene.gltf(filepath=str(filepath), export_format='GLB')
    print(f"Exported {filepath}")
