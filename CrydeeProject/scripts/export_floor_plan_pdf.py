import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas


PROJECT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_JSON = PROJECT_DIR / "data" / "buildings" / "castle_crydee_ground_v02_canon_safe.json"
DEFAULT_OUTPUT = PROJECT_DIR / "output" / "pdf" / "castle_crydee_floor_plan_v02.pdf"

PAGE_SIZE = landscape(A4)
MARGIN = 36
HEADER_H = 42
FOOTER_H = 22
SIDEBAR_W = 170
PLAN_GAP = 16

CERTAINTY_FILL = {
    "canon": colors.HexColor("#cfe2f3"),
    "implied": colors.HexColor("#f7deb0"),
    "reconstructed": colors.HexColor("#d9d9d9"),
}

SLAB_FILL = colors.HexColor("#f5f0e6")
FIXTURE_FILL = colors.HexColor("#b48a5a")
STAIR_FILL = colors.HexColor("#bdd7c2")
DOOR_STROKE = colors.HexColor("#b85450")
OUTLINE = colors.HexColor("#232323")
INNER_LINE = colors.HexColor("#555555")
LABEL_COLOR = colors.HexColor("#111111")
GRID_COLOR = colors.HexColor("#dddddd")
SIDEBAR_BG = colors.HexColor("#faf7f2")


def load_json(path: Path):
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def polygon_bbox(polygons):
    xs = []
    zs = []
    for polygon in polygons:
        for point in polygon:
            xs.append(float(point["x"]))
            zs.append(float(point["z"]))
    if not xs:
        return 0.0, 1.0, 0.0, 1.0
    return min(xs), max(xs), min(zs), max(zs)


def polygon_center(polygon):
    xs = [float(point["x"]) for point in polygon]
    zs = [float(point["z"]) for point in polygon]
    return sum(xs) / len(xs), sum(zs) / len(zs)


def point_in_room_bounds(point, polygon):
    x = float(point["x"])
    z = float(point["z"])
    xs = [float(p["x"]) for p in polygon]
    zs = [float(p["z"]) for p in polygon]
    return min(xs) <= x <= max(xs) and min(zs) <= z <= max(zs)


def build_levels(data):
    levels = [
        {
            "id": data["floor"]["id"],
            "name": data["floor"]["name"],
            "elevation": float(data["floor"]["metrics"].get("floor_z", 0.0)),
            "notes": [data.get("story_role", {}).get("summary", "")],
            "footprint": data["footprint"],
            "slab_regions": data.get("slab_regions", []),
            "rooms": data.get("rooms", []),
            "doors": data.get("doors", []),
            "stairs": data.get("stairs", []),
            "fixtures": data.get("fixtures", []),
            "labels": data.get("labels", []),
        }
    ]
    levels.extend(data.get("upper_levels", []))
    return levels


def compute_transform(level, plan_box):
    plan_left, plan_bottom, plan_width, plan_height = plan_box
    polygons = []
    if level.get("slab_regions"):
        polygons.extend(region["polygon"] for region in level["slab_regions"])
    if level.get("footprint", {}).get("polygon"):
        polygons.append(level["footprint"]["polygon"])
    polygons.extend(room["polygon"] for room in level.get("rooms", []) if room.get("polygon"))
    polygons.extend(stair["polygon"] for stair in level.get("stairs", []) if stair.get("polygon"))
    polygons.extend(fixture["polygon"] for fixture in level.get("fixtures", []) if fixture.get("polygon"))
    min_x, max_x, min_z, max_z = polygon_bbox(polygons)

    pad_x = max(2.0, (max_x - min_x) * 0.05)
    pad_z = max(2.0, (max_z - min_z) * 0.05)
    min_x -= pad_x
    max_x += pad_x
    min_z -= pad_z
    max_z += pad_z

    world_w = max(max_x - min_x, 1.0)
    world_h = max(max_z - min_z, 1.0)
    scale = min(plan_width / world_w, plan_height / world_h)

    used_w = world_w * scale
    used_h = world_h * scale
    origin_x = plan_left + (plan_width - used_w) / 2.0
    origin_y = plan_bottom + (plan_height - used_h) / 2.0

    def to_page(point):
        x = origin_x + (float(point["x"]) - min_x) * scale
        y = origin_y + (float(point["z"]) - min_z) * scale
        return x, y

    return {
        "bbox": (min_x, max_x, min_z, max_z),
        "scale": scale,
        "to_page": to_page,
        "origin": (origin_x, origin_y),
        "used_size": (used_w, used_h),
    }


