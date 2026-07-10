import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
MANIFEST_PATH = PROJECT_DIR / "data" / "pipeline_manifest.json"
GATES_PATH = PROJECT_DIR / "data" / "review_gates.json"
LOG_PATH = PROJECT_DIR / "logs" / "pipeline_last_run.json"

GATE_OK = {"approved", "approved_for_blockout", "generated", "ready"}
GATE_REQUIREMENTS = {
    "validate": [],
    "blender": ["floor_json_frozen"],
    "godot": ["blender_blockout_generated"],
}


def utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path):
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")


def rel(path):
    path = Path(path)
    try:
        return str(path.resolve().relative_to(PROJECT_DIR))
    except ValueError:
        return str(path)


def project_path(value):
    path = Path(value)
    if path.is_absolute():
        return path
    return PROJECT_DIR / path


def load_manifest():
    return load_json(MANIFEST_PATH)


def load_gates():
    if not GATES_PATH.exists():
        return {"schema_version": "university_review_gates_v01", "targets": {}}
    return load_json(GATES_PATH)


def target_key(building, floor):
    return f"{building}:{floor}"


def find_target(manifest, building, floor):
    for target in manifest.get("targets", []):
        if target.get("building") == building and target.get("floor") == floor:
            return target
    raise SystemExit(f"No pipeline target found for {building}/{floor}. Add it to {rel(MANIFEST_PATH)}.")


def print_heading(text):
    print()
    print(text)
    print("=" * len(text))


def run_command(command, dry_run=False):
    print(f"Command: {' '.join(str(part) for part in command)}")
    if dry_run:
        print("Dry run: command not executed.")
        return 0
    completed = subprocess.run(command, cwd=PROJECT_DIR)
    return completed.returncode


def run_command_capture(command, dry_run=False):
    print(f"Command: {' '.join(str(part) for part in command)}")
    if dry_run:
        print("Dry run: command not executed.")
        return 0, ""
    completed = subprocess.run(
        command,
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        errors="replace",
    )
    if completed.stdout:
        print(completed.stdout)
    return completed.returncode, completed.stdout or ""


def record_run(building, floor, stage, status, message):
    payload = {
        "building": building,
        "floor": floor,
        "stage": stage,
        "status": status,
        "message": message,
        "updated_at": utc_now(),
    }
    write_json(LOG_PATH, payload)


def get_target_gates(gates, building, floor):
    return gates.setdefault("targets", {}).setdefault(target_key(building, floor), {})


def show_gates(building, floor):
    gates = load_gates()
    target_gates = get_target_gates(gates, building, floor)
    print_heading(f"Review Gates: {building}/{floor}")
    for name, data in target_gates.items():
        print(f"- {name}: {data.get('status', 'missing')}")
        note = data.get("note")
        if note:
            print(f"  note: {note}")


def set_gate(building, floor, gate_name, status, note):
    gates = load_gates()
    target_gates = get_target_gates(gates, building, floor)
    target_gates[gate_name] = {
        "status": status,
        "updated_at": utc_now(),
        "note": note or "",
    }
    write_json(GATES_PATH, gates)
    print(f"Set gate {gate_name} for {building}/{floor} to {status}.")


def require_gates(building, floor, stage, review_gates):
    if review_gates == "off":
        return True

    gates = load_gates()
    target_gates = get_target_gates(gates, building, floor)
    missing = []
    for gate_name in GATE_REQUIREMENTS.get(stage, []):
        status = target_gates.get(gate_name, {}).get("status", "missing")
        if status not in GATE_OK:
            missing.append((gate_name, status))

    if not missing:
        return True

    print_heading("Review Gate Blocked")
    for gate_name, status in missing:
        print(f"- {gate_name}: {status}")
    print("Use --review-gates off for a deliberate bypass, or approve the gate explicitly.")
    return False


def find_blender(provided=None):
    if provided:
        path = Path(provided)
        return path if path.exists() else None

    path = shutil.which("blender")
    if path:
        return Path(path)

    candidates = [
        Path(r"C:\Program Files\Blender Foundation"),
        PROJECT_DIR,
        PROJECT_DIR.parent,
    ]
    for root in candidates:
        if root.exists():
            for exe in root.rglob("blender.exe"):
                return exe
    return None


def find_godot(provided=None):
    if provided:
        path = Path(provided)
        return path if path.exists() else None

    path = shutil.which("godot")
    if path:
        return Path(path)

    for exe in PROJECT_DIR.rglob("Godot*_console.exe"):
        return exe
    for exe in PROJECT_DIR.rglob("Godot*.exe"):
        if exe.suffix.lower() == ".exe":
            return exe
    return None


def stage_audit(target):
    print_heading("Pipeline Audit")
    items = [
        ("source_json", target["source_json"]),
        ("schema", target["schema"]),
        ("building_brief", target["building_brief"]),
        ("validator", load_manifest()["defaults"]["validator"]),
        ("blender_importer", load_manifest()["defaults"]["blender_importer"]),
        ("godot_setup", load_manifest()["defaults"]["godot_setup"]),
        ("review_gates", rel(GATES_PATH)),
    ]
    for label, path in items:
        resolved = project_path(path)
        exists = "yes" if resolved.exists() else "no"
        print(f"- {label}: {path} exists={exists}")

    print()
    print("Known mismatch resolved by this harness:")
    print("- Old files used building_id/floor_id/metadata/geometries.")
    print("- Current authoritative source uses building/floor/story_role/footprint/rooms/doors/stairs/labels/validation_flags.")
    print("- Blender importer targets one JSON and uses source x/z -> Blender x/y with Blender z as up.")
    return 0


