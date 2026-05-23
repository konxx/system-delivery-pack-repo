#!/usr/bin/env python3
"""
Validate the non-runnable full-stack code pack for minimum breadth and volume.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
    "__pycache__",
    ".next",
    ".vite",
}

FRONTEND_EXTENSIONS = {".ts", ".tsx", ".js", ".jsx", ".css", ".scss", ".json"}
BACKEND_EXTENSIONS = {".py"}
SQL_EXTENSIONS = {".sql"}


def safe_path_name(value: str) -> str:
    cleaned = re.sub(r'[<>:"/\\\\|?*\x00-\x1f]+', "-", value.strip())
    cleaned = re.sub(r"\s+", "-", cleaned)
    cleaned = re.sub(r"-{2,}", "-", cleaned).strip(" .-")
    return cleaned or "system-app"


def load_manifest(root: Path, system_name: str) -> dict:
    if system_name.strip():
        direct_manifest = root / safe_path_name(system_name) / "docs" / "Template" / "delivery-manifest.json"
        if direct_manifest.exists():
            return json.loads(direct_manifest.read_text(encoding="utf-8"))

    direct_matches = list(root.glob("*/docs/Template/delivery-manifest.json"))
    if len(direct_matches) == 1:
        return json.loads(direct_matches[0].read_text(encoding="utf-8"))

    return {}


def resolve_system_dir(root: Path, system_name: str) -> Path:
    manifest = load_manifest(root, system_name)
    if manifest:
        return Path(manifest["paths"]["system_root"])
    return root / safe_path_name(system_name)


def iter_files(root: Path, extensions: set[str]) -> list[Path]:
    if not root.exists():
        return []

    result: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        if path.suffix.lower() in extensions:
            result.append(path)
    return result


def count_nonblank_lines(files: list[Path]) -> int:
    total = 0
    for path in files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        total += sum(1 for line in text.splitlines() if line.strip())
    return total


def parse_module_plan(system_dir: Path) -> list[str]:
    module_plan_file = system_dir / "docs" / "Template" / "module-plan.md"
    if not module_plan_file.exists():
        return []

    modules: list[str] = []
    seen: set[str] = set()
    text = module_plan_file.read_text(encoding="utf-8", errors="ignore")
    for line in text.splitlines():
        match = re.match(r"^\s*(?:\d+[\.\、]\s*|[-*]\s+)(.+?)\s*$", line)
        if not match:
            continue
        name = re.split(r"\s+[-—:：]\s+", match.group(1).strip(), maxsplit=1)[0].strip()
        if name and name not in seen:
            seen.add(name)
            modules.append(name)
    return modules


def count_create_tables(sql_files: list[Path]) -> int:
    count = 0
    for path in sql_files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        count += len(re.findall(r"\bCREATE\s+TABLE\b", text, flags=re.IGNORECASE))
    return count


def validate_code_pack(system_dir: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    code_dir = system_dir / "code"
    frontend_dir = code_dir / "frontend"
    backend_dir = code_dir / "backend"
    database_dir = code_dir / "database"

    modules = parse_module_plan(system_dir)
    module_count = len(modules)

    if not code_dir.exists():
        errors.append(f"Missing code directory: {code_dir}")
        return errors, warnings

    if module_count < 8 or module_count > 10:
        errors.append("docs/Template/module-plan.md must list 8-10 first-level modules before code validation.")

    for required_dir in (frontend_dir, backend_dir, database_dir):
        if not required_dir.exists():
            errors.append(f"Missing required code subdirectory: {required_dir}")

    frontend_src = frontend_dir / "src"
    frontend_modules_dir = frontend_src / "modules"
    frontend_files = iter_files(frontend_src, FRONTEND_EXTENSIONS)
    frontend_lines = count_nonblank_lines(frontend_files)
    frontend_module_dirs = [path for path in frontend_modules_dir.iterdir() if path.is_dir()] if frontend_modules_dir.exists() else []

    if not (frontend_dir / "package.json").exists():
        errors.append("code/frontend/package.json is required.")
    if not frontend_src.exists():
        errors.append("code/frontend/src is required.")
    if not any((frontend_src / name).exists() for name in ("main.tsx", "main.ts", "main.jsx", "main.js", "App.tsx", "App.jsx")):
        errors.append("code/frontend/src must include an entry file such as main.tsx or App.tsx.")
    if len(frontend_module_dirs) < max(8, module_count):
        errors.append(
            f"code/frontend/src/modules must contain at least {max(8, module_count)} module directories; found {len(frontend_module_dirs)}."
        )
    min_frontend_files = max(18, module_count * 2)
    min_frontend_lines = max(600, module_count * 70)
    if len(frontend_files) < min_frontend_files:
        errors.append(f"Frontend code pack is too small: {len(frontend_files)} source files, need at least {min_frontend_files}.")
    if frontend_lines < min_frontend_lines:
        errors.append(f"Frontend code pack is too small: {frontend_lines} nonblank lines, need at least {min_frontend_lines}.")

    backend_app = backend_dir / "app"
    backend_router_dir = backend_app / "routers"
    backend_files = iter_files(backend_dir, BACKEND_EXTENSIONS)
    backend_lines = count_nonblank_lines(backend_files)
    router_files = [path for path in backend_router_dir.glob("*.py") if path.stem != "__init__"] if backend_router_dir.exists() else []

    if not ((backend_app / "main.py").exists() or (backend_dir / "main.py").exists()):
        errors.append("code/backend must include app/main.py or main.py.")
    if not backend_router_dir.exists():
        errors.append("code/backend/app/routers is required.")
    if len(router_files) < max(8, module_count):
        errors.append(f"Backend must include at least {max(8, module_count)} router files; found {len(router_files)}.")
    min_backend_files = max(18, module_count * 2)
    min_backend_lines = max(500, module_count * 60)
    if len(backend_files) < min_backend_files:
        errors.append(f"Backend code pack is too small: {len(backend_files)} Python files, need at least {min_backend_files}.")
    if backend_lines < min_backend_lines:
        errors.append(f"Backend code pack is too small: {backend_lines} nonblank lines, need at least {min_backend_lines}.")

    sql_files = iter_files(database_dir, SQL_EXTENSIONS)
    sql_lines = count_nonblank_lines(sql_files)
    table_count = count_create_tables(sql_files)
    if len(sql_files) < 2:
        errors.append(f"Database pack must include at least 2 SQL files; found {len(sql_files)}.")
    if table_count < max(8, module_count):
        errors.append(f"Database schema must include at least {max(8, module_count)} CREATE TABLE statements; found {table_count}.")
    if sql_lines < 100:
        errors.append(f"Database SQL is too small: {sql_lines} nonblank lines, need at least 100.")

    total_files = len(frontend_files) + len(backend_files) + len(sql_files)
    total_lines = frontend_lines + backend_lines + sql_lines
    if total_files < 45:
        errors.append(f"Full-stack code pack is too small: {total_files} counted source files, need at least 45.")
    if total_lines < 1300:
        errors.append(f"Full-stack code pack is too small: {total_lines} nonblank lines, need at least 1300.")

    if frontend_lines < backend_lines // 2:
        warnings.append("Frontend code is much smaller than backend code; verify that frontend pages were not skipped.")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate that <system>/code contains a complete full-stack source pack before downstream delivery steps.",
    )
    parser.add_argument("--root", default=".", help="Workspace root")
    parser.add_argument("--system-name", required=True, help="Display name of the system")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    system_dir = resolve_system_dir(root, args.system_name.strip())
    errors, warnings = validate_code_pack(system_dir)

    print(f"System directory: {system_dir}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print("Full-stack code validation failed.")
        return 1

    print("Full-stack code validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
