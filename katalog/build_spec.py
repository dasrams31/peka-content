#!/usr/bin/env python3
"""Build reel-spec.json for the Peka catalog reel from prices.json.

Usage: build_spec.py <edition_dir>
Reads ../prices.json (next to this script's folder), writes
<edition_dir>/reel-spec.json. Never invents prices: every field comes
from prices.json.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    edition_dir = sys.argv[1]
    with open(os.path.join(HERE, "prices.json"), encoding="utf-8") as fh:
        prices = json.load(fh)
    products = prices["products"]
    assert len(products) == 5, "catalog reel needs exactly 5 products"
    spec = {
        "date": prices["date_label"],
        "products": [
            {
                "sec": p["sec"],
                "name": p["name"],
                "dur": p["dur"],
                "price": p["price"],
                **({"note": p["note"]} if p.get("note") else {}),
            }
            for p in products
        ],
    }
    os.makedirs(edition_dir, exist_ok=True)
    out = os.path.join(edition_dir, "reel-spec.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(spec, fh, ensure_ascii=False, indent=2)
    print(f"wrote {out}")


main()
