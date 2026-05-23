#!/usr/bin/env python3
"""
Generate a code source DOCX by wrapping the user-installed `codeclean` CLI.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path


def safe_path_name(value: str) -> str:
    cleaned = re.sub(r'[<>:"/\\\\|?*\x00-\x1f]+', "-", value.strip())
    cleaned = re.sub(r"\s+", "-", cleaned)
    cleaned = re.sub(r"-{2,}", "-", cleaned).strip(" .-")
    return cleaned or "system-app"


def display_system_name(system_name: str) -> str:
    name = system_name.strip()
    return name if name.endswith("系统") else f"{name}系统"


def load_manifest(root: Path, system_name: str) -> dict:
    direct_manifest = root / safe_path_name(system_name) / "docs" / "Template" / "delivery-manifest.json"
    if direct_manifest.exists():
        return json.loads(direct_manifest.read_text(encoding="utf-8"))

    direct_matches = list(root.glob("*/docs/Template/delivery-manifest.json"))
    if len(direct_matches) == 1:
        return json.loads(direct_matches[0].read_text(encoding="utf-8"))

    legacy_manifest = root / "outputs" / "Template" / "delivery-manifest.json"
    if legacy_manifest.exists():
        return json.loads(legacy_manifest.read_text(encoding="utf-8"))

    return {}


def resolve_system_dir(root: Path, system_name: str) -> Path:
    manifest = load_manifest(root, system_name)
    safe_name = manifest.get("system_folder") or safe_path_name(system_name)
    return root / safe_name


def locate_generated_docx(docs_dir: Path, display_name: str) -> Path:
    candidates = [
        docs_dir / f"{display_name}-代码(前后30页).docx",
        docs_dir / f"{display_name}-代码(全量备份).docx",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate

    matches = sorted(
        docs_dir.glob(f"{display_name}-代码*.docx"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    if matches:
        return matches[0]

    raise FileNotFoundError(f"No codeclean output found in {docs_dir}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Wrap the user-installed codeclean CLI and rename the generated code-source DOCX.",
    )
    parser.add_argument("--root", default=".", help="Workspace root")
    parser.add_argument("--system-name", required=True, help="Display name of the system")
    parser.add_argument("--version", default="V1.0", help="Version string for the output file")
    parser.add_argument(
        "--suffixes",
        default="py,sql,tsx,ts,js,jsx,json,yml,yaml,html,css",
        help="Comma-separated source suffixes to include",
    )
    parser.add_argument("--key", default="937599", help="codeclean key")
    parser.add_argument("--order", default="2", help="codeclean order flag: 1 shuffle, 2 path order")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    system_name = display_system_name(args.system_name.strip())
    version = args.version.strip() or "V1.0"
    system_dir = resolve_system_dir(root, args.system_name.strip())
    code_dir = system_dir / "code"
    docs_dir = system_dir / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)

    if not code_dir.exists():
        raise FileNotFoundError(f"Code directory not found: {code_dir}")

    command = [
        "codeclean",
        system_name,
        version,
        str(code_dir),
        args.suffixes,
        args.key,
        str(args.order),
    ]
    subprocess.run(command, cwd=str(docs_dir), check=True)

    generated_docx = locate_generated_docx(docs_dir, system_name)
    final_docx = docs_dir / f"{system_name}代码源程序{version}.docx"
    if final_docx.exists():
        final_docx.unlink()
    generated_docx.replace(final_docx)

    print(f"Code source DOCX: {final_docx}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
