#!/usr/bin/env python3
"""Frame-by-frame renderer for reel-v2 (voiceover-led reels).

Same deterministic pattern as the proven HM reel builder: every frame
is produced by window.renderAt(t) after window.buildScene(spec), so the
output does not depend on wall-clock animation timing.

Usage:
  ~/workspace/megumi/venv/bin/python render.py <render-spec.json> [frames_dir] [fps] [scale]
  ~/workspace/megumi/venv/bin/python render.py <render-spec.json> --still <t> <out.jpg>

Scale 1.0 = 1080x1920, 2.0 = true 4K 2160x3840 (rounded to even dims).
Duration comes from the spec ("total" seconds, set by build_reel.py
from the voiceover timeline).
"""
import asyncio
import json
import os
import sys

from playwright.async_api import async_playwright

BASE = os.path.dirname(os.path.abspath(__file__))
CHROME = "/home/hatch/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome"


async def open_page(spec, scale):
    p = await async_playwright().start()
    browser = await p.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])
    vw = int(round(1080 * scale) / 2) * 2
    vh = int(round(1920 * scale) / 2) * 2
    page = await browser.new_page(viewport={"width": vw, "height": vh})
    await page.goto("file://" + os.path.join(BASE, "scene.html"))
    await page.evaluate(
        f"document.getElementById('stage').style.transform = 'scale({scale})';"
        "document.getElementById('stage').style.transformOrigin = '0 0';"
    )
    await page.evaluate("spec => window.buildScene(spec)", spec)
    await page.wait_for_timeout(800)
    return p, browser, page


async def render_frames(spec_path, out_dir, fps, scale):
    with open(spec_path, encoding="utf-8") as fh:
        spec = json.load(fh)
    dur = float(spec["total"])
    os.makedirs(out_dir, exist_ok=True)
    p, browser, page = await open_page(spec, scale)
    n = int(fps * dur)
    for i in range(n):
        path = os.path.join(out_dir, f"f{i:04d}.png")
        if os.path.exists(path):
            continue  # resume: frame already rendered, skip it
        await page.evaluate(f"window.renderAt({i / fps})")
        await page.screenshot(path=path)
        if i % 120 == 0:
            print(f"frame {i}/{n}", flush=True)
    await browser.close()
    await p.stop()
    print(f"done {n} frames -> {out_dir}")


async def render_still(spec_path, t, out_path, scale):
    with open(spec_path, encoding="utf-8") as fh:
        spec = json.load(fh)
    p, browser, page = await open_page(spec, scale)
    await page.evaluate(f"window.renderAt({t})")
    await page.wait_for_timeout(200)
    if out_path.lower().endswith((".jpg", ".jpeg")):
        await page.screenshot(path=out_path, type="jpeg", quality=92)
    else:
        await page.screenshot(path=out_path)
    await browser.close()
    await p.stop()
    print(f"still t={t}s -> {out_path}")


async def main():
    spec_path = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] == "--still":
        t = float(sys.argv[3])
        out_path = sys.argv[4]
        scale = float(sys.argv[5]) if len(sys.argv) > 5 else 2.0
        await render_still(spec_path, t, out_path, scale)
        return
    out_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(BASE, "frames")
    fps = int(sys.argv[3]) if len(sys.argv) > 3 else 24
    scale = float(sys.argv[4]) if len(sys.argv) > 4 else 2.0
    await render_frames(spec_path, out_dir, fps, scale)


asyncio.run(main())
