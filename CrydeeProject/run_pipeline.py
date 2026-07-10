import argparse
import json
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
    "source-audit": [],
    "audit": [],
    "validate": [],
    "blender": [],
    "godot": ["floor_json_frozen"],
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


def project_path(value):
    path = Path(value)
    if path.is_absolute():
        return path
    return PROJECT_DIR / path


def load_manifest():
    return load_json(MANIFEST_PATH)


def load_gates():
    if not GATES_PATH.exists():
        return {"schema_version": "crydee_review_gates_v01", "targets": {}}
    return load_json(GATES_PATH)


def find_target(manifest, target_id):
    for target in manifest.get("targets", []):
        if target.get("target_id") == target_id:
            return target
    raise SystemExit(f"No pipeline target found for {target_id}. Add it to {MANIFEST_PATH}.")


def print_heading(text):
    print()
    print(text)
    print("=" * len(text))


def run_command(command):
    print(f"Command: {' '.join(str(part) for part in command)}")
    completed = subprocess.run(command, cwd=PROJECT_DIR)
    return completed.returncode


def run_command_capture(command):
    print(f"Command: {' '.join(str(part) for part in command)}")
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


def record_run(target_id, stage, status, message):
    payload = {
        "target_id": target_id,
        "stage": stage,
        "status": status,
        "message": message,
        "updated_at": utc_now(),
    }
    write_json(LOG_PATH, payload)


def get_target_gates(gates, target_id):
    return gates.setdefault("targets", {}).setdefault(target_id, {})


def show_gates(target_id):
    gates = load_gates()
    target_gates = get_target_gates(gates, target_id)
    print_heading(f"Review Gates: {target_id}")
    for name, data in target_gates.items():
        print(f"- {name}: {data.get('status', 'missing')}")
        note = data.get("note")
        if note:
            print(f"  note: {note}")


def set_gate(target_id, gate_name, status, note):
    gates = load_gates()
    target_gates = get_target_gates(gates, target_id)
    target_gates[gate_name] = {
        "status": status,
        "updated_at": utc_now(),
        "note": note or "",
    }
    write_json(GATES_PATH, gates)
    print(f"Set gate {gate_name} for {target_id} to {status}.")


def require_gates(target_id, stage):
    gates = load_gates()
    target_gates = get_target_gates(gates, target_id)
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
    return False


def find_godot(provided=None):
    if provided:
        path = Path(provided)
        return path if path.exists() else None

    for exe in PROJECT_DIR.rglob("Godot*_console.exe"):
        return exe
    for exe in PROJECT_DIR.rglob("Godot*.exe"):
        if exe.suffix.lower() == ".exe":
            return exe
    return None


def stage_source_audit(target, manifest):
    script = project_path(manifest["defaults"]["source_auditor"])
    pdf_path = project_path(target["source_pdf"])
    doc_out = project_path(target["source_audit_doc"])
    json_out = PROJECT_DIR / "logs" / "source_audit.json"
    result = run_command(
        [
            sys.executable,
            str(script),
            "--pdf",
            str(pdf_path),
            "--doc-out",
            str(doc_out),
            "--json-out",
            str(json_out),
        ]
    )
    if result == 0:
        set_gate(target["target_id"], "source_audit_generated", "generated", f"Generated {doc_out} and {json_out}.")
    return result


def stage_audit(manifest):
    validator = project_path(manifest["defaults"]["repo_validator"])
    return run_command([sys.executable, str(validator)])


def stage_validate(target, manifest):
    source_json = project_path(target["source_json"])
    if not source_json.exists():
        print("Crydee source JSON is missing.")
        print(f"Expected target: {source_json}")
        return 2

    validator = project_path(manifest["defaults"]["validator"])
    return run_command([sys.executable, str(validator), str(source_json)])


def stage_blender():
    print("Blender generation is optional for the current Crydee prototype.")
    print("The working walkthrough is generated directly in Godot from the floor JSON.")
    return 0


def stage_godot(target, manifest, godot_exe=None, force=False):
    source_json = project_path(target["source_json"])
    if not source_json.exists():
        print("Crydee source JSON is missing.")
        print(f"Expected target: {source_json}")
        return 2

    setup_script = project_path(manifest["defaults"]["godot_setup"])
    command = [sys.executable, str(setup_script), str(source_json)]

    asset_path = target.get("godot_asset_path")
    if asset_path:
        command.extend(["--asset-path", str(project_path(asset_path))])
    if force:
        command.append("--force")

    result = run_command(command)
    if result != 0:
        return result

    godot = find_godot(godot_exe)
    if godot is None:
        print("Godot executable not found, so import and smoke test were skipped.")
        return 2

    godot_project = project_path(target["godot_project"])
    result, output = run_command_capture([str(godot), "--headless", "--import", "--path", str(godot_project)])
    if result != 0 or "ERROR:" in output:
        return result or 1

    scene_path = project_path(target["godot_main_scene"]).resolve()
    scene_res = "res://" + scene_path.relative_to(godot_project.resolve()).as_posix()
    result, output = run_command_capture(
        [str(godot), "--headless", "--path", str(godot_project), "--scene", scene_res, "--quit-after", "2"]
    )
    if result != 0 or "ERROR:" in output:
        return result or 1

    set_gate(target["target_id"], "godot_test_ready", "ready", f"Godot walkthrough smoke-tested successfully for {scene_res}.")
    return 0


def run_stage(stage, target, manifest, args):
    if not require_gates(target["target_id"], stage):
        return 2

    if stage == "source-audit":
        return stage_source_audit(target, manifest)
    if stage == "audit":
        return stage_audit(manifest)
    if stage == "validate":
        return stage_validate(target, manifest)
    if stage == "blender":
        return stage_blender()
    if stage == "godot":
        return stage_godot(target, manifest, godot_exe=args.godot_exe, force=args.force)
    raise SystemExit(f"Unknown stage: {stage}")


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Run the Crydee reconstruction scaffold pipeline.")
    parser.add_argument("--target", default="castle_crydee:site")
    parser.add_argument("--stage", choices=["source-audit", "audit", "validate", "blender", "godot", "all"], default="all")
    parser.add_argument("--show-gates", action="store_true")
    parser.add_argument("--approve-gate", help="Approve or update a review gate for the target, then exit.")
    parser.add_argument("--gate-status", default="approved", help="Status to use with --approve-gate.")
    parser.add_argument("--note", default="", help="Note to store with --approve-gate.")
    parser.add_argument("--godot-exe", help="Optional path to the Godot executable.")
    parser.add_argument("--force", action="store_true", help="Allow generators to overwrite generated files.")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    manifest = load_manifest()
    target = find_target(manifest, args.target)

    if args.show_gates:
        show_gates(args.target)
        return 0

    if args.approve_gate:
        set_gate(args.target, args.approve_gate, args.gate_status, args.note)
        return 0

    stages = ["source-audit", "audit", "validate", "godot"] if args.stage == "all" else [args.stage]
    for stage in stages:
        print_heading(f"Stage: {stage}")
        result = run_stage(stage, target, manifest, args)
        if result != 0:
            record_run(args.target, stage, "failed", f"Stage exited with code {result}.")
            return result

    record_run(args.target, args.stage, "passed", "Pipeline stage(s) completed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
