#!/usr/bin/env python3
"""Render a LOG PEKA animated reel frame by frame with Playwright.

4 scenes: cover / numbers / findings / question + follow.
Deterministic: every frame is produced by window.renderAt(t) after
window.buildScene(spec).
Usage: render.py <spec.json> [out_dir] [fps] [duration] [scale]
Scale 1.0 = 1080x1920, 2.0 = true 4K 2160x3840 (rounded to even dims).
Duration default = 4 + 4 + 4 + 3 = 15 seconds.
"""
import asyncio
import json
import os
import sys

from playwright.async_api import async_playwright

BASE = os.path.dirname(os.path.abspath(__file__))
CHROME = "/home/hatch/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome"


async def main():
    spec_path = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(BASE, "frames")
    fps = int(sys.argv[3]) if len(sys.argv) > 3 else 24
    with open(spec_path, encoding="utf-8") as fh:
        spec = json.load(fh)
    assert isinstance(spec["day"], int) and spec["day"] > 0, "day must be a positive int"
    assert len(spec["stats"]) == 3, "LOG PEKA reel needs exactly 3 stats"
    assert len(spec["findings"]) == 3, "LOG PEKA reel needs exactly 3 findings"
    assert spec.get("question"), "missing question"
    assert spec.get("title"), "missing title"
    assert spec.get("hypothesis"), "missing hypothesis"
    dur = float(sys.argv[4]) if len(sys.argv) > 4 else 15
    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 1.0
    vw = int(round(1080 * scale) / 2) * 2
    vh = int(round(1920 * scale) / 2) * 2
    os.makedirs(out_dir, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])
        page = await browser.new_page(viewport={"width": vw, "height": vh})
        await page.goto("file://" + os.path.join(BASE, "scene.html"))
        await page.evaluate(
            f"document.getElementById('stage').style.transform = 'scale({scale})';"
            "document.getElementById('stage').style.transformOrigin = '0 0';"
        )
        await page.evaluate("spec => window.buildScene(spec)", spec)
        await page.wait_for_timeout(800)
        n = int(fps * dur)
        for i in range(n):
            await page.evaluate(f"window.renderAt({i / fps})")
            await page.screenshot(path=os.path.join(out_dir, f"f{i:04d}.png"))
            if i % 60 == 0:
                print(f"frame {i}/{n}", flush=True)
        await browser.close()
    print(f"done {n} frames -> {out_dir}")


asyncio.run(main())
