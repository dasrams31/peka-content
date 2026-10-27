#!/usr/bin/env python3
"""Render the window-style SPILL reel demo frame by frame (Playwright).

Same deterministic approach as ../render.py, but loads scene-window.html
and accepts a demo spec with any number of repos.
Usage: render-window.py <spec.json> <out_dir> [fps] [duration] [scale]
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
    out_dir = sys.argv[2]
    fps = int(sys.argv[3]) if len(sys.argv) > 3 else 24
    dur = float(sys.argv[4]) if len(sys.argv) > 4 else 15.0
    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 1.0
    with open(spec_path, encoding="utf-8") as fh:
        spec = json.load(fh)
    for r in spec["repos"]:
        assert len(r["short"]) <= 110, f"short desc too long: {r['name']}"
    vw = int(round(1080 * scale) / 2) * 2
    vh = int(round(1920 * scale) / 2) * 2
    os.makedirs(out_dir, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])
        page = await browser.new_page(viewport={"width": vw, "height": vh})
        await page.goto("file://" + os.path.join(BASE, "scene-window.html"))
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
