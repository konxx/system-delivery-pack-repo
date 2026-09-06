#!/usr/bin/env python3
"""Verify that the machine-level Python Playwright and Chromium are ready."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version


def main() -> int:
    try:
        playwright_version = version("playwright")
        from playwright.sync_api import sync_playwright
    except (ImportError, PackageNotFoundError) as exc:
        print(f"ERROR: local Python Playwright is unavailable: {exc}")
        return 1

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            page.set_content("<title>playwright-ready</title><main>ready</main>")
            title = page.title()
            browser.close()
    except Exception as exc:
        print(f"ERROR: local Playwright Chromium could not start: {exc}")
        return 1

    print(f"Local Playwright: {playwright_version}")
    print(f"Chromium smoke test: {title}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
