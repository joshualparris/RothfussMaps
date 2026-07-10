import argparse
import json
import math
import sys
from pathlib import Path


ALLOWED_CERTAINTY = {"canon", "implied", "reconstructed"}
ALLOWED_FLAG_LEVELS = {"pass", "info", "warning", "error"}
REQUIRED_TOP_LEVEL = [
    "structure",
    "level",
    "zone_role",
    "footprint",
    "spaces",
    "links",
    "labels",
    "validation_flags",
]
EPSILON = 1e-7


class ValidationIssue:
    def __init__(self, level, path, message):
        self.level = level
        self.path = path
        self.message = message

    def __str__(self):
        return f"{self.level.upper()} {self.path}: {self.message}"


def load_json(path):
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def add(issues, level, path, message):
    issues.append(ValidationIssue(level, path, message))


def is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def point_tuple(point):
    return (float(point["x"]), float(point["z"]))


def validate_point(point, path, issues):
    if not isinstance(point, dict):
        add(issues, "error", path, "Point must be an object with x and z.")
        return False
    ok = True
    for key in ("x", "z"):
        if key not in point:
            add(issues, "error", path, f"Missing coordinate '{key}'.")
            ok = False
        elif not is_number(point[key]):
            add(issues, "error", f"{path}.{key}", "Coordinate must be a finite number.")
            ok = False
    return ok


def polygon_area(polygon):
    area = 0.0
    points = [point_tuple(point) for point in polygon]
    for index, (x1, z1) in enumerate(points):
        x2, z2 = points[(index + 1) % len(points)]
        area += x1 * z2 - x2 * z1
    return area / 2.0


def on_segment(a, b, point):
    ax, ay = a
    bx, by = b
    px, py = point
    cross = (px - ax) * (by - ay) - (py - ay) * (bx - ax)
    if abs(cross) > EPSILON:
        return False
    return min(ax, bx) - EPSILON <= px <= max(ax, bx) + EPSILON and min(ay, by) - EPSILON <= py <= max(ay, by) + EPSILON


def orientation(a, b, c):
    value = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    if abs(value) <= EPSILON:
        return 0
    return 1 if value > 0 else -1


def segments_intersect(a, b, c, d, include_touch=True):
    o1 = orientation(a, b, c)
    o2 = orientation(a, b, d)
    o3 = orientation(c, d, a)
    o4 = orientation(c, d, b)

    if not include_touch:
        return o1 * o2 < 0 and o3 * o4 < 0

    if o1 != o2 and o3 != o4:
        return True

    return (
        (o1 == 0 and on_segment(a, b, c))
        or (o2 == 0 and on_segment(a, b, d))
        or (o3 == 0 and on_segment(c, d, a))
        or (o4 == 0 and on_segment(c, d, b))
    )


def polygon_edges(polygon):
    points = [point_tuple(point) for point in polygon]
    for index, start in enumerate(points):
        yield start, points[(index + 1) % len(points)], index


def point_in_polygon(point, polygon, include_boundary=True):
    pt = point_tuple(point) if isinstance(point, dict) else point
    points = [point_tuple(poly_point) for poly_point in polygon]

    for start, end, _ in polygon_edges(polygon):
        if on_segment(start, end, pt):
            return include_boundary

    inside = False
    x, y = pt
    previous = points[-1]
    for current in points:
        xi, yi = current
        xj, yj = previous
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / ((yj - yi) or EPSILON) + xi):
            inside = not inside
        previous = current
    return inside


def validate_polygon(polygon, path, issues):
    if not isinstance(polygon, list):
        add(issues, "error", path, "Polygon must be a list.")
        return False
    if len(polygon) < 3:
        add(issues, "error", path, "Polygon needs at least three points.")
        return False

    ok = True
    for index, point in enumerate(polygon):
        ok = validate_point(point, f"{path}[{index}]", issues) and ok

    if not ok:
        return False

    points = [point_tuple(point) for point in polygon]
    if points[0] == points[-1]:
        add(issues, "warning", path, "Polygon repeats its first point at the end; closure is implicit in this schema.")

    for index in range(len(points)):
        if points[index] == points[(index + 1) % len(points)]:
            add(issues, "error", path, f"Consecutive duplicate polygon point at index {index}.")
            ok = False

    if abs(polygon_area(polygon)) <= EPSILON:
        add(issues, "error", path, "Polygon area is zero or too small.")
        ok = False

    edge_count = len(points)
    for a_start, a_end, a_index in polygon_edges(polygon):
        for b_start, b_end, b_index in polygon_edges(polygon):
            if b_index <= a_index:
                continue
            adjacent = abs(a_index - b_index) == 1 or {a_index, b_index} == {0, edge_count - 1}
            if adjacent:
                continue
            if segments_intersect(a_start, a_end, b_start, b_end, include_touch=True):
                add(issues, "error", path, f"Polygon self-intersects between edges {a_index} and {b_index}.")
                ok = False

    return ok


def validate_required(data, issues):
    for key in REQUIRED_TOP_LEVEL:
        if key not in data:
            add(issues, "error", key, "Missing required top-level key.")


