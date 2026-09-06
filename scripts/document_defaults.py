#!/usr/bin/env python3
"""Read document-only identity defaults from the bundled templates."""

from __future__ import annotations

import re
from pathlib import Path


def _skill_dir() -> Path:
    return Path(__file__).resolve().parent.parent


def _read_labeled_value(path: Path, label: str) -> str:
    text = path.read_text(encoding="utf-8")
    pattern = rf"^{re.escape(label)}[：:]\s*(.+?)\s*$"
    match = re.search(pattern, text, flags=re.MULTILINE)
    if not match:
        raise RuntimeError(f"Missing {label} value in document template: {path}")
    return match.group(1).strip()


def load_agreement_party_a() -> tuple[str, str]:
    template = _skill_dir() / "assets" / "agreement-template.md"
    return (
        _read_labeled_value(template, "甲方"),
        _read_labeled_value(template, "身份证号"),
    )


def load_manual_author() -> str:
    template = _skill_dir() / "assets" / "manual-template.md"
    return _read_labeled_value(template, "著作权人")
