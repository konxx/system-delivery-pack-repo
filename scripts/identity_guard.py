#!/usr/bin/env python3
"""Block document-only personal identity data from generated source code."""

from __future__ import annotations

from pathlib import Path

from document_defaults import load_agreement_party_a


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
MAX_TEXT_FILE_BYTES = 5 * 1024 * 1024


def _protected_variants() -> tuple[str, ...]:
    protected_name, _ = load_agreement_party_a()
    unicode_escape = "".join(f"\\u{ord(char):04x}" for char in protected_name)
    html_decimal = "".join(f"&#{ord(char)};" for char in protected_name)
    return protected_name, unicode_escape, html_decimal


def _contains_protected_value(path: Path, variants: tuple[str, ...]) -> bool:
    if path.stat().st_size > MAX_TEXT_FILE_BYTES:
        return False

    raw = path.read_bytes()
    if b"\x00" in raw:
        return False
    text = raw.decode("utf-8", errors="ignore").lower()
    return any(variant.lower() in text for variant in variants)


def find_identity_leaks(root: Path) -> list[Path]:
    if not root.exists():
        return []

    variants = _protected_variants()
    leaks: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file() or any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        relative_name = path.relative_to(root).as_posix().lower()
        if any(variant.lower() in relative_name for variant in variants) or _contains_protected_value(path, variants):
            leaks.append(path)
    return leaks
