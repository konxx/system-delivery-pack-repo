#!/usr/bin/env python3
"""
Check that built frontend routes render usable HTML before screenshots are taken.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path


FAIL_MARKERS = [
    "cannot get /",
    "not found",
    "application error",
    "unexpected application error",
    "vite",
]


def load_manifest(root: Path, system_name: str) -> dict:
    manifest_path = root / system_name / "docs" / "Template" / "delivery-manifest.json"
    if manifest_path.exists():
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    return {}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate that frontend routes return usable HTML before screenshot capture.",
    )
    parser.add_argument("--root", default=".", help="Workspace root")
    parser.add_argument("--system-name", required=True, help="System folder name")
    parser.add_argument("--base-url", required=True, help="Base URL of the running preview server")
    parser.add_argument(
        "--routes",
        nargs="*",
        default=["/", "/#dashboard"],
        help="Routes to validate",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    manifest = load_manifest(root, args.system_name.strip())
    if manifest:
        print(f"Using manifest for: {manifest.get('system_name')}")

    errors: list[str] = []
    for route in args.routes:
        url = args.base_url.rstrip("/") + route
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                body = response.read().decode("utf-8", errors="ignore").lower()
                status = getattr(response, "status", 200)
        except urllib.error.URLError as exc:
            errors.append(f"{route}: request failed: {exc}")
            continue

        if status >= 400:
            errors.append(f"{route}: bad status code {status}")
            continue

        if "<div id=\"root\"" not in body and "<div id='root'" not in body:
            errors.append(f"{route}: root container not found")
            continue

        if any(marker in body for marker in FAIL_MARKERS):
            errors.append(f"{route}: page content suggests an error or dev-only fallback")

    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print("Frontend route validation failed.")
        return 1

    print("Frontend route validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

