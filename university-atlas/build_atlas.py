from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ATLAS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = ATLAS_DIR.parent
DATA_FILE = ATLAS_DIR / "atlas-data.js"

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}
DOC_EXTS = {".docx", ".md", ".json", ".txt"}


DISTRICTS = {
    "campus": {
        "name": "Bridge & First Sight",
        "motto": "Where Stonebridge, the Archives, and the whole University first resolve into shape.",
        "order": 1,
    },
    "eastern": {
        "name": "The Stone Mind",
        "motto": "Archives, Hollows, and the paper-heavy edge of the University.",
        "order": 2,
    },
    "oldheart": {
        "name": "The Old Heart",
        "motto": "The old academic core, its accreted halls, and the Masters' more private authority.",
        "order": 3,
    },
    "student": {
        "name": "Student Life",
        "motto": "Where beds, baths, meals, and the daily rhythm of students belong.",
        "order": 4,
    },
    "workings": {
        "name": "The Workings",
        "motto": "Heat, industry, sympathy, and the practical labor of the University.",
        "order": 5,
    },
    "northern": {
        "name": "Northern Edge",
        "motto": "The formal road north, the fence, and the dangerous stillness of Haven.",
        "order": 6,
    },
    "below": {
        "name": "Below the University",
        "motto": "The buried routes, warm pipes, cracked halls, and hidden approaches under everything.",
        "order": 7,
    },
}


