extends Area3D

@export var title: String = ""
@export var building: String = ""
@export var floor_label: String = ""
@export var certainty: String = "reconstructed"
@export_multiline var lore_text: String = ""

signal hotspot_focused(data: Dictionary)

func interact() -> void:
	emit_signal("hotspot_focused", {
		"title": title,
		"building": building,
		"floor": floor_label,
		"certainty": certainty,
		"lore_text": lore_text
	})
