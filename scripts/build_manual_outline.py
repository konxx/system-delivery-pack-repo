#!/usr/bin/env python3
"""
Create a markdown outline for the system manual from available screenshots.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from document_defaults import load_manual_author

REVISION_DATE = "2026-6-15"
DATABASE_SOFTWARE = "PostgreSQL"


def load_manifest(root: Path, system_name: str) -> dict:
    if system_name.strip():
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


def normalize_screenshot_key(path: Path) -> str:
    stem = path.stem.lower().replace("_", "-")
    stem = re.sub(r"^\d+[-\s]*", "", stem)
    stem = re.sub(r"-{2,}", "-", stem).strip("- ")
    return stem


def label_from_filename(path: Path) -> str:
    key = normalize_screenshot_key(path)
    whole_map = {
        "login": "登录页面",
        "signin": "登录页面",
        "sign-in": "登录页面",
        "dashboard": "控制台页面",
        "overview": "总览页面",
        "home": "首页页面",
        "student-detail": "学生详情页面",
        "product-detail": "商品详情页面",
        "order-detail": "订单详情页面",
        "user-detail": "用户详情页面",
    }
    token_map = {
        "student": "学生",
        "students": "学生",
        "teacher": "教师",
        "teachers": "教师",
        "course": "课程",
        "courses": "课程",
        "class": "班级",
        "classes": "班级",
        "grade": "成绩",
        "grades": "成绩",
        "attendance": "考勤",
        "dashboard": "控制台",
        "overview": "总览",
        "home": "首页",
        "report": "报表",
        "reports": "报表",
        "setting": "系统设置",
        "settings": "系统设置",
        "user": "用户",
        "users": "用户管理",
        "role": "角色",
        "roles": "角色权限",
        "permission": "权限",
        "permissions": "权限",
        "workflow": "流程",
        "approval": "审批",
        "product": "商品",
        "products": "商品",
        "inventory": "库存",
        "order": "订单",
        "orders": "订单",
        "customer": "客户",
        "customers": "客户",
        "finance": "财务",
        "payment": "支付",
        "monitor": "监控",
        "audit": "审计",
        "message": "消息",
        "messages": "消息",
        "notification": "通知",
        "notifications": "通知",
        "profile": "资料",
        "detail": "详情",
        "details": "详情",
        "list": "列表",
        "form": "表单",
        "create": "新建",
        "edit": "编辑",
        "analytics": "分析",
        "analysis": "分析",
        "search": "检索",
        "schedule": "日程",
        "exam": "考试",
        "library": "图书馆",
        "resource": "资源",
        "resources": "资源",
    }
    if key in whole_map:
        return whole_map[key]
    if re.search(r"[\u4e00-\u9fff]", path.stem):
        return path.stem if path.stem.endswith("页面") else f"{path.stem}页面"
    parts = [token_map.get(part) for part in key.split("-") if part]
    parts = [part for part in parts if part]
    if not parts:
        return "功能页面"
    title = "".join(parts)
    return title if title.endswith("页面") else f"{title}页面"


def safe_path_name(value: str) -> str:
    cleaned = re.sub(r'[<>:"/\\\\|?*\x00-\x1f]+', "-", value.strip())
    cleaned = re.sub(r"\s+", "-", cleaned)
    cleaned = re.sub(r"-{2,}", "-", cleaned).strip(" .-")
    return cleaned or "system-app"


def display_system_name(system_name: str) -> str:
    name = system_name.strip()
    return name if name.endswith("系统") else f"{name}系统"


def derive_short_name(system_name: str) -> str:
    name = display_system_name(system_name)
    replacements = [
        ("高校学生信息管理系统", "高校管理系统"),
        ("学生信息管理系统", "学生管理系统"),
        ("信息管理系统", "管理系统"),
        ("业务管理系统", "管理系统"),
        ("服务管理系统", "管理系统"),
        ("平台管理系统", "管理系统"),
    ]
    for source, target in replacements:
        if source in name:
            shortened = name.replace(source, target)
            if shortened != name:
                return shortened
    return name


def infer_modules(system_dir: Path) -> list[str]:
    modules: list[str] = []
    seen: set[str] = set()

    module_plan_file = system_dir / "docs" / "Template" / "module-plan.md"
    if module_plan_file.exists():
        text = module_plan_file.read_text(encoding="utf-8", errors="ignore")
        for line in text.splitlines():
            match = re.match(r"^\s*(?:\d+[\.\、]\s*|[-*]\s+)(.+?)\s*$", line)
            if match:
                name = match.group(1).strip()
                if name and name not in seen:
                    seen.add(name)
                    modules.append(name)

    frontend_modules_dir = system_dir / "code" / "frontend" / "src" / "modules"
    if frontend_modules_dir.exists():
        for child in sorted(frontend_modules_dir.iterdir()):
            if child.is_dir():
                name = child.name.strip()
                if name and name not in seen:
                    seen.add(name)
                    modules.append(name)

    backend_router_dir = system_dir / "code" / "backend" / "app" / "routers"
    if backend_router_dir.exists():
        for child in sorted(backend_router_dir.glob("*.py")):
            if child.stem == "__init__":
                continue
            name = child.stem.strip()
            if name and name not in seen:
                seen.add(name)
                modules.append(name)

    if not modules:
        modules = ["仪表盘", "基础资料", "核心业务管理", "流程审批", "统计报表", "系统设置"]

    return modules[:10]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a markdown outline for the DOCX manual based on screenshots in <system>/photos.",
    )
    parser.add_argument("--root", default=".", help="Workspace root")
    parser.add_argument("--system-name", default="", help="Display name of the system")
    parser.add_argument("--revision-date", default="", help="Override the manual revision date")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    requested_system_name = args.system_name.strip()
    manifest = load_manifest(root, requested_system_name)
    system_name = requested_system_name or manifest.get("system_name") or "业务系统"
    title_name = display_system_name(system_name)
    short_name = derive_short_name(system_name)
    preferred_date = manifest.get("delivery_preferences", {}).get("manual_revision_date", "")
    revision_date = args.revision_date.strip() or preferred_date or REVISION_DATE
    author = load_manual_author()

    safe_name = manifest.get("system_folder") or safe_path_name(system_name)
    system_dir = root / safe_name
    photos_dir = system_dir / "photos"
    template_dir = system_dir / "docs" / "Template"
    template_dir.mkdir(parents=True, exist_ok=True)

    screenshots = sorted(
        [
            path
            for path in photos_dir.glob("*")
            if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
        ]
    )
    modules = infer_modules(system_dir)

    manual_content = {
        "system_name": title_name,
        "short_name": "",
        "version": "V1.0",
        "author": author,
        "revision_date": revision_date,
        "purpose_text": "",
        "function_text": "",
        "development_environment_text": "",
        "modules": modules,
        "screenshot_sections": [],
    }

    sections = [
        f"{title_name}[简称：{{SYSTEM_SHORT_NAME}}]V1.0",
        "",
        "产品说明书",
        "",
        "\\newpage",
        "",
        "## 修订记录",
        "",
        "| 版本号 | 生成日期 | 作者 | 修订内容 |",
        "| --- | --- | --- | --- |",
        f"| V1.0 | {revision_date} | {author} | 初始版本 |",
        "",
        "\\newpage",
        "",
        "## 一、软件介绍",
        "",
        f"软件名称：{title_name}",
        "",
        f"简称：{{SYSTEM_SHORT_NAME}}",
        "",
        "版本号：V1.0",
        "",
        "软件类别：应用软件",
        "",
        f"著作权人：{author}",
        "",
        "\\newpage",
        "",
        "## 二、软件用途",
        "",
        "[请基于系统模块生成软件用途描述，控制在 200 字以内]",
        "",
        "\\newpage",
        "",
        "## 三、软件功能",
        "",
        "[请基于系统模块生成软件功能描述，控制在 200 字以内]",
        "",
        "\\newpage",
        "",
        "## 四、运行环境",
        "",
        "### 4.1 硬件要求",
        "",
        "| 类型 | 基本要求 |",
        "| --- | --- |",
        "| 服务器端 | CPU 8核1.60GHz，内存8G，硬盘剩余空间10G |",
        "",
        "### 4.2 软件环境",
        "",
        "| 名称 | 基本环境 |",
        "| --- | --- |",
        "| 操作系统 | Windows 10 64位 |",
        f"| 数据库软件 | {DATABASE_SOFTWARE} |",
        "| 开发软件 | Opencode，Claude Code，Codex，IntelliJ IDEA，Navicat 16 |",
        "| 开发语言 | [按全栈代码如实填写并补版本号，例如 Python 3.10、TypeScript 5.0] |",
        "",
        "\\newpage",
        "",
        "### 4.3 软件开发环境",
        "",
        f"本软件分为前端页面和后端业务逻辑，其中前端页面使用[前端语言及版本]进行开发，后端业务逻辑使用[后端语言及版本]进行开发，数据库使用{DATABASE_SOFTWARE}，数据库管理采用Navicat 16，整个系统使用IntelliJ IDEA环境进行开发。开发界面如图4-1所示。",
        "",
        "[在此处粘贴开发界面图片]",
        "",
        "图4-1 软件开发界面",
        "",
        "\\newpage",
        "",
        "## 五、软件使用",
        "",
    ]

    if screenshots:
        for index, screenshot in enumerate(screenshots, start=1):
            title = label_from_filename(screenshot)
            manual_content["screenshot_sections"].append(
                {
                    "index": index,
                    "image": screenshot.name,
                    "title": "",
                    "title_options": [title],
                    "description_text": "",
                }
            )
            sections.extend(
                [
                    "",
                    f"### 5.{index} [待填写页面名称]",
                    "",
                    f"[插入截图：{screenshot.name}]",
                    "",
                    f"图5-{index} [待填写页面名称]",
                    "",
                    "[请用80-120字中文自然语言描述该页面，写清页面用途和一两项主要操作，避免机械模板化。]",
                    "",
                    "\\newpage",
                ]
            )
    else:
        sections.extend(
            [
                "",
                "### 5.1 页面说明待补充",
                "",
                "当前尚未发现截图文件。先完成前端演示与 Playwright 截图，再补充本章节内容。",
            ]
        )

    output_path = template_dir / f"{safe_name}-manual-outline.md"
    output_path.write_text("\n".join(sections), encoding="utf-8")
    content_path = template_dir / f"{safe_name}-manual-content.json"
    content_path.write_text(json.dumps(manual_content, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Manual outline written to: {output_path}")
    print(f"Manual content scaffold written to: {content_path}")
    print(f"Detected screenshots: {len(screenshots)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
