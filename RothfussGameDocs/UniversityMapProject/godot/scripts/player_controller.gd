extends CharacterBody3D

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
