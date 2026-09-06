#!/usr/bin/env python3
"""
Local cleanup and quality gate for manual-content.json.

This script intentionally does not call any external AI or API. It applies a
small deterministic cleanup pass, writes a report, and blocks strongly templated
or AI-ish manual copy from reaching the final DOCX builder.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


STRONG_AI_PHRASES = [
    "本系统旨在",
    "赋能",
    "一站式",
    "智能化",
    "数字化转型",
    "全面提升",
    "显著提升",
    "显著提高",
    "高效便捷",
    "全方位",
    "多维度",
    "闭环管理",
    "极大地",
    "从而实现",
    "致力于",
]

PLACEHOLDER_MARKERS = [
    "[请",
    "[待填写",
    "[在此",
    "页面用于展示当前模块的主要功能界面和核心业务内容",
    "面向业务管理、信息维护和流程协同等实际场景",
]

REPLACEMENTS = [
    ("本系统旨在", "本系统用于"),
    ("旨在", "用于"),
    ("赋能", "支持"),
    ("一站式", "统一"),
    ("智能化", ""),
    ("数字化转型", "日常管理"),
    ("全面提升", "提升"),
    ("显著提升", "提升"),
    ("显著提高", "提高"),
    ("高效便捷", "便捷"),
    ("全方位", ""),
    ("多维度", "多角度"),
    ("闭环管理", "流程管理"),
    ("极大地", ""),
    ("极大", ""),
    ("致力于", "用于"),
]


@dataclass
class Finding:
    level: str
    path: str
    message: str


def safe_path_name(value: str) -> str:
    cleaned = re.sub(r'[<>:"/\\\\|?*\x00-\x1f]+', "-", value.strip())
    cleaned = re.sub(r"\s+", "-", cleaned)
    cleaned = re.sub(r"-{2,}", "-", cleaned).strip(" .-")
    return cleaned or "system-app"


def load_manifest(root: Path, system_name: str) -> dict[str, Any]:
    direct = root / safe_path_name(system_name) / "docs" / "Template" / "delivery-manifest.json"
    if direct.exists():
        return json.loads(direct.read_text(encoding="utf-8"))
    matches = list(root.glob("*/docs/Template/delivery-manifest.json"))
    if len(matches) == 1:
        return json.loads(matches[0].read_text(encoding="utf-8"))
    return {}


def find_content_path(root: Path, system_name: str) -> tuple[Path, Path]:
    manifest = load_manifest(root, system_name)
    folder_name = manifest.get("system_folder") or safe_path_name(system_name)
    system_dir = root / folder_name
    template_dir = system_dir / "docs" / "Template"
    candidates = sorted(template_dir.glob("*-manual-content.json"))
    if not candidates:
        raise FileNotFoundError(f"未找到 manual-content.json：{template_dir}")
    return candidates[0], template_dir


def normalize_text(value: str) -> str:
    text = str(value or "").strip()
    for source, target in REPLACEMENTS:
        text = text.replace(source, target)
    text = re.sub(r"通过本系统[，,]?", "", text)
    text = re.sub(r"通过该页面[，,]?", "在该页面，", text)
    text = re.sub(r"通过此页面[，,]?", "在此页面，", text)
    text = re.sub(r"[，,]?从而实现", "，支持", text)
    text = re.sub(r"系统提供了(.{1,24}?)功能", r"系统支持\1", text)
    text = re.sub(r"用户可以方便地", "用户可以", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\s*([，。；：、])\s*", r"\1", text)
    text = re.sub(r"，{2,}", "，", text)
    text = re.sub(r"。{2,}", "。", text)
    text = re.sub(r"，。", "。", text)
    text = re.sub(r"（\s*", "（", text)
    text = re.sub(r"\s*）", "）", text)
    return text.strip(" ，。")


def chinese_char_count(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text or ""))


def collect_quality_findings(path: str, text: str, *, screenshot: bool = False) -> list[Finding]:
    findings: list[Finding] = []
    stripped = str(text or "").strip()
    if not stripped:
        findings.append(Finding("error", path, "内容为空，需要当前 agent 填写自然中文。"))
        return findings

    for marker in PLACEHOLDER_MARKERS:
        if marker in stripped:
            findings.append(Finding("error", path, f"仍包含占位或模板文案：{marker}"))

    for phrase in STRONG_AI_PHRASES:
        if phrase in stripped:
            findings.append(Finding("error", path, f"仍包含 AI 味较重的套话：{phrase}"))

    if re.search(r"通过.{0,24}实现", stripped):
        findings.append(Finding("error", path, "仍包含“通过...实现...”句式，请改成具体动作描述。"))
    if re.search(r"从而.{0,24}提升", stripped):
        findings.append(Finding("warning", path, "包含“从而...提升”句式，建议改成可见结果或用户动作。"))

    char_count = chinese_char_count(stripped)
    if screenshot:
        if char_count < 60:
            findings.append(Finding("warning", path, f"截图说明偏短（{char_count} 个中文字符），建议补充到 80-120 字。"))
        elif char_count > 150:
            findings.append(Finding("warning", path, f"截图说明偏长（{char_count} 个中文字符），建议压缩到 80-120 字。"))
    else:
        if char_count > 240:
            findings.append(Finding("warning", path, f"段落偏长（{char_count} 个中文字符），建议控制在 200 字左右。"))

    starts = re.findall(r"(?:^|。)(系统|页面|该页面|本系统)", stripped)
    if len(starts) >= 3:
        findings.append(Finding("warning", path, "多个句子以“系统/页面”开头，建议调换句式。"))

    return findings


def polish_string_field(container: dict[str, Any], key: str, path: str, changes: list[dict[str, str]]) -> None:
    before = str(container.get(key, "") or "")
    after = normalize_text(before)
    if after != before:
        container[key] = after
        changes.append({"path": path, "before": before, "after": after})


def main() -> int:
    parser = argparse.ArgumentParser(description="Polish and check manual-content.json without external AI APIs.")
    parser.add_argument("--root", default=".", help="Workspace root")
    parser.add_argument("--system-name", required=True, help="Display name of the system")
    parser.add_argument("--check-only", action="store_true", help="Only report issues; do not write cleaned JSON")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    content_path, template_dir = find_content_path(root, args.system_name.strip())
    data = json.loads(content_path.read_text(encoding="utf-8"))

    changes: list[dict[str, str]] = []
    for key in ("short_name", "purpose_text", "function_text", "development_environment_text"):
        polish_string_field(data, key, key, changes)

    for index, item in enumerate(data.get("screenshot_sections", []) or [], start=1):
        if isinstance(item, dict):
            polish_string_field(item, "title", f"screenshot_sections[{index}].title", changes)
            polish_string_field(item, "description_text", f"screenshot_sections[{index}].description_text", changes)

    findings: list[Finding] = []
    for key in ("short_name", "purpose_text", "function_text", "development_environment_text"):
        findings.extend(collect_quality_findings(key, str(data.get(key, "") or "")))

    for index, item in enumerate(data.get("screenshot_sections", []) or [], start=1):
        if not isinstance(item, dict):
            findings.append(Finding("error", f"screenshot_sections[{index}]", "截图条目不是对象。"))
            continue
        findings.extend(
            collect_quality_findings(
                f"screenshot_sections[{index}].title",
                str(item.get("title", "") or ""),
            )
        )
        findings.extend(
            collect_quality_findings(
                f"screenshot_sections[{index}].description_text",
                str(item.get("description_text", "") or ""),
                screenshot=True,
            )
        )

    report = {
        "content_path": str(content_path),
        "changed_fields": changes,
        "errors": [finding.__dict__ for finding in findings if finding.level == "error"],
        "warnings": [finding.__dict__ for finding in findings if finding.level == "warning"],
        "external_api_used": False,
    }

    report_path = template_dir / "manual-humanize-report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    if changes and not args.check_only:
        content_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    for finding in findings:
        print(f"{finding.level.upper()}: {finding.path}: {finding.message}")
    print(f"Manual humanize report: {report_path}")
    if changes and not args.check_only:
        print(f"Polished fields written back to: {content_path}")
    elif changes:
        print("Check-only mode: cleaned text was not written.")

    return 1 if any(finding.level == "error" for finding in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
