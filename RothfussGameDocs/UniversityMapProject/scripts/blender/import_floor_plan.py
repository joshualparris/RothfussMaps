import argparse
import json
import math
import sys
from pathlib import Path


try:
    import bpy
    from mathutils import Vector
except ImportError:
    bpy = None
    Vector = None


DEFAULT_MATERIALS = {
    "shell": ("archives_shell_stone", (0.34, 0.34, 0.32, 1.0)),
    "slab": ("archives_floor_slab", (0.18, 0.18, 0.18, 1.0)),
    "canon": ("certainty_canon_blue", (0.16, 0.36, 0.72, 0.72)),
    "implied": ("certainty_implied_gold", (0.82, 0.57, 0.18, 0.72)),
    "reconstructed": ("certainty_reconstructed_grey", (0.46, 0.46, 0.46, 0.72)),
    "door": ("archives_door_markers", (0.74, 0.18, 0.16, 1.0)),
    "stair": ("archives_stair_marker", (0.20, 0.58, 0.40, 0.85)),
    "label": ("archives_label_text", (0.06, 0.06, 0.06, 1.0)),
}


def require_blender():
    if bpy is None or Vector is None:
        raise RuntimeError("This importer must be run inside Blender's Python environment.")


def load_json(path):
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def safe_name(value):
    keep = []
    for char in str(value):
        if char.isalnum() or char in {"_", "-"}:
            keep.append(char)
        elif char.isspace():
            keep.append("_")
    return "".join(keep).strip("_").lower() or "unnamed"


def plan_to_blender(point, elevation=0.0):
    """Map source x/z plan coordinates onto Blender x/y with Blender z as up."""
    return (float(point["x"]), float(point["z"]), float(elevation))


def ensure_collection(name, parent=None):
    collection = bpy.data.collections.get(name)
    if collection is None:
        collection = bpy.data.collections.new(name)

    if parent is None:
        child_names = {child.name for child in bpy.context.scene.collection.children}
        if collection.name not in child_names:
            bpy.context.scene.collection.children.link(collection)
    else:
        child_names = {child.name for child in parent.children}
        if collection.name not in child_names:
            parent.children.link(collection)

    return collection


def remove_collection(name):
    collection = bpy.data.collections.get(name)
    if collection is None:
        return

    for child in list(collection.children):
        remove_collection(child.name)

    for obj in list(collection.objects):
        bpy.data.objects.remove(obj, do_unlink=True)

    bpy.data.collections.remove(collection)


def clear_scene():
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    for collection in list(bpy.data.collections):
        bpy.data.collections.remove(collection)


def make_material(name, color):
    material = bpy.data.materials.get(name)
    if material is None:
        material = bpy.data.materials.new(name)
    material.diffuse_color = color
    return material


def build_materials():
    return {key: make_material(name, color) for key, (name, color) in DEFAULT_MATERIALS.items()}


def assign_material(obj, material):
    obj.data.materials.clear()
    obj.data.materials.append(material)


def move_object_to_collection(obj, target_collection):
    object_names = {existing.name for existing in target_collection.objects}
    if obj.name not in object_names:
        target_collection.objects.link(obj)

    for collection in list(obj.users_collection):
        if collection != target_collection:
            collection.objects.unlink(obj)


def add_custom_props(obj, source_path, item):
    obj["source_json"] = str(source_path)

    for key, value in item.items():
        if isinstance(value, (str, int, float, bool)):
            obj[key] = value
        elif isinstance(value, (list, dict)):
            obj[f"{key}_json"] = json.dumps(value, ensure_ascii=True)


def certainty_material(item, materials):
    certainty = item.get("certainty", "reconstructed")
    return materials.get(certainty, materials["reconstructed"])


def create_mesh_object(name, verts, faces, collection, material=None):
    mesh = bpy.data.meshes.new(f"{name}_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()

    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)

    if material is not None:
        assign_material(obj, material)

    return obj


def create_polygon_surface(name, polygon, collection, elevation, material, source_path, item):
    verts = [plan_to_blender(point, elevation) for point in polygon]
    faces = [tuple(range(len(verts)))]
    obj = create_mesh_object(name, verts, faces, collection, material)
    add_custom_props(obj, source_path, item)
    return obj


def create_floor_slab(name, polygon, collection, thickness, material, source_path, item):
    bottom = [plan_to_blender(point, 0.0) for point in polygon]
    top = [plan_to_blender(point, thickness) for point in polygon]
    count = len(bottom)
    verts = bottom + top
    faces = [tuple(range(count)), tuple(range(count, count * 2))]

    for index in range(count):
        next_index = (index + 1) % count
        faces.append((index, next_index, next_index + count, index + count))

    obj = create_mesh_object(name, verts, faces, collection, material)
    add_custom_props(obj, source_path, item)
    return obj


