import argparse
import json
import math
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[2]
GODOT_DIR = PROJECT_DIR / "godot"

MATERIALS = {
    "slab": ("Mat_floor_slab", (0.24, 0.24, 0.23, 1.0)),
    "canon": ("Mat_room_canon", (0.76, 0.82, 0.90, 1.0)),
    "implied": ("Mat_room_implied", (0.90, 0.82, 0.56, 1.0)),
    "reconstructed": ("Mat_room_reconstructed", (0.72, 0.74, 0.72, 1.0)),
    "outer_wall": ("Mat_outer_wall", (0.09, 0.10, 0.11, 1.0)),
    "partition_wall": ("Mat_partition_wall", (0.17, 0.17, 0.18, 1.0)),
    "door": ("Mat_door_marker", (0.58, 0.16, 0.10, 1.0)),
    "stair": ("Mat_stair_marker", (0.22, 0.47, 0.30, 1.0)),
    "fixture": ("Mat_fixture", (0.41, 0.31, 0.19, 1.0)),
    "label": ("Mat_label_dark", (0.08, 0.08, 0.09, 1.0)),
    "grass": ("Mat_grass", (0.36, 0.49, 0.26, 1.0)),
    "road": ("Mat_road", (0.48, 0.40, 0.30, 1.0)),
    "water": ("Mat_water", (0.16, 0.31, 0.47, 1.0)),
    "cliff": ("Mat_cliff", (0.37, 0.35, 0.33, 1.0)),
    "forest": ("Mat_forest", (0.20, 0.32, 0.17, 1.0)),
    "timber": ("Mat_timber", (0.46, 0.30, 0.16, 1.0)),
    "stone": ("Mat_stone", (0.58, 0.57, 0.52, 1.0)),
    "wall_walk": ("Mat_wall_walk", (0.53, 0.55, 0.49, 1.0)),
    "merlon": ("Mat_merlon", (0.40, 0.42, 0.40, 1.0)),
    "banner": ("Mat_banner", (0.58, 0.15, 0.12, 1.0)),
    "canon_marker": ("Mat_canon_marker", (0.64, 0.84, 0.98, 1.0)),
    "implied_marker": ("Mat_implied_marker", (0.96, 0.85, 0.44, 1.0)),
    "reconstructed_marker": ("Mat_reconstructed_marker", (0.76, 0.76, 0.76, 1.0)),
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


def project_godot(main_scene, app_name):
    return f"""config_version=5

[animation]

compatibility/default_parent_skeleton_in_mesh_instance_3d=true

[application]

config/name="{app_name}"
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
sprint={{
"deadzone": 0.5,
"events": [Object(InputEventKey,"keycode":4194325)]
}}
toggle_fly={{
"deadzone": 0.5,
"events": [Object(InputEventKey,"physical_keycode":70)]
}}
respawn={{
"deadzone": 0.5,
"events": [Object(InputEventKey,"physical_keycode":82)]
}}
"""


def player_script():
    return """extends CharacterBody3D

@export var move_speed := 5.5
@export var sprint_multiplier := 1.8
@export var fly_speed := 8.8
@export var mouse_sensitivity := 0.0025
@export var jump_velocity := 4.5
@export var spawn_position := Vector3(42.0, 0.45, 108.0)
@export var spawn_yaw_degrees := 0.0

var _pitch := 0.0
var _fly_mode := false

@onready var camera: Camera3D = $Camera3D
@onready var collision_shape: CollisionShape3D = $CollisionShape3D


func _ready() -> void:
    floor_snap_length = 0.6
    floor_max_angle = deg_to_rad(62.0)
    Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
    respawn_to_spawn()


func _unhandled_input(event: InputEvent) -> void:
    if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
        Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

    if event.is_action_pressed("toggle_fly"):
        toggle_fly_mode()
        return

    if event.is_action_pressed("respawn"):
        respawn_to_spawn()
        return

    if event is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
        rotate_y(-event.relative.x * mouse_sensitivity)
        _pitch = clamp(_pitch - event.relative.y * mouse_sensitivity, deg_to_rad(-85), deg_to_rad(85))
        camera.rotation.x = _pitch
    elif event.is_action_pressed("ui_cancel"):
        Input.mouse_mode = Input.MOUSE_MODE_VISIBLE


func toggle_fly_mode() -> void:
    _fly_mode = !_fly_mode
    velocity = Vector3.ZERO
    collision_shape.disabled = _fly_mode


func respawn_to_spawn() -> void:
    velocity = Vector3.ZERO
    global_position = spawn_position
    global_rotation = Vector3(0.0, deg_to_rad(spawn_yaw_degrees), 0.0)
    _pitch = 0.0
    camera.rotation = Vector3.ZERO


func _movement_input() -> Vector2:
    var input_dir := Input.get_vector("move_left", "move_right", "move_forward", "move_back")
    if input_dir != Vector2.ZERO:
        return input_dir

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
    return Vector2(x_axis, z_axis).limit_length(1.0)


func _physics_process(delta: float) -> void:
    var input_dir := _movement_input()
    var speed := move_speed
    if Input.is_action_pressed("sprint") or Input.is_key_pressed(KEY_SHIFT):
        speed *= sprint_multiplier

    if _fly_mode:
        var fly_dir := (global_transform.basis * Vector3(input_dir.x, 0.0, input_dir.y))
        var vertical := 0.0
        if Input.is_action_pressed("jump"):
            vertical += 1.0
        if Input.is_key_pressed(KEY_Q) or Input.is_key_pressed(KEY_CTRL):
            vertical -= 1.0
        fly_dir += Vector3.UP * vertical
        if fly_dir.length() > 0.0:
            global_position += fly_dir.normalized() * fly_speed * (speed / move_speed) * delta
        velocity = Vector3.ZERO
        return

    if not is_on_floor():
        velocity += get_gravity() * delta
    elif velocity.y < 0.0:
        velocity.y = 0.0

    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = jump_velocity

    var direction := (global_transform.basis * Vector3(input_dir.x, 0.0, input_dir.y)).normalized()

    if direction.length() > 0.0:
        velocity.x = direction.x * speed
        velocity.z = direction.z * speed
    else:
        velocity.x = move_toward(velocity.x, 0.0, speed * delta * 8.0)
        velocity.z = move_toward(velocity.z, 0.0, speed * delta * 8.0)

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


def rect_center(polygon):
    min_x, max_x, min_z, max_z = rect_bounds(polygon)
    return (min_x + max_x) / 2.0, (min_z + max_z) / 2.0


def polygon_from_bounds(bounds):
    return [
        {"x": float(bounds["x1"]), "z": float(bounds["z1"])},
        {"x": float(bounds["x2"]), "z": float(bounds["z1"])},
        {"x": float(bounds["x2"]), "z": float(bounds["z2"])},
        {"x": float(bounds["x1"]), "z": float(bounds["z2"])},
    ]


def polygon_from_rect(rect):
    x1, x2, z1, z2 = rect
    return [
        {"x": float(x1), "z": float(z1)},
        {"x": float(x2), "z": float(z1)},
        {"x": float(x2), "z": float(z2)},
        {"x": float(x1), "z": float(z2)},
    ]


def bounds_center(bounds):
    x1 = float(bounds["x1"])
    x2 = float(bounds["x2"])
    z1 = float(bounds["z1"])
    z2 = float(bounds["z2"])
    return (x1 + x2) / 2.0, (z1 + z2) / 2.0


def bounds_size(bounds, height):
    x1 = float(bounds["x1"])
    x2 = float(bounds["x2"])
    z1 = float(bounds["z1"])
    z2 = float(bounds["z2"])
    return abs(x2 - x1), float(height), abs(z2 - z1)


def intersect_rect(rect_a, rect_b):
    ax1, ax2, az1, az2 = rect_a
    bx1, bx2, bz1, bz2 = rect_b
    x1 = max(ax1, bx1)
    x2 = min(ax2, bx2)
    z1 = max(az1, bz1)
    z2 = min(az2, bz2)
    if x2 - x1 <= 0.05 or z2 - z1 <= 0.05:
        return None
    return (x1, x2, z1, z2)


def subtract_rect(rect, opening):
    overlap = intersect_rect(rect, opening)
    if overlap is None:
        return [rect]

    rx1, rx2, rz1, rz2 = rect
    ox1, ox2, oz1, oz2 = overlap
    pieces = []

    if ox1 > rx1:
        pieces.append((rx1, ox1, rz1, rz2))
    if ox2 < rx2:
        pieces.append((ox2, rx2, rz1, rz2))

    mid_x1 = max(rx1, ox1)
    mid_x2 = min(rx2, ox2)
    if mid_x2 - mid_x1 > 0.05:
        if oz1 > rz1:
            pieces.append((mid_x1, mid_x2, rz1, oz1))
        if oz2 < rz2:
            pieces.append((mid_x1, mid_x2, oz2, rz2))

    return [piece for piece in pieces if piece[1] - piece[0] > 0.05 and piece[3] - piece[2] > 0.05]


def split_polygon_by_openings(polygon, openings):
    regions = [rect_bounds(polygon)]
    opening_rects = [rect_bounds(opening["polygon"]) for opening in openings if opening.get("polygon")]

    for opening_rect in opening_rects:
        next_regions = []
        for region in regions:
            next_regions.extend(subtract_rect(region, opening_rect))
        regions = next_regions

    return [polygon_from_rect(region) for region in regions]


def certainty_material(certainty):
    if certainty == "canon":
        return "canon_marker"
    if certainty == "implied":
        return "implied_marker"
    return "reconstructed_marker"


def certainty_color(certainty):
    return MATERIALS[certainty_material(certainty)][1]


def preferred_spawn_position(data):
    spawn = data.get("walkthrough", {}).get("spawn")
    if spawn:
        return {
            "x": float(spawn.get("x", 42.0)),
            "y": float(spawn.get("y", 0.45)),
            "z": float(spawn.get("z", 108.0)),
            "yaw_degrees": float(spawn.get("yaw_degrees", 0.0)),
        }

    preferred_room_ids = ["great_hall", "courtyard"]
    rooms = data.get("rooms", [])
    for room_id in preferred_room_ids:
        for room in rooms:
            if room.get("id") == room_id and room.get("polygon"):
                x, z = rect_center(room["polygon"])
                return {"x": x, "y": 0.32, "z": z, "yaw_degrees": 0.0}

    x, z = rect_center(data["footprint"]["polygon"])
    return {"x": x, "y": 0.32, "z": z, "yaw_degrees": 0.0}


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


def add_csg_cylinder(lines, name, parent, position, radius, height, material_key, collision=True, sides=24):
    material_id = MATERIALS[material_key][0]
    lines.extend(
        [
            "",
            f"[node name={quoted(name)} type=\"CSGCylinder3D\" parent={quoted(parent)}]",
            f"position = {vec3(*position)}",
            f"radius = {fmt(radius)}",
            f"height = {fmt(height)}",
            f"sides = {int(sides)}",
            f"use_collision = {'true' if collision else 'false'}",
            f"material = SubResource({quoted(material_id)})",
        ]
    )


def add_label(lines, name, parent, text, position, certainty="reconstructed", font_size=42, billboard=False, flat=False):
    rgba = certainty_color(certainty)
    lines.extend(
        [
            "",
            f"[node name={quoted(name)} type=\"Label3D\" parent={quoted(parent)}]",
            f"position = {vec3(*position)}",
            f"text = {quoted(text)}",
            f"font_size = {int(font_size)}",
            "pixel_size = 0.015",
            "outline_size = 8",
            f"modulate = {color(rgba)}",
        ]
    )
    if billboard:
        lines.append("billboard = 1")
    if flat:
        lines.append("rotation = Vector3(-1.5708, 0, 0)")


def add_bounds_box(lines, name, parent, bounds, y, height, material_key, collision=True):
    center_x, center_z = bounds_center(bounds)
    size_x, size_y, size_z = bounds_size(bounds, height)
    center = (center_x, float(y) + float(height) / 2.0, center_z)
    add_csg_box(lines, name, parent, center, (size_x, size_y, size_z), material_key, collision)


def add_rect_box(lines, name, parent, polygon, thickness, base_y, material_key, collision, rotation=None):
    min_x, max_x, min_z, max_z = rect_bounds(polygon)
    width = max_x - min_x
    depth = max_z - min_z
    center = ((min_x + max_x) / 2.0, base_y + thickness / 2.0, (min_z + max_z) / 2.0)
    add_csg_box(lines, name, parent, center, (width, thickness, depth), material_key, collision, rotation=rotation)


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


def add_route_segment(lines, name, parent, start, end, y, material_key):
    sx, sz = float(start["x"]), float(start["z"])
    ex, ez = float(end["x"]), float(end["z"])
    dx = ex - sx
    dz = ez - sz
    length = math.hypot(dx, dz)
    if length <= 0.1:
        return
    yaw = math.atan2(dx, dz)
    center = ((sx + ex) / 2.0, y, (sz + ez) / 2.0)
    add_csg_box(lines, name, parent, center, (0.38, 0.03, length), material_key, collision=False, rotation=(0.0, yaw, 0.0))


def add_walkable_stair_ramp(
    lines,
    name,
    parent,
    start,
    end,
    width,
    thickness,
    step_count,
    material_key="stair",
    landing_length=1.2,
):
    sx, sy, sz = float(start["x"]), float(start["y"]), float(start["z"])
    ex, ey, ez = float(end["x"]), float(end["y"]), float(end["z"])
    dx = ex - sx
    dz = ez - sz
    horizontal = math.hypot(dx, dz)
    if horizontal <= 0.1:
        return

    dir_x = dx / horizontal
    dir_z = dz / horizontal
    landing_length = min(float(landing_length), max(0.0, horizontal / 3.0))
    run_start = {"x": sx + dir_x * landing_length, "y": sy, "z": sz + dir_z * landing_length}
    run_end = {"x": ex - dir_x * landing_length, "y": ey, "z": ez - dir_z * landing_length}
    run_dx = float(run_end["x"]) - float(run_start["x"])
    run_dz = float(run_end["z"]) - float(run_start["z"])
    run_horizontal = math.hypot(run_dx, run_dz)
    if run_horizontal <= 0.1:
        run_start = {"x": sx, "y": sy, "z": sz}
        run_end = {"x": ex, "y": ey, "z": ez}
        run_dx = run_end["x"] - run_start["x"]
        run_dz = run_end["z"] - run_start["z"]
        run_horizontal = math.hypot(run_dx, run_dz)
        landing_length = 0.0

    run_rise = float(run_end["y"]) - float(run_start["y"])
    angle = math.atan2(run_rise, run_horizontal)
    yaw = math.atan2(run_dx, run_dz)
    pitch = -angle
    run_dir_x = run_dx / run_horizontal
    run_dir_z = run_dz / run_horizontal

    if landing_length > 0.05:
        bottom_center = (
            sx + dir_x * landing_length / 2.0,
            sy + thickness / 2.0,
            sz + dir_z * landing_length / 2.0,
        )
        add_csg_box(
            lines,
            f"{name}_BottomLanding",
            parent,
            bottom_center,
            (width, thickness, landing_length),
            material_key,
            collision=True,
            rotation=(0.0, math.atan2(dir_x, dir_z), 0.0),
        )

        top_center = (
            ex - dir_x * landing_length / 2.0,
            ey + thickness / 2.0,
            ez - dir_z * landing_length / 2.0,
        )
        add_csg_box(
            lines,
            f"{name}_TopLanding",
            parent,
            top_center,
            (width, thickness, landing_length),
            material_key,
            collision=True,
            rotation=(0.0, math.atan2(dir_x, dir_z), 0.0),
        )

    ramp_center = (
        (float(run_start["x"]) + float(run_end["x"])) / 2.0 + run_dir_x * math.sin(angle) * thickness / 2.0,
        (float(run_start["y"]) + float(run_end["y"])) / 2.0 - math.cos(angle) * thickness / 2.0,
        (float(run_start["z"]) + float(run_end["z"])) / 2.0 + run_dir_z * math.sin(angle) * thickness / 2.0,
    )
    slope_length = math.hypot(run_horizontal, run_rise)
    add_csg_box(
        lines,
        f"{name}_CollisionRamp",
        parent,
        ramp_center,
        (width, thickness, slope_length),
        material_key,
        collision=True,
        rotation=(pitch, yaw, 0.0),
    )

    tread_depth = max(run_horizontal / max(step_count, 1), 0.35)
    for step_index in range(step_count):
        t = (step_index + 0.5) / max(step_count, 1)
        x = float(run_start["x"]) + run_dx * t
        y = float(run_start["y"]) + run_rise * t + 0.03
        z = float(run_start["z"]) + run_dz * t
        add_csg_box(
            lines,
            f"{name}_Tread{step_index + 1:02d}",
            parent,
            (x, y, z),
            (width + 0.08, 0.05, tread_depth * 0.7),
            material_key,
            collision=False,
            rotation=(0.0, yaw, 0.0),
        )


def fixture_material_key(fixture):
    explicit = fixture.get("material_key")
    if explicit in MATERIALS:
        return explicit
    fixture_type = fixture.get("type", "")
    if "banner" in fixture_type:
        return "banner"
    if "hedge" in fixture_type or "rose" in fixture_type:
        return "forest"
    if "stone" in fixture_type:
        return "stone"
    if "marker" in fixture_type:
        return certainty_material(fixture.get("certainty", "reconstructed"))
    return "fixture"


def build_wall_nodes(lines, data, floor_data=None, parent="Blockout/Walls", name_prefix="", base_y=0.0):
    floor_data = floor_data or data
    if floor_data.get("generate_walls") is False:
        return

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
    slab_openings = floor_data.get("slab_openings", [])

    slab_regions = floor_data.get("slab_regions") or [floor_data["footprint"]]
    for index, slab in enumerate(slab_regions, start=1):
        material_key = slab.get("material_key", "slab")
        split_polygons = split_polygon_by_openings(slab["polygon"], slab_openings)
        for piece_index, split_polygon in enumerate(split_polygons, start=1):
            add_rect_box(
                lines,
                f"{name_prefix}Slab{index:02d}_{node_name(slab['id'])}_{piece_index:02d}",
                f"{parent}/Slabs",
                split_polygon,
                slab_thickness,
                base_y,
                material_key,
                collision=True,
            )

    for index, room in enumerate(floor_data.get("rooms", []), start=1):
        material_key = room.get("certainty", "reconstructed")
        if material_key not in {"canon", "implied", "reconstructed"}:
            material_key = "reconstructed"
        split_polygons = split_polygon_by_openings(room["polygon"], slab_openings)
        for piece_index, split_polygon in enumerate(split_polygons, start=1):
            add_rect_box(
                lines,
                f"{name_prefix}Room{index:02d}_{node_name(room['id'])}_{piece_index:02d}",
                f"{parent}/Rooms",
                split_polygon,
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
            0.08,
            base_y + slab_thickness + 0.04,
            "stair",
            collision=False,
        )

    for index, fixture in enumerate(floor_data.get("fixtures", []), start=1):
        height = float(fixture.get("height", 0.5))
        material_key = fixture_material_key(fixture)
        collision = bool(fixture.get("collision", fixture.get("type") != "floor_marker"))
        add_rect_box(
            lines,
            f"{name_prefix}Fixture{index:02d}_{node_name(fixture['id'])}",
            f"{parent}/Fixtures",
            fixture["polygon"],
            height,
            base_y + slab_thickness + 0.06,
            material_key,
            collision=collision,
        )

    for index, label in enumerate(floor_data.get("labels", []), start=1):
        position = label["position"]
        add_label(
            lines,
            f"{name_prefix}Label{index:02d}_{node_name(label['id'])}",
            f"{parent}/Labels",
            label.get("text", label.get("id", "Label")),
            (float(position["x"]), base_y + 0.34, float(position["z"])),
            certainty=label.get("certainty", "reconstructed"),
            font_size=44,
            flat=True,
        )


def build_vertical_links(lines, data):
    links = data.get("vertical_links", [])
    if not links:
        return

    lines.extend(["", "[node name=\"VerticalLinks\" type=\"Node3D\" parent=\"Blockout\"]"])
    lines.extend(["", "[node name=\"RouteLabels\" type=\"Node3D\" parent=\"Blockout/VerticalLinks\"]"])

    for index, link in enumerate(links, start=1):
        width = float(link.get("width", 2.2))
        thickness = float(link.get("thickness", 0.22))
        step_count = int(link.get("step_count", 14))
        landing_length = float(link.get("landing_length", 1.4))
        add_walkable_stair_ramp(
            lines,
            f"VerticalLink{index:02d}_{node_name(link['id'])}",
            "Blockout/VerticalLinks",
            link["start"],
            link["end"],
            width,
            thickness,
            step_count,
            material_key="stair",
            landing_length=landing_length,
        )
        sx, sy, sz = float(link["start"]["x"]), float(link["start"]["y"]), float(link["start"]["z"])
        ex, ey, ez = float(link["end"]["x"]), float(link["end"]["y"]), float(link["end"]["z"])
        add_label(
            lines,
            f"VerticalLinkLabel{index:02d}_{node_name(link['id'])}",
            "Blockout/VerticalLinks/RouteLabels",
            f"{link.get('label', link['id'])} [{link.get('certainty', 'reconstructed')}]",
            ((sx + ex) / 2.0, (sy + ey) / 2.0 + 0.9, (sz + ez) / 2.0),
            certainty=link.get("certainty", "reconstructed"),
            font_size=36,
            billboard=True,
        )


def build_scene_nodes(lines, data):
    add_level_containers(lines, "Blockout")
    build_floor_nodes(lines, data, data, "Blockout", "", 0.0)

    for level in data.get("upper_levels", []):
        level_node = node_name(level["id"])
        parent = f"Blockout/{level_node}"
        lines.extend(["", f"[node name={quoted(level_node)} type=\"Node3D\" parent=\"Blockout\"]"])
        add_level_containers(lines, parent)
        build_floor_nodes(lines, data, level, parent, f"{level_node}_", float(level.get("elevation", 0.0)))

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


def environment_resource():
    return [
        "",
        "[sub_resource type=\"Environment\" id=\"Env_default\"]",
        "background_mode = 1",
        "background_color = Color(0.64, 0.71, 0.79, 1)",
        "ambient_light_color = Color(0.54, 0.57, 0.61, 1)",
        "ambient_light_energy = 0.9",
    ]


def find_room(floor_data, room_id):
    for room in floor_data.get("rooms", []):
        if room.get("id") == room_id:
            return room
    return None


def find_level(data, level_id):
    for level in data.get("upper_levels", []):
        if level.get("id") == level_id:
            return level
    return None


def build_site_context(lines, data):
    lines.extend(["", "[node name=\"SiteContext\" type=\"Node3D\" parent=\".\"]"])
    for child in ("Terrain", "Town", "Forest", "Markers", "Legend"):
        lines.extend(["", f"[node name={quoted(child)} type=\"Node3D\" parent=\"SiteContext\"]"])

    features = data.get("site_context", {}).get("features", [])
    for index, feature in enumerate(features, start=1):
        feature_type = feature.get("type", "")
        certainty = feature.get("certainty", "reconstructed")
        feature_name = feature.get("name", feature.get("id", f"Feature{index}"))
        node_base = f"{index:02d}_{node_name(feature.get('id', feature_name))}"
        label_text = f"{feature_name} [{certainty}]"
        if feature_type in {"terrain_slab", "road", "water_plane", "grass_slab", "open_field"}:
            material_key = {
                "terrain_slab": "cliff",
                "road": "road",
                "water_plane": "water",
                "grass_slab": "grass",
                "open_field": "grass",
            }[feature_type]
            collision = feature_type != "water_plane"
            parent = "SiteContext/Terrain"
            bounds = feature["bounds"]
            add_bounds_box(lines, f"{node_base}_Slab", parent, bounds, feature.get("y", 0.0), feature.get("height", 0.12), material_key, collision=collision)
            center_x, center_z = bounds_center(bounds)
            label_y = float(feature.get("y", 0.0)) + float(feature.get("height", 0.12)) + 0.8
            add_label(lines, f"{node_base}_Label", "SiteContext/Markers", label_text, (center_x, label_y, center_z), certainty=certainty, billboard=True, font_size=34)
        elif feature_type == "town_cluster":
            bounds = feature["bounds"]
            add_bounds_box(lines, f"{node_base}_Ground", "SiteContext/Town", bounds, feature.get("y", -1.2), 0.12, "road", collision=True)
            x1 = float(bounds["x1"])
            x2 = float(bounds["x2"])
            z1 = float(bounds["z1"])
            z2 = float(bounds["z2"])
            cols = 4
            rows = 2
            house_width = (x2 - x1) / 6.5
            house_depth = (z2 - z1) / 4.5
            for row in range(rows):
                for col in range(cols):
                    base_x = x1 + 8 + col * ((x2 - x1 - 16) / max(cols - 1, 1))
                    base_z = z1 + 8 + row * ((z2 - z1 - 16) / max(rows - 1, 1))
                    add_csg_box(
                        lines,
                        f"{node_base}_House{row}{col}_Base",
                        "SiteContext/Town",
                        (base_x, float(feature.get("y", -1.2)) + 0.56, base_z),
                        (house_width, 1.1, house_depth),
                        "timber",
                        collision=False,
                    )
                    add_csg_box(
                        lines,
                        f"{node_base}_House{row}{col}_Roof",
                        "SiteContext/Town",
                        (base_x, float(feature.get("y", -1.2)) + 1.24, base_z),
                        (house_width + 0.4, 0.26, house_depth + 0.4),
                        "stone",
                        collision=False,
                    )
            center_x, center_z = bounds_center(bounds)
            add_label(lines, f"{node_base}_Label", "SiteContext/Markers", label_text, (center_x, float(feature.get("y", -1.2)) + 2.0, center_z), certainty=certainty, billboard=True, font_size=34)
        elif feature_type == "forest_edge":
            bounds = feature["bounds"]
            add_bounds_box(lines, f"{node_base}_Ground", "SiteContext/Forest", bounds, feature.get("y", -0.05), 0.1, "grass", collision=True)
            x1 = float(bounds["x1"])
            x2 = float(bounds["x2"])
            z1 = float(bounds["z1"])
            z2 = float(bounds["z2"])
            tree_rows = 3
            tree_cols = 4
            for row in range(tree_rows):
                for col in range(tree_cols):
                    x = x1 + 6 + col * ((x2 - x1 - 12) / max(tree_cols - 1, 1))
                    z = z1 + 8 + row * ((z2 - z1 - 16) / max(tree_rows - 1, 1))
                    trunk_y = float(feature.get("y", -0.05)) + 0.55
                    add_csg_cylinder(lines, f"{node_base}_Tree{row}{col}_Trunk", "SiteContext/Forest", (x, trunk_y, z), 0.22, 1.1, "timber", collision=False, sides=10)
                    add_csg_cylinder(lines, f"{node_base}_Tree{row}{col}_Canopy", "SiteContext/Forest", (x, trunk_y + 0.95, z), 0.85, 1.25, "forest", collision=False, sides=12)
            center_x, center_z = bounds_center(bounds)
            add_label(lines, f"{node_base}_Label", "SiteContext/Markers", label_text, (center_x, float(feature.get("y", -0.05)) + 2.2, center_z), certainty=certainty, billboard=True, font_size=34)
        elif feature_type == "distant_marker":
            position = feature["position"]
            x = float(position["x"])
            y = float(position.get("y", 0.4))
            z = float(position["z"])
            add_csg_cylinder(lines, f"{node_base}_Marker", "SiteContext/Markers", (x, y + 1.0, z), 0.35, 2.2, certainty_material(certainty), collision=False, sides=8)
            add_label(lines, f"{node_base}_Label", "SiteContext/Markers", label_text, (x, y + 2.5, z), certainty=certainty, billboard=True, font_size=30)
        elif feature_type == "distant_islands":
            position = feature["position"]
            anchor_x = float(position["x"])
            anchor_y = float(position.get("y", -1.1))
            anchor_z = float(position["z"])
            for island_index, offset in enumerate(((-18, -4), (0, 0), (22, 6)), start=1):
                add_csg_box(
                    lines,
                    f"{node_base}_Island{island_index}",
                    "SiteContext/Terrain",
                    (anchor_x + offset[0], anchor_y + 0.5, anchor_z + offset[1]),
                    (14.0, 1.0, 8.0),
                    "cliff",
                    collision=False,
                )
            add_label(lines, f"{node_base}_Label", "SiteContext/Markers", label_text, (anchor_x, anchor_y + 2.2, anchor_z), certainty=certainty, billboard=True, font_size=30)

    spawn = preferred_spawn_position(data)
    legend_x = spawn["x"] + 14.0
    legend_z = spawn["z"] - 8.0
    add_csg_box(lines, "LegendBase", "SiteContext/Legend", (legend_x, 0.1, legend_z), (12.0, 0.2, 7.0), "stone", collision=False)
    add_label(lines, "LegendTitle", "SiteContext/Legend", "Evidence Legend", (legend_x, 1.5, legend_z - 2.2), certainty="canon", billboard=True, font_size=36)
    legend_items = [
        ("Canon-supported function", "canon"),
        ("Implied function", "implied"),
        ("Reconstructed geometry", "reconstructed"),
    ]
    for index, (text, certainty) in enumerate(legend_items):
        x = legend_x - 3.8 + index * 3.8
        add_csg_cylinder(lines, f"LegendMarker{index + 1:02d}", "SiteContext/Legend", (x, 0.55, legend_z), 0.35, 0.7, certainty_material(certainty), collision=False, sides=16)
        add_label(lines, f"LegendLabel{index + 1:02d}", "SiteContext/Legend", text, (x, 1.3, legend_z + 1.2), certainty=certainty, billboard=True, font_size=24)
    add_label(
        lines,
        "LegendNote",
        "SiteContext/Legend",
        "Exact geometry is often reconstructed even when function is canon.",
        (legend_x, 1.2, legend_z + 2.6),
        certainty="reconstructed",
        billboard=True,
        font_size=24,
    )


def build_defensive_detail(lines, data):
    lines.extend(["", "[node name=\"DefensiveDetail\" type=\"Node3D\" parent=\".\"]"])
    for child in ("WallWalks", "Merlons", "Markers"):
        lines.extend(["", f"[node name={quoted(child)} type=\"Node3D\" parent=\"DefensiveDetail\"]"])

    min_x, max_x, min_z, max_z = rect_bounds(data["footprint"]["polygon"])
    walk_y = 4.42
    walk_height = 0.18
    walk_width = 2.4
    add_csg_box(lines, "NorthWallWalk", "DefensiveDetail/WallWalks", ((min_x + max_x) / 2.0, walk_y + walk_height / 2.0, max_z - 1.2), (max_x - min_x, walk_height, walk_width), "wall_walk", collision=True)
    add_csg_box(lines, "SouthWallWalk", "DefensiveDetail/WallWalks", ((min_x + max_x) / 2.0, walk_y + walk_height / 2.0, min_z + 1.2), (max_x - min_x, walk_height, walk_width), "wall_walk", collision=True)
    add_csg_box(lines, "WestWallWalk", "DefensiveDetail/WallWalks", (min_x + 1.2, walk_y + walk_height / 2.0, (min_z + max_z) / 2.0), (walk_width, walk_height, max_z - min_z), "wall_walk", collision=True)
    add_csg_box(lines, "EastWallWalk", "DefensiveDetail/WallWalks", (max_x - 1.2, walk_y + walk_height / 2.0, (min_z + max_z) / 2.0), (walk_width, walk_height, max_z - min_z), "wall_walk", collision=True)

    merlon_y = 5.05
    spacing = 4.0
    for x in range(int(min_x) + 3, int(max_x) - 1, int(spacing)):
        add_csg_box(lines, f"NorthMerlon{x:02d}", "DefensiveDetail/Merlons", (x, merlon_y, max_z - 0.6), (1.0, 1.0, 0.8), "merlon", collision=False)
        add_csg_box(lines, f"SouthMerlon{x:02d}", "DefensiveDetail/Merlons", (x, merlon_y, min_z + 0.6), (1.0, 1.0, 0.8), "merlon", collision=False)
    for z in range(int(min_z) + 3, int(max_z) - 1, int(spacing)):
        add_csg_box(lines, f"WestMerlon{z:02d}", "DefensiveDetail/Merlons", (min_x + 0.6, merlon_y, z), (0.8, 1.0, 1.0), "merlon", collision=False)
        add_csg_box(lines, f"EastMerlon{z:02d}", "DefensiveDetail/Merlons", (max_x - 0.6, merlon_y, z), (0.8, 1.0, 1.0), "merlon", collision=False)

    add_label(lines, "WestWallLabel", "DefensiveDetail/Markers", "West Wall [canon, geometry reconstructed]", (min_x - 2.5, 5.0, 36.0), certainty="canon", billboard=True, font_size=30)
    add_label(lines, "EastWallLabel", "DefensiveDetail/Markers", "East Wall / clearing view [canon]", (max_x + 2.5, 5.0, 36.0), certainty="canon", billboard=True, font_size=30)
    add_csg_cylinder(lines, "AlarmBell", "DefensiveDetail/Markers", (52.8, 5.15, 66.8), 0.45, 0.8, "implied_marker", collision=False, sides=12)
    add_label(lines, "AlarmBellLabel", "DefensiveDetail/Markers", "Alarm Bell [implied]", (52.8, 6.1, 66.8), certainty="implied", billboard=True, font_size=26)
    add_csg_box(lines, "SiegeHintLadder", "DefensiveDetail/Markers", (-6.0, 1.2, 42.0), (0.35, 2.4, 2.8), "reconstructed_marker", collision=False, rotation=(0.0, 0.0, 0.35))
    add_label(lines, "SiegeHintLabel", "DefensiveDetail/Markers", "Siege ladder hint [reconstructed variant]", (-8.0, 2.8, 42.0), certainty="reconstructed", billboard=True, font_size=24)


def build_gate_detail(lines, data):
    lines.extend(["", "[node name=\"GateDetail\" type=\"Node3D\" parent=\".\"]"])
    for child in ("Woodwork", "Stonework", "Labels"):
        lines.extend(["", f"[node name={quoted(child)} type=\"Node3D\" parent=\"GateDetail\"]"])

    add_csg_box(lines, "GreatGatePanelWest", "GateDetail/Woodwork", (37.2, 1.9, 71.35), (5.3, 3.4, 0.35), "timber", collision=False, rotation=(0.0, 0.24, 0.0))
    add_csg_box(lines, "GreatGatePanelEast", "GateDetail/Woodwork", (43.8, 1.9, 71.35), (5.3, 3.4, 0.35), "timber", collision=False, rotation=(0.0, -0.24, 0.0))
    add_csg_box(lines, "GreatGatePosternMarker", "GateDetail/Woodwork", (47.2, 1.25, 71.18), (1.2, 2.0, 0.08), "canon_marker", collision=False)

    add_csg_box(lines, "WestGateTowerMassing", "GateDetail/Stonework", (28.0, 6.1, 66.0), (8.0, 3.2, 12.0), "stone", collision=False)
    add_csg_box(lines, "EastGateTowerMassing", "GateDetail/Stonework", (54.0, 6.1, 66.0), (8.0, 3.2, 12.0), "stone", collision=False)
    add_csg_box(lines, "GateLintel", "GateDetail/Stonework", (41.0, 4.7, 71.0), (18.0, 1.0, 1.1), "stone", collision=False)

    add_label(lines, "GreatGateDetailLabel", "GateDetail/Labels", "Great Gate and inset door [canon function, structure reconstructed]", (41.0, 4.3, 75.0), certainty="canon", billboard=True, font_size=32)


def build_keep_front_detail(lines, data):
    lines.extend(["", "[node name=\"KeepFrontDetail\" type=\"Node3D\" parent=\".\"]"])
    for child in ("Stairs", "Doors", "Balcony", "Labels"):
        lines.extend(["", f"[node name={quoted(child)} type=\"Node3D\" parent=\"KeepFrontDetail\"]"])

    add_walkable_stair_ramp(
        lines,
        "KeepFrontBroadStairs",
        "KeepFrontDetail/Stairs",
        {"x": 39.0, "y": 0.22, "z": 39.6},
        {"x": 39.0, "y": 0.40, "z": 32.7},
        14.0,
        0.16,
        9,
        material_key="stone",
        landing_length=1.0,
    )

    add_csg_box(lines, "GreatHallDoorWest", "KeepFrontDetail/Doors", (36.3, 1.85, 31.75), (3.9, 3.3, 0.28), "timber", collision=False, rotation=(0.0, 0.12, 0.0))
    add_csg_box(lines, "GreatHallDoorEast", "KeepFrontDetail/Doors", (41.7, 1.85, 31.75), (3.9, 3.3, 0.28), "timber", collision=False, rotation=(0.0, -0.12, 0.0))

    add_csg_box(lines, "HeraldBalconyFloor", "KeepFrontDetail/Balcony", (39.0, 5.15, 34.2), (14.0, 0.18, 2.4), "stone", collision=False)
    add_csg_box(lines, "HeraldBalconyRail", "KeepFrontDetail/Balcony", (39.0, 5.7, 35.1), (14.0, 0.8, 0.18), "merlon", collision=False)
    add_label(lines, "CourtyardLabelRaised", "KeepFrontDetail/Labels", "Courtyard [canon]", (41.0, 1.1, 50.0), certainty="canon", billboard=True, font_size=30)
    add_label(lines, "KeepStairsLabel", "KeepFrontDetail/Labels", "Broad keep stairs [canon function]", (39.0, 1.2, 36.2), certainty="canon", billboard=True, font_size=30)
    add_label(lines, "OakDoorsLabel", "KeepFrontDetail/Labels", "Large oaken doors [canon]", (39.0, 4.0, 30.8), certainty="canon", billboard=True, font_size=30)
    add_label(lines, "HeraldBalconyLabelRaised", "KeepFrontDetail/Labels", "Herald balcony [canon]", (39.0, 6.2, 35.2), certainty="canon", billboard=True, font_size=30)


def build_room_function_detail(lines, data):
    lines.extend(["", "[node name=\"RoomFunctionDetail\" type=\"Node3D\" parent=\".\"]"])
    for child in ("GroundProps", "CellarProps", "TowerProps", "Labels"):
        lines.extend(["", f"[node name={quoted(child)} type=\"Node3D\" parent=\"RoomFunctionDetail\"]"])

    great_hall = find_room(data, "great_hall")
    if great_hall:
        add_csg_box(lines, "GreatHallDais", "RoomFunctionDetail/GroundProps", (39.0, 0.37, 20.5), (20.0, 0.25, 3.0), "stone", collision=True)
        add_csg_box(lines, "GreatHallHighTable", "RoomFunctionDetail/GroundProps", (39.0, 0.88, 21.0), (10.0, 0.8, 1.4), "timber", collision=True)
        for index, z in enumerate((24.2, 26.7, 29.2), start=1):
            add_csg_box(lines, f"GreatHallBenchWest{index}", "RoomFunctionDetail/GroundProps", (33.0, 0.72, z), (9.0, 0.65, 1.1), "timber", collision=True)
            add_csg_box(lines, f"GreatHallBenchEast{index}", "RoomFunctionDetail/GroundProps", (45.0, 0.72, z), (9.0, 0.65, 1.1), "timber", collision=True)
        add_csg_box(lines, "GreatHallAudienceZone", "RoomFunctionDetail/GroundProps", (39.0, 0.27, 26.5), (22.0, 0.05, 7.0), "canon_marker", collision=False)
        add_csg_box(lines, "GreatHallBannerWest", "RoomFunctionDetail/GroundProps", (26.0, 2.8, 22.0), (0.2, 2.4, 1.1), "banner", collision=False)
        add_csg_box(lines, "GreatHallBannerEast", "RoomFunctionDetail/GroundProps", (52.0, 2.8, 22.0), (0.2, 2.4, 1.1), "banner", collision=False)

    courtyard = find_room(data, "courtyard")
    if courtyard:
        add_csg_box(lines, "ChoosingAssemblyMarker", "RoomFunctionDetail/GroundProps", (41.0, 0.28, 49.5), (14.0, 0.05, 7.0), "canon_marker", collision=False)
        add_csg_box(lines, "BanapisTableWest", "RoomFunctionDetail/GroundProps", (31.0, 0.74, 53.0), (8.0, 0.7, 1.6), "timber", collision=True)
        add_csg_box(lines, "BanapisTableEast", "RoomFunctionDetail/GroundProps", (48.5, 0.74, 53.0), (7.0, 0.7, 1.6), "timber", collision=True)
        for index, x in enumerate((38.6, 40.3, 42.0), start=1):
            add_csg_cylinder(lines, f"CourtyardCask{index}", "RoomFunctionDetail/GroundProps", (x, 0.7, 55.0), 0.55, 1.0, "timber", collision=True, sides=16)

    service_corridor = find_room(data, "service_corridor")
    if service_corridor:
        add_csg_box(lines, "ServiceCorridorLongTable", "RoomFunctionDetail/GroundProps", (58.0, 0.8, 27.0), (2.0, 0.75, 10.5), "timber", collision=True)
        for index, z in enumerate((22.2, 24.8, 27.4, 30.0, 32.6), start=1):
            add_csg_cylinder(lines, f"GobletMarker{index}", "RoomFunctionDetail/GroundProps", (59.1, 1.22, z), 0.12, 0.18, "canon_marker", collision=False, sides=12)
        add_csg_box(lines, "ServiceCurtainMarker", "RoomFunctionDetail/GroundProps", (61.7, 1.2, 31.2), (0.18, 2.2, 3.6), "banner", collision=False)
        add_label(lines, "ServiceCorridorRouteLabel", "RoomFunctionDetail/Labels", "Long service corridor with dishware [canon]", (59.6, 2.2, 28.5), certainty="canon", billboard=True, font_size=26)

    kitchen = find_room(data, "kitchen")
    if kitchen:
        add_csg_box(lines, "KitchenHearth", "RoomFunctionDetail/GroundProps", (77.3, 1.15, 25.0), (3.4, 1.9, 7.2), "stone", collision=True)
        add_csg_box(lines, "KitchenPrepTableWest", "RoomFunctionDetail/GroundProps", (66.5, 0.82, 22.8), (4.8, 0.78, 1.8), "timber", collision=True)
        add_csg_box(lines, "KitchenPrepTableEast", "RoomFunctionDetail/GroundProps", (66.5, 0.82, 29.2), (4.8, 0.78, 1.8), "timber", collision=True)
        add_csg_box(lines, "KitchenShelfRun", "RoomFunctionDetail/GroundProps", (71.2, 1.15, 31.5), (1.0, 1.7, 4.0), "timber", collision=True)

    princess_garden = find_room(data, "princess_garden")
    if princess_garden:
        add_csg_box(lines, "GardenStoneBench", "RoomFunctionDetail/GroundProps", (63.0, 0.58, 5.0), (6.0, 0.5, 1.6), "stone", collision=True)
        add_csg_box(lines, "GardenScreenNorth", "RoomFunctionDetail/GroundProps", (67.0, 1.0, 1.0), (22.0, 1.8, 1.6), "forest", collision=False)
        add_csg_box(lines, "GardenScreenWest", "RoomFunctionDetail/GroundProps", (55.2, 1.0, 5.0), (1.4, 1.8, 6.0), "forest", collision=False)
        add_csg_box(lines, "GardenRoseScreen", "RoomFunctionDetail/GroundProps", (58.0, 0.95, 6.4), (2.2, 1.6, 3.2), "forest", collision=False)

    stables = find_room(data, "stables")
    if stables:
        for index, z in enumerate((56.5, 61.0, 65.5, 70.0), start=1):
            add_csg_box(lines, f"StableDivider{index}", "RoomFunctionDetail/GroundProps", (8.0, 1.0, z), (15.5, 1.8, 0.18), "timber", collision=True)
        add_label(lines, "StableWallMarker", "RoomFunctionDetail/Labels", "Wall behind stables [canon context, placement reconstructed]", (2.0, 2.2, 69.0), certainty="canon", billboard=True, font_size=24)

    cellar_level = find_level(data, "cellar_level")
    if cellar_level:
        add_csg_box(lines, "CellarStorageStacks", "RoomFunctionDetail/CellarProps", (63.0, -2.2, 24.0), (6.0, 1.2, 3.0), "timber", collision=True)
        add_csg_box(lines, "CellarRefugeMarker", "RoomFunctionDetail/CellarProps", (69.0, -3.08, 40.0), (16.0, 0.05, 12.0), "canon_marker", collision=False)
        for index, x in enumerate((73.0, 75.2, 77.4), start=1):
            add_csg_cylinder(lines, f"CellarBarrel{index}", "RoomFunctionDetail/CellarProps", (x, -2.55, 24.5), 0.55, 1.0, "timber", collision=True, sides=16)
        add_label(lines, "CellarRefugeLabel", "RoomFunctionDetail/Labels", "Cellar refuge / stores [canon function]", (69.0, -1.6, 40.0), certainty="canon", billboard=True, font_size=26)

    magician_tower_level = find_level(data, "magician_tower_level")
    if magician_tower_level:
        add_csg_box(lines, "PugBed", "RoomFunctionDetail/TowerProps", (75.8, 4.9, 43.2), (3.0, 0.6, 1.8), "timber", collision=True)
        add_csg_box(lines, "PugWorktable", "RoomFunctionDetail/TowerProps", (80.5, 5.0, 43.6), (2.2, 0.75, 1.4), "timber", collision=True)
        add_csg_box(lines, "PugBookshelf", "RoomFunctionDetail/TowerProps", (81.8, 5.6, 46.5), (0.8, 2.0, 2.4), "timber", collision=False)
        add_csg_box(lines, "TowerWindowMarker", "RoomFunctionDetail/TowerProps", (78.0, 6.2, 34.2), (2.2, 1.6, 0.12), "canon_marker", collision=False)
        add_label(lines, "PugTowerLabel", "RoomFunctionDetail/Labels", "Pug's room [canon function, geometry reconstructed]", (78.0, 7.0, 44.0), certainty="canon", billboard=True, font_size=26)

    kulgan_tower_level = find_level(data, "kulgan_tower_level")
    if kulgan_tower_level:
        add_csg_box(lines, "KulganStudyTable", "RoomFunctionDetail/TowerProps", (78.0, 8.55, 41.8), (3.0, 0.85, 2.2), "timber", collision=True)
        add_csg_box(lines, "KulganBookshelfWest", "RoomFunctionDetail/TowerProps", (74.8, 9.0, 44.0), (0.8, 1.9, 3.2), "timber", collision=False)
        add_csg_box(lines, "KulganBookshelfEast", "RoomFunctionDetail/TowerProps", (81.2, 9.0, 44.0), (0.8, 1.9, 3.2), "timber", collision=False)
        add_label(lines, "KulganTowerLabel", "RoomFunctionDetail/Labels", "Kulgan's room above [implied]", (78.0, 10.2, 44.0), certainty="implied", billboard=True, font_size=26)


def build_walkthrough_routes(lines, data):
    routes = data.get("walkthrough_routes", [])
    if not routes:
        return

    lines.extend(["", "[node name=\"WalkthroughRoutes\" type=\"Node3D\" parent=\".\"]"])
    for route in routes:
        route_parent = f"WalkthroughRoutes/{node_name(route['id'])}"
        lines.extend(["", f"[node name={quoted(node_name(route['id']))} type=\"Node3D\" parent=\"WalkthroughRoutes\"]"])
        certainty = route.get("certainty", "reconstructed")
        material_key = certainty_material(certainty)
        points = route.get("points", [])
        for index, point in enumerate(points, start=1):
            point_y = float(point.get("y", 0.24))
            add_csg_cylinder(lines, f"RoutePoint{index:02d}", route_parent, (float(point["x"]), point_y + 0.08, float(point["z"])), 0.35, 0.12, material_key, collision=False, sides=12)
            add_label(lines, f"RouteLabel{index:02d}", route_parent, f"{point.get('label', 'Route point')} [{certainty}]", (float(point["x"]), point_y + 0.55, float(point["z"])), certainty=certainty, billboard=True, font_size=22)
            if index < len(points):
                next_point = points[index]
                next_y = float(next_point.get("y", point_y))
                add_route_segment(lines, f"RouteSegment{index:02d}", route_parent, point, next_point, min(point_y, next_y) + 0.02, material_key)


def main_scene(scene_name, data):
    load_steps = len(MATERIALS) + 4
    spawn = preferred_spawn_position(data)
    lines = [
        f"[gd_scene load_steps={load_steps} format=3]",
        "",
        "[ext_resource type=\"PackedScene\" path=\"res://scenes/player.tscn\" id=\"1_player\"]",
    ]
    lines.extend(material_resources())
    lines.extend(environment_resource())
    lines.extend(
        [
            "",
            f"[node name={quoted(scene_name)} type=\"Node3D\"]",
            "",
            "[node name=\"Blockout\" type=\"Node3D\" parent=\".\"]",
        ]
    )

    detail_flags = data.get("scene_detail_pass", {})
    if detail_flags.get("site_context_enabled", True):
        build_site_context(lines, data)
    build_scene_nodes(lines, data)
    if detail_flags.get("defensive_detail_enabled", True):
        build_defensive_detail(lines, data)
    if detail_flags.get("gate_detail_enabled", True):
        build_gate_detail(lines, data)
    if detail_flags.get("keep_front_detail_enabled", True):
        build_keep_front_detail(lines, data)
    if detail_flags.get("room_function_detail_enabled", True):
        build_room_function_detail(lines, data)
    if detail_flags.get("walkthrough_routes_enabled", True):
        build_walkthrough_routes(lines, data)

    lines.extend(
        [
            "",
            "[node name=\"Player\" parent=\".\" instance=ExtResource(\"1_player\")]",
            f"position = {vec3(spawn['x'], spawn['y'], spawn['z'])}",
            f"rotation = {vec3(0.0, math.radians(spawn['yaw_degrees']), 0.0)}",
            f"spawn_position = {vec3(spawn['x'], spawn['y'], spawn['z'])}",
            f"spawn_yaw_degrees = {fmt(spawn['yaw_degrees'])}",
            "",
            "[node name=\"Environment\" type=\"WorldEnvironment\" parent=\".\"]",
            "environment = SubResource(\"Env_default\")",
            "",
            "[node name=\"Sun\" type=\"DirectionalLight3D\" parent=\".\"]",
            "transform = Transform3D(0.707107, -0.5, 0.5, 0, 0.707107, 0.707107, -0.707107, -0.5, 0.5, 0, 18, 0)",
            "light_energy = 2.4",
            "",
            "[node name=\"FillLight\" type=\"OmniLight3D\" parent=\".\"]",
            "position = Vector3(42, 8, 34)",
            "light_energy = 1.15",
            "omni_range = 120.0",
        ]
    )
    return "\n".join(lines) + "\n"


def readme(scene_res, source_json, app_name, asset_path=None):
    lines = [
        "# Godot Walkthrough Scaffold",
        "",
        f"This is a generated Godot 4 walkthrough scaffold for {app_name}.",
        "",
        "Source JSON:",
        "",
        f"`{source_json}`",
        "",
        "Current walkthrough scene:",
        "",
        f"`{scene_res}`",
        "",
        "The scene is generated from the source JSON using native Godot CSG, including site context, battlements, route markers, room-function props, and walkable stair ramps.",
    ]

    if asset_path:
        lines.extend(
            [
                "",
                "Optional sidecar asset path:",
                "",
                f"`{asset_path}`",
            ]
        )

    lines.extend(
        [
            "",
            "Controls:",
            "",
            "- WASD: move",
            "- Mouse: look",
            "- Left click: capture mouse when the window is active",
            "- Space: jump or rise while flying",
            "- Shift: sprint",
            "- F: toggle fly / noclip inspection mode",
            "- R: respawn at the source JSON spawn point",
            "- Q or Ctrl: descend while flying",
            "- Esc: release mouse",
        ]
    )
    return "\n".join(lines) + "\n"


def setup(json_path, asset_path=None, force=False):
    data = load_json(json_path)
    building_name = data["building"].get("name", data["building"]["id"])
    building_id = safe_name(data["building"]["id"])
    floor_id = safe_name(data["floor"]["id"])
    scene_base = f"{building_id}_{floor_id}_walkthrough"
    scene_res = f"res://scenes/{scene_base}.tscn"
    app_name = f"{building_name} Source Walkthrough"

    asset_resource_path = None
    if asset_path is not None:
        asset_path = Path(asset_path).resolve()
        asset_resource_path = res_path(asset_path)

    files = {
        GODOT_DIR / "project.godot": project_godot(scene_res, app_name),
        GODOT_DIR / "scripts" / "player_controller.gd": player_script(),
        GODOT_DIR / "scenes" / "player.tscn": player_scene(),
        GODOT_DIR / "scenes" / f"{scene_base}.tscn": main_scene(scene_base, data),
        GODOT_DIR / "README.md": readme(scene_res, json_path, building_name, asset_resource_path),
    }

    for path, content in files.items():
        result = write_file(path, content, force=force)
        print(f"{result}: {path}")

    (GODOT_DIR / "assets").mkdir(parents=True, exist_ok=True)
    print(f"Godot native CSG walkthrough ready: {GODOT_DIR}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Create a Godot walkthrough scaffold for one validated floor plan.")
    parser.add_argument("json_path", type=Path)
    parser.add_argument("--asset-path", type=Path)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)

    setup(args.json_path, args.asset_path, force=args.force)


if __name__ == "__main__":
    main()
