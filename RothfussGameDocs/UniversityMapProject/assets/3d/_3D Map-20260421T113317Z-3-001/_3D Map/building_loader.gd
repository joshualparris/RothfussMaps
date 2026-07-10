extends Node3D

@export var buildings_manifest_path: String = "res://data/buildings.json"

func _ready() -> void:
	var data = _load_json(buildings_manifest_path)
	if data.is_empty():
		push_error("No building manifest loaded.")
		return

	for building in data.get("buildings", []):
		_spawn_building(building)

func _load_json(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		return {}
	var f = FileAccess.open(path, FileAccess.READ)
	var text = f.get_as_text()
	var parsed = JSON.parse_string(text)
	if typeof(parsed) == TYPE_DICTIONARY:
		return parsed
	return {}

func _spawn_building(building: Dictionary) -> void:
	var glb_path = building.get("glb", "")
	if glb_path == "":
		return
	var scene_res = load(glb_path)
	if scene_res == null:
		push_warning("Could not load GLB: %s" % glb_path)
		return
	var inst = scene_res.instantiate()
	inst.name = building.get("name", "Building")
	var pos = building.get("position", [0,0,0])
	inst.position = Vector3(pos[0], pos[1], pos[2])
	inst.rotation_degrees = Vector3(0, building.get("rotation_deg", 0), 0)
	add_child(inst)