def create_wall_segment(name, start, end, collection, thickness, height, base_z, material, source_path, item):
    a = Vector(plan_to_blender(start, base_z))
    b = Vector(plan_to_blender(end, base_z))
    direction = b - a
    length = direction.length

    if length == 0:
        return None

    center = (a + b) / 2
    bpy.ops.mesh.primitive_cube_add(location=(center.x, center.y, base_z + height / 2))
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (length / 2, thickness / 2, height / 2)
    obj.rotation_euler[2] = math.atan2(direction.y, direction.x)
    assign_material(obj, material)
    move_object_to_collection(obj, collection)
    add_custom_props(obj, source_path, item)
    return obj


def create_footprint(data, collections, materials, source_path):
    footprint = data["footprint"]
    metrics = data["floor"]["metrics"]
    polygon = footprint["polygon"]
    building_id = safe_name(data["building"]["id"])
    floor_id = safe_name(data["floor"]["id"])

    create_floor_slab(
        f"{building_id}_{floor_id}_footprint_slab",
        polygon,
        collections["footprint"],
        metrics.get("floor_slab_thickness", 0.12),
        materials["slab"],
        source_path,
        footprint,
    )

    wall_item = {
        "id": footprint.get("id", "footprint"),
        "label": footprint.get("label", "Footprint outer wall"),
        "certainty": footprint.get("certainty", ""),
        "geometry_certainty": footprint.get("geometry_certainty", ""),
        "notes": footprint.get("notes", []),
    }
    wall_thickness = metrics.get("wall_thickness_default", 0.6)
    wall_height = metrics.get("floor_height", 4.6)
    wall_base_z = metrics.get("floor_slab_thickness", 0.12)

    for index, start in enumerate(polygon):
        end = polygon[(index + 1) % len(polygon)]
        create_wall_segment(
            f"{building_id}_{floor_id}_outer_wall_{index + 1:02d}",
            start,
            end,
            collections["footprint"],
            wall_thickness,
            wall_height,
            wall_base_z,
            materials["shell"],
            source_path,
            wall_item,
        )


def create_rooms(data, collections, materials, source_path):
    metrics = data["floor"]["metrics"]
    base_elevation = metrics.get("floor_slab_thickness", 0.12) + 0.02
    building_id = safe_name(data["building"]["id"])
    floor_id = safe_name(data["floor"]["id"])

    for room in data.get("rooms", []):
        create_polygon_surface(
            f"{building_id}_{floor_id}_room_{safe_name(room['id'])}",
            room["polygon"],
            collections["rooms"],
            base_elevation,
            certainty_material(room, materials),
            source_path,
            room,
        )


def create_door_marker(data, door, collection, material, source_path):
    line = door["line"]
    a = Vector(plan_to_blender(line["start"], 0.22))
    b = Vector(plan_to_blender(line["end"], 0.22))
    direction = b - a
    length = direction.length

    if length == 0:
        return None

    direction.normalize()
    perpendicular = Vector((-direction.y, direction.x, 0)) * 0.22
    height = Vector((0, 0, 0.1))
    verts = [
        tuple(a + perpendicular),
        tuple(a - perpendicular),
        tuple(b - perpendicular),
        tuple(b + perpendicular),
        tuple(a + perpendicular + height),
        tuple(a - perpendicular + height),
        tuple(b - perpendicular + height),
        tuple(b + perpendicular + height),
    ]
    faces = [
        (0, 1, 2, 3),
        (4, 7, 6, 5),
        (0, 4, 5, 1),
        (1, 5, 6, 2),
        (2, 6, 7, 3),
        (3, 7, 4, 0),
    ]
    building_id = safe_name(data["building"]["id"])
    floor_id = safe_name(data["floor"]["id"])
    obj = create_mesh_object(
        f"{building_id}_{floor_id}_door_{safe_name(door['id'])}",
        verts,
        faces,
        collection,
        material,
    )
    add_custom_props(obj, source_path, door)
    return obj


def create_doors(data, collections, materials, source_path):
    for door in data.get("doors", []):
        create_door_marker(data, door, collections["doors"], materials["door"], source_path)


def create_stairs(data, collections, materials, source_path):
    metrics = data["floor"]["metrics"]
    elevation = metrics.get("floor_slab_thickness", 0.12) + 0.05
    building_id = safe_name(data["building"]["id"])
    floor_id = safe_name(data["floor"]["id"])

    for stair in data.get("stairs", []):
        create_polygon_surface(
            f"{building_id}_{floor_id}_stair_{safe_name(stair['id'])}",
            stair["polygon"],
            collections["stairs"],
            elevation,
            materials["stair"],
            source_path,
            stair,
        )


