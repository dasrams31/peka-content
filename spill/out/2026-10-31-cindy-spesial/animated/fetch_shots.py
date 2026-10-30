#!/usr/bin/env python3
"""Fetch each repo's GitHub social card (og:image) for the reel spec.

Usage: fetch_shots.py <spec.json> <shots_dir>
Downloads the og:image of every repo in the spec into <shots_dir> as
<owner>-<repo>.png and writes the absolute path back into the spec
as each repo's "shot" field. Fails loudly if any download fails, so
the reel step never renders with a missing screenshot.
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from urllib.parse import urlparse

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from spill_repo_carousel import enrich, github_card_image

UA = {"User-Agent": "peka-spill-carousel"}


def _download(url, timeout=20, attempts=4):
    """Download with backoff on 429/5xx (opengraph rate-limits bursts)."""
    delay = 15
    for i in range(attempts):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except urllib.error.HTTPError as exc:
            if exc.code in (429, 500, 502, 503) and i < attempts - 1:
                print(f"retry {url} after HTTP {exc.code} in {delay}s")
                time.sleep(delay)
                delay *= 2
                continue
            raise
    raise SystemExit(f"download failed: {url}")


def main():
    spec_path, shots_dir = sys.argv[1], sys.argv[2]
    os.makedirs(shots_dir, exist_ok=True)
    import datetime
    cache_dir = f"/tmp/spill-shots/{datetime.date.today().isoformat()}"
    os.makedirs(cache_dir, exist_ok=True)
    with open(spec_path, encoding="utf-8") as fh:
        spec = json.load(fh)
    for r in spec["repos"]:
        full = r["name"]
        out = os.path.join(shots_dir, full.replace("/", "-") + ".png")
        if os.path.exists(out) and os.path.getsize(out) > 0:
            r["shot"] = out
            print(f"shot (cached): {full} -> {out}")
            continue
        cached = os.path.join(cache_dir, full.replace("/", "-") + ".png")
        if os.path.exists(cached) and os.path.getsize(cached) > 0:
            import shutil
            shutil.copyfile(cached, out)
            r["shot"] = out
            print(f"shot (day cache): {full} -> {out}")
            continue
        html = _download(f"https://github.com/{full}").decode("utf-8", "replace")
        m = re.search(r'<meta property="og:image" content="([^"]+)"', html)
        og_url = m.group(1) if m else None
        if og_url and urlparse(og_url).hostname == "opengraph.githubassets.com":
            data = _download(og_url)
            with open(out, "wb") as fh:
                fh.write(data)
            try:
                with open(cached, "wb") as fh:
                    fh.write(data)
            except Exception:
                pass
            r["shot"] = out
            print(f"shot: {full} -> {out} ({len(data)} bytes)")
        else:
            # Custom upload (repository-images host) or no og image:
            # draw the GitHub-default-card look from API data instead.
            en = enrich({"name": full, "stars": r.get("stars", ""),
                         "desc": "", "install": "x"}, fetch_og=False)
            card = github_card_image({"name": full}, en)
            card.save(out)
            try:
                card.save(cached)
            except Exception:
                pass
            r["shot"] = out
            print(f"shot (drawn card): {full} -> {out}")
    with open(spec_path, "w", encoding="utf-8") as fh:
        json.dump(spec, fh, ensure_ascii=False, indent=2)
    print("spec updated:", spec_path)


if __name__ == "__main__":
    main()