def validate_certainty(value, path, issues):
    if value not in ALLOWED_CERTAINTY:
        add(issues, "error", path, f"Invalid certainty '{value}'. Expected one of {sorted(ALLOWED_CERTAINTY)}.")


def validate_certified_item(item, path, issues, require_id=True):
    if not isinstance(item, dict):
        add(issues, "error", path, "Expected object.")
        return
    if require_id and not item.get("id"):
        add(issues, "error", f"{path}.id", "Missing id.")
    if "certainty" not in item:
        add(issues, "error", f"{path}.certainty", "Missing certainty tag.")
    else:
        validate_certainty(item["certainty"], f"{path}.certainty", issues)
    if "geometry_certainty" in item:
        validate_certainty(item["geometry_certainty"], f"{path}.geometry_certainty", issues)


def collect_ids(data, issues):
    seen = {}
    groups = [
        ("footprint", [data.get("footprint")]),
        ("spaces", data.get("spaces", [])),
        ("links", data.get("links", [])),
        ("vertical_links", data.get("vertical_links", [])),
        ("fixtures", data.get("fixtures", [])),
        ("labels", data.get("labels", [])),
        ("validation_flags", data.get("validation_flags", [])),
    ]

    for group, items in groups:
        if not isinstance(items, list):
            add(issues, "error", group, "Expected a list.")
            continue
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                continue
            item_id = item.get("id")
            if not item_id:
                continue
            if item_id in seen:
                add(issues, "error", f"{group}[{index}].id", f"Duplicate id '{item_id}' also used at {seen[item_id]}.")
            else:
                seen[item_id] = f"{group}[{index}]"
    return seen


def validate_containment(data, issues):
    footprint_polygon = data.get("footprint", {}).get("polygon")
    if not isinstance(footprint_polygon, list):
        return

    for group in ("spaces", "vertical_links", "fixtures"):
        for index, item in enumerate(data.get(group, [])):
            polygon = item.get("polygon")
            if not isinstance(polygon, list):
                continue
            for point_index, point in enumerate(polygon):
                if validate_point(point, f"{group}[{index}].polygon[{point_index}]", []):
                    if not point_in_polygon(point, footprint_polygon, include_boundary=True):
                        add(issues, "error", f"{group}[{index}].polygon[{point_index}]", "Point sits outside footprint.")

    for index, label in enumerate(data.get("labels", [])):
        position = label.get("position")
        if isinstance(position, dict) and validate_point(position, f"labels[{index}].position", []):
            if not point_in_polygon(position, footprint_polygon, include_boundary=True):
                add(issues, "warning", f"labels[{index}].position", "Label position sits outside footprint.")


def validate_space_overlaps(data, issues):
    spaces = data.get("spaces", [])
    for left_index, left in enumerate(spaces):
        left_polygon = left.get("polygon")
        if not isinstance(left_polygon, list):
            continue
        for right_index in range(left_index + 1, len(spaces)):
            right = spaces[right_index]
            right_polygon = right.get("polygon")
            if not isinstance(right_polygon, list):
                continue

            overlap = False
            for point in left_polygon:
                pt = point_tuple(point)
                if point_in_polygon(pt, right_polygon, include_boundary=False):
                    overlap = True
                    break
            for point in right_polygon:
                pt = point_tuple(point)
                if point_in_polygon(pt, left_polygon, include_boundary=False):
                    overlap = True
                    break
            for a_start, a_end, _ in polygon_edges(left_polygon):
                for b_start, b_end, _ in polygon_edges(right_polygon):
                    if segments_intersect(a_start, a_end, b_start, b_end, include_touch=False):
                        overlap = True
                        break
                if overlap:
                    break

            if overlap:
                add(
                    issues,
                    "error",
                    f"spaces[{left_index}], spaces[{right_index}]",
                    f"Space polygons overlap with positive area: {left.get('id')} and {right.get('id')}.",
                )


def validate_link_references(data, issues):
    space_ids = {space.get("id") for space in data.get("spaces", []) if isinstance(space, dict)}
    allowed = space_ids | {"exterior"}
    footprint_polygon = data.get("footprint", {}).get("polygon", [])

    for index, link in enumerate(data.get("links", [])):
        path = f"links[{index}]"
        validate_certified_item(link, path, issues)

        connects = link.get("connects")
        if not isinstance(connects, list) or len(connects) < 2:
            add(issues, "error", f"{path}.connects", "Link must connect at least two spaces.")
        else:
            for ref in connects:
                if ref not in allowed:
                    add(issues, "error", f"{path}.connects", f"Link references unknown space '{ref}'.")

        line = link.get("line")
        if not isinstance(line, dict):
            add(issues, "error", f"{path}.line", "Link must define a line with start and end points.")
            continue
        if not validate_point(line.get("start"), f"{path}.line.start", issues):
            continue
        if not validate_point(line.get("end"), f"{path}.line.end", issues):
            continue

        start = point_tuple(line["start"])
        end = point_tuple(line["end"])
        if start == end:
            add(issues, "error", f"{path}.line", "Link line has zero length.")

        if footprint_polygon:
            if not point_in_polygon(start, footprint_polygon, include_boundary=True):
                add(issues, "error", f"{path}.line.start", "Link start sits outside footprint.")
            if not point_in_polygon(end, footprint_polygon, include_boundary=True):
                add(issues, "error", f"{path}.line.end", "Link end sits outside footprint.")


