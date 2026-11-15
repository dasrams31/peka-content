#!/usr/bin/env python3
"""Render the Peka-design catalog reel frame by frame with Playwright.

Deterministic: every frame is produced by window.renderAt(t) after
window.buildScene(spec). Duration follows the product count: 3s cover
+ 5s per 3-product chunk + 3s closing, unless overridden by argv[4].
Scale 2.0 = true 4K 2160x3840.
Usage: render.py <spec.json> [out_dir] [fps] [duration] [scale]
"""
import asyncio
import json
import math
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
    assert len(spec["products"]) >= 1, "catalog reel needs at least 1 product"
    for p in spec["products"]:
        assert p.get("name") and p.get("dur") and p.get("price") and p.get("sec"), \
            f"incomplete product: {p}"
    if len(sys.argv) > 4:
        dur = float(sys.argv[4])
    else:
        dur = 3 + 5 * math.ceil(len(spec["products"]) / 3) + 3
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
