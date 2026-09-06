#!/usr/bin/env python3
"""Capture demo routes with the machine-level Python Playwright runtime."""

from __future__ import annotations

import argparse
from pathlib import Path


def parse_page_spec(raw: str) -> tuple[str, str]:
    if "=" not in raw:
        raise argparse.ArgumentTypeError("Use <filename>=<route>, for example 01-login.png=/login")
    filename, route = raw.split("=", 1)
    filename = Path(filename.strip()).name
    if not filename:
        raise argparse.ArgumentTypeError("Screenshot filename cannot be empty")
    if Path(filename).suffix.lower() not in {".png", ".jpg", ".jpeg"}:
        raise argparse.ArgumentTypeError("Screenshot filename must end in .png, .jpg, or .jpeg")
    return filename, route.strip()


def route_url(base_url: str, route: str) -> str:
    if route.startswith(("http://", "https://")):
        return route
    if not route:
        return base_url
    return f"{base_url.rstrip('/')}/{route.lstrip('/')}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Capture frontend routes with the already-installed local Python Playwright runtime.",
    )
    parser.add_argument("--base-url", required=True, help="Validated preview server URL")
    parser.add_argument("--output-dir", required=True, help="Screenshot output directory")
    parser.add_argument(
        "--page",
        action="append",
        type=parse_page_spec,
        required=True,
        help="Repeatable <filename>=<route> mapping",
    )
    parser.add_argument("--width", type=int, default=1440, help="Viewport width")
    parser.add_argument("--height", type=int, default=1000, help="Viewport height")
    parser.add_argument("--wait-ms", type=int, default=800, help="Extra settle time after navigation")
    parser.add_argument("--full-page", action="store_true", help="Capture the full scrollable page")
    args = parser.parse_args()

    try:
        from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        print(f"ERROR: local Python Playwright is unavailable: {exc}")
        print("Run scripts/verify_local_playwright.py and repair the machine-level prerequisite outside this delivery run.")
        return 1

    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": args.width, "height": args.height})
        page = context.new_page()

        for filename, route in args.page:
            url = route_url(args.base_url, route)
            page.goto(url, wait_until="domcontentloaded")
            try:
                page.wait_for_load_state("networkidle", timeout=5000)
            except PlaywrightTimeoutError:
                pass
            page.wait_for_timeout(max(0, args.wait_ms))
            target = output_dir / filename
            page.screenshot(path=str(target), full_page=args.full_page)
            print(f"Captured: {target} <- {url}")

        context.close()
        browser.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
