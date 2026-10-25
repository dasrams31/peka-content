#!/usr/bin/env python3
"""Render an animated tools-launch reel frame by frame with Playwright.

Deterministic: every frame is produced by window.renderAt(t), so the
output does not depend on wall-clock animation timing.
Usage: render.py [out_dir] [fps] [duration] [scale]
Scale 1.0 = 1080x1920, 1.3333 = true 2K 1440x2560 (rounded to even dims).
"""
import asyncio
import os
import sys

from playwright.async_api import async_playwright

BASE = os.path.dirname(os.path.abspath(__file__))
CHROME = "/home/hatch/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome"


async def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, "frames")
    fps = int(sys.argv[2]) if len(sys.argv) > 2 else 24
    dur = float(sys.argv[3]) if len(sys.argv) > 3 else 15.0
    scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
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
