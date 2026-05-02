#!/usr/bin/env python3
"""
Validate that the pure frontend demo has the minimum structure needed before launching and screenshotting it.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_manifest(root: Path, system_name: str) -> dict:
    system_dir = root / system_name
    manifest_path = system_dir / "docs" / "Template" / "delivery-manifest.json"
    if manifest_path.exists():
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    return {}


def validate_demo(demo_dir: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not demo_dir.exists():
        errors.append(f"Missing demo directory: {demo_dir}")
        return errors, warnings

    package_json = demo_dir / "package.json"
    index_html = demo_dir / "index.html"
    src_dir = demo_dir / "src"

    if not package_json.exists():
        errors.append("Missing package.json")
    if not index_html.exists():
        errors.append("Missing index.html")
    if not src_dir.exists():
        errors.append("Missing src directory")

    package_data = {}
    if package_json.exists():
        try:
            package_data = json.loads(package_json.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid package.json: {exc}")

    if package_data:
        scripts = package_data.get("scripts", {})
        dependencies = package_data.get("dependencies", {})
        dev_dependencies = package_data.get("devDependencies", {})

        if not isinstance(scripts, dict):
            errors.append("package.json scripts must be an object")
        else:
            if "dev" not in scripts:
                errors.append("Missing scripts.dev in package.json")
            if "build" not in scripts:
                warnings.append("Missing scripts.build in package.json")

        if "react" not in dependencies:
            warnings.append("Missing react dependency")
        if "react-dom" not in dependencies:
            warnings.append("Missing react-dom dependency")
        if "vite" not in dev_dependencies and "vite" not in dependencies:
            warnings.append("Missing vite dependency")

    if src_dir.exists():
        main_candidates = [
            src_dir / "main.tsx",
            src_dir / "main.ts",
            src_dir / "main.jsx",
            src_dir / "main.js",
            src_dir / "App.tsx",
            src_dir / "App.jsx",
        ]
        if not any(path.exists() for path in main_candidates):
            errors.append("Missing frontend entry file such as src/main.tsx or src/App.tsx")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate that the demo frontend has the minimum required structure before Playwright screenshots.",
    )
    parser.add_argument("--root", default=".", help="Workspace root")
    parser.add_argument("--system-name", required=True, help="System folder name")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    manifest = load_manifest(root, args.system_name.strip())
    demo_dir = None

    if manifest:
        demo_dir = Path(manifest["paths"]["frontend_demo"])
    else:
        demo_dir = root / args.system_name.strip() / "demo"

    errors, warnings = validate_demo(demo_dir)

    print(f"Demo directory: {demo_dir}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print("Frontend demo validation failed.")
        return 1

    print("Frontend demo validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

