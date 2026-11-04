"""Screenshot the Piko 3D viewer (local vendor build) in all 4 states."""
import os
import subprocess
import time

from playwright.sync_api import sync_playwright

ROOT = os.path.expanduser("~/workspace/peka-content/piko/3d")
SHOTS = [
    ("idle", "0"),
    ("listening", "0"),
    ("speaking", "0"),
    ("roast", "0"),
    ("roast-hero", "0.6"),
]

srv = subprocess.Popen(
    ["python3", "-m", "http.server", "8901", "--bind", "127.0.0.1"],
    cwd=ROOT,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
time.sleep(1.0)
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=os.path.expanduser(
                "~/.cache/ms-playwright/chromium_headless_shell-1243/"
                "chrome-headless-shell-linux64/chrome-headless-shell"
            ),
            args=[
                "--no-sandbox",
                "--use-gl=angle",
                "--use-angle=swiftshader",
                "--enable-unsafe-swiftshader",
            ],
        )
        page = browser.new_page(viewport={"width": 1080, "height": 1080})
        for name, ry in SHOTS:
            state = name.replace("-hero", "")
            url = f"http://127.0.0.1:8901/shot.html?state={state}&still=1&ry={ry}"
            page.goto(url, wait_until="networkidle", timeout=30000)
            page.wait_for_function("window.__pikoReady === true", timeout=30000)
            page.wait_for_timeout(600)
            out = os.path.join(ROOT, "shots", f"piko-3d-{name}.png")
            page.screenshot(path=out)
            print("shot", name, os.path.getsize(out))
        browser.close()
finally:
    srv.terminate()
print("done")
