import json
from pathlib import Path
from collections import defaultdict

FLOOR_DIR = Path("./examples")

def load_jsons():
    return [json.loads(p.read_text()) for p in FLOOR_DIR.glob("*.json")]

def validate_ids(data):
    seen = set()
    problems = []
    for group in ["walls", "doors", "stairs", "rooms", "hotspots"]:
        for item in data.get(group, []):
            item_id = item["id"]
            if item_id in seen:
                problems.append(f"Duplicate id: {item_id}")
            seen.add(item_id)
    return problems

def validate_door_wall_refs(data):
    wall_ids = {w["id"] for w in data["walls"]}
    problems = []
    for d in data["doors"]:
        if d["wall_id"] not in wall_ids:
            problems.append(f'Door {d["id"]} references missing wall {d["wall_id"]}')
    return problems

def validate_stair_alignment(datas):
    by_building = defaultdict(list)
    for d in datas:
        by_building[d["building"]].append(d)
    problems = []
    for building, floors in by_building.items():
        names = defaultdict(list)
        for f in floors:
            for s in f.get("stairs", []):
                names[s["name"]].append((f["floor"], round(s["x"], 2), round(s["y"], 2)))
        for stair_name, uses in names.items():
            xs = {u[1] for u in uses}
            ys = {u[2] for u in uses}
            if len(uses) > 1 and (len(xs) > 1 or len(ys) > 1):
                problems.append(f"{building}: stair '{stair_name}' misaligned across floors: {uses}")
    return problems

def main():
    datas = load_jsons()
    problems = []
    for d in datas:
        problems.extend([f'{d["id"]}: {p}' for p in validate_ids(d)])
        problems.extend([f'{d["id"]}: {p}' for p in validate_door_wall_refs(d)])
    problems.extend(validate_stair_alignment(datas))
    if problems:
        print("VALIDATION PROBLEMS:")
        for p in problems:
            print("-", p)
    else:
        print("All validations passed.")

if __name__ == "__main__":
    main()