def validate_vertical_link_references(data, issues):
    space_ids = {space.get("id") for space in data.get("spaces", []) if isinstance(space, dict)}
    level_id = data.get("level", {}).get("id")

    for index, link in enumerate(data.get("vertical_links", [])):
        path = f"vertical_links[{index}]"
        validate_certified_item(link, path, issues)

        access_from = link.get("access_from")
        if access_from is not None and access_from not in space_ids:
            add(issues, "error", f"{path}.access_from", f"Vertical link references unknown space '{access_from}'.")

        if link.get("from_level") is not None and link.get("from_level") != level_id:
            add(issues, "warning", f"{path}.from_level", "from_level does not match this level id.")


def validate_draft_flags(data, issues):
    level = data.get("level", {})
    if level.get("draft") is not True:
        add(issues, "error", "level.draft", "Draft/source status must be explicit and true for approximate reconstruction data.")
    if level.get("approximate_dimensions") is not True:
        add(issues, "error", "level.approximate_dimensions", "Approximate dimensions must be explicitly flagged.")

    for group in ("spaces", "links", "vertical_links", "fixtures"):
        for index, item in enumerate(data.get(group, [])):
            if item.get("approximate") is not True:
                add(issues, "warning", f"{group}[{index}].approximate", "Approximate geometry should be explicitly flagged true.")

    messages = " ".join(flag.get("message", "").lower() for flag in data.get("validation_flags", []) if isinstance(flag, dict))
    if "approximate" not in messages and "uncertain" not in messages:
        add(issues, "warning", "validation_flags", "Validation flags should mention approximate or uncertain geometry.")


def validate_validation_flags(data, issues):
    for index, flag in enumerate(data.get("validation_flags", [])):
        path = f"validation_flags[{index}]"
        if not isinstance(flag, dict):
            add(issues, "error", path, "Validation flag must be an object.")
            continue
        if not flag.get("id"):
            add(issues, "error", f"{path}.id", "Missing validation flag id.")
        if flag.get("level") not in ALLOWED_FLAG_LEVELS:
            add(issues, "error", f"{path}.level", f"Invalid flag level. Expected one of {sorted(ALLOWED_FLAG_LEVELS)}.")
        if not flag.get("message"):
            add(issues, "error", f"{path}.message", "Missing validation message.")


def validate(data):
    issues = []
    validate_required(data, issues)

    if "schema_version" in data and data["schema_version"] != "canon_structure_plan_v01":
        add(issues, "warning", "schema_version", "Expected 'canon_structure_plan_v01'.")

    validate_certified_item(data.get("structure", {}), "structure", issues)
    validate_certified_item(data.get("footprint", {}), "footprint", issues)
    if isinstance(data.get("level"), dict):
        validate_certainty(data["level"].get("certainty"), "level.certainty", issues)
    if isinstance(data.get("zone_role"), dict):
        validate_certainty(data["zone_role"].get("certainty"), "zone_role.certainty", issues)

    collect_ids(data, issues)

    footprint_polygon = data.get("footprint", {}).get("polygon")
    if footprint_polygon is not None:
        validate_polygon(footprint_polygon, "footprint.polygon", issues)

    for group in ("spaces", "vertical_links", "fixtures"):
        for index, item in enumerate(data.get(group, [])):
            polygon = item.get("polygon")
            if polygon is not None:
                validate_polygon(polygon, f"{group}[{index}].polygon", issues)

    for index, space in enumerate(data.get("spaces", [])):
        validate_certified_item(space, f"spaces[{index}]", issues)

    for index, label in enumerate(data.get("labels", [])):
        validate_certified_item(label, f"labels[{index}]", issues)
        position = label.get("position")
        if position is not None:
            validate_point(position, f"labels[{index}].position", issues)

    validate_containment(data, issues)
    validate_space_overlaps(data, issues)
    validate_link_references(data, issues)
    validate_vertical_link_references(data, issues)
    validate_draft_flags(data, issues)
    validate_validation_flags(data, issues)

    return issues


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate canon-safe Crydee structure JSON.")
    parser.add_argument("json_path", type=Path, help="Path to a canon_structure_plan_v01 JSON file.")
    parser.add_argument("--warnings-as-errors", action="store_true", help="Return failure if warnings are found.")
    args = parser.parse_args(argv)

    data = load_json(args.json_path)
    issues = validate(data)

    errors = [issue for issue in issues if issue.level == "error"]
    warnings = [issue for issue in issues if issue.level == "warning"]

    if issues:
        print(f"Validation report for {args.json_path}")
        for issue in issues:
            print(f"- {issue}")
    else:
        print(f"Validation passed: {args.json_path}")

    if errors or (args.warnings_as_errors and warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