def draw_polygon(pdf, polygon, to_page, fill_color=None, stroke_color=OUTLINE, stroke_width=1.0, dash=None):
    path = pdf.beginPath()
    first_x, first_y = to_page(polygon[0])
    path.moveTo(first_x, first_y)
    for point in polygon[1:]:
        x, y = to_page(point)
        path.lineTo(x, y)
    path.close()

    pdf.saveState()
    pdf.setLineWidth(stroke_width)
    pdf.setStrokeColor(stroke_color)
    if dash:
        pdf.setDash(dash)
    if fill_color is not None:
        pdf.setFillColor(fill_color)
        pdf.drawPath(path, stroke=1, fill=1)
    else:
        pdf.drawPath(path, stroke=1, fill=0)
    pdf.restoreState()


def draw_door(pdf, door, to_page):
    start = door["line"]["start"]
    end = door["line"]["end"]
    x1, y1 = to_page(start)
    x2, y2 = to_page(end)
    pdf.saveState()
    pdf.setStrokeColor(DOOR_STROKE)
    pdf.setLineWidth(2.8)
    pdf.line(x1, y1, x2, y2)
    pdf.restoreState()


def draw_room_labels(pdf, level, transform):
    scale = transform["scale"]
    to_page = transform["to_page"]
    explicit_positions = [
        label.get("position")
        for label in level.get("labels", [])
        if label.get("position") and label.get("id") != "castle_label"
    ]

    for room in level.get("rooms", []):
        if any(point_in_room_bounds(position, room["polygon"]) for position in explicit_positions):
            continue
        x, z = polygon_center(room["polygon"])
        width = (max(float(p["x"]) for p in room["polygon"]) - min(float(p["x"]) for p in room["polygon"])) * scale
        height = (max(float(p["z"]) for p in room["polygon"]) - min(float(p["z"]) for p in room["polygon"])) * scale
        if width < 48 or height < 18:
            continue
        label_text = room.get("name", room.get("id", "Room"))
        px, py = to_page({"x": x, "z": z})
        draw_centered_text(pdf, label_text, px, py, max_width=max(40, width - 8), font_name="Helvetica", font_size=7.5)

    for label in level.get("labels", []):
        if label.get("id") == "castle_label":
            continue
        pos = label.get("position")
        if not pos:
            continue
        px, py = to_page(pos)
        draw_centered_text(pdf, label.get("text", label.get("id", "Label")), px, py, max_width=72, font_name="Helvetica-Bold", font_size=8.5)


def draw_centered_text(pdf, text, center_x, center_y, max_width, font_name, font_size):
    lines = simpleSplit(str(text), font_name, font_size, max_width)
    if not lines:
        return
    line_h = font_size + 1.5
    start_y = center_y + ((len(lines) - 1) * line_h) / 2.0 - font_size * 0.35
    pdf.saveState()
    pdf.setFillColor(LABEL_COLOR)
    pdf.setFont(font_name, font_size)
    for index, line in enumerate(lines):
        pdf.drawCentredString(center_x, start_y - index * line_h, line)
    pdf.restoreState()