AREA_META: dict[str, dict[str, Any]] = {
    "1 Campus Wide ": {
        "id": "campus",
        "title": "Campus Wide",
        "district": "campus",
        "order": 1,
        "blurb": "Master campus studies for the University approach, bridge logic, and overall settlement shape.",
        "canon_note": "Use this as the first image anchor before switching to any building shell or interior level.",
        "overview_title": "Campus Studies",
        "links": [
            ("Master Campus Prompt", "ai-prompts/university-site-plan.md"),
            ("Campus Freeze", "campus-layout.md"),
        ],
    },
    "2 Archives": {
        "id": "archives",
        "title": "The Archives",
        "district": "eastern",
        "order": 2,
        "blurb": "The five-story stone mind of the University: threshold logic first, public Tomes next, deeper Stacks after.",
        "canon_note": "Current canon freeze is five occupied stories plus a roof. Older sixth-level studies are preserved but marked legacy.",
        "overview_title": "Overall Studies",
        "links": [
            ("Archives Site Plan Prompt", "ai-prompts/archives-site-plan.md"),
            ("Archives Ground Floor Prompt", "ai-prompts/floor-plan-archives-ground.md"),
            ("Archives Floorplan JSON", "floorplans/archives-floorplan.json"),
            ("Archives Brief", "buildings/archives-brief.md"),
        ],
    },
    "3 Bursar_s Office ": {
        "id": "bursar",
        "title": "Bursar's Office",
        "district": "eastern",
        "order": 4,
        "blurb": "A route-driven study: courtyard, stone building, hallway, stairs down, then the bursar.",
        "canon_note": "The route sequence matters more than office ornament or administrative over-detail.",
        "overview_title": "Bursar Approach Studies",
        "links": [
            ("Bursar Site Plan Prompt", "ai-prompts/bursar-office-site-plan.md"),
            ("Bursar Floor Prompt", "ai-prompts/floor-plan-bursar-office-ground.md"),
        ],
    },
    "4 The Crucible ": {
        "id": "crucible",
        "title": "The Crucible",
        "district": "workings",
        "order": 10,
        "blurb": "A chimney-heavy chemical or sympathy work building where atmosphere and flue logic matter more than ornament.",
        "canon_note": "Treat the industrial scent and chimney forest as stronger anchors than any specific room roster.",
        "overview_title": "Crucible Studies",
        "links": [
            ("Crucible Site Plan Prompt", "ai-prompts/crucible-site-plan.md"),
            ("Crucible Floor Prompt", "ai-prompts/floor-plan-crucible-ground.md"),
        ],
    },
    "5 The Fishery": {
        "id": "fishery",
        "title": "The Fishery / Artificery",
        "district": "workings",
        "order": 9,
        "blurb": "The great industrial workshop: low east-wall windows, a south courtyard exit, and Kilvin's office opening off the main floor.",
        "canon_note": "Treat Fishery and Artificery as one working complex unless a narrower distinction becomes necessary.",
        "overview_title": "Fishery Studies",
        "links": [
            ("Fishery Site Plan Prompt", "ai-prompts/fishery-artificery-site-plan.md"),
            ("Fishery Ground Floor Prompt", "ai-prompts/floor-plan-fishery-artificery-ground.md"),
            ("Fishery Reconstruction Brief", "reconstruction-briefs/fishery-artificery-reconstruction.md"),
        ],
    },
    "6 Haven": {
        "id": "haven",
        "title": "Haven",
        "district": "northern",
        "order": 11,
        "blurb": "The north-road asylum-compound: manor-like, fenced, elegant at first glance, and built for danger underneath that polish.",
        "canon_note": "This is not a Masters' office building. It must stay separate, formal, and unsettling.",
        "overview_title": "Haven Studies",
        "links": [
            ("Haven Site Plan Prompt", "ai-prompts/haven-site-plan.md"),
            ("Haven Ground Floor Prompt", "ai-prompts/floor-plan-haven-ground.md"),
            ("Haven Brief", "buildings/haven-brief.md"),
        ],
    },
    "7 Hollows": {
        "id": "hollows",
        "title": "Hollows",
        "district": "eastern",
        "order": 3,
        "blurb": "Square, stained-glass, and close to the Archives: admissions, offices, and a building with more locked routes than it first appears.",
        "canon_note": "Elodin's office is canon here. The lecture-hall placement remains more fragile and should stay marked as reconstructed when asserted.",
        "overview_title": "Hollows Dossier",
        "links": [
            ("Hollows Site Plan Prompt", "ai-prompts/hollows-site-plan.md"),
            ("Hollows Ground Floor Prompt", "ai-prompts/floor-plan-hollows-ground.md"),
            ("Hollows Brief", "buildings/hollows-brief.md"),
        ],
    },
    "8 Mains": {
        "id": "mains",
        "title": "The Mains",
        "district": "oldheart",
        "order": 5,
        "blurb": "The sprawling old heart of the University: accreted, crooked, and more maze than plan.",
        "canon_note": "Any clean, unified shell is suspect here. The Mains should feel swallowed together over centuries.",
        "overview_title": "Mains Dossier",
        "links": [
            ("Mains Site Plan Prompt", "ai-prompts/mains-site-plan.md"),
            ("Mains Ground Floor Prompt", "ai-prompts/floor-plan-mains-ground.md"),
            ("Mains Brief", "buildings/mains-brief.md"),
            ("Mains Floorplan JSON", "floorplans/mains-floorplan.json"),
        ],
    },
    "9 Masters Hall": {
        "id": "masters-hall",
        "title": "Masters' Hall",
        "district": "oldheart",
        "order": 6,
        "blurb": "Senior lodging and governance space: quieter, greyer, and less theatrical than Hollows.",
        "canon_note": "No renders yet. The hall remains mixed residential-governance space, not a pure office block.",
        "overview_title": "Masters' Hall Queue",
        "links": [
            ("Masters' Hall Site Plan Prompt", "ai-prompts/masters-hall-site-plan.md"),
            ("Masters' Hall Floor Prompt", "ai-prompts/floor-plan-masters-hall-ground.md"),
            ("Masters' Hall Brief", "buildings/masters-hall-brief.md"),
        ],
    },
    "10 Medica": {
        "id": "medica",
        "title": "The Medica",
        "district": "eastern",
        "order": 7,
        "blurb": "The large, oddly shaped medical institution on the far side of the Archives from one known approach.",
        "canon_note": "The Medica is a real institution, not a tiny infirmary. It serves townspeople too, not just students.",
        "overview_title": "Medica Studies",
        "links": [
            ("Medica Site Plan Prompt", "ai-prompts/medica-site-plan.md"),
            ("Medica Ground Floor Prompt", "ai-prompts/floor-plan-medica-ground.md"),
            ("Medica Reconstruction Brief", "reconstruction-briefs/medica-reconstruction.md"),
        ],
    },
    "11 Mess": {
        "id": "mess",
        "title": "The Mess",
        "district": "student",
        "order": 8,
        "blurb": "The long, low-roofed dining hall across the lawn from the Mews.",
        "canon_note": "No renders yet. The anchor facts are the lawn relationship, the long low roof, and the roughly two hundred seats at plank tables.",
        "overview_title": "Mess Queue",
        "links": [
            ("Mess Site Plan Prompt", "ai-prompts/mess-site-plan.md"),
            ("Mess Ground Floor Prompt", "ai-prompts/floor-plan-mess-ground.md"),
            ("Mess Reconstruction Brief", "reconstruction-briefs/mess-reconstruction.md"),
        ],
    },
    "12 Mews": {
        "id": "mews",
        "title": "The Mews",
        "district": "student",
        "order": 7,
        "blurb": "The radial student residence: hub, eight wings, baths below, and a lingering east-wing upper-level tension.",
        "canon_note": "No top-level Mews renders are in this drop yet. The current bridge keeps the exterior three-storied while allowing a reconstructed partial upper east-wing level.",
        "overview_title": "Mews Queue",
        "links": [
            ("Mews Site Plan Prompt", "ai-prompts/mews-site-plan.md"),
            ("Mews Ground Floor Prompt", "ai-prompts/floor-plan-mews-ground.md"),
            ("Mews Brief", "buildings/mews-brief.md"),
            ("Mews Floorplan JSON", "floorplans/mews-floorplan.json"),
        ],
    },
    "13 Underthing": {
        "id": "underthing",
        "title": "The Underthing",
        "district": "below",
        "order": 12,
        "blurb": "The buried counter-map beneath the University: grates, steam, crawlways, cracks, wind, and hidden approaches.",
        "canon_note": "Treat these as network studies, not as a fully solved single map. The Underthing remains broader than any one floor plan.",
        "overview_title": "Underthing Studies",
        "links": [
            ("Underthing Site Plan Prompt", "ai-prompts/underthing-site-plan.md"),
            ("Underthing Main-Level Prompt", "ai-prompts/floor-plan-underthing-main.md"),
            ("Underthing Reconstruction Brief", "reconstruction-briefs/underthing-reconstruction.md"),
        ],
    },
}