def create_labels(data, collections, materials, source_path):
    building_id = safe_name(data["building"]["id"])
    floor_id = safe_name(data["floor"]["id"])

    for label in data.get("labels", []):
        position = label["position"]
        bpy.ops.object.text_add(location=(float(position["x"]), float(position["z"]), 0.34))
        obj = bpy.context.active_object
        obj.name = f"{building_id}_{floor_id}_label_{safe_name(label['id'])}"
        obj.data.body = label["text"]
        obj.data.align_x = "CENTER"
        obj.data.align_y = "CENTER"
        obj.data.size = 0.75
        obj.data.materials.append(materials["label"])
        move_object_to_collection(obj, collections["labels"])
        add_custom_props(obj, source_path, label)


def iter_collection_objects(collection):
    for obj in collection.objects:
        yield obj
    for child in collection.children:
        yield from iter_collection_objects(child)


def select_collection_objects(collection):
    bpy.ops.object.select_all(action="DESELECT")
    selected = list(iter_collection_objects(collection))
    for obj in selected:
        obj.select_set(True)
    if selected:
        bpy.context.view_layer.objects.active = selected[0]
    return selected


def import_floor_plan(
    source_path,
    collection_name=None,
    clear_existing=True,
    clear_scene_first=False,
    save_blend=None,
    export_glb=None,
):
    require_blender()
    source_path = Path(source_path).resolve()
    data = load_json(source_path)

    building_id = safe_name(data["building"]["id"])
    floor_id = safe_name(data["floor"]["id"])
    collection_name = collection_name or f"{building_id}_{floor_id}_{safe_name(data.get('schema_version', 'floor_plan'))}"

    bpy.context.scene.unit_settings.system = "METRIC"
    bpy.context.scene.unit_settings.scale_length = 1.0

    if clear_scene_first:
        clear_scene()

    if clear_existing:
        remove_collection(collection_name)

    root = ensure_collection(collection_name)
    collections = {
        "footprint": ensure_collection("footprint", root),
        "rooms": ensure_collection("rooms", root),
        "doors": ensure_collection("doors", root),
        "stairs": ensure_collection("stairs", root),
        "labels": ensure_collection("labels", root),
    }
    materials = build_materials()

    create_footprint(data, collections, materials, source_path)
    create_rooms(data, collections, materials, source_path)
    create_doors(data, collections, materials, source_path)
    create_stairs(data, collections, materials, source_path)
    create_labels(data, collections, materials, source_path)

    print(f"Imported {data['building'].get('name', building_id)} / {data['floor'].get('name', floor_id)}")
    print(f"Source JSON: {source_path}")
    print("Coordinate mapping: JSON x/z -> Blender x/y; Blender z is vertical.")

    if save_blend is not None:
        save_blend = Path(save_blend).resolve()
        save_blend.parent.mkdir(parents=True, exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=str(save_blend))
        print(f"Saved blend: {save_blend}")

    if export_glb is not None:
        export_glb = Path(export_glb).resolve()
        export_glb.parent.mkdir(parents=True, exist_ok=True)
        selected = select_collection_objects(root)
        if not selected:
            raise RuntimeError("No generated blockout objects selected for GLB export.")
        bpy.ops.export_scene.gltf(filepath=str(export_glb), export_format="GLB", use_selection=True)
        print(f"Exported GLB: {export_glb}")

    return root


def blender_argv(argv):
    if "--" in argv:
        return argv[argv.index("--") + 1 :]
    return argv[1:]


def main(argv=None):
    parser = argparse.ArgumentParser(description="Import one canon_floor_plan_v02 JSON file into Blender.")
    parser.add_argument("json_path", type=Path, help="Target floor JSON file.")
    parser.add_argument("--collection-name", help="Override root Blender collection name.")
    parser.add_argument("--keep-existing", action="store_true", help="Do not remove an existing collection with the same name.")
    parser.add_argument("--clear-scene", action="store_true", help="Remove all existing Blender objects and collections before import.")
    parser.add_argument("--save-blend", type=Path, help="Optional .blend path to save after import.")
    parser.add_argument("--export-glb", type=Path, help="Optional .glb path to export after import.")
    args = parser.parse_args(blender_argv(sys.argv) if argv is None else argv)

    import_floor_plan(
        source_path=args.json_path,
        collection_name=args.collection_name,
        clear_existing=not args.keep_existing,
        clear_scene_first=args.clear_scene,
        save_blend=args.save_blend,
        export_glb=args.export_glb,
    )


if __name__ == "__main__":
    main()
