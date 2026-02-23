#!/usr/bin/env python3
import json
import subprocess
import sys
from datetime import datetime


def get_git_branch():
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, timeout=3
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return "N/A"


def get_project_name():
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, timeout=3
        )
        if result.returncode == 0:
            return result.stdout.strip().rsplit("/", 1)[-1]
    except Exception:
        pass
    return "N/A"


def abbreviate_model(model_id):
    """Convert full model ID to abbreviated format.

    Examples:
        claude-opus-4-6 -> Opus 4.6
        claude-sonnet-4-5-20250929 -> Sonnet 4.5
        claude-haiku-4-5-20251001 -> Haiku 4.5
    """
    # Extract major and minor version numbers
    import re

    # Pattern to match model type and version
    match = re.search(r'claude-(opus|sonnet|haiku)-(\d+)-(\d+)', model_id.lower())
    if match:
        model_type = match.group(1).capitalize()
        major_version = match.group(2)
        minor_version = match.group(3)
        return f"{model_type} {major_version}.{minor_version}"

    # Fallback to original ID if pattern doesn't match
    return model_id


def main():
    data = json.loads(sys.stdin.read())

    # Extract model ID from the model object
    model_obj = data.get("model", {})
    if isinstance(model_obj, dict):
        model_id = model_obj.get("id", "unknown")
    else:
        model_id = str(model_obj)

    model = abbreviate_model(model_id)
    now = datetime.now().strftime("%H:%M:%S")
    branch = get_git_branch()
    project = get_project_name()

    parts = [
        f"🕐 {now}",
        f"🤖 {model}",
        f"📁 {project}",
        f"🔀 {branch}",
    ]
    print(" | ".join(parts))


if __name__ == "__main__":
    main()