ITEM_OVERRIDES: dict[tuple[str, str], dict[str, Any]] = {
    ("2 Archives", "__root__"): {
        "title": "Overall Studies",
        "note": "Collected shell or overview studies that sit above the level-by-level Archives work.",
        "badge": "overview",
        "kind": "overview",
        "order": 0,
    },
    ("2 Archives", "Archives - Level 0 Ground Floor "): {
        "title": "Ground Floor",
        "note": "Threshold logic, antechamber branching, Tomes access, and the first constrained public reading layer.",
        "badge": "level",
    },
    ("2 Archives", "Archives - Level 1"): {
        "title": "Level 1",
        "note": "The first restricted layer above the public threshold.",
        "badge": "level",
    },
    ("2 Archives", "Archives - Level 2"): {
        "title": "Level 2",
        "note": "A deeper restricted layer continuing the Stacks-city logic.",
        "badge": "level",
    },
    ("2 Archives", "Archives - Level 3"): {
        "title": "Level 3",
        "note": "Mid-stack study with more maze pressure and inherited disorder.",
        "badge": "level",
    },
    ("2 Archives", "Archives - Level 4"): {
        "title": "Level 4",
        "note": "Upper restricted district study.",
        "badge": "level",
    },
    ("2 Archives", "Archives - Level 5_"): {
        "title": "Level 5",
        "note": "Top occupied floor study under the current five-story freeze.",
        "badge": "level",
    },
    ("2 Archives", "Archives - Level 6"): {
        "title": "Legacy Level 6",
        "note": "Preserved from the older six-story interpretation. Keep this separate from the current five-story-plus-roof canon freeze.",
        "badge": "legacy",
        "kind": "legacy",
        "order": 96,
        "caution": "legacy drift",
    },
    ("2 Archives", "Archives - Roof_"): {
        "title": "Roof",
        "note": "Bare roof studies above the courtyard edge.",
        "badge": "roof",
        "kind": "roof",
    },
    ("2 Archives", "Archives - Tomes"): {
        "title": "Tomes",
        "note": "Public reading-room studies. Better lit than the rest of the Archives, but still windowless.",
        "badge": "room",
    },
    ("2 Archives", "Archives - Stacks"): {
        "title": "Stacks",
        "note": "Restricted Stacks studies with darker, lamp-scale logic.",
        "badge": "room",
    },
    ("2 Archives", "Archives - Acquisitions Room"): {
        "title": "Acquisitions Office",
        "note": "The tiny, dark room dominated by the lacquered acquisition map.",
        "badge": "room",
    },
    ("7 Hollows", "Hollows - Level 0 Basement "): {
        "title": "Level 0 Basement",
        "note": "Highly reconstructed below-grade Hollows study. Treat as a speculative support layer, not settled canon.",
        "badge": "reconstructed",
        "caution": "high reconstruction",
    },
    ("7 Hollows", "Hollows - Level 1-Ground Floor"): {
        "title": "Ground Floor",
        "note": "The main Hollows shell study for admissions and office logic.",
        "badge": "level",
    },
    ("7 Hollows", "Hollows - Level 2"): {
        "title": "Level 2",
        "note": "Upper Hollows study with more reconstruction than the ground floor.",
        "badge": "level",
    },
    ("7 Hollows", "Hollows - Admissions Theatre "): {
        "title": "Admissions Theatre",
        "note": "Room study focused on the dark theatre and raised crescent table.",
        "badge": "room",
    },
    ("7 Hollows", "Hollows - Ledgers and Lists"): {
        "title": "Ledgers and Lists",
        "note": "Legacy placement study. The office exists canonically, but its placement inside Hollows is not frozen canon.",
        "badge": "legacy",
        "caution": "location unsettled",
    },
    ("8 Mains", "Mains - Level 1 - Ground Floor"): {
        "title": "Ground Floor",
        "note": "The crooked heart of the Mains, with accreted circulation and non-rational room shape.",
        "badge": "level",
    },
    ("8 Mains", "Mains - Elodin_s Lecture Hall"): {
        "title": "Elodin's Lecture Hall",
        "note": "Preserved as a lecture-hall study. Building placement remains unsettled in the broader project freeze.",
        "badge": "legacy",
        "caution": "building assignment unsettled",
    },
    ("6 Haven", "Haven - Level 1"): {
        "title": "Level 1",
        "note": "Formal entry and ward-level studies.",
        "badge": "level",
    },
    ("6 Haven", "Haven - Level 2"): {
        "title": "Level 2",
        "note": "Upper Haven study continuing the institutional and secure-compound logic.",
        "badge": "level",
    },
    ("10 Medica", "__root__"): {
        "title": "Ground Floor Studies",
        "note": "Current Medica render set is focused on the ground floor treatment level.",
        "badge": "level",
        "kind": "level",
    },
    ("13 Underthing", "__root__"): {
        "title": "Underthing Studies",
        "note": "Representative network studies rather than a full solved map of every buried route.",
        "badge": "network",
    },
    ("5 The Fishery", "__root__"): {
        "title": "Fishery Studies",
        "note": "Workshop and complex-level studies for the industrial quarter.",
        "badge": "overview",
    },
    ("4 The Crucible ", "__root__"): {
        "title": "Crucible Studies",
        "note": "Chimney-heavy work-building studies.",
        "badge": "overview",
    },
    ("3 Bursar_s Office ", "__root__"): {
        "title": "Bursar Approach Studies",
        "note": "Route-centered studies preserving the courtyard, stone building, hallway, and descent.",
        "badge": "overview",
    },
}


