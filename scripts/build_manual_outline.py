#!/usr/bin/env python3
"""
Create a markdown outline for the system manual from available screenshots.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def load_manifest(root: Path) -> dict:
    manifest_path = root / "outputs" / "Template" / "delivery-manifest.json"
    if not manifest_path.exists():
        return {}
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def label_from_filename(path: Path) -> str:
    stem = path.stem.replace("_", " ").replace("-", " ")
    return " ".join(part for part in stem.split() if part).title() or path.stem


def safe_path_name(value: str) -> str:
    cleaned = re.sub(r'[<>:"/\\\\|?*\x00-\x1f]+', "-", value.strip())
    cleaned = re.sub(r"\s+", "-", cleaned)
    cleaned = re.sub(r"-{2,}", "-", cleaned).strip(" .-")
    return cleaned or "system-app"


def display_system_name(system_name: str) -> str:
    name = system_name.strip()
    return name if name.endswith("系统") else f"{name}系统"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a markdown outline for the DOCX manual based on screenshots in outputs/photos.",
    )
    parser.add_argument("--root", default=".", help="Workspace root")
    parser.add_argument("--system-name", default="", help="Display name of the system")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    manifest = load_manifest(root)
    system_name = args.system_name.strip() or manifest.get("system_name") or "业务系统"
    title_name = display_system_name(system_name)

    photos_dir = root / "outputs" / "photos"
    template_dir = root / "outputs" / "Template"
    template_dir.mkdir(parents=True, exist_ok=True)

    screenshots = sorted(
        [
            path
            for path in photos_dir.glob("*")
            if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
        ]
    )

    sections = [
        f"# {title_name}说明书",
        "",
        "## 1. 文档说明",
        f"- 文档对象: {title_name}",
        "- 文档用途: 说明主要页面、业务流程与操作方式。",
        "- 文档来源: 基于当前交付包中的前端演示页面与截图整理。",
        "",
        "## 2. 系统概览",
        "- 说明系统定位、适用角色、核心模块与使用价值。",
        "",
        "## 3. 角色与权限",
        "- 列出主要角色，并说明每类角色的核心职责。",
        "",
        "## 4. 主要页面说明",
    ]

    if screenshots:
        for index, screenshot in enumerate(screenshots, start=1):
            sections.extend(
                [
                    "",
                    f"### 4.{index} {label_from_filename(screenshot)}",
                    f"- 截图文件: {screenshot.name}",
                    "- 页面用途: [补充该页面承担的业务目标]",
                    "- 核心信息: [补充页面中的关键数据或状态]",
                    "- 主要操作: [补充用户在该页面可执行的动作]",
                ]
            )
    else:
        sections.extend(
            [
                "",
                "### 4.1 页面说明待补充",
                "- 当前尚未发现截图文件。先完成前端演示与 Playwright 截图，再补全文档。",
            ]
        )

    sections.extend(
        [
            "",
            "## 5. 关键业务流程",
            "- 按用户实际演示流程说明从进入系统到完成业务的主要步骤。",
            "",
            "## 6. 数据与报表说明",
            "- 总结关键字段、统计看板、列表筛选、导出与审批等能力。",
            "",
            "## 7. 使用注意事项",
            "- 说明演示数据、权限前提、常见限制与已知假设。",
            "",
        ]
    )

    safe_name = manifest.get("system_folder") or safe_path_name(system_name)
    output_path = template_dir / f"{safe_name}-manual-outline.md"
    output_path.write_text("\n".join(sections), encoding="utf-8")

    print(f"Manual outline written to: {output_path}")
    print(f"Detected screenshots: {len(screenshots)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
