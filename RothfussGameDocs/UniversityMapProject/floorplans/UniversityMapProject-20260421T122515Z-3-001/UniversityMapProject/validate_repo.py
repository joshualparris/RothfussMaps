#!/usr/bin/env python3
"""
Validation script for University Map Project.
Checks for contradictions, hard-ban violations, and consistency issues.
"""

import os
import json
import re
from pathlib import Path

def load_manifest():
    with open('canon_manifest.json', 'r') as f:
        return json.load(f)

def check_archives_height():
    """Check that Archives site and prompt have six stories."""
    errors = []
    archives_files = [
        'ai-prompts/archives-site-plan.md',
        'ai-prompts/archives-prompt.md'
    ]
    for file in archives_files:
        if os.path.exists(file):
            with open(file, 'r') as f:
                content = f.read()
                if 'five-story' in content.lower():
                    errors.append(f"{file}: contains 'five-story'")
                if 'six-story' not in content.lower():
                    errors.append(f"{file}: missing 'six-story'")
    return errors

def check_archives_windows():
    """Check for hard ban violations: no windows in Archives without windowless or no windows context."""
    errors = []
    archives_files = [
        'ai-prompts/archives-site-plan.md',
        'ai-prompts/archives-prompt.md',
        'ai-prompts/floor-plan-archives-ground.md',
        'ai-prompts/floor-plan-archives-2nd.md',
        'ai-prompts/floor-plan-archives-3rd.md',
        'ai-prompts/floor-plan-archives-4th.md',
        'ai-prompts/floor-plan-archives-5th.md',
        'ai-prompts/floor-plan-archives-6th.md'
    ]
    for file in archives_files:
        if os.path.exists(file):
            with open(file, 'r') as f:
                content = f.read()
                if 'window' in content.lower() and 'windowless' not in content.lower() and 'no windows' not in content.lower():
                    errors.append(f"{file}: mentions windows without windowless or no windows context")
    return errors

def check_natural_light():
    """Check for natural light in windowless buildings."""
    errors = []
    files_to_check = [
        'ai-prompts/archives-prompt.md',
        'ai-prompts/archives-site-plan.md'
    ]
    for file in files_to_check:
        if os.path.exists(file):
            with open(file, 'r') as f:
                content = f.read()
                if 'natural light' in content.lower():
                    errors.append(f"{file}: contains 'natural light' in windowless building")
    return errors

def check_floor_specificity():
    """Check that Archives floor prompts are floor-specific."""
    errors = []
    floor_files = [
        ('ai-prompts/floor-plan-archives-ground.md', 'entry sequence'),
        ('ai-prompts/floor-plan-archives-2nd.md', 'scriv-work'),
        ('ai-prompts/floor-plan-archives-3rd.md', 'sorting hall'),
        ('ai-prompts/floor-plan-archives-4th.md', 'cataloger'),
        ('ai-prompts/floor-plan-archives-5th.md', 'scriptorium'),
        ('ai-prompts/floor-plan-archives-6th.md', 'roof access')
    ]
    for file, expected in floor_files:
        if os.path.exists(file):
            with open(file, 'r') as f:
                content = f.read()
                if expected not in content.lower():
                    errors.append(f"{file}: missing floor-specific content '{expected}'")
    return errors

def main():
    manifest = load_manifest()
    errors = []

    errors.extend(check_archives_height())
    errors.extend(check_archives_windows())
    errors.extend(check_natural_light())
    errors.extend(check_floor_specificity())

    if errors:
        print("Validation failed with the following errors:")
        for error in errors:
            print(f"- {error}")
        return 1
    else:
        print("Validation passed.")
        return 0

if __name__ == '__main__':
    exit(main())