def draw_grid(pdf, transform, plan_box):
    min_x, max_x, min_z, max_z = transform["bbox"]
    to_page = transform["to_page"]
    plan_left, plan_bottom, plan_width, plan_height = plan_box
    pdf.saveState()
    pdf.setStrokeColor(GRID_COLOR)
    pdf.setLineWidth(0.4)
    for x in range(int(min_x // 10 * 10), int(max_x) + 10, 10):
        px1, py1 = to_page({"x": x, "z": min_z})
        px2, py2 = to_page({"x": x, "z": max_z})
        pdf.line(px1, py1, px2, py2)
    for z in range(int(min_z // 10 * 10), int(max_z) + 10, 10):
        px1, py1 = to_page({"x": min_x, "z": z})
        px2, py2 = to_page({"x": max_x, "z": z})
        pdf.line(px1, py1, px2, py2)
    pdf.restoreState()


def draw_scale_bar(pdf, transform, plan_box):
    plan_left, plan_bottom, _, _ = plan_box
    scale = transform["scale"]
    bar_units = 10
    bar_w = scale * bar_units
    x = plan_left + 10
    y = plan_bottom + 12
    pdf.saveState()
    pdf.setStrokeColor(OUTLINE)
    pdf.setFillColor(colors.white)
    pdf.rect(x, y, bar_w / 2.0, 8, stroke=1, fill=1)
    pdf.setFillColor(OUTLINE)
    pdf.rect(x + bar_w / 2.0, y, bar_w / 2.0, 8, stroke=1, fill=1)
    pdf.setFillColor(LABEL_COLOR)
    pdf.setFont("Helvetica", 7)
    pdf.drawString(x, y - 10, "0")
    pdf.drawCentredString(x + bar_w, y - 10, f"{bar_units} units")
    pdf.restoreState()


def draw_north_arrow(pdf, sidebar_x, sidebar_top):
    arrow_x = sidebar_x + 22
    arrow_y = sidebar_top - 20
    pdf.saveState()
    pdf.setStrokeColor(OUTLINE)
    pdf.setFillColor(OUTLINE)
    pdf.setLineWidth(1.2)
    pdf.line(arrow_x, arrow_y - 18, arrow_x, arrow_y + 12)
    path = pdf.beginPath()
    path.moveTo(arrow_x, arrow_y + 18)
    path.lineTo(arrow_x - 6, arrow_y + 8)
    path.lineTo(arrow_x + 6, arrow_y + 8)
    path.close()
    pdf.drawPath(path, stroke=1, fill=1)
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawCentredString(arrow_x, arrow_y + 24, "N")
    pdf.restoreState()


def draw_sidebar(pdf, level, level_index, total_levels, sidebar_box, source_rel):
    x, y, w, h = sidebar_box
    top = y + h
    pdf.saveState()
    pdf.setFillColor(SIDEBAR_BG)
    pdf.setStrokeColor(colors.HexColor("#dfd8ce"))
    pdf.rect(x, y, w, h, stroke=1, fill=1)
    pdf.restoreState()

    draw_north_arrow(pdf, x + 14, top - 8)

    text_x = x + 14
    cursor_y = top - 62

    pdf.setFont("Helvetica-Bold", 13)
    pdf.setFillColor(OUTLINE)
    pdf.drawString(text_x, cursor_y, level.get("name", "Level"))
    cursor_y -= 16

    pdf.setFont("Helvetica", 8)
    pdf.drawString(text_x, cursor_y, f"Level {level_index + 1} of {total_levels}")
    cursor_y -= 11
    pdf.drawString(text_x, cursor_y, f"Elevation: {level.get('elevation', 0.0):.1f}")
    cursor_y -= 16

    notes = [note for note in level.get("notes", []) if note]
    if notes:
        pdf.setFont("Helvetica-Bold", 8.5)
        pdf.drawString(text_x, cursor_y, "Notes")
        cursor_y -= 11
        pdf.setFont("Helvetica", 7.4)
        for note in notes[:2]:
            lines = simpleSplit(note, "Helvetica", 7.4, w - 28)
            for line in lines[:4]:
                pdf.drawString(text_x, cursor_y, line)
                cursor_y -= 9
            cursor_y -= 4

    pdf.setFont("Helvetica-Bold", 8.5)
    pdf.drawString(text_x, cursor_y, "Legend")
    cursor_y -= 12

    legend_items = [
        ("Canon room", CERTAINTY_FILL["canon"]),
        ("Implied room", CERTAINTY_FILL["implied"]),
        ("Reconstructed room", CERTAINTY_FILL["reconstructed"]),
        ("Slab / court", SLAB_FILL),
        ("Stair zone", STAIR_FILL),
        ("Fixture", FIXTURE_FILL),
    ]
    pdf.setFont("Helvetica", 7.4)
    for label, fill in legend_items:
        pdf.setFillColor(fill)
        pdf.setStrokeColor(OUTLINE)
        pdf.rect(text_x, cursor_y - 7, 10, 8, stroke=1, fill=1)
        pdf.setFillColor(LABEL_COLOR)
        pdf.drawString(text_x + 16, cursor_y - 1, label)
        cursor_y -= 12

    pdf.setStrokeColor(DOOR_STROKE)
    pdf.setLineWidth(2.8)
    pdf.line(text_x, cursor_y - 3, text_x + 12, cursor_y - 3)
    pdf.setFillColor(LABEL_COLOR)
    pdf.drawString(text_x + 16, cursor_y - 6, "Door")
    cursor_y -= 16

    pdf.setFont("Helvetica-Bold", 8.5)
    pdf.drawString(text_x, cursor_y, "Source")
    cursor_y -= 11
    pdf.setFont("Helvetica", 7.1)
    for line in simpleSplit(source_rel, "Helvetica", 7.1, w - 28):
        pdf.drawString(text_x, cursor_y, line)
        cursor_y -= 8


def draw_header_footer(pdf, title, level_name, source_name, page_number):
    page_w, page_h = PAGE_SIZE
    pdf.saveState()
    pdf.setFillColor(OUTLINE)
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(MARGIN, page_h - MARGIN + 6, title)
    pdf.setFont("Helvetica", 9)
    pdf.drawString(MARGIN, page_h - MARGIN - 8, level_name)

    pdf.setStrokeColor(colors.HexColor("#d3cec7"))
    pdf.setLineWidth(0.8)
    pdf.line(MARGIN, page_h - MARGIN - 14, page_w - MARGIN, page_h - MARGIN - 14)
    pdf.line(MARGIN, MARGIN - 4, page_w - MARGIN, MARGIN - 4)

    pdf.setFont("Helvetica", 7.5)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    pdf.drawString(MARGIN, MARGIN - 16, f"Generated from {source_name}")
    pdf.drawRightString(page_w - MARGIN, MARGIN - 16, f"Page {page_number} | {timestamp}")
    pdf.restoreState()


def draw_level(pdf, data, level, level_index, total_levels, source_rel):
    page_w, page_h = PAGE_SIZE
    title = f"{data['building']['name']} Floor Plan"
    draw_header_footer(pdf, title, level.get("name", "Level"), source_rel, level_index + 1)

    plan_left = MARGIN
    plan_bottom = MARGIN + FOOTER_H
    plan_width = page_w - (MARGIN * 2) - SIDEBAR_W - PLAN_GAP
    plan_height = page_h - (MARGIN * 2) - HEADER_H - FOOTER_H
    plan_box = (plan_left, plan_bottom, plan_width, plan_height)
    sidebar_box = (plan_left + plan_width + PLAN_GAP, plan_bottom, SIDEBAR_W, plan_height)

    transform = compute_transform(level, plan_box)

    draw_grid(pdf, transform, plan_box)

    if level.get("slab_regions"):
        for region in level["slab_regions"]:
            draw_polygon(pdf, region["polygon"], transform["to_page"], fill_color=SLAB_FILL, stroke_color=colors.HexColor("#c8c0b1"), stroke_width=0.9)

    for room in level.get("rooms", []):
        fill = CERTAINTY_FILL.get(room.get("certainty", "reconstructed"), CERTAINTY_FILL["reconstructed"])
        draw_polygon(pdf, room["polygon"], transform["to_page"], fill_color=fill, stroke_color=INNER_LINE, stroke_width=1.0)

    for fixture in level.get("fixtures", []):
        if fixture.get("type") == "floor_marker":
            draw_polygon(pdf, fixture["polygon"], transform["to_page"], fill_color=None, stroke_color=FIXTURE_FILL, stroke_width=1.0, dash=[4, 2])
        else:
            draw_polygon(pdf, fixture["polygon"], transform["to_page"], fill_color=FIXTURE_FILL, stroke_color=INNER_LINE, stroke_width=0.8)

    for stair in level.get("stairs", []):
        draw_polygon(pdf, stair["polygon"], transform["to_page"], fill_color=STAIR_FILL, stroke_color=colors.HexColor("#5b7f60"), stroke_width=1.0, dash=[2, 2])

    if level.get("footprint", {}).get("polygon"):
        draw_polygon(pdf, level["footprint"]["polygon"], transform["to_page"], fill_color=None, stroke_color=OUTLINE, stroke_width=2.0)

    for door in level.get("doors", []):
        draw_door(pdf, door, transform["to_page"])

    draw_room_labels(pdf, level, transform)
    draw_scale_bar(pdf, transform, plan_box)
    draw_sidebar(pdf, level, level_index, total_levels, sidebar_box, source_rel)


def export_pdf(data, json_path: Path, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(output_path), pagesize=PAGE_SIZE)

    source_rel = json_path.relative_to(PROJECT_DIR).as_posix() if json_path.is_relative_to(PROJECT_DIR) else json_path.name
    levels = build_levels(data)
    for index, level in enumerate(levels):
        draw_level(pdf, data, level, index, len(levels), source_rel)
        pdf.showPage()
    pdf.save()


def main():
    parser = argparse.ArgumentParser(description="Export a multi-page floor-plan PDF from the Crydee floor JSON.")
    parser.add_argument("json_path", nargs="?", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    data = load_json(args.json_path)
    export_pdf(data, args.json_path.resolve(), args.output.resolve())
    print(f"wrote: {args.output.resolve()}")


if __name__ == "__main__":
    main()
