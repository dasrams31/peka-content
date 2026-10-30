#!/usr/bin/env python3
"""Screenshot the BLUEPRINT reel cover scene at 2160x3840 (scale 2)."""
import os
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))

with sync_playwright() as p:
    b = p.chromium.launch(
        executable_path="/home/hatch/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome",
        args=["--no-sandbox"],
    )
    pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=2)
    pg.goto("file://" + HERE + "/scene.html")
    pg.wait_for_timeout(700)
    pg.screenshot(path=HERE + "/blueprint-reel-scene.png")
    b.close()
print("scene OK")
