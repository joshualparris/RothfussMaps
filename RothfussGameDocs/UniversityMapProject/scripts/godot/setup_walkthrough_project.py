import argparse
import json
import math
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[2]
GODOT_DIR = PROJECT_DIR / "godot"

MATERIALS = {
    "slab": ("Mat_floor_slab", (0.23, 0.23, 0.22, 1.0)),
    "canon": ("Mat_room_canon", (0.78, 0.84, 0.90, 1.0)),
    "implied": ("Mat_room_implied", (0.86, 0.78, 0.55, 1.0)),
    "reconstructed": ("Mat_room_reconstructed", (0.72, 0.74, 0.72, 1.0)),
    "outer_wall": ("Mat_outer_wall", (0.05, 0.05, 0.05, 1.0)),
    "partition_wall": ("Mat_partition_wall", (0.13, 0.13, 0.13, 1.0)),
    "door": ("Mat_door_marker", (0.70, 0.14, 0.10, 1.0)),
    "stair": ("Mat_stair_marker", (0.12, 0.45, 0.25, 1.0)),
    "fixture": ("Mat_fixture", (0.38, 0.29, 0.17, 1.0)),
    "label": ("Mat_label_dark", (0.02, 0.02, 0.02, 1.0)),
}


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


def node_name(value):
    name = safe_name(value)
    return "".join(part.capitalize() for part in name.replace("-", "_").split("_") if part) or "Node"


