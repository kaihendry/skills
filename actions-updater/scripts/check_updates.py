#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""Check GitHub Actions workflow files for available version updates.

Usage:
  uv run check_updates.py                        # scans .github/workflows/*.yml/*.yaml
  uv run check_updates.py path/to/workflow.yaml   # scans specific file(s)

Requires: gh cli (authenticated)
"""

import subprocess
import sys
from pathlib import Path

import yaml


def find_uses(node):
    """Recursively find all 'uses' values in a YAML structure."""
    actions = []
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "uses" and isinstance(value, str):
                actions.append(value)
            else:
                actions.extend(find_uses(value))
    elif isinstance(node, list):
        for item in node:
            actions.extend(find_uses(item))
    return actions


def major_version(tag):
    """Extract major version from a release tag, e.g. 'v6.0.2' -> 'v6'."""
    return tag.split(".")[0]


def get_latest_release(repo):
    """Query gh CLI for the latest release tag."""
    try:
        result = subprocess.run(
            ["gh", "release", "view", "--repo", repo,
             "--json", "tagName", "-q", ".tagName"],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


def main():
    if len(sys.argv) > 1:
        # Specific files passed as arguments
        files = [Path(f) for f in sys.argv[1:]]
        for f in files:
            if not f.is_file():
                print(f"Error: File not found: {f}", file=sys.stderr)
                sys.exit(1)
    else:
        # Default: scan .github/workflows/
        workflow_dir = Path(".github/workflows")
        if not workflow_dir.is_dir():
            print(f"Error: Directory not found: {workflow_dir}", file=sys.stderr)
            sys.exit(1)
        files = sorted(workflow_dir.glob("*.yml")) + sorted(workflow_dir.glob("*.yaml"))
        if not files:
            print(f"No workflow files found in {workflow_dir}", file=sys.stderr)
            sys.exit(1)

    print(f"Scanning: {', '.join(str(f) for f in files)}")
    print()

    # Parse all workflow files and collect unique actions
    all_actions = set()
    for filepath in files:
        with open(filepath) as fh:
            try:
                data = yaml.safe_load(fh)
                if data:
                    for action in find_uses(data):
                        if action.startswith("./") or action.startswith("docker://"):
                            continue
                        if "@" in action:
                            all_actions.add(action)
            except yaml.YAMLError as e:
                print(f"Warning: Failed to parse {filepath}: {e}", file=sys.stderr)

    if not all_actions:
        print("No external actions found.")
        sys.exit(0)

    print(f"{'ACTION':<45} {'CURRENT':<12} {'LATEST':<12} STATUS")
    print(f"{'------':<45} {'-------':<12} {'------':<12} ------")

    updates = 0
    for action in sorted(all_actions):
        repo, current = action.rsplit("@", 1)
        latest = get_latest_release(repo)

        if latest is None:
            print(f"{repo:<45} {current:<12} {'?':<12} no releases found")
            continue

        # Compare at major version level
        latest_major = major_version(latest)
        current_major = major_version(current)

        if current_major == latest_major:
            print(f"{repo:<45} {current:<12} {latest_major:<12} up to date")
        else:
            print(f"{repo:<45} {current:<12} {latest_major:<12} UPDATE AVAILABLE")
            updates += 1

    print()
    print(f"{updates} update(s) available.")


if __name__ == "__main__":
    main()
