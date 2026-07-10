extends CharacterBody3D

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