def write_file(path, content, force=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        existing = path.read_text(encoding="utf-8")
        if existing == content:
            return "unchanged"
        return "kept"
    path.write_text(content, encoding="utf-8")
    return "written"


def res_path(path):
    path = Path(path).resolve()
    try:
        return "res://" + path.relative_to(GODOT_DIR.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def fmt(value):
    text = f"{float(value):.4f}".rstrip("0").rstrip(".")
    if text in {"", "-0"}:
        return "0"
    return text


def vec3(x, y, z):
    return f"Vector3({fmt(x)}, {fmt(y)}, {fmt(z)})"


def color(values):
    r, g, b, a = values
    return f"Color({fmt(r)}, {fmt(g)}, {fmt(b)}, {fmt(a)})"


def quoted(value):
    return json.dumps(str(value))


def project_godot(main_scene):
    return f"""config_version=5

[animation]

compatibility/default_parent_skeleton_in_mesh_instance_3d=true

[application]

config/name="Rothfuss University Blockout"
run/main_scene="{main_scene}"
config/features=PackedStringArray("4.6", "Forward Plus")

[input]

move_forward={{
"deadzone": 0.5,
"events": [Object(InputEventKey,"physical_keycode":87)]
}}
move_back={{
"deadzone": 0.5,
"events": [Object(InputEventKey,"physical_keycode":83)]
}}
move_left={{
"deadzone": 0.5,
"events": [Object(InputEventKey,"physical_keycode":65)]
}}
move_right={{
"deadzone": 0.5,
"events": [Object(InputEventKey,"physical_keycode":68)]
}}
jump={{
"deadzone": 0.5,
"events": [Object(InputEventKey,"physical_keycode":32)]
}}
"""


def player_script():
    return """extends CharacterBody3D

@export var move_speed := 5.5
@export var mouse_sensitivity := 0.0025
@export var jump_velocity := 4.5

var _pitch := 0.0
@onready var camera: Camera3D = $Camera3D

func _ready() -> void:
    floor_snap_length = 0.45
    floor_max_angle = deg_to_rad(50.0)
    Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

func _unhandled_input(event: InputEvent) -> void:
    if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
        Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

    if event is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
        rotate_y(-event.relative.x * mouse_sensitivity)
        _pitch = clamp(_pitch - event.relative.y * mouse_sensitivity, deg_to_rad(-85), deg_to_rad(85))
        camera.rotation.x = _pitch
    elif event.is_action_pressed("ui_cancel"):
        Input.mouse_mode = Input.MOUSE_MODE_VISIBLE

func _physics_process(delta: float) -> void:
    if not is_on_floor():
        velocity += get_gravity() * delta
    elif velocity.y < 0.0:
        velocity.y = 0.0

    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = jump_velocity

    var input_dir := Input.get_vector("move_left", "move_right", "move_forward", "move_back")

    if input_dir == Vector2.ZERO:
        var x_axis := 0.0
        var z_axis := 0.0
        if Input.is_key_pressed(KEY_A):
            x_axis -= 1.0
        if Input.is_key_pressed(KEY_D):
            x_axis += 1.0
        if Input.is_key_pressed(KEY_W):
            z_axis -= 1.0
        if Input.is_key_pressed(KEY_S):
            z_axis += 1.0
        input_dir = Vector2(x_axis, z_axis).limit_length(1.0)

    var direction := (global_transform.basis * Vector3(input_dir.x, 0.0, input_dir.y)).normalized()

    if direction.length() > 0.0:
        velocity.x = direction.x * move_speed
        velocity.z = direction.z * move_speed
    else:
        velocity.x = move_toward(velocity.x, 0.0, move_speed)
        velocity.z = move_toward(velocity.z, 0.0, move_speed)

    move_and_slide()
"""


def player_scene():
    return """[gd_scene load_steps=3 format=3]

[ext_resource type="Script" path="res://scripts/player_controller.gd" id="1_player_script"]

[sub_resource type="CapsuleShape3D" id="CapsuleShape3D_player"]
radius = 0.35
height = 1.8

[node name="Player" type="CharacterBody3D"]
script = ExtResource("1_player_script")

[node name="CollisionShape3D" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.9, 0)
shape = SubResource("CapsuleShape3D_player")

[node name="Camera3D" type="Camera3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.65, 0)
current = true
fov = 78.0
"""


def rect_bounds(polygon):
    xs = [float(point["x"]) for point in polygon]
    zs = [float(point["z"]) for point in polygon]
    return min(xs), max(xs), min(zs), max(zs)


def iter_edges(polygon):
    for index, start in enumerate(polygon):
        yield start, polygon[(index + 1) % len(polygon)]


def axis_aligned_segment(start, end):
    if math.isclose(float(start["x"]), float(end["x"]), abs_tol=1e-6):
        return "z"
    if math.isclose(float(start["z"]), float(end["z"]), abs_tol=1e-6):
        return "x"
    return None


def interval_overlap(a_min, a_max, b_min, b_max):
    return max(a_min, b_min) < min(a_max, b_max)


def merge_intervals(intervals):
    if not intervals:
        return []
    ordered = sorted(intervals)
    merged = [ordered[0]]
    for start, end in ordered[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))
    return merged


def split_edge_for_doors(start, end, door_lines, clearance=0.08):
    axis = axis_aligned_segment(start, end)
    if axis is None:
        return []

    sx, sz = float(start["x"]), float(start["z"])
    ex, ez = float(end["x"]), float(end["z"])
    if axis == "x":
        constant = sz
        seg_min, seg_max = sorted((sx, ex))
    else:
        constant = sx
        seg_min, seg_max = sorted((sz, ez))

    cuts = []
    for door_start, door_end in door_lines:
        door_axis = axis_aligned_segment(door_start, door_end)
        if door_axis != axis:
            continue

        dsx, dsz = float(door_start["x"]), float(door_start["z"])
        dex, dez = float(door_end["x"]), float(door_end["z"])
        if axis == "x":
            if not math.isclose(dsz, constant, abs_tol=1e-5) or not math.isclose(dez, constant, abs_tol=1e-5):
                continue
            door_min, door_max = sorted((dsx, dex))
        else:
            if not math.isclose(dsx, constant, abs_tol=1e-5) or not math.isclose(dex, constant, abs_tol=1e-5):
                continue
            door_min, door_max = sorted((dsz, dez))

        door_min -= clearance
        door_max += clearance
        if interval_overlap(seg_min, seg_max, door_min, door_max):
            cuts.append((max(seg_min, door_min), min(seg_max, door_max)))

    cuts = merge_intervals(cuts)
    remaining = []
    cursor = seg_min
    for cut_min, cut_max in cuts:
        if cursor < cut_min:
            remaining.append((cursor, cut_min))
        cursor = max(cursor, cut_max)
    if cursor < seg_max:
        remaining.append((cursor, seg_max))

    if not remaining:
        return []

    segments = []
    for low, high in remaining:
        if high - low < 0.05:
            continue
        if axis == "x":
            first = {"x": low, "z": constant}
            second = {"x": high, "z": constant}
            if sx > ex:
                first, second = second, first
        else:
            first = {"x": constant, "z": low}
            second = {"x": constant, "z": high}
            if sz > ez:
                first, second = second, first
        segments.append((first, second))
    return segments


def edge_key(start, end):
    a = (round(float(start["x"]), 3), round(float(start["z"]), 3))
    b = (round(float(end["x"]), 3), round(float(end["z"]), 3))
    return tuple(sorted((a, b)))


def add_csg_box(lines, name, parent, center, size, material_key, collision=True, rotation=None):
    material_id = MATERIALS[material_key][0]
    lines.extend(
        [
            "",
            f"[node name={quoted(name)} type=\"CSGBox3D\" parent={quoted(parent)}]",
            f"position = {vec3(*center)}",
        ]
    )
    if rotation is not None:
        lines.append(f"rotation = {vec3(*rotation)}")
    lines.extend(
        [
            f"size = {vec3(*size)}",
            f"use_collision = {'true' if collision else 'false'}",
            f"material = SubResource({quoted(material_id)})",
        ]
    )


def add_rect_box(lines, name, parent, polygon, thickness, base_y, material_key, collision):
    min_x, max_x, min_z, max_z = rect_bounds(polygon)
    width = max_x - min_x
    depth = max_z - min_z
    center = ((min_x + max_x) / 2.0, base_y + thickness / 2.0, (min_z + max_z) / 2.0)
    add_csg_box(lines, name, parent, center, (width, thickness, depth), material_key, collision)


def add_wall_segment(lines, name, parent, start, end, thickness, height, base_y, material_key):
    axis = axis_aligned_segment(start, end)
    if axis is None:
        return

    sx, sz = float(start["x"]), float(start["z"])
    ex, ez = float(end["x"]), float(end["z"])
    if axis == "x":
        length = abs(ex - sx)
        center = ((sx + ex) / 2.0, base_y + height / 2.0, sz)
        size = (length, height, thickness)
    else:
        length = abs(ez - sz)
        center = (sx, base_y + height / 2.0, (sz + ez) / 2.0)
        size = (thickness, height, length)

    if length < 0.05:
        return
    add_csg_box(lines, name, parent, center, size, material_key, collision=True)


def build_wall_nodes(lines, data, floor_data=None, parent="Blockout/Walls", name_prefix="", base_y=0.0):
    floor_data = floor_data or data
    metrics = data["floor"]["metrics"]
    slab_thickness = float(metrics.get("floor_slab_thickness", 0.12))
    outer_height = float(floor_data.get("floor_height", metrics.get("floor_height", 4.6)))
    outer_thickness = float(metrics.get("wall_thickness_default", 0.6))
    partition_height = float(metrics.get("partition_height", 2.9))
    partition_thickness = float(metrics.get("partition_wall_thickness", 0.22))
    wall_base_y = base_y + slab_thickness
    door_lines = [(door["line"]["start"], door["line"]["end"]) for door in floor_data.get("doors", [])]

    seen = set()
    wall_index = 1
    for start, end in iter_edges(floor_data["footprint"]["polygon"]):
        for split_start, split_end in split_edge_for_doors(start, end, door_lines):
            key = ("outer", edge_key(split_start, split_end))
            if key in seen:
                continue
            seen.add(key)
            add_wall_segment(
                lines,
                f"{name_prefix}OuterWall{wall_index:02d}",
                parent,
                split_start,
                split_end,
                outer_thickness,
                outer_height,
                wall_base_y,
                "outer_wall",
            )
            wall_index += 1

    partition_index = 1
    for room in floor_data.get("rooms", []):
        for start, end in iter_edges(room["polygon"]):
            for split_start, split_end in split_edge_for_doors(start, end, door_lines):
                key = ("partition", edge_key(split_start, split_end))
                if key in seen:
                    continue
                seen.add(key)
                add_wall_segment(
                    lines,
                    f"{name_prefix}Partition{partition_index:03d}_{node_name(room['id'])}",
                    parent,
                    split_start,
                    split_end,
                    partition_thickness,
                    partition_height,
                    wall_base_y,
                    "partition_wall",
                )
                partition_index += 1


def build_door_nodes(lines, data, floor_data=None, parent="Blockout/Doors", name_prefix="", base_y=0.0):
    floor_data = floor_data or data
    width = float(data["floor"]["metrics"].get("door_marker_width", 0.55))
    for index, door in enumerate(floor_data.get("doors", []), start=1):
        start = door["line"]["start"]
        end = door["line"]["end"]
        axis = axis_aligned_segment(start, end)
        if axis is None:
            continue
        sx, sz = float(start["x"]), float(start["z"])
        ex, ez = float(end["x"]), float(end["z"])
        if axis == "x":
            length = abs(ex - sx)
            center = ((sx + ex) / 2.0, base_y + 0.18, sz)
            size = (length, 0.08, width)
        else:
            length = abs(ez - sz)
            center = (sx, base_y + 0.18, (sz + ez) / 2.0)
            size = (width, 0.08, length)
        add_csg_box(lines, f"{name_prefix}Door{index:02d}_{node_name(door['id'])}", parent, center, size, "door", collision=False)


def add_level_containers(lines, parent):
    for container in ("Slabs", "Rooms", "Walls", "Doors", "Stairs", "Fixtures", "Labels"):
        lines.extend(["", f"[node name=\"{container}\" type=\"Node3D\" parent={quoted(parent)}]"])


def build_floor_nodes(lines, data, floor_data, parent, name_prefix, base_y):
    metrics = data["floor"]["metrics"]
    slab_thickness = float(metrics.get("floor_slab_thickness", 0.12))

    slab_regions = floor_data.get("slab_regions") or [floor_data["footprint"]]
    for index, slab in enumerate(slab_regions, start=1):
        add_rect_box(
            lines,
            f"{name_prefix}Slab{index:02d}_{node_name(slab['id'])}",
            f"{parent}/Slabs",
            slab["polygon"],
            slab_thickness,
            base_y,
            "slab",
            collision=True,
        )

    for index, room in enumerate(floor_data.get("rooms", []), start=1):
        material_key = room.get("certainty", "reconstructed")
        if material_key not in {"canon", "implied", "reconstructed"}:
            material_key = "reconstructed"
        add_rect_box(
            lines,
            f"{name_prefix}Room{index:02d}_{node_name(room['id'])}",
            f"{parent}/Rooms",
            room["polygon"],
            0.04,
            base_y + slab_thickness + 0.01,
            material_key,
            collision=False,
        )

    build_wall_nodes(lines, data, floor_data, f"{parent}/Walls", name_prefix, base_y)
    build_door_nodes(lines, data, floor_data, f"{parent}/Doors", name_prefix, base_y)

    for index, stair in enumerate(floor_data.get("stairs", []), start=1):
        add_rect_box(
            lines,
            f"{name_prefix}Stair{index:02d}_{node_name(stair['id'])}",
            f"{parent}/Stairs",
            stair["polygon"],
            0.10,
            base_y + slab_thickness + 0.06,
            "stair",
            collision=False,
        )

    for index, fixture in enumerate(floor_data.get("fixtures", []), start=1):
        height = float(fixture.get("height", 0.5))
        fixture_type = fixture.get("type")
        add_rect_box(
            lines,
            f"{name_prefix}Fixture{index:02d}_{node_name(fixture['id'])}",
            f"{parent}/Fixtures",
            fixture["polygon"],
            height,
            base_y + slab_thickness + 0.06,
            "fixture",
            collision=fixture_type != "floor_marker",
        )

    for index, label in enumerate(floor_data.get("labels", []), start=1):
        position = label["position"]
        lines.extend(
            [
                "",
                f"[node name={quoted(f'{name_prefix}Label{index:02d}_{node_name(label['id'])}')} type=\"Label3D\" parent={quoted(f'{parent}/Labels')}]",
                f"position = {vec3(float(position['x']), base_y + 0.36, float(position['z']))}",
                "rotation = Vector3(-1.5708, 0, 0)",
                f"text = {quoted(label.get('text', label.get('id', 'Label')))}",
                "font_size = 48",
                "pixel_size = 0.015",
                "outline_size = 6",
                "modulate = Color(0.02, 0.02, 0.02, 1)",
            ]
        )


def build_vertical_links(lines, data):
    links = data.get("vertical_links", [])
    if not links:
        return

    lines.extend(["", "[node name=\"VerticalLinks\" type=\"Node3D\" parent=\"Blockout\"]"])

    for index, link in enumerate(links, start=1):
        start = link["start"]
        end = link["end"]
        sx, sy, sz = float(start["x"]), float(start["y"]), float(start["z"])
        ex, ey, ez = float(end["x"]), float(end["y"]), float(end["z"])
        dx = ex - sx
        dz = ez - sz
        horizontal = math.hypot(dx, dz)
        if horizontal <= 0.05:
            continue

        rise = ey - sy
        width = float(link.get("width", 2.0))
        thickness = float(link.get("thickness", 0.25))
        slope_length = math.hypot(horizontal, rise)
        angle = math.atan2(rise, horizontal)
        yaw = math.atan2(dx, dz)
        pitch = -angle if dz >= 0 else angle
        dir_x = dx / horizontal
        dir_z = dz / horizontal
        center = (
            (sx + ex) / 2.0 + dir_x * math.sin(angle) * thickness / 2.0,
            (sy + ey) / 2.0 - math.cos(angle) * thickness / 2.0,
            (sz + ez) / 2.0 + dir_z * math.sin(angle) * thickness / 2.0,
        )

        add_csg_box(
            lines,
            f"VerticalLink{index:02d}_{node_name(link['id'])}_Ramp",
            "Blockout/VerticalLinks",
            center,
            (width, thickness, slope_length),
            "stair",
            collision=True,
            rotation=(pitch, yaw, 0.0),
        )

        step_count = int(link.get("step_count", 0))
        for step_index in range(1, step_count):
            t = step_index / step_count
            x = sx + dx * t
            y = sy + rise * t + 0.08
            z = sz + dz * t
            add_csg_box(
                lines,
                f"VerticalLink{index:02d}_{node_name(link['id'])}_Tread{step_index:02d}",
                "Blockout/VerticalLinks",
                (x, y, z),
                (width + 0.12, 0.05, 0.12),
                "stair",
                collision=False,
                rotation=(pitch, yaw, 0.0),
            )


def build_scene_nodes(lines, data):
    add_level_containers(lines, "Blockout")
    build_floor_nodes(lines, data, data, "Blockout", "", 0.0)

    for level in data.get("upper_levels", []):
        level_node = node_name(level["id"])
        parent = f"Blockout/{level_node}"
        lines.extend(["", f"[node name={quoted(level_node)} type=\"Node3D\" parent=\"Blockout\"]"])
        add_level_containers(lines, parent)
        build_floor_nodes(
            lines,
            data,
            level,
            parent,
            f"{level_node}_",
            float(level.get("elevation", 0.0)),
        )

    build_vertical_links(lines, data)


def material_resources():
    lines = []
    for material_id, rgba in MATERIALS.values():
        lines.extend(
            [
                "",
                f"[sub_resource type=\"StandardMaterial3D\" id={quoted(material_id)}]",
                f"albedo_color = {color(rgba)}",
                "roughness = 0.82",
            ]
        )
    return lines


def main_scene(scene_name, data):
    load_steps = len(MATERIALS) + 2
    lines = [
        f"[gd_scene load_steps={load_steps} format=3]",
        "",
        "[ext_resource type=\"PackedScene\" path=\"res://scenes/player.tscn\" id=\"1_player\"]",
    ]
    lines.extend(material_resources())
    lines.extend(
        [
            "",
            f"[node name={quoted(scene_name)} type=\"Node3D\"]",
            "",
            "[node name=\"Blockout\" type=\"Node3D\" parent=\".\"]",
        ]
    )
    build_scene_nodes(lines, data)
    lines.extend(
        [
            "",
            "[node name=\"Player\" parent=\".\" instance=ExtResource(\"1_player\")]",
            "transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.24, 15)",
            "",
            "[node name=\"Sun\" type=\"DirectionalLight3D\" parent=\".\"]",
            "transform = Transform3D(0.707107, -0.5, 0.5, 0, 0.707107, 0.707107, -0.707107, -0.5, 0.5, 0, 18, 0)",
            "light_energy = 2.2",
            "",
            "[node name=\"FillLight\" type=\"OmniLight3D\" parent=\".\"]",
            "position = Vector3(0, 6, 2)",
            "light_energy = 1.0",
            "omni_range = 45.0",
        ]
    )
    return "\n".join(lines) + "\n"


def readme(asset_path, source_json):
    return f"""# Godot Walkthrough Scaffold

This is a generated Godot 4 walkthrough scaffold for the University blockout pipeline.

Source JSON:

`{source_json}`

Current walkthrough scene:

`res://scenes/archives_ground_walkthrough.tscn`

The scene is now generated as native Godot CSG from the source JSON, so it is visible in the editor and includes simple floor/wall collision. The old imported GLB can still exist at:

`{asset_path}`

This scene includes reconstructed upper Archives levels and playable stair links between them. Stairs are implemented as shallow collision ramps with visual treads so walking up and down is reliable in Godot.

Controls:

- WASD: move
- Mouse: look
- Left click: recapture mouse after pressing Esc
- Space: jump
- Esc: release mouse

Open the project, press Play, click into the game window if needed, then use WASD.
"""


def setup(json_path, asset_path, force=False):
    data = load_json(json_path)
    building_id = safe_name(data["building"]["id"])
    floor_id = safe_name(data["floor"]["id"])
    scene_base = f"{building_id}_{floor_id}_walkthrough"

    asset_path = Path(asset_path).resolve()
    asset_resource_path = res_path(asset_path)

    files = {
        GODOT_DIR / "project.godot": project_godot(f"res://scenes/{scene_base}.tscn"),
        GODOT_DIR / "scripts" / "player_controller.gd": player_script(),
        GODOT_DIR / "scenes" / "player.tscn": player_scene(),
        GODOT_DIR / "scenes" / f"{scene_base}.tscn": main_scene(scene_base, data),
        GODOT_DIR / "README.md": readme(asset_resource_path, json_path),
    }

    for path, content in files.items():
        result = write_file(path, content, force=force)
        print(f"{result}: {path}")

    (GODOT_DIR / "assets").mkdir(parents=True, exist_ok=True)
    print(f"Godot native CSG walkthrough ready: {GODOT_DIR}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Create a Godot walkthrough scaffold for one validated floor plan.")
    parser.add_argument("json_path", type=Path)
    parser.add_argument("--asset-path", type=Path, required=True)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)

    setup(args.json_path, args.asset_path, force=args.force)


if __name__ == "__main__":
    main()