def natural_key(text: str) -> list[Any]:
    parts = re.split(r"(\d+)", text.lower())
    out: list[Any] = []
    for part in parts:
        if part.isdigit():
            out.append(int(part))
        else:
            out.append(part)
    return out


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = text.replace("_s", "'s")
    text = text.replace("_", " ")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def clean_name(text: str) -> str:
    text = text.strip().replace("_s", "'s").replace("_", " ")
    text = re.sub(r"\s+", " ", text)
    text = text.rstrip(" -")
    return text


def infer_kind(name: str) -> str:
    lowered = name.lower()
    if "roof" in lowered:
        return "roof"
    if "level" in lowered or "ground floor" in lowered or "basement" in lowered:
        return "level"
    if any(token in lowered for token in ["theatre", "office", "room", "bathing", "tomes", "stacks"]):
        return "room"
    return "overview"


def infer_badge(kind: str) -> str:
    return {
        "level": "level",
        "room": "room",
        "roof": "roof",
        "legacy": "legacy",
    }.get(kind, "overview")


def infer_order(name: str, kind: str) -> int:
    lowered = name.lower()
    if kind == "overview":
        return 0
    if "basement" in lowered or "level 0" in lowered:
        return 10
    if "ground floor" in lowered:
        return 20
    match = re.search(r"level\s*(\d+)", lowered)
    if match:
        return 20 + int(match.group(1)) * 10
    if "roof" in lowered:
        return 95
    if kind == "room":
        return 60
    return 80


