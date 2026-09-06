#!/usr/bin/env python3
"""
Create the standard output tree for the ruanzhu skill.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path


DEFAULT_AGREEMENT_DATE = "2026年4月15日"
DEFAULT_MANUAL_REVISION_DATE = "2026-6-15"
DEFAULT_TECHNICAL_STYLE = "React + TypeScript、FastAPI、PostgreSQL，界面按选定 UI prompt 与布局原型实现"
DEFAULT_TECHNICAL_HIGHLIGHTS = ["模块化全栈架构", "角色权限与操作审计", "可视化业务分析"]


def safe_path_name(value: str) -> str:
    cleaned = re.sub(r'[<>:"/\\\\|?*\x00-\x1f]+', "-", value.strip())
    cleaned = re.sub(r"\s+", "-", cleaned)
    cleaned = re.sub(r"-{2,}", "-", cleaned).strip(" .-")
    return cleaned or "system-app"


def copy_if_missing(source: Path, target: Path) -> bool:
    if target.exists():
        return False
    shutil.copy2(source, target)
    return True


def build_manifest(
    root: Path,
    system_name: str,
    system_folder: str,
    *,
    agreement_date: str,
    manual_revision_date: str,
    technical_style: str,
    technical_highlights: list[str],
) -> dict:
    system_dir = root / system_folder
    docs_dir = system_dir / "docs"
    template_dir = docs_dir / "Template"
    return {
        "system_name": system_name,
        "system_folder": system_folder,
        "paths": {
            "system_root": str(system_dir),
            "fullstack_code": str(system_dir / "code"),
            "frontend_demo": str(system_dir / "demo"),
            "photos": str(system_dir / "photos"),
            "docs": str(docs_dir),
            "templates": str(template_dir),
        },
        "template_files": {
            "agreement_seed": str(template_dir / f"{system_folder}-agreement-template.md"),
            "manual_seed": str(template_dir / f"{system_folder}-manual-template.md"),
        },
        "delivery_preferences": {
            "agreement_date": agreement_date,
            "manual_revision_date": manual_revision_date,
            "technical_style": technical_style,
            "technical_highlights": technical_highlights,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create <system>/code, <system>/demo, <system>/photos, <system>/docs, and <system>/docs/Template.",
    )
    parser.add_argument("--root", default=".", help="Workspace root")
    parser.add_argument("--system-name", required=True, help="Display name of the system")
    parser.add_argument(
        "--document-date",
        default="",
        help="Apply one user-supplied date to both the agreement and manual",
    )
    parser.add_argument("--agreement-date", default="", help="Override only the agreement date")
    parser.add_argument("--manual-date", default="", help="Override only the manual revision date")
    parser.add_argument("--technical-style", default="", help="Requested stack, architecture, or UI direction")
    parser.add_argument(
        "--technical-highlight",
        action="append",
        default=[],
        help="Repeat for each requested technical highlight",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    skill_dir = Path(__file__).resolve().parent.parent
    assets_dir = skill_dir / "assets"

    system_name = args.system_name.strip()
    system_folder = safe_path_name(system_name)
    shared_date = args.document_date.strip()
    agreement_date = args.agreement_date.strip() or shared_date or DEFAULT_AGREEMENT_DATE
    manual_revision_date = args.manual_date.strip() or shared_date or DEFAULT_MANUAL_REVISION_DATE
    technical_style = args.technical_style.strip() or DEFAULT_TECHNICAL_STYLE
    technical_highlights = [item.strip() for item in args.technical_highlight if item.strip()]
    if not technical_highlights:
        technical_highlights = list(DEFAULT_TECHNICAL_HIGHLIGHTS)

    system_dir = root / system_folder
    code_dir = system_dir / "code"
    photos_dir = system_dir / "photos"
    docs_dir = system_dir / "docs"
    template_dir = docs_dir / "Template"
    frontend_dir = system_dir / "demo"

    for path in (system_dir, code_dir, photos_dir, docs_dir, template_dir, frontend_dir):
        path.mkdir(parents=True, exist_ok=True)

    agreement_seed_target = template_dir / f"{system_folder}-agreement-template.md"
    manual_seed_target = template_dir / f"{system_folder}-manual-template.md"

    copied_files = []
    if copy_if_missing(assets_dir / "agreement-template.md", agreement_seed_target):
        copied_files.append(str(agreement_seed_target))
    if copy_if_missing(assets_dir / "manual-template.md", manual_seed_target):
        copied_files.append(str(manual_seed_target))

    manifest = build_manifest(
        root,
        system_name,
        system_folder,
        agreement_date=agreement_date,
        manual_revision_date=manual_revision_date,
        technical_style=technical_style,
        technical_highlights=technical_highlights,
    )
    manifest_path = template_dir / "delivery-manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Created output tree for: {system_name}")
    print(f"System folder: {system_folder}")
    print(f"System root: {system_dir}")
    print(f"Manifest: {manifest_path}")
    print(f"Agreement date: {agreement_date}")
    print(f"Manual revision date: {manual_revision_date}")
    print(f"Technical style: {technical_style}")
    print(f"Technical highlights: {', '.join(technical_highlights)}")
    if copied_files:
        print("Copied seed templates:")
        for file_path in copied_files:
            print(f"  {file_path}")
    else:
        print("Seed templates already existed; left them unchanged.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