def stage_validate(target, dry_run=False):
    validator = project_path(load_manifest()["defaults"]["validator"])
    source_json = project_path(target["source_json"])
    command = [sys.executable, str(validator), str(source_json)]
    return run_command(command, dry_run=dry_run)


def stage_blender(target, blender_exe=None, dry_run=False):
    blender = find_blender(blender_exe)
    if blender is None:
        print("Blender executable not found. Add Blender to PATH or pass --blender-exe.")
        return 2

    importer = project_path(load_manifest()["defaults"]["blender_importer"])
    source_json = project_path(target["source_json"])
    export_blend = project_path(target["export_blend"])
    export_glb = project_path(target["export_glb"])
    export_blend.parent.mkdir(parents=True, exist_ok=True)
    export_glb.parent.mkdir(parents=True, exist_ok=True)

    command = [
        str(blender),
        "--background",
        "--python",
        str(importer),
        "--",
        str(source_json),
        "--clear-scene",
        "--save-blend",
        str(export_blend),
        "--export-glb",
        str(export_glb),
    ]
    result = run_command(command, dry_run=dry_run)
    if result == 0 and not dry_run:
        set_gate(target["building"], target["floor"], "blender_blockout_generated", "generated", f"Generated {rel(export_blend)} and {rel(export_glb)}.")
    return result


def stage_godot(target, godot_exe=None, dry_run=False, force=False):
    setup_script = project_path(load_manifest()["defaults"]["godot_setup"])
    source_json = project_path(target["source_json"])
    export_glb = project_path(target["export_glb"])
    command = [
        sys.executable,
        str(setup_script),
        str(source_json),
        "--asset-path",
        str(export_glb),
    ]
    if force:
        command.append("--force")

    result = run_command(command, dry_run=dry_run)
    if result != 0 or dry_run:
        return result

    godot = find_godot(godot_exe)
    if godot is None:
        print("Godot project scaffold created. Godot executable not found, so editor smoke test was skipped.")
    else:
        godot_project = project_path(target["godot_project"])
        import_cmd = [str(godot), "--headless", "--import", "--path", str(godot_project)]
        result, output = run_command_capture(import_cmd, dry_run=False)
        if result != 0 or "ERROR:" in output:
            set_gate(target["building"], target["floor"], "godot_test_ready", "pending", "Godot import reported errors. See latest pipeline output.")
            return result or 1

        scene_path = project_path(target["godot_main_scene"]).resolve()
        scene_res = "res://" + scene_path.relative_to(godot_project.resolve()).as_posix()
        smoke = [str(godot), "--headless", "--path", str(godot_project), "--scene", scene_res, "--quit-after", "2"]
        result, output = run_command_capture(smoke, dry_run=False)
        if result != 0 or "ERROR:" in output:
            set_gate(target["building"], target["floor"], "godot_test_ready", "pending", "Godot scene smoke test reported errors. See latest pipeline output.")
            return result

    if export_glb.exists():
        set_gate(target["building"], target["floor"], "godot_test_ready", "ready", f"Godot scaffold points at {rel(export_glb)}.")
    else:
        set_gate(target["building"], target["floor"], "godot_test_ready", "pending", "Godot scaffold exists, but generated GLB is still missing.")
    return 0


def run_stage(args, target, stage):
    if not require_gates(args.building, args.floor, stage, args.review_gates):
        return 2

    if stage == "audit":
        return stage_audit(target)
    if stage == "validate":
        return stage_validate(target, dry_run=args.dry_run)
    if stage == "blender":
        return stage_blender(target, blender_exe=args.blender_exe, dry_run=args.dry_run)
    if stage == "godot":
        return stage_godot(target, godot_exe=args.godot_exe, dry_run=args.dry_run, force=args.force)
    raise SystemExit(f"Unknown stage: {stage}")


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Run the University reconstruction automation pipeline.")
    parser.add_argument("--building", default="archives")
    parser.add_argument("--floor", default="ground")
    parser.add_argument("--stage", choices=["audit", "validate", "blender", "godot", "all"], default="validate")
    parser.add_argument("--review-gates", choices=["on", "off"], default="on")
    parser.add_argument("--show-gates", action="store_true")
    parser.add_argument("--approve-gate", help="Approve or update a review gate for the target, then exit.")
    parser.add_argument("--gate-status", default="approved", help="Status to use with --approve-gate.")
    parser.add_argument("--note", default="", help="Note to store with --approve-gate.")
    parser.add_argument("--blender-exe", help="Path to blender.exe.")
    parser.add_argument("--godot-exe", help="Path to Godot executable.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true", help="Allow scaffold scripts to overwrite generated files.")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    manifest = load_manifest()
    target = find_target(manifest, args.building, args.floor)

    if args.show_gates:
        show_gates(args.building, args.floor)
        return 0

    if args.approve_gate:
        set_gate(args.building, args.floor, args.approve_gate, args.gate_status, args.note)
        return 0

    stages = ["validate", "blender", "godot"] if args.stage == "all" else [args.stage]
    for stage in stages:
        print_heading(f"Stage: {stage}")
        result = run_stage(args, target, stage)
        if result != 0:
            record_run(args.building, args.floor, stage, "failed", f"Stage exited with code {result}.")
            return result

    record_run(args.building, args.floor, args.stage, "passed", "Pipeline stage(s) completed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
