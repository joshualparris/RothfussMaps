import json
import math
from pathlib import Path
import bpy
from mathutils import Vector

JSON_PATH = Path("/ABSOLUTE/PATH/TO/archives_ground.json")

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def ensure_collection(name, parent=None):
    if name in bpy.data.collections:
        return bpy.data.collections[name]
    col = bpy.data.collections.new(name)
    if parent is None:
        bpy.context.scene.collection.children.link(col)
    else:
        parent.children.link(col)
    return col

def load_data(path):
    return json.loads(Path(path).read_text())

def point_lookup(data):
    return {p["id"]: Vector((p["x"], p["y"], 0.0)) for p in data.get("points", [])}

def make_floor_slab(name, footprint, z, thickness, collection):
    mesh = bpy.data.meshes.new(name + "_mesh")
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    verts = [(p["x"], p["y"], z) for p in footprint]
    faces = [tuple(range(len(verts)))]
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, thickness)})
    bpy.ops.object.mode_set(mode='OBJECT')
    obj.select_set(False)
    return obj

def build_wall_segment(name, a, b, thickness, height, z, collection):
    direction = (b - a)
    length = direction.length
    center = (a + b) / 2
    bpy.ops.mesh.primitive_cube_add(location=(center.x, center.y, z + height / 2))
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (length / 2, thickness / 2, height / 2)
    angle = math.atan2(direction.y, direction.x)
    obj.rotation_euler[2] = angle
    collection.objects.link(obj)
    bpy.context.scene.collection.objects.unlink(obj)
    return obj

def build_walls(data, collection):
    pts = point_lookup(data)
    defaults = data["defaults"]
    z = data["levels"]["floor_z"] + data["levels"]["slab_thickness"]
    for wall in data["walls"]:
        a = pts[wall["a"]]
        b = pts[wall["b"]]
        thickness = wall.get("thickness", defaults["wall_thickness"])
        build_wall_segment(wall["id"], a, b, thickness, defaults["wall_height"], z, collection)

def build_room_markers(data, collection):
    for room in data["rooms"]:
        poly = room["polygon"]
        xs = [p["x"] for p in poly]
        ys = [p["y"] for p in poly]
        cx = sum(xs) / len(xs)
        cy = sum(ys) / len(ys)
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=(cx, cy, data["levels"]["floor_z"] + 0.2))
        obj = bpy.context.active_object
        obj.name = f'ROOM_{room["id"]}_{room["name"]}'
        collection.objects.link(obj)
        bpy.context.scene.collection.objects.unlink(obj)

def build_stairs(data, collection):
    z = data["levels"]["floor_z"] + data["levels"]["slab_thickness"]
    for stair in data["stairs"]:
        bpy.ops.mesh.primitive_cube_add(location=(stair["x"], stair["y"], z + 0.15))
        obj = bpy.context.active_object
        obj.name = stair["id"]
        obj.scale = (stair["run_length"]/2, stair["width"]/2, 0.15)
        collection.objects.link(obj)
        bpy.context.scene.collection.objects.unlink(obj)

def main():
    clear_scene()
    data = load_data(JSON_PATH)
    building_col = ensure_collection(data["building"])
    floor_col = ensure_collection(data["floor"], building_col)
    make_floor_slab(f'{data["building"]}_{data["floor"]}_slab', data["footprint"], data["levels"]["floor_z"], data["levels"]["slab_thickness"], floor_col)
    build_walls(data, floor_col)
    build_stairs(data, floor_col)
    build_room_markers(data, floor_col)
    print(f'Imported {data["id"]}')

if __name__ == "__main__":
    main()