def rel_from_atlas(path: Path) -> str:
    return path.relative_to(ATLAS_DIR).as_posix() if path.is_relative_to(ATLAS_DIR) else Path("..", path.relative_to(PROJECT_ROOT)).as_posix()


def file_entry(path: Path) -> dict[str, Any]:
    return {
        "name": path.name,
        "path": rel_from_atlas(path),
        "ext": path.suffix.lower(),
    }


def collect_files(folder: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    images = sorted(
        [file_entry(p) for p in folder.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXTS],
        key=lambda item: natural_key(item["name"]),
    )
    docs = sorted(
        [file_entry(p) for p in folder.rglob("*") if p.is_file() and p.suffix.lower() in DOC_EXTS],
        key=lambda item: natural_key(item["name"]),
    )
    return images, docs


def build_item(area_folder_name: str, item_key: str, source_folder: Path, *, is_root: bool = False) -> dict[str, Any] | None:
    images, docs = collect_files(source_folder)
    if not images and not docs:
        return None

    override = ITEM_OVERRIDES.get((area_folder_name, item_key), {})
    raw_title = AREA_META[area_folder_name].get("overview_title", "Overview") if is_root else clean_name(item_key)
    kind = override.get("kind", infer_kind(raw_title))
    title = override.get("title", raw_title)
    order = override.get("order", infer_order(title, kind))

    return {
        "id": slugify(title if not is_root else f"{AREA_META[area_folder_name]['id']}-overview"),
        "title": title,
        "kind": kind,
        "badge": override.get("badge", infer_badge(kind)),
        "order": order,
        "note": override.get("note", ""),
        "caution": override.get("caution", ""),
        "images": images,
        "docs": docs,
        "imageCount": len(images),
    }


def build_area(folder_name: str) -> dict[str, Any]:
    meta = AREA_META[folder_name]
    folder = PROJECT_ROOT / folder_name

    items: list[dict[str, Any]] = []

    root_images = sorted([p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTS], key=lambda p: natural_key(p.name))
    root_docs = sorted([p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in DOC_EXTS], key=lambda p: natural_key(p.name))
    if root_images or root_docs:
        item = build_item(folder_name, "__root__", folder, is_root=True)
        if item:
            items.append(item)

    for child in sorted([p for p in folder.iterdir() if p.is_dir()], key=lambda p: natural_key(p.name)):
        item = build_item(folder_name, child.name, child)
        if item:
            items.append(item)

    items.sort(key=lambda item: (item["order"], natural_key(item["title"])))

    total_images = sum(item["imageCount"] for item in items)
    status = "awaiting" if total_images == 0 else "rendered"

    return {
        "id": meta["id"],
        "title": meta["title"],
        "folder": folder_name,
        "district": meta["district"],
        "districtName": DISTRICTS[meta["district"]]["name"],
        "order": meta["order"],
        "blurb": meta["blurb"],
        "canonNote": meta["canon_note"],
        "status": status,
        "renderCount": total_images,
        "links": [{"label": label, "path": rel_from_atlas(PROJECT_ROOT / path)} for label, path in meta["links"]],
        "items": items,
    }


def main() -> None:
    areas = [build_area(folder_name) for folder_name in AREA_META]
    areas.sort(key=lambda area: (DISTRICTS[area["district"]]["order"], area["order"]))

    payload = {
        "title": "The University Atlas",
        "subtitle": "A browser for campus studies, building shells, floor plans, room work, and unresolved legacy branches.",
        "generatedFrom": str(PROJECT_ROOT),
        "districts": [
            {
                "id": district_id,
                "name": meta["name"],
                "motto": meta["motto"],
                "order": meta["order"],
            }
            for district_id, meta in sorted(DISTRICTS.items(), key=lambda item: item[1]["order"])
        ],
        "areas": areas,
    }

    DATA_FILE.write_text(
        "window.UNIVERSITY_ATLAS_DATA = " + json.dumps(payload, indent=2, ensure_ascii=False) + ";\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
