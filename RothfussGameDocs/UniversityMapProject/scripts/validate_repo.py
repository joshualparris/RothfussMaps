import difflib
import glob
import json
import os
import sys


ROOT = os.path.dirname(os.path.abspath(__file__))
MANIFEST_PATH = os.path.join(ROOT, "canon_manifest.json")


def load_manifest():
    with open(MANIFEST_PATH, "r", encoding="utf-8") as fh:
        return json.load(fh)


def read_text(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def norm(text):
    return text.lower()


def contains(text, pattern):
    return pattern.lower() in text


def validate_rule(rule):
    scope = os.path.join(ROOT, rule["scope_glob"])
    files = sorted(glob.glob(scope))
    failures = []
    contents = [(path, norm(read_text(path))) for path in files]

    for path, text in contents:
        for pattern in rule.get("must_not_contain_any", []):
            if contains(text, pattern):
                failures.append(f"{rule['rule_id']}: banned text '{pattern}' in {os.path.relpath(path, ROOT)}")

        must_contain_all = rule.get("must_contain_all", [])
        for pattern in must_contain_all:
            if not contains(text, pattern):
                failures.append(f"{rule['rule_id']}: missing required text '{pattern}' in {os.path.relpath(path, ROOT)}")

        must_contain_any = rule.get("must_contain_any")
        if must_contain_any and not any(contains(text, p) for p in must_contain_any):
            failures.append(
                f"{rule['rule_id']}: none of the required anchors {must_contain_any} found in {os.path.relpath(path, ROOT)}"
            )

        for conditional in rule.get("if_contains_then_require", []):
            trigger = conditional["trigger"]
            if contains(text, trigger):
                required = conditional["require_any"]
                if not any(contains(text, p) for p in required):
                    failures.append(
                        f"{rule['rule_id']}: found trigger '{trigger}' without any of {required} in {os.path.relpath(path, ROOT)}"
                    )

    threshold = rule.get("max_pairwise_similarity")
    if threshold is not None:
        for i in range(len(contents)):
            for j in range(i + 1, len(contents)):
                a_path, a_text = contents[i]
                b_path, b_text = contents[j]
                ratio = difflib.SequenceMatcher(None, a_text, b_text).ratio()
                if ratio > threshold:
                    failures.append(
                        f"{rule['rule_id']}: {os.path.relpath(a_path, ROOT)} and {os.path.relpath(b_path, ROOT)} similarity {ratio:.3f} exceeds {threshold:.3f}"
                    )

    return failures


def main():
    manifest = load_manifest()
    all_failures = []
    for rule in manifest.get("validation_rules", []):
        all_failures.extend(validate_rule(rule))

    if all_failures:
        print("VALIDATION FAILED")
        for failure in all_failures:
            print(f"- {failure}")
        return 1

    print("VALIDATION PASSED")
    print(f"Checked {len(manifest.get('validation_rules', []))} rules from canon_manifest.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
