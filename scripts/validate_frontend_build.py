#!/usr/bin/env python3
"""
Validate that the frontend demo is ready for a build-first screenshot workflow.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_manifest(root: Path, system_name: str) -> dict:
    manifest_path = root / system_name / "docs" / "Template" / "delivery-manifest.json"
    if manifest_path.exists():
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    return {}


def resolve_demo_dir(root: Path, system_name: str) -> Path:
    manifest = load_manifest(root, system_name)
    if manifest:
        return Path(manifest["paths"]["frontend_demo"])
    return root / system_name / "demo"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate that the demo frontend is suitable for a build-first screenshot workflow.",
    )
    parser.add_argument("--root", default=".", help="Workspace root")
    parser.add_argument("--system-name", required=True, help="System folder name")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    demo_dir = resolve_demo_dir(root, args.system_name.strip())
    package_json = demo_dir / "package.json"
    errors: list[str] = []
    warnings: list[str] = []

    if not demo_dir.exists():
        errors.append(f"Missing demo directory: {demo_dir}")
    if not package_json.exists():
        errors.append("Missing package.json")

    package_data = {}
    if package_json.exists():
        try:
            package_data = json.loads(package_json.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid package.json: {exc}")

    if package_data:
        scripts = package_data.get("scripts", {})
        if not isinstance(scripts, dict):
            errors.append("package.json scripts must be an object")
        else:
            if "build" not in scripts:
                errors.append("Missing scripts.build in package.json")
            if "preview" not in scripts:
                warnings.append("Missing scripts.preview in package.json")

    if (demo_dir / "vite.config.ts").exists() or (demo_dir / "vite.config.js").exists():
        warnings.append("Vite config detected. Prefer screenshotting the built preview instead of the dev server.")

    print(f"Demo directory: {demo_dir}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print("Frontend build validation failed.")
        return 1

    print("Frontend build validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

